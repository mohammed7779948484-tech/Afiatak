# Sequence Diagram — Resolve Operational Exception
## Aafiatak Medical Appointment Booking System — MVP Sequence Diagram Specification

**Diagram ID:** `SD-06`  
**Deliverable:** UML Sequence Diagram  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** MUC-19; FAUC-36; BRUC-32..43; UCM-13 Manage Operational Exceptions; Project Specification §§23–24  
**Semantic status:** FINAL REVIEWED — ready for diagram execution

---


## 1. Authority and Conflict Rules

Use this precedence for this Sequence Diagram:

1. `Aafiatak_Project_Specification_EN.md` — authoritative current MVP product truth.
2. Lecturer UML PDF and the lecturer-course notes supplied for this project — academic Sequence Diagram method and notation.
3. Reviewed Aafiatak Use Case Modeling — scenario/precondition/postcondition traceability.
4. `Aafiatak_MVP_Class_Diagram_Spec_FINAL_VERIFIED_v2.md` — approved domain names and lifecycle separation; it does **not** define implementation architecture.
5. This file — exact execution contract for this Sequence Diagram.
6. Rendering/tooling — presentation mechanics only.

If anything in this file genuinely conflicts with the root project specification, the root project specification wins.

Do not invent product behavior, a clinical workflow, or an implementation architecture merely because it is common in similar systems.

The lecturer PDF classifies Sequence and Collaboration as **Interaction Diagrams**. The supplied lecturer notes further state that Sequence Diagram shows the chronological order of messages, uses Actor/Object/Lifeline/Activation/Message/Return, shows requests with solid arrows and responses with dashed arrows, and may model one operation or a coherent linked interaction. The lecturer does **not** prescribe a fixed number of Sequence Diagrams for a project.

All visible diagram labels must be **English**.

## 2. Lecturer Sequence-Diagram Rules Applied

This is a **UML Sequence Diagram**.

It answers:

> In what chronological order do the participants exchange messages to complete this scenario?

It is **not**:
- a Use Case Diagram;
- an Activity Diagram;
- a State Diagram;
- a Class Diagram;
- an ERD/database schema;
- a Component Diagram;
- a UI mockup.

### Required notation

- Human role: Actor with a lifeline.
- Internal/external software participant: named object/system lifeline.
- Lifelines run vertically; time flows **top to bottom**.
- Request/command/event message: **solid** horizontal arrow.
- Direct return/response message: **dashed** arrow back to the caller.
- Activation bars show when a participant is executing work.
- A self-message is allowed only for a meaningful internal validation/revalidation.
- Do not use Use Case `<<include>>` / `<<extend>>` arrows inside a Sequence Diagram.
- Do not use Class Association/Aggregation/Composition diamonds inside a Sequence Diagram.
- Do not use arrows merely as decoration.
- Do not expose passwords, OTP values, secrets, tokens, or sensitive payloads in message labels.

### Combined-fragment policy

The lecturer material supplied does not make `alt` / `opt` / `loop` fragments a mandatory course requirement. They may be used as standard UML drawing aids **only when they make a critical branch clearer**.

For this specification:
- main success flow is mandatory;
- only the explicitly listed critical alternatives should be rendered;
- do not turn every validation rule into another `alt` frame;
- when a branch would overcrowd the sheet, keep the main flow visually dominant and use one compact note for the less important failure cases.

### Internal architecture neutrality

The project specification does not mandate microservices. Therefore do not invent `BookingMicroservice`, `QueueMicroservice`, etc.

Use these implementation-neutral internal participants where specified:
- application/dashboard boundary;
- `Aafiatak Backend`;
- `Aafiatak Data Store`.

The Data Store is a **Sequence participant**, not a Use Case actor and not a Class Diagram class.

## 3. Scenario Definition

### Goal
Record an approved operational exception, preserve affected confirmed Appointments, document an approved action/outcome for each affected Appointment, and close the exception only after all resolution obligations are satisfied.

For concreteness, the main branch is anchored on `CONFLICT_DETECTED`, while compact alternatives cover `SESSION_CANCELLED`, facility-side cancellation/refund, and documented escalation.

### Primary facility actor
Use `Booking & Reception Staff` in the rendered main scenario because it is the principal daily-operations role.

`Facility Administrator` is also authorized for the generic operational-exception lifecycle. The diagram may add a small note:
`Facility Administrator may perform the same authorized facility-actor steps.`

Do not combine both human actors into a fake inheritance hierarchy.

### Conditional supporting participants
- `Patient`
- `Notification Service`
- `Payment Gateway` — only when facility-responsible full refund is needed.

`Platform Administrator` review belongs to a **later, separate escalation-review use case**. It is therefore deliberately not a lifeline in this Sequence Diagram.

### Preconditions
1. Authorized facility actor is authenticated.
2. Supported unplanned event occurs after publication/during daily operation.
3. Event can be classified as an approved OperationalException type.
4. Affected operational context/appointments can be identified.

### Success postconditions
- OperationalException closes only when every affected Appointment has documented action/outcome.
- Appointment/payment/capacity history remains preserved/auditable.
- No silent deletion.
- No reverse import of internal free capacity into same published release.
- Facility-responsible paid cancellation starts full refund.

## 4. Exact Participants

Left-to-right:

| # | Lifeline | Kind | Responsibility |
|---:|---|---|---|
| 1 | `Booking & Reception Staff` | Human Actor | Records exception, chooses/records resolution, requests closure |
| 2 | `Facility Web Dashboard` | Boundary | Facility interaction boundary |
| 3 | `Aafiatak Backend` | Control/System | Orchestrates exception/resolution/closure rules |
| 4 | `Aafiatak Data Store` | Internal data participant | Persists OperationalException, affected Appointments, resolution records and audit |
| 5 | `Notification Service` | External system | Delivers affected-Patient operational notifications |
| 6 | `Patient` | Human Actor | Receives information and may agree to a suitable alternative |
| 7 | `Payment Gateway` | External system | Executes full refund when facility responsibility and collected payment require it |

Do not add Doctor as the actor who records delay/absence. Doctor communicates outside the system; facility staff records the exception.

## 5. Mandatory Main Sequence — Open and Assess Exception

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| 1 | Booking & Reception Staff | Facility Web Dashboard | `Record operational event and context` | Solid action |
| 2 | Facility Web Dashboard | Aafiatak Backend | `Create OperationalException(type, context, reason)` | Solid request |
| 3 | Aafiatak Backend | Aafiatak Data Store | `Persist OPEN exception and link operational context` | Solid request |
| 4 | Aafiatak Data Store | Aafiatak Backend | `OperationalException created` | Dashed response |
| 5 | Aafiatak Backend | Aafiatak Data Store | `Identify affected CONFIRMED Appointments and relevant active holds/capacity` | Solid request |
| 6 | Aafiatak Data Store | Aafiatak Backend | `Affected context / unresolved Appointment set` | Dashed response |
| 7 | Aafiatak Backend | Facility Web Dashboard | `Display affected Appointments and required resolution status` | Dashed response |

For `CONFLICT_DETECTED`, preserve the confirmed Appointment while resolution is being decided.

## 6. Mandatory Resolution Choice Fragment

Use an `alt` fragment with these three approved resolution paths.

### Branch A — `[suitable equivalent alternative agreed]`

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| A1 | Booking & Reception Staff | Patient | `Communicate suitable alternative` | Solid real-world interaction |
| A2 | Patient | Booking & Reception Staff | `Agree to equivalent alternative` | Dashed response |
| A3 | Booking & Reception Staff | Facility Web Dashboard | `Record agreed alternative and reason` | Solid action |
| A4 | Facility Web Dashboard | Aafiatak Backend | `Apply approved same-service/equivalent-terms reschedule` | Solid request |
| A5 | Aafiatak Backend | Aafiatak Data Store | `Secure valid destination first; preserve history; write exception resolution` | Solid request |
| A6 | Aafiatak Data Store | Aafiatak Backend | `Alternative committed / resolution recorded` | Dashed response |

The reschedule must obey SD-04 invariants: same ServiceOffering/equivalent saved terms and valid capacity first.

### Branch B — `[facility-side cancellation required]`

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| B1 | Booking & Reception Staff | Facility Web Dashboard | `Record facility-side cancellation outcome` | Solid action |
| B2 | Facility Web Dashboard | Aafiatak Backend | `Cancel affected Appointment by facility` | Solid request |
| B3 | Aafiatak Backend | Aafiatak Data Store | `Set CANCELLED_BY_FACILITY + preserve history + write resolution` | Solid request |
| B4 | Aafiatak Data Store | Aafiatak Backend | `Cancellation committed / paid?` | Dashed response |

If an electronic amount was collected:

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| B5 | Aafiatak Backend | Payment Gateway | `Initiate full collected-amount refund` | Solid request |
| B6 | Payment Gateway | Aafiatak Backend | `Refund result/pending reference` | Dashed response |
| B7 | Aafiatak Backend | Aafiatak Data Store | `Persist independent refund status` | Solid request |
| B8 | Aafiatak Data Store | Aafiatak Backend | `Refund state saved` | Dashed response |

Facility-responsible full refund applies regardless of Patient self-cancellation policy.

### Branch C — `[immediate safe resolution unavailable]`

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| C1 | Booking & Reception Staff | Facility Web Dashboard | `Create documented support escalation` | Solid action |
| C2 | Facility Web Dashboard | Aafiatak Backend | `Record escalation context` | Solid request |
| C3 | Aafiatak Backend | Aafiatak Data Store | `Persist escalation; keep exception OPEN` | Solid request |
| C4 | Aafiatak Data Store | Aafiatak Backend | `Escalation recorded for later platform review` | Dashed response |

Add a compact note:

`Platform Administrator review occurs later through the separate escalation-review use case; it is outside this sequence.`

Do not imply that Platform Administrator performs daily facility resolution automatically.

## 7. Notifications

After a resolution decision that affects Patient communication:

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| N1 | Aafiatak Backend | Notification Service | `Send affected-Patient operational notification` | Solid request |
| N2 | Notification Service | Aafiatak Backend | `Notification accepted/result` | Dashed response |
| N3 | Notification Service | Patient | `Deliver exception/resolution information` | Solid notification event |

WhatsApp must **not** be used for these general notifications in current scope.

## 8. Mandatory Closure Sequence

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| 8 | Booking & Reception Staff | Facility Web Dashboard | `Request Close Operational Exception` | Solid action |
| 9 | Facility Web Dashboard | Aafiatak Backend | `Close exception request` | Solid request |
| 10 | Aafiatak Backend | Aafiatak Data Store | `Verify documented action/outcome for every affected Appointment` | Solid request |
| 11 | Aafiatak Data Store | Aafiatak Backend | `Resolution completeness result` | Dashed response |

Use final `alt`:

### `[all affected Appointments resolved]`
- Backend -> Data Store: `Close OperationalException and preserve audit trail` (solid)
- Data Store --> Backend: `Exception CLOSED` (dashed)
- Backend --> Dashboard: `Closure confirmed` (dashed)

### `[one or more affected Appointments unresolved]`
- Backend --> Dashboard: `Closure rejected; show unresolved requirements` (dashed)
- Exception remains `OPEN`.

## 9. Special `SESSION_CANCELLED` Alternative

If exception type is `SESSION_CANCELLED`:
- affected release/session becomes non-bookable;
- active ReservationHolds are released;
- confirmed Appointments are **not deleted**;
- every confirmed Appointment requires a documented alternative/cancellation/refund/escalation resolution;
- cancelled session/group does not republish seats for new booking.

Represent this as one compact note or `alt` block; do not duplicate the entire main lifecycle.

## 10. Binding Rules

Supported exception examples:
- `DOCTOR_DELAYED`
- `DOCTOR_ABSENT`
- `SESSION_CANCELLED`
- `FACILITY_CLOSED`
- `CAPACITY_REDUCED`
- `POWER_OR_CONNECTIVITY_OUTAGE`
- `CONFLICT_DETECTED`

Additional binding rules:
- Doctor does not record delay/absence in-system.
- Internal free facility capacity cannot be imported into same Aafiatak release to solve conflict.
- Resolution records must preserve action/outcome per affected Appointment.
- Facility-side paid cancellation -> full refund.
- Payment Gateway result cannot be arbitrarily overwritten by Reception.
- Notification state is independent of Appointment/exception resolution.
- Exception closure gate is mandatory.

## 11. Forbidden Content

Do not show:
- silent deletion of affected Appointment.
- closing exception while unresolved Appointments remain.
- importing internal free capacity into same release.
- Doctor pressing an in-system `Report Delay/Absence` action.
- partial refund.
- manual gateway-result override.
- WhatsApp general notification.
- Platform Administrator operating daily facility queue/availability.
- automatic alternative booking without Patient communication/agreement where agreement is required.


## Visual and Layout Contract

- Landscape orientation.
- One diagram per page/artboard.
- Exact title from this file at the top.
- Participants arranged left-to-right in the exact order defined here.
- Human Actor lifelines should be visually distinct from software/system lifelines.
- Keep `Aafiatak Backend` near the center because it orchestrates the interaction.
- External services should be placed to the right unless the exact participant order says otherwise.
- Use consistent lifeline spacing and activation-bar width.
- Preserve enough vertical space between messages for readable labels.
- Avoid crossing messages; Sequence diagrams should normally need almost none.
- Return messages must be visibly dashed.
- Do not shrink text below normal report readability.
- Do not add decorative icons, gradients, dashboards, or unrelated annotations.
- Use concise English message labels; do not put paragraph-length explanations on arrows.

## 12. Deep Review Record

- Pass 1: lecturer Sequence chronology/notation.
- Pass 2: supported exception type scope.
- Pass 3: actor authorization.
- Pass 4: affected-Appointment preservation.
- Pass 5: per-Appointment documented resolution.
- Pass 6: equivalent-alternative constraints.
- Pass 7: facility-side cancellation/full refund.
- Pass 8: escalation boundary.
- Pass 9: Notification Service / WhatsApp boundary.
- Pass 10: session-cancellation hold/appointment handling.
- Pass 11: mandatory closure gate.
- Pass 12: audit/history preservation.
- Pass 13: no internal-capacity reverse import.
- Pass 14: external gateway result authority.
- Pass 15: final UCM-13 / MVP §§23–24 traceability.


## Mandatory QA Gates

Before marking the diagram ready:

1. Verify the exact title.
2. Verify every mandatory participant exists exactly once unless this file explicitly permits a repeated actor view.
3. Verify left-to-right participant order.
4. Verify every mandatory main-flow message and its sender/receiver.
5. Verify message chronology top-to-bottom.
6. Verify request/command arrows are solid.
7. Verify direct responses are dashed.
8. Verify all critical alternative fragments listed in this file.
9. Verify all stated preconditions and postconditions are respected.
10. Verify state/lifecycle changes against the authoritative project rules.
11. Verify no prohibited behavior or deferred feature is introduced.
12. Verify no Database is modeled as a human/external Actor.
13. Verify the rendered SVG/PNG/PDF is opened and visually inspected.
14. Perform at least three correction passes: semantics, message notation, visual layout.
15. Final visual status: `awaiting-user-approval`.

Do not self-approve the visual as “100% final” without user inspection.
