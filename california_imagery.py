"""California's official 58 counties with individually auditable imagery sources.

Source county FIPS: California state county list / US FIPS 001-115 (odd).
One statewide CDFW 2022/60cm service is a RESOLUTION-LIMITED BASELINE,
not claimed as modern three-inch property photography.
"""
CALIFORNIA_COUNTY_NAMES=["Alameda","Alpine","Amador","Butte","Calaveras","Colusa","Contra Costa","Del Norte","El Dorado","Fresno","Glenn","Humboldt","Imperial","Inyo","Kern","Kings","Lake","Lassen","Los Angeles","Madera","Marin","Mariposa","Mendocino","Merced","Modoc","Mono","Monterey","Napa","Nevada","Orange","Placer","Plumas","Riverside","Sacramento","San Benito","San Bernardino","San Diego","San Francisco","San Joaquin","San Luis Obispo","San Mateo","Santa Barbara","Santa Clara","Santa Cruz","Shasta","Sierra","Siskiyou","Solano","Sonoma","Stanislaus","Sutter","Tehama","Trinity","Tulare","Tuolumne","Ventura","Yolo","Yuba"]
CALIFORNIA_COUNTIES={f"06{(2*i+1):03d}": name for i,name in enumerate(CALIFORNIA_COUNTY_NAMES)}
assert len(CALIFORNIA_COUNTIES)==58
CALIFORNIA_STATE_NAIP_2022="https://gis.wildlife.ca.gov/images/rest/services/Base_Remote_Sensing/NAIP_2022/ImageServer"
CALIFORNIA_NAIP_RIGHTS="https://catalog.data.gov/dataset/naip-2022-60cm-california"
LOCAL_PROVIDERS={
 "06055":{"provider":"CA_NAPA_2025","name":"Napa County April 2025",
  "native_inches":round(0.07464553541190348*39.3700787,2),"year":2025,
  "rights":"Public imagery service; commercial reuse/redistribution needs confirmation",
  "public_source":"https://gis.napa.ca.gov/arcgis/rest/services/OrthoImagery/NapaCountyTiles2025/ImageServer"},
 "06073":{"provider":"CA_SAN_DIEGO_2023_9IN","name":"SANDAG San Diego 2023",
  "native_inches":9,"year":2023,
  "rights":"Nine-inch public-domain display per SANDAG/Nearmap partnership; three-inch is partner-only",
  "public_source":"https://gis.sandag.org/sdgis/rest/services/Imagery/SD2023_9inch/ImageServer"},
}
SAN_DIEGO_OLD_4IN={"provider":"CA_SAN_DIEGO_2017_4IN","native_inches":4,"year":2017,
 "rights":"2017 four-inch service described as public domain; older than 2023 nine-inch mosaic",
 "public_source":"https://gis.sandag.org/sdgis/rest/services/Imagery/SD2017_4inch/ImageServer"}
# LA County acquired 2023 four-inch orthos (LARIAC7); public ArcGIS service
# currently advertises land cover derivatives restricted to LARIAC members.
# DO NOT use those derivatives as RGB aerial imagery or imply rights for them.
POTENTIAL_RESTRICTED={
 "06037":{"name":"Los Angeles","resolution_candidate_inches":4,"year":2023,
  "status":"LARIAC7 RGB 2023 not verified as publicly reusable tile service; do not activate restricted landcover derivative"}
}
def california_county_info(fips):
 fips=str(fips or "")
 name=CALIFORNIA_COUNTIES.get(fips)
 if not name:return None
 local=LOCAL_PROVIDERS.get(fips)
 restricted=POTENTIAL_RESTRICTED.get(fips)
 return {
  "fips":fips,"county":name,
  "statewide_streaming_source":"CA_CDFW_NAIP_2022",
  "statewide_year":2022,"statewide_native_inches":round(0.6*39.3700787,2),
  "statewide_rights":"California CDFW NAIP 2022: CC BY, attribution required",
  "preferred_county_source":local["provider"] if local else "CA_CDFW_NAIP_2022",
  "county_source_year":local["year"] if local else None,
  "county_source_native_inches":local["native_inches"] if local else None,
  "county_source_reference":local["public_source"] if local else "",
  "county_source_rights":local["rights"] if local else "",
  "restricted_or_unverified_higher_resolution":restricted or None,
  "county_source_configured":bool(local),
  "county_completed":False,
  "county_audit_status":"Awaiting 3 live address tests; actual coverage, pixel size/year and licensing/reuse verification",
  "notes":"USGS NAIP Plus can be newer than the explicit California 2022 baseline; no statewide three-inch source is known."}
def california_summary():
 rows=[california_county_info(f) for f in CALIFORNIA_COUNTIES]
 return {
  "state":"CA","county_count":58,"statewide_source_configured":True,
  "statewide_resolution_inches_approx":round(0.6*39.3700787,2),
  "statewide_year":2022,"statewide_fallback_quality":"Lower-resolution 60-cm public aerial",
  "county_specific_sources_configured":len(LOCAL_PROVIDERS),
  "restricted_newer_orthos_count":len(POTENTIAL_RESTRICTED),
  "county_audits_completed":0,
  "county_rows":rows,
  "disclaimer":"All 58 counties tracked and statewide imagery configured, but zero counties independently quality/rights verified. No 3-inch promise statewide."}
