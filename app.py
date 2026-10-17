"""LawnMeasure: experimental lawn vegetation estimator from US public aerial imagery.
Square footage is approximate and must be reviewed before quoting.
"""
from __future__ import annotations
import base64, io, json, math, re
from difflib import SequenceMatcher
from functools import lru_cache
import numpy as np
import requests
from flask import Flask, jsonify, request
from PIL import Image, ImageDraw
from scipy.ndimage import binary_closing, binary_opening, uniform_filter
from shapely.geometry import Point, shape, mapping
from shapely.ops import transform

app=Flask(__name__)
CENSUS="https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
NAIP="https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer/exportImage"
BOONE="https://secure.boonecountygis.com/server/rest/services/ParcelLayers/MapServer/32/query"
R=6378137.; PX=768; FT=10.76391041671
http=requests.Session()
http.headers["User-Agent"]="LawnMeasure/1.0 (US aerial imagery estimator)"

class MapUnavailable(Exception): pass

def get_json(url, params):
    try:
        res=http.get(url, params=params, timeout=26);res.raise_for_status()
        data=res.json()
        if isinstance(data,dict) and data.get("error"):
            raise MapUnavailable(str(data["error"].get("message","Mapping provider error")))
        return data
    except (requests.RequestException,ValueError) as exc:
        raise MapUnavailable("Mapping service unavailable. Please try again.") from exc

@lru_cache(maxsize=128)
def geocode(address):
    matches=get_json(CENSUS,{"address":address,"benchmark":"Public_AR_Current","format":"json"}).get("result",{}).get("addressMatches",[])
    if not matches: raise ValueError("Address not found. Enter street address, city and state.")
    m=matches[0]
    return dict(lat=float(m["coordinates"]["y"]), lon=float(m["coordinates"]["x"]),
                address=m.get("matchedAddress",address),state=m.get("addressComponents",{}).get("state",""))

def mx(lon): return math.radians(lon)*R
def my(lat): return R*math.log(math.tan(math.pi/4+math.radians(max(-85,min(85,lat)))/2))
def ilon(x): return math.degrees(x/R)
def ilat(y): return math.degrees(2*math.atan(math.exp(y/R))-math.pi/2)

def norm(value):
    substitutions={"STREET":"ST","ROAD":"RD","AVENUE":"AVE","DRIVE":"DR","LANE":"LN","COURT":"CT",
      "BOULEVARD":"BLVD","PLACE":"PL","PARKWAY":"PKWY","CIRCLE":"CIR","HIGHWAY":"HWY","NORTH":"N",
      "SOUTH":"S","EAST":"E","WEST":"W"}
    s=re.sub(r"[^A-Z0-9 ]"," ",value.upper())
    return " ".join(substitutions.get(w,w) for w in s.split())

def county_boundary(address,lon,lat):
    if not (-85<lon<-84.45 and 38.75<lat<39.25): return None
    street=norm(address.split(",")[0])
    match=re.match(r"^(\d+[A-Z]?)\s+(.+)$",street)
    if not match: return None
    house,road=match.groups()
    prefix=" ".join(road.split()[:2]).replace("'","''")
    try:
        features=get_json(BOONE,{"where":f"SITEADD1 LIKE '{house} {prefix}%'",
            "outFields":"SITEADD1,PIDN","outSR":4326,"returnGeometry":"true",
            "resultRecordCount":100,"f":"geojson"}).get("features",[])
    except MapUnavailable: return None
    candidates=[]
    for f in features:
        try:
            site=norm(str(f.get("properties",{}).get("SITEADD1") or ""))
            if not site or site.split()[0]!=house: continue
            score=SequenceMatcher(None,street,site).ratio()
            if score<.80: continue
            p=shape(f["geometry"])
            if not p.is_valid:p=p.buffer(0)
            if p.is_empty or p.geom_type not in ("Polygon","MultiPolygon"): continue
            distance=p.distance(Point(lon,lat))*111000
            if distance>500:continue
            candidates.append((score-distance/100000,p))
        except (KeyError,ValueError,TypeError,IndexError):continue
    return max(candidates,key=lambda x:x[0])[1] if candidates else None

def bbox_for(poly,lat,lon,radius):
    cs=max(.1,math.cos(math.radians(lat)))
    if poly is None:
        side=max(radius*2.7,95)/cs
        cx,cy=mx(lon),my(lat)
    else:
        mapped=transform(lambda x,y,z=None:(np.radians(x)*R,
          R*np.log(np.tan(np.pi/4+np.radians(np.clip(y,-85,85))/2))),poly)
        x1,y1,x2,y2=mapped.bounds
        side=max(max((x2-x1)*cs,(y2-y1)*cs)*1.16+15,85)/cs
        cx,cy=(x1+x2)/2,(y1+y2)/2
    return cx-side/2,cy-side/2,cx+side/2,cy+side/2

def image(bbox,rendering):
    x1,y1,x2,y2=bbox
    args={"bbox":f"{x1},{y1},{x2},{y2}","bboxSR":3857,"imageSR":3857,
      "size":f"{PX},{PX}","format":"jpg","interpolation":"RSP_NearestNeighbor","f":"image"}
    if rendering:args["renderingRule"]=json.dumps({"rasterFunction":rendering})
    try:
        r=http.get(NAIP,params=args,timeout=50);r.raise_for_status()
        if not r.headers.get("content-type","").lower().startswith("image/"):
            raise MapUnavailable("Aerial imagery isn't available for that property.")
        return Image.open(io.BytesIO(r.content)).convert("RGB")
    except (requests.RequestException,OSError,ValueError) as exc:
        raise MapUnavailable("USGS aerial imagery unavailable. Try another address.") from exc

def polygon_mask(poly,bbox):
    out=Image.new("L",(PX,PX),0)
    d=ImageDraw.Draw(out)
    x1,y1,x2,y2=bbox
    def point(x,y):return ((mx(x)-x1)/(x2-x1)*PX,(y2-my(y))/(y2-y1)*PX)
    for p in [poly] if poly.geom_type=="Polygon" else poly.geoms:
        d.polygon([point(x,y) for x,y in p.exterior.coords],fill=255)
        for hole in p.interiors:
            d.polygon([point(x,y) for x,y in hole.coords],fill=0)
    return np.asarray(out)>127

def grass_mask(natural,falsecolor,sensitivity):
    rgb=np.asarray(natural,dtype=np.float32)
    red,green,blue=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    gray=.299*red+.587*green+.114*blue
    mean=uniform_filter(gray,size=9)
    texture=np.sqrt(np.maximum(0,uniform_filter(gray*gray,size=9)-mean*mean))
    t=max(0,min(100,sensitivity))/100
    if falsecolor is not None:
        fc=np.asarray(falsecolor,dtype=np.float32)
        nir,visible_red=fc[:,:,0],fc[:,:,1]
        proxy=(nir-visible_red)/(nir+visible_red+1e-6)
        veg=(proxy>.18-t*.14)&(nir>65-t*14)
    else:
        veg=(green>red*(1.08-t*.28))&(green>blue*(1.05-t*.25))&(green>43)
    mask=veg&(texture<15+t*27)&(gray>37-t*10)&(gray<244)
    mask=binary_opening(mask,structure=np.ones((3,3),dtype=bool))
    return binary_closing(mask,structure=np.ones((4,4),dtype=bool))

def png_mask(mask):
    arr=np.zeros((PX,PX,4),dtype=np.uint8)
    arr[mask]=[36,240,112,112]
    buf=io.BytesIO();Image.fromarray(arr,"RGBA").save(buf,format="PNG")
    return "data:image/png;base64,"+base64.b64encode(buf.getvalue()).decode()

def jpeg(img):
    buf=io.BytesIO();img.save(buf,format="JPEG",quality=86)
    return "data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()

@app.get("/")
def home():
    from flask import send_from_directory
    return send_from_directory("static","index.html")

@app.get("/health")
def health(): return jsonify(ok=True, service="LawnMeasure")

@app.post("/api/measure")
def measure():
    args=request.get_json(silent=True) or {}
    addr=str(args.get("address","")).strip()
    if not 8<=len(addr)<=220:return jsonify(error="Enter a full street address including city and state."),400
    try:
        sensitivity=max(0,min(100,int(args.get("sensitivity",55))))
        radius=max(15,min(150,int(args.get("radius_m",37))))
        loc=geocode(addr)
        lat,lon=loc["lat"],loc["lon"]
        polygon=None;scope="search-zone"
        custom=args.get("custom_boundary")
        if custom:
            polygon=shape(custom)
            if not polygon.is_valid:polygon=polygon.buffer(0)
            if polygon.is_empty or polygon.geom_type not in ("Polygon","MultiPolygon"):
                raise ValueError("Draw a valid polygon.")
            if polygon.area>.0003 or polygon.distance(Point(lon,lat))>.03:
                raise ValueError("Drawn boundary is too large or too far away.")
            scope="user-drawn"
        elif loc["state"]=="KY":
            polygon=county_boundary(loc["address"],lon,lat)
            if polygon is not None:scope="matched-parcel"
        if polygon is None:
            x,y=mx(lon),my(lat)
            cs=max(.1,math.cos(math.radians(lat)))
            polygon=transform(lambda xx,yy,z=None:(ilon(xx),ilat(yy)),
                  Point(x,y).buffer(radius/cs,resolution=80))
        box=bbox_for(polygon if scope!="search-zone" else None,lat,lon,radius)
        natural=image(box,"NaturalColor")
        try:false=image(box,"FalseColorComposite")
        except MapUnavailable:false=None
        roi=polygon_mask(polygon,box)
        grass=grass_mask(natural,false,sensitivity)&roi
        x1,y1,x2,y2=box
        coslat=math.cos(math.radians(lat))
        pixel_area=(x2-x1)*(y2-y1)/PX**2*coslat**2*FT
        warnings=["Experimental image-color/texture vegetation detection may mistake trees, shrubs, shadows and landscaping for lawn."]
        if scope=="search-zone":warnings.insert(0,"No confirmed parcel. This is a circular search-zone estimate, NOT property-specific lawn square footage. Draw the actual property boundary.")
        if false is None:warnings.append("False-color imagery unavailable; detection used the less reliable visible-green approximation.")
        return jsonify(address=loc["address"],location={"lat":lat,"lon":lon},
            sqft=round(float(grass.sum())*pixel_area),
            scope_sqft=round(float(roi.sum())*pixel_area),
            scope=scope, bounds=[[ilat(y1),ilon(x1)],[ilat(y2),ilon(x2)]],
            aerial_image=jpeg(natural),grass_overlay=png_mask(grass),
            boundary=mapping(polygon.simplify(.0000008,preserve_topology=True)),
            warnings=warnings,imagery_attribution="USGS / USDA / The National Map – NAIP")
    except ValueError as exc:return jsonify(error=str(exc)),422
    except MapUnavailable as exc:return jsonify(error=str(exc)),503
    except Exception:
        app.logger.exception("Measurement failed")
        return jsonify(error="Unexpected measurement error. Try another address."),500

if __name__=="__main__":app.run(host="0.0.0.0",port=5000)
