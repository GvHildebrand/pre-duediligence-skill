# pre-dd: a first-pass due diligence report on a piece of land

A [Claude](https://claude.ai) skill that turns a property you are thinking of buying
(land, a farm, a lodge or a small hotel) into a sourced PDF report, with every claim
tagged by how sure it is.

It is for buyers, co-investors and their advisers who need to know, before paying for
a full due diligence, what is known, what is a guess, and what to ask the seller.

## Install and run

- **In the Claude app / Cowork:** open `pre-dd.skill` and choose **Save skill**
  (available when your organisation allows skill creation). Then type `/pre-dd`, or
  describe a property you are weighing.
- **In Claude Code or any skills folder:** copy `SKILL.md`, `references/`, `assets/`
  and `scripts/` into a `pre-dd/` folder in your skills directory.

The land reading step needs only Python 3:

```bash
python3 scripts/terra_read.py --lat <LAT> --lon <LON>
```

Rendering the PDF needs headless Chromium (`scripts/build_pdf.sh`).

## What it produces

A single PDF in sixteen sections: an executive summary and preliminary valuation range;
the **TERRA land reading** from [Dear Wise Earth](https://read.dearwise.earth) (land
score, model fit, physical metrics, conservation-priority and hospitality-fit scores,
climate exposure to 2050, and the flags TERRA raises); a physical asset inventory; a
commercial and operating snapshot; market context and benchmarks; a legal and
regulatory red-flag screen; a risk matrix; a confirmatory due diligence workplan; a
data-room request list; an indicative process and timeline; and the questions to put
to the seller.

It is the *screening* layer that sits **before** a formal confirmatory due diligence.
It says plainly what has not yet been verified, and it doubles as the scope of work
for the diligence that follows.

## Confidence tags

Every material claim carries one of five tags, rendered as a coloured chip, so a
reader sees at once what is load-bearing and what is a guess:

| Tag | Meaning |
|-----|---------|
| **CONFIRMED** | primary source, first-party data, or a direct quote |
| **LIKELY** | credible secondary source |
| **VERIFY** | cannot be established remotely, so it becomes a due diligence action |
| **DERIVED** | a calculation from sourced inputs (e.g. $/key, $/ha) |
| **FLAG** | a genuine discrepancy the due diligence must resolve |

Inferences are never passed off as facts. When satellite land cover says 96% tree
cover but the seller says they reforested bare pasture, that is a **FLAG**, and flags
like that are often the most valuable output in the report.

## How it works

1. **Scope** the assignment briefly (asset, coordinates, purpose, legal depth).
2. **Research first**, in five parallel workstreams: sale status, physical asset,
   operating history and reputation, market and comparables, and risk/legal.
3. **Run the TERRA reading** on the parcel with one API call, no browser and no
   login: `scripts/terra_read.py` POSTs to the open `read.dearwise.earth/api/dossier`
   endpoint, saves the full reading JSON, and returns the shareable reading URL. A
   browser fallback is documented for environments where the API is unreachable.
4. **Assemble** the 16-section report from the bundled HTML template.
5. **Render** the PDF (headless Chromium) and deliver it.

## Repository layout

```
SKILL.md                     # the method (read first)
references/
  report-structure.md        # the 16-section template
  terra-workflow.md          # the TERRA API contract + browser fallback
  research-plan.md           # the five research workstreams
  benchmark-library.md       # a dated Costa Rica / Latin America benchmark starter set
assets/
  template.html              # the styled HTML/PDF scaffold
scripts/
  terra_read.py              # calls the TERRA API → reading JSON (no browser)
  build_pdf.sh               # headless-Chromium HTML → PDF renderer
pre-dd.skill                 # packaged, installable skill archive
```

## Limits

- The `benchmark-library.md` starter set is dated Costa Rica and Latin America data
  and **must be re-sourced and re-dated** for a new asset or region.
- TERRA's default read is a 1 km² box at the parcel centre, not the exact titled
  boundary. A boundary-exact re-read is always listed as a first-tier due diligence
  item.
- This skill produces a *preliminary* research document. It is not a valuation,
  appraisal, audit, or legal, tax or investment advice, and its outputs require
  confirmation through formal due diligence and local counsel.

## License

[MIT](LICENSE) © Gregorio von Hildebrand · Dear Wise Earth

Built by Gregorio von Hildebrand · [github.com/GvHildebrand](https://github.com/GvHildebrand) · [sovran.works](https://sovran.works)
