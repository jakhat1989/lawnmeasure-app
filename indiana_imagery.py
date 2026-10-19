"""Indiana 92-county live imagery registry and review tracker (2026-10-19).
Official county FIPS list: https://tigerweb.geo.census.gov/tigerwebmain/Files/acs26/tigerweb_acs26_county_in.html
Some 2026 three-inch datasets are bulk-download ONLY, not yet streamed through
the 2022-2025 current ImageServer. Do not falsely call a file release live.
"""
INDIANA_COUNTY_NAMES=["Adams","Allen","Bartholomew","Benton","Blackford","Boone","Brown","Carroll","Cass","Clark","Clay","Clinton","Crawford","Daviess","Dearborn","Decatur","DeKalb","Delaware","Dubois","Elkhart","Fayette","Floyd","Fountain","Franklin","Fulton","Gibson","Grant","Greene","Hamilton","Hancock","Harrison","Hendricks","Henry","Howard","Huntington","Jackson","Jasper","Jay","Jefferson","Jennings","Johnson","Knox","Kosciusko","LaGrange","Lake","LaPorte","Lawrence","Madison","Marion","Marshall","Martin","Miami","Monroe","Montgomery","Morgan","Newton","Noble","Ohio","Orange","Owen","Parke","Perry","Pike","Porter","Posey","Pulaski","Putnam","Randolph","Ripley","Rush","St. Joseph","Scott","Shelby","Spencer","Starke","Steuben","Sullivan","Switzerland","Tippecanoe","Tipton","Union","Vanderburgh","Vermillion","Vigo","Wabash","Warren","Warrick","Washington","Wayne","Wells","White","Whitley"]
INDIANA_COUNTIES={f"18{(2*i+1):03d}":name for i,name in enumerate(INDIANA_COUNTY_NAMES)}
assert len(INDIANA_COUNTIES)==92
INDIANA_CURRENT_URL="https://di-ingov.img.arcgis.com/arcgis/rest/services/DynamicWebMercator/Indiana_Current_Imagery/ImageServer"
INDIANA_HAMILTON_2024_URL="https://di-ingov.img.arcgis.com/arcgis/rest/services/DynamicWebMercator/Indiana_County_Collect_2024_Imagery/ImageServer"
INDIANA_PUBLIC_DOMAIN_SOURCE="https://www.in.gov/gis/geoinsights/posts/indiana-leafoff-and-leaf-on-imagery-updates/"
# The Indiana Geographic Information Office publicly released these counties in
# September 2026 as 3-inch COG files, but their current streaming service only
# advertises imagery through 2025. They must not be claimed as loaded in LawnQuote.
INDIANA_2026_3IN_DOWNLOAD_COUNTIES=frozenset({
 "Bartholomew","Brown","Crawford","Harrison","Jackson",
 "Lawrence","Monroe","Morgan","Orange",
})
INDIANA_2025_6IN_LEAF_ON_DOWNLOAD_COUNTIES=frozenset({
 "Gibson","Knox","Lake","Newton","Pike","Posey","Sullivan",
 "Vanderburgh","Vermillion","Vigo","Warrick",
})
INDIANA_LOCAL_STREAMED={
 "18057":{"provider":"IN_HAMILTON_2024_3IN","year":2024,
         "native_inches":3,"area":"Hamilton County",
         "source_url":INDIANA_HAMILTON_2024_URL,
         "note":"Official 2024 3-inch Hamilton orthophotography ImageServer."},
 "18081":{"provider":"IN_JOHNSON_NORTH_2025","year":2025,
         "native_inches":None,"area":"North Johnson County / Greenwood (partial)",
         "source_url":"https://greenwoodgis.greenwood.in.gov/arcgis/rest/services/Ortho/JCNorth2025Ortho/MapServer",
         "note":"Official 2025 northern Johnson acquisition; pixels and full county coverage unverified."},
}
def indiana_county_info(fips):
 fips=str(fips or "")
 name=INDIANA_COUNTIES.get(fips)
 if not name:return None
 local=INDIANA_LOCAL_STREAMED.get(fips)
 bulk2026=name in INDIANA_2026_3IN_DOWNLOAD_COUNTIES
 leaf2025=name in INDIANA_2025_6IN_LEAF_ON_DOWNLOAD_COUNTIES
 return {
  "fips":fips,"county":name,
  "base_source":"Indiana current orthophotography ImageServer (2022-2025)",
  "base_source_url":INDIANA_CURRENT_URL,
  "base_native_inches":"6-inch generally, some 3-inch areas; per-address varies",
  "preferred_streaming_source":local["provider"] if local else "IN_CURRENT",
  "local_streaming_vintage":local["year"] if local else None,
  "local_native_inches":local["native_inches"] if local else None,
  "local_streaming_extent":local["area"] if local else "",
  "local_source_url":local["source_url"] if local else "",
  "has_2026_three_inch_bulk_release":bulk2026,
  "has_2025_six_inch_leafon_bulk_release":leaf2025,
  "bulk_release_note":(
   "2026 3-inch leaf-off download available; not confirmed in current live map service"
   if bulk2026 else
   "2025 6-inch leaf-on download available; current live map service may be different"
   if leaf2025 else ""),
  "status":"local_streaming_source_configured" if local else "state_current_streaming_source_configured",
  "county_completed":False,
  "county_audit_status":"Pending multi-address rooftop QA, pixel size/year/footprint validation, license and source-response verification",
 }
def indiana_summary():
 rows=[indiana_county_info(fips) for fips in INDIANA_COUNTIES]
 return {
  "state":"IN","county_count":92,"state_current_imagery_configured":True,
  "current_live_service_years":"2022–2025",
  "general_native_inches":6,"some_native_three_inch":True,
  "local_streaming_source_count":len(INDIANA_LOCAL_STREAMED),
  "county_2026_three_inch_bulk_release_count":len(INDIANA_2026_3IN_DOWNLOAD_COUNTIES),
  "county_2025_six_inch_leafon_bulk_release_count":len(INDIANA_2025_6IN_LEAF_ON_DOWNLOAD_COUNTIES),
  "county_audits_completed":0,
  "license":"IGIO current service: CC0/public domain; other county endpoints require individual review",
  "disclaimer":"No Indiana county is certified image-clear and newest three-inch across all homes. 2026 downloads are not yet live in our map.",
  "county_rows":rows,
 }
