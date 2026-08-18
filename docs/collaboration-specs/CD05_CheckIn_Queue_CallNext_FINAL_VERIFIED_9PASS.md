# Collaboration Diagram — Patient Check-in, Queue & Call Next Patient

**Diagram ID:** `CD-05`  
**System:** Aafiatak Medical Appointment Booking System  
**Status:** FINAL VERIFIED — 9-PASS SOURCE-MATCHED SEMANTIC SPECIFICATION  
**Rendered language:** English only  
**Traceability:** UCM-10 + UCM-14; BRUC-17/18/19/21/22/23/24; DUC-06/07/08; SD-05; MVP arrival/queue scope

## Scenario Scope

One coherent service-day interaction: the Patient presents a booking identifier; facility staff validates the intended `CONFIRMED` Appointment and registers check-in; the system creates/activates `VisitInstance` and `QueueEntry` in the original ArrivalGroup; queue order is calculated; the Doctor views the assigned waiting context and calls the next eligible Patient. Corresponds to UCM-10 + UCM-14 / SD-05.

## Source Priority and Conflict Rule

Use this exact precedence:

1. `Aafiatak_Project_Specification_EN.md` at the repository root — **authoritative MVP/product truth**.
2. `Aafiatak_Use_Case_Modeling_AR_SUBMISSION_READY_VERIFIED(2).docx` — current reviewed Use Case Modeling supplied for this audit.
3. `Aafiatak_SD05_Checkin_Queue_Call_Next_FINAL_REVIEWED(1).md` — exact reviewed Sequence Diagram interaction baseline for this selected scenario.
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
2. Patient presents a valid booking identifier.
3. Intended Appointment is `CONFIRMED` and not cancelled.
4. Main path assumes normal arrival eligibility, not a late-arrival branch.
5. Doctor is authenticated and sees only the Doctor-assigned Aafiatak waiting context.

## Participants

| # | Participant | Role in this selected interaction |
|---:|---|---|
| 1 | `Patient` | Presents booking identifier and receives check-in/call information |
| 2 | `Booking & Reception Staff` | Searches Appointment and confirms arrival |
| 3 | `Facility Web Dashboard` | Staff interaction boundary |
| 4 | `Aafiatak Backend` | Validates Appointment, check-in, queue and Doctor-call rules |
| 5 | `Aafiatak Data Store` | Persists VisitInstance/QueueEntry and retrieves queue state |
| 6 | `Doctor Interface` | Doctor's limited waiting/call interface |
| 7 | `Doctor` | Views waiting list and calls next Patient |
| 8 | `Notification Service` | Sends independent check-in/turn notification when used |

## Structural Communication Links

| Link | Participant A | Participant B | Messages using this Link |
|---|---|---|---|
| L01 | `Aafiatak Backend` | `Aafiatak Data Store` | 4, 5, 10, 11, 12, 13, 20, 21, 25, 26 |
| L02 | `Aafiatak Backend` | `Doctor Interface` | 19, 22, 24, 27 |
| L03 | `Aafiatak Backend` | `Facility Web Dashboard` | 3, 7, 9, 14 |
| L04 | `Aafiatak Backend` | `Notification Service` | 15, 16, 28, 29 |
| L05 | `Booking & Reception Staff` | `Facility Web Dashboard` | 2, 8 |
| L06 | `Booking & Reception Staff` | `Patient` | 1 |
| L07 | `Doctor` | `Doctor Interface` | 18, 23 |
| L08 | `Notification Service` | `Patient` | 17, 30 |

A Link is structural and reusable. Do not create one parallel connector for every message between the same two participants.

## Ordered Messages — Binding

The message table below is the execution contract. Sender, receiver, label, and number must not be changed during rendering.

| # | Sender | Receiver | Exact message label |
|---:|---|---|---|
| 1 | `Patient` | `Booking & Reception Staff` | `Present booking number / phone / QR / verification code` |
| 2 | `Booking & Reception Staff` | `Facility Web Dashboard` | `Search or scan Appointment` |
| 3 | `Facility Web Dashboard` | `Aafiatak Backend` | `Find intended Appointment(identifier)` |
| 4 | `Aafiatak Backend` | `Aafiatak Data Store` | `Load Appointment + arrival context + existing VisitInstance` |
| 5 | `Aafiatak Data Store` | `Aafiatak Backend` | `Appointment/visit context` |
| 6 | `Aafiatak Backend` | `Aafiatak Backend` | `Validate facility + CONFIRMED + normal arrival eligibility` |
| 7 | `Aafiatak Backend` | `Facility Web Dashboard` | `Display valid Appointment for check-in` |
| 8 | `Booking & Reception Staff` | `Facility Web Dashboard` | `Confirm Patient arrival` |
| 9 | `Facility Web Dashboard` | `Aafiatak Backend` | `Register Patient check-in` |
| 10 | `Aafiatak Backend` | `Aafiatak Data Store` | `Atomic check-in: create VisitInstance if needed; set CHECKED_IN; record actual arrival; create/activate QueueEntry in original group` |
| 11 | `Aafiatak Data Store` | `Aafiatak Backend` | `Check-in and QueueEntry committed` |
| 12 | `Aafiatak Backend` | `Aafiatak Data Store` | `Calculate normal queue order by check-in time; confirmed_at tie-break` |
| 13 | `Aafiatak Data Store` | `Aafiatak Backend` | `Current waiting order / approximate Patient position` |
| 14 | `Aafiatak Backend` | `Facility Web Dashboard` | `Check-in complete` |
| 15 | `Aafiatak Backend` | `Notification Service` | `Send check-in confirmation / approaching-turn status when applicable` |
| 16 | `Notification Service` | `Aafiatak Backend` | `Notification accepted/result` |
| 17 | `Notification Service` | `Patient` | `Deliver check-in/queue notification` |
| 18 | `Doctor` | `Doctor Interface` | `View waiting Patients` |
| 19 | `Doctor Interface` | `Aafiatak Backend` | `Request Doctor-assigned waiting context` |
| 20 | `Aafiatak Backend` | `Aafiatak Data Store` | `Load callable QueueEntries using approved ordering` |
| 21 | `Aafiatak Data Store` | `Aafiatak Backend` | `Waiting list / callable entries` |
| 22 | `Aafiatak Backend` | `Doctor Interface` | `Display relevant waiting list` |
| 23 | `Doctor` | `Doctor Interface` | `Choose Call Next Patient` |
| 24 | `Doctor Interface` | `Aafiatak Backend` | `Call selected QueueEntry` |
| 25 | `Aafiatak Backend` | `Aafiatak Data Store` | `Revalidate callable state and set QueueEntry = CALLED` |
| 26 | `Aafiatak Data Store` | `Aafiatak Backend` | `Queue call recorded` |
| 27 | `Aafiatak Backend` | `Doctor Interface` | `Call confirmed` |
| 28 | `Aafiatak Backend` | `Notification Service` | `Send turn/call notification when applicable` |
| 29 | `Notification Service` | `Aafiatak Backend` | `Notification accepted/result` |
| 30 | `Notification Service` | `Patient` | `Notify Patient to proceed when applicable` |

## Self-Messages

- Message **6** — `Aafiatak Backend` self-message: `Validate facility + CONFIRMED + normal arrival eligibility`.

## Binding Domain / Lifecycle Invariants

- Patient cannot self-check-in; facility staff registers arrival.
- Appointment state remains independent from VisitInstance and QueueEntry.
- QueueEntry is created/activated only after valid or accepted-late facility check-in.
- Normal QueueEntry path is `WAITING -> CALLED -> DONE`; audited correction may produce `REMOVED`.
- Full payment grants no queue priority.
- Doctor may view/identify/call but may not set VisitInstance to IN_SERVICE/COMPLETED/NOT_COMPLETED/NO_SHOW.
- No automatic movement between ArrivalGroups.

## Success Postconditions

- VisitInstance is `CHECKED_IN` with actual arrival time.
- One QueueEntry exists in the original ArrivalGroup.
- Normal queue ordering uses actual check-in time, then `confirmed_at` as tie-breaker.
- Doctor call records QueueEntry `CALLED` when applicable.
- Doctor call does not change VisitInstance state.
- Patient may receive supported check-in/turn notification information.

## Explicitly Forbidden Interpretations

- Patient self-check-in.
- Appointment status `CHECKED_IN`.
- Doctor changing VisitInstance lifecycle state.
- Payment-based priority.
- Automatic late transfer/requeue/re-entry.
- Exposure of unrelated Patient private information.



## Nine-Pass Verification Record

1. **Lecturer-method pass:** verified against the lecturer's Collaboration example and Interaction-Diagram classification.
2. **Authority/scope pass:** checked against the root MVP; no deferred/open decision was invented.
3. **Use Case Modeling pass:** scenario, actor, preconditions, selected success path, and postconditions matched to the current reviewed UCM.
4. **Sequence pass:** participants and selected interaction messages were reconciled against `Aafiatak_SD05_Checkin_Queue_Call_Next_FINAL_REVIEWED(1).md`; any intentional deviation is documented explicitly in this file.
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
