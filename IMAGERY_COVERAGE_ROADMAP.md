# LawnQuote nationwide public-aerial imagery rollout

Updated 2026-10-19. This is a **coverage audit and implementation tracker**, not a claim that county imagery is live, licensed, or three-inch resolution everywhere.

## Acceptance criteria for each county

- [ ] Identify the county FIPS and authoritative government GIS publisher.
- [ ] Locate the most recent public imagery, year, native resolution (prefer <= 3 inches, then 6 inches), and exact image-service URL or tiled cache.
- [ ] Verify imagery footprint contains representative urban and rural properties inside the county.
- [ ] Request at least three sample rooftop views and check source, response status, blank tiles, alignment, and actual sharpness at residential zoom.
- [ ] Review license, attribution requirements, commercial use, and API rate limits. Public viewability alone does not equal license approval.
- [ ] Add vetted service to the priority registry with FIPS/footprint conditions and fallback; include automated regression tests.
- [ ] Mark county completed only once production requests and rights are checked.

## Coverage audit — state by state

| State | Code | Current implementation | County audits |
|---|---|---|---|
| Kentucky | KY | State 3-inch cached tiles in app (KyFromAbove 2022–2024); county-level audit pending | Not complete |
| Florida | FL | Marion County 2024 first, 2023 backup, SW regional service; other counties national backup pending | Not complete |
| Illinois | IL | Cook County 2025 6-inch plus eight 2025 Illinois 6-inch regional blocks cataloged; coverage excludes some collar counties; county audit pending | Not complete |
| Maryland | MD | 3-inch service in selected areas 2020–2025; 6-inch statewide 2023–2025; county footprint audit pending | Not complete |
| North Carolina | NC | Statewide latest 6-inch imagery service cataloged; county vintage, service response and rights audit pending | Not complete |
| Massachusetts | MA | State 2025 cached tiles in app: 6-inch statewide, 3-inch on Cape Cod; county-level audit pending | Not complete |
| Alaska | AK | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Alabama | AL | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Arkansas | AR | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Arizona | AZ | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| California | CA | Napa 2025 ~2.94-inch, San Diego 2023 public 9-inch, CDFW statewide 2022 60-cm baseline; [58-county tracker](CALIFORNIA_COUNTY_TRACKER.md) | 0/58 audited |
| Colorado | CO | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Connecticut | CT | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| District of Columbia | DC | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Delaware | DE | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Georgia | GA | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Hawaii | HI | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Iowa | IA | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Idaho | ID | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Indiana | IN | IGIO current 2022–2025 statewide streaming candidate, generally six-inch with three-inch areas; Hamilton 2024 3-inch and Johnson North 2025 overrides; 2026 three-inch download releases in nine counties; [92-county tracker](INDIANA_COUNTY_TRACKER.md) | 0/92 audited |
| Kansas | KS | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Louisiana | LA | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Maine | ME | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Michigan | MI | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Minnesota | MN | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Missouri | MO | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Mississippi | MS | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Montana | MT | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| North Dakota | ND | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Nebraska | NE | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| New Hampshire | NH | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| New Jersey | NJ | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| New Mexico | NM | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Nevada | NV | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| New York | NY | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Ohio | OH | Ohio OSIP statewide 2018–2025 cached aerials for all 88 counties; 2025 Licking 3-inch and Stark 6-inch sources; **88 county audits outstanding** — [register](OHIO_COUNTY_TRACKER.md) | Not complete |
| Oklahoma | OK | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Oregon | OR | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Pennsylvania | PA | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Rhode Island | RI | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| South Carolina | SC | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| South Dakota | SD | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Tennessee | TN | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Texas | TX | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Utah | UT | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Virginia | VA | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Vermont | VT | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Washington | WA | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Wisconsin | WI | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| West Virginia | WV | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |
| Wyoming | WY | Federal USDA/USGS aerial fallback only; public 3–6-inch imagery research pending | Not complete |

**Current audit status:** 0 states and 0 counties independently certified complete. Curated state/county imagery integrations now exist in **9 states** (CA, IN, OH, KY, FL, IL, MD, NC, MA). This does not guarantee three-inch or even six-inch imagery throughout a state. California has a [58-county tracker](CALIFORNIA_COUNTY_TRACKER.md), Indiana a [92-county tracker](INDIANA_COUNTY_TRACKER.md), and Ohio an [88-county tracker](OHIO_COUNTY_TRACKER.md). Remaining states still rely on federal aerial fallbacks; D.C. is tracked separately.

## Confirmed official public service metadata

- [Kentucky KyFromAbove 3-inch 2022–2024 tiled imagery](https://kygisserver.ky.gov/arcgis/rest/services/WGS84WM_Services/Ky_Imagery_Phase3_3IN_WGS84WM/MapServer)
- [Marion County FL 2024 imagery](https://gis.marionfl.org/image/rest/services/Aerials/Aerial2024/ImageServer)
- [Cook County IL 2025 six-inch imagery](https://gis.cookcountyil.gov/imagery/rest/services/CookOrtho2025/ImageServer/info/iteminfo)
- [Illinois 2025 eight-block six-inch statewide acquisition](https://clearinghouse.isgs.illinois.edu/data/imagery/illinois-911-aerial-acquisition)
- [Maryland three-inch 2020/2023/2024/2025 imagery service](https://mdgeodata.md.gov/imagery/rest/services/ThreeInch/MD_ThreeInchImagery/ImageServer)
- [Maryland statewide six-inch 2023–2025 imagery service](https://mdgeodata.md.gov/imagery/rest/services/SixInch/SixInchImagery/ImageServer)
- [North Carolina latest statewide six-inch imagery service](https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_Latest/ImageServer)
- [Massachusetts 2025 3-inch Cape Cod / 6-inch statewide](https://www.mass.gov/info-details/massgis-data-2025-aerial-imagery)
- [USGS NAIP Plus federal fallback (6 inches to 1 metre depending on location)](https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer)

## Next candidate states with published acquisitions but no fully integrated verified image service

- **Indiana**: 2026 3-inch released for select counties (Bartholomew, Brown, Crawford, Harrison, Jackson, Lawrence, Monroe, Morgan, Orange), and 2025 6-inch leaf-on imagery is releasing county-by-county. Needs imagery REST/COG endpoints and commercial-rights checks ([Indiana GIS update](https://www.in.gov/gis/geoinsights/posts/indiana-leafoff-and-leaf-on-imagery-updates/)).
- **Ohio**: OSIP4 statewide 6-inch collection runs 2025–2028, with 3-inch options purchased locally; determine active services and county footprints ([Ohio OSIP](https://das.ohio.gov/technology-and-strategy/ogrip/projects/osip)).

### Implementation details

- The server's `imagery_registry.py` is the curated provider inventory and FIPS override list. Census geographies identifies county FIPS for each address; fall back to legacy address lookup if Census geographies is unavailable.
- The browser's Kentucky and Massachusetts official public tiled imagery run without an Esri World Imagery subscription; other state and county image servers use their publicly published export endpoints.
- The server checks candidate images for invalid content and nearly uniform/blank rasters, labels the provider and advertised native resolution and year, and falls back when a regional source is unavailable.
- Existing lawn polygon measurement, house exclusion, pricing, and house-pin correction are independent of imagery selection.
- A separate ongoing full-county audit and targeted source integration is required for verified 3–6 inch coverage; neither the code nor a statewide name proves every county has that resolution.
