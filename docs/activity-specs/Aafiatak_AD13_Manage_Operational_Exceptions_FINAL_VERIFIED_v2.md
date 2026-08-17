# Activity Diagram — Manage Operational Exceptions
## Aafiatak Medical Appointment Booking System — MVP Activity Diagram Specification

**Diagram ID:** `AD-13`  
**Deliverable:** UML Activity Diagram  
**Use Case:** `Manage Operational Exceptions`  
**Traceability:** UCM-13; MUC-19/FAUC-36/BRUC-32..43; Project Specification §§23–24  
**Package:** Facility Administrator + Booking & Reception Staff  
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

1. Authorized facility actor is authenticated.
2. Supported unplanned event occurs after publication/during daily operation.
3. Event can be classified in approved exception scope and affected context can be identified.

## 7. Exact Node Inventory

The renderer must implement exactly the following semantic nodes. It may wrap text or adjust geometry, but must not rename, omit, merge, or invent business actions.

- `I` — **Initial Node:** Start
- `A01` — **Action:** Facility actor records operational event and doctor/session/release context
- `A02` — **Action:** Create OPEN OperationalException with approved type and link affected context
- `D01` — **Decision:** Exception type = SESSION_CANCELLED?
- `A03` — **Action:** Make affected session/release non-bookable and release active ReservationHolds
- `A04` — **Action:** Preserve all confirmed Appointments and identify affected unresolved set
- `A05` — **Action:** Present affected Appointments and relevant hold/capacity state
- `A06` — **Action:** Select one unresolved affected Appointment
- `D02` — **Decision:** Approved resolution path?
- `A07` — **Action:** Offer / secure suitable equivalent alternative after Patient communication using reschedule invariants
- `A08` — **Action:** Cancel Appointment from facility side and preserve history
- `D03` — **Decision:** Electronic amount collected?
- `A09` — **Action:** Initiate full collected-amount refund
- `A10` — **Action:** Record facility-cancellation outcome with no electronic refund
- `A11` — **Action:** Create documented support escalation for later Platform review
- `A12` — **Action:** Record completed resolution action / outcome for affected Appointment
- `A17` — **Action:** Keep OperationalException OPEN pending escalated resolution; do not close
- `D04` — **Decision:** More affected Appointments unresolved?
- `A13` — **Action:** Notify affected Patients through Notification Service when required
- `A14` — **Action:** Facility actor requests Close Operational Exception
- `D05` — **Decision:** Every affected Appointment has a completed documented action/outcome?
- `A15` — **Action:** Reject closure and identify remaining resolution requirement
- `A16` — **Action:** Close OperationalException and preserve audit trail
- `MEND` — **Merge:** End-path merge
- `F` — **Final Node:** End

## 8. Exact Control-Flow / Edge Table

| From | To | Guard | Meaning / rendering instruction |
|---|---|---|---|
| `I` | `A01` | — | Begin exception |
| `A01` | `A02` | — | Open exception |
| `A02` | `D01` | — | Special session-cancel handling |
| `D01` | `A03` | [Yes] | Session becomes non-bookable; release active holds |
| `A03` | `A04` | — | Confirmed Appointments preserved |
| `D01` | `A04` | [No] | Identify affected set |
| `A04` | `A05` | — | Review impact |
| `A05` | `A06` | — | Process affected Appointments one-by-one |
| `A06` | `D02` | — | Choose approved resolution |
| `D02` | `A07` | [Equivalent alternative] | Same-service/same-terms safe path |
| `A07` | `A12` | — | Record completed outcome |
| `D02` | `A08` | [Facility cancellation] | Cancel by facility |
| `A08` | `D03` | — | Refund decision |
| `D03` | `A09` | [Paid] | Full refund only |
| `A09` | `A12` | — | Record completed outcome |
| `D03` | `A10` | [No electronic payment] | No electronic refund |
| `A10` | `A12` | — | Record completed outcome |
| `D02` | `A11` | [Escalation] | Document support escalation |
| `A11` | `A17` | — | Escalation is not a completed resolution |
| `A17` | `MEND` | — | End current activity with exception still OPEN |
| `A12` | `D04` | — | Check remaining unresolved set |
| `D04` | `A06` | [Yes] | Loop to next affected Appointment |
| `D04` | `A13` | [No] | All completed outcomes documented; notify if required |
| `A13` | `A14` | — | Request closure |
| `A14` | `D05` | — | Strict closure gate |
| `D05` | `A15` | [No] | Cannot close |
| `A15` | `A06` | — | Return to unresolved Appointment handling |
| `D05` | `A16` | [Yes] | Close and audit |
| `A16` | `MEND` | — | Closed-success path ends |
| `MEND` | `F` | — | Activity final |

## 9. Branch Semantics

### Conflict resolution
For `CONFLICT_DETECTED`, approved paths are equivalent alternative after communication, facility cancellation/full refund if paid, or documented escalation.

### SESSION_CANCELLED
Session/release becomes non-bookable; active holds are released; confirmed Appointments remain preserved and each needs documented resolution.

### Notifications
When needed, use Notification Service/system notifications, not WhatsApp.

### Closure
The exception cannot close while any affected Appointment lacks a **completed** documented action/outcome.

### Escalation does not satisfy closure by itself
A documented support escalation is a valid action, but it is not automatically a completed resolution. The OperationalException stays OPEN until the later escalation/review path produces the required affected-Appointment outcome.

### Capacity boundary
Never import free internal facility capacity into the same published release as a conflict solution.


## 10. Binding Business Rules

- Doctor does not record delay/absence through Doctor interface; facility staff records the OperationalException.
- Platform Administrator appears only in later escalation review, not daily operational handling.
- Facility-responsible paid cancellation starts full refund.

## 11. Explicitly Forbidden in This Diagram

- Silent deletion of affected Appointments/history.
- Reverse import of internal capacity.
- Partial refund.
- Doctor as exception-recording actor.
- Platform Administrator running daily facility resolution.
- Closing with unresolved affected Appointment.

## 12. Review Record

- Pass 1: lecturer branching/loop
- Pass 2: UCM-13 main flow
- Pass 3: supported exception context
- Pass 4: SESSION_CANCELLED
- Pass 5: affected-Appointment loop
- Pass 6: three resolution paths
- Pass 7: same-term alternative
- Pass 8: facility cancellation
- Pass 9: full refund
- Pass 10: escalation
- Pass 11: notification boundary
- Pass 12: strict closure gate
- Pass 13: no reverse capacity
- Pass 14: role boundaries
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
