# Sequence Diagram — Book Appointment
## Aafiatak Medical Appointment Booking System — MVP Sequence Diagram Specification

**Diagram ID:** `SD-02`  
**Deliverable:** UML Sequence Diagram  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** MUC-06/MUC-07/MUC-08/MUC-09/MUC-10; PUC-11/12/13/14/21/22; UCM-03/UCM-04; Project Specification §§13.3–16.5, 18, 19  
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
Create exactly one confirmed Aafiatak Appointment from the earliest currently bookable ArrivalGroup while respecting the governing booking policy and ReservationHold rules.

This single Sequence Diagram deliberately contains two policy branches:
- `PAY_AT_FACILITY`
- `FULL_PAYMENT_REQUIRED`

The Patient does not choose the policy; the published release terms govern it.

### Primary actor
- `Patient`

### Supporting external participants
- `Payment Gateway` — only in the full-payment branch.
- `Notification Service` — after successful confirmation; notification failure must not reverse a successful booking/payment.

### Preconditions
1. Patient is authenticated.
2. Selected `ServiceOffering` and branch/doctor context are active/valid.
3. A `PUBLISHED` AvailabilityRelease exists for the selected service/day.
4. Patient has no overlapping active hold/confirmed appointment except controlled rescheduling.
5. A group is bookable only if release/group state, remaining capacity, and timing permit a full hold window.

### Success postconditions
- Exactly one `CONFIRMED` Appointment exists.
- Exactly one capacity unit is consumed.
- ReservationHold is `CONSUMED`.
- Appointment contains the required historical booking snapshot.
- `PAY_AT_FACILITY`: no PaymentIntent exists.
- `FULL_PAYMENT_REQUIRED`: trusted success is verified and PaymentIntent is `SUCCEEDED`.
- Notification state remains independent.

## 4. Exact Participants

Use exactly these lifelines, left-to-right:

| # | Lifeline | Kind | Responsibility |
|---:|---|---|---|
| 1 | `Patient` | Human Actor | Selects context, confirms booking, completes payment when required |
| 2 | `Patient Application` | Boundary | Presents availability/terms/countdown and submits actions |
| 3 | `Aafiatak Backend` | Control/System | Enforces booking, hold, policy, payment, idempotency and atomic confirmation rules |
| 4 | `Aafiatak Data Store` | Internal data participant | Reads/writes AvailabilityRelease, ArrivalGroup, ReservationHold, PaymentIntent, Appointment and snapshots transactionally |
| 5 | `Payment Gateway` | External system | Processes and returns trusted full-payment result only in FULL_PAYMENT_REQUIRED |
| 6 | `Notification Service` | External system | Delivers booking/payment notification after core transaction |

Do not add the facility internal schedule/HIS as a participant.

## 5. Mandatory Common Booking Prefix

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| 1 | Patient | Patient Application | `Select service / doctor context / day` | Solid action |
| 2 | Patient Application | Aafiatak Backend | `Request currently bookable Aafiatak capacity` | Solid request |
| 3 | Aafiatak Backend | Aafiatak Data Store | `Load PUBLISHED release + frozen booking terms` | Solid request |
| 4 | Aafiatak Data Store | Aafiatak Backend | `Release terms and current capacity state` | Dashed response |
| 5 | Aafiatak Backend | Aafiatak Data Store | `Find earliest currently bookable ArrivalGroup` | Solid request |
| 6 | Aafiatak Data Store | Aafiatak Backend | `Selected group/window + remaining capacity` | Dashed response |
| 7 | Aafiatak Backend | Patient Application | `Display arrival window and governing booking terms` | Dashed response |
| 8 | Patient | Patient Application | `Confirm intent to proceed` | Solid action |
| 9 | Patient Application | Aafiatak Backend | `Create temporary ReservationHold` | Solid request |
| 10 | Aafiatak Backend | Aafiatak Data Store | `Atomically revalidate group and acquire one ACTIVE hold` | Solid request |
| 11 | Aafiatak Data Store | Aafiatak Backend | `Hold acquired: id + expiresAt + selected group` | Dashed response |
| 12 | Aafiatak Backend | Patient Application | `Show protected group and hold countdown` | Dashed response |

The hold duration value itself must **not** be invented; exact default remains open.

## 6. Mandatory `alt` Fragment — Booking Policy

### Branch A — `[bookingPolicy = PAY_AT_FACILITY]`

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| A1 | Patient | Patient Application | `Accept payment due at facility and confirm booking` | Solid action |
| A2 | Patient Application | Aafiatak Backend | `Finalize pay-at-facility booking(holdId)` | Solid request |
| A3 | Aafiatak Backend | Aafiatak Data Store | `Revalidate hold + release + group + time eligibility` | Solid request |
| A4 | Aafiatak Data Store | Aafiatak Backend | `Eligible and hold ACTIVE` | Dashed response |
| A5 | Aafiatak Backend | Aafiatak Data Store | `Atomic commit: consume hold + consume capacity once + create CONFIRMED Appointment snapshot` | Solid request |
| A6 | Aafiatak Data Store | Aafiatak Backend | `Appointment confirmed; hold CONSUMED` | Dashed response |
| A7 | Aafiatak Backend | Notification Service | `Send pay-at-facility booking confirmation` | Solid request |
| A8 | Notification Service | Aafiatak Backend | `Notification accepted/result` | Dashed response |
| A9 | Aafiatak Backend | Patient Application | `Confirmed appointment + booking/verification code + DUE_AT_FACILITY presentation` | Dashed response |
| A10 | Patient Application | Patient | `Display confirmation and arrival window` | Dashed response |

Mandatory note:
`No PaymentIntent is created in this branch.`

### Branch B — `[bookingPolicy = FULL_PAYMENT_REQUIRED]`

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| B1 | Patient | Patient Application | `Proceed to full electronic payment` | Solid action |
| B2 | Patient Application | Aafiatak Backend | `Start full payment for active hold` | Solid request |
| B3 | Aafiatak Backend | Aafiatak Data Store | `Load hold/snapshot and enforce one non-terminal PaymentIntent` | Solid request |
| B4 | Aafiatak Data Store | Aafiatak Backend | `Valid hold + amount/currency + PaymentIntent context` | Dashed response |
| B5 | Aafiatak Backend | Aafiatak Data Store | `Create or safely reuse PaymentIntent` | Solid request |
| B6 | Aafiatak Data Store | Aafiatak Backend | `PaymentIntent ready` | Dashed response |
| B7 | Aafiatak Backend | Payment Gateway | `Initiate full amount payment` | Solid request |
| B8 | Payment Gateway | Aafiatak Backend | `Gateway payment session/reference` | Dashed response |
| B9 | Aafiatak Backend | Patient Application | `Continue approved gateway interaction` | Dashed response |
| B10 | Patient | Payment Gateway | `Complete gateway payment interaction` | Solid external action |
| B11 | Payment Gateway | Patient Application | `Return to application` | Dashed return — NOT payment truth |
| B12 | Patient Application | Aafiatak Backend | `Report client return from gateway` | Solid request |
| B13 | Aafiatak Backend | Payment Gateway | `Verify payment through trusted gateway channel` | Solid request |
| B14 | Payment Gateway | Aafiatak Backend | `Trusted payment result: SUCCESS` | Dashed response |
| B15 | Aafiatak Backend | Aafiatak Data Store | `Persist SUCCEEDED and atomically revalidate hold/release/group/time` | Solid request |
| B16 | Aafiatak Data Store | Aafiatak Backend | `Payment persisted; booking target still eligible` | Dashed response |
| B17 | Aafiatak Backend | Aafiatak Data Store | `Atomic commit: consume hold/capacity once + create CONFIRMED Appointment snapshot` | Solid request |
| B18 | Aafiatak Data Store | Aafiatak Backend | `Appointment confirmed; hold CONSUMED` | Dashed response |
| B19 | Aafiatak Backend | Notification Service | `Send full-payment booking confirmation` | Solid request |
| B20 | Notification Service | Aafiatak Backend | `Notification accepted/result` | Dashed response |
| B21 | Aafiatak Backend | Patient Application | `Confirmed Appointment + independent SUCCEEDED payment status` | Dashed response |
| B22 | Patient Application | Patient | `Display confirmation / receipt summary / arrival window` | Dashed response |

Critical visual note beside B11–B14:

`Browser/app return is not payment truth. Trusted webhook/query verification is required.`

## 7. Critical Alternative / Failure Fragments

Render only these critical branches so the diagram remains readable.

### `alt` C1 — No currently bookable capacity
Occurs before hold creation:
- Backend returns `No currently bookable capacity`.
- No hold/Appointment is created.
- Patient may use Notify Me When Available; that action grants no reservation/priority.

### `alt` C2 — Another request wins the last unit
At atomic hold acquisition:
- Data Store returns `Hold acquisition failed`.
- No duplicate capacity ownership.
- No Appointment created.

### `alt` C3 — Hold expires or target becomes ineligible before confirmation
- Hold becomes `EXPIRED`/`RELEASED`.
- No Appointment is created.
- A hold is never consumed at/after group start or after release cancellation.

### `alt` C4 — Full payment fails
- PaymentIntent records terminal failure/expiry as verified.
- Appointment is not created.
- A new payment attempt is allowed only while hold remains valid and idempotent rules permit.

### `alt` C5 — Trusted payment succeeds but hold/target is no longer eligible
- Persist successful payment independently.
- Do **not** fabricate/conflict an Appointment.
- Attempt only safe equivalent recovery under equivalent terms.
- Otherwise start full refund when applicable or move case to `UNDER_REVIEW`.

### `alt` C6 — Duplicate/delayed gateway event
- Process idempotently.
- No duplicate charge, Appointment, refund, or payment transition.

### `opt` C7 — Notification delivery fails after successful core transaction
- Payment/Appointment success remains persisted.
- Notification retries independently.
- Do not roll back successful payment/booking because notification failed.

## 8. Binding Domain Rules

- Earliest currently bookable ArrivalGroup is selected; Patient does not choose an arbitrary group.
- Active ReservationHold protects exactly one capacity unit.
- `remaining = published - held - confirmed - withdrawn_to_facility`.
- `published` cannot increase after publication.
- Active held/confirmed units cannot be withdrawn.
- Appointment, PaymentIntent, ReservationHold are independent lifecycles.
- FULL_PAYMENT_REQUIRED confirms only after trusted payment verification while booking target is valid.
- PAY_AT_FACILITY has no PaymentIntent.
- No deposit/partial payment/remaining balance.
- Full payment grants no queue priority.
- Booking is confirmed directly; there is no manual facility-approval state.
- Appointment snapshot preserves branch/doctor/service/amount/currency/policy/group/window/cancellation/no-show terms.

## 9. Forbidden Sequence Content

Do not show:
- Patient selecting booking policy.
- Patient selecting arbitrary ArrivalGroup.
- manual booking approval.
- deposit or partial payment.
- reverse import of internal facility capacity.
- automatic group rebalance.
- browser return used as sole payment truth.
- creation of multiple active PaymentIntents for the same hold.
- duplicate Appointment from retry.
- exact guaranteed doctor-entry time.


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

- Pass 1: lecturer chronological-message rules.
- Pass 2: booking eligibility and earliest-group allocation.
- Pass 3: release/group lifecycle and timing.
- Pass 4: ReservationHold concurrency/expiry.
- Pass 5: PAY_AT_FACILITY branch.
- Pass 6: FULL_PAYMENT_REQUIRED trusted-gateway boundary.
- Pass 7: PaymentIntent idempotency.
- Pass 8: atomic Appointment/capacity confirmation.
- Pass 9: booking snapshot immutability.
- Pass 10: payment-success/appointment-failure recovery.
- Pass 11: notification independence.
- Pass 12: no approval/deposit/partial-payment drift.
- Pass 13: duplicate/retry audit.
- Pass 14: request/response notation audit.
- Pass 15: final traceability to UCM-03/UCM-04 and MVP §§13–19.


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
