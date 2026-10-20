"""Top 50 U.S. metropolitan statistical areas by Census July 1, 2025 population.

MSA footprint is defined by Census TIGERweb (ACS 2025), NOT radius around the
principal city. Each metro includes its OMB-designated suburban counties.
This is an imagery SOURCE RESEARCH PRIORITY registry, not a completed audit.
Population vintage: https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-metro-and-micro-statistical-areas.html
MSA delineation: https://www.census.gov/programs-surveys/metro-micro/about/delineation-files.html
"""

import re
METRO_RANKING_2025=[["New York-Newark-Jersey City, NY-NJ",20112448],["Los Angeles-Long Beach-Anaheim, CA",12844441],["Chicago-Naperville-Elgin, IL-IN",9434123],["Dallas-Fort Worth-Arlington, TX",8477157],["Houston-Pasadena-The Woodlands, TX",7904627],["Atlanta-Sandy Springs-Roswell, GA",6482182],["Washington-Arlington-Alexandria, DC-VA-MD-WV",6465724],["Miami-Fort Lauderdale-West Palm Beach, FL",6391072],["Philadelphia-Camden-Wilmington, PA-NJ-DE-MD",6329118],["Phoenix-Mesa-Chandler, AZ",5228938],["Boston-Cambridge-Newton, MA-NH",5034221],["Riverside-San Bernardino-Ontario, CA",4769007],["San Francisco-Oakland-Fremont, CA",4630041],["Detroit-Warren-Dearborn, MI",4390913],["Seattle-Tacoma-Bellevue, WA",4161883],["Minneapolis-St. Paul-Bloomington, MN-WI",3790295],["Tampa-St. Petersburg-Clearwater, FL",3418895],["San Diego-Chula Vista-Carlsbad, CA",3282248],["Denver-Aurora-Centennial, CO",3092037],["Orlando-Kissimmee-Sanford, FL",2957672],["Charlotte-Concord-Gastonia, NC-SC",2938830],["Baltimore-Columbia-Towson, MD",2857781],["St. Louis, MO-IL",2814421],["San Antonio-New Braunfels, TX",2813140],["Austin-Round Rock-San Marcos, TX",2620945],["Portland-Vancouver-Hillsboro, OR-WA",2542282],["Sacramento-Roseville-Folsom, CA",2477274],["Pittsburgh, PA",2421992],["Las Vegas-Henderson-North Las Vegas, NV",2407226],["Cincinnati, OH-KY-IN",2312858],["Kansas City, MO-KS",2270682],["Columbus, OH",2242028],["Indianapolis-Carmel-Greenwood, IN",2205695],["Nashville-Davidson--Murfreesboro--Franklin, TN",2197416],["Cleveland, OH",2165775],["San Jose-Sunnyvale-Santa Clara, CA",1984473],["Virginia Beach-Chesapeake-Norfolk, VA-NC",1797213],["Jacksonville, FL",1785500],["Providence-Warwick, RI-MA",1708161],["Raleigh-Cary, NC",1595720],["Milwaukee-Waukesha, WI",1575010],["Oklahoma City, OK",1512813],["Louisville/Jefferson County, KY-IN",1402509],["Richmond, VA",1389338],["Memphis, TN-MS-AR",1341412],["Salt Lake City-Murray, UT",1308377],["Fresno, CA",1203383],["Birmingham, AL",1197766],["Grand Rapids-Wyoming-Kentwood, MI",1183645],["Hartford-West Hartford-East Hartford, CT",1171426]]
assert len(METRO_RANKING_2025)==50
assert len({name for name,_ in METRO_RANKING_2025})==50
assert all(METRO_RANKING_2025[i][1]>METRO_RANKING_2025[i+1][1] for i in range(49))
CENSUS_TIGER_METRO_QUERY=(
 "https://tigerweb.geo.census.gov/arcgis/rest/services/"
 "TIGERweb/CBSA/MapServer/15/query"
)

def _metro_parts(title):
 """Name and list of states from an official 'Name, NY-NJ' title."""
 city, states=title.rsplit(", ",1)
 return city,[x.strip() for x in states.split("-")]

def _metro_key(text):
 core=str(text or "").rsplit(", ",1)[0]
 # Exact first principal city avoids relying on renamed secondary cities.
 return re.sub(r"[^a-z0-9]+","",re.split(r"[-/]",core,1)[0].lower())

def metro_record(index):
 name,pop=METRO_RANKING_2025[index]
 _,states=_metro_parts(name)
 houston=index==4
 return {
  "rank":index+1,"name":name,"population_2025":pop,
  "states":states,"core_city":re.split(r"[-/]",name,1)[0],
  "boundary":"OMB metropolitan statistical area, 2025 Census TIGERweb",
  "imagery_status":"regional_public_source_configured_qa_pending" if houston else "source_research_pending",
  "metro_image_qa_complete":False,
  "county_and_suburb_coverage_audited":False,
  "note":(
   "City of Galveston 2026/2025/2024 public aerials added. Galveston 2025 ImageServer reports ~1 inch native pixels; Houston core, Katy, Sugar Land, and The Woodlands still lack a confirmed freely commercially reusable rooftop-quality imagery source. 2024 six-inch H-GAC regional photography requires purchase/license. Live imagery clarity and city service use rights are not yet audited."
   if houston else
   "Existing state/county aerial fallbacks remain. No native 3-inch, source year or reuse-rights guarantee."),
 }

TOP_50_METROS=[metro_record(i) for i in range(50)]
def find_top_metro(metro_basename, cbsa_code=None):
 """Validate both primary-city match AND states to avoid e.g. Portland ME/OR."""
 text=str(metro_basename or "").strip()
 if not text:return None
 cleaned=_metro_key(text)
 try:_,reported_states=_metro_parts(text)
 except ValueError:reported_states=[]
 for item in TOP_50_METROS:
  if _metro_key(item["name"])!=cleaned:continue
  # The official metropolitan label may contain additional/fewer secondary
  # cities. Require the principal state's two-letter code, not an exact title.
  if not reported_states or item["states"][0] not in reported_states:continue
  return {
   "rank":item["rank"],"name":item["name"],
   "population_2025":item["population_2025"],
   "cbsa_code":str(cbsa_code or ""),
   "target":True,"boundary_source":"Census TIGERweb / ACS 2025 MSA",
   "imagery_status":"source_research_pending",
   "metro_image_qa_complete":False,
  }
 return None

def metro_summary():
 return {
  "total_target_metros":50,"population_estimate_year":2025,
  "boundary_year":2025,"metro_qa_completed":0,
  "metro_qa_pending":50,
  "metro_definition":"Metropolitan statistical areas include suburbs and commuting-linked counties; not fixed radius around a downtown point.",
  "out_of_scope_policy":"Keep existing government aerial and national fallbacks; do not block property measurements.",
  "metros":TOP_50_METROS,
  "data_sources":[
   "https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-metro-and-micro-statistical-areas.html",
   "https://www.census.gov/programs-surveys/metro-micro/about/delineation-files.html",
  ]
 }
