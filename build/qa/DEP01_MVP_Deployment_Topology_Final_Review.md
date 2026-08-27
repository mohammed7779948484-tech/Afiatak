# DEP-01 — Final UML Notation Refinement Review

## Scope, semantic boundary, and conclusion

This review records the **final UML-notation and visual-fidelity refinement** of the one approved logical Deployment Diagram for the Aafiatak Medical Appointment Booking System. The task changed only the shared visual representation of deployed contents and logical execution boundaries. It did **not** modify the approved deployment topology, semantic model inventory, ViewSpec selection, communication-path endpoints, or any open technical decision.

> **Visual-review boundary.** The final SVG and final PNG were actually reviewed by Manus AI. This confirms the recorded artifact was inspected; it is not user approval. The ViewSpec status remains `awaiting-user-approval`.

| Item | Final value |
|---|---|
| Diagram ID / View ID | `DEP-01` / `aafiatak-mvp-deployment` |
| Reviewed execution specification | `docs/deployment-specs/Aafiatak_DEP01_MVP_Deployment_Topology_FINAL_REVIEWED.md` |
| Final SVG / PNG review hash | `b2349ccf435c11990259abb28ee5c62aec88e198ff4f9096e43f88d5cbabe992` (PNG) |
| Canvas / preview | 10800×6400 SVG artboard / 8192×4855 PNG |
| Visual-review state | `awaiting-user-approval` |

## Final semantic inventory

| Contract item | Required | Verified |
|---|---:|---:|
| Deployment Diagrams | 1 | 1 |
| Top-level Deployment Nodes | 9 | 9 |
| Communication Paths | 7 | 7 |
| Internal software components mapped | 5 | 5 |
| External service Nodes | 4 | 4 |
| Map Service Communication Paths | 0 | 0 |
| Invented infrastructure Nodes | 0 | 0 |

The final diagram still contains only Patient Mobile Device, Facility Client Device, Platform Administrator Client Device, Aafiatak Centralized Server, PostgreSQL Database Environment, WhatsApp Authentication Provider, Payment Gateway, Notification Service, and Map Service. The seven approved communication paths have their same endpoints, and Map Service remains a deliberate zero-path exception.

## UML notation refinement applied

| Visual concern | Final treatment | Rationale |
|---|---|---|
| Client Device | Outer shallow 3D UML node with secondary `«device»` marker | Retains the approved node name while making the device role explicit and subordinate to the name. |
| Android / iOS and Web Browser | Small contained 3D `«executionEnvironment»` blocks | Expresses runtime/access environment rather than business software. |
| Desktop / Tablet | Small dashed contained `«device»` context block | Shows the approved access context without claiming a specific hardware product or duplicating dashboard software. |
| Patient Application, both Dashboards, Backend, PostgreSQL Database | Folded-corner `«artifact»` blocks | Makes deployed software visibly different from execution environments, without importing Component-Diagram lollipops, sockets, or dependencies. |
| Aafiatak Centralized Server | Approved name retained with secondary `«executionEnvironment»` marker | Clarifies a logical server-side boundary rather than committing to one physical server machine. |
| PostgreSQL Database Environment | Secondary `«executionEnvironment»` marker containing the PostgreSQL `«artifact»` | Preserves the unresolved co-location/separation decision and avoids renaming it to an unsupported Database Server. |
| External services | Simple unadorned shallow 3D UML deployment nodes | Keeps WhatsApp, Payment, Notification, and Map as external runtime/service boundaries without vendor, cloud, or actor imagery. |
| Communication paths | Solid, unnumbered, unlabeled, unarrowed paths at node boundaries, routed through short dedicated corridors | Preserves their non-temporal UML Communication Path meaning while preventing the line-dominated composition seen before the final routing refinement. |

## Nine-pass final review record

| Pass | Evidence checked | Finding | Result |
|---:|---|---|---|
| 1. Semantic freeze | DEP-01 model, ViewSpec, expected-count checks, traceability | The 9-node / 7-path topology, mappings, and open decisions are unchanged. | Passed |
| 2. Lecturer deployment notation | Actual lecturer PDF introduction page and deployment-example page | The shallow 3D nodes, contained blocks, monochrome palette, plain lines, and academic simplicity remain faithful to the reference. | Passed |
| 3. Device vs Execution Environment | SVG/PNG regions for all three clients and Q4 notation assertions | Devices use `«device»`; Android/iOS and browsers use `«executionEnvironment»`; Desktop/Tablet is device context. | Passed |
| 4. Deployed software / artifact | SVG/PNG server, patient, and PostgreSQL regions; Q4 inventory/notation checks | The five approved deployed software items are distinct folded-corner `«artifact»` blocks, not generic runtime/component boxes. | Passed |
| 5. Communication Paths | SVG metadata, Q4/Q5, final PNG tiles, draw.io lint | All seven paths are solid, unnumbered, unarrowed, endpoint-attached, and use separate short client/provider corridors without unrelated node or label crossings. | Passed |
| 6. Open decisions / no invention | Model/ViewSpec, visible notes, forbidden-content checks | Map caller and DB placement remain unresolved; no cloud, provider, OS, framework, container, proxy, or invented node appears. | Passed |
| 7. SVG / diagrams.net parity | Shared `ContainedItem` visual model, SVG renderer, draw.io exporter, export test | Both exports consume the same visual kind, stereotype, dimensions, routes, and shared tokens. | Passed |
| 8. Geometry / readability | DEP-01 Q5, final SVG/PNG visual review, draw.io strict lint | No clipping, node or label overlap, escaped contained item, path collision, or arrowhead was found. | Passed |
| 9. Actual final render comparison | Final SVG opened directly; final 8192×4855 PNG viewed at fit-to-page and as 12 overlapping tiles | The compact 10800×6400 recomposition and all required regions A–K were inspected, including Map Service's intentionally unconnected state. | Passed |

## QA and regression evidence

| Gate / check | Result |
|---|---|
| Source registration validation | Passed |
| DEP-01 model validation | Passed |
| DEP-01 ViewSpec validation | Passed |
| DEP-01 traceability | 16/16 records covered |
| DEP-01 focused test suite | 9 passed |
| Full regression suite | 34 passed |
| DEP-01 Q4 structural QA | Passed; no diagnostics |
| DEP-01 Q5 geometry QA | Passed; no diagnostics |
| CMP-01 QA after shared-pipeline regression check | Passed |
| Editable diagrams.net strict structural lint | 0 errors; 0 warnings; score 0 |
| Recorded preview hash matches inspected artifact | True |

The focused tests were written before implementation and initially failed as expected: they exposed the absence of typed execution-environment, device-context, and artifact rendering, the absence of logical-node stereotypes, and the absence of draw.io parity. The final tests exercise real SVG and draw.io exports, mutate a runtime element into an artifact to verify that Q4 rejects the regression, and constrain the composition to the shorter dedicated route corridors introduced in the final line-and-design pass.

## Actual visual inspection summary

The final 8192×4855 PNG was opened at fit-to-page scale and examined in twelve ordered overlapping 2300×2300-pixel tiles. The visual audit explicitly covered Patient Mobile Device, Facility Client Device, Platform Administrator Client Device, the Centralized Server and each of its three artifacts, PostgreSQL Database Environment and its physical-placement note, the four external service nodes, all seven communication paths, and the full-page composition. Compared with the former 12400×7200 layout, the final 10800×6400 composition removes overextended horizontal route bands, shortens the longest path segments, places PostgreSQL directly beneath the server, and reserves separate ingress/egress corridors. The final vector SVG was also opened directly after PNG review.

The final result remains a light formal-university UML diagram, not a cloud architecture, DevOps board, network map, or system-design infographic. Node names dominate; stereotypes are small and secondary; contained execution environments and deployed artifacts are legible and distinct; small unresolved subtitles do not overwhelm their owners; and the white page with dark neutral strokes follows the lecturer example's academic restraint.

## Preserved open decisions

| Decision | DEP-01 treatment |
|---|---|
| Map Service technical caller | Explicitly unresolved; Map Service has no communication path. |
| PostgreSQL co-location or separation from the logical centralized server boundary | Explicitly unresolved; no physical server claim is made. |
| Backend and web technology | Unspecified; no framework, web server, or proxy is shown. |
| Provider, operating system, cloud, container, and host topology | Unresolved; none is inferred or rendered. |

Semantic status: verified

Structural QA: passed

Geometry QA: passed

Lecturer-style visual review: passed

Visual status: awaiting-user-approval
