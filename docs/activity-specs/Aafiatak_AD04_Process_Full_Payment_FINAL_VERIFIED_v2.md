# Activity Diagram — Process Full Payment
## Aafiatak Medical Appointment Booking System — MVP Activity Diagram Specification

**Diagram ID:** `AD-04`  
**Deliverable:** UML Activity Diagram  
**Use Case:** `Process Full Payment`  
**Traceability:** UCM-04; MUC-09/MUC-10/PUC-21/PUC-22; Project Specification §§18.1–18.3, 19.3  
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

1. Booking policy is FULL_PAYMENT_REQUIRED.
2. An ACTIVE ReservationHold exists.
3. Amount/currency are the booking-attempt snapshot values.
4. No other non-terminal PaymentIntent is active for the same hold.

## 7. Exact Node Inventory

The renderer must implement exactly the following semantic nodes. It may wrap text or adjust geometry, but must not rename, omit, merge, or invent business actions.

- `I` — **Initial Node:** Start
- `A01` — **Action:** Create or safely reuse the one permitted PaymentIntent
- `A02` — **Action:** Patient completes approved Payment Gateway interaction
- `A03` — **Action:** Treat client/browser return as non-authoritative
- `A04` — **Action:** Verify result through trusted webhook or trusted gateway query
- `D01` — **Decision:** Trusted payment result available?
- `A05` — **Action:** Keep payment unresolved / UNDER_REVIEW as applicable
- `D02` — **Decision:** Trusted payment outcome?
- `A06` — **Action:** Record FAILED or EXPIRED payment result
- `D03` — **Decision:** Patient requests another attempt while hold remains valid?
- `A07` — **Action:** Start new idempotent attempt only after terminal failure/expiry
- `A08` — **Action:** Persist trusted SUCCEEDED financial result
- `A09` — **Action:** Revalidate ReservationHold and release/group/time eligibility
- `D04` — **Decision:** Original booking target still eligible?
- `A10` — **Action:** Attempt safe equivalent recovery under equivalent snapshotted terms
- `D05` — **Decision:** Equivalent recovery completed safely?
- `A11` — **Action:** Create / complete confirmed booking under equivalent valid capacity
- `D06` — **Decision:** Full refund can be initiated as approved recovery?
- `A12` — **Action:** Initiate full refund
- `A13` — **Action:** Keep payment case UNDER_REVIEW for documented support path
- `A14` — **Action:** Atomically consume hold and create CONFIRMED Appointment
- `A15` — **Action:** Show independent payment result, receipt/reference and booking result
- `MEND` — **Merge:** End-path merge
- `F` — **Final Node:** End

## 8. Exact Control-Flow / Edge Table

| From | To | Guard | Meaning / rendering instruction |
|---|---|---|---|
| `I` | `A01` | — | Prepare idempotent payment attempt |
| `A01` | `A02` | — | Gateway interaction |
| `A02` | `A03` | — | Client returns |
| `A03` | `A04` | — | Trusted verification required |
| `A04` | `D01` | — | Check trusted result availability |
| `D01` | `A05` | [Not yet] | Unresolved case |
| `A05` | `MEND` | — | Current activity instance ends in review/unresolved state |
| `D01` | `D02` | [Available] | Classify trusted outcome |
| `D02` | `A06` | [FAILED / EXPIRED] | Record terminal failed attempt |
| `A06` | `D03` | — | Optional retry rule |
| `D03` | `A07` | [Yes — hold still valid] | New attempt allowed under idempotent rules |
| `A07` | `A02` | — | Loop to gateway interaction |
| `D03` | `MEND` | [No] | No confirmed booking from failed payment |
| `D02` | `A08` | [SUCCEEDED] | Persist financial truth |
| `A08` | `A09` | — | Booking eligibility revalidation |
| `A09` | `D04` | — | Check target |
| `D04` | `A14` | [Eligible] | Normal successful confirmation |
| `A14` | `A15` | — | Display result |
| `A15` | `MEND` | — | Success ends |
| `D04` | `A10` | [Ineligible / appointment creation failed] | Critical recovery |
| `A10` | `D05` | — | Evaluate equivalent recovery |
| `D05` | `A11` | [Yes] | Complete safe equivalent booking |
| `A11` | `A15` | — | Show recovered success |
| `D05` | `D06` | [No] | Choose approved financial recovery |
| `D06` | `A12` | [Refund path available] | Full refund only |
| `A12` | `MEND` | — | Refund path ends/pends independently |
| `D06` | `A13` | [Cannot resolve immediately] | Documented UNDER_REVIEW path |
| `A13` | `MEND` | — | Review path ends |
| `MEND` | `F` | — | Activity final |

## 9. Branch Semantics

### Trusted result
Browser/app return never drives `SUCCEEDED`; only trusted gateway verification does.

### Failure retry
A new attempt after terminal FAILED/EXPIRED is allowed only while the hold remains valid and server-side idempotency permits it.

### Success but booking fails
Financial success is preserved independently; never fabricate a conflicting Appointment.

### Duplicate/delayed gateway event
Process idempotently; do not duplicate charge, booking, refund, or transition. Keep as a compact note on `A04/A08`.

### Notification failure
Notification retries independently and must not reverse successful financial/Appointment result; keep as a rule, not a payment control-flow branch.

### Patient presents a receipt while the gateway result is unresolved
The receipt is evidence for the defined verification/escalation path only. Ordinary facility users must not overwrite PaymentIntent truth. Keep this as a compact note beside the `UNDER_REVIEW` / trusted-verification area rather than inventing a new payment transition.


## 10. Binding Business Rules

- At most one non-terminal PaymentIntent per ReservationHold.
- No PaymentIntent for PAY_AT_FACILITY.
- Refund is full amount or zero.
- Ordinary facility users cannot force a financial state.

## 11. Explicitly Forbidden in This Diagram

- Client return -> SUCCEEDED directly.
- Partial payment/refund.
- Cashier/accounting lifecycle.
- Multiple gateways.
- Arbitrary Reception payment override.

## 12. Review Record

- Pass 1: lecturer notation
- Pass 2: UCM-04 success
- Pass 3: trusted-gateway boundary
- Pass 4: failure/expiry
- Pass 5: retry loop
- Pass 6: UNDER_REVIEW
- Pass 7: success target revalidation
- Pass 8: equivalent recovery
- Pass 9: full-refund-only
- Pass 10: idempotent duplicate event
- Pass 11: payment/appointment independence
- Pass 12: hold validity
- Pass 13: no client truth
- Pass 14: branch routing
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
