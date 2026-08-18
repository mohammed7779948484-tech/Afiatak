# Aafiatak UML Collaboration / Communication Diagrams — Final Label-Proximity Refinement

This package contains six UML Collaboration/Communication Diagrams for the **Aafiatak Medical Appointment Booking System**. The final refinement makes each numbered message label a local visual annotation of its owning communication link, adds an explicit Q5 ownership-distance check, and preserves every approved semantic element and exact scenario message.

| Deliverable | Contents |
|---|---|
| `diagrams/` | Six editable diagrams.net files, SVG files, high-resolution PNG previews, and A0-landscape vector PDFs; plus the merged six-page A0 vector PDF. |
| `qa/` | Q4/Q5 reports, source-match audits, geometry regression, own-label-to-link proximity evidence, and the final refinement report. |
| `work/` | Visual audit notes and final family contact sheet used for human inspection. |
| `source/` | The shared geometry engine, SVG renderer, diagrams.net exporter, composition settings, Q5 validator, and proximity-evidence tool used for this release. |

The diagrams preserve all participants, message labels, global message numbers, senders, receivers, structural-link memberships, and self-message assignments. The output style remains lecturer-like: white academic page, simple underlined participant rectangles, thin neutral links, unboxed local message labels, small open direction marks, and no Sequence-Diagram constructs.

The individual PDFs and merged six-page PDF are vector-only. `pdfimages -list` reports no embedded raster images.

> **Approval status:** all six Views remain `awaiting-user-approval`. Passing QA and visual inspection is evidence for user review; it does not self-approve the diagrams.
