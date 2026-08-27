# Deployment Diagram — Aafiatak MVP Runtime Topology
## Aafiatak Medical Appointment Booking System — Deployment Diagram Specification

**Diagram ID:** `DEP-01`
**Deliverable:** UML Deployment Diagram
**Title:** `Deployment Diagram — Aafiatak Medical Appointment Booking System`
**Visible language:** English only
**Scope:** Current approved MVP only
**Diagram count:** Exactly one system-level Deployment Diagram
**Mode:** Conceptual/logical deployment topology constrained by the approved MVP
**Semantic status:** FINAL REVIEWED EXECUTION SPECIFICATION

---

## 1. Purpose

This diagram answers:

> On which logical runtime/device nodes do the approved Aafiatak software components execute or become available, and which deployment nodes communicate with one another?

It is a structural Deployment Diagram. It is not a Use Case, Activity, Sequence, Collaboration, State, Class, Component, ERD, cloud-provider architecture, DevOps pipeline, or production runbook.

Exactly **one** Deployment Diagram is required for the current MVP.

---

## 2. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — product and technical-boundary truth.
2. Lecturer UML PDF, especially page 11 `10. Deployment Diagram.` — academic notation and visual reference.
3. Lecturer-course rules supplied for this project.
4. Reviewed CMP-01 Component Diagram specification and canonical Component model — component-boundary consistency.
5. Existing Use Case / Sequence / Collaboration / Class / State / Activity work — cross-check only.
6. This file — execution contract for `DEP-01`.
7. Renderer/layout tooling — presentation only.

Do not resolve an intentionally open technical decision just to make the diagram look more complete.

All visible labels must be English.

---

## 3. Lecturer Deployment Rules Applied

The lecturer PDF lists Deployment Diagram as a required UML diagram and presents it on page 11.

The parsed PDF exposes the heading but does not reliably expose the internal labels of the example. Therefore the implementation agent must **visually inspect the actual page-11 image** and match its academic Deployment-node style rather than inventing example labels from OCR.

The lecturer/course rules define Deployment Diagram as showing **where the system runs**. Typical element categories include:

- Client
- Web Server
- Application Server
- Database Server
- Cloud

and the relationship:

- **Communication Path**

Those are categories/examples, not mandatory Aafiatak nodes. Do not invent a Web Server or Cloud node if the MVP does not specify one.

Repository course rules identify:

- Nodes
- deployed artifacts/components
- Communication Paths

### Mandatory notation

- Standard UML Deployment Node / Device / Execution Environment notation.
- Contained deployed component/artifact when source-supported.
- Communication Path = solid line between Nodes.
- Communication Path has **no chronological meaning and no message numbering**.
- **Do not add arrowheads** merely to show request direction.

---

## 4. Do Not Mix Diagram Types

Do not place:

- Actors/stick figures
- Use Case ellipses
- `<<include>>` / `<<extend>>`
- lifelines / activation bars
- numbered Sequence or Collaboration messages
- Activity Initial/Final/Decision/Fork/Join
- State-machine states
- Class attributes/operations/multiplicities
- Component lollipop/socket interfaces
- database tables/columns
- CI/CD stages

inside DEP-01.

---

## 5. Source-Supported Deployment Facts

The MVP fixes these facts:

### Patient Application
- Flutter
- Android and iOS
- connects to a centralized server

### Facility Dashboard
- responsive web dashboard
- works on desktop or tablet
- role-dependent
- used by Facility Administrator, Booking & Reception Staff, and Doctor

### Platform Administration Dashboard
- protected web dashboard
- used by Aafiatak platform staff

### Centralized server
Responsible for authentication, roles, facilities, availability, ReservationHold, appointments, payments/refunds, VisitInstance/QueueEntry, operational exceptions, notifications, permissions, and audit history.

### Database
- PostgreSQL

### External services
- Notification Service
- Map Service
- one Payment Gateway when approved
- official WhatsApp Authentication Provider/API

### Still open
- final backend technology
- final web-dashboard technology
- OS / hosting provider / cloud / VPS / container topology
- physical server count
- physical PostgreSQL placement

---

## 6. Deployment Modeling Decisions

DEP-01 is intentionally a **logical deployment topology**, not a production-provider commitment.

### 6.1 Logical server-side node

Use one node:

`Aafiatak Centralized Server`

It contains the approved server-side software grouping:

- `Facility Web Dashboard`
- `Aafiatak Platform Administration Dashboard`
- `Aafiatak Backend`

This is a logical UML deployment grouping. It does **not** claim that final production must use one VM or one physical host.

Do not infer OS, framework, reverse proxy, web-server product, container runtime, or cloud provider.

### 6.2 PostgreSQL boundary

Use one logical node:

`PostgreSQL Database Environment`

containing:

`PostgreSQL Database`

This makes persistence explicit while leaving physical co-location vs separation from the centralized server unresolved.

### 6.3 Web client devices

Facility and Platform dashboards are web applications. Client Devices show a `Web Browser` access environment. The complete server-side web application is not claimed to be physically stored on the client.

---

## 7. Exact Deployment Node Inventory

Render exactly these **9 top-level Nodes**.

| ID | Exact visible name | Role | Contained runtime/component | Status |
|---|---|---|---|---|
| `N01` | `Patient Mobile Device` | Device | `Android / iOS`; `Patient Application` | Direct source fact |
| `N02` | `Facility Client Device` | Device | `Web Browser`; `Desktop / Tablet` | Direct source fact |
| `N03` | `Platform Administrator Client Device` | Device | `Web Browser` | Minimal modeling representation; exact hardware type unspecified |
| `N04` | `Aafiatak Centralized Server` | Logical server Node | `Facility Web Dashboard`; `Aafiatak Platform Administration Dashboard`; `Aafiatak Backend` | Centralized-server fact + logical grouping |
| `N05` | `PostgreSQL Database Environment` | Logical execution environment | `PostgreSQL Database` | PostgreSQL fact; physical placement unresolved |
| `N06` | `WhatsApp Authentication Provider` | External service Node | maps to CMP-01 external component | Source-supported |
| `N07` | `Payment Gateway` | External service Node | maps to CMP-01 external component | Source-supported |
| `N08` | `Notification Service` | External service Node | maps to CMP-01 external component | Source-supported |
| `N09` | `Map Service` | External service Node | technical caller unresolved | Source-supported |

**Node count = 9**

Do not add or remove a top-level Node without new authoritative evidence.

---

## 8. Component-to-Node Mapping

| CMP-01 Component | DEP-01 Node |
|---|---|
| Patient Application | N01 |
| Facility Web Dashboard | N04 |
| Aafiatak Platform Administration Dashboard | N04 |
| Aafiatak Backend | N04 |
| PostgreSQL Database | N05 |
| WhatsApp Authentication Provider | N06 |
| Payment Gateway | N07 |
| Notification Service | N08 |
| Map Service | N09 |

N02 and N03 are client access Devices containing Web Browser runtime, not duplicate deployments of the dashboard components.

---

## 9. Exact Communication Paths

Render exactly **7** solid UML Communication Paths and **no arrowheads**.

| ID | Node A | Node B | Evidence |
|---|---|---|---|
| `CP01` | Patient Mobile Device | Aafiatak Centralized Server | Patient Application explicitly connects to centralized server |
| `CP02` | Facility Client Device | Aafiatak Centralized Server | Facility web access + approved Dashboard↔Backend architecture |
| `CP03` | Platform Administrator Client Device | Aafiatak Centralized Server | Platform web access + approved Dashboard↔Backend architecture |
| `CP04` | Aafiatak Centralized Server | PostgreSQL Database Environment | persistence boundary |
| `CP05` | Aafiatak Centralized Server | WhatsApp Authentication Provider | OTP authentication integration |
| `CP06` | Aafiatak Centralized Server | Payment Gateway | trusted payment/refund integration |
| `CP07` | Aafiatak Centralized Server | Notification Service | general notification integration |

**Communication Path count = 7**

Do not add direction arrows, message numbers, ports, or protocols.

---

## 10. Map Service — Intentionally Unresolved Path

Map Service is approved and must appear.

But the current MVP does not fix whether the technical caller is:

- the Patient Application/client;
- the centralized backend;
- another web/client integration mechanism.

Therefore:

- render `N09 Map Service`;
- do not draw N01↔N09;
- do not draw N04↔N09;
- do not invent another caller;
- allow N09 to remain intentionally unconnected;
- optionally show a small subtitle `Technical caller unresolved` if it remains lecturer-like.

This must not be treated as a QA error.

---

## 11. Explicitly Forbidden Deployment Nodes

Do not add:

- Cloud
- AWS / Azure / GCP
- Vercel / Railway
- VPS
- Docker Host / container
- Kubernetes Cluster
- Load Balancer
- CDN
- Reverse Proxy
- Nginx / Caddy / Apache
- API Gateway
- Redis
- Cache Server
- Queue Worker
- Message Broker / Kafka / RabbitMQ
- Object Storage / File Server
- Backup / Monitoring / Log Server
- SMS Gateway
- Facility HIS / EHR
- Facility Internal Scheduling Server
- Cashier / Accounting Server
- Pharmacy / Lab / Radiology Server

unless the authoritative Aafiatak architecture is formally changed.

---

## 12. No Facility-System Integration

The MVP explicitly does not require technical integration with the facility's existing system.

Therefore:

- no Facility HIS node;
- no facility internal scheduling node;
- no facility database/API node;
- no Communication Path to such a system.

Aafiatak works beside the facility's system through bounded digital capacity, not through deployment-level synchronization.

---

## 13. Authentication Boundary

- WhatsApp Authentication Provider is external.
- Authentication is passwordless.
- OTP uses the official WhatsApp provider/API.
- SMS is not used.
- General notifications do not use the WhatsApp authentication provider.
- CP05 is the approved server-side authentication integration path.

Do not expose OTP values/tokens/secrets in the diagram.

---

## 14. Payment Boundary

- Payment Gateway is external.
- Backend uses trusted verification for electronic payment truth.
- PAY_AT_FACILITY does not require electronic PaymentIntent.
- No cashier/accounting node.
- CP06 is the stable server-to-gateway deployment path.

Do not add Patient Mobile Device↔Payment Gateway as a deployment path merely because a user-facing gateway interaction exists in Sequence/Collaboration; the current deployment contract does not fix that network topology.

---

## 15. Notification Boundary

- Notification Service is external and separate from WhatsApp authentication.
- CP07 connects the server environment to Notification Service.
- Do not add one Node per notification type.
- Do not add Notification Service↔Patient Mobile Device unless future architecture explicitly fixes that transport.

---

## 16. Technology-Neutrality Rules

May show:

- Flutter
- Android / iOS
- Web Browser
- PostgreSQL

Do not show or imply:

- backend framework
- web-dashboard framework
- OS
- reverse proxy/web server
- container runtime
- hosting provider
- exact protocol/port
- managed vs self-hosted PostgreSQL
- physical server count

---

## 17. Repository Semantic Contract

Use current repository deployment semantics:

- element type: `deployment_node`
- relation type: `communication_path`

The current UML validator expects Deployment Views to select **Deployment Nodes only**; deployed artifacts/components belong in contained node metadata.

Canonical DEP-01 data must contain:

- exactly 9 selected `deployment_node` elements;
- exactly 7 `communication_path` relations;
- contained runtime/component metadata;
- no selected artifact element unless repository architecture is deliberately revised.

Recommended IDs:

- `node.dep01.patient-mobile-device`
- `node.dep01.facility-client-device`
- `node.dep01.platform-admin-client-device`
- `node.dep01.aafiatak-centralized-server`
- `node.dep01.postgresql-environment`
- `node.dep01.whatsapp-auth-provider`
- `node.dep01.payment-gateway`
- `node.dep01.notification-service`
- `node.dep01.map-service`

Every Node and Communication Path must have valid sourceRefs.

Metadata should clearly distinguish open/modeling-inference facts, e.g.:

- `modelingInference`
- `physicalPlacement: unresolved`
- `technicalCaller: unresolved`

Coordinates/colors are never semantics.

---

## 18. Reviewed-Spec Source Registration

Copy this MD into repository `docs/` and register it in `registry/sources.yaml` before semantic records reference it.

Recommended source identity:

`dep01-mvp-deployment-reviewed-spec`

Do not create dangling sourceRefs to an unregistered execution-spec source.

---

## 19. Cross-Diagram Consistency

### CMP-01
All 9 approved components must map consistently to Nodes. Do not invent a Deployment Node that implies a new Component.

### Sequence / Collaboration
Use only to verify stable boundaries:

- Patient Application ↔ Backend
- Facility Dashboard ↔ Backend
- Backend ↔ persistence
- Backend ↔ WhatsApp Authentication Provider
- Backend ↔ Payment Gateway
- Backend ↔ Notification Service

Do not promote Patient, Doctor, Booking & Reception Staff, or `Doctor Interface` into Deployment Nodes.

### Use Case
Verify approved external systems: Payment Gateway, Notification Service, Map Service, WhatsApp Authentication Provider.

### Class / State / Activity
Contradiction checks only; they do not define deployment nodes.

---

## 20. Exact Visual Composition Contract

The final output must visually follow the lecturer page-11 Deployment Diagram.

The agent must inspect the actual page.

### Recommended landscape topology

**Left — clients**
- Patient Mobile Device
- Facility Client Device
- Platform Administrator Client Device

**Center**
- Aafiatak Centralized Server

**Lower center**
- PostgreSQL Database Environment

**Right — external services**
- WhatsApp Authentication Provider
- Payment Gateway
- Notification Service
- Map Service

### Visual rules

- white/light neutral background
- dark monochrome academic UML
- standard 3D-style Deployment Nodes if consistent with lecturer example
- contained runtime/component labels clearly inset
- solid Communication Paths
- **no arrowheads**
- no decorative icons/logos/cloud graphics
- no gradients/shadows/cards
- no DevOps infographic look
- compact readable title
- minimal line crossings
- no path through unrelated Node
- Map Service may remain intentionally unconnected

---

## 21. Rendering Contract

Renderer may:

- resize nodes
- wrap labels
- route paths orthogonally
- resize artboard
- use deterministic curated coordinates

Renderer may not:

- rename nodes
- change node/path counts
- add Cloud/Web Server/VPS/Proxy nodes
- add arrowheads
- connect Map Service to a guessed caller
- move approved components to different Nodes
- infer semantics from proximity

Deployment is already classified as a deterministic layout type in repository policy; use a curated deterministic composition rather than unnecessary auto-layout infrastructure.

---

## 22. Deployment QA Contract

### Semantic / structural
Validate:

- exact Node IDs/names/count;
- exact Communication Path IDs/endpoints/count;
- only `communication_path` relations;
- no duplicates;
- all endpoints visible;
- contained runtime/component metadata;
- no forbidden technology/node;
- Map Service has zero paths;
- sourceRefs resolve to registered sources.

### Geometry
Validate:

- Node↔Node overlap;
- contained item outside owner Node;
- path through unrelated Node;
- path↔label collision;
- title collision;
- clipping;
- unreadably small labels;
- paths rendered without arrowheads.

Automated QA is not visual approval.

---

## 23. Engine Integration Expectations

Known repository state before DEP-01:

- semantic schema already supports `deployment_node`, `artifact`, `communication_path`, `deployment`;
- UML validator already has Deployment rules;
- modeling policy already classifies Deployment as deterministic;
- `model/catalog/deployment-nodes/` is empty except `.gitkeep`;
- `views/deployment/` is empty except `.gitkeep`;
- current ViewSpec enum does not yet include `deployment`;
- current pipeline does not yet support `deployment`;
- no Deployment SVG renderer exists;
- no Deployment-specific SVG QA exists;
- Deployment is not registered in `registry/diagram-types.yaml`.

Expected implementation:

- add `deployment` to view schema;
- add pipeline validation/render/QA dispatch;
- create `engine/svg/deployment_diagram.py`;
- create deterministic DEP-01 composition;
- create `qa/deployment_svg_validation.py`;
- register Deployment diagram type;
- create canonical model/view;
- register this MD as source;
- use current generic build/manifest/artifact-registry path;
- do not regress Component or earlier diagram support.

---

## 24. Nine Review Passes

1. Authority/source integrity.
2. Exact 9-Node inventory.
3. Component-to-Node mapping.
4. Exact 7 Communication Paths / no arrowheads.
5. Cross-diagram consistency.
6. Open-decision/no-invention audit.
7. Lecturer page-11 notation audit.
8. Geometry/readability audit.
9. Actual SVG/PNG final visual inspection.

Do not claim a pass without checking it.

---

## 25. Mandatory QA Gates

Before delivery verify:

1. Exact title.
2. Diagram ID `DEP-01`.
3. Exactly 9 top-level Nodes.
4. Exactly 7 Communication Paths.
5. English labels only.
6. Patient Mobile Device shows Android/iOS + Patient Application.
7. Facility Client Device shows Desktop/Tablet + Web Browser.
8. Platform Administrator Client Device shows Web Browser without inventing hardware type.
9. Centralized Server contains Facility Web Dashboard, Platform Administration Dashboard, Backend.
10. PostgreSQL environment contains PostgreSQL Database.
11. Physical DB co-location/separation remains unresolved.
12. All four external service Nodes exist.
13. Map Service has no invented path.
14. No SMS node.
15. No Facility HIS/internal scheduling node.
16. No Cloud/VPS/Docker/Kubernetes/provider node.
17. No Web Server/reverse-proxy product invented.
18. Backend/web-dashboard framework choices remain unspecified.
19. No other UML notation leaks in.
20. All path endpoints are included deployment nodes.
21. Communication Paths are solid with no arrowheads.
22. No duplicate path.
23. No path crosses unrelated Node.
24. No contained item escapes its Node.
25. No clipped labels.
26. SVG parses.
27. Deployment structural QA passes.
28. Geometry QA passes.
29. Actual SVG opened and inspected.
30. Actual PNG opened and inspected.
31. Visual comparison with lecturer page 11 completed.
32. Existing Component/mature diagram families remain operational.
33. Visual status remains `awaiting-user-approval`.

---

## 26. Final Acceptance Counts

| Item | Required |
|---|---:|
| Deployment Diagrams | **1** |
| Top-level Deployment Nodes | **9** |
| Communication Paths | **7** |
| Internal software components mapped | **5** |
| External service Nodes | **4** |
| Map Service Communication Paths | **0** |
| Invented Cloud/Web Server/VPS/Container Nodes | **0** |

---

## 27. Traceability Summary

Primary product evidence:

- Project Specification §5 — no required facility-system technical integration.
- §8.1 — Patient Application.
- §8.2 — Facility Web Dashboard.
- §8.3 — Platform Administration Dashboard.
- §8.4 — WhatsApp OTP boundary.
- §30.3 — Android/iOS and responsive web platform expectations.
- §31.1 — Flutter + Android/iOS + centralized-server connection.
- §31.2 — Facility Dashboard desktop/tablet.
- §31.3 — protected Platform Administration dashboard.
- §31.4 — centralized server responsibilities.
- §31.5 — PostgreSQL.
- §31.6 — external services.
- CMP-01 reviewed/canonical model — approved component inventory and stable integration boundaries.
- approved Sequence/Collaboration suite — communication cross-check only.

Lecturer evidence:

- lecturer UML PDF page 11 — Deployment Diagram visual/notation reference.
- course rules — Nodes, deployed artifacts/components, Communication Paths.

---

## 28. Final Status Rule

This MD is the authoritative execution contract for DEP-01.

If the engine cannot render it, fix Deployment support rather than changing the semantics.

Final report must end with:

- **Semantic status:** verified / not verified
- **Structural QA:** passed / failed
- **Geometry QA:** passed / failed
- **Visual status:** awaiting-user-approval
