# State Diagram — AvailabilityRelease Lifecycle
## Aafiatak Medical Appointment Booking System — MVP State Diagram Specification

**Diagram ID:** `STD-01`  
**Deliverable:** UML State Diagram  
**Modeled Object:** `AvailabilityRelease`  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** Project Specification §13.3; Class Diagram class AvailabilityRelease  
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

`AvailabilityRelease` has a clearly defined lifecycle with:
- an editable pre-publication state;
- a live bookable state;
- a reversible temporary freeze;
- two terminal non-bookable outcomes.

It is therefore a strong lecturer-style State Diagram candidate.

`EXHAUSTED` and `STALE` must **not** be rendered as States. They are explicitly defined as **derived indicators**, not lifecycle states.

## 4. Exact State Inventory

Render exactly these five States:

1. `DRAFT`
2. `PUBLISHED`
3. `FROZEN`
4. `CLOSED`
5. `CANCELLED`

### State semantics

- `DRAFT`: editable pre-publication state; Patient capacity cannot be consumed.
- `PUBLISHED`: published release; new holds are possible only when the target ArrivalGroup is also bookable.
- `FROZEN`: new holds/bookings are temporarily stopped while valid existing holds and confirmed Appointments are preserved.
- `CLOSED`: terminal for new-booking purposes.
- `CANCELLED`: terminal session/release cancellation; new holds are forbidden, active holds are released, and confirmed Appointments require OperationalException resolution.

**Lecturer-style decision:** no `do / ...` line is rendered in these States because the source gives state permissions/semantics, not a distinct continuous in-state activity.

## 5. Exact Transition Set

| From | To | Transition label | Meaning |
|---|---|---|---|
| Initial | `DRAFT` | `create AvailabilityRelease` | A new release starts as draft configuration |
| `DRAFT` | `PUBLISHED` | `publish [configuration valid] / freeze published booking terms` | Publication makes the release govern new bookings |
| `PUBLISHED` | `FROZEN` | `freeze` | Temporarily stops new holds/bookings |
| `FROZEN` | `PUBLISHED` | `resume publication` | Reversible freeze returns the release to published operation |
| `PUBLISHED` | `CLOSED` | `close` | Administrative/session completion closure |
| `FROZEN` | `CLOSED` | `close` | Frozen release may be closed |
| `PUBLISHED` | `CANCELLED` | `cancel / release active holds` | Session/release cancellation |
| `FROZEN` | `CANCELLED` | `cancel / release active holds` | Frozen session/release may be cancelled |
| `CLOSED` | Final | completion | State machine terminates for new-booking lifecycle |
| `CANCELLED` | Final | completion | State machine terminates for new-booking lifecycle |

### Guard clarification

The publication guard is intentionally high-level:

`[release configuration is valid]`

Its product-backed meaning includes the approved pre-publication configuration, including ArrivalGroups/capacity consistency. Do not invent a new validation algorithm or numeric rule beyond the project specification.

## 6. Binding Rules

- Allowed lifecycle transitions are exactly:
  `DRAFT -> PUBLISHED`
  `PUBLISHED <-> FROZEN`
  `PUBLISHED/FROZEN -> CLOSED | CANCELLED`
- `CLOSED` and `CANCELLED` must never reopen into a bookable state.
- Published capacity cannot be increased after transition to `PUBLISHED`.
- Publication freezes amount, currency, booking policy, cancellation/refund policy, and no-show policy for that release.
- `FROZEN` preserves valid existing holds and confirmed Appointments.
- Administrative close does not by itself invalidate a valid pre-existing hold; such a hold may complete only if its own validity/time rules and parent cancellation rules still permit it.
- `CANCELLED` releases active holds and requires documented handling of confirmed Appointments.
- History is preserved; Final does not mean record deletion.

## 7. Explicitly Forbidden States / Transitions

Do not add:
- `EXHAUSTED` as a State;
- `STALE` as a State;
- `ACTIVE`;
- `OPEN`;
- `REOPENED`;
- `COMPLETED`;
- `ARCHIVED`;
- `DRAFT -> FROZEN`;
- `CLOSED -> PUBLISHED`;
- `CANCELLED -> PUBLISHED`;
- a `+1 capacity` transition.


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

- Pass 1: lecturer one-Object State Diagram rule.
- Pass 2: exact lifecycle state extraction from §13.3.
- Pass 3: derived-indicator exclusion (`EXHAUSTED`, `STALE`).
- Pass 4: allowed-transition audit.
- Pass 5: reversible freeze rule.
- Pass 6: terminal CLOSED/CANCELLED audit.
- Pass 7: published-term immutability.
- Pass 8: hold-preservation/cancellation interaction.
- Pass 9: capacity-increase prohibition.
- Pass 10: `do /` activity support audit.
- Pass 11: guard/action syntax audit.
- Pass 12: final cross-check against MVP scope.


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
