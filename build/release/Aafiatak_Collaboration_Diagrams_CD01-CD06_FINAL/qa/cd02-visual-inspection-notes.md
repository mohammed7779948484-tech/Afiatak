# CD-02 Visual Inspection Notes

## Round 1 — Tiles 001–002

The upper-left page field and border are clean. The L03 message block begins in tile 002 at the expected lower edge; no unintended participant, lifeline, activation bar, or clipped graphic is visible in this region.

Next: inspect tiles 003–004 in reading order.

## Round 2 — Tiles 003–004

The title and **Aafiatak Data Store** participant rectangle are visible, correctly styled, and fully inside the page. The vertical L01 link starts at the Data Store boundary with alternating directional arrow markers. The 14-message L01 stack starts in a separate right-hand column; it remains outside the participant box in these tiles. Its full text and relationship to the link must be checked across the next tiles.

Next: inspect tiles 005–006 in reading order.

## Round 3 — Tiles 005–006

All fourteen L01 labels are present in order and readable in the right-hand stack: **3, 4, 5, 6, 10, 11, 15, 16, 17, 18, 27, 28, 29, 30**. The stack is contained within the page; the repetitive blank portions in tile 006 are the right-hand extensions of its opaque label boxes rather than clipped text. No forbidden UML notation appears.

Next: inspect tiles 007–008 in reading order.

## Round 4 — Tiles 007–008

The far upper-right page margin is clean and the L01 stack remains inside the canvas. The second row begins the **Patient Application** participant box with its border and label intact. No connector crosses the participant box in this first visible segment.

Next: inspect tiles 009–010 in reading order.

## Round 5 — Tiles 009–010

The L03 label stack is readable and contains the required sequences **2, 7, 9, 12, 14, 21, 24, 33**. Its structural link between Patient Application and Backend is rendered once as a slightly diagonal line with the corresponding short directional arrows. The arrows stay outside the participant boundaries and no label crosses the link in these tiles.

Next: inspect tiles 011–012 in reading order.

## Round 6 — Tiles 011–012

The **Aafiatak Backend** rectangle remains central. The long L01 vertical structural link is drawn once with alternating arrows. L02’s messages **31–32** are visible as a two-row stack and L04’s messages **19, 20, 25, 26** appear in a separate stack below; both stay readable and outside the Backend box. The diagonal communication paths remain distinct from the label backgrounds in this region.

Next: inspect tiles 013–014 in reading order.

## Round 7 — Tiles 013–014

The portions of L02 and its two label boxes remain within the page, while the far right margin is clean. The visible edges terminate at participant boundaries rather than creating detached or duplicated connectors. No Sequence lifeline, activation bar, or fragment is visible.

Next: inspect tiles 015–016 in reading order.

## Round 8 — Tiles 015–016

The L05 message labels **1, 8, 13, 34** are complete and readable, but the vertical Patient–Patient Application structural link crosses through their label rectangles. This is a routing defect, even though the text remains legible. The L05 stack must move to a clear side corridor before CD-02 can pass visual QA.

Action: reposition L05 label block and re-render before continuing visual inspection.

## Round 9 — L05 correction verification

After rerendering, the vertical L05 structural link remains in the left corridor and the L05 label stack now occupies a clear central corridor. The required labels **1, 8, 13, 34** are complete, readable, and do not intersect the link. The routing defect found in Round 8 is corrected.

Next: inspect final-version tiles 017–018.

## Round 10 — Tiles 017–018

The L07 message **23. Return to application** occupies a separate label row below its communication path. The nearby diagonal links remain in open whitespace and reach participant boundaries without passing through an unrelated object. No extra link has been introduced for this message.

Next: inspect final-version tiles 019–020.

## Round 11 — Tiles 019–020

The **Payment Gateway** participant rectangle is fully inside the page. The three payment-related communication paths approach separate edges of the box and do not cross its interior. Their arrow markers are distinct, and no participant or label overlap is visible in this region.

Next: inspect final-version tiles 021–022.

## Round 12 — Tiles 021–022

The lower-right page field is clear, and the **Patient** participant box is legible and fully inside the canvas. The visible communication path connects to the Patient boundary rather than entering its interior. No clipped label or forbidden notation appears.

Next: inspect final-version tiles 023–024.

## Round 13 — Tiles 023–024

The L06 link reaches the Patient boundary and continues toward Payment Gateway through open space. Its sole required label, **22. Complete gateway payment interaction**, appears once in a dedicated box that does not intersect the diagonal link. The lower page border is preserved.

Next: inspect final-version tiles 025–026.

## Round 14 — Tiles 025–026

The remaining lower-centre corridor contains only the expected L06 path and the trailing portions of its label box. There is no cross-link, clipped text, or off-canvas participant. The lower border remains clean.

Next: inspect final-version tiles 027–028.

## Round 15 — Tiles 027–028

The final lower-right tiles show only the expected participant boundary, page border, and white margin. No clipped labels, stray arrows, or hidden UML notation is present. The complete final PNG has now been inspected in manifest order. CD-02 passes visual routing after the L05 correction: all participant boxes are rectangular, links are reused, messages are numbered and readable, and no lifelines or activation bars appear.

## Final SVG Opening Record

The final CD-02 SVG was opened directly in a browser and loaded successfully as a scalable document with its native page boundary. The complete routing/readability inspection used all ordered PNG tiles because the SVG canvas is substantially wider than the browser viewport. The final A0 vector PDF was opened separately and contains no embedded raster objects.
