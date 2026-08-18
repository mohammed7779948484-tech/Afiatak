# Final visual refinement — current-state audit

## Evidence reviewed

- `IMG_1379.jpeg` (lecturer's Collaboration Diagram reference), 1290×958 px.
- Current `CD-02` high-resolution PNG, sliced using the dense-image workflow; inspected tile `tile_012_x004528_y001271.png`.
- Current `CD-02` SVG and editable `.drawio` geometry metadata.

## Lecturer-reference visual language

The lecturer example uses plain participant rectangles and thin communication links. Message groups sit immediately beside or above/below their owning line, and each small open arrow is visually adjacent to the corresponding message group. The title is visually more prominent than the participant labels, and message text is subordinate to participant labels.

## Confirmed current defect

The current CD-02 L01 Backend ↔ Data Store vertical corridor lies at approximately `x=6483` in layout coordinates. Its label group is placed on the left beginning near `x=3554`; short labels therefore leave a visibly detached horizontal gulf before the owning corridor. The inspected PNG tile confirms that the current output can form a floating text column even though it is collision-free. This is inconsistent with the local object + link + numbered-message language of the reference.

## Initial root-cause hypothesis

`_place_link_run` iterates preferred sides, anchors and longitudinal shifts, but its candidate selection accepts the first collision-free rectangle. It uses cardinal `right/left/above/below` placement rather than a link-tangent/normal local frame, does not score candidates by their true shortest distance to the owning polyline, and has no hard own-label-to-link proximity constraint. Consequently, a group can remain far from its own link while passing existing Q5 collision checks.

## Planned corrective direction

Introduce a generic local tangent/normal placement frame, rank candidates by shortest label-edge-to-own-link distance with the smallest safe distance preferred, couple arrow placement to the local group corridor, and add explicit Q5 own-label-to-link proximity validation. Preserve all semantic models, links, messages, and per-scenario coordinates.

## Typography defect confirmed by code review

The current SVG title is 48 px, while participants and messages are both 58 px. The required correction is a shared hierarchy of heading > participant > message, mirrored in the editable diagrams.net export.

## CD-02 post-change visual check

Two high-resolution tiles from the regenerated CD-02 PNG were inspected. L01 message labels now terminate at the nearby edge of the vertical Backend ↔ Data Store corridor; the previous large blank gulf between short labels and L01 is absent. The arrows remain short and open on the corridor, preserving the intended numbered-message reading.

The L03 Backend ↔ Patient Application corridor now uses local stacked annotation lanes. The inspected horizontal/diagonal region shows numbered labels arranged immediately above or below the line with compact direction marks on the same corridor, rather than as a detached remote column. The densest L03 labels use the controlled dense-lane exception, with a measured maximum own-link edge distance of 400.95 layout units; this remains under the explicit Q5 ceiling of 450 and is materially smaller than the prior 2,700–3,500-unit fallback separation.

The new title/message hierarchy is visible in the regenerated output: the heading is larger than participant labels, while message text is smaller and remains readable. The remaining inherent limitation is scenario density, not detachment: CD-02 necessarily contains many long exact labels, so its L03 annotations require multiple local lanes rather than a single short booklet-style stack.

## Family and dense-corridor visual check

The six-diagram contact sheet shows a consistent white academic page, calm monochrome links, simple underlined participant rectangles, and a visibly stronger heading hierarchy across the complete family. No lifelines, activation bars, framed message cards, or decorative panels appear.

A high-resolution CD-05 tile was inspected at the Backend ↔ Data Store corridor. The dense numbered run remains immediately beside the vertical communication line; direction marks are short and open in adjacent local lanes. The Backend object remains clear and the refined smaller message typography preserves room around the dense corridor. Q5 independently confirms the self-message geometry and all collision checks pass.

## CD-06 and vector-output check

A high-resolution CD-06 tile was inspected at its dense operational-exception Backend ↔ Data Store run. The messages are visibly anchored at the nearby right edge of the vertical corridor, with small open direction marks on the corridor and no detached text column. The single-affected-Appointment wording remains present because semantic source-match passed unchanged.

The geometry regression passed for all six scenarios with zero unresolved layout issues, complete geometry metadata, and distinct self-loop bounds where self messages are defined. `pdfimages -list` returned no embedded image rows for every individual PDF and the merged six-page A0-landscape PDF, confirming the release PDF outputs remain vector-only.
