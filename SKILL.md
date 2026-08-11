---
name: pre-dd
description: >-
  Produce an institutional-grade preliminary (pre-acquisition) due-diligence
  report as a polished PDF for a real-estate, land, farm, or hospitality asset —
  the screening layer that sits BEFORE a formal confirmatory due diligence. Use
  this whenever the user wants to evaluate, prepare to bid on, or brief someone
  on an asset they might acquire, including phrasings like
  "pre-DD", "/pre-dd", "preliminary due diligence", "pre-acquisition report",
  "diligence pack", "prepare me for negotiations on a property", "should we buy
  this lodge/finca/hotel/land", or when a Dear Wise Earth / TERRA land reading is
  wanted in an acquisition write-up. It runs the research, drives a TERRA land
  reading on the parcel when a browser is available, benchmarks the opportunity,
  and assembles a sourced, confidence-tagged PDF with a valuation range, risk
  matrix, confirmatory-DD workplan, data-room request list, and seller questions.
  Trigger it even when the user only describes an acquisition they are weighing
  without saying "due diligence".
---

# preDD — Preliminary (pre-acquisition) due-diligence report

## Purpose, in one line

Bring together all the risk-relevant information on a specific piece of land,
cross it with the TERRA engine from Dear Wise Earth, and produce a pre-diligence
document. Everything below is how to do that well: the land's own signals (title,
setbacks, hazards, market, condition) on one side, TERRA's first-party read of
the parcel on the other, reconciled into a single sourced, confidence-tagged PDF.

## What this produces

A single, institutional PDF that a buy-side principal can act on: it states what
is reliably known about an asset today, surfaces the red flags a full diligence
must resolve, benchmarks the opportunity against the market to frame a price, and
hands the reader a confirmatory-DD workplan, a data-room request list, and the
questions to put to the seller. It is deliberately the *pre-* layer: honest about
what has NOT been verified, and built to be handed to counsel and surveyors as a
scope of work.

This skill was distilled from a real engagement: a preliminary due-diligence
report on a large off-grid eco-lodge and farm acquisition. Read
`references/report-structure.md` for the full section-by-section template; it is
the spine of the deliverable.

## The one rule that makes these reports trustworthy: confidence tags

Every material claim carries a tag, rendered as a small coloured chip. This is
what separates a real diligence document from marketing — the reader can see
instantly what is load-bearing and what is a guess. Use exactly five:

- **CONFIRMED** — primary source, first-party data, or a direct quote.
- **LIKELY** — credible secondary source.
- **VERIFY** — cannot be established remotely; an explicit DD action.
- **DERIVED** — your own calculation from sourced inputs (e.g. $/key, $/ha).
- **FLAG** — a genuine discrepancy the DD must resolve (two sources disagree, or
  a fact contradicts the seller's narrative).

Never launder an inference into a fact. If the land-cover data says 96% tree
cover but the owner says they reforested bare pasture, that is a **FLAG**, not a
finding — and flags like that are often the most valuable thing in the report.

## Workflow

Work in this order. The research must be done *before* you touch the PDF
machinery — anchoring on document mechanics before you have facts produces a
handsome, empty report.

### 1 — Scope the assignment (briefly)

If the user is present, ask only what changes the deliverable and isn't already
known: the asset and its location (ideally coordinates or a precise place), the
purpose (personal decision vs. raising capital vs. preparing to negotiate), how
deep to go on local legal/regulatory law, and the output format (default PDF).
If the session is unattended or the user has already given enough, state your
assumptions in one line and proceed — don't block.

Get the parcel **centroid coordinates** if at all possible: TERRA and the maps
depend on them. If you only have a name, geocode it during research.

### 2 — Research first, in parallel

Spin up parallel research agents (or work through the workstreams inline if you
can't). The five standard workstreams and ready-to-use agent prompts are in
`references/research-plan.md`. In summary:

1. **Sale status** — is it actually for sale? listing, broker, price, distress
   signals, why it's selling. (Off-market is common; say so plainly.)
2. **Physical asset** — land, tenure, buildings, keys, energy, water, farm,
   infrastructure, intangibles, with a source for every number.
3. **Operating history & reputation** — founding, timeline, revenue model,
   pricing over time, demand signals, review-sentiment trajectory, certifications.
4. **Market & comparables** — arrivals/occupancy/ADR/RevPAR, competitive set,
   transaction and asking-price comps, land-value gradient, yield benchmarks.
5. **Risk, legal & regulatory** — title/registry, environmental setbacks, water
   and operating permits, labour liability, tax and transfer mechanics, hazards.

Agents routinely hit web-search caps — that's fine; capture what they found and
tag the gaps **VERIFY**. Absence of evidence (e.g. no public listing) is itself a
finding worth stating, not a failure.

### 3 — Run the TERRA land reading (when a browser is available)

This is the one first-party dataset in the report and Dear Wise Earth's
differentiator. Follow `references/terra-workflow.md` step by step. In short:
drive `read.dearwise.earth/engine`, search the centroid coordinates, click
**READ THIS PARCEL**, wait for it to compute, then capture the full reading text,
save screenshots of the score/radar and the analytical-layer panels, and grab the
shareable `/d/…` URL. Feed the score, the four/five sub-readings, the physical
metrics, the conservation-priority and hospitality-fit scores, the percentile
ranking, and especially any **FLAG** (jurisdiction mismatches, forest-history vs.
narrative, watercourse-name mismatches) into §3 of the report.

If no browser is connected, say so, embed the parcel centroid and any prior public
TERRA reading for calibration, and list "run a boundary-exact TERRA reading" as a
Tier-1 DD action. Never fabricate a reading.

**Scope honesty:** TERRA's default read is a 1 km² (100 ha) box at the centroid,
not the exact titled boundary. State this, and make a boundary-exact re-read a
DD item.

### 4 — Assemble the report

Build the HTML from `assets/template.html` (it carries the full stylesheet, the
confidence-tag chips, the cover, and the section scaffolding). Populate the
16 sections defined in `references/report-structure.md`. Pull benchmark numbers
from your research; `references/benchmark-library.md` holds a dated Costa
Rica / LatAm starter library you can draw on and MUST re-date and re-source for a
new asset or region.

Keep the register institutional but readable: prose over bullet-spam, tables for
anything comparative, and a valuation section that shows the triangulation
methods explicitly and *rejects* the ones that don't hold (per-ha metrics from
tiny lodges don't scale to a large holding; development-land comps that assume
access the asset lacks). Anchor a price range, then name the conditions that move
it up.

### 5 — Render the PDF and deliver

Render with headless Chromium (see `scripts/build_pdf.sh`), verify the page
count and that figures embedded, then deliver with `SendUserFile`. A one-line
caption; don't re-describe the document. If the user wanted a different format
(Word), read the `docx` skill after the research is done and build there instead.

## What good looks like

- Every number has a source or a tag. No orphan figures.
- The flags are prominent — surfaced in the executive summary, not buried.
- The valuation rejects bad methods out loud and explains why.
- The confirmatory-DD workplan and data-room list are specific enough to hand
  to counsel and a surveyor as-is.
- The seller questions are the ones that could end the deal cheaply, asked early.
- It reads like it was written by someone who has done this before and is on the
  buyer's side.

## Files in this skill

- `references/report-structure.md` — the 16-section template, in detail. Read
  this before writing the report.
- `references/terra-workflow.md` — how to drive the TERRA engine and what to
  extract. Read this before step 3.
- `references/research-plan.md` — the five research workstreams with copy-ready
  agent prompts. Read this before step 2.
- `references/benchmark-library.md` — a dated CR/LatAm benchmark starter set to
  draw from and re-source. Read when writing §7.
- `assets/template.html` — the full HTML/CSS deliverable scaffold. Copy and fill.
- `scripts/build_pdf.sh` — headless-Chromium HTML→PDF renderer.
