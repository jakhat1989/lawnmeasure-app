"""Official Ohio 88 counties (2026 Census FIPS) and imagery audit tracker.

State OSIP cached imagery is configured across Ohio; a county is NOT considered
audited until service, coverage, native resolution, year, licensing and several
representative addresses have been checked. No faux 3-inch blanket claims.
Source names/FIPS: https://tigerweb.geo.census.gov/tigerwebmain/Files/acs26/tigerweb_acs26_county_oh.html
"""
OHIO_COUNTY_NAMES=["Adams","Allen","Ashland","Ashtabula","Athens","Auglaize","Belmont","Brown","Butler","Carroll","Champaign","Clark","Clermont","Clinton","Columbiana","Coshocton","Crawford","Cuyahoga","Darke","Defiance","Delaware","Erie","Fairfield","Fayette","Franklin","Fulton","Gallia","Geauga","Greene","Guernsey","Hamilton","Hancock","Hardin","Harrison","Henry","Highland","Hocking","Holmes","Huron","Jackson","Jefferson","Knox","Lake","Lawrence","Licking","Logan","Lorain","Lucas","Madison","Mahoning","Marion","Medina","Meigs","Mercer","Miami","Monroe","Montgomery","Morgan","Morrow","Muskingum","Noble","Ottawa","Paulding","Perry","Pickaway","Pike","Portage","Preble","Putnam","Richland","Ross","Sandusky","Scioto","Seneca","Shelby","Stark","Summit","Trumbull","Tuscarawas","Union","Van Wert","Vinton","Warren","Washington","Wayne","Williams","Wood","Wyandot"]
OHIO_COUNTIES={
  f"39{2*i+1:03d}":name for i,name in enumerate(OHIO_COUNTY_NAMES)
}
assert len(OHIO_COUNTIES)==88
OHIO_SPECIAL={
  "39089":{"provider":"OH_LICKING_2025","year":2025,"native_inches":3,
    "evidence":"https://apps.lickingcounty.gov/arcgis/rest/services/Basemaps/Imagery2025/MapServer",
    "notes":"Official county 2025 3-inch service; REST map export image endpoint configured, actual live crop not independently verified."},
  "39151":{"provider":"OH_STARK_2025","year":2025,"native_inches":6,
    "evidence":"https://tiles.arcgis.com/tiles/1JiK2PayqrHvvJhM/arcgis/rest/services/Aerial_2025/MapServer",
    "notes":"Stark County 2025 6-inch cached tiles; needs multi-address display QA."},
}
OSIP_CACHE="https://maps.ohio.gov/image/rest/services/osip_most_current_cache/MapServer"
OSIP_INDEX="https://maps.ohio.gov/arcgis/rest/services/Hosted/OSIP_Index_June_2026/FeatureServer/0"

def ohio_county_info(fips):
 fips=str(fips or "")
 name=OHIO_COUNTIES.get(fips)
 if not name:return None
 local=OHIO_SPECIAL.get(fips)
 return {
    "fips":fips,"county":name,
    "state_cached_imagery":"OSIP most-current cache, 2018–2025 mosaics",
    "statewide_source_url":OSIP_CACHE,
    "county_preferred_source":local["provider"] if local else "OH_OSIP_CACHE",
    "candidate_year":local["year"] if local else None,
    "candidate_native_inches":local["native_inches"] if local else None,
    "source_evidence":local["evidence"] if local else OSIP_INDEX,
    "integration_status":"county_source_configured_not_verified" if local else "statewide_source_configured",
    "county_completed":False,
    "county_audit_status":"pending sample image, footprint, year/resolution and reuse-rights check",
    "notes":local["notes"] if local else "Statewide OSIP mosaic covers Ohio; actual county pixel resolution and image year vary."
 }

def ohio_summary():
 rows=[ohio_county_info(code) for code in OHIO_COUNTIES]
 return {"state":"OH","county_count":len(rows),"statewide_source_configured":True,
         "county_specific_sources_configured":len(OHIO_SPECIAL),
         "county_audits_completed":sum(int(row["county_completed"]) for row in rows),
         "year_range":"2018–2025 (mixed imagery in OSIP cached mosaic; index updated 2026)",
         "target_native_inches":3,
         "baseline_native_inches":None,
         "coverage_claim":"Statewide tiled OSIP imagery available for Ohio; no guarantee of 3-inch or newest imagery at every house.",
         "county_rows":rows}
