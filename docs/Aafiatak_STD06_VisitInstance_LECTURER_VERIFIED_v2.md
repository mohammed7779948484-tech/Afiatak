# State Diagram — VisitInstance Lifecycle
## Aafiatak Medical Appointment Booking System — MVP State Diagram Specification

**Diagram ID:** `STD-06`  
**Deliverable:** UML State Diagram  
**Modeled Object:** `VisitInstance`  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** Project Specification §§19.4, 19.7, 20, 22  
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

`VisitInstance` represents what actually happens on the service day and intentionally separates operational outcomes from Appointment state.

It has normal, exception, correction, late-arrival, and terminal paths, making it one of the most important State Diagrams in the project.

## 4. Exact State Inventory

Render exactly:

1. `CREATED`
2. `CHECKED_IN`
3. `IN_SERVICE`
4. `COMPLETED`
5. `NOT_COMPLETED`
6. `NO_SHOW`

### State semantics and supported `do` activity

- `CREATED`: VisitInstance exists before valid check-in or a terminal no-show decision.
- `CHECKED_IN`: valid facility-staff check-in has been recorded.
- `IN_SERVICE`: service is currently in progress.
- `COMPLETED`, `NOT_COMPLETED`, `NO_SHOW`: terminal operational outcomes.

Only `IN_SERVICE` retains a lecturer-style continuous activity:

`do / service in progress`

No `do / ...` line is rendered in `CREATED` or `CHECKED_IN` because their source-backed meaning is a state condition, not a distinct continuous activity.

## 5. Exact Transition Set

| From | To | Transition label |
|---|---|---|
| Initial | `CREATED` | `first relevant service-day operational event / create VisitInstance` |
| `CREATED` | `CHECKED_IN` | `Reception registers arrival / record arrival and create/activate QueueEntry` |
| `CREATED` | `CHECKED_IN` | `Reception accepts late arrival [NO_SHOW not recorded] / record late acceptance and manual queue handling` |
| `CREATED` | `NO_SHOW` | `ArrivalGroup window ends [no valid check-in] / facility staff records no-show` |
| `CHECKED_IN` | `IN_SERVICE` | `facility staff records service start` |
| `CHECKED_IN` | `NOT_COMPLETED` | `service cannot be completed / record non-completion` |
| `IN_SERVICE` | `COMPLETED` | `facility staff records operational completion` |
| `IN_SERVICE` | `NOT_COMPLETED` | `service cannot be completed / record non-completion` |
| `CHECKED_IN` | `CREATED` | `correct erroneous check-in [before service start] / remove QueueEntry and audit reason` |
| `COMPLETED` | Final | completion |
| `NOT_COMPLETED` | Final | completion |
| `NO_SHOW` | Final | completion |

## 6. Binding Rules

- Patient cannot self-check-in.
- Facility staff, not Doctor, changes VisitInstance states.
- `NO_SHOW` may be recorded only after assigned ArrivalGroup window ends without valid check-in.
- Once validly `NO_SHOW`, the VisitInstance is not reopened for late check-in.
- Accepted late Patient keeps original Appointment and original ArrivalGroup.
- Accepted late Patient is flagged for manual queue handling; this is not another VisitInstance State.
- Erroneous check-in correction is allowed only before service starts and must be audited.
- VisitInstance contains no diagnosis, prescriptions, test results, or clinical notes.

## 7. Explicitly Forbidden States / Transitions

Do not add:
- `WAITING`;
- `CALLED`;
- `DONE`;
- `REMOVED`;
- `LATE`;
- `REENTERED`;
- `REQUEUED`;
- `CANCELLED_BY_PATIENT`;
- `CANCELLED_BY_FACILITY`;
- `PAID`;
- `NO_SHOW -> CHECKED_IN`;
- Doctor-triggered `IN_SERVICE`/`COMPLETED`/`NOT_COMPLETED`/`NO_SHOW`.

Queue states belong to QueueEntry; cancellation belongs to Appointment.


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

- Pass 1: exact six states.
- Pass 2: Appointment/Visit separation.
- Pass 3: normal path.
- Pass 4: NOT_COMPLETED paths.
- Pass 5: NO_SHOW timing guard.
- Pass 6: erroneous check-in correction.
- Pass 7: late-arrival accepted path.
- Pass 8: terminal NO_SHOW no-reopen rule.
- Pass 9: original-group preservation.
- Pass 10: manual-handling flag vs State distinction.
- Pass 11: Doctor permission boundary.
- Pass 12: clinical-data exclusion.
- Pass 13: final transition audit.


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
