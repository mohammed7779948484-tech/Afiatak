# Collaboration Diagram — Resolve Operational Exception — Facility Cancellation & Full-Refund Initiation

**Diagram ID:** `CD-06`  
**System:** Aafiatak Medical Appointment Booking System  
**Status:** FINAL VERIFIED — 9-PASS SOURCE-MATCHED SEMANTIC SPECIFICATION  
**Rendered language:** English only  
**Traceability:** UCM-13; BRUC-38/39/42/43 + facility cancellation/refund rules; SD-06 branch-B intent with plural/singular ambiguity corrected by higher-priority MVP/UCM; MVP §§23–24

## Scenario Scope

Concrete UCM-13 `CONFLICT_DETECTED` scenario with **exactly one affected CONFIRMED, fully paid Appointment**. The selected authorized facility actor records the conflict, resolves that Appointment through `CANCELLED_BY_FACILITY`, initiates the required full-refund lifecycle, notifies the affected Patient, and closes the OperationalException only after the Appointment has a completed documented resolution outcome.

This deliberate one-Appointment scope fixes the ambiguity in SD-06, whose general prefix retrieves a plural affected set while a single rendered branch can otherwise appear to process only one Appointment before closure. The generic UCM-13 rule remains: if more than one Appointment is affected, **every one** must receive a documented completed resolution before closure.

## Source Priority and Conflict Rule

Use this exact precedence:

1. `Aafiatak_Project_Specification_EN.md` at the repository root — **authoritative MVP/product truth**.
2. `Aafiatak_Use_Case_Modeling_AR_SUBMISSION_READY_VERIFIED(2).docx` — current reviewed Use Case Modeling supplied for this audit.
3. `Aafiatak_SD06_Operational_Exception_FINAL_REVIEWED(1).md` — exact reviewed Sequence Diagram interaction baseline for this selected scenario.
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

1. Booking & Reception Staff is authenticated/authorized for the facility.
2. A supported `CONFLICT_DETECTED` event exists after confirmation.
3. This selected concrete scenario contains exactly one affected `CONFIRMED` Appointment.
4. That Appointment has a collected full electronic payment.
5. Facility-side cancellation is the selected approved resolution path.

## Participants

| # | Participant | Role in this selected interaction |
|---:|---|---|
| 1 | `Booking & Reception Staff` | Selected authorized facility actor for this concrete daily-operations scenario. Facility Administrator is also authorized by UCM-13/MVP but is intentionally omitted from this one concrete interaction. |
| 2 | `Facility Web Dashboard` | Facility-side operational-exception interaction boundary. |
| 3 | `Aafiatak Backend` | Orchestrates exception, facility cancellation, refund initiation/status persistence, notification dispatch, and closure gate. |
| 4 | `Aafiatak Data Store` | Persists OperationalException, the affected Appointment resolution/history, independent refund status, and audit trail. |
| 5 | `Notification Service` | Delivers the affected-Patient operational notification in this selected interaction. |
| 6 | `Patient` | The single affected Patient receiving the facility-cancellation/resolution information. |
| 7 | `Payment Gateway` | Executes the full-refund lifecycle for the already collected full payment. |

## Structural Communication Links

| Link | Participant A | Participant B | Messages using this Link |
|---|---|---|---|
| L01 | `Aafiatak Backend` | `Aafiatak Data Store` | 3, 4, 5, 6, 10, 11, 14, 15, 21, 22, 23, 24 |
| L02 | `Aafiatak Backend` | `Facility Web Dashboard` | 2, 7, 9, 20, 25 |
| L03 | `Aafiatak Backend` | `Notification Service` | 16, 17 |
| L04 | `Aafiatak Backend` | `Payment Gateway` | 12, 13 |
| L05 | `Booking & Reception Staff` | `Facility Web Dashboard` | 1, 8, 19 |
| L06 | `Notification Service` | `Patient` | 18 |

A Link is structural and reusable. Do not create one parallel connector for every message between the same two participants.

## Ordered Messages — Binding

The message table below is the execution contract. Sender, receiver, label, and number must not be changed during rendering.

| # | Sender | Receiver | Exact message label |
|---:|---|---|---|
| 1 | `Booking & Reception Staff` | `Facility Web Dashboard` | `Record detected conflict and context` |
| 2 | `Facility Web Dashboard` | `Aafiatak Backend` | `Create OperationalException(CONFLICT_DETECTED, context, reason)` |
| 3 | `Aafiatak Backend` | `Aafiatak Data Store` | `Persist OPEN exception and link operational context` |
| 4 | `Aafiatak Data Store` | `Aafiatak Backend` | `OperationalException created` |
| 5 | `Aafiatak Backend` | `Aafiatak Data Store` | `Identify the single affected CONFIRMED Appointment and relevant payment/capacity context` |
| 6 | `Aafiatak Data Store` | `Aafiatak Backend` | `Affected Appointment context: unresolved and fully paid` |
| 7 | `Aafiatak Backend` | `Facility Web Dashboard` | `Display affected Appointment and required resolution status` |
| 8 | `Booking & Reception Staff` | `Facility Web Dashboard` | `Record facility-side cancellation outcome` |
| 9 | `Facility Web Dashboard` | `Aafiatak Backend` | `Cancel affected Appointment by facility` |
| 10 | `Aafiatak Backend` | `Aafiatak Data Store` | `Set CANCELLED_BY_FACILITY + preserve history + write completed Appointment resolution` |
| 11 | `Aafiatak Data Store` | `Aafiatak Backend` | `Cancellation committed; collected payment exists` |
| 12 | `Aafiatak Backend` | `Payment Gateway` | `Initiate full collected-amount refund` |
| 13 | `Payment Gateway` | `Aafiatak Backend` | `Refund result/pending reference` |
| 14 | `Aafiatak Backend` | `Aafiatak Data Store` | `Persist independent refund status` |
| 15 | `Aafiatak Data Store` | `Aafiatak Backend` | `Refund state saved` |
| 16 | `Aafiatak Backend` | `Notification Service` | `Send affected-Patient operational notification` |
| 17 | `Notification Service` | `Aafiatak Backend` | `Notification accepted/result` |
| 18 | `Notification Service` | `Patient` | `Deliver exception/resolution information` |
| 19 | `Booking & Reception Staff` | `Facility Web Dashboard` | `Request Close Operational Exception` |
| 20 | `Facility Web Dashboard` | `Aafiatak Backend` | `Close exception request` |
| 21 | `Aafiatak Backend` | `Aafiatak Data Store` | `Verify documented completed action/outcome for the single affected Appointment` |
| 22 | `Aafiatak Data Store` | `Aafiatak Backend` | `Resolution complete for the selected affected Appointment` |
| 23 | `Aafiatak Backend` | `Aafiatak Data Store` | `Close OperationalException and preserve audit trail` |
| 24 | `Aafiatak Data Store` | `Aafiatak Backend` | `OperationalException CLOSED` |
| 25 | `Aafiatak Backend` | `Facility Web Dashboard` | `Closure confirmed` |

## Self-Messages

None in this selected scenario.

## Binding Domain / Lifecycle Invariants

- Facility Administrator is also authorized for generic UCM-13 handling, but this concrete scenario intentionally uses Booking & Reception Staff only.
- `CANCELLED_BY_FACILITY` is terminal for the Appointment.
- Facility-responsible cancellation/conflict requires a full refund of any collected electronic amount; no partial refund exists.
- PaymentIntent refund status remains independent from Appointment and OperationalException status.
- OperationalException cannot close while any affected Appointment lacks a completed documented action/outcome.
- If multiple Appointments are affected in another scenario, processing one Appointment is never sufficient for closure.
- No free internal facility capacity may be imported into the same published Aafiatak release to solve the conflict.

## Success Postconditions

- Affected Appointment is `CANCELLED_BY_FACILITY` and its history/resolution is preserved.
- Full collected-amount refund lifecycle is initiated and its independent status is persisted.
- Patient receives the supported operational resolution information.
- The selected Appointment has a completed documented resolution outcome.
- OperationalException may become `CLOSED` after the closure gate verifies resolution completeness for this one-Appointment scenario.
- `CLOSED` does **not** mean PaymentIntent is necessarily already `REFUNDED`; refund settlement may remain independently pending/reviewed according to trusted payment/refund events.

## Explicitly Forbidden Interpretations

- Treating the plural SD-06 affected set as resolved after processing only one Appointment.
- Closing an exception from the escalation branch alone.
- Claiming refund settlement is complete merely because refund was initiated.
- Partial refund.
- Silent deletion of Appointment/history.
- Importing internal free capacity into the same release.
- Making Platform Administrator perform normal facility daily operations.

## Intentional SD-06 Deviation — Required Correction

The uploaded SD-06 is a **general multi-Appointment interaction**: it loads an `Affected context / unresolved Appointment set` and later requires `documented action/outcome for every affected Appointment`. A single branch rendered without iteration can falsely imply that one processed Appointment is enough to close the exception.

This Collaboration file therefore does **not** copy that ambiguity. It selects one concrete conflict containing exactly one affected Appointment, which makes the single facility-cancellation branch and closure gate internally complete. This is supported by the higher-priority MVP/UCM and does not change the generic rule for multi-Appointment exceptions.


## Nine-Pass Verification Record

1. **Lecturer-method pass:** verified against the lecturer's Collaboration example and Interaction-Diagram classification.
2. **Authority/scope pass:** checked against the root MVP; no deferred/open decision was invented.
3. **Use Case Modeling pass:** scenario, actor, preconditions, selected success path, and postconditions matched to the current reviewed UCM.
4. **Sequence pass:** participants and selected interaction messages were reconciled against `Aafiatak_SD06_Operational_Exception_FINAL_REVIEWED(1).md`; any intentional deviation is documented explicitly in this file.
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
