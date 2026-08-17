# Activity Diagram — Book Appointment
## Aafiatak Medical Appointment Booking System — MVP Activity Diagram Specification

**Diagram ID:** `AD-03`  
**Deliverable:** UML Activity Diagram  
**Use Case:** `Book Appointment`  
**Traceability:** UCM-03; MUC-06/PUC-11; Project Specification §§13.3–16.5, 19  
**Package:** Patient Package  
**Visible language:** English only  
**Scope:** Current approved MVP critical-Use-Case set  
**Semantic status:** FINAL VERIFIED v2 — lecturer-aligned and source-matched — ready for execution

---


## 1. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative current MVP product truth.
2. Lecturer UML PDF + lecturer-course rules supplied by the project owner — academic Activity Diagram method and notation.
3. `Aafiatak_Critical_Use_Case_Modeling_FINAL_15-Pass_Reviewed_v2` — scenario, actor, precondition, alternative/failure, and postcondition truth for the selected critical Use Case.
4. Reviewed State/Sequence/Class work — consistency checks only; they must not override the MVP or UCM.
5. This file — exact execution contract for this Activity Diagram.
6. Rendering/tooling — presentation mechanics only.

If a branch, action, condition, state change, or outcome is not supported by the authoritative sources, do not invent it.

All visible diagram labels must be **English**.

## 2. Lecturer Activity-Diagram Rules Applied

### What the lecturer material actually supports

The lecturer PDF lists the diagram as `Activate Diagram` on page 2 and gives the heading `9. Activate Diagram.` on page 11. The available PDF page 11 does **not** contain a readable worked Activity-Diagram example below that heading. Therefore, no pixel-for-pixel reconstruction of a missing lecturer figure is claimed.

The lecturer-course rules supplied for this project explicitly define the Activity Diagram as the diagram that shows **how a process is executed step by step**, and state that an independent Activity Diagram is prepared for a Use Case. The supplied rules identify these core elements:

- Initial Node
- Activity / Action
- Decision
- Merge
- Fork
- Join
- Final Node
- Control Flow
- Object Flow

They also state that Activity Diagram relationships are flow relationships and must **not** use Association, Generalization, or Aggregation.

### Mandatory lecturer-style notation

- **Initial Node:** one filled black circle.
- **Action / Activity:** rounded rectangle, concise verb-led label.
- **Decision Node:** diamond with one incoming flow and multiple guarded outgoing flows.
- **Merge Node:** diamond used only to reunite alternative paths.
- **Fork / Join:** thick bar only when true parallel/concurrent activity is explicitly supported. Do not add one for decoration.
- **Final Node:** UML Activity Final (bullseye).
- **Control Flow:** solid directed arrow.
- **Object Flow:** use only when a data/object transfer itself materially improves the diagram and is source-supported.
- **Guard:** write on outgoing Decision flows in square brackets, for example `[Valid]`, `[No capacity]`, `[FULL_PAYMENT_REQUIRED]`.

### Simplicity rule

The lecturer warns against both overly short and excessively detailed scenario steps. Therefore:

- represent meaningful business/system activities;
- do not convert every UI click, database query, API call, or implementation detail into an Activity;
- do not add Sequence lifelines/messages;
- do not add Use Case ellipses/`<<include>>`/`<<extend>>`;
- do not add Class relationships;
- do not add State-machine notation;
- do not invent swimlanes: swimlanes were not part of the supplied lecturer Activity-Diagram rules for this assignment.

## 3. Diagram-Wide Drawing Contract

- One Use Case / coherent Activity workflow per page/artboard.
- One Initial Node and one final Activity Final unless this file explicitly says otherwise.
- Main success path must be visually dominant.
- Important source-supported alternatives/failures are shown with Decision/Merge branches.
- Small retry/idempotency rules that do not change the business goal may remain as a compact UML Note rather than creating a visually noisy loop, when this file says so.
- No Actors/stick figures inside the Activity Diagram.
- Actor names may appear inside action labels only when necessary to show responsibility, e.g. `Patient confirms cancellation`.
- No system boundary.
- No numbered Sequence messages.
- No legend unless specifically required (none is required in this set).
- Use Control Flow arrows throughout unless an Object Flow is explicitly defined.

## 4. Visual Contract

- Formal university-report style.
- White/light-neutral background.
- Dark navy/charcoal text and control-flow arrows.
- Restrained accent only for Start/End or decision emphasis if needed.
- Exact title at the top.
- Main path generally top-to-bottom.
- Keep Decision/Merge diamonds aligned with the branch they control.
- Place guard labels next to the correct outgoing edge; never in ambiguous empty space.
- Avoid crossings, clipped text, tiny labels, and excessive blank areas.
- Keep action labels concise enough to be read at normal PDF/report zoom.

## 5. Generic Forbidden Content

Do not add:

- screens/pages as architectural participants;
- controllers, repositories, microservices, event buses, APIs, SQL/database calls;
- clinical diagnosis, prescriptions, test results, medical notes;
- SMS/password fallback;
- partial payment or partial refund;
- manual booking approval states;
- hidden capacity increase or reverse CapacityWithdrawal;
- any status that belongs to another lifecycle.


## 6. Preconditions

1. Patient is authenticated.
2. Selected ServiceOffering and facility/branch context are valid/active.
3. A published AvailabilityRelease exists for the selected service/day.
4. Patient has no prohibited overlapping active hold/confirmed Appointment.

## 7. Exact Node Inventory

The renderer must implement exactly the following semantic nodes. It may wrap text or adjust geometry, but must not rename, omit, merge, or invent business actions.

- `I` — **Initial Node:** Start
- `A01` — **Action:** Patient selects service / doctor context and day
- `D00` — **Decision:** Conflicting overlapping ACTIVE ReservationHold or CONFIRMED Appointment exists?
- `A00` — **Action:** Reject conflicting new booking attempt; preserve existing booking/hold
- `A02` — **Action:** Find earliest currently bookable ArrivalGroup
- `D01` — **Decision:** Currently bookable ArrivalGroup available?
- `A03` — **Action:** Offer Notify Me When Available; create no hold
- `A04` — **Action:** Display arrival window and governing snapshotted terms
- `A05` — **Action:** Patient confirms intent to proceed
- `A06` — **Action:** Atomically acquire one ACTIVE ReservationHold and start countdown
- `D02` — **Decision:** Hold acquisition succeeded?
- `A07` — **Action:** Report capacity full / temporarily held; create no Appointment
- `D03` — **Decision:** Governing booking policy?
- `A08` — **Action:** Patient completes final booking information and accepts payment due at facility
- `A09` — **Action:** Revalidate hold, release, group and time eligibility
- `D04` — **Decision:** Hold / target still eligible?
- `A10` — **Action:** Expire or release hold; create no Appointment
- `A11` — **Action:** Atomically consume hold and create one CONFIRMED Appointment
- `A12` — **Action:** Display booking confirmation and payment due at facility
- `A13` — **Action:** Run Process Full Payment activity for full snapshotted amount
- `D05` — **Decision:** Trusted full-payment result supports confirmation while target remains eligible?
- `A14` — **Action:** Do not create conflicting Appointment; follow payment recovery/refund/UNDER_REVIEW rules
- `A15` — **Action:** Atomically consume hold and create one CONFIRMED Appointment with booking snapshot
- `A16` — **Action:** Display confirmed Appointment and paid payment state separately
- `MEND` — **Merge:** End-path merge
- `F` — **Final Node:** End

## 8. Exact Control-Flow / Edge Table

| From | To | Guard | Meaning / rendering instruction |
|---|---|---|---|
| `I` | `A01` | — | Begin booking |
| `A01` | `D00` | — | Check overlap boundary |
| `D00` | `A00` | [Yes] | UCM overlapping-booking failure boundary |
| `A00` | `MEND` | — | No conflicting booking created |
| `D00` | `A02` | [No] | Continue capacity allocation |
| `A02` | `D01` | — | Evaluate availability |
| `D01` | `A03` | [No] | No capacity path |
| `A03` | `MEND` | — | No booking created |
| `D01` | `A04` | [Yes] | Show proposed group/terms |
| `A04` | `A05` | — | Patient reviews/accepts |
| `A05` | `A06` | — | Atomic last-seat protection |
| `A06` | `D02` | — | Check hold acquisition |
| `D02` | `A07` | [Failed / concurrent winner] | No double booking |
| `A07` | `MEND` | — | End concurrency failure |
| `D02` | `D03` | [Succeeded] | Branch by authoritative policy |
| `D03` | `A08` | [PAY_AT_FACILITY] | No PaymentIntent path |
| `A08` | `A09` | — | Final revalidation |
| `A09` | `D04` | — | Eligibility decision |
| `D04` | `A10` | [Invalid / expired / started / cancelled] | No Appointment |
| `A10` | `MEND` | — | End invalid-target path |
| `D04` | `A11` | [Valid] | Confirm pay-at-facility booking |
| `A11` | `A12` | — | Show success |
| `A12` | `MEND` | — | Pay-at-facility success ends |
| `D03` | `A13` | [FULL_PAYMENT_REQUIRED] | Invoke payment workflow |
| `A13` | `D05` | — | Evaluate trusted payment/booking result |
| `D05` | `A14` | [No] | Critical-payment handling; no conflicting Appointment |
| `A14` | `MEND` | — | Payment recovery branch ends/continues outside booking |
| `D05` | `A15` | [Yes] | Atomic confirmation |
| `A15` | `A16` | — | Show success |
| `A16` | `MEND` | — | Full-payment success ends |
| `MEND` | `F` | — | Activity final |

## 9. Branch Semantics

### No capacity
Notify Me is optional recovery and never reserves/guarantees a seat.

### Last-seat race
Atomic ReservationHold acquisition decides ownership; the losing request creates no hold/Appointment.

### Policy split
Exactly two branches exist: `PAY_AT_FACILITY` and `FULL_PAYMENT_REQUIRED`.

### Hold invalidation
An expired/released hold, started ArrivalGroup, or CANCELLED parent release cannot create a conflicting Appointment.

### Overlapping booking boundary
If the Patient already has an overlapping ACTIVE ReservationHold or CONFIRMED Appointment, reject the conflicting new booking attempt. The only exception is the controlled atomic rescheduling operation defined separately.

### Client retry
Idempotency must return the existing result instead of duplicating capacity or Appointment creation; keep as compact note near atomic confirmation.


## 10. Binding Business Rules

- Patient does not choose arbitrary ArrivalGroup; system uses earliest currently bookable group.
- One booking action protects/consumes one capacity unit.
- PAY_AT_FACILITY creates no PaymentIntent.
- FULL_PAYMENT_REQUIRED confirms only from trusted payment success while booking target remains valid.
- Arrival window is not an exact doctor-entry time.

## 11. Explicitly Forbidden in This Diagram

- Deposit/partial payment.
- Manual facility approval/pending approval.
- Arbitrary group selection.
- Duplicate Appointment or hold on retry.
- Exact unresolved ReservationHold default duration.

## 12. Review Record

- Pass 1: lecturer Activity structure
- Pass 2: UCM-03 S1/S2
- Pass 3: earliest group rule
- Pass 4: capacity Decision
- Pass 5: atomic hold race
- Pass 6: two-policy branch
- Pass 7: pay-at-facility no PaymentIntent
- Pass 8: trusted-payment boundary
- Pass 9: target revalidation
- Pass 10: idempotency
- Pass 11: state separation
- Pass 12: no manual approval
- Pass 13: no partial payment
- Pass 14: branch readability
- Pass 15: final cross-check



## Final Source-Match Re-Audit v2

This specification was re-audited against:
- lecturer UML PDF Activity-diagram references;
- lecturer-course Activity rules supplied for this project;
- the corresponding scenario(s) in `Aafiatak_Critical_Use_Case_Modeling_FINAL_15-Pass_Reviewed_v2`;
- the current root `Aafiatak_Project_Specification_EN.md`.

The diagram renderer must treat the project specification as higher authority if any older artifact conflicts with it.

## Mandatory QA Gates

Before delivery:

1. Verify the exact Use Case title and scope.
2. Verify the Initial Node exists and has no incoming flow.
3. Verify the Activity Final exists and has no outgoing flow.
4. Verify every Action is source-supported and verb-led.
5. Verify every Decision has meaningful guarded outgoing flows.
6. Verify every Merge is used only to reunite alternatives, not as decoration.
7. Verify Fork/Join is absent unless true parallelism is explicitly required.
8. Verify all arrows are Control Flows unless an Object Flow is explicitly specified.
9. Verify no Association/Generalization/Aggregation/Use-Case relationship appears.
10. Verify no Sequence lifeline/message notation appears.
11. Verify actor permissions and product boundaries.
12. Verify independent lifecycle states are not collapsed into one generic status.
13. Verify all rendered branch guards are mutually understandable and not contradictory.
14. Render SVG/PNG/PDF; open every actual output and inspect it visually.
15. Compare the render against this MD item-by-item and correct semantic, notation, routing, and readability issues.
16. Final status must be `awaiting-user-approval`.
