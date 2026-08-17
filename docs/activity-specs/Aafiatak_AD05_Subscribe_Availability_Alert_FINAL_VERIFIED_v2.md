# Activity Diagram — Subscribe to Availability Alert
## Aafiatak Medical Appointment Booking System — MVP Activity Diagram Specification

**Diagram ID:** `AD-05`  
**Deliverable:** UML Activity Diagram  
**Use Case:** `Subscribe to Availability Alert`  
**Traceability:** UCM-05; MUC-11/PUC-15; Project Specification §§15–15.1  
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

1. Patient is authenticated.
2. Relevant service/doctor/date/release context is selected.
3. Suitable capacity is currently unavailable or protected by another ACTIVE hold.

## 7. Exact Node Inventory

The renderer must implement exactly the following semantic nodes. It may wrap text or adjust geometry, but must not rename, omit, merge, or invent business actions.

- `I` — **Initial Node:** Start
- `A01` — **Action:** Patient chooses Notify Me When Available
- `A02` — **Action:** Revalidate current Aafiatak bookability
- `D01` — **Decision:** Capacity now bookable?
- `A03` — **Action:** Direct Patient to normal booking; create no hidden reservation
- `A04` — **Action:** Create AvailabilityAlertSubscription for Patient/context
- `A05` — **Action:** Confirm subscription as interest only — no hold / queue / priority
- `A06` — **Action:** Wait for approved capacity-return event, successful Patient booking, or session end
- `D02` — **Decision:** Which source-supported event occurs?
- `A07` — **Action:** Expire corresponding subscription after successful Patient booking
- `A08` — **Action:** Expire subscription when session ends
- `A09` — **Action:** Detect zero-to-positive bookable capacity from approved Aafiatak event
- `A10` — **Action:** Notify eligible subscriptions through Notification Service
- `A11` — **Action:** Patient competes through normal booking; first valid ReservationHold wins
- `D03` — **Decision:** Patient successfully books?
- `A12` — **Action:** Keep subscription lifecycle subject to duplicate-notification suppression until booking/session end
- `MEND` — **Merge:** End-path merge
- `F` — **Final Node:** End

## 8. Exact Control-Flow / Edge Table

| From | To | Guard | Meaning / rendering instruction |
|---|---|---|---|
| `I` | `A01` | — | Begin subscription |
| `A01` | `A02` | — | Revalidate availability |
| `A02` | `D01` | — | Check race with returning capacity |
| `D01` | `A03` | [Yes] | Normal booking opportunity; no alert reservation |
| `A03` | `MEND` | — | Subscription not required |
| `D01` | `A04` | [No] | Create subscription |
| `A04` | `A05` | — | Confirm non-reserving semantics |
| `A05` | `A06` | — | Wait for lifecycle event |
| `A06` | `D02` | — | Classify event |
| `D02` | `A07` | [Patient books successfully] | Expire subscription |
| `A07` | `MEND` | — | Ends |
| `D02` | `A08` | [Session ends] | Expire subscription |
| `A08` | `MEND` | — | Ends |
| `D02` | `A09` | [Approved capacity returns] | Eligible alert event |
| `A09` | `A10` | — | Send in-app/system alert |
| `A10` | `A11` | — | No priority; normal race |
| `A11` | `D03` | — | Booking outcome |
| `D03` | `A07` | [Booked] | Expire after booking |
| `D03` | `A12` | [Not booked] | Subscription remains governed by lifecycle/duplicate-suppression rules |
| `A12` | `A06` | — | Return to waiting lifecycle |
| `MEND` | `F` | — | Activity final |

## 9. Branch Semantics

### Approved capacity return
Alert may arise from hold expiry/release, eligible same-group seat republication, or documented technical correction.

### Forbidden source
Free internal facility capacity is not imported into Aafiatak and must not trigger an alert.

### Alert semantics
Notification never reserves capacity, grants priority, or creates queue position.

### Duplicate suppression
Do not send repetitive/annoying duplicate availability notifications.


## 10. Binding Business Rules

- Subscription expires on session end or successful relevant booking.
- After an alert, normal ReservationHold competition applies.
- General alert notifications use Notification Service/system channel, not WhatsApp.

## 11. Explicitly Forbidden in This Diagram

- Reservation/priority semantics for alert.
- Automatic capacity import from internal facility schedule.
- Queue position created by alert.
- WhatsApp general alert delivery.

## 12. Review Record

- Pass 1: lecturer flow
- Pass 2: UCM-05 creation
- Pass 3: availability revalidation
- Pass 4: capacity race
- Pass 5: subscription semantics
- Pass 6: lifecycle wait
- Pass 7: approved alert causes
- Pass 8: no reverse import
- Pass 9: normal booking race
- Pass 10: expiry rules
- Pass 11: notification boundary
- Pass 12: loop clarity
- Pass 13: no Fork/Join
- Pass 14: visual complexity control
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
