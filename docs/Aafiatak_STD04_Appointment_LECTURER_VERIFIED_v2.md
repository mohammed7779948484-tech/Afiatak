# State Diagram — Appointment Lifecycle
## Aafiatak Medical Appointment Booking System — MVP State Diagram Specification

**Diagram ID:** `STD-04`  
**Deliverable:** UML State Diagram  
**Modeled Object:** `Appointment`  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** Project Specification §§16.4, 17, 19.2, 19.7  
**Semantic status:** FINAL REVIEWED — ready for diagram execution

---


## 1. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative current MVP product truth.
2. Lecturer UML PDF and the lecturer-course notes supplied for this project — academic State Diagram method and notation.
3. Reviewed Aafiatak Use Case Modeling and the approved Sequence work — behavioral traceability only.
4. `Aafiatak_MVP_Class_Diagram_Spec_FINAL_VERIFIED_v2.md` — approved domain/class names and lifecycle separation.
5. This file — exact execution contract for this State Diagram.
6. Rendering/tooling — presentation mechanics only.

If a transition, state, guard, or action is not supported by the authoritative MVP, do not invent it.

All visible labels must be **English**.

## 2. Lecturer State-Diagram Rules Applied

The lecturer PDF identifies **State Diagram** as a required UML diagram (page 2 list; page 9 heading), but the available PDF page 9 does not contain a readable State-Diagram example. Therefore the exact drawing mechanics below come only from the lecturer-course explanation supplied with this project, not from an invented reconstruction of a missing PDF figure.

The lecturer-course explanation describes a State Diagram as a diagram for **one Object** whose lifecycle/state changes are important, ambiguous, or complex.

The lecturer-course notes supplied for this project emphasize:

1. Choose one Object.
2. Extract its valid States.
3. Determine the valid Transitions.
4. Add an Initial State.
5. Add an End/Final State.
6. Label state changes by the **Event** that causes them.
7. Add a **Guard Condition** when the transition is conditional.
8. Add an **Action** when an operation occurs during the transition.
9. When useful and supported, show `do / ...` behavior inside a State to explain what happens while the Object remains in that State.

Use this transition-label form when all parts exist:

`event [guard] / action`

If there is no supported guard or action, omit that part rather than inventing one.

### Required notation

- Initial pseudostate: filled black circle.
- State: rounded rectangle.
- Transition: solid directed arrow.
- Guard: `[condition]`.
- Transition action: `/ action`.
- In-state activity: `do / activity` only when explicitly supported and useful.
- Final pseudostate: UML final/bullseye symbol.

### Do not mix diagram types

Do **not** place:
- Actors or Sequence lifelines;
- Use Case ellipses;
- `<<include>>` / `<<extend>>`;
- Class attributes/operations compartments;
- Association/Aggregation/Composition;
- database tables;
- API/controller/service architecture;
- Activity swimlanes

inside these State Diagrams.

### Lecturer-style simplicity

The target is the lecturer's taught style, not a demonstration of every advanced UML feature.

Therefore:
- keep one Object lifecycle per sheet;
- render the **main state machine only**, with no explanatory legend;
- show State names, Initial/Final nodes, transitions, and concise event/guard/action labels;
- use `do / ...` only when the source supports a real activity that occurs while the Object remains in that State; do not use `do /` merely as a description of what the State means;
- prefer direct transitions with event/guard/action labels;
- do not add composite states, orthogonal regions, history pseudostates, or other advanced notation unless the lecturer material or product explicitly requires them;
- do not number states merely for decoration.

## 3. Why This Object Requires a State Diagram

The Appointment lifecycle is intentionally small because booking commitment, payment, visit, queue, and no-show are modeled separately.

This diagram is particularly important to prevent incorrect states from being added to Appointment.

## 4. Exact State Inventory

Render exactly:

1. `CONFIRMED`
2. `CANCELLED_BY_PATIENT`
3. `CANCELLED_BY_FACILITY`

No pending approval/rejection state exists.

### State semantics

`CONFIRMED` preserves the booking commitment and its historical booking snapshot.

**Lecturer-style decision:** no `do / ...` line is rendered because preserving a snapshot is a state invariant/responsibility, not a continuous activity.

## 5. Exact Transition Set

| From | To | Transition label |
|---|---|---|
| Initial | `CONFIRMED` | `booking requirements satisfied / create Appointment with immutable booking snapshot` |
| `CONFIRMED` | `CANCELLED_BY_PATIENT` | `Patient cancels [not checked in & group window not started] / preserve history and release same-group capacity when eligible` |
| `CONFIRMED` | `CANCELLED_BY_FACILITY` | `Facility cancels [operationally required] / preserve history and start full refund if paid` |
| `CANCELLED_BY_PATIENT` | Final | completion |
| `CANCELLED_BY_FACILITY` | Final | completion |

### Initial-transition clarification

For `FULL_PAYMENT_REQUIRED`, booking requirements include trusted payment success while the ReservationHold remains valid.

For `PAY_AT_FACILITY`, booking requirements include completion of the final booking flow while the ReservationHold remains valid.

Do not split these into separate Appointment states.


## 5.1 Important Non-Transition Behavior

**Rescheduling is deliberately NOT drawn as a state transition.**

A successful in-place reschedule:
- keeps the Appointment in `CONFIRMED`;
- requires the same `ServiceOffering`;
- preserves the same saved financial/booking terms;
- secures valid destination capacity first;
- writes `AppointmentStatusHistory`.

Because the Appointment state does not change, the lecturer-style State Diagram should not use a self-loop merely to depict an operation that leaves the Object in the same state. Keep this rule as a compact note beside `CONFIRMED` if needed.

## 6. Binding Rules

- Appointment begins directly as `CONFIRMED`.
- There is no manual facility-approval state.
- Rescheduling does **not** change Appointment status.
- Successful in-place reschedule stays `CONFIRMED` and records history.
- Patient self-cancellation is blocked after check-in or once the assigned group window starts.
- Facility-side cancellation remains available when operationally necessary.
- Cancellation states are terminal.
- Check-in, IN_SERVICE, COMPLETED, NOT_COMPLETED and NO_SHOW belong to `VisitInstance`, not Appointment.
- Payment/refund states belong to `PaymentIntent`.
- Cancellation/refund policy is taken from the Appointment's saved snapshot, not current changed configuration.

## 7. Explicitly Forbidden States

Do not add:
- `PENDING`;
- `PENDING_APPROVAL`;
- `APPROVED`;
- `REJECTED`;
- `RESCHEDULED`;
- `PAID`;
- `CHECKED_IN`;
- `IN_SERVICE`;
- `COMPLETED`;
- `NOT_COMPLETED`;
- `NO_SHOW`;
- `REFUND_PENDING`;
- `REFUNDED`.

These belong to other lifecycles or do not exist.


## Lecturer-Style Visible Diagram Contract

The final rendered diagram itself must remain simple, like the lecturer's explained State-Diagram method.

Visible content should contain only:
- exact diagram title;
- Initial pseudostate;
- approved State names;
- supported `do / ...` activity only where this file explicitly retains one;
- solid directed transitions;
- concise `event [guard] / action` labels;
- Final pseudostate(s).

Do **not** render the internal QA sections, source references, Deep Review record, state IDs, transition table columns, or forbidden-state lists inside the diagram.

Do **not** add:
- Actor;
- lifeline;
- message numbering;
- legend;
- advanced state-machine notation;
- a separate Decision/Choice diamond unless a source-backed decision cannot be expressed cleanly as guards on transitions.

Guards such as `[condition]` are preferred for branching, matching the lecturer's explanation of Guard Condition.

## Visual Contract

- One State Diagram per page/artboard.
- White or very light neutral background.
- Dark navy/charcoal linework and text.
- Restrained academic styling.
- Large exact title at top.
- Initial state positioned before the first lifecycle State.
- Terminal states clearly separated near the end.
- Transition labels must not overlap arrows or state boxes.
- Keep arrows short, direct, and easy to trace.
- Use a consistent rounded-rectangle State style across the complete Aafiatak State Diagram family.
- If `do / ...` is used, separate the State name from the internal activity cleanly.
- Avoid legends unless the lecturer explicitly requires one.
- Ensure normal academic-report readability; do not use tiny text.

## 8. Deep Review Record

- Pass 1: independent lifecycle boundary.
- Pass 2: exact three-state inventory.
- Pass 3: direct CONFIRMED creation.
- Pass 4: no manual-approval drift.
- Pass 5: reschedule correctly excluded as a state transition.
- Pass 6: same-service/same-terms guard.
- Pass 7: patient-cancellation guard.
- Pass 8: facility-cancellation/refund action boundary.
- Pass 9: terminal cancellations.
- Pass 10: Visit-state leakage audit.
- Pass 11: Payment-state leakage audit.
- Pass 12: snapshot precedence audit.
- Pass 13: final traceability.


## Mandatory QA Gates

Before delivery:

1. Verify the diagram models exactly **one Object**.
2. Verify every visible State name is approved for that Object.
3. Verify no status from another lifecycle has leaked into this diagram.
4. Verify Initial and Final pseudostates are present where specified.
5. Verify every transition direction.
6. Verify every Event label.
7. Verify every Guard is supported by the MVP.
8. Verify every `/ action` is supported and does not create a new business rule.
9. Verify every `do / ...` activity is supported.
10. Verify terminal states have no business transition back into the lifecycle.
11. Verify no advanced UML notation was invented.
12. Render the SVG/PNG/PDF.
13. Open the actual rendered output and inspect it visually.
14. Compare the render against this MD line-by-line/item-by-item.
15. Perform semantic, notation, and visual correction passes.
16. Final visual status: `awaiting-user-approval`.

Do not self-approve the final visual as perfect without user inspection.
