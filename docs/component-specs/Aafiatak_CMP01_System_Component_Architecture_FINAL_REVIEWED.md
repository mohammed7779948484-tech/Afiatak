# Component Diagram — Aafiatak System Component Architecture
## Aafiatak Medical Appointment Booking System — MVP Component Diagram Specification

**Diagram ID:** `CMP-01`  
**Deliverable:** UML Component Diagram  
**Title:** `Component Diagram — Aafiatak Medical Appointment Booking System`  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Diagram count:** Exactly one system-level Component Diagram  
**Semantic status:** FINAL REVIEWED EXECUTION SPECIFICATION — ready for diagram-engine implementation

---

## 1. Purpose and Diagram Boundary

This Component Diagram answers:

> What are the approved software components of Aafiatak, what interfaces do they provide or require, and how are those components connected at the current MVP architecture level?

This is a **structural implementation-view UML diagram**. It is not a behavioral workflow and it must not show chronological execution.

It is **not**:

- a Use Case Diagram;
- a Use Case Model;
- an Activity Diagram;
- a Sequence Diagram;
- a Collaboration / Communication Diagram;
- a State Machine Diagram;
- a Class Diagram;
- an ERD/database schema;
- a Deployment Diagram;
- a cloud-infrastructure diagram;
- a UI/dashboard mockup;
- a microservices diagram.

The final submission requires **one** Component Diagram for the current Aafiatak MVP. Do not create one Component Diagram per actor, per Use Case, per Sequence scenario, or per application role.

---

## 2. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative current MVP product and architecture truth.
2. Lecturer UML PDF at the repository root, especially page 10 `8. Component Diagram.` — academic UML notation and presentation reference.
3. Lecturer-course rules supplied for this project — Component Diagram purpose/elements/relationships.
4. Current approved Aafiatak Use Case, Sequence, Collaboration, Class, State, and Activity artifacts — consistency evidence only; they must not override the MVP.
5. This file — exact reviewed execution contract for `CMP-01` after applying the rules above.
6. Rendering/layout tooling — presentation mechanics only.

If a lower-priority source conflicts with a higher-priority source, the higher-priority source wins.

Do not resolve an intentionally open implementation decision merely to make the diagram look more complete.

All visible labels must be **English**.

---

## 3. Lecturer Component-Diagram Rules Applied

The lecturer's UML material lists **Component Diagram** as a required UML diagram and presents it on page 10. The project course profile records the lecturer's illustrated Component-Diagram elements as:

- Components;
- Interfaces;
- Connectors.

The practical course rules supplied for this project additionally identify:

- Dependency;
- Interface;
- Provided Interface;
- Required Interface.

### Mandatory notation contract

- **Component:** standard UML Component shape/rectangle with the component glyph or an equivalent standard UML component notation consistent with the lecturer example.
- **Provided Interface:** UML lollipop notation (small circle) attached to the provider Component.
- **Required Interface:** UML socket notation attached to the requiring Component.
- **Assembly Connector:** connects one Required Interface to the matching Provided Interface.
- **Dependency:** dashed directed dependency arrow only when a real component-level dependency is needed and an interface connector is not the clearer notation.
- **Realization:** semantic ownership of a Provided Interface by its provider Component. When lollipop notation is used, the visible diagram may use the attached lollipop shorthand instead of drawing a redundant explicit realization arrow.

### Do not mix diagram types

Do **not** place any of the following inside this Component Diagram:

- Actors/stick figures;
- Use Case ellipses;
- `<<include>>` / `<<extend>>`;
- lifelines;
- activation bars;
- numbered Sequence/Collaboration messages;
- Activity Initial/Final nodes;
- Decision/Merge/Fork/Join nodes;
- State-machine states/transitions;
- Class attributes or operations;
- Association/Aggregation/Composition multiplicities;
- Deployment nodes/devices/servers as physical nodes;
- cloud/provider infrastructure icons.

---

## 4. Architecture-Neutrality Rules

The current MVP explicitly leaves the **final backend technology** and **web-dashboard technology** open.

Therefore the diagram must not invent or display:

- Django;
- .NET / ASP.NET;
- Spring Boot;
- Node.js;
- NestJS;
- Next.js;
- React;
- Angular;
- Laravel;
- an API Gateway product;
- Redis;
- Kafka;
- RabbitMQ;
- a message bus;
- a cache layer;
- service mesh;
- container/orchestration technology;
- AWS/Azure/GCP architecture.

The following technology labels are source-supported and may be shown where useful:

- `Flutter` for the Patient Application;
- `PostgreSQL` for the database.

Do not turn server responsibilities into separate components or microservices.

---

## 5. Exact Component Inventory

Render exactly the following **9 Components**.

| ID | Exact visible name | Classification | Source-backed responsibility / rationale |
|---|---|---|---|
| `C01` | `Patient Application` | Internal client application | Flutter Android/iOS patient-facing application; connects to the centralized Aafiatak server and supports discovery, booking, payment presentation, appointments, notifications, and visit/queue visibility. |
| `C02` | `Facility Web Dashboard` | Internal web application | One responsive role-dependent dashboard used by Facility Administrator, Booking & Reception Staff, and Doctor. Do not split it into separate role applications. |
| `C03` | `Aafiatak Platform Administration Dashboard` | Internal web application | Protected platform-administration dashboard for Platform Administrator users. |
| `C04` | `Aafiatak Backend` | Internal centralized server component | Central server-side orchestration for authentication, roles, facility data, availability, holds, appointments, payments/refunds, visit/queue, operational exceptions, notifications, permissions, and audit responsibilities. |
| `C05` | `PostgreSQL Database` | Internal persistence component | Approved MVP database technology. Do not expose tables/columns in this diagram. |
| `C06` | `WhatsApp Authentication Provider` | External service component | Official WhatsApp provider/API used only for phone verification and passwordless OTP authentication. |
| `C07` | `Payment Gateway` | External service component | External full-electronic-payment verification and refund integration for `FULL_PAYMENT_REQUIRED` flows. |
| `C08` | `Notification Service` | External service component | Approved general system-notification delivery service. WhatsApp is not the general notification channel. |
| `C09` | `Map Service` | External service component | Approved map/location service used by the system for facility-location capability. |

### Component-count invariant

`Component count = 9`

Do not add or remove a Component without new authoritative source evidence.

---

## 6. Explicitly Forbidden Components

Do **not** create any of the following as separate Components in `CMP-01`:

- `Doctor Application`;
- `Reception Application`;
- `Facility Administrator Application`;
- `Authentication Service`;
- `User Service`;
- `Booking Service`;
- `Availability Service`;
- `Reservation Service`;
- `ReservationHold Service`;
- `Payment Service`;
- `Refund Service`;
- `Queue Service`;
- `Visit Service`;
- `Operational Exception Service`;
- `Audit Service`;
- `Notification Microservice`;
- `API Gateway`;
- `SMS Provider`;
- `Facility HIS` / `Hospital Information System`;
- `EHR`;
- facility internal scheduling system;
- cashier/accounting system;
- pharmacy/laboratory/radiology systems.

The MVP describes responsibilities of a **centralized server**. Responsibilities are not automatically Components.

---

## 7. Role-to-Application Clarification

The following three facility roles all use the **same** `Facility Web Dashboard`:

- Facility Administrator;
- Booking & Reception Staff;
- Doctor.

Role-dependent functionality does not authorize separate software Components.

Existing Sequence/Collaboration diagrams may use labels such as `Doctor Interface` to clarify a scenario boundary. Those interaction-participant labels must **not** be promoted into standalone architecture Components unless the MVP explicitly defines a separate application.

---

## 8. Exact Provided Interface Inventory

Render exactly the following **6 Provided Interfaces**.

| ID | Provider Component | Exact visible interface label | Meaning |
|---|---|---|---|
| `PI01` | `Aafiatak Backend` | `Aafiatak Application Interface` | Implementation-neutral application/server contract used by Aafiatak client/dashboard components. Do not expose a framework or protocol choice. |
| `PI02` | `PostgreSQL Database` | `Persistence Interface` | Persistence capability consumed by the Aafiatak Backend. |
| `PI03` | `WhatsApp Authentication Provider` | `WhatsApp Authentication Interface` | Official authentication/phone-verification integration capability. |
| `PI04` | `Payment Gateway` | `Payment Interface` | Full-payment verification/payment/refund integration capability. |
| `PI05` | `Notification Service` | `Notification Interface` | General system-notification delivery capability. |
| `PI06` | `Map Service` | `Map / Location Interface` | Facility map/location capability. |

### Provided-interface count invariant

`Provided Interface count = 6`

---

## 9. Exact Required Interface Inventory

Render exactly the following **7 Required Interfaces**.

| ID | Owner / requiring Component | Exact visible interface label | Matching Provided Interface |
|---|---|---|---|
| `RI01` | `Patient Application` | `Aafiatak Application Interface` | `PI01` |
| `RI02` | `Facility Web Dashboard` | `Aafiatak Application Interface` | `PI01` |
| `RI03` | `Aafiatak Platform Administration Dashboard` | `Aafiatak Application Interface` | `PI01` |
| `RI04` | `Aafiatak Backend` | `Persistence Interface` | `PI02` |
| `RI05` | `Aafiatak Backend` | `WhatsApp Authentication Interface` | `PI03` |
| `RI06` | `Aafiatak Backend` | `Payment Interface` | `PI04` |
| `RI07` | `Aafiatak Backend` | `Notification Interface` | `PI05` |

### Required-interface count invariant

`Required Interface count = 7`

### Required-interface ownership

Every Required Interface must have one explicit owning Component in the semantic model. If the repository's current relation vocabulary does not contain a dedicated UML ownership relation for required interfaces, record ownership in validated metadata such as `ownerComponent`; do not invent a fake UML relationship merely to encode ownership.

---

## 10. Exact Interface Connectors

Render exactly the following **7 Assembly Connectors**.

| Connector ID | Required Interface | Provided Interface | Architectural meaning |
|---|---|---|---|
| `K01` | `RI01` Patient Application | `PI01` Aafiatak Backend | Patient Application consumes the centralized Aafiatak application/server contract. |
| `K02` | `RI02` Facility Web Dashboard | `PI01` Aafiatak Backend | Facility Dashboard consumes the centralized Aafiatak application/server contract. |
| `K03` | `RI03` Platform Administration Dashboard | `PI01` Aafiatak Backend | Platform Administration Dashboard consumes the centralized Aafiatak application/server contract. |
| `K04` | `RI04` Aafiatak Backend | `PI02` PostgreSQL Database | Backend consumes persistence capability. |
| `K05` | `RI05` Aafiatak Backend | `PI03` WhatsApp Authentication Provider | Backend consumes the official WhatsApp authentication capability. |
| `K06` | `RI06` Aafiatak Backend | `PI04` Payment Gateway | Backend consumes payment/refund capability. |
| `K07` | `RI07` Aafiatak Backend | `PI05` Notification Service | Backend consumes general notification delivery capability. |

### Connector-count invariant

`Assembly Connector count = 7`

A connector must join **one Required Interface to one Provided Interface**. Do not connect two provided interfaces or two required interfaces.

---

## 11. Map Service — Deliberately Unresolved Technical Consumer

`Map Service` is unquestionably in scope as an approved external service, and the system includes `View Facility Location` behavior.

However, the approved MVP does **not** fix whether the technical integration call is made:

- directly by the Patient Application; or
- through the Aafiatak Backend.

Therefore `CMP-01` must **not invent the technical caller**.

Binding rule:

- Render `C09 Map Service` with its source-supported Provided Interface `PI06 Map / Location Interface`.
- Do **not** create a Required Interface or Assembly Connector to `PI06` in this version.
- Do **not** draw a dependency from Patient Application to Map Service.
- Do **not** draw a dependency from Aafiatak Backend to Map Service.
- Keep this as a documented architecture-open point rather than presenting speculation as approved design.

An intentionally unconnected provided interface is acceptable here because it preserves a known external Component while keeping the technical consumer unresolved.

---

## 12. Exact Realization Semantics

The semantic model must contain the following **6 Provided-Interface realization relationships**:

| Relation ID | Source Component | Target Provided Interface |
|---|---|---|
| `RZ01` | `C04 Aafiatak Backend` | `PI01 Aafiatak Application Interface` |
| `RZ02` | `C05 PostgreSQL Database` | `PI02 Persistence Interface` |
| `RZ03` | `C06 WhatsApp Authentication Provider` | `PI03 WhatsApp Authentication Interface` |
| `RZ04` | `C07 Payment Gateway` | `PI04 Payment Interface` |
| `RZ05` | `C08 Notification Service` | `PI05 Notification Interface` |
| `RZ06` | `C09 Map Service` | `PI06 Map / Location Interface` |

The visible lollipop attachment may serve as the UML shorthand for these realizations. Do not duplicate each attachment with an unnecessary dashed realization arrow if that would conflict with the lecturer-style notation or reduce readability.

---

## 13. Component Dependencies

No additional component-to-component `dependency` relationship is required in this reviewed specification because the approved technical relationships represented here are expressed more precisely through Required/Provided Interfaces and Assembly Connectors.

Therefore:

`Component Dependency count = 0`

Do not add dashed dependency arrows merely because the course mentions the relationship type.

Use an explicit dependency later only if authoritative architecture evidence requires a dependency that is not already represented by an interface connector.

---

## 14. Authentication Boundary

The following rules are binding:

- Authentication is passwordless.
- OTP is delivered through the official WhatsApp authentication provider/API.
- SMS is not used.
- No `Password Service` Component exists.
- No `Forgot Password` Component or interface exists.
- WhatsApp is in scope only for authentication/phone verification.
- General reminders/alerts/operational notifications belong to `Notification Service`, not `WhatsApp Authentication Provider`.

Do not connect `Notification Service` through the WhatsApp provider in `CMP-01`.

---

## 15. Payment Boundary

The Component Diagram must preserve these architecture-level truths:

- `Payment Gateway` is external.
- It is used only when electronic payment/refund behavior is required.
- `PAY_AT_FACILITY` does not create an electronic PaymentIntent.
- The Component Diagram must not add deposit/partial-payment Components.
- Browser/client return is not the trusted payment truth; trusted verification is a backend responsibility.

Do not model payment as a direct Patient Application → Payment Gateway component connector in this structural diagram unless future approved architecture explicitly fixes such a technical contract. The approved architecture-level integration represented here is Backend ↔ Payment Gateway.

---

## 16. Notification Boundary

- `Notification Service` is the general approved system-notification external service.
- Notification delivery is separate from WhatsApp authentication.
- Do not add WhatsApp reminder/alert/support messaging.
- Do not create separate notification Components per event type.

---

## 17. Persistence Boundary

`PostgreSQL Database` is one persistence Component for the current MVP Component Diagram.

Do not display:

- tables;
- columns;
- foreign keys;
- Class Diagram entities;
- ERD relationships;
- SQL queries;
- repository classes;
- ORM technology.

The only structural relationship required here is that `Aafiatak Backend` consumes the database `Persistence Interface`.

---

## 18. Cross-Diagram Consistency Contract

Use existing diagrams only to verify that `CMP-01` does not contradict approved behavior.

### Sequence / Collaboration evidence to cross-check

- Patient Application communicates with Aafiatak Backend.
- Aafiatak Backend communicates with the internal data store/persistence boundary.
- Aafiatak Backend communicates with WhatsApp Authentication Provider in authentication flows.
- Aafiatak Backend communicates with Payment Gateway in full-payment/refund flows.
- Aafiatak Backend communicates with Notification Service for system notifications.
- Facility operational interactions use the facility dashboard/boundary and centralized backend.
- Doctor interaction does not prove a separate Doctor Application.

### Use Case evidence to cross-check

- Map Service participates in facility-location capability.
- Payment Gateway, Notification Service, WhatsApp Authentication Provider, and Map Service are approved external systems.

### Class / State / Activity evidence

Use them only to ensure the component architecture can support the approved domain and lifecycles. Do not convert Classes, States, or Activities into Components.

---

## 19. Exact Visual Composition Contract

The final render must follow the lecturer's simple academic Component-Diagram visual language rather than a modern cloud architecture infographic.

### Recommended topology

Use a balanced landscape composition with these logical placements:

**Left / upper-left client side**

1. `Patient Application`
2. `Facility Web Dashboard`
3. `Aafiatak Platform Administration Dashboard`

**Center**

4. `Aafiatak Backend`

**Lower center**

5. `PostgreSQL Database`

**Right / outer service side**

6. `WhatsApp Authentication Provider`
7. `Payment Gateway`
8. `Notification Service`
9. `Map Service`

This placement is presentation guidance only. Coordinates are not semantic truth.

### Visual rules

- White or very light neutral background.
- Dark charcoal/black UML strokes and text.
- No gradients.
- No drop shadows.
- No decorative icons or logos.
- No colored cards.
- No AWS/Azure/GCP/cloud symbols.
- No phone/browser illustrations.
- Standard UML Component symbols.
- Provided lollipops and Required sockets must be immediately recognizable.
- Interface labels stay close to the correct interface glyph.
- Assembly connectors must be short and easy to trace.
- Avoid crossing through unrelated component rectangles.
- Avoid connector/label collisions.
- Keep external services visually peripheral without adding decorative region boxes unless genuinely needed for readability.
- Keep the main title readable at normal university-report zoom.
- The Backend should be the visual center because it is the centralized orchestration component.
- `Map Service` may remain intentionally without an assembly connector; do not distort the architecture merely to make every component visually connected.

---

## 20. Rendering Contract

The renderer may:

- wrap long component/interface labels;
- adjust component widths/heights;
- adjust connector routing;
- alter whitespace;
- choose exact lollipop/socket attachment points;
- use a deterministic graph-assisted or curated composition.

The renderer may **not**:

- rename a Component;
- rename an Interface;
- merge Components;
- split Components;
- invent Components;
- infer connections from proximity;
- change connector endpoints;
- add a Map Service consumer;
- substitute dependency arrows for the required assembly connectors without a semantic reason.

---

## 21. Semantic Record Contract for the Repository

The canonical semantic YAML for `CMP-01` must contain:

- 9 `component` elements;
- 6 `provided_interface` elements;
- 7 `required_interface` elements;
- 6 `realization` relations;
- 7 `connector` relations;
- 0 component `dependency` relations.

Every semantic element and every semantic relation must contain source references consistent with repository governance.

Required Interface ownership must be explicit and machine-checkable.

The ViewSpec must select exactly the semantic IDs defined by this file.

---

## 22. Engine Integration Expectations

This specification defines diagram truth. The implementation agent must extend the existing diagram engine without changing this semantic contract.

Known repository integration work may include:

- allowing `component` in `engine/schemas/view.schema.json`;
- allowing `component` in pipeline view validation/dispatch;
- creating a dedicated component SVG renderer;
- creating a component composition/layout module;
- creating component-specific SVG QA;
- updating `registry/diagram-types.yaml` so it truthfully lists supported diagram families;
- fixing generic `build()` dispatch if it remains hard-coded to the Main Use Case renderer;
- optional draw.io export if the current delivery workflow requires it.

Implementation code is allowed to change. The component inventory/interfaces/connectors defined above are not.

---

## 23. Nine-Pass Review Record

The final implementation must perform and report these review passes:

### Pass 1 — Authority and source integrity
Verify the root MVP is product truth and the lecturer PDF is the notation/presentation source.

### Pass 2 — Component inventory
Verify exactly 9 Components and no unsupported microservice/application split.

### Pass 3 — Interface inventory and ownership
Verify 6 Provided Interfaces and 7 Required Interfaces, with correct provider/owner.

### Pass 4 — Connector and direction semantics
Verify exactly 7 Required↔Provided Assembly Connectors with correct endpoints.

### Pass 5 — Cross-diagram consistency
Compare with current Use Case, Sequence, Collaboration, Class, State, and Activity artifacts without letting them override the MVP.

### Pass 6 — Open-decision / no-invention audit
Verify backend/web technology remains open and Map Service caller remains unresolved.

### Pass 7 — Lecturer UML notation audit
Verify Component / Provided Interface / Required Interface / Connector notation matches the lecturer-style Component Diagram and does not leak other UML diagram syntax.

### Pass 8 — Geometry/readability audit
Verify no component overlap, clipped text, interface collision, connector-through-box errors, label collisions, or illegible scaling.

### Pass 9 — Final actual-render inspection
Open the actual SVG and PNG, compare item-by-item against this MD and the lecturer page-10 example, then correct any remaining visual issue before delivery.

---

## 24. Mandatory QA Gates

Before delivery, verify all of the following:

1. Exact title is correct.
2. Diagram ID is `CMP-01`.
3. Exactly 9 Components exist.
4. Exactly 6 Provided Interfaces exist.
5. Exactly 7 Required Interfaces exist.
6. Exactly 7 Assembly Connectors exist.
7. Exactly 6 Provided-Interface realization semantic relations exist.
8. No extra component-level dependency is invented.
9. Every selected relation endpoint is visible.
10. Every Required Interface is owned by the intended requiring Component.
11. Every Provided Interface belongs to the intended provider Component.
12. Every Assembly Connector joins one Required Interface to one Provided Interface.
13. `Facility Web Dashboard` remains one Component for all three facility roles.
14. No `Doctor Application` exists.
15. No microservice decomposition exists.
16. No SMS/password component exists.
17. WhatsApp is authentication-only.
18. General notifications use Notification Service.
19. PostgreSQL is represented as persistence only, not as an ERD.
20. Map Service exists but no technical consumer is invented.
21. Backend and web-dashboard technology remain unspecified.
22. No Actor/Lifeline/Message/Decision/State/Class notation leaks into the diagram.
23. No connector crosses an unrelated Component body unless unavoidable and explicitly corrected through routing.
24. No visible label collides with another label or interface glyph.
25. No element is clipped by the artboard.
26. The SVG parses successfully.
27. The generated PNG is opened and inspected visually.
28. The generated SVG is opened and inspected visually.
29. The implementation passes repository semantic/schema/UML validation.
30. Final visual status remains `awaiting-user-approval` until explicitly approved by the project owner.

---

## 25. Final Acceptance Counts

The implementation is semantically complete only if the final counts are:

| Item | Required count |
|---|---:|
| Components | **9** |
| Provided Interfaces | **6** |
| Required Interfaces | **7** |
| Assembly Connectors | **7** |
| Provided-Interface Realizations | **6** |
| Component Dependencies | **0** |
| Component Diagrams | **1** |

Any count mismatch is a blocking defect unless authoritative project scope is changed first.

---

## 26. Final Traceability Summary

Primary product evidence:

- Project Specification §8.1 — Patient Application.
- Project Specification §8.2 — Facility Web Dashboard.
- Project Specification §8.3 — Platform Administration Dashboard.
- Project Specification §8.4 — authentication/identity and WhatsApp OTP boundary.
- Project Specification §31.1 — Patient Application technical architecture.
- Project Specification §31.2 — Facility Dashboard technical architecture.
- Project Specification §31.3 — Platform Administration Dashboard technical architecture.
- Project Specification §31.4 — centralized server responsibilities.
- Project Specification §31.5 — PostgreSQL database.
- Project Specification §31.6 — external services.
- Main Use Case — `View Facility Location` / Map Service participation.
- Approved Sequence/Collaboration suite — interaction-boundary consistency evidence.

Lecturer/course evidence:

- Lecturer UML PDF page 10 — `8. Component Diagram.` visual/notation reference.
- Course rules — Components, Interfaces, Connectors, Dependency, Provided Interface, Required Interface.

---

## 27. Final Status Rule

This MD is the **authoritative execution specification for CMP-01** after the above review.

The implementation agent must treat it as the diagram contract.

If the repository implementation cannot currently render part of this contract, fix the diagram engine rather than silently changing the diagram semantics.

Final implementation status must be reported as:

- **Semantic status:** verified / not verified
- **Structural QA:** passed / failed
- **Geometry QA:** passed / failed
- **Visual status:** awaiting-user-approval
