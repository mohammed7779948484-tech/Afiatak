# Collaboration Diagram Geometry Redesign — Engineering TODO

## Scope and invariants

The six authoritative semantic models, verified source specifications, participants, exact message labels, global sequence numbers, senders, receivers, structural-link membership, self-message sequences, and CD-06 selected-single-appointment semantics are read-only inputs. This redesign changes only reusable rendering, geometry, routing, generated SVG metadata, validation, and reproducible export outputs. Every final View continues to declare `visualReview.status: awaiting-user-approval`.

## Baseline evidence

The source auditor passed for CD-01 through CD-06 before this redesign. The existing SVGs contain the expected participant/link/message counts and the individual PDFs contain no embedded raster image. The engineering deficiency is therefore not semantic completeness; it is the current rendering architecture: fixed `labelBox` coordinates, approximate character-count wrapping, unsafe dense-arrow placement, detached self-message labels, and no geometry collision diagnostics.

## Execution checklist

| ID | Engineering task | Completion evidence | State |
|---|---|---|---|
| A1 | Introduce explicit reusable geometry types for rectangles, segments, text blocks, message runs, self loops, occupied regions, and collisions. | `engine/collaboration_geometry.py` and all-six regression report. | Implemented — geometry regression pass |
| A2 | Replace `labelBox`-based message positioning with link-anchored candidate lanes selected against occupied geometry. | No renderer lookup of `labelBox`; every message group has an associated structural link and rendered geometry metadata. | Implemented — geometry regression pass |
| A3 | Implement deterministic text measurement and wrapping using font metrics rather than character count. | Width/height of every participant and message label is calculated from the configured font and line height. | Implemented — font-metric layout plan |
| A4 | Implement density-aware directional-arrow layout using usable link length, arrow lanes, size reduction, and minimum separation. | Dense CD-02/CD-05/CD-06 link checks report no arrow-overlap error. | Implemented — Q5 regression pass |
| A5 | Implement self-loop lanes with ordered loop indices, side selection, collision testing, and an adjacent label. | CD-01 messages 3 and 12 use distinct geometries; CD-03/05 loops avoid linked corridors. | Implemented — Q5 regression pass |
| A6 | Upgrade diagram specifications from free-floating label boxes to topology-aware participant placement plus side/routing hints. | Layout source contains positions/allowed sides only, with no manual message-label coordinates. | Implemented — composition migrated |
| A7 | Emit SVG data attributes for computed geometry: page, participant bounds, label bounds, link segments, arrow segments, and loop bounds. | Machine validator can inspect the generated geometry directly. | Implemented — all-six metadata complete |
| A8 | Add Q5 geometry validation for page bounds, participant/label intersections, label/label intersections, unrelated link/label intersections, self-loop collisions, duplicate loops, and arrow density. | Q5 blocks a render when unresolved collisions remain. | Implemented — all-six Q5 pass |
| A9 | Preserve existing Q4 semantic SVG validation and source-match auditing. | CD-01 through CD-06 source audits and Q4 reports pass unchanged. | Implemented — regression pass |
| A10 | Make SVG and `.drawio` consume the same computed render plan. | Corresponding objects, links, arrows, labels, and loops have congruent source geometry. | Implemented — shared render-plan source |
| A11 | Restore a compact, unobtrusive academic heading and retain the lecturer’s sparse monochrome object/link/message language. | Full-page review shows heading, underlined object names, thin links, unboxed labels, and no sequence primitives/cards/frames. | Implemented — full-page visual pass |
| A12 | Regenerate SVG, PNG, vector PDF, and `.drawio` for CD-01 through CD-06 from source only. | Reproducible final files; individual and merged PDFs contain no embedded raster images. | Implemented — release rebuilt |
| A13 | Run full-page and dense-area visual inspection, including all grids/tiles required for dense diagrams. | Inspection notes include CD-02, CD-05, and CD-06 stress cases. | Implemented — visual inspection record complete |
| A14 | Rebuild reports, release archive, and commit/push the corrective implementation. | QA package, merged PDF, release ZIP, clean Git state, and remote commit hash. | Pending |

## Required regression cases

| Diagram | Mandatory geometry proof |
|---|---|
| CD-01 | L01 labels clear Data Store; loops 3 and 12 differ; each label remains attached to its loop; no loop crosses Backend–Data Store. |
| CD-02 | L01 labels 16–18 and 27–30 clear all participants; no L01 arrow overlap; labels 23 and 34 separate; payment links remain traceable. |
| CD-03 | L01 clears Data Store and Notification Service; loop 5 and its label stay by Backend and avoid all unrelated links. |
| CD-04 | L01 clears Data Store/Notification Service; notification links do not cross unrelated labels. |
| CD-05 | Loop 6 and its label clear L01 and message 18; dense L01 arrows do not overlap; message 1 is not crossed by any unrelated link. |
| CD-06 | L01 labels 3, 4, 5, 6, 10, 11, and 14 clear Data Store; dense L01 arrows do not overlap; all six communication groups remain distinguishable. |

## Acceptance gate

No item is complete merely because the code executes. A task becomes complete only after the generated SVG passes Q4 semantic validation and new Q5 geometry validation, the source auditor passes, the relevant vector PDF is inspected, and the changed file is recorded in the final engineering report.
