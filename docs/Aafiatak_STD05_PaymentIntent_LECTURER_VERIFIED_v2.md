# State Diagram — PaymentIntent Lifecycle
## Aafiatak Medical Appointment Booking System — MVP State Diagram Specification

**Diagram ID:** `STD-05`  
**Deliverable:** UML State Diagram  
**Modeled Object:** `PaymentIntent`  
**Visible language:** English only  
**Scope:** Current approved MVP only  
**Traceability:** Project Specification §§18, 19.3, 19.7  
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

`PaymentIntent` has the richest financial state model in the MVP and must remain independent from Appointment.

The State Diagram must be conservative: the authoritative MVP lists all supported States but does **not** fully enumerate every possible reconciliation transition out of `UNDER_REVIEW`. Do not invent unsupported resolution arrows merely to make the diagram symmetrical.

## 4. Exact State Inventory

Render exactly:

1. `CREATED`
2. `PROCESSING`
3. `SUCCEEDED`
4. `FAILED`
5. `EXPIRED`
6. `UNDER_REVIEW`
7. `REFUND_PENDING`
8. `REFUNDED`

### Supported `do` activities

#### `PROCESSING`
`do / await trusted gateway result`

#### `UNDER_REVIEW`
`do / await documented reconciliation`

#### `REFUND_PENDING`
`do / await full-refund completion`

## 5. Approved Transition Set

Render the transitions below.

| From | To | Transition label | Evidence basis |
|---|---|---|---|
| Initial | `CREATED` | `create PaymentIntent [FULL_PAYMENT_REQUIRED AND valid booking attempt]` | Every electronic attempt creates an independent intent |
| `CREATED` | `PROCESSING` | `start gateway payment` | Payment processing lifecycle |
| `CREATED` | `EXPIRED` | `payment attempt expires before completion` | Intent has expiry and EXPIRED state |
| `PROCESSING` | `SUCCEEDED` | `trusted gateway confirms success` | Browser return alone is not truth |
| `PROCESSING` | `FAILED` | `trusted gateway confirms failure` | FAILED is supported gateway outcome |
| `PROCESSING` | `EXPIRED` | `payment attempt expires` | EXPIRED supported |
| `PROCESSING` | `UNDER_REVIEW` | `payment result cannot be safely resolved / record reconciliation case` | outage/delay/unresolved result cases |
| `SUCCEEDED` | `UNDER_REVIEW` | `booking completion or safe recovery remains unresolved / move payment case to review` | critical success-without-appointment handling |
| `SUCCEEDED` | `REFUND_PENDING` | `full refund required / initiate refund` | facility cancellation/conflict, saved Patient policy, or saved no-show policy |
| `REFUND_PENDING` | `REFUNDED` | `trusted refund completion` | full refund lifecycle |
| `FAILED` | Final | completion |
| `EXPIRED` | Final | completion |
| `REFUNDED` | Final | completion |

## 6. Intentionally Unspecified Reconciliation Exits

The authoritative MVP does not provide a complete formal transition table for every possible resolution out of `UNDER_REVIEW`.

Therefore:

- do **not** invent `UNDER_REVIEW -> SUCCEEDED`;
- do **not** invent `UNDER_REVIEW -> FAILED`;
- do **not** invent `UNDER_REVIEW -> REFUNDED`;

unless a future authoritative project decision defines the exact reconciliation result transitions.

The diagram should leave `UNDER_REVIEW` visibly non-terminal/pending and may attach a small note:

`Exact reconciliation exit transitions are intentionally not fixed by the current MVP.`

This is more accurate than fabricating a lifecycle.

### Visible handling of `UNDER_REVIEW`

Render `UNDER_REVIEW` as a real non-terminal State with **no invented outgoing transition** in the current diagram. Do not connect it to Final. Do not invent a recovery destination. The current MVP intentionally does not fix those reconciliation exit transitions.

## 7. Important Lifecycle Rules

- Electronic PaymentIntent exists only for `FULL_PAYMENT_REQUIRED`.
- `PAY_AT_FACILITY` has **no PaymentIntent**; `DUE_AT_FACILITY` is a UI presentation state, not a PaymentIntent state.
- At most one non-terminal PaymentIntent may be active for one ReservationHold.
- Client retry must not automatically create a duplicate charge attempt.
- Ordinary facility users cannot force payment transitions.
- Trusted webhook/query result, not browser/app return, governs payment result.
- Refund is full collected amount or zero; no partial-refund state.
- Notification success/failure does not change payment truth.
- `SUCCEEDED` is not forced into Final because a later legitimate full refund may occur.

## 8. Explicitly Forbidden States / Transitions

Do not add:
- `DUE_AT_FACILITY`;
- `PARTIALLY_PAID`;
- `PARTIALLY_REFUNDED`;
- `CANCELLED`;
- `APPOINTMENT_CONFIRMED`;
- `CHECKED_IN`;
- `PROCESSING -> REFUNDED` bypassing refund pending;
- browser-return event directly setting `SUCCEEDED`;
- ordinary Reception action directly setting payment success/failure.


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

- Pass 1: exact eight-state inventory.
- Pass 2: Payment/Appointment independence.
- Pass 3: FULL_PAYMENT_REQUIRED-only boundary.
- Pass 4: trusted gateway truth.
- Pass 5: CREATED/PROCESSING outcome paths.
- Pass 6: critical UNDER_REVIEW entry cases.
- Pass 7: success-without-appointment handling.
- Pass 8: refund path.
- Pass 9: full-or-zero refund restriction.
- Pass 10: idempotency/one-non-terminal-intent rule.
- Pass 11: terminal-state audit.
- Pass 12: intentionally unspecified UNDER_REVIEW exits identified instead of invented.
- Pass 13: UI-state leakage audit.
- Pass 14: final MVP traceability.


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
