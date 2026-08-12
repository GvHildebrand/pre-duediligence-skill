#!/usr/bin/env python3
"""
terra_read.py — call the TERRA engine directly (no browser, no login).

TERRA (read.dearwise.earth) exposes an open JSON endpoint that generates a full
land reading and publishes it to the public wall:

    POST https://read.dearwise.earth/api/dossier
    body: {"geometry": {"type": "Polygon", "coordinates": [ring]}}
    -> 200, ~22 KB JSON reading; the returned `id` is the /d/<id> wall page.

No authentication is required. Every reading generated this way is public and
joins the wall (this is intended). Pass a centroid and this builds the standard
~1 km (100 ha) box TERRA uses by default; or pass your own GeoJSON polygon to
read an exact boundary.

Usage:
    python3 terra_read.py --lat 9.7489 --lon -83.7534
    python3 terra_read.py --lat 9.75 --lon -83.75 --half-km 0.5 --out reading.json
    python3 terra_read.py --geojson parcel.geojson        # exact boundary

Prints a concise summary and writes the full JSON to --out (default
terra_reading.json). Stdlib only (urllib); no pip install needed.
"""
import argparse, json, math, sys, urllib.request, urllib.error

API = "https://read.dearwise.earth/api/dossier"

def box_ring(lat, lon, half_km=0.5):
    """Closed [lon,lat] ring, ~ (2*half_km) square, centred on the point."""
    dlat = half_km / 111.0
    dlon = half_km / (111.0 * math.cos(math.radians(lat)))
    return [[lon-dlon, lat-dlat], [lon+dlon, lat-dlat],
            [lon+dlon, lat+dlat], [lon-dlon, lat+dlat], [lon-dlon, lat-dlat]]

def read_parcel(polygon):
    """POST a GeoJSON Polygon, return the parsed reading dict."""
    body = json.dumps({"geometry": polygon}).encode()
    req = urllib.request.Request(
        API, data=body, method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        sys.exit(f"TERRA API {e.code}: {e.read().decode('utf-8','replace')[:200]}")
    except Exception as e:
        sys.exit(f"TERRA API call failed: {e}\n"
                 "If the network blocks this call, fall back to the browser flow "
                 "in references/terra-workflow.md.")

def summarize(j):
    sc = j.get("scores", {}) or {}
    v  = j.get("verdict", {}) or {}
    pl = j.get("place", {}) or {}
    rid = j.get("id")
    lines = [
        f"Reading of record : https://read.dearwise.earth/d/{rid}" if rid else "(no id returned)",
        f"Place             : {pl.get('display') or pl.get('name')}",
        f"Area              : {j.get('area_ha')} ha",
        f"Land score        : {sc.get('composite')}/100   (model fit: {v.get('class')})",
        f"Verdict           : {v.get('headline')}",
        f"Pillars           : water {sc.get('water')} · soil {sc.get('soil')} · "
        f"ecology {sc.get('ecology')} · climate {sc.get('climate_resilience')} · "
        f"pressure {sc.get('pressure')}  (confidence {sc.get('data_confidence')}%)",
    ]
    dep = j.get("deployment") or {}
    pm  = j.get("project_model") or {}
    if dep: lines.append(f"Deployment        : tier={dep.get('tier')} role={dep.get('role')} "
                         f"priority={dep.get('priority') or dep.get('score')}")
    if pm:  lines.append(f"Best-fit model    : {pm.get('name')} ({pm.get('fit')})")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(description="Generate a TERRA land reading via the API.")
    ap.add_argument("--lat", type=float); ap.add_argument("--lon", type=float)
    ap.add_argument("--half-km", type=float, default=0.5,
                    help="half-width of the box in km (0.5 = ~1 km / 100 ha, TERRA default)")
    ap.add_argument("--geojson", help="path to a GeoJSON file with a Polygon geometry (exact boundary)")
    ap.add_argument("--out", default="terra_reading.json")
    a = ap.parse_args()

    if a.geojson:
        gj = json.load(open(a.geojson))
        poly = gj.get("geometry", gj)  # accept a Feature or a bare geometry
        if poly.get("type") != "Polygon":
            sys.exit("GeoJSON must contain a Polygon geometry.")
    elif a.lat is not None and a.lon is not None:
        poly = {"type": "Polygon", "coordinates": [box_ring(a.lat, a.lon, a.half_km)]}
    else:
        ap.error("provide --lat/--lon (a centroid) or --geojson (an exact boundary)")

    j = read_parcel(poly)
    json.dump(j, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(summarize(j))
    print(f"\nFull reading JSON written to {a.out}")

if __name__ == "__main__":
    main()
