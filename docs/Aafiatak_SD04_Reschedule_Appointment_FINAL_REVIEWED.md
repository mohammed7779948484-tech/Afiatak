# Sequence Diagram — Reschedule Appointment
## Aafiatak Medical Appointment Booking System — MVP Sequence Diagram Specification

**Diagram ID:** `SD-04`  
**Deliverable:** UML Sequence Diagram  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** BRUC-15; UCM-09 Reschedule Appointment; Project Specification §17.3 and late-arrival boundary §22  
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
Move one eligible `CONFIRMED` Appointment to valid new capacity **after Patient communication/agreement**, securing the destination first and preserving the same ServiceOffering and historical financial/booking terms.

### Primary actor
- `Booking & Reception Staff`

### Secondary participant
- `Patient` — agreement/communication participant; final change notification may be delivered after the transaction.

### Preconditions
1. Staff is authenticated and authorized for the facility.
2. Appointment is `CONFIRMED`.
3. Patient and facility have communicated and agreed to the change.
4. Destination is same `ServiceOffering`.
5. Destination preserves same snapshotted amount/booking/cancellation/no-show terms.
6. Valid destination capacity is currently bookable.

### Success postconditions
- Appointment remains `CONFIRMED`.
- New scheduling/group details are stored.
- Old capacity is released **only after** destination capacity is secured.
- `AppointmentStatusHistory` preserves previous/new scheduling data, actor and reason.
- Financial snapshot remains unchanged.
- No top-up, partial refund, or mixed payment lifecycle is created.

## 4. Exact Participants

Left-to-right:

| # | Lifeline | Kind | Responsibility |
|---:|---|---|---|
| 1 | `Booking & Reception Staff` | Human Actor | Selects agreed destination and confirms reason |
| 2 | `Facility Web Dashboard` | Boundary | Shows Appointment/history and submits reschedule |
| 3 | `Aafiatak Backend` | Control/System | Validates terms and performs atomic move |
| 4 | `Aafiatak Data Store` | Internal data participant | Locks/validates capacity, updates Appointment, writes history |
| 5 | `Notification Service` | External system | Sends independent appointment-change notification |
| 6 | `Patient` | Human recipient | Receives final change notification / is party to prior agreement |

Do not add Payment Gateway to the successful in-place reschedule. The financial snapshot does not change.

## 5. Mandatory Main Success Sequence

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| 1 | Booking & Reception Staff | Facility Web Dashboard | `Open CONFIRMED Appointment and choose Reschedule` | Solid action |
| 2 | Facility Web Dashboard | Aafiatak Backend | `Load reschedule context` | Solid request |
| 3 | Aafiatak Backend | Aafiatak Data Store | `Read Appointment snapshot/history/current capacity` | Solid request |
| 4 | Aafiatak Data Store | Aafiatak Backend | `Current booking and governing terms` | Dashed response |
| 5 | Aafiatak Backend | Facility Web Dashboard | `Display current snapshot and permitted destination context` | Dashed response |
| 6 | Booking & Reception Staff | Facility Web Dashboard | `Select agreed new day/group/session` | Solid action |
| 7 | Facility Web Dashboard | Aafiatak Backend | `Validate destination` | Solid request |
| 8 | Aafiatak Backend | Aafiatak Data Store | `Check same ServiceOffering/terms + current destination bookability` | Solid request |
| 9 | Aafiatak Data Store | Aafiatak Backend | `Destination valid and currently bookable` | Dashed response |
| 10 | Aafiatak Backend | Facility Web Dashboard | `Display valid proposed move` | Dashed response |
| 11 | Booking & Reception Staff | Facility Web Dashboard | `Confirm reschedule and record reason` | Solid action |
| 12 | Facility Web Dashboard | Aafiatak Backend | `Commit reschedule` | Solid request |
| 13 | Aafiatak Backend | Aafiatak Data Store | `Atomic transaction: secure destination first; update schedule/group; release old seat after secure; write history` | Solid request |
| 14 | Aafiatak Data Store | Aafiatak Backend | `Reschedule committed; Appointment remains CONFIRMED` | Dashed response |
| 15 | Aafiatak Backend | Notification Service | `Send appointment-change notification` | Solid request |
| 16 | Notification Service | Aafiatak Backend | `Notification accepted/result` | Dashed response |
| 17 | Notification Service | Patient | `Deliver new agreed arrival details` | Solid notification event |
| 18 | Aafiatak Backend | Facility Web Dashboard | `Display successful reschedule` | Dashed response |

## 6. Critical Alternative / Failure Fragments

### A1 — Destination becomes unavailable before commit
At message 13:
- Data Store cannot acquire destination.
- Backend aborts transaction.
- Old capacity is **not** released.
- Original Appointment remains unchanged.

### A2 — Destination terms differ
If different ServiceOffering, amount, booking policy, cancellation/refund policy or no-show policy:
- Backend rejects in-place reschedule.
- Correct path is old Appointment cancellation under saved rules + separate new Patient booking under new terms.
- Do not create top-up payment or partial refund.

### A3 — Concurrent request wins destination capacity
- Atomic destination acquisition fails safely.
- Original seat remains intact.
- No double consumption.

### A4 — Appointment no longer CONFIRMED
- Reschedule rejected.
- Do not reopen terminally cancelled Appointment.

### A5 — Late Patient is being rescheduled
- Same rules apply: communication/agreement + same-service/same-terms + valid new capacity.
- No automatic late transfer.
- Terminal `NO_SHOW` is not reversed through this flow.

## 7. Binding Domain Rules

- Secure destination first.
- Release old capacity only after destination is secured.
- Operation must be atomic.
- Appointment state remains `CONFIRMED`; reschedule is not a new Appointment status.
- Preserve previous/new release/group/window, actor, reason and history.
- Preserve original financial snapshot.
- No automatic rescheduling.
- No Patient self-rescheduling in current scope.

## 8. Forbidden Content

Do not show:
- Patient directly editing the appointment date/group.
- old seat released before destination acquisition.
- different-price/policy in-place move.
- top-up payment.
- partial refund.
- automatic late-patient transfer.
- new Appointment status called `RESCHEDULED`.
- deletion/replacement of history.


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

## 9. Deep Review Record

- Pass 1: lecturer chronological flow.
- Pass 2: role permission (Reception, not Patient).
- Pass 3: communication/agreement precondition.
- Pass 4: same ServiceOffering rule.
- Pass 5: same financial/booking snapshot rule.
- Pass 6: destination-first atomicity.
- Pass 7: old-capacity preservation on failure.
- Pass 8: Appointment remains CONFIRMED.
- Pass 9: AppointmentStatusHistory traceability.
- Pass 10: concurrent acquisition handling.
- Pass 11: late-arrival boundary.
- Pass 12: notification independence and final UCM-09 traceability.


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
