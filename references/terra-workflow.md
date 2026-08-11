# Driving the TERRA land reading

TERRA (`read.dearwise.earth`) is Dear Wise Earth's own land-intelligence engine.
It scores any parcel from live satellite and open-geospatial data (Sentinel-2,
AWS Terrain Tiles, ESA WorldCover, GBIF, ERA5/Open-Meteo, Hansen Global Forest
Change, NASA Black Marble, and SNIT jurisdiction records for Costa Rica). The
reading is the report's one first-party dataset — treat it as CONFIRMED primary
data and build §3 around it.

## Prerequisites

- A connected browser via the `claude-in-chrome` tools (load them with ToolSearch
  first). If two browsers are connected, the tool will make you pick — ask the
  user which one with AskUserQuestion, then `select_browser`.
- The parcel **centroid coordinates** (decimal degrees). If you only have a place
  name, TERRA's search will try to geocode it, but coordinates are far more
  reliable and let you target the exact spot.

If no browser is available, do NOT fabricate a reading. Note the centroid, cite
any pre-existing public reading nearby for calibration, and add "run a
boundary-exact TERRA reading" as a Tier-1 DD action.

## Steps

1. `tabs_context_mcp{createIfEmpty:true}` → `navigate` to
   `https://read.dearwise.earth/engine`.
2. Screenshot to confirm the search panel loaded.
3. Click the search field, type the coordinates as `LAT, LON` (e.g.
   `9.7489, -83.7534`), click **SEARCH**. The engine drops a default
   **1 km² (100 ha) read box** at that point and shows "READ THIS PARCEL".
   - Place names also work but often fail or land imprecisely; coordinates win.
   - To read the exact titled boundary instead of the default box, use the
     draw-on-map mode ("CLICK TO DRAW") if you have the cadastral outline. The
     default box is fine for a first reading — just disclose it.
4. Click **READ THIS PARCEL**. It computes for up to ~60s ("MEASURING THE
   TERRAIN…"). Wait, then screenshot until the score appears.
5. Once the score renders, `get_page_text` on the tab to capture the entire
   reading verbatim — this is the richest capture and includes every metric.
6. Save two screenshots to disk (`save_to_disk:true`): the score + radar + parcel
   view, and (after scrolling the right panel down ~10 ticks) the six analytical
   layer panels (NDVI, NDMI, relief, land cover). These become the figures.
7. Capture the **shareable URL** — it appears near the top ("OPEN SHAREABLE
   PAGE") and again in the page text as `read.dearwise.earth/d/<id>`. This is the
   reading of record; cite it in the report.
8. Close the tab you opened when done.

## What to extract into §3

- **Land score** (/100) and **model fit** (RECLAIM / CULTIVATE / RESTORE / ANCHOR).
- The one-line verdict (e.g. "Worth restoring — and worth the patience").
- **Sub-readings** (radar): Water, Ecology, Climate, Pressure — note if one is
  "unavailable" (e.g. soil) and weight redistributed.
- **Physical metrics:** tree cover %, grassland %, built %, elevation range +
  mean, relief, mean slope, rainfall mm/yr and its 20-yr trend, distance to road,
  soil-data availability.
- **Deployment layer:** conservation-priority score, hospitality-fit score,
  nearest declared biological corridor and conservation area, best-fit regenerative
  model and alternates.
- **Comparative:** percentile vs. the like-land corpus, and per-signal percentiles
  (ecology/water/climate/low-pressure).
- **Climate-to-2050:** projected Δ temperature and Δ rainfall, exposure rating,
  current mean temp.
- **Forest history (Hansen):** tree cover in 2000, cover lost since, latest loss
  year — a powerful cross-check on any "we reforested bare land" narrative.
- **Rainfall record, biodiversity record, jurisdiction (SNIT).**

## Flags TERRA frequently surfaces — hunt for these

- **Jurisdiction mismatch.** The SNIT layer can return the parcel under two
  different cantón/distrito names (the header vs. the land-record reading). That
  means a **cantonal boundary** runs near the parcel and determines which
  municipality issues permits and collects tax. Tag **FLAG**.
- **Forest-history vs. narrative.** If Hansen shows high tree cover in 2000 and
  near-zero loss, but the seller's story is "bare pasture we reforested", the
  satellite record disputes the marketing. Tag **FLAG**, make it a DD item.
- **Watercourse naming.** TERRA maps the river by its cadastral name, which may
  differ from the name the seller uses. Reconcile — and note that a mapped
  watercourse confirms riparian setback rules apply.
- **Low-confidence tree-cover upside.** TERRA itself warns satellite land-cover
  can't tell natural forest from monoculture — carry that caveat into the report
  and make "ground-truth the canopy with a botanist" a DD action.

Always state the scope honestly: the default reading is a 1 km² box centred on
the centroid, not the exact titled boundary. A boundary-exact re-read is a
Tier-1 DD action.
