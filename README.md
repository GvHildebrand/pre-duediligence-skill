# pre-dd — Preliminary (pre-acquisition) due-diligence skill

A [Claude](https://claude.ai) skill that produces an **institutional-grade
preliminary due-diligence report** — as a polished PDF — for a real-estate, land,
farm, or hospitality asset. It brings together all the risk-relevant information
on a specific piece of land, crosses it with the **[TERRA](https://read.dearwise.earth)
land-intelligence engine** from Dear Wise Earth, and assembles a sourced,
confidence-tagged report you can hand to counsel, co-investors, or a seller.

It is the *screening* layer that sits **before** a formal confirmatory due
diligence: honest about what has not yet been verified, and built to double as a
scope of work for the diligence that follows.

## What it produces

A single institutional PDF covering, in sixteen sections: an executive summary
and preliminary valuation range; the **TERRA land reading** (the one first-party
dataset — land score, model fit, physical metrics, conservation-priority and
hospitality-fit scores, climate-to-2050 exposure, and the flags TERRA surfaces);
a physical asset inventory; a commercial and operating snapshot; market context
and benchmarks; a legal and regulatory red-flag screen; a consolidated risk
matrix; a confirmatory-DD workplan; a data-room request list; an indicative
process and timeline; and the questions to put to the seller.

## The one discipline that makes it trustworthy: confidence tags

Every material claim carries one of five tags, rendered as a coloured chip, so a
reader sees instantly what is load-bearing and what is a guess:

| Tag | Meaning |
|-----|---------|
| **CONFIRMED** | primary source, first-party data, or a direct quote |
| **LIKELY** | credible secondary source |
| **VERIFY** | cannot be established remotely — an explicit DD action |
| **DERIVED** | a calculation from sourced inputs (e.g. $/key, $/ha) |
| **FLAG** | a genuine discrepancy the DD must resolve |

Inferences are never laundered into facts. When the satellite land-cover says 96%
tree cover but the seller says they reforested bare pasture, that is a **FLAG** —
and flags like that are often the most valuable output in the report.

## How it works

1. **Scope** the assignment briefly (asset, coordinates, purpose, legal depth).
2. **Research first**, in five parallel workstreams: sale status, physical asset,
   operating history and reputation, market and comparables, and risk/legal.
3. **Run the TERRA reading** on the parcel via a connected browser — search the
   centroid coordinates, read the parcel, and capture the score, figures, and the
   shareable reading-of-record URL.
4. **Assemble** the 16-section report from the bundled HTML template.
5. **Render** the PDF (headless Chromium) and deliver it.

## Installing

- **In the Claude app / Cowork:** open `pre-dd.skill` and choose **Save skill**
  (available when your organisation allows skill creation). Then invoke it with
  `/pre-dd`, or simply describe a property you are weighing.
- **Manually:** copy the `pre-dd/` contents (`SKILL.md`, `references/`, `assets/`,
  `scripts/`) into your skills directory.

## Repository layout

```
SKILL.md                     # the method (read first)
references/
  report-structure.md        # the 16-section template
  terra-workflow.md          # how to drive the TERRA engine
  research-plan.md           # the five research workstreams
  benchmark-library.md       # a dated CR/LatAm benchmark starter set
assets/
  template.html              # the styled HTML/PDF scaffold
scripts/
  build_pdf.sh               # headless-Chromium HTML → PDF renderer
pre-dd.skill                 # packaged, installable skill archive
```

## Notes

- The `benchmark-library.md` starter set is dated Costa Rica / LatAm data and
  **must be re-sourced and re-dated** for a new asset or region.
- TERRA's default read is a 1 km² box at the parcel centroid, not the exact
  titled boundary; a boundary-exact re-read is always listed as a Tier-1 DD item.
- This skill produces a *preliminary* research document. It is not a valuation,
  appraisal, audit, or legal, tax, or investment advice, and its outputs require
  confirmation through formal due diligence and local counsel.

## License

[MIT](LICENSE) © Gregorio von Hildebrand · Dear Wise Earth
