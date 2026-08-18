# Aafiatak Collaboration Diagrams — Geometry Redesign Report

## Purpose

This report records the corrective implementation applied to Collaboration/Communication Diagrams CD-01 through CD-06. The authoritative semantic models and binding Markdown contracts were not changed. The corrective scope was limited to reusable layout geometry, SVG rendering, diagrams.net export, SVG validation, preview generation, vector-PDF generation, and inspection records.

> **Review state:** Every View remains `awaiting-user-approval`. Passing automated and visual checks identifies a reviewable artifact; it does not replace the user's final approval.

## Architectural correction

The previous approach positioned message text through manually specified free-floating `labelBox` rectangles and used a character-count wrapper. The new implementation moves all geometry into `engine/collaboration_geometry.py`. It calculates font-metric text dimensions, routes structural links against participant obstacles, places full message runs beside their actual links through collision-tested candidate lanes, allocates density-aware arrow lanes, and allocates distinct self-loop routes and adjacent labels.

| Layer | Corrective implementation | Verification consequence |
|---|---|---|
| Semantic model and View | Preserved as the source of participants, exact labels, sequences, senders, receivers, links, and self-message sequences. | Source auditors continue to compare each model/View to its binding Markdown contract. |
| Composition | Replaced message `labelBox` coordinates with participant topology, preferred label sides, maximum label widths, and loop-side hints. | Message placement becomes calculated and topology-aware rather than static. |
| Geometry | Added `Rect`, `Segment`, `Polyline`, text measurement, message runs, arrow lanes, loop lanes, collision candidates, and render-plan metadata. | Every visible spatial object has deterministically calculated bounds or route points. |
| SVG and diagrams.net | Both consume the same `CollaborationRenderPlan`. | The editable `.drawio` geometry tracks the verified SVG geometry. |
| Validation | Preserved Q4 semantic SVG validation and added Q5 page-bound, collision, routing, loop, and arrow-density checks. | A rendering failure now blocks unresolved layout candidates or unsafe geometry. |

## Lecturer-compatible visual language

The corrected outputs use a compact academic heading, plain white canvas, unfilled object rectangles, underlined object names, one thin reusable structural link per communicating pair, unboxed numbered message text, short solid directional arrows, and small smooth self-loops only for contractually specified self-messages. The renderer continues to prohibit lifelines, activation bars, sequence fragments, card/panel message boxes, and invented architecture elements.

## Regression results

| Diagram | Participants | Links | Messages | Self messages | Source audit | Q4 semantic SVG | Q5 geometry | Visual inspection |
|---|---:|---:|---:|---|---|---|---|---|
| CD-01 — Patient Registration & WhatsApp OTP Verification | 5 | 5 | 19 | 3, 12 | Pass | Pass | Pass | Full page; both distinct Backend loops reviewed. |
| CD-02 — Book Appointment FULL_PAYMENT_REQUIRED | 6 | 7 | 34 | None | Pass | Pass | Pass | Full page and dense L01 review. |
| CD-03 — Cancel Appointment Full Refund | 6 | 5 | 18 | 5 | Pass | Pass | Pass | Full page and Backend loop review. |
| CD-04 — Reschedule Appointment | 6 | 5 | 18 | None | Pass | Pass | Pass | Full page review. |
| CD-05 — Patient Check-in, Queue & Call Next Patient | 8 | 8 | 30 | 6 | Pass | Pass | Pass | Full page plus dense L01/self-loop review. |
| CD-06 — Resolve Operational Exception | 7 | 6 | 25 | None | Pass | Pass | Pass | Full page and dense L01 review. |

The machine-readable all-six result is recorded in `build/qa/Aafiatak_Collaboration_Geometry_Regression.json`. It confirms complete geometry metadata, no unresolved render-plan candidates, unique self-loop bounds, and no Q4/Q5 error for every diagram. The detailed visual record is `build/work/collaboration-geometry-visual-inspection.md`.

## Delivery verification

| Artifact set | Result |
|---|---|
| Individual SVG, PNG, `.drawio`, and PDF for CD-01 through CD-06 | Rebuilt from the corrected source pipeline. |
| Merged PDF | `Aafiatak_Collaboration_Diagrams_CD01-CD06_FINAL.pdf`, six A0 landscape pages in CD-01 to CD-06 order. |
| Vector check | Each individual PDF and the merged PDF have zero embedded raster images according to `pdfimages -list`. |
| Preview hashes | Every View records the current preview hash, and final QA reports show `hashMatchesRecordedPreview: true`. |
| Human approval | Not granted; all six Views remain `awaiting-user-approval`. |

## Reproduction commands

```bash
python3 tools/verify_collaboration_geometry.py \
  --output build/qa/Aafiatak_Collaboration_Geometry_Regression.json

python3 -m engine.cli qa views/collaboration/aafiatak-cd05-checkin-queue-call-next.yaml
python3 -m tools.audit_collaboration_source CD05 \
  --output build/qa/Aafiatak_CD05_geometry_source_match.json
python3 -m tools.export_collaboration_drawio \
  views/collaboration/aafiatak-cd05-checkin-queue-call-next.yaml \
  build/final/Aafiatak_CD05_CheckIn_Queue_CallNext.drawio
```
