# Sequence Diagram — Patient Registration & WhatsApp OTP Verification
## Aafiatak Medical Appointment Booking System — MVP Sequence Diagram Specification

**Diagram ID:** `SD-01`  
**Deliverable:** UML Sequence Diagram  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** VUC-05 / VUC-07; UCM-01 Register Patient; Project Specification §§8.4, 9, 10.1  
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
Create one verified Patient account/profile from an unauthenticated Visitor through the approved WhatsApp OTP phone-verification channel.

### Primary actor
- `Visitor`

### Supporting external participant
- `WhatsApp Authentication Provider`

### Preconditions
1. Visitor is not authenticated as a Patient.
2. Visitor has a phone number that can be normalized and verified.
3. Public Patient self-registration is available.
4. No password/SMS registration flow is introduced.

### Success postconditions
1. Exactly one verified `User` identity exists for the normalized phone.
2. Exactly one related `Patient` profile is created for this registration.
3. No password credential is created.
4. Registration retry does not create duplicate identities/profiles.

## 4. Exact Participants

Use exactly these lifelines, left-to-right:

| # | Lifeline | Kind | Responsibility in this sequence |
|---:|---|---|---|
| 1 | `Visitor` | Human Actor | Starts registration, receives OTP, submits OTP/profile data |
| 2 | `Patient Application` | Boundary | Collects input and displays registration/verification results |
| 3 | `Aafiatak Backend` | Control/System | Normalizes phone, enforces registration/OTP rules, orchestrates creation |
| 4 | `Aafiatak Data Store` | Internal data participant | Checks uniqueness and persists User/Patient records |
| 5 | `WhatsApp Authentication Provider` | External system | Delivers the approved OTP through official WhatsApp integration |

Do not add:
- SMS Provider;
- Password Service;
- `Forgot Password`;
- `FacilityAdministrator`;
- Payment Gateway;
- clinical/profile-record systems.

## 5. Mandatory Main Success Sequence

| # | Sender | Receiver | Message label | UML message type |
|---:|---|---|---|---|
| 1 | Visitor | Patient Application | `Enter phone number and choose Register` | Solid request/action |
| 2 | Patient Application | Aafiatak Backend | `Start patient registration(phone)` | Solid request |
| 3 | Aafiatak Backend | Aafiatak Backend | `Normalize and validate phone number` | Solid self-message |
| 4 | Aafiatak Backend | Aafiatak Data Store | `Check phone identity uniqueness` | Solid request |
| 5 | Aafiatak Data Store | Aafiatak Backend | `Identity lookup result: available` | Dashed response |
| 6 | Aafiatak Backend | WhatsApp Authentication Provider | `Request short-lived single-use OTP delivery` | Solid request |
| 7 | WhatsApp Authentication Provider | Aafiatak Backend | `OTP delivery request accepted` | Dashed response |
| 8 | Aafiatak Backend | Patient Application | `Verification required` | Dashed response |
| 9 | WhatsApp Authentication Provider | Visitor | `Deliver OTP via official WhatsApp channel` | Solid external event |
| 10 | Visitor | Patient Application | `Submit OTP` | Solid action |
| 11 | Patient Application | Aafiatak Backend | `Verify OTP attempt` | Solid request |
| 12 | Aafiatak Backend | Aafiatak Backend | `Validate expiry, single-use and security limits` | Solid self-message |
| 13 | Aafiatak Backend | Patient Application | `OTP verified; request basic Patient profile` | Dashed response |
| 14 | Visitor | Patient Application | `Submit approved basic profile data` | Solid action |
| 15 | Patient Application | Aafiatak Backend | `Create verified Patient account/profile` | Solid request |
| 16 | Aafiatak Backend | Aafiatak Data Store | `Atomically create User + Patient for verified phone` | Solid request |
| 17 | Aafiatak Data Store | Aafiatak Backend | `Account/profile created exactly once` | Dashed response |
| 18 | Aafiatak Backend | Patient Application | `Registration confirmed` | Dashed response |
| 19 | Patient Application | Visitor | `Display Patient registration success` | Dashed response |

### Activation guidance
- Backend activation begins at message 2 and pauses/returns around nested provider/data-store calls.
- Data Store activation is short around messages 4–5 and 16–17.
- WhatsApp provider activation covers the delivery request; actual delivery to Visitor is an external event.
- Do not draw the OTP value as text.

## 6. Critical Alternatives to Render

### `alt` A1 — Phone already belongs to an existing User
After message 5:
- Data Store returns `Identity already exists`.
- Backend returns `Registration rejected: existing verified identity`.
- No duplicate User/Patient record is created.
- Do **not** invent a password-reset path.

### `alt` A2 — OTP invalid, expired, or reused
After message 11:
- Backend rejects verification.
- No Patient profile is created.
- No authenticated/verified registration is established.

### `alt` A3 — OTP request/verification rate-limited
- Backend rejects or delays the abusive/excessive attempt according to security controls.
- No duplicate registration is created.

### `alt` A4 — WhatsApp provider unavailable
- OTP delivery cannot complete.
- Registration remains incomplete.
- Do not fall back to SMS or password.

### Retry/idempotency note
If the client retries because of weak connectivity, the backend/database uniqueness and idempotent rules must prevent duplicate User/Patient creation.

## 7. State and Domain Rules

- One normalized verified phone identifies one `User`.
- Patient self-registration is allowed only after phone verification.
- Privileged facility/platform roles are not created by this flow.
- WhatsApp is used only for authentication/phone verification.
- General appointment/reminder notifications do not belong in this sequence.
- Registration contains no clinical data collection.

## 8. Forbidden Messages/Behaviors

Do not show:
- `Create password`;
- `Send SMS OTP`;
- `Forgot Password`;
- `Reset Password`;
- `Create medical record`;
- `Assign Facility role`;
- `Assign Platform role`;
- duplicate `User` creation on retry;
- unofficial WhatsApp browser automation.


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

- Pass 1: lecturer Sequence semantics and message notation.
- Pass 2: current authentication channel and SMS/password exclusions.
- Pass 3: unified User identity and phone uniqueness.
- Pass 4: Patient self-registration scope.
- Pass 5: privileged-role provisioning exclusion.
- Pass 6: OTP security constraints.
- Pass 7: idempotency/duplicate-account protection.
- Pass 8: Participant minimization; no invented microservices.
- Pass 9: request vs response arrow audit.
- Pass 10: sensitive-data label audit.
- Pass 11: success/failure postcondition audit.
- Pass 12: final traceability to UCM-01 and MVP scope.


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
