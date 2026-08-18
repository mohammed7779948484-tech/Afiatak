# Collaboration Diagram — Book Appointment — FULL_PAYMENT_REQUIRED Success

**Diagram ID:** `CD-02`  
**System:** Aafiatak Medical Appointment Booking System  
**Status:** FINAL VERIFIED — 9-PASS SOURCE-MATCHED SEMANTIC SPECIFICATION  
**Rendered language:** English only  
**Traceability:** UCM-03 + UCM-04; PUC-11/12/13/21/22; SD-02 full-payment branch; MVP booking/payment scope

## Scenario Scope

Successful `FULL_PAYMENT_REQUIRED` booking from published Aafiatak capacity discovery through atomic `ReservationHold`, trusted full-payment verification, atomic `CONFIRMED` Appointment creation, and independent notification dispatch. This deliberately selects only the full-payment branch of UCM-03 + UCM-04 / SD-02; it does not represent `PAY_AT_FACILITY`.

## Source Priority and Conflict Rule

Use this exact precedence:

1. `Aafiatak_Project_Specification_EN.md` at the repository root — **authoritative MVP/product truth**.
2. `Aafiatak_Use_Case_Modeling_AR_SUBMISSION_READY_VERIFIED(2).docx` — current reviewed Use Case Modeling supplied for this audit.
3. `Aafiatak_SD02_Book_Appointment_FINAL_REVIEWED(1).md` — exact reviewed Sequence Diagram interaction baseline for this selected scenario.
4. Current repository Use Case Package, Class, and State semantic models — **cross-check only** for actor permissions, domain names, and lifecycle legality.
5. Lecturer UML handout, especially page 10 — Collaboration/Communication notation and presentation convention.
6. The practical UML rules supplied by the project owner.

If a lower-priority source conflicts with a higher-priority source, the higher-priority source wins. Never preserve an older diagram mistake merely for consistency.


## Lecturer-Mandated Collaboration / Communication Rules

The lecturer handout classifies **Sequence Diagram** and **Collaboration Diagram** together as **Interaction Diagrams**. The page-10 Collaboration example is the binding presentation reference for this deliverable.

1. The diagram shows **who communicates with whom**, not a vertical time axis.
2. Draw each participant as a simple object/participant rectangle.
3. Draw one reusable structural communication **Link** between every pair that communicates.
4. Put directional message arrows and numbered message labels on/near the relevant Link.
5. Number this selected concrete scenario with one global sequence `1, 2, 3, ...`, matching the lecturer's page-10 example. Do not reset numbering per Link.
6. Draw a self-message as a small loop on the same participant.
7. Do **not** use lifelines, activation bars, Sequence combined fragments, or the Sequence dashed-return convention.
8. Do **not** add Use Case ovals, `<<include>>`, `<<extend>>`, decision diamonds, Activity nodes, Class multiplicities, State nodes, Component nodes, or Deployment nodes.
9. The Data Store may appear as an **interaction object/participant**; it is not a Use Case actor.
10. Do not invent participants, technical services, messages, states, or implementation architecture.
11. All visible labels are English.
12. This file defines one concrete interaction scenario. Alternative/failure scenarios remain in Use Case Modeling/Activity/State models unless this file explicitly selects one.
13. Nested numbering such as `4.1` is valid UML, but is **not required for these six selected scenarios** because the lecturer's worked example uses a single global integer sequence and the reviewed Sequence baselines are already linearized.


## Preconditions

1. Patient is authenticated.
2. ServiceOffering is active.
3. A PUBLISHED AvailabilityRelease and currently bookable ArrivalGroup exist.
4. No prohibited overlapping ACTIVE hold or CONFIRMED Appointment exists.
5. The selected ServiceOffering policy is `FULL_PAYMENT_REQUIRED`.

## Participants

| # | Participant | Role in this selected interaction |
|---:|---|---|
| 1 | `Patient` | Selects context, confirms booking, completes payment when required |
| 2 | `Patient Application` | Presents availability/terms/countdown and submits actions |
| 3 | `Aafiatak Backend` | Enforces booking, hold, policy, payment, idempotency and atomic confirmation rules |
| 4 | `Aafiatak Data Store` | Reads/writes AvailabilityRelease, ArrivalGroup, ReservationHold, PaymentIntent, Appointment and snapshots transactionally |
| 5 | `Payment Gateway` | Processes and returns trusted full-payment result only in FULL_PAYMENT_REQUIRED |
| 6 | `Notification Service` | External notification-dispatch participant. In this selected SD-02 interaction it accepts booking-notification dispatch; no unsupported direct Notification Service → Patient message is invented. |

## Structural Communication Links

| Link | Participant A | Participant B | Messages using this Link |
|---|---|---|---|
| L01 | `Aafiatak Backend` | `Aafiatak Data Store` | 3, 4, 5, 6, 10, 11, 15, 16, 17, 18, 27, 28, 29, 30 |
| L02 | `Aafiatak Backend` | `Notification Service` | 31, 32 |
| L03 | `Aafiatak Backend` | `Patient Application` | 2, 7, 9, 12, 14, 21, 24, 33 |
| L04 | `Aafiatak Backend` | `Payment Gateway` | 19, 20, 25, 26 |
| L05 | `Patient` | `Patient Application` | 1, 8, 13, 34 |
| L06 | `Patient` | `Payment Gateway` | 22 |
| L07 | `Patient Application` | `Payment Gateway` | 23 |

A Link is structural and reusable. Do not create one parallel connector for every message between the same two participants.

## Ordered Messages — Binding

The message table below is the execution contract. Sender, receiver, label, and number must not be changed during rendering.

| # | Sender | Receiver | Exact message label |
|---:|---|---|---|
| 1 | `Patient` | `Patient Application` | `Select service / doctor context / day` |
| 2 | `Patient Application` | `Aafiatak Backend` | `Request currently bookable Aafiatak capacity` |
| 3 | `Aafiatak Backend` | `Aafiatak Data Store` | `Load PUBLISHED release + frozen booking terms` |
| 4 | `Aafiatak Data Store` | `Aafiatak Backend` | `Release terms and current capacity state` |
| 5 | `Aafiatak Backend` | `Aafiatak Data Store` | `Find earliest currently bookable ArrivalGroup` |
| 6 | `Aafiatak Data Store` | `Aafiatak Backend` | `Selected group/window + remaining capacity` |
| 7 | `Aafiatak Backend` | `Patient Application` | `Display arrival window and governing booking terms` |
| 8 | `Patient` | `Patient Application` | `Confirm intent to proceed` |
| 9 | `Patient Application` | `Aafiatak Backend` | `Create temporary ReservationHold` |
| 10 | `Aafiatak Backend` | `Aafiatak Data Store` | `Atomically revalidate group and acquire one ACTIVE hold` |
| 11 | `Aafiatak Data Store` | `Aafiatak Backend` | `Hold acquired: id + expiresAt + selected group` |
| 12 | `Aafiatak Backend` | `Patient Application` | `Show protected group and hold countdown` |
| 13 | `Patient` | `Patient Application` | `Proceed to full electronic payment` |
| 14 | `Patient Application` | `Aafiatak Backend` | `Start full payment for active hold` |
| 15 | `Aafiatak Backend` | `Aafiatak Data Store` | `Load hold/snapshot and enforce one non-terminal PaymentIntent` |
| 16 | `Aafiatak Data Store` | `Aafiatak Backend` | `Valid hold + amount/currency + PaymentIntent context` |
| 17 | `Aafiatak Backend` | `Aafiatak Data Store` | `Create or safely reuse PaymentIntent` |
| 18 | `Aafiatak Data Store` | `Aafiatak Backend` | `PaymentIntent ready` |
| 19 | `Aafiatak Backend` | `Payment Gateway` | `Initiate full amount payment` |
| 20 | `Payment Gateway` | `Aafiatak Backend` | `Gateway payment session/reference` |
| 21 | `Aafiatak Backend` | `Patient Application` | `Continue approved gateway interaction` |
| 22 | `Patient` | `Payment Gateway` | `Complete gateway payment interaction` |
| 23 | `Payment Gateway` | `Patient Application` | `Return to application` |
| 24 | `Patient Application` | `Aafiatak Backend` | `Report client return from gateway` |
| 25 | `Aafiatak Backend` | `Payment Gateway` | `Verify payment through trusted gateway channel` |
| 26 | `Payment Gateway` | `Aafiatak Backend` | `Trusted payment result: SUCCESS` |
| 27 | `Aafiatak Backend` | `Aafiatak Data Store` | `Persist SUCCEEDED and atomically revalidate hold/release/group/time` |
| 28 | `Aafiatak Data Store` | `Aafiatak Backend` | `Payment persisted; booking target still eligible` |
| 29 | `Aafiatak Backend` | `Aafiatak Data Store` | `Atomic commit: consume hold/capacity once + create CONFIRMED Appointment snapshot` |
| 30 | `Aafiatak Data Store` | `Aafiatak Backend` | `Appointment confirmed; hold CONSUMED` |
| 31 | `Aafiatak Backend` | `Notification Service` | `Send full-payment booking confirmation` |
| 32 | `Notification Service` | `Aafiatak Backend` | `Notification accepted/result` |
| 33 | `Aafiatak Backend` | `Patient Application` | `Confirmed Appointment + independent SUCCEEDED payment status` |
| 34 | `Patient Application` | `Patient` | `Display confirmation / receipt summary / arrival window` |

## Self-Messages

None in this selected scenario.

## Binding Domain / Lifecycle Invariants

- The system allocates the earliest currently bookable ArrivalGroup; Patient does not arbitrarily select a later group.
- ReservationHold protects exactly one unit and prevents last-seat double booking.
- Client/browser gateway return is not financial truth.
- Only trusted gateway verification may establish `SUCCEEDED`.
- PaymentIntent, ReservationHold, and Appointment lifecycles remain independent.
- No partial payment or remaining balance exists.
- Notification dispatch happens only after the core booking transaction and cannot rewrite booking/payment truth.

## Success Postconditions

- Exactly one Appointment is `CONFIRMED`.
- ReservationHold becomes `CONSUMED`.
- Exactly one capacity unit is consumed.
- PaymentIntent is `SUCCEEDED` from trusted gateway truth.
- Appointment preserves the required booking/financial/arrival snapshot.
- Patient sees the confirmed booking, payment status, receipt summary, and arrival window.

## Explicitly Forbidden Interpretations

- `PAY_AT_FACILITY` branch in this diagram.
- Manual facility booking approval.
- Deposit/partial payment.
- Appointment confirmation from client/browser return alone.
- Payment-based queue priority.
- Duplicate hold, PaymentIntent, Appointment, or capacity consumption on retry.



## Nine-Pass Verification Record

1. **Lecturer-method pass:** verified against the lecturer's Collaboration example and Interaction-Diagram classification.
2. **Authority/scope pass:** checked against the root MVP; no deferred/open decision was invented.
3. **Use Case Modeling pass:** scenario, actor, preconditions, selected success path, and postconditions matched to the current reviewed UCM.
4. **Sequence pass:** participants and selected interaction messages were reconciled against `Aafiatak_SD02_Book_Appointment_FINAL_REVIEWED(1).md`; any intentional deviation is documented explicitly in this file.
5. **Use Case Package / permission pass:** actor responsibilities were checked against the current repository actor-package Use Case models.
6. **Class/domain pass:** domain terminology and entity responsibility were checked against the current Class model.
7. **State/lifecycle pass:** ReservationHold / Appointment / PaymentIntent / VisitInstance / QueueEntry transitions used here were checked against the current State models where applicable.
8. **Communication-structure pass:** message numbering, sender/receiver existence, Link coverage, self-messages, and duplicate/missing communication pairs were machine-validated.
9. **Adversarial cross-diagram pass:** checked for hidden partial payment/refund, state leakage, forbidden role expansion, reverse capacity flow, invented notification channel, and contradictions with the other five Collaboration scenarios.

## Final Rendering QA Gate

Before a rendered Collaboration Diagram is accepted:

- Every participant in this file exists exactly once.
- Every structural Link listed here exists.
- Every message appears exactly once with the exact number, sender, receiver, and label.
- Messages use the correct reusable Link.
- Self-messages are loops on the correct participant.
- No lifelines or activation bars appear.
- No Sequence `alt/opt/loop` frame appears.
- No Use Case / Activity / State / Class notation is mixed in.
- No new participant or message is invented for visual convenience.
- Diagram remains readable at normal report zoom.
- Final status remains `awaiting-user-approval` until human visual review.
