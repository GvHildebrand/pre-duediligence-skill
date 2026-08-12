# The TERRA land reading — API first, browser as fallback

TERRA (`read.dearwise.earth`) is Dear Wise Earth's own land-intelligence engine.
It scores any parcel from live satellite and open-geospatial data (Sentinel-2,
AWS Terrain Tiles, ESA WorldCover, GBIF, ERA5/Open-Meteo, Hansen Global Forest
Change, NASA Black Marble, and SNIT jurisdiction records for Costa Rica). The
reading is the report's one first-party dataset — treat it as CONFIRMED primary
data and build §3 around it.

## Preferred path: call the API directly

The engine is a thin client over an **open JSON API — no authentication, no
browser required.** Generate a reading in one call:

    python3 scripts/terra_read.py --lat 9.7489 --lon -83.7534
    python3 scripts/terra_read.py --geojson parcel.geojson   # exact boundary

Under the hood:

    POST https://read.dearwise.earth/api/dossier
    Content-Type: application/json
    body: { "geometry": { "type": "Polygon", "coordinates": [ ring ] } }

where `ring` is a closed list of `[lon, lat]` pairs. For a centroid read, build
the ~1 km (100 ha) box TERRA uses by default:

    dlat = 0.5/111
    dlon = 0.5/(111*cos(lat))
    ring = [[lon-dlon,lat-dlat],[lon+dlon,lat-dlat],[lon+dlon,lat+dlat],
            [lon-dlon,lat+dlat],[lon-dlon,lat-dlat]]

The response is `200`, ~22 KB of JSON — the entire reading. **Every call publishes
the reading to the public wall** and returns an `id`; the reading of record is
`https://read.dearwise.earth/d/<id>`. Cite it in the report. (Readings are freshly
synthesised each call, so the headline wording and minor scores can shift slightly
between runs — always cite the exact `id` you used.)

### Response shape (top-level keys)

`geometry, area_ha, centroid, place, cadastre, terrain, water, soil, cover,
pressure, ecology, climate, surface_water, deforestation, forest_loss, plantation,
canopy, biomass, ndvi, lst, radar, nightlights, security, corridor, scores,
verdict, deployment, project_model, comparison, ecoregion, meta, id`

The fields that drive §3:

| Report element | JSON path |
|---|---|
| Land score (0–100) | `scores.composite` |
| Pillar scores | `scores.water`, `scores.soil`, `scores.ecology`, `scores.climate_resilience`, `scores.pressure` |
| Data confidence | `scores.data_confidence` |
| Model fit + verdict | `verdict.class`, `verdict.headline`, `verdict.summary` |
| Findings / actions / questions | `verdict.findings[]`, `verdict.actions[]`, `verdict.questions[]`, `verdict.report_narrative[]` |
| Conservation priority & hospitality fit | `deployment.*`, `project_model.*` |
| Climate to 2050 | `climate.*` |
| Forest history (Hansen) | `forest_loss.*`, `deforestation.*` |
| Percentiles vs. like land | `comparison.*` |
| Jurisdiction (SNIT) | `cadastre.*` (and compare to `place.display`) |
| Watercourse | `surface_water.*` |

### Imagery for the report figures

Two GET endpoints, keyless:

    GET /api/imagery/meta?g=<ring-json>                       # available scenes
    GET /api/imagery/render?g=<ring-json>&layer=<layer>&scene=<sceneId>

`g` here is the bare ring (`[[lon,lat],...]`, URL-encoded), not the wrapped
Polygon. Layers include `truecolor` and `ndvi`; pick a recent low-cloud `scene`
from the meta response. Save the rendered PNGs as `fig_*.png` next to the report
HTML. (For the composite score/radar figure, a browser screenshot of the `/d/<id>`
page is still the richest single image — grab it if a browser is connected.)

Other endpoints seen in the app: `GET /api/story?g=…` (rainfall/sun/moon/satellite
almanac), `GET /api/story/visitors?g=…`, `POST /api/lead` (contact capture).

## Flags to hunt in the reading

- **Jurisdiction mismatch.** `cadastre` can resolve to a different cantón/distrito
  than the `place.display` header — meaning a cantonal boundary runs near the
  parcel and determines which municipality issues permits and collects tax. **FLAG.**
- **Forest-history vs. narrative.** If `forest_loss`/`deforestation` show high tree
  cover years back and near-zero loss, but the seller's story is "bare pasture we
  reforested," the satellite record disputes the marketing. **FLAG**, make it a DD item.
- **Watercourse naming.** `surface_water` names the river by its cadastral name,
  which may differ from the seller's; reconcile, and note that a mapped watercourse
  confirms riparian setback rules apply.
- **Low-confidence tree-cover upside.** Satellite land-cover can't tell natural
  forest from monoculture — carry that caveat and make "ground-truth the canopy
  with a botanist" a DD action.

Always state scope honestly: the default read is a 1 km² box at the centroid, not
the exact titled boundary. A boundary-exact re-read (pass `--geojson`) is a Tier-1
DD action.

## Browser fallback (only if the API is unreachable)

If the local network blocks the API call, drive the engine by hand with the
`claude-in-chrome` tools:

1. `navigate` to `https://read.dearwise.earth/engine`.
2. Click the search field, type the coordinates as `LAT, LON`, click **SEARCH**
   (the engine drops the default 100 ha box). Place names also work but are less
   reliable than coordinates.
3. Click **READ THIS PARCEL**; it computes for up to ~60 s. Wait, then
   `get_page_text` to capture the whole reading, and screenshot the score/radar
   and the analytical-layer panels for figures.
4. Grab the shareable `/d/<id>` URL. Close the tab when done.

Never fabricate a reading. If neither the API nor a browser is available, note the
centroid, cite any nearby public reading for calibration, and list "run a TERRA
reading" as a Tier-1 DD action.
