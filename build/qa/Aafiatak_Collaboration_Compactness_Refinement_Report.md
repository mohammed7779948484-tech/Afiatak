# Aafiatak Collaboration Diagrams — Compactness & Link-Adherence Refinement

## Purpose

This report records the refinement of the six UML Collaboration/Communication Diagrams, CD-01 through CD-06. The refinement responds to the remaining presentation gap against the lecturer reference: the previous rendered network was too spread out, message groups could appear visually detached from long links, and directional arrowheads were heavier than the sparse academic reference language.

The authoritative product specification, the six immutable scenario specifications, and the lecturer interaction-diagram convention remained unchanged. The semantic models and View selections were not altered. Every diagram remains in `awaiting-user-approval` status.

## System-level changes

| Area | Refinement applied | Semantic effect |
|---|---|---|
| Network footprint | Reduced the shared render canvas from `16000 × 10400` to `14000 × 9000` and transformed authored participant coordinates around the composition centre using a shared `0.86` scale. | None. Participants, structural links, and their memberships are unchanged. |
| Participant objects | Reduced box dimensions and used a compact underlined serif object-name treatment. | None. Every participant still renders exactly once. |
| Message placement | Replaced a structural-link bounding-box anchor with local anchor points sampled on the actual link. Candidate placement now searches adjacent sides and local offsets while avoiding occupied geometry. | None. Exact sequence numbers, labels, senders, receivers, and structural-link assignments remain model-sourced. |
| Arrow layout | Converted to short, density-aware arrow lanes that reserve all label bounds and use more parallel lanes on dense links. | None. Each non-self message remains a solid directional arrow on its prescribed reusable structural link. |
| Arrow styling | Replaced oversized filled heads with a smaller open arrowhead and lighter stroke. | None. Direction remains encoded by the same rendered arrow segment. |
| Self messages | Reduced loop size/clearance while preserving separate lanes and nearby labels; SVG curves remain smooth Bézier paths. | None. Self messages remain loops on the original owner only. |
| Editable source | Updated the diagrams.net exporter to consume the same compact geometry plan and open-arrow visual rules. | None. The `.drawio` artifact is derived from the same model/view/render plan as SVG. |

## Verification evidence

| Control | Result |
|---|---|
| Immutable source specifications CD-01–CD-06 | Read before refinement; no protected specification changed. |
| Product-scope consistency | Checked against `Aafiatak_Project_Specification_EN.md`; no actor, service, message, state, or flow was invented. |
| Source-match audit | Passed for CD-01, CD-02, CD-03, CD-04, CD-05, and CD-06. |
| Q4 semantic SVG gate | Passed for all six diagrams. |
| Q5 geometry gate | Passed for all six diagrams after checking page bounds, participant/label separation, label separation, unrelated link/label intersections, arrow density, and self-loop geometry. |
| Dense scenario inspection | CD-02 L01, CD-05 L01 plus self loop, and CD-06 L01 reviewed at full-page/dense-state render level. |
| Family consistency inspection | Six-diagram compact contact sheet reviewed. |
| Vector PDF delivery | Six individual PDFs and the six-page merged PDF verified without embedded raster images. |

## Visual review result

The current render family presents a compact, monochrome academic communication-diagram language: a modest heading, simple unfilled participant rectangles, underlined object names, one light reusable structural link per pair, free numbered message labels near their link, smaller open directional heads, and only the specified small self-message loops. It contains no cards, page frames, lifelines, activation bars, combined fragments, Use Case notation, Activity notation, or Class/State notation.

Full-page review records are available in [`build/work/compact-review/visual-inspection.md`](../work/compact-review/visual-inspection.md), and the rendered family comparison is available in [`build/work/compact-review/collaboration-compact-contact-sheet.png`](../work/compact-review/collaboration-compact-contact-sheet.png).

## Deliverables and review status

The final delivery set contains the updated SVG, high-resolution PNG, editable `.drawio`, and vector PDF for CD-01 through CD-06, plus `Aafiatak_Collaboration_Diagrams_CD01-CD06_FINAL.pdf` as the merged six-page artifact. All six Views retain the exact status `awaiting-user-approval`; this report is evidence of engineering/semantic/geometry/visual checks and is **not** a substitute for user approval.
