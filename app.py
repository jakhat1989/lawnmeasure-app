import os, hmac, math, re, html, time, logging
from io import BytesIO
from functools import wraps
import requests
from flask import Flask, jsonify, request, session, send_file, send_from_directory
from shapely.geometry import shape
from shapely.ops import transform, unary_union

app=Flask(__name__,static_folder="static")
app.config.update(SECRET_KEY=os.getenv("APP_SECRET_KEY","local-development-only"),
 SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE="Lax",
 SESSION_COOKIE_SECURE=os.getenv("RENDER","").lower()=="true",
 PERMANENT_SESSION_LIFETIME=1209600,MAX_CONTENT_LENGTH=512000)
http=requests.Session()
http.headers["User-Agent"]="LawnQuoteOwner/1.0"
failed={}
R=6378137.0; SFT=10.76391041671
CENSUS="https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
NAIP="https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer/exportImage"

def err(message,status=400):return jsonify(error=message),status
def authorized(fn):
 @wraps(fn)
 def wrapped(*args,**kwargs):
  if not session.get("owner"):return err("Sign in to continue.",401)
  return fn(*args,**kwargs)
 return wrapped
def configured():return bool(os.getenv("RESEND_API_KEY") and os.getenv("RESEND_FROM_EMAIL"))
def public_satellite_token():
 # ArcGIS Location Platform browser API key: restrict to the site's HTTPS referrer.
 # It is an app access token (not an admin or personal account secret).
 token=os.getenv("ARCGIS_API_KEY","").strip()
 return token if 24<=len(token)<=2200 and " " not in token else ""
@app.get("/")
def home():return send_from_directory("static","index.html")
@app.get("/health")
def health():return jsonify(ok=True,product="LawnQuote Owner")
@app.get("/api/status")
def status():return jsonify(authenticated=bool(session.get("owner")),
  email_configured=configured(),satellite_configured=bool(public_satellite_token()))
@app.get("/api/map-config")
@authorized
def map_config():
 response=jsonify(provider="arcgis" if public_satellite_token() else "government_fallback",
                  public_token=public_satellite_token(),
                  provider_configured=bool(public_satellite_token()),
                  max_zoom=21)
 response.headers["Cache-Control"]="private,no-store"
 return response

@app.post("/api/login")
def login():
 code=os.getenv("OWNER_ACCESS_CODE")
 if not code:return err("Owner access code is not configured.",503)
 ip=request.remote_addr or "-"
 now=time.time()
 recent=[t for t in failed.get(ip,[]) if now-t<900]
 if len(recent)>=12:return err("Too many attempts. Try again in 15 minutes.",429)
 value=str((request.get_json(silent=True) or {}).get("code",""))
 if not hmac.compare_digest(value,code):
  recent.append(now);failed[ip]=recent
  return err("Incorrect access code.",401)
 failed.pop(ip,None);session.clear();session.permanent=True;session["owner"]=True
 return jsonify(ok=True)
@app.post("/api/logout")
def logout():session.clear();return jsonify(ok=True)
def number(value,low,high,name):
 try:
  n=float(value)
  if math.isfinite(n) and low<=n<=high:return n
 except (TypeError,ValueError):pass
 raise ValueError("Invalid "+name)
def merc(lon,lat):
 return R*math.radians(lon),R*math.log(math.tan(math.pi/4+math.radians(lat)/2))
def unmerc(x,y):
 return math.degrees(x/R),math.degrees(2*math.atan(math.exp(y/R))-math.pi/2)
def bounding(lat,lon,radius):
 x,y=merc(lon,lat); half=radius/max(.2,math.cos(math.radians(lat)))
 return (x-half,y-half,x+half,y+half)
NAD_POINTS="https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/Address_Points_from_National_Address_Database_view/FeatureServer/0/query"

def normalized_street(value):
 # Normalize road suffixes and compass directions without losing house/street identity.
 replacements={"STREET":"ST","ST":"ST","ROAD":"RD","RD":"RD","AVENUE":"AVE",
    "AVE":"AVE","DRIVE":"DR","DR":"DR","LANE":"LN","LN":"LN","COURT":"CT",
    "CT":"CT","PLACE":"PL","PL":"PL","BOULEVARD":"BLVD","PARKWAY":"PKWY",
    "CIRCLE":"CIR","TERRACE":"TER","HIGHWAY":"HWY","TRAIL":"TRL",
    "NORTH":"N","SOUTH":"S","EAST":"E","WEST":"W",
    "NORTHEAST":"NE","NORTHWEST":"NW","SOUTHEAST":"SE","SOUTHWEST":"SW"}
 words=re.findall(r"[A-Z0-9]+",str(value or "").upper())
 return " ".join(replacements.get(word,word) for word in words)

def nad_address_point(address,census_lat,census_lon):
 """Prefer an exact, nearby US DOT NAD address point; never infer a rooftop.
    The authoritative dataset varies in coverage and Placement quality.
 """
 match=re.match(r"^\s*(\d{1,6})([A-Za-z]?)\s+(.+?),",address)
 if not match:return None
 house_number=int(match.group(1))
 house_suffix=match.group(2).upper()
 searched_street=normalized_street(match.group(3))
 if not searched_street:return None
 state_match=re.search(r",\s*([A-Z]{2})\s*(?:,\s*|\s+)(\d{5})(?:-\d{4})?\s*$",address.upper())
 if not state_match:return None
 state,zip_code=state_match.groups()
 if not re.fullmatch(r"[A-Z]{2}",state):return None

 # Bounded spatial search avoids querying the entire ~100m record dataset.
 meters=350.0
 delta_lat=meters/111000.0
 delta_lon=meters/(111000.0*max(.2,math.cos(math.radians(census_lat))))
 envelope={"xmin":census_lon-delta_lon,"ymin":census_lat-delta_lat,
           "xmax":census_lon+delta_lon,"ymax":census_lat+delta_lat,
           "spatialReference":{"wkid":4326}}
 params={"where":f"Add_Number={house_number} AND State='{state}'",
   "geometry":__import__("json").dumps(envelope),"geometryType":"esriGeometryEnvelope",
   "inSR":4326,"outSR":4326,"spatialRel":"esriSpatialRelIntersects",
   "outFields":"Add_Number,AddNum_Suf,StNam_Full,St_Name,St_PreDir,St_PosTyp,St_PosDir,Zip_Code,State,Placement,Lifecycle",
   "returnGeometry":"true","resultRecordCount":120,"f":"json"}
 try:
  response=http.get(NAD_POINTS,params=params,timeout=(3,9))
  response.raise_for_status()
  data=response.json()
  if data.get("error"):return None
  matches=[]
  for feature in data.get("features",[]):
   attrs=feature.get("attributes") or {}
   try:
    if int(attrs.get("Add_Number"))!=house_number:continue
   except (ValueError,TypeError):continue
   if house_suffix and house_suffix!=str(attrs.get("AddNum_Suf") or "").upper().strip():continue
   if attrs.get("State") and str(attrs["State"]).upper()!=state:continue
   if attrs.get("Lifecycle") in ("Retired","Replaced","Expired"):continue
   candidate_street=normalized_street(attrs.get("StNam_Full") or
      " ".join(str(attrs.get(field) or "") for field in
       ("St_PreDir","St_Name","St_PosTyp","St_PosDir")))
   if candidate_street!=searched_street:continue
   candidate_zip=re.search(r"\d{5}",str(attrs.get("Zip_Code") or ""))
   if candidate_zip and candidate_zip.group(0)!=zip_code:continue
   point=feature.get("geometry") or {}
   lat=float(point.get("y"));lon=float(point.get("x"))
   if not (18<=lat<=72 and -180<=lon<=180):continue
   dist=math.hypot((lat-census_lat)*111000,
                  (lon-census_lon)*111000*math.cos(math.radians(census_lat)))
   if dist>350:continue
   placement=str(attrs.get("Placement") or "").strip()
   roof=placement.lower().startswith("structure - rooftop")
   # Prefer explicitly recorded rooftop placement and exact ZIP.
   score=(1 if roof else 0,int(bool(candidate_zip)), -dist)
   matches.append((score,lat,lon,roof,placement))
  if not matches:return None
  matches.sort(reverse=True)
  _,lat,lon,roof,placement=matches[0]
  if roof:
   return {"lat":lat,"lon":lon,"pin_accuracy":"rooftop_recorded",
    "pin_source":"U.S. DOT National Address Database",
    "pin_note":"Government address point classified as structure rooftop. Verify against the photo; records can still be wrong or outdated."}
  return {"lat":lat,"lon":lon,"pin_accuracy":"address_point",
   "pin_source":"U.S. DOT National Address Database",
   "pin_note":"Exact street/house-number match to an address point ("+
      (placement or "placement not stated")+
      "). Not certified as rooftop location; verify manually."}
 except (requests.RequestException,ValueError,TypeError,KeyError):
  logging.info("USDOT NAD address point lookup unavailable; using another geocoder")
 return None

def rooftop_geocode(address, census_lat, census_lon):
 # World Geocoding returns display points for PointAddress matches when available.
 # It requires geocoding privileges. A separate server-side key is preferred.
 # Do not store provider results: forStorage=false; each search is a new request.
 token=(os.getenv("ARCGIS_GEOCODING_API_KEY") or
        os.getenv("ARCGIS_API_KEY") or "").strip()
 if not token:return None
 endpoint="https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"
 params={"SingleLine":address,"sourceCountry":"USA","outFields":"Addr_type,AddNum,Match_addr,DisplayX,DisplayY",
         "locationType":"rooftop","outSR":4326,"maxLocations":4,
         "forStorage":"false","f":"json","token":token}
 try:
  r=http.get(endpoint,params=params,headers={"Referer":"https://lawnquote-owner-tool.onrender.com/"},timeout=(4,8))
  r.raise_for_status()
  data=r.json()
  if data.get("error"):
   logging.warning("ArcGIS geocoder unavailable: provider rejected request")
   return None
  number_match=re.match(r"^\\s*(\\d+[A-Za-z]?)\\b",address)
  requested_house=number_match.group(1).upper() if number_match else None
  for candidate in data.get("candidates",[]):
   attrs=candidate.get("attributes") or {}
   if attrs.get("Addr_type") not in ("PointAddress","Subaddress"):continue
   if float(candidate.get("score",0))<93:continue
   if requested_house:
    matched_house=str(attrs.get("AddNum") or "").strip().upper()
    if not matched_house:
     matched_house_match=re.match(r"^\\s*(\\d+[A-Za-z]?)\\b",
       str(attrs.get("Match_addr") or candidate.get("address") or ""))
     matched_house=matched_house_match.group(1).upper() if matched_house_match else ""
    if matched_house!=requested_house:continue
   def coord(key,other):
    try:return float(attrs[key])
    except (TypeError,KeyError,ValueError):return float(candidate["location"][other])
   lon=coord("DisplayX","x");lat=coord("DisplayY","y")
   if not (-180<=lon<=180 and 18<=lat<=72):continue
   # Prevent an unrelated high-score candidate across town.
   meter_dist=math.hypot((lat-census_lat)*111000,
                         (lon-census_lon)*111000*math.cos(math.radians(census_lat)))
   if meter_dist>900:continue
   return {"lat":lat,"lon":lon,"pin_accuracy":"address_point",
           "pin_source":"ArcGIS address point",
           "pin_note":"Building/parcel address-point match. Verify the blue pin against the roof; some points still represent an entrance or nearby location."}
 except (requests.RequestException,KeyError,ValueError,TypeError):
  logging.info("ArcGIS address-point lookup unavailable; using Census fallback")
 return None

@app.get("/api/address")
@authorized
def address():
 q=request.args.get("q","").strip()
 if not 8<=len(q)<=220:return err("Enter an address with street, city and state.")
 try:
  r=http.get(CENSUS,params={"address":q,"benchmark":"Public_AR_Current","format":"json"},timeout=(4,18))
  r.raise_for_status()
  found=r.json().get("result",{}).get("addressMatches",[])
  if not found:return err("Address not found. Include city, state and ZIP.",404)
  m=found[0]
  lat=float(m["coordinates"]["y"]);lon=float(m["coordinates"]["x"])
  result={"address":m.get("matchedAddress",q),"lat":lat,"lon":lon,
          "pin_accuracy":"approximate","pin_source":"U.S. Census geocoder",
          "pin_note":"Approximate street-address location; this is not a verified rooftop point. Tap Place pin on roof to correct it."}
  government=nad_address_point(result["address"],lat,lon)
  # A high-quality official rooftop point is preferred; a non-roof point can be
  # superseded by an ArcGIS PointAddress display location when available.
  improved=government if government and government["pin_accuracy"]=="rooftop_recorded" else None
  if not improved:
   paid=rooftop_geocode(result["address"],lat,lon)
   improved=paid or government
  if improved:result.update(improved)
  response=jsonify(result);response.headers["Cache-Control"]="private,no-store"
  return response
 except (requests.RequestException,KeyError,ValueError,TypeError):
  return err("Address search unavailable. Try again.",502)
@app.get("/api/aerial")
@authorized
def aerial():
 try:
  lat=number(request.args.get("lat"),18,72,"latitude")
  lon=number(request.args.get("lon"),-180,180,"longitude")
  radius=number(request.args.get("radius",90),25,600,"view radius")
 except ValueError as e:return err(str(e))
 box=bounding(lat,lon,radius)
 params={"bbox":",".join(map(str,box)),"bboxSR":3857,"imageSR":3857,
    "size":"900,900","format":"jpg","f":"image"}
 providers=[
  ("USGS NAIP Imagery","https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer/exportImage"),
  ("USGS NAIP Plus",NAIP),
 ]
 for name,url in providers:
  try:
   r=http.get(url,params=params,timeout=(4,11))
   r.raise_for_status()
   if not r.headers.get("Content-Type","").lower().startswith("image/"):
    logging.warning("Aerial provider %s returned non-image content",name)
    continue
   if len(r.content)<1000 or not (r.content.startswith(bytes.fromhex("ffd8")) or
                                 r.content.startswith(bytes.fromhex("89504e47"))):
    logging.warning("Aerial provider %s returned invalid image bytes",name)
    continue
   mimetype="image/png" if r.content.startswith(bytes.fromhex("89504e47")) else "image/jpeg"
   resp=send_file(BytesIO(r.content),mimetype=mimetype)
   resp.headers["Cache-Control"]="private,max-age=600"
   resp.headers["X-Imagery-Source"]=name
   return resp
  except requests.RequestException as exc:
   logging.warning("Aerial provider %s temporarily unavailable: %s",name,type(exc).__name__)
 # This error does not prevent using the separate USGS tile basemap in the app.
 return err("High-resolution aerial imagery is temporarily unavailable. Continue with the USGS aerial basemap.",503)
def parse_shapes(data,field):
 a=data.get(field,[])
 if not isinstance(a,list) or len(a)>75:raise ValueError("Too many outlines.")
 polys=[]
 for item in a:
  p=shape(item)
  if p.geom_type!="Polygon" or not p.is_valid or len(p.exterior.coords)>500:
   raise ValueError("Invalid polygon. Avoid self-crossing lines.")
  for lon,lat in p.exterior.coords:
   if not (-180<=lon<=180 and 18<lat<72):
    raise ValueError("Outline coordinates outside supported region.")
  polys.append(p)
 return polys
def measured(data):
 areas=parse_shapes(data,"areas");exclusions=parse_shapes(data,"exclusions")
 if not areas:return {"area_sqft":0,"gross_sqft":0,"excluded_sqft":0}
 joined=unary_union(areas)
 if joined.bounds[2]-joined.bounds[0]>.05 or joined.bounds[3]-joined.bounds[1]>.05:
  raise ValueError("Drawing is too large.")
 net=joined.difference(unary_union(exclusions)) if exclusions else joined
 coslat=math.cos(math.radians(joined.centroid.y))
 def meters(x,y,z=None):return math.radians(x)*R*coslat,math.radians(y)*R
 gross=transform(meters,joined).area*SFT
 area=transform(meters,net).area*SFT
 if gross>50000000:raise ValueError("Drawing exceeds supported property size.")
 return {"area_sqft":round(area),"gross_sqft":round(gross),"excluded_sqft":round(max(0,gross-area))}
@app.post("/api/area")
@authorized
def area():
 try:return jsonify(measured(request.get_json(silent=True) or {}))
 except (ValueError,TypeError,KeyError) as e:return err(str(e))
def valid_email(v):
 v=str(v or "").strip()
 if len(v)>254 or not re.fullmatch(r"[^@\s]{1,100}@[^@\s]+\.[^@\s]{2,}",v):
  raise ValueError("Enter a valid email address.")
 return v
def clean(v,n=120):return str(v or "").strip()[:n]
def money(v):return chr(36)+format(v,",.2f")
@app.post("/api/send")
@authorized
def send():
 if not configured():return err("Email sending requires RESEND_API_KEY and RESEND_FROM_EMAIL in Render.",503)
 data=request.get_json(silent=True) or {}
 try:
  measure=measured(data);sqft=measure["area_sqft"]
  if sqft<1:raise ValueError("Draw the area being priced before sending.")
  customer=valid_email(data.get("customer_email"))
  owner=valid_email(data.get("owner_email"))
  if owner.lower()==customer.lower():raise ValueError("Customer and owner email must be different.")
  company=clean(data.get("company"),80) or "LawnQuote"
  address=clean(data.get("address"),220)
  if len(address)<8:raise ValueError("Enter the property address.")
  customer_name=clean(data.get("customer_name"),100) or "Customer"
  phone=clean(data.get("phone"),50)
  notes=clean(data.get("notes"),900)
  selected=data.get("services",[])
  if not isinstance(selected,list) or not 1<=len(selected)<=25:raise ValueError("Choose a service.")
  lines=[]
  for s in selected:
   name=clean(s.get("name"),80)
   if not name:raise ValueError("Service name is missing.")
   rate=number(s.get("rate"),0,100000,"service rate")
   minimum=number(s.get("minimum",0),0,100000,"minimum price")
   price=round(max(sqft/1000*rate,minimum)+1e-9,2)
   lines.append((name,rate,price))
  total=round(sum(row[2] for row in lines),2)
 except (ValueError,TypeError,KeyError,AttributeError) as e:return err(str(e))
 rows="".join("<tr><td style='padding:12px;border-bottom:1px solid #dde4dd'>"+
     html.escape(name)+" ("+money(rate)+" / 1,000 sq ft)</td><td style='text-align:right'>"+
     money(price)+"</td></tr>" for name,rate,price in lines)
 body=("<div style='font-family:Arial,sans-serif;max-width:640px;margin:auto;color:#1c392b'>"
   "<h1>"+html.escape(company)+"</h1><h2>Lawn Service Estimate</h2><p>Prepared for "+
   html.escape(customer_name)+"<br>Property: "+html.escape(address)+"</p><p><strong>Manually drawn service area: "+
   format(sqft,",")+" square feet</strong></p><table style='width:100%;border-collapse:collapse'>"+
   rows+"</table><h2>Total estimate: "+money(total)+"</h2><p>"+
   html.escape(notes)+"</p><p>"+html.escape(phone)+"</p><p style='color:#777;font-size:12px'>"
   "Approximate aerial measurements; prices subject to on-site verification.</p></div>")
 template={"from":os.getenv("RESEND_FROM_EMAIL"),"reply_to":owner,
  "subject":company+" | Lawn Service Estimate | "+address,"html":body}
 results={}
 for label,receiver in (("customer",customer),("owner",owner)):
  try:
   res=http.post("https://api.resend.com/emails",
      headers={"Authorization":"Bearer "+os.environ["RESEND_API_KEY"],"Content-Type":"application/json"},
      json={**template,"to":[receiver]},timeout=20)
   res.raise_for_status()
   results[label]={"accepted":True,"id":res.json().get("id")}
  except (requests.RequestException,ValueError) as ex:
   logging.warning("Email %s failed: %s",label,type(ex).__name__)
   results[label]={"accepted":False}
 ok=all(r["accepted"] for r in results.values())
 return jsonify(ok=ok,results=results,total=total,sqft=sqft,
  message=("Both emails accepted by sending service." if ok else
     "One or more sends failed. Check statuses before retrying to avoid duplicates.")),(200 if ok else 207)
if __name__=="__main__":app.run(host="0.0.0.0",port=int(os.getenv("PORT",5000)))
