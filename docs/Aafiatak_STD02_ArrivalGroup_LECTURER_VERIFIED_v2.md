# State Diagram — ArrivalGroup Lifecycle
## Aafiatak Medical Appointment Booking System — MVP State Diagram Specification

**Diagram ID:** `STD-02`  
**Deliverable:** UML State Diagram  
**Modeled Object:** `ArrivalGroup`  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** Project Specification §13.4; Class Diagram class ArrivalGroup  
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

`ArrivalGroup` has its own lifecycle independent from the parent `AvailabilityRelease`, with a reversible freeze and terminal closure.

Its State Diagram is useful because a group may have positive numeric remaining capacity while still being **not bookable** because of group/parent/time conditions.

## 4. Exact State Inventory

Render exactly:

1. `OPEN`
2. `FROZEN`
3. `CLOSED`

### State semantics

- `OPEN`: group lifecycle is open; actual bookability still depends on parent release, remaining capacity, and time eligibility.
- `FROZEN`: new holds are stopped while valid existing holds and confirmed Appointments are preserved.
- `CLOSED`: terminal for new-booking purposes.

**Lecturer-style decision:** no `do / ...` line is rendered because these are state permissions/semantics rather than distinct continuous activities.

## 5. Exact Transition Set

| From | To | Transition label |
|---|---|---|
| Initial | `OPEN` | completion transition (first defined group lifecycle state) |
| `OPEN` | `FROZEN` | `freeze group` |
| `FROZEN` | `OPEN` | `resume group` |
| `OPEN` | `CLOSED` | `close group` |
| `FROZEN` | `CLOSED` | `close group` |
| `CLOSED` | Final | completion |

### Important modeling note

The MVP defines `OPEN`, `FROZEN`, and `CLOSED` as the ArrivalGroup state set but does not define a separate pre-OPEN lifecycle state or a named event for entering `OPEN`. Therefore the Initial pseudostate connects to `OPEN` with an unlabeled/completion transition rather than inventing an initialization event. A group can still be non-bookable while `OPEN` if its parent release is not `PUBLISHED`, remaining capacity is not positive, or time eligibility fails.

## 6. Bookability Guard — Do Not Convert Into More States

A new ReservationHold may use an `OPEN` group only when all are true:

`[group remaining > 0 AND parent release = PUBLISHED AND enough time remains for the full hold window before group start]`

This is a **guard/bookability condition**, not additional states.

## 7. Binding Rules

- `OPEN <-> FROZEN` is reversible.
- `OPEN/FROZEN -> CLOSED`.
- `CLOSED` is terminal for new-booking purposes.
- Freeze/close does not rewrite confirmed Appointments.
- A valid pre-existing hold may complete only while its hold/time validity remains satisfied and the parent release is not cancelled.
- Sum of ArrivalGroup capacities equals the release's published digital capacity.
- Existing holds and confirmed Appointments are never automatically rebalanced between groups.
- Patient does not choose an arbitrary group; new booking attempts use the earliest currently bookable group.

## 8. Explicitly Forbidden States

Do not add:
- `EXHAUSTED`;
- `STALE`;
- `FULL`;
- `ACTIVE`;
- `PUBLISHED`;
- `CANCELLED`;
- `REOPENED`;
- `LATE`;
- `WAITING`.

Those concepts belong to indicators, parent release lifecycle, arrival/queue behavior, or other objects.


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

## 9. Deep Review Record

- Pass 1: one-Object lifecycle scope.
- Pass 2: exact three states.
- Pass 3: OPEN/FROZEN reversibility.
- Pass 4: CLOSED terminality.
- Pass 5: bookability-vs-state distinction.
- Pass 6: parent-release guard interaction.
- Pass 7: time-eligibility guard.
- Pass 8: existing hold preservation.
- Pass 9: no automatic rebalance.
- Pass 10: no Patient arbitrary group choice.
- Pass 11: indicator leakage audit.
- Pass 12: final MVP traceability.


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
