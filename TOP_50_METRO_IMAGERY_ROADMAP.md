# LawnQuote: 50 largest U.S. metropolitan areas — imagery priority

Last updated 2026-10-19. **This is the active imagery improvement focus.**
The previous 50-state and individual-county source research is retained for reuse, but we will prioritize the **top 50 metropolitan statistical areas (MSAs)** by official July 1, 2025 Census estimated population.

## Why metros instead of cities or every county

Metropolitan statistical areas are defined by OMB and comprise the urban core **plus economically connected surrounding counties and suburbs**. This avoids excluding major suburban markets (e.g. Fort Worth, Naperville, Northern Kentucky, Anaheim) simply because they are outside a principal-city limit.

Official ranking: [U.S. Census Bureau, CBSA-MET-EST2025-POP](https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-metro-and-micro-statistical-areas.html).
Official MSA footprints: [Census delineation files](https://www.census.gov/programs-surveys/metro-micro/about/delineation-files.html), served as 2025 polygon data from [TIGERweb Census ArcGIS MapServer metropolitan areas (layer 15)](https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/CBSA/MapServer/15).

## Current implementation

- 50/50 metro target entries registered in `metro_imagery.py`.
- Address lookup now requests Census **Metropolitan Statistical Areas** geography and can query 2025 TIGERweb MSA polygons by location. A suburb inside an official metro is identified as belonging to that target even when the address is not in the core city.
- Authenticated `/api/top-metros` returns ranked targets and audit progress. The main app has a **Top 50 metro-area imagery tracker**.
- Local government and statewide image sources from earlier work are still selected as before; other markets retain national government fallbacks. Out-of-scope addresses can still be measured and quoted.
- **No imagery provider is newly certified as sharp or licensed metro-wide.** 0 of 50 areas have been independently audited end to end.

## Active Houston metro improvement (priority #5)

[Detailed Houston/Galveston imagery implementation and licensing status](HOUSTON_METRO_IMAGERY.md): public City of Galveston aerial photography **2026** (native pixel size not yet confirmed), **2025 at 1-inch**, and **2024 at 3-inch**, routed only within the city's conservative public mosaic footprint. These sources do **not** cover most of Harris, Fort Bend, Montgomery, Brazoria or the wider Houston metro. H-GAC's **2024 six-inch regional imagery** is sold under license rather than being free commercial imagery. Existing USGS NAIP Plus remains the fallback for most Houston addresses. Houston metro QA is still **pending**.

## Metro-by-metro imagery QA criteria

- [ ] Record Census MSA CBSA code and complete county membership/boundaries, including multi-state suburban counties.
- [ ] Discover official county/city/state/municipal orthoimagery across the metropolitan footprint, preferring **latest available near-3-inch native pixels**, then 6-inch or better where possible.
- [ ] Compare imagery **capture year** against pixel resolution; newer 6-inch may be more useful than older 3-inch.
- [ ] Check free/commercial image rights, attribution and rate limits; public image visibility alone is not commercial redistribution permission.
- [ ] Verify coverage, color, alignment, no-data boundaries and **three real residential test sites per metro subregion** before marking that metro complete.
- [ ] Preserve an explicit fall back to existing government imagery; never upscale a low-res photo while labeling it sharp.
- [ ] Update metro-specific source priority and regression tests when each verified service is integrated.

## Fifty target metros

| Rank | Official 2025 metropolitan statistical area | Estimated population July 2025 | Source audit | End-to-end QA |
|---:|---|---:|---|---|
| 1 | New York-Newark-Jersey City, NY-NJ | 20,112,448 | Pending city/county imagery review | Not complete |
| 2 | Los Angeles-Long Beach-Anaheim, CA | 12,844,441 | Pending city/county imagery review | Not complete |
| 3 | Chicago-Naperville-Elgin, IL-IN | 9,434,123 | Pending city/county imagery review | Not complete |
| 4 | Dallas-Fort Worth-Arlington, TX | 8,477,157 | Pending city/county imagery review | Not complete |
| 5 | Houston-Pasadena-The Woodlands, TX | 7,904,627 | Pending city/county imagery review | Not complete |
| 6 | Atlanta-Sandy Springs-Roswell, GA | 6,482,182 | Pending city/county imagery review | Not complete |
| 7 | Washington-Arlington-Alexandria, DC-VA-MD-WV | 6,465,724 | Pending city/county imagery review | Not complete |
| 8 | Miami-Fort Lauderdale-West Palm Beach, FL | 6,391,072 | Pending city/county imagery review | Not complete |
| 9 | Philadelphia-Camden-Wilmington, PA-NJ-DE-MD | 6,329,118 | Pending city/county imagery review | Not complete |
| 10 | Phoenix-Mesa-Chandler, AZ | 5,228,938 | Pending city/county imagery review | Not complete |
| 11 | Boston-Cambridge-Newton, MA-NH | 5,034,221 | Pending city/county imagery review | Not complete |
| 12 | Riverside-San Bernardino-Ontario, CA | 4,769,007 | Pending city/county imagery review | Not complete |
| 13 | San Francisco-Oakland-Fremont, CA | 4,630,041 | Pending city/county imagery review | Not complete |
| 14 | Detroit-Warren-Dearborn, MI | 4,390,913 | Pending city/county imagery review | Not complete |
| 15 | Seattle-Tacoma-Bellevue, WA | 4,161,883 | Pending city/county imagery review | Not complete |
| 16 | Minneapolis-St. Paul-Bloomington, MN-WI | 3,790,295 | Pending city/county imagery review | Not complete |
| 17 | Tampa-St. Petersburg-Clearwater, FL | 3,418,895 | Pending city/county imagery review | Not complete |
| 18 | San Diego-Chula Vista-Carlsbad, CA | 3,282,248 | Pending city/county imagery review | Not complete |
| 19 | Denver-Aurora-Centennial, CO | 3,092,037 | Pending city/county imagery review | Not complete |
| 20 | Orlando-Kissimmee-Sanford, FL | 2,957,672 | Pending city/county imagery review | Not complete |
| 21 | Charlotte-Concord-Gastonia, NC-SC | 2,938,830 | Pending city/county imagery review | Not complete |
| 22 | Baltimore-Columbia-Towson, MD | 2,857,781 | Pending city/county imagery review | Not complete |
| 23 | St. Louis, MO-IL | 2,814,421 | Pending city/county imagery review | Not complete |
| 24 | San Antonio-New Braunfels, TX | 2,813,140 | Pending city/county imagery review | Not complete |
| 25 | Austin-Round Rock-San Marcos, TX | 2,620,945 | Pending city/county imagery review | Not complete |
| 26 | Portland-Vancouver-Hillsboro, OR-WA | 2,542,282 | Pending city/county imagery review | Not complete |
| 27 | Sacramento-Roseville-Folsom, CA | 2,477,274 | Pending city/county imagery review | Not complete |
| 28 | Pittsburgh, PA | 2,421,992 | Pending city/county imagery review | Not complete |
| 29 | Las Vegas-Henderson-North Las Vegas, NV | 2,407,226 | Pending city/county imagery review | Not complete |
| 30 | Cincinnati, OH-KY-IN | 2,312,858 | Pending city/county imagery review | Not complete |
| 31 | Kansas City, MO-KS | 2,270,682 | Pending city/county imagery review | Not complete |
| 32 | Columbus, OH | 2,242,028 | Pending city/county imagery review | Not complete |
| 33 | Indianapolis-Carmel-Greenwood, IN | 2,205,695 | Pending city/county imagery review | Not complete |
| 34 | Nashville-Davidson--Murfreesboro--Franklin, TN | 2,197,416 | Pending city/county imagery review | Not complete |
| 35 | Cleveland, OH | 2,165,775 | Pending city/county imagery review | Not complete |
| 36 | San Jose-Sunnyvale-Santa Clara, CA | 1,984,473 | Pending city/county imagery review | Not complete |
| 37 | Virginia Beach-Chesapeake-Norfolk, VA-NC | 1,797,213 | Pending city/county imagery review | Not complete |
| 38 | Jacksonville, FL | 1,785,500 | Pending city/county imagery review | Not complete |
| 39 | Providence-Warwick, RI-MA | 1,708,161 | Pending city/county imagery review | Not complete |
| 40 | Raleigh-Cary, NC | 1,595,720 | Pending city/county imagery review | Not complete |
| 41 | Milwaukee-Waukesha, WI | 1,575,010 | Pending city/county imagery review | Not complete |
| 42 | Oklahoma City, OK | 1,512,813 | Pending city/county imagery review | Not complete |
| 43 | Louisville/Jefferson County, KY-IN | 1,402,509 | Pending city/county imagery review | Not complete |
| 44 | Richmond, VA | 1,389,338 | Pending city/county imagery review | Not complete |
| 45 | Memphis, TN-MS-AR | 1,341,412 | Pending city/county imagery review | Not complete |
| 46 | Salt Lake City-Murray, UT | 1,308,377 | Pending city/county imagery review | Not complete |
| 47 | Fresno, CA | 1,203,383 | Pending city/county imagery review | Not complete |
| 48 | Birmingham, AL | 1,197,766 | Pending city/county imagery review | Not complete |
| 49 | Grand Rapids-Wyoming-Kentwood, MI | 1,183,645 | Pending city/county imagery review | Not complete |
| 50 | Hartford-West Hartford-East Hartford, CT | 1,171,426 | Pending city/county imagery review | Not complete |

## Rollout groups (10 metros per wave)

- **Wave 1 — ranks 1–10:** New York, Los Angeles, Chicago, Dallas–Fort Worth, Houston, Atlanta, Washington DC, Miami, Philadelphia, Phoenix.
- **Wave 2 — ranks 11–20:** Boston, Inland Empire, Bay Area/San Francisco, Detroit, Seattle, Twin Cities, Tampa Bay, San Diego, Denver, Orlando.
- **Wave 3 — ranks 21–30:** Charlotte, Baltimore, St. Louis, San Antonio, Austin, Portland, Sacramento, Pittsburgh, Las Vegas, Cincinnati (including Northern Kentucky).
- **Wave 4 — ranks 31–40:** Kansas City, Columbus, Indianapolis, Nashville, Cleveland, San Jose, Virginia Beach–Norfolk, Jacksonville, Providence, Raleigh.
- **Wave 5 — ranks 41–50:** Milwaukee, Oklahoma City, Louisville, Richmond, Memphis, Salt Lake City, Fresno, Birmingham, Grand Rapids, Hartford.

**Scope note:** The official metro delineation is county-based and may cover a substantial area beyond the visible urban/suburban neighborhood. We use the official boundary for *priority detection*, then focus image-source verification on populated residential neighborhoods throughout the metro's counties.

**No automatic future execution is implied by this roadmap.** This repository tracks completed changes across subsequent implementation sessions.
