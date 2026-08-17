# State Diagram — QueueEntry Lifecycle
## Aafiatak Medical Appointment Booking System — MVP State Diagram Specification

**Diagram ID:** `STD-07`  
**Deliverable:** UML State Diagram  
**Modeled Object:** `QueueEntry`  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** Project Specification §§19.5, 19.7, 20–22  
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

`QueueEntry` has a small but explicit lifecycle separate from VisitInstance. This prevents queue-call state from being confused with service state.

## 4. Exact State Inventory

Render exactly:

1. `WAITING`
2. `CALLED`
3. `DONE`
4. `REMOVED`

### State semantics

`WAITING` means the QueueEntry remains in the approved Aafiatak waiting context for the original ArrivalGroup.

**Lecturer-style decision:** no `do / ...` line is rendered because this is the meaning of the state rather than a distinct continuous activity.

For normal on-time Patients, queue ordering is based on:
1. actual check-in time;
2. earlier Appointment `confirmed_at` as tie-breaker.

For accepted late Patients, the QueueEntry remains within this same state model but uses `manualHandling`; it is excluded from automatic numeric queue-position calculation. On the Initial -> `WAITING` transition, `manualHandling` is set only for the accepted-late context; it is not a separate State.

## 5. Exact Transition Set

| From | To | Transition label |
|---|---|---|
| Initial | `WAITING` | `valid or accepted-late check-in / create or activate QueueEntry` |
| `WAITING` | `CALLED` | `call next Patient [entry currently callable]` |
| `CALLED` | `DONE` | `queue handling completed / mark entry done` |
| `WAITING` | `REMOVED` | `audited correction/removal [valid operational reason] / record reason` |
| `CALLED` | `REMOVED` | `audited correction/removal [valid operational reason] / record reason` |
| `DONE` | Final | completion |
| `REMOVED` | Final | completion |

## 6. Binding Rules

- Normal lifecycle is `WAITING -> CALLED -> DONE`.
- `WAITING` or `CALLED` may become `REMOVED` only through audited operational correction/removal.
- `DONE` and `REMOVED` are terminal.
- No automatic re-entry/requeue mechanism exists.
- Full online payment grants no queue priority.
- Doctor may identify/call next Patient but may not change VisitInstance states.
- Manual handling for accepted late arrival is a flag/mode, not a QueueEntry state.
- Aafiatak queue covers Aafiatak patients inside their ArrivalGroup; it does not claim to merge the facility's full internal queue.

## 7. Event/Guard Clarification

`[entry is currently callable]` means the selected QueueEntry still belongs to the valid waiting context and has not already become terminal/removed.

Do not invent a numeric priority score or a payment-based guard.

## 8. Explicitly Forbidden States / Transitions

Do not add:
- `CHECKED_IN`;
- `IN_SERVICE`;
- `COMPLETED` as QueueEntry state;
- `NO_SHOW`;
- `LATE`;
- `MANUAL_HANDLING` as a state;
- `REENTERED`;
- `REQUEUED`;
- `DONE -> WAITING`;
- `REMOVED -> WAITING`;
- payment-priority transitions.


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

- Pass 1: exact four states.
- Pass 2: normal queue path.
- Pass 3: audited removal paths.
- Pass 4: terminal-state audit.
- Pass 5: Visit/Queue separation.
- Pass 6: Doctor permission boundary.
- Pass 7: normal ordering rule.
- Pass 8: payment-no-priority rule.
- Pass 9: accepted-late manual handling.
- Pass 10: no re-entry/requeue.
- Pass 11: internal-facility-queue boundary.
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
