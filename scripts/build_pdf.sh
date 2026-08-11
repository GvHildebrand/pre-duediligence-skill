#!/usr/bin/env bash
# Render a preDD HTML report to PDF with headless Chromium.
# Usage: bash build_pdf.sh input.html output.pdf
# Figures referenced by the HTML (fig_score.png, fig_satellite.png,
# fig_layers.png) must sit next to input.html so relative src= resolves.
set -euo pipefail
IN="${1:?usage: build_pdf.sh input.html output.pdf}"
OUT="${2:?usage: build_pdf.sh input.html output.pdf}"

# Find a Chromium binary. In this cloud environment Playwright ships one at
# /opt/pw-browsers/chromium; fall back to common names elsewhere.
CHROME=""
for c in /opt/pw-browsers/chromium chromium chromium-browser google-chrome google-chrome-stable; do
  if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then CHROME="$c"; break; fi
done
[ -z "$CHROME" ] && { echo "No Chromium binary found."; exit 1; }

ABS_IN="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --print-to-pdf="$OUT" --virtual-time-budget=15000 "file://$ABS_IN" 2>/dev/null || true

if [ -f "$OUT" ]; then
  echo "Wrote $OUT"
  python3 - "$OUT" <<'PY' 2>/dev/null || true
import sys
from pypdf import PdfReader
print("pages:", len(PdfReader(sys.argv[1]).pages))
PY
else
  echo "Render failed."; exit 1
fi
