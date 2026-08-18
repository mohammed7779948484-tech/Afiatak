# CD-01 Visual Inspection Notes

## Round 1 — Tiles 001–002

The first two upper-left tiles show only the white page field and the thin black page border. No unintended shapes, text clipping, or raster artefacts are visible in these regions. This is consistent with a centred title and a spatial network positioned away from the left margin; the title is outside the first two horizontal tile positions.

Next: inspect tiles 003–004 in reading order.

## Round 2 — Tiles 003–004

The centred page title is present, readable, and fully contained across the overlap between tiles 003 and 004. The upper participant box, **Aafiatak Data Store**, is rendered as the required plain rectangle with clear readable typography. The L01 label stack begins to the right of this participant, as intended. Several long diagonal leaders are visible entering that stack; they require inspection across the next tiles because they may add unnecessary visual clutter around the otherwise single reusable structural link.

Next: inspect tiles 005–006 in reading order.

## Final Inspection Round 1 — Corrected tiles 001–002

The upper-left blank margins and page border remain clean after the routing correction. No stray leader line, clipped label, or unintended UML construct appears in either tile.

Next: inspect corrected tiles 003–004.

## Final Inspection Round 2 — Corrected tiles 003–004

The page title is readable and fully contained. The **Aafiatak Data Store** object box is clear and proportionate. The previously observed fan of diagonal leader lines is absent after correction. L01's stacked labels remain adjacent to the vertical Backend–Data Store structural link; the next tiles will confirm their full text and local arrow markers.

Next: inspect corrected tiles 005–006.

## Final Inspection Round 3 — Corrected tiles 005–006

All four L01 labels are readable with their required visible numbers: **4**, **5**, **16**, and **17**. Their text is presented once each in an orderly vertical stack, with no overlap or clipping at the page edge. Tile 006 contains only the right-hand white space of those label boxes, confirming the stack is contained before the canvas edge.

Next: inspect corrected tiles 007–008.

## Final Inspection Round 4 — Corrected tiles 007–008

The far upper-right page field is clear and bounded without clipped diagram content. The first tile of the second row begins the **Patient Application** rectangle cleanly; no connector passes through that participant box.

Next: inspect corrected tiles 009–010.

## Final Inspection Round 5 — Corrected tiles 009–010

The L02 block visibly contains the six required labels with numbers **2, 8, 11, 13, 15, 18**. The single horizontal structural link between Patient Application and Backend remains distinct from its short directional arrow markers; opposing request directions are visually legible. No vertical lifeline, activation bar, or sequence frame appears.

Next: inspect corrected tiles 011–012.

## Final Inspection Round 6 — Corrected tiles 011–012

The **Aafiatak Backend** box is central and unobstructed. The L01 vertical structural link is rendered once with clearly opposing arrow markers for its bidirectional messages. The self-message for **3. Normalize and validate phone number** appears as a visible loop attached to Backend, rather than a fabricated participant. The L03 stack correctly displays labels **6** and **7** with no text overlap.

Next: inspect corrected tiles 013–014.

## Final Inspection Round 7 — Corrected tiles 013–014

The remaining right-hand portions of the L03 label boxes are within the canvas and do not overlap another participant or link. The far right of the second row is intentionally clear; the WhatsApp Authentication Provider lies in the lower row according to the graph-derived layout. No clipping or non-UML notation is present.

Next: inspect corrected tiles 015–016.

## Final Inspection Round 8 — Corrected tiles 015–016

The L04 stack contains the exact required labels **1, 10, 14, 19**, and its diagonal structural link connects the correct participant boundary points. However, the tile shows that this label stack overlaps the diagonal structural-link corridor, creating a text/connector collision. This is a routing defect. The L04 label block must be moved into the free left-side area before CD-01 can pass visual QA.

Action: reposition L04 label block; re-render; restart the affected visual inspection.

## Final Inspection Round 9 — L04 correction verification

The L04 block now sits in a clear left-side corridor. Its four labels are fully readable and no longer intersect the diagonal structural link. The link remains visible to the right with distinct directional arrow markers and does not pass through any label or participant box. The prior routing defect is corrected.

Next: inspect final-version tiles 017–018.

## Final Inspection Round 10 — Tiles 017–018

The lower central canvas remains free of accidental elements. The **12. Validate expiry, single-use and security limits** self-message is visibly separate from message 3 and is drawn as an attached Backend loop. The diagonal L03 link exits Backend at its boundary and remains outside the participant box; its directional markers do not collide with the self-message labels.

Next: inspect final-version tiles 019–020.

## Final Inspection Round 11 — Tiles 019–020

The **WhatsApp Authentication Provider** participant box is clear, fully inside the page, and uses the same rectangular geometry and typography as the other participants. L03 enters its upper-left boundary and L05 approaches through a separate lower-left path; neither connector passes through the box. The self-message 12 label remains readable and is visually separated from the provider box.

Next: inspect final-version tiles 021–022.

## Final Inspection Round 12 — Tiles 021–022

The lower-left page margin and continuing portion of the WhatsApp provider box are clean. No label, connector, or shape is clipped at the border. Tile 022 is intentionally empty page space between the outer margin and the lower communication network.

Next: inspect final-version tiles 023–024.

## Final Inspection Round 13 — Tiles 023–024

The **Visitor** participant is legible in a plain UML rectangle. The L04 link joins its upper boundary and L05 joins its right boundary, while both lines stay outside the box and do not cross each other within it. The relevant directional markers remain visible on their separate structural links.

Next: inspect final-version tiles 025–026.

## Final Inspection Round 14 — Tiles 025–026

The sole L05 message, **9. Deliver OTP via official WhatsApp channel**, is readable in a dedicated label block below its diagonal structural link. The directional arrow marker remains on the link and does not collide with the label. The label remains fully inside the canvas; the apparent cropped word in tile 026 is only the overlap boundary, with the full text confirmed in tile 025.

Next: inspect final-version tiles 027–028.

## Final Inspection Round 15 — Tiles 027–028

The lower-right margin and page border are clean. No clipped participant, label, arrowhead, or extraneous notation appears at the canvas edge. The final PNG inspection has covered all regions of the rendered page, including all overlapping tiles in reading order. The corrected CD-01 visual routing now passes: labels are readable, links meet participant boundaries, self loops are visible, and no lifelines or activation bars are present.

## Final SVG Opening Record

The final CD-01 SVG was opened directly in a browser and loaded successfully as a scalable page; its page border and native SVG document were visible. Because the 16,000-unit-wide canvas exceeds the browser viewport, the complete detailed routing inspection was performed from the separately rendered 8,192×5,325 PNG using all ordered overlapping tiles. The final vector PDF was also opened separately.
