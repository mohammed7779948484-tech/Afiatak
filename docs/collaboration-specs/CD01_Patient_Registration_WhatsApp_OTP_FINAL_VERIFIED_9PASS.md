# Collaboration Diagram — Patient Registration & WhatsApp OTP Verification

**Diagram ID:** `CD-01`  
**System:** Aafiatak Medical Appointment Booking System  
**Status:** FINAL VERIFIED — 9-PASS SOURCE-MATCHED SEMANTIC SPECIFICATION  
**Rendered language:** English only  
**Traceability:** UCM-01; VUC-05/VUC-07; SD-01; MVP authentication/identity scope

## Scenario Scope

Successful patient self-registration from an unauthenticated `Visitor` through the official WhatsApp OTP channel, ending with exactly one verified `User` identity and one linked `Patient` profile. This is the concrete success interaction for UCM-01 / SD-01.

## Source Priority and Conflict Rule

Use this exact precedence:

1. `Aafiatak_Project_Specification_EN.md` at the repository root — **authoritative MVP/product truth**.
2. `Aafiatak_Use_Case_Modeling_AR_SUBMISSION_READY_VERIFIED(2).docx` — current reviewed Use Case Modeling supplied for this audit.
3. `Aafiatak_SD01_Patient_Registration_OTP_FINAL_REVIEWED(1).md` — exact reviewed Sequence Diagram interaction baseline for this selected scenario.
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

1. Visitor is not authenticated as a Patient.
2. A valid phone number can be normalized and verified.
3. Patient self-registration is available.

## Participants

| # | Participant | Role in this selected interaction |
|---:|---|---|
| 1 | `Visitor` | Starts registration, receives OTP, submits OTP/profile data |
| 2 | `Patient Application` | Collects input and displays registration/verification results |
| 3 | `Aafiatak Backend` | Normalizes phone, enforces registration/OTP rules, orchestrates creation |
| 4 | `Aafiatak Data Store` | Checks uniqueness and persists User/Patient records |
| 5 | `WhatsApp Authentication Provider` | Delivers the approved OTP through official WhatsApp integration |

## Structural Communication Links

| Link | Participant A | Participant B | Messages using this Link |
|---|---|---|---|
| L01 | `Aafiatak Backend` | `Aafiatak Data Store` | 4, 5, 16, 17 |
| L02 | `Aafiatak Backend` | `Patient Application` | 2, 8, 11, 13, 15, 18 |
| L03 | `Aafiatak Backend` | `WhatsApp Authentication Provider` | 6, 7 |
| L04 | `Patient Application` | `Visitor` | 1, 10, 14, 19 |
| L05 | `Visitor` | `WhatsApp Authentication Provider` | 9 |

A Link is structural and reusable. Do not create one parallel connector for every message between the same two participants.

## Ordered Messages — Binding

The message table below is the execution contract. Sender, receiver, label, and number must not be changed during rendering.

| # | Sender | Receiver | Exact message label |
|---:|---|---|---|
| 1 | `Visitor` | `Patient Application` | `Enter phone number and choose Register` |
| 2 | `Patient Application` | `Aafiatak Backend` | `Start patient registration(phone)` |
| 3 | `Aafiatak Backend` | `Aafiatak Backend` | `Normalize and validate phone number` |
| 4 | `Aafiatak Backend` | `Aafiatak Data Store` | `Check phone identity uniqueness` |
| 5 | `Aafiatak Data Store` | `Aafiatak Backend` | `Identity lookup result: available` |
| 6 | `Aafiatak Backend` | `WhatsApp Authentication Provider` | `Request short-lived single-use OTP delivery` |
| 7 | `WhatsApp Authentication Provider` | `Aafiatak Backend` | `OTP delivery request accepted` |
| 8 | `Aafiatak Backend` | `Patient Application` | `Verification required` |
| 9 | `WhatsApp Authentication Provider` | `Visitor` | `Deliver OTP via official WhatsApp channel` |
| 10 | `Visitor` | `Patient Application` | `Submit OTP` |
| 11 | `Patient Application` | `Aafiatak Backend` | `Verify OTP attempt` |
| 12 | `Aafiatak Backend` | `Aafiatak Backend` | `Validate expiry, single-use and security limits` |
| 13 | `Aafiatak Backend` | `Patient Application` | `OTP verified; request basic Patient profile` |
| 14 | `Visitor` | `Patient Application` | `Submit approved basic profile data` |
| 15 | `Patient Application` | `Aafiatak Backend` | `Create verified Patient account/profile` |
| 16 | `Aafiatak Backend` | `Aafiatak Data Store` | `Atomically create User + Patient for verified phone` |
| 17 | `Aafiatak Data Store` | `Aafiatak Backend` | `Account/profile created exactly once` |
| 18 | `Aafiatak Backend` | `Patient Application` | `Registration confirmed` |
| 19 | `Patient Application` | `Visitor` | `Display Patient registration success` |

## Self-Messages

- Message **3** — `Aafiatak Backend` self-message: `Normalize and validate phone number`.
- Message **12** — `Aafiatak Backend` self-message: `Validate expiry, single-use and security limits`.

## Binding Domain / Lifecycle Invariants

- One normalized verified phone identifies one User identity.
- WhatsApp is used only for authentication/phone verification.
- OTP is short-lived, single-use, rate-limited, and never exposed in diagram labels.
- Basic Patient data is non-clinical.
- Account/profile creation is idempotent and must not duplicate identity/profile records.

## Success Postconditions

- Exactly one verified User identity exists for the normalized phone.
- Exactly one linked Patient profile exists.
- No password is created.
- No SMS authentication path is created.

## Explicitly Forbidden Interpretations

- Password or Forgot Password flow.
- SMS OTP.
- Creation of a Patient before successful phone verification.
- Clinical profile/medical-record data.
- Duplicate User/Patient creation on retry.



## Nine-Pass Verification Record

1. **Lecturer-method pass:** verified against the lecturer's Collaboration example and Interaction-Diagram classification.
2. **Authority/scope pass:** checked against the root MVP; no deferred/open decision was invented.
3. **Use Case Modeling pass:** scenario, actor, preconditions, selected success path, and postconditions matched to the current reviewed UCM.
4. **Sequence pass:** participants and selected interaction messages were reconciled against `Aafiatak_SD01_Patient_Registration_OTP_FINAL_REVIEWED(1).md`; any intentional deviation is documented explicitly in this file.
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
