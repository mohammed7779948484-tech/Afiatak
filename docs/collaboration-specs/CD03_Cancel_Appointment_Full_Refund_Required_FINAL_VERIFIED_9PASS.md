# Collaboration Diagram — Cancel Appointment — Full Refund Required

**Diagram ID:** `CD-03`  
**System:** Aafiatak Medical Appointment Booking System  
**Status:** FINAL VERIFIED — 9-PASS SOURCE-MATCHED SEMANTIC SPECIFICATION  
**Rendered language:** English only  
**Traceability:** UCM-06; PUC-19; SD-03 full-refund-required branch; MVP cancellation/refund scope

## Scenario Scope

Successful Patient self-cancellation of the Patient's own eligible `CONFIRMED` fully paid Appointment where the Appointment's saved cancellation policy requires a **full refund**. The selected interaction shows cancellation and initiation/persistence of the full-refund lifecycle; the refund may be `REFUND_PENDING`, `REFUNDED`, or require review depending on the trusted gateway result. Zero-refund and `PAY_AT_FACILITY` outcomes are outside this concrete Collaboration scenario.

## Source Priority and Conflict Rule

Use this exact precedence:

1. `Aafiatak_Project_Specification_EN.md` at the repository root — **authoritative MVP/product truth**.
2. `Aafiatak_Use_Case_Modeling_AR_SUBMISSION_READY_VERIFIED(2).docx` — current reviewed Use Case Modeling supplied for this audit.
3. `Aafiatak_SD03_Cancel_Appointment_Refund_FINAL_REVIEWED(1).md` — exact reviewed Sequence Diagram interaction baseline for this selected scenario.
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

1. Patient is authenticated and owns the Appointment.
2. Appointment is `CONFIRMED`.
3. Patient has not checked in.
4. Assigned ArrivalGroup window has not started.
5. The Appointment is fully paid and its saved cancellation policy yields a full refund in this selected scenario.

## Participants

| # | Participant | Role in this selected interaction |
|---:|---|---|
| 1 | `Patient` | Reviews and confirms cancellation |
| 2 | `Patient Application` | Displays cancellation/refund consequence and status |
| 3 | `Aafiatak Backend` | Revalidates eligibility, applies saved policy, orchestrates cancellation |
| 4 | `Aafiatak Data Store` | Persists Appointment/history, capacity and PaymentIntent refund state |
| 5 | `Payment Gateway` | Executes full refund only when required |
| 6 | `Notification Service` | External cancellation-notification dispatch participant. This selected SD-03 interaction records dispatch acceptance but does not invent a direct notification-delivery message to Patient. |

## Structural Communication Links

| Link | Participant A | Participant B | Messages using this Link |
|---|---|---|---|
| L01 | `Aafiatak Backend` | `Aafiatak Data Store` | 3, 4, 9, 10, 13, 14 |
| L02 | `Aafiatak Backend` | `Notification Service` | 15, 16 |
| L03 | `Aafiatak Backend` | `Patient Application` | 2, 6, 8, 17 |
| L04 | `Aafiatak Backend` | `Payment Gateway` | 11, 12 |
| L05 | `Patient` | `Patient Application` | 1, 7, 18 |

A Link is structural and reusable. Do not create one parallel connector for every message between the same two participants.

## Ordered Messages — Binding

The message table below is the execution contract. Sender, receiver, label, and number must not be changed during rendering.

| # | Sender | Receiver | Exact message label |
|---:|---|---|---|
| 1 | `Patient` | `Patient Application` | `Open confirmed Appointment and choose Cancel` |
| 2 | `Patient Application` | `Aafiatak Backend` | `Request cancellation consequence(appointmentId)` |
| 3 | `Aafiatak Backend` | `Aafiatak Data Store` | `Load Appointment snapshot + payment + check-in + group timing` |
| 4 | `Aafiatak Data Store` | `Aafiatak Backend` | `Saved policy / payment / eligibility context` |
| 5 | `Aafiatak Backend` | `Aafiatak Backend` | `Validate ownership, CONFIRMED, not checked-in, group not started` |
| 6 | `Aafiatak Backend` | `Patient Application` | `Display cancellation allowed + expected refund: FULL or ZERO` |
| 7 | `Patient` | `Patient Application` | `Confirm cancellation` |
| 8 | `Patient Application` | `Aafiatak Backend` | `Cancel Appointment` |
| 9 | `Aafiatak Backend` | `Aafiatak Data Store` | `Atomic revalidation + set CANCELLED_BY_PATIENT + write history + release same-group capacity when eligible` |
| 10 | `Aafiatak Data Store` | `Aafiatak Backend` | `Cancellation committed + refund decision + capacity result` |
| 11 | `Aafiatak Backend` | `Payment Gateway` | `Initiate full collected-amount refund` |
| 12 | `Payment Gateway` | `Aafiatak Backend` | `Refund result / pending reference` |
| 13 | `Aafiatak Backend` | `Aafiatak Data Store` | `Persist REFUND_PENDING / REFUNDED / review status` |
| 14 | `Aafiatak Data Store` | `Aafiatak Backend` | `Payment refund state saved` |
| 15 | `Aafiatak Backend` | `Notification Service` | `Send Patient/facility cancellation notification` |
| 16 | `Notification Service` | `Aafiatak Backend` | `Notification accepted/result` |
| 17 | `Aafiatak Backend` | `Patient Application` | `Cancelled Appointment + independent refund/payment status` |
| 18 | `Patient Application` | `Patient` | `Display cancellation result` |

## Self-Messages

- Message **5** — `Aafiatak Backend` self-message: `Validate ownership, CONFIRMED, not checked-in, group not started`.

## Binding Domain / Lifecycle Invariants

- Patient-cancellation eligibility is revalidated immediately before commit.
- Appointment cancellation and PaymentIntent refund are independent lifecycles.
- Refund is either the full collected amount or zero; no partial refund exists.
- The saved Appointment policy/window governs; later ServiceOffering policy changes do not rewrite this booking.
- Same-group capacity return does not mean it is automatically bookable; release/group/time eligibility still governs.
- Notification dispatch is independent of cancellation/refund truth.

## Success Postconditions

- Appointment is `CANCELLED_BY_PATIENT`.
- Cancellation/history is preserved.
- Capacity returns only to the same ArrivalGroup and is bookable only when release/group/time rules permit.
- A full collected-amount refund lifecycle is initiated and its independent status is persisted.
- Cancellation remains final even if refund settlement remains pending/reviewed.

## Explicitly Forbidden Interpretations

- Partial refund.
- Cancellation after valid check-in or after the assigned group window starts.
- Returning capacity to another ArrivalGroup.
- Reversing Appointment cancellation because refund is delayed.
- Treating notification success/failure as refund truth.
- Claiming the refund is necessarily settled merely because it was initiated.



## Nine-Pass Verification Record

1. **Lecturer-method pass:** verified against the lecturer's Collaboration example and Interaction-Diagram classification.
2. **Authority/scope pass:** checked against the root MVP; no deferred/open decision was invented.
3. **Use Case Modeling pass:** scenario, actor, preconditions, selected success path, and postconditions matched to the current reviewed UCM.
4. **Sequence pass:** participants and selected interaction messages were reconciled against `Aafiatak_SD03_Cancel_Appointment_Refund_FINAL_REVIEWED(1).md`; any intentional deviation is documented explicitly in this file.
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
