# State Diagram — ReservationHold Lifecycle
## Aafiatak Medical Appointment Booking System — MVP State Diagram Specification

**Diagram ID:** `STD-03`  
**Deliverable:** UML State Diagram  
**Modeled Object:** `ReservationHold`  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** Project Specification §§14, 19.1, 19.7; booking flow §16  
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

`ReservationHold` is a core concurrency object with a short but strict lifecycle. Its terminal-state rules protect Aafiatak from double booking.

## 4. Exact State Inventory

Render exactly:

1. `ACTIVE`
2. `CONSUMED`
3. `EXPIRED`
4. `RELEASED`

### Supported `do` activity

#### `ACTIVE`
`do / protect one capacity unit and maintain countdown`

The exact default hold duration is an intentionally unresolved product decision. Do not place `3 minutes`, `5 minutes`, or another fixed default in the diagram.

`CONSUMED`, `EXPIRED`, and `RELEASED` are terminal for that hold.

## 5. Exact Transition Set

| From | To | Transition label |
|---|---|---|
| Initial | `ACTIVE` | `create hold [ArrivalGroup is currently bookable] / protect one capacity unit` |
| `ACTIVE` | `CONSUMED` | `confirm full-payment booking [trusted success & hold valid & before group start & release not CANCELLED] / create CONFIRMED Appointment atomically` |
| `ACTIVE` | `CONSUMED` | `confirm pay-at-facility booking [booking complete & hold valid & before group start & release not CANCELLED] / create CONFIRMED Appointment atomically` |
| `ACTIVE` | `EXPIRED` | `hold time expires / release protected capacity` |
| `ACTIVE` | `RELEASED` | `Patient abandons or cancels booking / release protected capacity` |
| `ACTIVE` | `RELEASED` | `parent release is CANCELLED / release protected capacity` |
| `CONSUMED` | Final | completion |
| `EXPIRED` | Final | completion |
| `RELEASED` | Final | completion |

## 6. Binding Rules

- ACTIVE hold prevents another user from owning the same capacity unit.
- Hold identifies one selected ArrivalGroup/window.
- A hold expires automatically.
- It cannot be extended arbitrarily by Patient.
- It cannot be consumed at/after ArrivalGroup start.
- It cannot be consumed after parent release becomes `CANCELLED`.
- FULL_PAYMENT_REQUIRED requires trusted payment success before consumption.
- PAY_AT_FACILITY creates no PaymentIntent.
- Consumption occurs exactly once.
- Retry/idempotency must not create duplicate Appointments.
- Terminal states have no transition back to `ACTIVE`.

## 7. Explicitly Forbidden States / Transitions

Do not add:
- `PENDING`;
- `PAID`;
- `CONFIRMED`;
- `CANCELLED`;
- `PROCESSING`;
- `UNDER_REVIEW`;
- `ACTIVE -> ACTIVE` extension;
- `EXPIRED -> ACTIVE`;
- `RELEASED -> ACTIVE`;
- `CONSUMED -> ACTIVE`.

Payment and Appointment states belong to their own independent objects.


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

- Pass 1: lecturer object-state rule.
- Pass 2: exact four-state extraction.
- Pass 3: ACTIVE concurrency semantics.
- Pass 4: two booking-policy consumption guards.
- Pass 5: automatic expiry.
- Pass 6: explicit release causes.
- Pass 7: arrival-group start boundary.
- Pass 8: parent cancellation boundary.
- Pass 9: terminal-state audit.
- Pass 10: hold-duration open-decision audit.
- Pass 11: independent Payment/Appointment lifecycle audit.
- Pass 12: idempotency/double-booking audit.
- Pass 13: final transition-direction check.


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
