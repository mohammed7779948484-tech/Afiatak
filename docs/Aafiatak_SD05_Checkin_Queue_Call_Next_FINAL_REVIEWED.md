# Sequence Diagram — Patient Check-in, Queue & Call Next Patient
## Aafiatak Medical Appointment Booking System — MVP Sequence Diagram Specification

**Diagram ID:** `SD-05`  
**Deliverable:** UML Sequence Diagram  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** BRUC-17/18/19/21/22/23/24; DUC-06/07/08; UCM-10 Register Patient Check-in + UCM-14 Call Next Patient; Project Specification §§19.4–22  
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
Model one coherent service-day interaction:
1. Reception verifies the intended confirmed Appointment and registers Patient check-in.
2. System creates/activates VisitInstance and QueueEntry in the original ArrivalGroup.
3. Queue order is calculated using approved rules.
4. Doctor views the relevant waiting list and calls the next Patient.
5. Doctor call changes QueueEntry call state only; it does **not** change VisitInstance state.

This is intentionally one linked Sequence because the lecturer allows a coherent chain of interactions, and these actions form one continuous arrival-to-call scenario.

### Human actors
- `Patient`
- `Booking & Reception Staff`
- `Doctor`

### Preconditions
1. Reception staff is authenticated/authorized.
2. Patient presents a valid booking identifier.
3. Intended Appointment is `CONFIRMED` and not cancelled.
4. Main path assumes normal on-time/eligible arrival.
5. Doctor is authenticated and views only the Doctor's assigned waiting context.

### Success postconditions
- VisitInstance is `CHECKED_IN`.
- Exactly one active QueueEntry exists in the original ArrivalGroup.
- Appointment remains `CONFIRMED`.
- QueueEntry becomes `CALLED` when Doctor successfully calls.
- Doctor call does not set VisitInstance to `IN_SERVICE`, `COMPLETED`, `NOT_COMPLETED`, or `NO_SHOW`.

## 4. Exact Participants

Left-to-right:

| # | Lifeline | Kind | Responsibility |
|---:|---|---|---|
| 1 | `Patient` | Human Actor | Presents booking identifier and receives check-in/call information |
| 2 | `Booking & Reception Staff` | Human Actor | Searches Appointment and confirms arrival |
| 3 | `Facility Web Dashboard` | Boundary | Staff interaction boundary |
| 4 | `Aafiatak Backend` | Control/System | Validates Appointment, check-in, queue and Doctor-call rules |
| 5 | `Aafiatak Data Store` | Internal data participant | Persists VisitInstance/QueueEntry and retrieves queue state |
| 6 | `Doctor Interface` | Boundary | Doctor's limited waiting/call interface |
| 7 | `Doctor` | Human Actor | Views waiting list and calls next Patient |
| 8 | `Notification Service` | External system | Sends independent check-in/turn notification when used |

Participant order is intentionally chosen to keep facility operations in the center and avoid crossing lines.

## 5. Mandatory Main Sequence — Check-in

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| 1 | Patient | Booking & Reception Staff | `Present booking number / phone / QR / verification code` | Solid real-world action |
| 2 | Booking & Reception Staff | Facility Web Dashboard | `Search or scan Appointment` | Solid action |
| 3 | Facility Web Dashboard | Aafiatak Backend | `Find intended Appointment(identifier)` | Solid request |
| 4 | Aafiatak Backend | Aafiatak Data Store | `Load Appointment + arrival context + existing VisitInstance` | Solid request |
| 5 | Aafiatak Data Store | Aafiatak Backend | `Appointment/visit context` | Dashed response |
| 6 | Aafiatak Backend | Aafiatak Backend | `Validate facility + CONFIRMED + normal arrival eligibility` | Solid self-message |
| 7 | Aafiatak Backend | Facility Web Dashboard | `Display valid Appointment for check-in` | Dashed response |
| 8 | Booking & Reception Staff | Facility Web Dashboard | `Confirm Patient arrival` | Solid action |
| 9 | Facility Web Dashboard | Aafiatak Backend | `Register Patient check-in` | Solid request |
| 10 | Aafiatak Backend | Aafiatak Data Store | `Atomic check-in: create VisitInstance if needed; set CHECKED_IN; record actual arrival; create/activate QueueEntry in original group` | Solid request |
| 11 | Aafiatak Data Store | Aafiatak Backend | `Check-in and QueueEntry committed` | Dashed response |
| 12 | Aafiatak Backend | Aafiatak Data Store | `Calculate normal queue order by check-in time; confirmed_at tie-break` | Solid request |
| 13 | Aafiatak Data Store | Aafiatak Backend | `Current waiting order / approximate Patient position` | Dashed response |
| 14 | Aafiatak Backend | Facility Web Dashboard | `Check-in complete` | Dashed response |
| 15 | Aafiatak Backend | Notification Service | `Send check-in confirmation / approaching-turn status when applicable` | Solid request |
| 16 | Notification Service | Aafiatak Backend | `Notification accepted/result` | Dashed response |
| 17 | Notification Service | Patient | `Deliver check-in/queue notification` | Solid notification event |

## 6. Mandatory Continuation — Doctor Calls Next Patient

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| 18 | Doctor | Doctor Interface | `View waiting Patients` | Solid action |
| 19 | Doctor Interface | Aafiatak Backend | `Request Doctor-assigned waiting context` | Solid request |
| 20 | Aafiatak Backend | Aafiatak Data Store | `Load callable QueueEntries using approved ordering` | Solid request |
| 21 | Aafiatak Data Store | Aafiatak Backend | `Waiting list / callable entries` | Dashed response |
| 22 | Aafiatak Backend | Doctor Interface | `Display relevant waiting list` | Dashed response |
| 23 | Doctor | Doctor Interface | `Choose Call Next Patient` | Solid action |
| 24 | Doctor Interface | Aafiatak Backend | `Call selected QueueEntry` | Solid request |
| 25 | Aafiatak Backend | Aafiatak Data Store | `Revalidate callable state and set QueueEntry = CALLED` | Solid request |
| 26 | Aafiatak Data Store | Aafiatak Backend | `Queue call recorded` | Dashed response |
| 27 | Aafiatak Backend | Doctor Interface | `Call confirmed` | Dashed response |
| 28 | Aafiatak Backend | Notification Service | `Send turn/call notification when applicable` | Solid request |
| 29 | Notification Service | Aafiatak Backend | `Notification accepted/result` | Dashed response |
| 30 | Notification Service | Patient | `Notify Patient to proceed when applicable` | Solid notification event |

Place UML Notes next to messages 20–27:

`The Patient who just checked in is NOT automatically next. Approved queue ordering determines the callable QueueEntry. This sequence depicts the case in which that Patient's QueueEntry is eventually selected.`

`Doctor call changes QueueEntry only. VisitInstance state is unchanged by Doctor.`

## 7. Critical Alternative / Failure Fragments

### A1 — Appointment already cancelled
At validation:
- Backend rejects check-in.
- No valid VisitInstance check-in or QueueEntry is created.

### A2 — Late arrival detected
Do not continue the normal numeric queue path automatically.
If staff chooses manual late acceptance:
- Keep original Appointment and ArrivalGroup.
- Register check-in.
- Mark late accepted.
- Create/activate QueueEntry with `manualHandling`.
- Exclude from automatic numeric position.
- No re-entry and no consumption of another ArrivalGroup.
If terminal NO_SHOW already exists, do not reopen it.

### A3 — Erroneous check-in correction before service start
If separately invoked by staff:
- QueueEntry -> `REMOVED`.
- correction reason is audited.
- VisitInstance may return `CHECKED_IN -> CREATED`.
- Do not apply after service has started.

### A4 — No callable Patient
Doctor call performs no state change.

### A5 — Selected QueueEntry changed/removed/completed before Doctor confirmation
- Backend rejects stale call.
- Refresh waiting context.

### A6 — Accepted late Patient selected for manual call
- Staff/Doctor may call when operationally appropriate.
- No guaranteed numeric queue priority.

## 8. Binding Queue/Visit Rules

Normal queue ordering inside one ArrivalGroup:
1. actual check-in time;
2. earlier Appointment `confirmed_at` as tie-breaker.

Additional rules:
- Full payment gives no priority.
- Aafiatak does not know/merge the facility's complete internal queue.
- Patient sees only own approximate position.
- Patient cannot self-check-in.
- Facility staff changes VisitInstance states.
- Doctor may identify/call next but cannot change VisitInstance lifecycle.
- `QueueEntry`: WAITING -> CALLED -> DONE; audited REMOVED when applicable.
- no automatic re-entry/requeue state.

## 9. Forbidden Content

Do not show:
- Patient self-check-in.
- Doctor setting `IN_SERVICE`, `COMPLETED`, `NOT_COMPLETED`, `NO_SHOW`.
- payment priority.
- automatic late transfer to next group.
- exact guaranteed service-entry time.
- merging with complete facility internal queue.
- Doctor reporting delay/absence through this interface.
- medical notes/diagnosis/prescription.


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

## 10. Deep Review Record

- Pass 1: lecturer linked-interaction suitability.
- Pass 2: check-in actor authorization.
- Pass 3: Appointment eligibility.
- Pass 4: VisitInstance creation/state.
- Pass 5: QueueEntry creation/state.
- Pass 6: normal queue ordering.
- Pass 7: payment-no-priority rule.
- Pass 8: Doctor permission boundary.
- Pass 9: stale call/concurrency handling.
- Pass 10: late-arrival/manual-handling branch.
- Pass 11: erroneous check-in correction boundary.
- Pass 12: notification independence and final UCM-10/UCM-14 traceability.


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
