# DEP-01 Visual Inspection Audit

## Final-render review in progress — 2026-08-27

The final PNG is **8192×4757**, so it is being inspected as 12 ordered overlapping 2300×2300 grid tiles. The review checks the actual rasterized SVG rather than source/XML only.

### Tiles 001–003

- **Tile 001 — Patient Mobile Device:** The node has a recognisable plain 3D UML deployment silhouette, a clear central title, and two contained item blocks for `Android / iOS` and `Patient Application`. The blocks are inset, readable, and contained. The communications line reaches the node boundary without an arrowhead.
- **Tile 002 — title/client-server transition:** The serif title is visibly clean and university-report appropriate. The incoming client route is orthogonal and has no message number or directional arrow. The central server begins in the expected middle column, with contained software blocks visually distinct from the outer deployment node.
- **Tile 003 — central/right upper transition:** The central server's 3D boundary, contained Dashboard blocks, and the upper external-service corridor remain legible and monochrome. The apparent text truncation occurs only at tile boundaries; adjoining tiles are being used to verify full labels.

No clipping, use-case/sequence notation, cloud/provider graphics, or arrowheads were observed in the inspected upper tiles. The final verdict remains pending the remaining tiles and whole-page reconciliation.

### Tiles 004–005

- **Tile 004 — WhatsApp Authentication Provider and Payment Gateway:** Both external service nodes use the same restrained 3D UML deployment notation and readable centered names. WhatsApp wraps across two balanced lines without clipping; Payment is compact and legible. No provider-specific logo, unapproved infrastructure, or arrowhead is present.
- **Tile 005 — Facility Client Device:** The device node is spacious enough for `Desktop / Tablet` and `Web Browser`, both rendered as contained runtime labels. The depth faces are visibly coherent and the communications route leaves from the right boundary in the intended corridor.

No visual defect requiring a source/composition correction was observed in tiles 004–005.

### Tiles 006–008

- **Tiles 006–007 — Aafiatak Centralized Server:** The logical server node is dominant and centrally placed. It contains exactly three visibly bounded items: `Facility Web Dashboard`, `Aafiatak Platform Administration Dashboard`, and `Aafiatak Backend`. The italic physical-placement note is legible and makes the unresolved placement explicit rather than inventing a provider or infrastructure node. The three client arrivals and three external-service departures use separate orthogonal lanes.
- **Tile 008 — Payment Gateway and Notification Service:** The two external nodes are evenly aligned in the right-hand column, use the same standard 3D node notation, and retain clear centered labels. The blank interiors introduce no invented implementation technology or deployment artifact.

The central-to-external routes are visually unarrowed, noncrossing, and contained in dedicated corridors. No source correction is required after tiles 006–008.

### Tiles 009–010

- **Tile 009 — Platform Administrator Client Device:** The longest client-node name wraps across two clear centered lines and the single `Web Browser` item is visibly contained. Its connection is routed from the right boundary through the lower client corridor, not through the device contents.
- **Tile 010 — PostgreSQL Database Environment:** The database environment is centered beneath the server and uses the same logical-node notation rather than an unsupported database/server infrastructure icon. The two-line node name, `PostgreSQL Database` contained item, and italic `Physical placement unresolved` note are all legible. The server-to-database path is vertical at the boundary and is unarrowed.

No node, label, or connector clipping was observed in tiles 009–010. The visible continuity across tile edges confirms that partial texts in individual tiles are crop effects, not truncated source text.

### Tiles 011–012

- **Tile 011 — lower central/right reconciliation:** PostgreSQL remains visually below the server with its contained `PostgreSQL Database` item and explicit unresolved-placement note. The surrounding corridors remain clear of labels and connectors.
- **Tile 012 — Notification Service and Map Service:** Notification Service is displayed as the final connected external service. Map Service is present in the lower right as an external deployment node with the visible `Technical caller unresolved` note and no communication path; this preserves the intentional constraint exactly.

## PNG acceptance result

All twelve ordered overlapping tiles were reviewed. The final PNG has clear title hierarchy, standard 3D deployment nodes, correctly contained runtime/component labels, solid unarrowed orthogonal communication paths, no clipping, no visible collisions, no foreign UML notation, and no invented infrastructure. The view is consistent with the lecturer's simple deployment example: nodes contain deployed material and solid lines communicate between nodes. SVG review is the remaining acceptance check.


## Final UML notation refinement baseline — 2026-08-27

The current final SVG and the 8192×4757 PNG were opened at fit-to-page scale. The overall deployment topology remains orderly and semantically correct, with the expected left/centre/lower-centre/right composition, plain unarrowed paths, and no cloud/DevOps imagery. However, the contained `Android / iOS`, `Web Browser`, deployed applications, backend, and `PostgreSQL Database` blocks all use the same module/component-like marker and outline. This makes execution environments visually indistinguishable from deployed software, which is the targeted notation-fidelity defect for this refinement.

The next revision will preserve all node and path coordinates unless a collision emerges, but will render a small, secondary `«executionEnvironment»` type line for runtime/access environments and `«artifact»` for deployed software inside their existing owner nodes. The node title remains visually dominant, and all external nodes retain the existing simple UML deployment-node silhouette.


## Lecturer deployment-reference comparison — 2026-08-27

The actual lecturer reference was opened visually. Page 11 introduces **10. Deployment Diagram**; page 12 shows the example. Its visual language is deliberately simple: shallow 3D rectangular deployment nodes, compact contained blocks carrying the small UML component/artifact marker, node names above or within the node, and plain connecting lines. It does not use clouds, vendor icons, coloured architecture cards, protocols, or DevOps decoration.

The DEP-01 outer 3D node silhouette and monochrome path language are already compatible with this reference. The contained-item refinement must therefore stay compact and academic: a small secondary stereotype line will distinguish runtime environments from deployed software, while retaining the lecturer-compatible contained-block silhouette and marker. No topological or infrastructure change is justified by the reference.


## Refined final-render review — tiles 001–002

- **Patient Mobile Device:** The parent node now has a secondary `«device»` stereotype above its dominant name. `Android / iOS` is visually a small 3D `«executionEnvironment»` rather than a component-like module. `Patient Application` uses a visibly distinct folded-corner `«artifact»` block. The distinction is readable at the detailed inspection scale and both remain inside the device.
- **Central-server upper transition:** `Aafiatak Centralized Server` now keeps its approved visible name while adding the secondary `«executionEnvironment»` stereotype, accurately signalling a logical execution boundary rather than declaring a particular physical machine. The first server-contained dashboard is a folded-corner `«artifact»`. The patient communication path remains solid, unnumbered, and unarrowed, with no collision with the new title/contained text.

No visual correction is required from tiles 001–002.


## Refined final-render review — tiles 003–004

- **Central server and provider corridor:** The `«executionEnvironment»` line above the centralized-server name is readable but subordinate. Its folded-corner `«artifact»` blocks are compact and visibly different from the execution-environment block used on the client devices. The existing orthogonal corridors remain clear of titles and block text.
- **WhatsApp Authentication Provider and Payment Gateway:** Both remain deliberately unadorned 3D external deployment nodes with readable wrapped names. Their communication paths are simple solid lines with no arrowheads, protocol labels, cloud imagery, or added provider assumptions.

No visual correction is required from tiles 003–004.


## Refined final-render review — tiles 005–006

- **Facility Client Device:** The secondary `«device»` stereotype, dashed `«device»` Desktop/Tablet context, and 3D `«executionEnvironment»` Web Browser now communicate their separate roles without adding an unsupported hardware choice or duplicating the Facility Web Dashboard on the client.
- **Centralized Server contained software:** Facility Web Dashboard, Aafiatak Platform Administration Dashboard, and Aafiatak Backend all appear once as folded-corner `«artifact»` blocks. The long Platform Administration name remains visible and does not collide with either client, service, or database routes. The inherited physical-placement note remains contained and legible.

No visual correction is required from tiles 005–006.


## Refined final-render review — tiles 007–008

- **Payment and Notification corridors:** The folded-corner artifacts inside the central server remain clear of CP06 and CP07. Connector routes remain orthogonal where routed and are visibly plain solid communication paths without arrowheads, labels, or protocol claims.
- **Payment Gateway and Notification Service:** Both external nodes remain uncluttered, proportionate 3D UML deployment nodes. Their labels are readable, their physical page bounds are clear, and no stereotype or artifact is invented within an external service node.

No visual correction is required from tiles 007–008.


## Refined final-render review — tiles 009–010

- **Platform Administrator Client Device:** The longer approved node name wraps cleanly under a secondary `«device»` marker. Its sole Web Browser content is an execution-environment cube; no unsupported physical hardware type or duplicate dashboard deployment appears.
- **PostgreSQL Database Environment:** The node now explicitly and visually reads as `«executionEnvironment»`, while its contained PostgreSQL Database is a separate folded-corner `«artifact»`. The physical-placement subtitle remains intact. CP04 stays a plain vertical communication path and has clear separation from the node title and contained artifact.

No visual correction is required from tiles 009–010.


## Refined final-render review — tiles 011–012

- **Lower-centre/notification region:** PostgreSQL Database remains exactly once as a folded-corner artifact inside its explicit execution environment; Notification Service remains a separate external node with its approved single server path. No overflow, clipping, arrowhead, or accidental path crossing is visible.
- **Map Service:** The Map Service node remains present, legible, and deliberately unconnected. Its `Technical caller unresolved` subtitle is fully visible; no line reaches the node from any client, server, or provider.

All twelve ordered overlapping PNG tiles were inspected. The final detailed review found no remaining visual defect requiring a source-level correction.
