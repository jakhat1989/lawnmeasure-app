# California 58-county aerial-imagery tracker

**Started:** October 19, 2026. All 58 California counties have individual FIPS records, a base imagery source, and explicit quality/rights audit tasks. **None is certified complete.**

Source of county names and FIPS: [California Department of Technology counties list](https://data.ca.gov/@california-department-of-technology/county-names) and [California FIPS counties](https://ccrcal.org/wp-content/uploads/V1_2017_Online_Manual/Appendix/Appendix_L_1_Calif_Counties.htm).

## Sources now configured

- **Statewide (58 county lookups)**: California Department of Fish and Wildlife / USDA [NAIP 2022, 60 centimeters (about 23.62 inches)](https://catalog.data.gov/dataset/naip-2022-60cm-california). Public CC BY service (attribution required). This is a **lower-resolution baseline**, not the requested 3-inch result. Federal USGS NAIP Plus and NAIP are additional fallbacks.
- **Napa County** (FIPS 06055): [April 2025 orthoimage service](https://gis.napa.ca.gov/arcgis/rest/services/OrthoImagery/NapaCountyTiles2025/ImageServer). Server-reported pixel size 0.074645535 m (approximately **2.94 inches/pixel**). Source returns an ArcGIS ImageServer; live house image clarity and commercial reuse permission still to be checked.
- **San Diego County** (FIPS 06073): [2023 9-inch SANDAG / SanGIS / Nearmap public-domain ImageServer](https://gis.sandag.org/sdgis/rest/services/Imagery/SD2023_9inch/ImageServer/info/iteminfo). The newer **3-inch native dataset is partner-only**; it cannot be represented as publicly available imagery. [2017 4-inch public image service](https://gis.sandag.org/sdgis/rest/services/Imagery/SD2017_4inch/ImageServer/info/iteminfo) is an older-resolution alternative if the 2023 service fails. This application prioritizes more recent 2023 imagery over 2017, even though the 2017 pixel size is smaller.

### Candidate not activated

- **Los Angeles County (FIPS 06037):** the LARIAC7 **2023 four-inch** photography exists, but the public REST catalog found so far provides [land-cover layers restricted to consortium members](https://cache.gis.lacounty.gov/cache/rest/services/LARIAC7/LANDCOVER_2023/MapServer), rather than an unrestricted RGB aerial cache. We did not enable restricted derivatives as aerial photography.
- **Remaining counties:** state 2022 baseline / national NAIP fallback only, pending service-by-service county research. Do not claim three-inch imagery across California.

## Completion criteria for each county

- [ ] Identify and inspect current official city/county aerial image services with acquisition dates newer than 2022 and native resolution at/near 3 inches.
- [ ] Verify county/municipal coverage footprint, exact service URL, published pixel size and reuse rights, particularly any aerial photography licensed from vendors.
- [ ] Test three distinct residential properties (suburban, urban, rural) and verify actual zoom sharpness, imagery alignment and age against the source service.
- [ ] Ensure fallback doesn't silently show a low-resolution image with a high-resolution label.
- [ ] Pass automated source-precedence tests and correctly credit image providers in the map attribution.
- [ ] Mark completion only when all checks above pass.

## Complete county register

| FIPS | County | Preferred live source | Advertised native detail | QA state |
|---|---|---|---|---|
| 06001 | Alameda | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06003 | Alpine | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06005 | Amador | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06007 | Butte | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06009 | Calaveras | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06011 | Colusa | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06013 | Contra Costa | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06015 | Del Norte | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06017 | El Dorado | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06019 | Fresno | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06021 | Glenn | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06023 | Humboldt | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06025 | Imperial | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06027 | Inyo | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06029 | Kern | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06031 | Kings | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06033 | Lake | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06035 | Lassen | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06037 | Los Angeles | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06039 | Madera | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06041 | Marin | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06043 | Mariposa | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06045 | Mendocino | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06047 | Merced | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06049 | Modoc | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06051 | Mono | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06053 | Monterey | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06055 | Napa | Napa 2025 official high-res -> CA state fallback | ~2.94 in | Pending |
| 06057 | Nevada | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06059 | Orange | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06061 | Placer | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06063 | Plumas | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06065 | Riverside | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06067 | Sacramento | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06069 | San Benito | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06071 | San Bernardino | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06073 | San Diego | San Diego 2023 public 9-inch -> 2017 4-inch older -> CA state fallback | 9 in (2023); 4 in (2017 older) | Pending |
| 06075 | San Francisco | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06077 | San Joaquin | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06079 | San Luis Obispo | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06081 | San Mateo | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06083 | Santa Barbara | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06085 | Santa Clara | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06087 | Santa Cruz | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06089 | Shasta | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06091 | Sierra | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06093 | Siskiyou | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06095 | Solano | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06097 | Sonoma | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06099 | Stanislaus | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06101 | Sutter | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06103 | Tehama | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06105 | Trinity | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06107 | Tulare | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06109 | Tuolumne | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06111 | Ventura | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06113 | Yolo | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |
| 06115 | Yuba | California statewide NAIP 2022 / USGS NAIP+ fallback | 23.62 in (60 cm) state baseline | Pending |

## Change log

- 2026-10-19: Added all 58 counties to `california_imagery.py`. Configured California CDFW statewide baseline and Napa/San Diego county services in `imagery_registry.py`. Added authenticated `/api/california-counties` and county imagery selector in LawnQuote. Work remains for county-level verification and additional high-resolution public aerial services.
