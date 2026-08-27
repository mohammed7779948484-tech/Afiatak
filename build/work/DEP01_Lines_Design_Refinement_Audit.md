# DEP-01 Lines and Design Refinement Audit

## Baseline findings — tiles 001–002

- **LD-01 — Overextended communication corridors.** The top-level patient-to-server route crosses a disproportionately large blank region before reaching its destination. Its long continuous horizontal segment has more visual weight than the client and server nodes it connects.
- **LD-02 — Dense central route band.** Multiple client/server and server/provider paths converge through nearly aligned central corridors. Even though their endpoints are valid, the adjacent long horizontal runs and closely spaced vertical turns make the routing visually difficult to scan at normal report scale.
- **LD-03 — Weak composition balance.** Large unused whitespace above and between node bands combines with overly long wire paths, reducing the compact academic clarity expected of a deployment diagram.

The semantic topology, node ownership, and communication-path endpoints remain frozen. Any repair must be made in the canonical composition, SVG renderer, diagrams.net exporter, and geometry QA—not by patching generated artifacts.


## Baseline findings — tiles 003–006

- **LD-04 — Client-to-server routes span the central field.** The Facility route makes a long horizontal run before its vertical turn, while the Patient and Platform routes occupy neighbouring horizontal bands. The result is technically valid but visually reads as several wires cutting across the composition.
- **LD-05 — Service routes share visual bands with client routes.** The server-to-provider routes use the same broad horizontal field as incoming client paths. At detailed scale they can be traced, but the set is not compact or immediately readable at report scale.
- **LD-06 — Central-server emphasis is diluted.** The node remains structurally central, but surrounding wire length and empty space make the eye follow lines rather than the intended client → server → provider topology.

Planned correction: retain all node identities, containment, and endpoints, but recompose the canvas and path channels to shorten routes, reserve separate inbound/outbound corridors, and produce a more balanced academic landscape.


## Baseline findings — tiles 007–011

The right-side provider nodes remain visually clean and are not the source of the complaint. The design issue is concentrated in the **routing geometry and composition density around the central server and PostgreSQL environment**. Several communication paths occupy long parallel horizontal bands that stretch across wide empty regions, and their turns are packed into a narrow central corridor. At normal viewing scale, this makes the diagram feel line-dominated even though the endpoints are technically correct.

A second issue is the **large blank field between node bands**. The clients, central server, database environment, and right-side services are all validly placed, but the current separations make the communication paths much longer than necessary. This weakens the intended visual hierarchy of **client → centralized server → external provider/database** and causes the eye to follow wires before it reads the nodes.

The corrective direction is now clear: retain the frozen topology, keep all seven paths and their endpoints, but **recompose the canvas more compactly**, move the central server and PostgreSQL environment into a tighter academic grouping, shorten inbound and outbound corridors, and separate client-side and provider-side path channels so that the lines read as deliberate orthogonal routes rather than broad continuous stripes.


## Recomposition review — tiles 001–002

The compact layout reduces the canvas from **12400×7200** to **10800×6400** (approximately 13% narrower and 11% shorter) while preserving every top-level node and communication-path endpoint. The Patient route now uses a short dedicated ingress corridor and the WhatsApp route leaves the server via a separate upper egress corridor. At detailed scale the two paths remain distinguishable, and their corners are deliberate orthogonal turns rather than extended parallel stripes.

No post-render correction is required in the upper-left or upper-central regions.


## Recomposition review — tiles 003–004

The central server now reads as the visual anchor. Its upper provider route turns through a short, dedicated corridor before reaching WhatsApp Authentication Provider; the client route terminates independently at the server's left boundary. WhatsApp and Payment retain simple 3D UML node silhouettes, but the reduced canvas places them closer to their relevant server side without crowding labels or contained artifacts.

No visual correction is required in the upper provider region.


## Recomposition review — tiles 005–008

The Facility, Payment, and Notification regions confirm the intended repair. Each client and provider uses a dedicated approach corridor at the nearest relevant side of the centralized server. The resulting lines have clear right-angle turns, no long shared run across the central field, no label crossings, and no intrusion into an artifact or node face. The server remains dominant, while the three internal deployed artifacts remain readable and visually quiet beneath its title.

No visual correction is required in the middle-row client, server, or provider regions.


## Recomposition review — tiles 009–010

The lower-left and lower-centre regions are now balanced. Platform Administrator Client Device reaches the server through a separate lower ingress corridor, while PostgreSQL Database Environment sits directly beneath the server and is connected by a short, clear vertical path. The database node, its artifact, and its unresolved-placement subtitle remain legible and isolated from all client/service routes.

No visual correction is required in the platform or PostgreSQL regions.


## Recomposition review — tiles 011–012 and acceptance

The final lower-right inspection confirms that Notification Service retains only its approved path and Map Service remains intentionally unconnected with its concise unresolved-caller subtitle. Across all twelve ordered overlapping tiles, no clipped label, node collision, path-through-node defect, label collision, accidental shared route, or unintended connector was found.

The final composition is materially more compact, with shorter communication paths and a clearer visual hierarchy: clients on the left, the centralized logical execution boundary at the centre, PostgreSQL directly beneath it, and external providers on the right. The original topology is unchanged. No additional source-level repair is required.
