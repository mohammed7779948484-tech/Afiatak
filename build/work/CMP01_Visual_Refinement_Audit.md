# CMP-01 Visual Refinement Audit

## Baseline review

The current final artifact was read as a full 8192×4608 PNG and as 12 ordered overlapping 2300×2300 tiles. The lecturer reference on PDF page 11 uses the classic UML Component silhouette: a recognisable rectangle with two **attached** small tabs at the left perimeter, plain black strokes, readable names, and uncomplicated connectors. The baseline SVG instead draws two floating rectangles near the top-right interior of each component; this is semantically harmless but visually weaker and not consistent with the `shape=module` component form already emitted to diagrams.net.

### Baseline tiles 001–002

`Patient Application` and `Facility Web Dashboard` use the two-floating-rectangle SVG glyph. Their repeated `Aafiatak Application Interface` labels sit inside their component bodies near the right edge, making them compete with the component identity rather than clearly belong to their right-side sockets. The required sockets are present but their labels are too far from the glyph relative to the large available whitespace. The route toward Backend is visibly long and the overall canvas has excessive open space.

### Baseline tiles 003–004

The Backend right-side sockets are recognisable, but the interface labels are placed inside Backend and occupy its name/identity field. The provider labels are also inside their component bodies even though their lollipop glyphs sit outside the left boundary. `WhatsApp Authentication Provider` and `Payment Gateway` show the same floating-tab SVG glyph issue. The result is clear enough semantically but does not give interface labels a local visual relationship with their own lollipop/socket.

### Baseline tiles 005–006

The lower client component repeats the same inside-body interface-label pattern. `Aafiatak Backend` is centred semantically but has large unused interior space while its provided and persistence-interface labels consume interior positions. The three inbound client connectors use long vertical trunks before converging at the backend lollipop. The backend-to-database assembly is traceable but longer than necessary because of the broad original canvas and separated vertical levels.

### Baseline tiles 007–008

The three right-side Backend sockets are vertically distinct and their paths avoid component bodies, but all labels remain inside Backend. Payment Gateway and Notification Service show a lollipop outside their left edge while the matching label remains inside the body, creating the same detached visual hierarchy. The routes are mechanically clean but spread too widely across the page relative to the lecturer's compact example.

### Baseline tiles 009–010

The long platform-dashboard name wraps cleanly, yet its interface label still competes inside the same component body. PostgreSQL is correctly a persistence component rather than an ERD, but it is positioned too far below Backend for the otherwise simple relationship. Its `Persistence Interface` label appears inside the component; the provider lollipop and required socket are separated by a long vertical corridor.

### Baseline tiles 011–012

`Notification Service` and `Map Service` are semantically correct. Map remains intentionally unconnected, with a single provided-interface lollipop; this must remain unchanged. Both provider labels, however, sit inside their components and are visually detached from the left-edge lollipops. The final lower-right region confirms that the original 16000×9000 composition has substantial unused page space. All 12 baseline tiles were inspected in row-major order.

## Baseline defect register

| ID | Actual defect observed | Canonical correction target |
|---|---|---|
| V-01 | SVG component notation is a plain box with two floating rectangles, while diagrams.net uses `shape=module`. | Shared visual token plus SVG component glyph and draw.io parity. |
| V-02 | The 16000×9000 layout has excessive inter-column and vertical whitespace. | Component composition only; recompose client, Backend, database, and providers without scaling the diagram blindly. |
| V-03 | Interface labels sit inside their owners and compete with component names. | Shared interface-label placements and label metrics. |
| V-04 | Labels are too distant from their own lollipop/socket relative to the available exterior lanes. | Label-to-glyph proximity rule in Q5 plus composition anchors. |
| V-05 | The three inbound client routes have long trunks and visually ambiguous late convergence. | Deterministic connector corridors and endpoint lanes in composition. |
| V-06 | Q5 does not yet protect name/glyph clearance, label-to-glyph distance, connector-label intersections, connector crossings/overlaps, stem attachment, or compactness. | Component SVG QA and focused regression tests. |

## Final refined-render inspection — 2026-08-27 (tiles 001–002)

- **A — Patient Application:** The new left-attached two-tab component glyph is visually integrated with the component boundary rather than appearing as detached decorative rectangles. The component name is legible, centred in the body, and clear of the glyph.
- **B — upper client socket and ingress:** The required socket is visibly attached to the right boundary through its short stem. Its external two-line label is legible and sits beside its own glyph. The connector leaves from the socket via an orthogonal free corridor; no text, glyph, or component-boundary collision is visible in this region.
- **Title crop note:** tile slicing intentionally crops the page title across tile boundaries; this is not a final-render clipping defect and will be confirmed in whole-page review.
- **C — Backend and upper provider corridor:** The backend boundary, its external required socket, and the WhatsApp provider lollipop have visible attached stems. The `WhatsApp Authentication Interface` labels are external to their owner components and remain separate from the orthogonal route.
- **D — WhatsApp Authentication Provider / Payment Gateway:** Each provider has the same attached two-tab UML component glyph, a centred name that wraps legibly when needed, and an attached external lollipop. No floating-glyph, connector-through-name, or clipping defect is visible. The title text is complete across the adjoining tiles, confirming the apparent truncation in one tile is only a tile boundary.
- **E/F — Facility Web Dashboard and central convergence:** `Facility Web Dashboard` uses the same coherent UML glyph and clear interior name. Its socket and the backend lollipop are visibly attached to their owners. The matching labels sit externally and are clear of the short horizontal terminal route; the orthogonal ingress lane remains distinct without a connector/label or connector/component crossing. The backend persistence socket and label also remain external to the Backend name field.
- **G/H — Backend, Payment and Notification lanes:** Backend remains visually central and its name dominates its body. The WhatsApp, Payment, and Notification sockets are vertically separated on its right boundary; labels are external, readable, and do not overlap their matching connector. The visible Payment and Notification provider lollipops are attached to short stems on the providers’ left boundaries. Their routes are crisp orthogonal paths with open clearance and no accidental crossings.
- **I/J — Platform Administration and PostgreSQL:** The longest client name wraps into two balanced lines and remains clear of the component glyph. Its socket label is external and the rerouted line uses a distinct near-Backend ingress lane, avoiding the label corridor and the backend’s provided-interface label. PostgreSQL is visually close below Backend; both persistence labels and the socket/lollipop pair are legible and externally placed. No line cuts through a label or component body in this lower central region.
- **K/L — Notification, PostgreSQL and Map Service:** The PostgreSQL persistence pair is visibly attached and connected by one short vertical assembly route. Notification is cleanly separated on the provider side. `Map Service` has a single attached lollipop and external `Map / Location Interface` label with no connector, preserving the explicitly intentional unresolved-consumer condition. No clipping, floating tab, crossed line, or unintended Map relationship was observed.

## Final review conclusion

The actual final 8192×4757 PNG was inspected in all 12 overlapping row-major tiles, covering required review regions **A–L**. The final renderer presents coherent left-attached UML module glyphs; supplied interfaces as attached lollipops; required interfaces as attached sockets; and uncluttered orthogonal assembly connectors. The recomposed 12400×7200 canvas is materially tighter than the 16000×9000 baseline while retaining whitespace around labels and connectors. The appearance is a restrained, white, dark-stroke academic component diagram consistent with the lecturer reference rather than a dashboard or decorated architecture graphic. This is an implementation-side visual inspection only; `visualReview.status` remains `awaiting-user-approval` and no user approval is implied.
