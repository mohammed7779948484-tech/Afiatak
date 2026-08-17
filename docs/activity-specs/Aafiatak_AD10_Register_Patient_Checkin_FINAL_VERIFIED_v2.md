# Activity Diagram — Register Patient Check-in
## Aafiatak Medical Appointment Booking System — MVP Activity Diagram Specification

**Diagram ID:** `AD-10`  
**Deliverable:** UML Activity Diagram  
**Use Case:** `Register Patient Check-in`  
**Traceability:** UCM-10; BRUC-17/18/19; Project Specification §§19.4–21  
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
2. Intended Appointment can be identified by booking number, phone, QR, or verification code.
3. Appointment is CONFIRMED and not cancelled.
4. Normal check-in applies only in the valid normal arrival context; late arrivals use AD-12.

## 7. Exact Node Inventory

The renderer must implement exactly the following semantic nodes. It may wrap text or adjust geometry, but must not rename, omit, merge, or invent business actions.

- `I` — **Initial Node:** Start
- `A01` — **Action:** Staff searches/scans Appointment identifier
- `A02` — **Action:** Retrieve intended Appointment and validate facility/state/arrival context
- `D01` — **Decision:** Correct intended Appointment and state = CONFIRMED?
- `A03` — **Action:** Reject check-in; create no valid Visit/Queue arrival state
- `D02` — **Decision:** Arrival eligible for normal check-in?
- `A04` — **Action:** Route to Handle Late Arrival activity; do not auto-transfer group
- `D03` — **Decision:** Valid check-in already exists from retry?
- `A05` — **Action:** Return existing VisitInstance / QueueEntry state idempotently
- `A06` — **Action:** Staff confirms Patient arrival
- `A07` — **Action:** Create VisitInstance if needed and set CHECKED_IN
- `A08` — **Action:** Record actual arrival time and original ArrivalGroup
- `A09` — **Action:** Create / activate one QueueEntry inside original ArrivalGroup
- `A10` — **Action:** Apply normal queue ordering by check-in time; earlier confirmed_at only as tie-breaker
- `A11` — **Action:** Show check-in confirmation and approximate own-group position/number ahead
- `MEND` — **Merge:** End-path merge
- `F` — **Final Node:** End

## 8. Exact Control-Flow / Edge Table

| From | To | Guard | Meaning / rendering instruction |
|---|---|---|---|
| `I` | `A01` | — | Begin staff check-in |
| `A01` | `A02` | — | Resolve booking |
| `A02` | `D01` | — | Context/state decision |
| `D01` | `A03` | [No] | Wrong/cancelled context |
| `A03` | `MEND` | — | Rejected |
| `D01` | `D02` | [Yes] | Evaluate arrival timing |
| `D02` | `A04` | [Late / outside normal context] | Use late-arrival workflow |
| `A04` | `MEND` | — | Normal check-in ends |
| `D02` | `D03` | [Normal arrival] | Check duplicate retry |
| `D03` | `A05` | [Existing valid check-in] | Idempotent return |
| `A05` | `MEND` | — | No duplicate |
| `D03` | `A06` | [No existing check-in] | Register arrival |
| `A06` | `A07` | — | Visit state |
| `A07` | `A08` | — | Arrival data |
| `A08` | `A09` | — | Queue entry |
| `A09` | `A10` | — | Ordering |
| `A10` | `A11` | — | Patient-facing confirmation |
| `A11` | `MEND` | — | Success |
| `MEND` | `F` | — | Activity final |

## 9. Branch Semantics

### Staff-only boundary
Patient self-check-in is not part of MVP.

### Late arrival
Normal check-in never silently moves Patient to another ArrivalGroup.

### Retry
Duplicate check-in must not create duplicate VisitInstance/QueueEntry.

### Erroneous check-in
Correction is a separate operation allowed only before service starts: QueueEntry -> REMOVED and VisitInstance may return CHECKED_IN -> CREATED with audited reason. Keep as a compact note rather than extending this main activity.


## 10. Binding Business Rules

- Appointment remains CONFIRMED; check-in is represented in VisitInstance.
- Queue position is approximate and only within Patient own group.
- Full payment grants no queue priority.

## 11. Explicitly Forbidden in This Diagram

- Patient self-check-in.
- Appointment state = CHECKED_IN.
- Automatic late transfer.
- Payment-based queue priority.
- Exposure of other Patients private data.

## 12. Review Record

- Pass 1: lecturer flow
- Pass 2: UCM-10 success
- Pass 3: identifier validation
- Pass 4: CONFIRMED boundary
- Pass 5: late branch
- Pass 6: duplicate idempotency
- Pass 7: VisitInstance creation
- Pass 8: CHECKED_IN
- Pass 9: original group
- Pass 10: QueueEntry
- Pass 11: queue ordering
- Pass 12: no payment priority
- Pass 13: staff-only
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
