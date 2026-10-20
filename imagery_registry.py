"""Curated public-orthophoto service catalog (2026-10-19).
Adding a county requires an official published image service, not just a dataset.
The catalog does not certify live availability, actual footprints, or reuse rights.
Do not imply national three-inch coverage. Add state and county providers after review.
"""
STATE_CODES=frozenset(("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME "
 "MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN "
 "TX UT VT VA WA WV WI WY DC").split())

# Entries: display label, public image URL, service type, approximate native inch/pixel,
# source vintage, publisher, documentation or authoritative service metadata URL.
SOURCES={
 "CA_NAPA_2025":("Napa County CA April 2025 ~2.94 inch official aerial imagery",
  "https://gis.napa.ca.gov/arcgis/rest/services/OrthoImagery/NapaCountyTiles2025/ImageServer/exportImage",
  "image",2.94,"2025","Napa County GIS",
  "https://gis.napa.ca.gov/arcgis/rest/services/OrthoImagery/NapaCountyTiles2025/ImageServer"),
 "CA_SAN_DIEGO_2023_9IN":("San Diego regional public 2023 9-inch aerial imagery",
  "https://gis.sandag.org/sdgis/rest/services/Imagery/SD2023_9inch/ImageServer/exportImage",
  "image",9,"2023","SANDAG / SanGIS / Nearmap (9-inch public domain)",
  "https://gis.sandag.org/sdgis/rest/services/Imagery/SD2023_9inch/ImageServer/info/iteminfo"),
 "CA_SAN_DIEGO_2017_4IN":("San Diego 2017 public 4-inch orthophotos (older alternative)",
  "https://gis.sandag.org/sdgis/rest/services/Imagery/SD2017_4inch/ImageServer/exportImage",
  "image",4,"2017","SANDAG / SanGIS public four-inch 2017 dataset",
  "https://gis.sandag.org/sdgis/rest/services/Imagery/SD2017_4inch/ImageServer/info/iteminfo"),
 "CA_CDFW_NAIP_2022":("California CDFW NAIP 2022 60-centimeter natural color aerial",
  "https://gis.wildlife.ca.gov/images/rest/services/Base_Remote_Sensing/NAIP_2022/ImageServer/exportImage",
  "image",23.62,"2022","California Department of Fish and Wildlife / USDA (CC BY)",
  "https://catalog.data.gov/dataset/naip-2022-60cm-california"),
 "IN_HAMILTON_2024_3IN":("Hamilton County IN 2024 native 3-inch orthophotos",
  "https://di-ingov.img.arcgis.com/arcgis/rest/services/DynamicWebMercator/Indiana_County_Collect_2024_Imagery/ImageServer/exportImage",
  "image",3,"2024","Indiana Geographic Information Office",
  "https://di-ingov.img.arcgis.com/arcgis/rest/services/DynamicWebMercator/Indiana_County_Collect_2024_Imagery/ImageServer"),
 "IN_JOHNSON_NORTH_2025":("North Johnson County Indiana spring 2025 ortho (partial coverage)",
  "https://greenwoodgis.greenwood.in.gov/arcgis/rest/services/Ortho/JCNorth2025Ortho/MapServer/export",
  "map",None,"2025","City of Greenwood GIS",
  "https://greenwoodgis.greenwood.in.gov/arcgis/rest/services/Ortho/JCNorth2025Ortho/MapServer"),
 "IN_CURRENT":("Indiana state latest streamed orthophotography (some 3-inch)",
  "https://di-ingov.img.arcgis.com/arcgis/rest/services/DynamicWebMercator/Indiana_Current_Imagery/ImageServer/exportImage",
  "image",None,"2022-2025 by county","Indiana Geographic Information Office (CC0)",
  "https://di-ingov.img.arcgis.com/arcgis/rest/services/DynamicWebMercator/Indiana_Current_Imagery/ImageServer"),
 "OH_LICKING_2025":("Licking County Ohio 2025 three-inch orthophotography",
  "https://apps.lickingcounty.gov/arcgis/rest/services/Basemaps/Imagery2025/MapServer/export",
  "map",3,"2025","Licking County GIS",
  "https://apps.lickingcounty.gov/arcgis/rest/services/Basemaps/Imagery2025/MapServer"),
 "OH_OSIP_DYNAMIC":("Ohio statewide OSIP most-current (dynamic backup)",
  "https://maps.ohio.gov/image/rest/services/osip_most_current/ImageServer/exportImage",
  "image",None,"2017-2024 dynamic service","Ohio OGRIP",
  "https://maps.ohio.gov/image/rest/services/osip_most_current/ImageServer"),
 "IL_COOK":("Cook County 2025 orthoimagery",
  "https://gis.cookcountyil.gov/imagery/rest/services/CookOrtho2025/ImageServer/exportImage",
  "image",6,"2025","Cook County GIS",
  "https://gis.cookcountyil.gov/imagery/rest/services/CookOrtho2025/ImageServer/info/iteminfo"),
 "FL_MARION_2024":("Marion County Florida 2024 aerial imagery",
  "https://gis.marionfl.org/image/rest/services/Aerials/Aerial2024/ImageServer/exportImage",
  "image",1.5,"2024","Marion County GIS",
  "https://gis.marionfl.org/image/rest/services/Aerials/Aerial2024/ImageServer"),
 "FL_MARION":("Marion County Florida 2023 imagery backup",
  "https://gis.marionfl.org/image/rest/services/Aerials/Aerials_2023/ImageServer/exportImage",
  "image",None,"2023","Marion County GIS",
  "https://gis.marionfl.org/image/rest/services/Aerials/Aerials_2023/ImageServer"),
 "FL_SW":("Southwest Florida water district 2023 orthophotos",
  "https://www25.swfwmd.state.fl.us/arcgiswmis/rest/services/Imagery/Imagery_2023_NC/MapServer/export",
  "map",6,"2023","Southwest Florida Water Management District",
  "https://www25.swfwmd.state.fl.us/arcgiswmis/rest/services/Imagery/Imagery_2023_NC/MapServer"),
 "MD_3IN":("Maryland current available 3-inch orthophotos",
  "https://mdgeodata.md.gov/imagery/rest/services/ThreeInch/MD_ThreeInchImagery/ImageServer/exportImage",
  "image",3,"2020–2025","Maryland iMAP",
  "https://mdgeodata.md.gov/imagery/rest/services/ThreeInch/MD_ThreeInchImagery/ImageServer"),
 "MD_6IN":("Maryland statewide 6-inch orthophotos",
  "https://mdgeodata.md.gov/imagery/rest/services/SixInch/SixInchImagery/ImageServer/exportImage",
  "image",6,"2023–2025","Maryland iMAP",
  "https://mdgeodata.md.gov/imagery/rest/services/SixInch/SixInchImagery/ImageServer"),
 "NC_LATEST":("North Carolina latest 6-inch statewide orthophotos",
  "https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_Latest/ImageServer/exportImage",
  "image",6,"varies by county","NC OneMap / NC 911 Board",
  "https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_Latest/ImageServer"),
 "USGS_PLUS":("USGS NAIP Plus national aerial photography",
  "https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer/exportImage",
  "image",None,"varies by location","USGS / USDA",
  "https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer"),
 "USGS_NAIP":("USGS NAIP national imagery fallback",
  "https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer/exportImage",
  "image",None,"varies by location","USGS / USDA",
  "https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer"),
}
for block in range(1,5):
 for side in ("East","West"):
  key=f"IL_{block}_{side.upper()}"
  path=f"Imagery/IL_Blk{block}_{side}_2025/ImageServer"
  endpoint=f"https://data.isgs.illinois.edu/arcgis/rest/services/{path}"
  SOURCES[key]=(f"Illinois 2025 block {block} {side.lower()} 6-inch orthophotos",
    endpoint+"/exportImage","image",6,"2025","Illinois State Geological Survey",endpoint)

COUNTY_OVERRIDE={
 "06055":("CA_NAPA_2025",),
 "06073":("CA_SAN_DIEGO_2023_9IN","CA_SAN_DIEGO_2017_4IN"),
 "18057":("IN_HAMILTON_2024_3IN",),
 "18081":("IN_JOHNSON_NORTH_2025",),
 "39089":("OH_LICKING_2025",),
 # FIPS from Census geographies API. County point bbox is used only when FIPS is unavailable.
 "17031":("IL_COOK",),
 "12083":("FL_MARION_2024","FL_MARION"),
}

STATE_SERVICES={
 "MD":("MD_3IN","MD_6IN"),
 "OH":("OH_OSIP_DYNAMIC",),
 "IN":("IN_CURRENT",),
 "CA":("CA_CDFW_NAIP_2022",),
 "NC":("NC_LATEST",),
}
# Massachusetts 2025 public TILE cache is in frontend (3-inch Cape Cod; 6-inch elsewhere).
# Kentucky's 2022-2024 3-inch TILE cache is in frontend.
PUBLIC_TILE_STATES={"KY","MA"}

def select_government_sources(state,lat,lon,county_fips=""):
 state=str(state or "").upper()
 county_fips=str(county_fips or "")
 chosen=list(COUNTY_OVERRIDE.get(county_fips,()))
 if state=="CA" and not county_fips:
  # Conservative address-search fallback limited to central Napa or the
  # San Diego metro. Do not guess county from a statewide rectangle.
  if 38.18<=lat<=38.56 and -122.52<=lon<=-122.10:
   chosen.append("CA_NAPA_2025")
  if 32.55<=lat<=33.1 and -117.34<=lon<=-116.82:
   chosen.extend(("CA_SAN_DIEGO_2023_9IN","CA_SAN_DIEGO_2017_4IN"))
 if state=="IL":
  # If Census county lookup is down, retain a conservative Cook County
  # approximate region for the previously supported Chicago-area addresses.
  if not county_fips and 41.35<=lat<=42.25 and -88.4<=lon<=-87.45:
   chosen.append("IL_COOK")
  # Approximate 2025 acquisition block boundaries based on service extents.
  # A missing/non-covered tile must fall back instead of being counted complete.
  block=1 if lat>=41.0 else 2 if lat>=40.0 else 3 if lat>=38.5 else 4
  side="EAST" if lon>-89.2 else "WEST"
  counterpart="WEST" if side=="EAST" else "EAST"
  # First preferred geographic block, then adjacent for edge/mosaic coverage.
  for b in (block, max(1,block-1),min(4,block+1)):
   for orientation in (side,counterpart):
    key=f"IL_{b}_{orientation}"
    if key not in chosen:chosen.append(key)
 elif state=="FL" and not county_fips:
  if 28.94<=lat<=29.56 and -82.58<=lon<=-81.58:
   chosen.extend(("FL_MARION_2024","FL_MARION"))
 if state=="FL" and 25.7<=lat<=29.55 and -83.5<=lon<=-81.15:
  chosen.append("FL_SW")
 chosen.extend(STATE_SERVICES.get(state,()))
 chosen.extend(("USGS_PLUS","USGS_NAIP"))
 return list(dict.fromkeys(chosen))

def coverage_summary():
 # This shows registry progress only. It does not claim counties verified.
 curated={"KY":"3-inch state tile service","MA":"2025 3/6-inch state tile service",
   "OH":"OSIP statewide 2018-2025 mixed-resolution cache; Licking 3-inch and Stark 6-inch county sources",
   "IN":"Indiana latest 2022-2025 6-inch generally, selected 3-inch; 2026 bulk files in 9 counties not live",
   "CA":"58 counties tracked; Napa 2025 ~3-inch and San Diego 2023 9-inch; statewide 2022 60cm baseline is not 3-inch",
   "MD":"partial 3-inch plus statewide 6-inch","NC":"statewide latest 6-inch",
   "IL":"2025 regional 6-inch block services plus Cook County",
   "FL":"selected county/district high-resolution services"}
 return {
  "states_total":len(STATE_CODES),
  "states_with_curated_regional_sources":len(curated),
  "curated_states":curated,
  "states_using_national_fallback":sorted(STATE_CODES-set(curated)),
  "county_audits_completed":0,
  "disclaimer":"No state or county is certified complete without spot tests, service rights, footprint verification, and current imagery review."
 }
