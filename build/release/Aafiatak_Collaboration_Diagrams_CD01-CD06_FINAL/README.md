# Aafiatak Collaboration Diagrams — CD-01 to CD-06

## Delivery contents

This release contains six UML Collaboration/Communication Diagrams for the Aafiatak Medical Appointment Booking System. Each diagram is delivered as editable diagrams.net XML (`.drawio`), scalable vector graphics (`.svg`), a high-resolution PNG preview (`.png`), and an A0-landscape vector PDF (`.pdf`). The file `Aafiatak_Collaboration_Diagrams_CD01-CD06_FINAL.pdf` merges the six diagrams in order from CD-01 to CD-06.

## Rendering approach

The artifacts are generated from immutable semantic models and View specifications through a shared collision-aware geometry plan. Message labels are placed in local corridors adjacent to their own structural communication links; dense links use compact directional-arrow lanes; specified self messages use separate small loop lanes. The SVG and `.drawio` exports use the same render plan.

The intended lecturer-style language is sparse and academic: simple unfilled object rectangles with underlined names, one reusable structural link per communicating pair, unboxed globally numbered message labels, small open arrowheads, and self loops only where the selected scenario specifies them. No lifelines, activation bars, sequence fragments, page frames, cards, or unrelated UML notation are included.

## Verification

The six diagrams pass source-match audits, Q4 semantic SVG validation, and Q5 geometry validation. The final delivery PDFs are vector PDFs verified without embedded raster images. The compactness/refinement report and visual-inspection record are included in `qa/` and `work/`.

## Review status

All Views deliberately retain `visualReview.status: awaiting-user-approval`. The package provides validated artifacts for the user's final visual review; it does not grant approval automatically.
