# Collaboration Diagram — Reschedule Appointment

**Diagram ID:** `CD-04`  
**System:** Aafiatak Medical Appointment Booking System  
**Status:** FINAL VERIFIED — 9-PASS SOURCE-MATCHED SEMANTIC SPECIFICATION  
**Rendered language:** English only  
**Traceability:** UCM-09; BRUC-15; SD-04; MVP rescheduling scope

## Scenario Scope

Successful controlled in-place rescheduling of one existing `CONFIRMED` Appointment **after prior Patient communication/agreement**, to valid new capacity for the same `ServiceOffering` under the same saved financial/booking terms. Corresponds to UCM-09 / SD-04.

## Source Priority and Conflict Rule

Use this exact precedence:

1. `Aafiatak_Project_Specification_EN.md` at the repository root — **authoritative MVP/product truth**.
2. `Aafiatak_Use_Case_Modeling_AR_SUBMISSION_READY_VERIFIED(2).docx` — current reviewed Use Case Modeling supplied for this audit.
3. `Aafiatak_SD04_Reschedule_Appointment_FINAL_REVIEWED(1).md` — exact reviewed Sequence Diagram interaction baseline for this selected scenario.
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

1. Booking & Reception Staff is authenticated/authorized.
2. Appointment is `CONFIRMED`.
3. Patient and facility have already communicated and agreed to the change.
4. Destination uses the same ServiceOffering and same saved terms.
5. Valid destination capacity is currently bookable.

## Participants

| # | Participant | Role in this selected interaction |
|---:|---|---|
| 1 | `Booking & Reception Staff` | Selects agreed destination and confirms reason |
| 2 | `Facility Web Dashboard` | Shows Appointment/history and submits reschedule |
| 3 | `Aafiatak Backend` | Validates terms and performs atomic move |
| 4 | `Aafiatak Data Store` | Locks/validates capacity, updates Appointment, writes history |
| 5 | `Notification Service` | Sends independent appointment-change notification |
| 6 | `Patient` | Receives final change notification / is party to prior agreement |

## Structural Communication Links

| Link | Participant A | Participant B | Messages using this Link |
|---|---|---|---|
| L01 | `Aafiatak Backend` | `Aafiatak Data Store` | 3, 4, 8, 9, 13, 14 |
| L02 | `Aafiatak Backend` | `Facility Web Dashboard` | 2, 5, 7, 10, 12, 18 |
| L03 | `Aafiatak Backend` | `Notification Service` | 15, 16 |
| L04 | `Booking & Reception Staff` | `Facility Web Dashboard` | 1, 6, 11 |
| L05 | `Notification Service` | `Patient` | 17 |

A Link is structural and reusable. Do not create one parallel connector for every message between the same two participants.

## Ordered Messages — Binding

The message table below is the execution contract. Sender, receiver, label, and number must not be changed during rendering.

| # | Sender | Receiver | Exact message label |
|---:|---|---|---|
| 1 | `Booking & Reception Staff` | `Facility Web Dashboard` | `Open CONFIRMED Appointment and choose Reschedule` |
| 2 | `Facility Web Dashboard` | `Aafiatak Backend` | `Load reschedule context` |
| 3 | `Aafiatak Backend` | `Aafiatak Data Store` | `Read Appointment snapshot/history/current capacity` |
| 4 | `Aafiatak Data Store` | `Aafiatak Backend` | `Current booking and governing terms` |
| 5 | `Aafiatak Backend` | `Facility Web Dashboard` | `Display current snapshot and permitted destination context` |
| 6 | `Booking & Reception Staff` | `Facility Web Dashboard` | `Select agreed new day/group/session` |
| 7 | `Facility Web Dashboard` | `Aafiatak Backend` | `Validate destination` |
| 8 | `Aafiatak Backend` | `Aafiatak Data Store` | `Check same ServiceOffering/terms + current destination bookability` |
| 9 | `Aafiatak Data Store` | `Aafiatak Backend` | `Destination valid and currently bookable` |
| 10 | `Aafiatak Backend` | `Facility Web Dashboard` | `Display valid proposed move` |
| 11 | `Booking & Reception Staff` | `Facility Web Dashboard` | `Confirm reschedule and record reason` |
| 12 | `Facility Web Dashboard` | `Aafiatak Backend` | `Commit reschedule` |
| 13 | `Aafiatak Backend` | `Aafiatak Data Store` | `Atomic transaction: secure destination first; update schedule/group; release old seat after secure; write history` |
| 14 | `Aafiatak Data Store` | `Aafiatak Backend` | `Reschedule committed; Appointment remains CONFIRMED` |
| 15 | `Aafiatak Backend` | `Notification Service` | `Send appointment-change notification` |
| 16 | `Notification Service` | `Aafiatak Backend` | `Notification accepted/result` |
| 17 | `Notification Service` | `Patient` | `Deliver new agreed arrival details` |
| 18 | `Aafiatak Backend` | `Facility Web Dashboard` | `Display successful reschedule` |

## Self-Messages

None in this selected scenario.

## Binding Domain / Lifecycle Invariants

- Secure destination capacity first; release old capacity only after successful destination acquisition.
- Rescheduling does not create a `RESCHEDULED` Appointment state.
- Different ServiceOffering/price/policy requires cancellation + normal new booking, not in-place reschedule.
- No automatic late-arrival transfer.
- No top-up, partial refund, or mixed financial adjustment is invented.

## Success Postconditions

- Appointment remains `CONFIRMED`.
- Destination scheduling/group details are stored.
- Destination capacity is secured before old capacity is released.
- Old/new scheduling data, actor, and reason are preserved in history.
- Financial/booking snapshot remains unchanged.
- Patient receives the agreed updated arrival details through the supported notification interaction.

## Explicitly Forbidden Interpretations

- Releasing the old seat before the new seat is secured.
- `RESCHEDULED` as a new Appointment status.
- Changing saved price/policy in place.
- Automatic movement of a late Patient.
- Rescheduling without prior Patient communication/agreement.



## Nine-Pass Verification Record

1. **Lecturer-method pass:** verified against the lecturer's Collaboration example and Interaction-Diagram classification.
2. **Authority/scope pass:** checked against the root MVP; no deferred/open decision was invented.
3. **Use Case Modeling pass:** scenario, actor, preconditions, selected success path, and postconditions matched to the current reviewed UCM.
4. **Sequence pass:** participants and selected interaction messages were reconciled against `Aafiatak_SD04_Reschedule_Appointment_FINAL_REVIEWED(1).md`; any intentional deviation is documented explicitly in this file.
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
