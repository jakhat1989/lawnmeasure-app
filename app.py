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
@app.get("/")
def home():return send_from_directory("static","index.html")
@app.get("/health")
def health():return jsonify(ok=True,product="LawnQuote Owner")
@app.get("/api/status")
def status():return jsonify(authenticated=bool(session.get("owner")),email_configured=configured())
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
@app.get("/api/address")
@authorized
def address():
 q=request.args.get("q","").strip()
 if not 8<=len(q)<=220:return err("Enter an address with street, city and state.")
 try:
  r=http.get(CENSUS,params={"address":q,"benchmark":"Public_AR_Current","format":"json"},timeout=18)
  r.raise_for_status()
  found=r.json().get("result",{}).get("addressMatches",[])
  if not found:return err("Address not found. Include city, state and ZIP.",404)
  m=found[0];lat=float(m["coordinates"]["y"]);lon=float(m["coordinates"]["x"])
  return jsonify(address=m.get("matchedAddress",q),lat=lat,lon=lon)
 except (requests.RequestException,KeyError,ValueError,TypeError):
  return err("Address search unavailable. Try again.",502)
@app.get("/api/aerial")
@authorized
def aerial():
 try:
  lat=number(request.args.get("lat"),18,72,"latitude")
  lon=number(request.args.get("lon"),-170,-60,"longitude")
  radius=number(request.args.get("radius",90),25,600,"view radius")
 except ValueError as e:return err(str(e))
 b=bounding(lat,lon,radius)
 try:
  r=http.get(NAIP,params={"bbox":",".join(map(str,b)),"bboxSR":3857,"imageSR":3857,
    "size":"1200,1200","format":"jpg","f":"image"},timeout=55)
  r.raise_for_status()
  if not r.headers.get("content-type","").startswith("image/"):
   return err("No aerial imagery available at this location.",502)
  resp=send_file(BytesIO(r.content),mimetype="image/jpeg")
  resp.headers["Cache-Control"]="private, max-age=900"
  return resp
 except requests.RequestException:return err("USGS imagery service is temporarily unavailable.",502)
def parse_shapes(data,field):
 a=data.get(field,[])
 if not isinstance(a,list) or len(a)>75:raise ValueError("Too many outlines.")
 polys=[]
 for item in a:
  p=shape(item)
  if p.geom_type!="Polygon" or not p.is_valid or len(p.exterior.coords)>500:
   raise ValueError("Invalid polygon. Avoid self-crossing lines.")
  for lon,lat in p.exterior.coords:
   if not (-170<lon<-60 and 18<lat<72):
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
