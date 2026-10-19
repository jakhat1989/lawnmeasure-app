# Indiana 92-county aerial-imagery tracker
Last reviewed: 2026-10-19

**Official county names/FIPS:** [2026 Census Indiana county list](https://tigerweb.geo.census.gov/tigerwebmain/Files/acs26/tigerweb_acs26_county_in.html).

## Implementation and audit totals

- **92/92 county FIPS records tracked** in `indiana_imagery.py`.
- **92/92 county lookups have a live-source *candidate*:** [Indiana Geographic Information Office current orthoimagery service](https://di-ingov.img.arcgis.com/arcgis/rest/services/DynamicWebMercator/Indiana_Current_Imagery/ImageServer). This statewide service advertises 2022–2025 imagery, generally 6 inches with some 3-inch areas; **CC0/public domain**. Real image resolution, age, and tile availability vary per address.
- **Two local priority services:** Hamilton County 2024 3-inch streamed ortho; North Johnson County/Greenwood 2025 streamed ortho with unverified pixel size and *partial* footprint.
- **Nine counties have released 2026 3-inch leaf-off COG download packages** but these files are **not** claimed to be visible in the currently live 2022–2025 IGIO image service.
- **Eleven counties have released 2025 6-inch leaf-on imagery** as downloadable products; current app prioritizes the IGIO live orthos rather than claiming a file download is accessible as interactive imagery.
- **Counties independently audited for 3+ residential samples, exact acquisition year/pixel size, live response, alignment and use rights:** **0/92**. Do not label Indiana fully finished yet.

Official announcements: [Indiana September 28, 2026 2026 and 2025 imagery releases](https://www.in.gov/gis/geoinsights/posts/indiana-leafoff-and-leaf-on-imagery-updates/); [IGIO official streaming imagery guide](https://www.in.gov/gis/geoinsights/posts/indianas-imagery-services/).

## All 92 counties

| Census GEOID | County | Preferred configured live imagery | New 2026 3-inch download? | 2025 6-inch leaf-on download? | Rooftop QA |
|---|---|---|---|---|---|
| 18001 | Adams | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18003 | Allen | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18005 | Bartholomew | Indiana IGIO current 2022–2025 | Yes — files only | Not listed | Pending |
| 18007 | Benton | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18009 | Blackford | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18011 | Boone | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18013 | Brown | Indiana IGIO current 2022–2025 | Yes — files only | Not listed | Pending |
| 18015 | Carroll | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18017 | Cass | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18019 | Clark | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18021 | Clay | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18023 | Clinton | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18025 | Crawford | Indiana IGIO current 2022–2025 | Yes — files only | Not listed | Pending |
| 18027 | Daviess | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18029 | Dearborn | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18031 | Decatur | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18033 | DeKalb | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18035 | Delaware | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18037 | Dubois | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18039 | Elkhart | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18041 | Fayette | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18043 | Floyd | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18045 | Fountain | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18047 | Franklin | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18049 | Fulton | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18051 | Gibson | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18053 | Grant | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18055 | Greene | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18057 | Hamilton | Hamilton County 2024 3-inch | Not listed | Not listed | Pending |
| 18059 | Hancock | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18061 | Harrison | Indiana IGIO current 2022–2025 | Yes — files only | Not listed | Pending |
| 18063 | Hendricks | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18065 | Henry | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18067 | Howard | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18069 | Huntington | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18071 | Jackson | Indiana IGIO current 2022–2025 | Yes — files only | Not listed | Pending |
| 18073 | Jasper | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18075 | Jay | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18077 | Jefferson | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18079 | Jennings | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18081 | Johnson | Johnson North 2025 partial | Not listed | Not listed | Pending |
| 18083 | Knox | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18085 | Kosciusko | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18087 | LaGrange | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18089 | Lake | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18091 | LaPorte | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18093 | Lawrence | Indiana IGIO current 2022–2025 | Yes — files only | Not listed | Pending |
| 18095 | Madison | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18097 | Marion | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18099 | Marshall | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18101 | Martin | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18103 | Miami | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18105 | Monroe | Indiana IGIO current 2022–2025 | Yes — files only | Not listed | Pending |
| 18107 | Montgomery | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18109 | Morgan | Indiana IGIO current 2022–2025 | Yes — files only | Not listed | Pending |
| 18111 | Newton | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18113 | Noble | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18115 | Ohio | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18117 | Orange | Indiana IGIO current 2022–2025 | Yes — files only | Not listed | Pending |
| 18119 | Owen | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18121 | Parke | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18123 | Perry | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18125 | Pike | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18127 | Porter | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18129 | Posey | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18131 | Pulaski | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18133 | Putnam | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18135 | Randolph | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18137 | Ripley | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18139 | Rush | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18141 | St. Joseph | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18143 | Scott | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18145 | Shelby | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18147 | Spencer | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18149 | Starke | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18151 | Steuben | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18153 | Sullivan | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18155 | Switzerland | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18157 | Tippecanoe | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18159 | Tipton | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18161 | Union | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18163 | Vanderburgh | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18165 | Vermillion | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18167 | Vigo | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18169 | Wabash | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18171 | Warren | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18173 | Warrick | Indiana IGIO current 2022–2025 | Not listed | Yes — files only | Pending |
| 18175 | Washington | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18177 | Wayne | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18179 | Wells | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18181 | White | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |
| 18183 | Whitley | Indiana IGIO current 2022–2025 | Not listed | Not listed | Pending |

## County verification procedure

- [ ] Obtain three or more representative real house coordinates in each county and verify that the high-resolution imagery (not blurred federal backup) loads in LawnQuote.
- [ ] Compare actual official 2025/2026 raster acquisitions to the 2022–2025 live statewide service, recording address-level acquisition year and native inches per pixel.
- [ ] Prefer publicly available 2026 3-inch COG files where legally and technically feasible. A download package is **not** an interactive image service: conversion into a licensed cache/tile server or verified COG tile gateway may be needed.
- [ ] Compare government aerial sources for distinct city/urban, rural, and border properties; reject blank and wrong-extent imagery, confirm map alignment.
- [ ] Document imagery licenses and use terms for county-specific sources (the Indiana state IGIO current service states CC0; not all county GIS services do).
- [ ] Update `indiana_imagery.py` audit status with evidence and test results, then mark county as completed only when all checks pass.

## Change history

2026-10-19: Created all 92 Census FIPS county records; integrated IGIO current 2022–2025 image server, Hamilton County 2024 3-inch and north Johnson County 2025 alternatives, data per-property metadata query, source fallbacks and an Indiana county table in LawnQuote. Released 2026 3-inch county downloads are tracked but **not** served as map imagery. 0 county audits complete.
