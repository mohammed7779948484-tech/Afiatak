# Sequence Diagram — Cancel Appointment & Refund
## Aafiatak Medical Appointment Booking System — MVP Sequence Diagram Specification

**Diagram ID:** `SD-03`  
**Deliverable:** UML Sequence Diagram  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** PUC-19; UCM-06 Cancel Appointment; Project Specification §§15.1, 17.1, 18, 19.2  
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
Allow Patient self-cancellation of the Patient's own eligible `CONFIRMED` Appointment and correctly handle capacity return plus full-or-zero refund using the Appointment's saved historical rules.

### Primary actor
- `Patient`

### Supporting external participants
- `Payment Gateway` — only if a full electronic refund is required.
- `Notification Service` — cancellation/availability notifications are independent of the cancellation transaction.

### Preconditions
1. Patient is authenticated and owns the Appointment.
2. Appointment is `CONFIRMED`.
3. Patient has not checked in.
4. Assigned ArrivalGroup window has not started.

### Success postconditions
- Appointment is `CANCELLED_BY_PATIENT`.
- Cancellation/history is preserved.
- Consumed seat returns only to the same ArrivalGroup and becomes bookable only if release/group/time rules allow.
- Refund is full collected amount or zero.
- PAY_AT_FACILITY produces no electronic refund.
- Cancellation remains final even when refund is pending.

## 4. Exact Participants

Left-to-right:

| # | Lifeline | Kind | Responsibility |
|---:|---|---|---|
| 1 | `Patient` | Human Actor | Reviews and confirms cancellation |
| 2 | `Patient Application` | Boundary | Displays cancellation/refund consequence and status |
| 3 | `Aafiatak Backend` | Control/System | Revalidates eligibility, applies saved policy, orchestrates cancellation |
| 4 | `Aafiatak Data Store` | Internal data participant | Persists Appointment/history, capacity and PaymentIntent refund state |
| 5 | `Payment Gateway` | External system | Executes full refund only when required |
| 6 | `Notification Service` | External system | Sends cancellation/availability notifications independently |

## 5. Mandatory Main Success Sequence

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| 1 | Patient | Patient Application | `Open confirmed Appointment and choose Cancel` | Solid action |
| 2 | Patient Application | Aafiatak Backend | `Request cancellation consequence(appointmentId)` | Solid request |
| 3 | Aafiatak Backend | Aafiatak Data Store | `Load Appointment snapshot + payment + check-in + group timing` | Solid request |
| 4 | Aafiatak Data Store | Aafiatak Backend | `Saved policy / payment / eligibility context` | Dashed response |
| 5 | Aafiatak Backend | Aafiatak Backend | `Validate ownership, CONFIRMED, not checked-in, group not started` | Solid self-message |
| 6 | Aafiatak Backend | Patient Application | `Display cancellation allowed + expected refund: FULL or ZERO` | Dashed response |
| 7 | Patient | Patient Application | `Confirm cancellation` | Solid action |
| 8 | Patient Application | Aafiatak Backend | `Cancel Appointment` | Solid request |
| 9 | Aafiatak Backend | Aafiatak Data Store | `Atomic revalidation + set CANCELLED_BY_PATIENT + write history + release same-group capacity when eligible` | Solid request |
| 10 | Aafiatak Data Store | Aafiatak Backend | `Cancellation committed + refund decision + capacity result` | Dashed response |

Then use an `alt` fragment for refund result.

### Branch `[full electronic refund required]`

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| R1 | Aafiatak Backend | Payment Gateway | `Initiate full collected-amount refund` | Solid request |
| R2 | Payment Gateway | Aafiatak Backend | `Refund result / pending reference` | Dashed response |
| R3 | Aafiatak Backend | Aafiatak Data Store | `Persist REFUND_PENDING / REFUNDED / review status` | Solid request |
| R4 | Aafiatak Data Store | Aafiatak Backend | `Payment refund state saved` | Dashed response |

### Branch `[refund due = zero OR PAY_AT_FACILITY]`

- No Payment Gateway call.
- For PAY_AT_FACILITY, no PaymentIntent exists.
- Appointment cancellation remains valid.

### Common completion

| # | Sender | Receiver | Message label | UML type |
|---:|---|---|---|---|
| 11 | Aafiatak Backend | Notification Service | `Send Patient/facility cancellation notification` | Solid request |
| 12 | Notification Service | Aafiatak Backend | `Notification accepted/result` | Dashed response |
| 13 | Aafiatak Backend | Patient Application | `Cancelled Appointment + independent refund/payment status` | Dashed response |
| 14 | Patient Application | Patient | `Display cancellation result` | Dashed response |

### Optional availability-alert continuation
Only when the returned seat becomes bookable and creates an approved zero-to-positive availability change:
- Backend identifies eligible subscriptions.
- Notification Service may send availability alerts.
- The alert does **not** reserve the seat or grant priority.

## 6. Critical Alternative / Failure Fragments

### A1 — `NON_REFUNDABLE`
- Cancellation may succeed if otherwise eligible.
- Refund due = zero.

### A2 — `REFUNDABLE_WITHIN_WINDOW` but refund window ended
- Cancellation may still succeed if self-cancellation timing still permits.
- Refund due = zero.

### A3 — `PAY_AT_FACILITY`
- Cancellation succeeds if eligible.
- No PaymentIntent and no electronic refund.

### A4 — Checked in OR ArrivalGroup window started
- Backend denies Patient self-cancellation.
- Arrival/late/no-show operational handling takes precedence.
- Appointment remains unchanged.

### A5 — Refund remains pending/delayed
- Appointment cancellation remains final.
- Payment refund status remains independent (`REFUND_PENDING`/review as applicable).

### A6 — Appointment already terminally cancelled
- Do not create another cancellation.
- Do not create duplicate refund.

## 7. Binding Domain Rules

- Use Appointment's saved cancellation policy/window; later configuration cannot rewrite it.
- Refund = full collected amount or zero only.
- Facility-responsible cancellation is different; it requires full refund when payment exists and is handled in operational-exception flow.
- Returned capacity goes to the **same ArrivalGroup** only.
- Returned numeric capacity is not necessarily bookable; release/group/time must permit a full new hold.
- A cancelled session/group does not silently re-offer capacity.
- Appointment and PaymentIntent status are independent.

## 8. Forbidden Content

Do not show:
- partial refund;
- refund percentage tiers;
- Patient self-cancellation after check-in/window start;
- seat moved to another ArrivalGroup;
- internal facility capacity imported into Aafiatak;
- Patient directly overwriting gateway state;
- deletion of cancelled Appointment/history;
- PAY_AT_FACILITY refund PaymentIntent.


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

- Pass 1: lecturer request/response chronology.
- Pass 2: Patient self-cancellation eligibility.
- Pass 3: saved policy/window precedence.
- Pass 4: full-or-zero refund rule.
- Pass 5: PAY_AT_FACILITY no-PaymentIntent rule.
- Pass 6: same-group seat return.
- Pass 7: returned-seat bookability conditions.
- Pass 8: Appointment/Payment lifecycle separation.
- Pass 9: duplicate cancellation/refund prevention.
- Pass 10: notification independence.
- Pass 11: history/audit preservation.
- Pass 12: final UCM-06 / MVP traceability.


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
