# Houston–Pasadena–The Woodlands metro imagery: actual high-resolution status

Updated 2026-10-20. **Metro #5 in July 2025 Census population ranking.**

## Currently configured public imagery sources

| Geographic area | Source | Native ground pixel size | Vintage | Integration & status |
|---|---|---|---|---|
| City of Galveston image-service footprint (part of broader Houston area; may extend beyond city boundary) | [Galveston 2026 ImageServer](https://gis.galvestontx.gov/image/rest/services/Basemap/Aerial_2026/ImageServer), newer published imagery | not verified | 2026 | Preferred candidate where raster data actually exists; live image QA and rights pending |
| Same restricted Galveston footprint | [Galveston 2025 ImageServer](https://gis.galvestontx.gov/image/rest/services/Basemap/AERIALS_Aerial_2025/ImageServer) | **0.0833333 State Plane feet = 1 inch** | 2025 | First high-detail fallback, based on official pixel-size metadata; independent residential QA/rights pending |
| Restricted Galveston footprint | [Galveston 2024 ImageServer](https://gis.galvestontx.gov/image/rest/services/Basemap/Aerials2024/ImageServer) | **0.25 State Plane feet = 3 inches** | 2024 | Older high-detail fallback, live QA/rights pending |
| Rest of Houston/Pasadena/Woodlands, including Harris County and most suburbs | [USGS NAIP Plus federal orthoimages](https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer) and plain NAIP | 6 inches to 1 meter, depends on actual address; most locations are significantly coarser | varies | Currently permitted/public government fallback, potentially blurry |

**Geographic routing warning:** Galveston City's 2026/2025 mosaic is not the same as Galveston County and definitely not all Houston. The app selects this source only for a conservative geographic extent in the southern metro, then checks the returned image for empty/invalid tiles before display. It is never offered for Houston proper based on metro classification alone.

**Licensing warning:** An ArcGIS ImageServer being publicly viewable does **not** automatically grant permission to commercially redistribute/rehost its image pixels. Commercial terms and attribution for the Galveston services must be confirmed with the City. This app requests on demand, labels the source, and does not bulk-copy those orthos.

## True Houston-wide 2024 six-inch images — commercial access required

The [Houston-Galveston Area Council (H-GAC) 2024 orthoimagery program](https://www.h-gac.com/imagery/aerial) offers **6-inch and 12-inch RGB/infrared aerials** across up to 13 regional counties, though coverage may be partial. It is a paid imagery program. The agency publishes county and tile prices. It does not present an unrestricted free commercial image API and typically distributes MrSID aerial files through FTP or physical storage. Therefore it has **not** been added as a free live imagery service in LawnQuote. A buyer would need to clarify permitted commercial SaaS display, per-property streaming and caching, redistribution, number of users, and image attribution; then arrange tiling/hosting of the purchased data or a licensed streaming endpoint.

The [Texas Imagery Service (TxGIO / Hexagon / Sanborn)](https://gio.texas.gov/texas-imagery-service.html) also streams statewide **6-inch licensed imagery** (2022–2024) **to government agencies and certain eligible contractors**. Its license restricts redistribution and commercial resale. That URL is intentionally *not* wired into LawnQuote's commercial owner SaaS.

## Remaining work before Houston is “high resolution complete”

1. Determine legally available recent 3- or 6-inch imagery for **Harris County**, including Houston, Pasadena, Kingwood/Humble, and suburban Houston; compare H-GAC licensed terms against commercial alternatives.
2. Expand suburb coverage (Fort Bend County: Sugar Land and Missouri City; Montgomery: The Woodlands and Conroe; Brazoria: Pearland; Waller: Katy; Galveston: League City, Texas City, and Galveston). The City of Galveston mosaic does *not* cover all these areas.
3. Verify detailed 2026 and 2025 Galveston image exports at three residential test properties; confirm footprint gaps, real per-location sharpness, service response and commercial rights.
4. For licensed commercial sources, host tiled data in appropriately permissioned storage / CDN or integrate an expressly licensed imagery endpoint rather than circumventing restricted services.
5. Mark the Houston metro "audited" only when the entire priority urban-and-suburban footprint has been reviewed. Current progress is **partial**, and metro QA complete = **false**.

The existing polygon/lawn calculation and pricing are independent of imagery provider resolution.
