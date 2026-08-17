# Activity Diagram — Cancel Appointment
## Aafiatak Medical Appointment Booking System — MVP Activity Diagram Specification

**Diagram ID:** `AD-06`  
**Deliverable:** UML Activity Diagram  
**Use Case:** `Cancel Appointment`  
**Traceability:** UCM-06; PUC-19; Project Specification §§15.1, 17.1, 18, 19.2  
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

1. Patient is authenticated and owns the Appointment.
2. Appointment is CONFIRMED.
3. Patient has not checked in.
4. Assigned ArrivalGroup window has not started.

## 7. Exact Node Inventory

The renderer must implement exactly the following semantic nodes. It may wrap text or adjust geometry, but must not rename, omit, merge, or invent business actions.

- `I` — **Initial Node:** Start
- `A01` — **Action:** Patient opens Appointment and chooses Cancel Appointment
- `D00` — **Decision:** Appointment already terminally cancelled?
- `A00` — **Action:** Return existing cancellation/refund result; create no duplicate cancellation or refund
- `A02` — **Action:** Load saved cancellation/refund policy, payment state and ArrivalGroup timing
- `A03` — **Action:** Revalidate ownership, CONFIRMED state, check-in and group-start conditions
- `D01` — **Decision:** Patient self-cancellation still eligible?
- `A04` — **Action:** Deny self-cancellation and preserve arrival / late / no-show handling
- `A05` — **Action:** Calculate and display expected refund result from saved booking snapshot
- `A06` — **Action:** Patient confirms cancellation
- `A07` — **Action:** Record CANCELLED_BY_PATIENT and preserve Appointment history
- `A08` — **Action:** Return consumed unit to the same ArrivalGroup; expose it as bookable only when release/group/time rules permit
- `D02` — **Decision:** Aafiatak electronic amount was collected?
- `A09` — **Action:** Create no electronic refund
- `D03` — **Decision:** Saved policy says full refund is due?
- `A10` — **Action:** Refund due is zero
- `A11` — **Action:** Initiate full collected-amount refund
- `D04` — **Decision:** Refund completion immediate?
- `A12` — **Action:** Keep independent REFUND_PENDING / review status; cancellation remains final
- `A13` — **Action:** Record completed full refund
- `A14` — **Action:** Display cancelled Appointment and independent payment/refund status
- `MEND` — **Merge:** End-path merge
- `F` — **Final Node:** End

## 8. Exact Control-Flow / Edge Table

| From | To | Guard | Meaning / rendering instruction |
|---|---|---|---|
| `I` | `A01` | — | Begin cancellation |
| `A01` | `D00` | — | Check duplicate/terminal cancellation boundary |
| `D00` | `A00` | [Yes] | Preserve existing terminal cancellation/result |
| `A00` | `MEND` | — | No duplicate cancellation/refund |
| `D00` | `A02` | [No] | Continue cancellation review |
| `A02` | `A03` | — | Eligibility revalidation |
| `A03` | `D01` | — | Decision |
| `D01` | `A04` | [No] | Self-cancellation denied |
| `A04` | `MEND` | — | End denial branch |
| `D01` | `A05` | [Yes] | Show consequence before commit |
| `A05` | `A06` | — | Patient confirms |
| `A06` | `A07` | — | Cancel Appointment |
| `A07` | `A08` | — | Same-group capacity consequence |
| `A08` | `D02` | — | Evaluate financial branch |
| `D02` | `A09` | [No — PAY_AT_FACILITY / no collected electronic amount] | No Aafiatak refund |
| `A09` | `A14` | — | Show result |
| `D02` | `D03` | [Yes] | Apply saved policy |
| `D03` | `A10` | [Zero refund] | No refund created |
| `A10` | `A14` | — | Show result |
| `D03` | `A11` | [Full refund] | Full amount only |
| `A11` | `D04` | — | Refund status |
| `D04` | `A12` | [Pending / delayed] | Cancellation remains final |
| `A12` | `A14` | — | Show independent states |
| `D04` | `A13` | [Completed] | Record refunded |
| `A13` | `A14` | — | Show result |
| `A14` | `MEND` | — | End |
| `MEND` | `F` | — | Activity final |

## 9. Branch Semantics

### Eligibility
If checked in or group window started, Patient self-cancellation is denied.

### Refund policy
Use the Appointment saved snapshot; later facility policy changes do not alter this booking.

### Capacity
Returned capacity stays in the original ArrivalGroup and is bookable only when parent/group/time rules permit.

### Pending refund
Appointment cancellation remains final while refund is pending/reviewed.

### Duplicate / already-cancelled request
If the Appointment is already terminally cancelled, return the existing state/result and do not create another cancellation, capacity release, or refund.


## 10. Binding Business Rules

- Refund is exactly full collected amount or zero.
- PAY_AT_FACILITY has no Aafiatak electronic refund.
- No partial refund.
- Appointment state and PaymentIntent state remain independent.

## 11. Explicitly Forbidden in This Diagram

- Partial refund percentages.
- Cancellation after check-in through Patient self-service.
- Moving returned seat to another group.
- Reversing cancellation because refund is delayed.

## 12. Review Record

- Pass 1: lecturer structure
- Pass 2: UCM-06 eligibility
- Pass 3: historical snapshot
- Pass 4: expected-refund-before-confirm
- Pass 5: CANCELLED_BY_PATIENT
- Pass 6: same-group seat return
- Pass 7: PAY_AT_FACILITY branch
- Pass 8: full/zero refund
- Pass 9: pending refund independence
- Pass 10: no partial
- Pass 11: state separation
- Pass 12: Decision/Merge use
- Pass 13: no Fork/Join
- Pass 14: visual flow
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
