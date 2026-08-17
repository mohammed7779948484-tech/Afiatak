# Activity Diagram — Register Patient
## Aafiatak Medical Appointment Booking System — MVP Activity Diagram Specification

**Diagram ID:** `AD-01`  
**Deliverable:** UML Activity Diagram  
**Use Case:** `Register Patient`  
**Traceability:** UCM-01; VUC-05/VUC-07; Project Specification §§8.4, 9, 10.1  
**Package:** Visitor Package  
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

1. Visitor is not authenticated as a Patient.
2. A phone number can be normalized and verified.
3. Public Patient self-registration is available.

## 7. Exact Node Inventory

The renderer must implement exactly the following semantic nodes. It may wrap text or adjust geometry, but must not rename, omit, merge, or invent business actions.

- `I` — **Initial Node:** Start
- `A01` — **Action:** Visitor chooses Register Patient and provides phone number
- `A02` — **Action:** Normalize phone number and check global identity uniqueness
- `D01` — **Decision:** Existing identity?
- `A03` — **Action:** Reject duplicate registration and direct to existing-account login path
- `A04` — **Action:** Request short-lived single-use WhatsApp OTP
- `D02` — **Decision:** WhatsApp authentication channel available?
- `A05` — **Action:** Keep registration incomplete; no fallback authentication
- `A06` — **Action:** Visitor receives and submits OTP
- `A07` — **Action:** Verify OTP expiry, single-use, rate-limit and brute-force controls
- `D03` — **Decision:** OTP valid and permitted?
- `A08` — **Action:** Reject verification; create no Patient account
- `A09` — **Action:** Visitor provides approved basic Patient profile data and confirms registration
- `A10` — **Action:** Validate non-clinical registration data
- `A11` — **Action:** Create User + Patient exactly once for verified phone identity
- `A12` — **Action:** Establish approved Patient account context without password
- `MEND` — **Merge:** End-path merge
- `F` — **Final Node:** End

## 8. Exact Control-Flow / Edge Table

| From | To | Guard | Meaning / rendering instruction |
|---|---|---|---|
| `I` | `A01` | — | Begin registration |
| `A01` | `A02` | — | Normalize and check identity |
| `A02` | `D01` | — | Evaluate uniqueness |
| `D01` | `A03` | [Yes — existing identity] | No duplicate identity |
| `A03` | `MEND` | — | Alternative/failure ends |
| `D01` | `A04` | [No — identity available] | Continue verification |
| `A04` | `D02` | — | Evaluate official WhatsApp channel |
| `D02` | `A05` | [Unavailable] | No SMS/password fallback |
| `A05` | `MEND` | — | Incomplete registration ends |
| `D02` | `A06` | [Available] | Continue OTP exchange |
| `A06` | `A07` | — | Verify OTP |
| `A07` | `D03` | — | Evaluate OTP result/security limits |
| `D03` | `A08` | [Invalid / expired / reused / rate-limited] | No verified account |
| `A08` | `MEND` | — | Failed verification ends |
| `D03` | `A09` | [Valid] | Continue profile creation |
| `A09` | `A10` | — | Validate allowed profile data |
| `A10` | `A11` | — | Idempotent identity/profile creation |
| `A11` | `A12` | — | Establish Patient context |
| `A12` | `MEND` | — | Success path ends |
| `MEND` | `F` | — | Activity final |

## 9. Branch Semantics

### Identity branch
An already-owned normalized phone must never create a duplicate User/Patient. The branch terminates through the existing-account login direction.

### OTP branch
Unavailable WhatsApp or invalid/expired/reused/over-limit OTP leaves registration incomplete; no password or SMS fallback is added.

### Retry/idempotency
Weak-connectivity retries must return the existing successful identity/profile result rather than create a duplicate. Keep this as a compact note near `A11` instead of another large loop.


## 10. Binding Business Rules

- One normalized verified phone identifies one User.
- Create Patient profile only after successful phone verification.
- No clinical data in registration.
- OTP exact lifetime is not fixed in this diagram.

## 11. Explicitly Forbidden in This Diagram

- Patient as the starting actor label instead of Visitor.
- Creating an UNVERIFIED Patient before OTP success.
- Password, Forgot Password, SMS authentication.
- Actual OTP/secret values in labels.

## 12. Review Record

- Pass 1: lecturer Activity notation
- Pass 2: UCM-01 success flow
- Pass 3: identity uniqueness
- Pass 4: WhatsApp-only authentication
- Pass 5: OTP failure branches
- Pass 6: idempotency
- Pass 7: non-clinical scope
- Pass 8: no swimlanes
- Pass 9: Decision/Merge correctness
- Pass 10: no Fork/Join without concurrency
- Pass 11: state separation
- Pass 12: MVP actor boundary
- Pass 13: label concision
- Pass 14: visual routing
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
