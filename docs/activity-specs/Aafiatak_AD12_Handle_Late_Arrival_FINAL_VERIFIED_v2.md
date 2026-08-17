# Activity Diagram — Handle Late Arrival
## Aafiatak Medical Appointment Booking System — MVP Activity Diagram Specification

**Diagram ID:** `AD-12`  
**Deliverable:** UML Activity Diagram  
**Use Case:** `Handle Late Arrival`  
**Traceability:** UCM-12; MUC-24/BRUC-30/31 + BRUC-15/28/29; Project Specification §22 and §19.7  
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
2. Assigned ArrivalGroup window ended without valid normal check-in.
3. Appointment is the relevant booking context.

## 7. Exact Node Inventory

The renderer must implement exactly the following semantic nodes. It may wrap text or adjust geometry, but must not rename, omit, merge, or invent business actions.

- `I` — **Initial Node:** Start
- `A01` — **Action:** Staff identifies Patient arriving after assigned ArrivalGroup window
- `D01` — **Decision:** Terminal NO_SHOW already recorded?
- `A02` — **Action:** Do not reopen VisitInstance; require documented reschedule / new operational arrangement
- `A03` — **Action:** Staff records late arrival condition
- `D02` — **Decision:** Which real operational outcome is chosen?
- `A04` — **Action:** Accept Patient manually while keeping original Appointment and ArrivalGroup
- `A05` — **Action:** Register check-in / actual arrival and mark late accepted arrival
- `A06` — **Action:** Create/activate QueueEntry and set manualHandling flag
- `A07` — **Action:** Exclude from automatic numeric queue position; make no priority promise
- `A08` — **Action:** Call Patient when operationally appropriate without consuming another group capacity
- `A09` — **Action:** Reschedule after Patient agreement using same-service / same-terms atomic rules
- `A10` — **Action:** Record terminal NO_SHOW and apply saved no-show financial policy
- `A11` — **Action:** Record NOT_COMPLETED when Patient arrived but service was not completed
- `MEND` — **Merge:** End-path merge
- `F` — **Final Node:** End

## 8. Exact Control-Flow / Edge Table

| From | To | Guard | Meaning / rendering instruction |
|---|---|---|---|
| `I` | `A01` | — | Begin late handling |
| `A01` | `D01` | — | Check terminal boundary |
| `D01` | `A02` | [Yes] | Terminal NO_SHOW cannot reopen |
| `A02` | `MEND` | — | End current late-check-in path |
| `D01` | `A03` | [No] | Record late condition |
| `A03` | `D02` | — | Manual staff outcome decision |
| `D02` | `A04` | [Accept manually] | No automatic reassignment |
| `A04` | `A05` | — | Late accepted check-in |
| `A05` | `A06` | — | Manual queue visibility |
| `A06` | `A07` | — | No numeric priority |
| `A07` | `A08` | — | Operational call |
| `A08` | `MEND` | — | Manual-accept path ends |
| `D02` | `A09` | [Reschedule] | Use AD-09 invariants; secure new capacity first |
| `A09` | `MEND` | — | Reschedule path ends |
| `D02` | `A10` | [NO_SHOW is actual outcome] | Terminal no-show path |
| `A10` | `MEND` | — | No-show path ends |
| `D02` | `A11` | [NOT_COMPLETED is actual outcome] | Non-completion path |
| `A11` | `MEND` | — | Non-completion ends |
| `MEND` | `F` | — | Activity final |

## 9. Branch Semantics

### Manual acceptance
Original Appointment and original ArrivalGroup remain unchanged.

### Manual queue handling
`manualHandling` is a flag/mode, not a QueueEntry or VisitInstance state.

### Reschedule
Requires communication/agreement and valid new capacity; no automatic late transfer.

### Terminal boundary
Once NO_SHOW is validly recorded, any later accommodation requires another documented arrangement rather than state reversal.


## 10. Binding Business Rules

- No automatic move to a later group.
- No re-entry/requeue state.
- No numeric queue priority promise.
- No capacity consumption from another ArrivalGroup for manual acceptance.

## 11. Explicitly Forbidden in This Diagram

- LATE / LATE_ACCEPTED as a new Visit/Queue state.
- Automatic next-group assignment.
- Guaranteed priority for late Patient.
- NO_SHOW reopening.
- Platform-created requeue state.

## 12. Review Record

- Pass 1: lecturer branching
- Pass 2: UCM-12 success
- Pass 3: terminal NO_SHOW gate
- Pass 4: manual outcome Decision
- Pass 5: manual acceptance
- Pass 6: original group preservation
- Pass 7: manualHandling flag
- Pass 8: no numeric priority
- Pass 9: reschedule alternative
- Pass 10: NO_SHOW alternative
- Pass 11: NOT_COMPLETED alternative
- Pass 12: no reentry
- Pass 13: no new state
- Pass 14: visual branching
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
