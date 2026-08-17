# Activity Diagram — Record No-show
## Aafiatak Medical Appointment Booking System — MVP Activity Diagram Specification

**Diagram ID:** `AD-11`  
**Deliverable:** UML Activity Diagram  
**Use Case:** `Record No-show`  
**Traceability:** UCM-11; BRUC-29; Project Specification §§17.2, 19.4/19.7, 22  
**Package:** Booking & Reception Staff Package  
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

1. Staff is authenticated/authorized.
2. Appointment is relevant to the service-day context.
3. Assigned ArrivalGroup window should have ended.
4. A valid check-in must not exist.
5. No terminal VisitInstance outcome may already exist.

## 7. Exact Node Inventory

The renderer must implement exactly the following semantic nodes. It may wrap text or adjust geometry, but must not rename, omit, merge, or invent business actions.

- `I` — **Initial Node:** Start
- `A01` — **Action:** Staff selects overdue Appointment / visit and chooses Record No-show
- `A02` — **Action:** Validate ArrivalGroup time, check-in state and existing terminal outcome
- `D01` — **Decision:** ArrivalGroup window ended?
- `A03` — **Action:** Reject premature NO_SHOW
- `D02` — **Decision:** Valid check-in exists?
- `A04` — **Action:** Reject NO_SHOW; use actual checked-in Visit path
- `D03` — **Decision:** Terminal outcome already recorded?
- `A05` — **Action:** Return existing terminal outcome; do not reopen or duplicate
- `A06` — **Action:** Staff confirms no-show decision
- `A07` — **Action:** Create/use permitted VisitInstance context and record terminal NO_SHOW
- `A08` — **Action:** Record actor, timestamp and audit information
- `D04` — **Decision:** Booking has collected electronic payment?
- `A09` — **Action:** Create no Aafiatak electronic refund
- `D05` — **Decision:** Saved no-show financial policy?
- `A10` — **Action:** Apply NO_SHOW_NON_REFUNDABLE — refund due = zero
- `A11` — **Action:** Initiate full collected-amount refund under NO_SHOW_FULL_REFUND
- `A12` — **Action:** Display terminal Visit outcome and independent payment/refund state
- `MEND` — **Merge:** End-path merge
- `F` — **Final Node:** End

## 8. Exact Control-Flow / Edge Table

| From | To | Guard | Meaning / rendering instruction |
|---|---|---|---|
| `I` | `A01` | — | Begin no-show |
| `A01` | `A02` | — | Validate conditions |
| `A02` | `D01` | — | Time decision |
| `D01` | `A03` | [No] | Too early |
| `A03` | `MEND` | — | End rejected |
| `D01` | `D02` | [Yes] | Check arrival |
| `D02` | `A04` | [Yes] | Patient did arrive |
| `A04` | `MEND` | — | End rejected |
| `D02` | `D03` | [No] | Check terminality |
| `D03` | `A05` | [Yes] | No duplicate/reopen |
| `A05` | `MEND` | — | End existing-result branch |
| `D03` | `A06` | [No] | Record no-show |
| `A06` | `A07` | — | Terminal visit outcome |
| `A07` | `A08` | — | Audit |
| `A08` | `D04` | — | Financial branch |
| `D04` | `A09` | [No / PAY_AT_FACILITY] | No electronic refund |
| `A09` | `A12` | — | Show result |
| `D04` | `D05` | [Yes] | Use saved policy |
| `D05` | `A10` | [NO_SHOW_NON_REFUNDABLE] | Zero refund |
| `A10` | `A12` | — | Show result |
| `D05` | `A11` | [NO_SHOW_FULL_REFUND] | Full refund lifecycle |
| `A11` | `A12` | — | Show result/pending status |
| `A12` | `MEND` | — | End |
| `MEND` | `F` | — | Activity final |

## 9. Branch Semantics

### Timing
NO_SHOW only after assigned ArrivalGroup window ends without valid check-in.

### Terminality
A valid NO_SHOW is terminal and cannot be reopened for late check-in.

### Financial policy
Use the Appointment saved no-show policy; refund is full or zero only.

### PAY_AT_FACILITY
No PaymentIntent exists, therefore no Aafiatak electronic refund.


## 10. Binding Business Rules

- Facility staff, not Doctor, records NO_SHOW.
- Appointment state remains separate; NO_SHOW belongs to VisitInstance.
- Refund status remains independent.

## 11. Explicitly Forbidden in This Diagram

- Premature NO_SHOW.
- NO_SHOW when valid check-in exists.
- Doctor recording NO_SHOW.
- Appointment status = NO_SHOW.
- Partial no-show refund.
- NO_SHOW -> CHECKED_IN reopening.

## 12. Review Record

- Pass 1: lecturer structure
- Pass 2: UCM-11 success
- Pass 3: window-ended condition
- Pass 4: check-in condition
- Pass 5: terminality
- Pass 6: NO_SHOW Visit state
- Pass 7: audit
- Pass 8: PAY_AT_FACILITY
- Pass 9: saved no-show policy
- Pass 10: full/zero refund
- Pass 11: no partial
- Pass 12: role boundary
- Pass 13: Decision/Merge
- Pass 14: no reopen
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
