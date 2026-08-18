# Aafiatak Collaboration Diagrams — Final Label-Proximity Refinement Report

**Scope.** This report records the final visual-only refinement of the six UML Collaboration/Communication Diagrams, CD-01 through CD-06. Participant identities, message text, global sequence numbers, senders, receivers, structural-link membership, self-message membership, and all scenario source specifications were preserved. Each View remains **`awaiting-user-approval`**.

## Root cause corrected

The previous placement routine accepted the first collision-free **group envelope**. For a left-aligned run beside a vertical or shallow horizontal/diagonal link, a long label could bring the envelope near the link while shorter labels retained the unused group width as empty space. Those short labels therefore appeared as detached text columns despite passing collision checks. CD-02 L01 provided the clear instance: its link corridor was near `x=6483`, while some label bounds ended thousands of layout units away.

## Layout-engine changes

The geometry engine now places each message run in a link-local coordinate frame. It derives a tangent and normal from the real structural-link polyline, restricts ordinary vertical links to right/left corridors and ordinary horizontal links to above/below corridors, and projects diagonal choices into that same local frame. The candidate score is based on the farthest **actual individual label bound** from the owning polyline rather than the envelope of the full group.

The renderer also aligns every individual label's link-facing edge with its local corridor. Thus, labels left of a vertical link are right-aligned to the link-facing edge; labels above or below a horizontal/diagonal link are centred about the local link position. Dense runs first attempt a single block, then the fewest local sub-runs, then compact local lanes. No fallback text column is accepted as a valid solution.

| Behaviour | Final implementation |
|---|---|
| Ordinary target distance | **80–250 layout units** from the own-link corridor |
| Dense local-lane allowance | Up to **450 layout units**, only where a nearer local lane collides |
| Candidate frame | Link tangent + local normal, not a canvas-wide floating column |
| Dense-run strategy | One block → fewest local sub-runs → bounded local lanes |
| Label alignment | Link-facing edge for vertical corridors; local-centre alignment for horizontal/diagonal corridors |
| Direction mark | Existing short, thin, open arrowhead retained and placed on the same owning link corridor |

## New Q5 ownership rule

Q5 now includes **`own-label-to-link-distance`**. For every non-self message, the validator parses the message label bounds and its declared owning structural-link polyline, calculates the shortest edge-to-edge geometric distance, and fails above the strict practical ceiling of **450 layout units**. This is distinct from the existing unrelated-link-versus-label collision rule.

## Typography and visual-style changes

The academic hierarchy is now **Heading 68 px > Participant 56 px > Message 48 px** in the SVG renderer, with the same hierarchy mirrored in the editable diagrams.net export. Message line height is 60 px. The participant boxes, neutral thin structural links, and the small open direction marker remain restrained. No filled arrowheads, lifelines, activations, fragments, cards, panels, or non-academic embellishments were introduced.

## Quantitative own-link proximity evidence

The table compares the maximum individual label-to-own-link distance before and after this refinement. The post-change figures come from `tools/audit_own_label_proximity.py` applied to the final SVG assets.

| Diagram | Prior maximum | Final maximum | Worst final message/link | Result |
|---|---:|---:|---|---|
| CD-01 | 739.71 | 380.00 | #18 / L02 | Pass |
| CD-02 | 2,195.83 | 400.95 | #14 / L03 | Pass |
| CD-03 | 396.36 | 397.88 | #17 / L03 | Pass |
| CD-04 | 622.99 | 319.55 | #2 / L02 | Pass |
| CD-05 | 385.39 | 397.04 | #3 / L03 | Pass |
| CD-06 | 444.02 | 290.68 | #2 / L02 | Pass |

CD-02 L01 no longer uses its previous remote left text column. Its labels now sit immediately beside the vertical Backend ↔ Data Store corridor. CD-02 L03 is the densest remaining local arrangement: its exact long labels use stacked local lanes, with a maximum of 400.95 units rather than the previous 2,700–3,500-unit detached fallback range.

## Validation evidence

| Verification | CD-01 | CD-02 | CD-03 | CD-04 | CD-05 | CD-06 |
|---|---|---|---|---|---|---|
| Q4 semantic SVG validation | Pass | Pass | Pass | Pass | Pass | Pass |
| Q5 geometry, collisions, arrows, self loops | Pass | Pass | Pass | Pass | Pass | Pass |
| Q5 own-label-to-link distance | Pass | Pass | Pass | Pass | Pass | Pass |
| Source-match audit | Pass | Pass | Pass | Pass | Pass | Pass |
| Geometry-regression suite | Pass | Pass | Pass | Pass | Pass | Pass |
| Visual status | Awaiting user approval | Awaiting user approval | Awaiting user approval | Awaiting user approval | Awaiting user approval | Awaiting user approval |

The final geometry regression confirms no unresolved layout candidates, complete geometry metadata, and distinct self-loop bounds for CD-01, CD-03, and CD-05. The source-match audits confirm unchanged participants, structural links, message counts, numbering, sender/receiver mappings, and self-message definitions. The CD-06 single-affected-Appointment correction remains preserved.

## Lecturer-reference comparison

Compared with the lecturer example, the final family uses the same visual grammar: **object rectangle + thin communication link + local numbered label + small open direction mark**. The previous detached-column defect is removed. The heading is visibly above the participant/message hierarchy, participant names remain underlined, and labels remain unboxed and local to their communication lines.

The inherent remaining limitation is scenario density. CD-02, CD-05, and CD-06 contain substantially more exact, long message text than the four-object lecture example. The engine addresses that without inventing a different notation by using compact multiline text and stacked local annotation lanes; those dense cases are necessarily busier, but all message groups remain locally associated with their own links.

## Files changed

| Category | Files |
|---|---|
| Shared geometry | `engine/collaboration_geometry.py` |
| SVG renderer | `engine/svg/collaboration_diagram.py` |
| Editable diagrams.net exporter | `engine/collaboration_drawio_export.py` |
| Shared composition typography | `engine/compositions/collaboration_diagram_layouts.py` |
| Q5 validator | `qa/collaboration_svg_validation.py` |
| Read-only proximity evidence tool | `tools/audit_own_label_proximity.py` |
| Final deliverables | `build/final/Aafiatak_CD01…CD06_*` and merged PDF |
| QA evidence | `build/qa/*final_label_proximity*` and proximity summary |

## Final deliverables

The release includes six editable `.drawio` files, six SVGs, six high-resolution PNGs, six A0-landscape vector PDFs, and one merged six-page A0-landscape vector PDF. `pdfimages -list` returned no embedded raster-image rows for every individual PDF and the merged PDF.

> Engineering and QA are complete. This evidence does **not** constitute user approval; all Views intentionally remain `awaiting-user-approval`.
