# Aafiatak State Diagram Implementation Checklists

This internal checklist records the seven reviewed execution contracts. It is not rendered into any UML diagram. All final visible labels remain English and must match the corresponding reviewed contract.

## Shared Lecturer-Style Contract

Each diagram models **one object only** on one light, academic page. It uses a filled initial pseudostate, rounded state rectangles, solid directed transitions, direct guards in square brackets, transition actions after `/`, and a final bullseye for each terminal outcome. No actor, lifeline, message numbering, note, legend, package, class/ERD notation, choice diamond, composite/nested state, history, fork, join, or unsupported advanced state-machine feature may be drawn. State names and transition labels are never numbered. The final visual-review status for every diagram is `awaiting-user-approval`.

## STD01_CHECKLIST — AvailabilityRelease

| Item | Contract |
|---|---|
| Title / object | `State Diagram — AvailabilityRelease Lifecycle` / `AvailabilityRelease` |
| Approved states | `DRAFT`, `PUBLISHED`, `FROZEN`, `CLOSED`, `CANCELLED` |
| Initial | `create AvailabilityRelease` → `DRAFT` |
| Transitions | `DRAFT` → `PUBLISHED`: `publish [configuration valid] / freeze published booking terms`; `PUBLISHED` → `FROZEN`: `freeze`; `FROZEN` → `PUBLISHED`: `resume publication`; `PUBLISHED`/`FROZEN` → `CLOSED`: `close`; `PUBLISHED`/`FROZEN` → `CANCELLED`: `cancel / release active holds`; `CLOSED`/`CANCELLED` → Final: `completion` |
| Approved in-state activity | None |
| Terminal states | `CLOSED`, `CANCELLED` |
| Forbidden | `EXHAUSTED`, `STALE`, `ACTIVE`, `OPEN`, `REOPENED`, `COMPLETED`, `ARCHIVED`; any reopening; `DRAFT` → `FROZEN`; capacity-increase transition |
| Layout caution | Separate the reversible `PUBLISHED`/`FROZEN` arrows visibly. |

## STD02_CHECKLIST — ArrivalGroup

| Item | Contract |
|---|---|
| Title / object | `State Diagram — ArrivalGroup Lifecycle` / `ArrivalGroup` |
| Approved states | `OPEN`, `FROZEN`, `CLOSED` |
| Initial | Unlabeled completion transition → `OPEN` |
| Transitions | `OPEN` → `FROZEN`: `freeze group`; `FROZEN` → `OPEN`: `resume group`; `OPEN`/`FROZEN` → `CLOSED`: `close group`; `CLOSED` → Final: `completion` |
| Approved in-state activity | None |
| Terminal states | `CLOSED` |
| Forbidden | `DRAFT`, `INITIALIZED`, `CREATED`, `PENDING`, `FULL`, `EXHAUSTED`, `UNAVAILABLE`, `STALE`, `LATE`, `WAITING`, `PUBLISHED`, `CANCELLED`, `REOPENED` |
| Special rule | Bookability stays a guard/context condition, not a State. |

## STD03_CHECKLIST — ReservationHold

| Item | Contract |
|---|---|
| Title / object | `State Diagram — ReservationHold Lifecycle` / `ReservationHold` |
| Approved states | `ACTIVE`, `CONSUMED`, `EXPIRED`, `RELEASED` |
| Initial | `create hold [ArrivalGroup is currently bookable] / protect one capacity unit` → `ACTIVE` |
| Transitions | `ACTIVE` → `CONSUMED`: `confirm full-payment booking [trusted success & hold valid & before group start & release not CANCELLED] / create CONFIRMED Appointment atomically`; `ACTIVE` → `CONSUMED`: `confirm pay-at-facility booking [booking complete & hold valid & before group start & release not CANCELLED] / create CONFIRMED Appointment atomically`; `ACTIVE` → `EXPIRED`: `hold time expires / release protected capacity`; `ACTIVE` → `RELEASED`: `Patient abandons or cancels booking / release protected capacity`; `ACTIVE` → `RELEASED`: `parent release is CANCELLED / release protected capacity`; every terminal state → Final: `completion` |
| Approved in-state activity | In `ACTIVE`: `do / protect one capacity unit and maintain countdown` |
| Terminal states | `CONSUMED`, `EXPIRED`, `RELEASED` |
| Forbidden | Fixed countdown duration; `PENDING`, `PROCESSING`, `PAID`, `CONFIRMED`, `CANCELLED`, `UNDER_REVIEW`; all terminal-to-`ACTIVE` arrows; hold-extension self-loop |

## STD04_CHECKLIST — Appointment

| Item | Contract |
|---|---|
| Title / object | `State Diagram — Appointment Lifecycle` / `Appointment` |
| Approved states | `CONFIRMED`, `CANCELLED_BY_PATIENT`, `CANCELLED_BY_FACILITY` |
| Initial | `booking requirements satisfied / create Appointment with immutable booking snapshot` → `CONFIRMED` |
| Transitions | `CONFIRMED` → `CANCELLED_BY_PATIENT`: `Patient cancels [not checked in & group window not started] / preserve history and release same-group capacity when eligible`; `CONFIRMED` → `CANCELLED_BY_FACILITY`: `Facility cancels [operationally required] / preserve history and start full refund if paid`; each cancellation → Final: `completion` |
| Approved in-state activity | None |
| Terminal states | `CANCELLED_BY_PATIENT`, `CANCELLED_BY_FACILITY` |
| Forbidden | `PENDING`, `PENDING_APPROVAL`, `APPROVED`, `REJECTED`, `RESCHEDULED`, `PAID`, all visit/refund states, and a `CONFIRMED` self-loop for rescheduling |
| Special rule | Rescheduling stays in `CONFIRMED` and is not rendered as a transition. |

## STD05_CHECKLIST — PaymentIntent

| Item | Contract |
|---|---|
| Title / object | `State Diagram — PaymentIntent Lifecycle` / `PaymentIntent` |
| Approved states | `CREATED`, `PROCESSING`, `SUCCEEDED`, `FAILED`, `EXPIRED`, `UNDER_REVIEW`, `REFUND_PENDING`, `REFUNDED` |
| Initial | `create PaymentIntent [FULL_PAYMENT_REQUIRED AND valid booking attempt]` → `CREATED` |
| Transitions | `CREATED` → `PROCESSING`: `start gateway payment`; `CREATED` → `EXPIRED`: `payment attempt expires before completion`; `PROCESSING` → `SUCCEEDED`: `trusted gateway confirms success`; `PROCESSING` → `FAILED`: `trusted gateway confirms failure`; `PROCESSING` → `EXPIRED`: `payment attempt expires`; `PROCESSING` → `UNDER_REVIEW`: `payment result cannot be safely resolved / record reconciliation case`; `SUCCEEDED` → `UNDER_REVIEW`: `booking completion or safe recovery remains unresolved / move payment case to review`; `SUCCEEDED` → `REFUND_PENDING`: `full refund required / initiate refund`; `REFUND_PENDING` → `REFUNDED`: `trusted refund completion`; `FAILED`/`EXPIRED`/`REFUNDED` → Final: `completion` |
| Approved in-state activities | `PROCESSING`: `do / await trusted gateway result`; `UNDER_REVIEW`: `do / await documented reconciliation`; `REFUND_PENDING`: `do / await full-refund completion` |
| Terminal states | `FAILED`, `EXPIRED`, `REFUNDED` |
| Forbidden | `DUE_AT_FACILITY`, `PARTIALLY_PAID`, `PARTIALLY_REFUNDED`, `CANCELLED`, `APPOINTMENT_CONFIRMED`, `CHECKED_IN`; browser-return success; direct `PROCESSING` → `REFUNDED`; every outgoing transition from `UNDER_REVIEW` |

## STD06_CHECKLIST — VisitInstance

| Item | Contract |
|---|---|
| Title / object | `State Diagram — VisitInstance Lifecycle` / `VisitInstance` |
| Approved states | `CREATED`, `CHECKED_IN`, `IN_SERVICE`, `COMPLETED`, `NOT_COMPLETED`, `NO_SHOW` |
| Initial | `first relevant service-day operational event / create VisitInstance` → `CREATED` |
| Transitions | `CREATED` → `CHECKED_IN`: `Reception registers arrival / record arrival and create/activate QueueEntry`; `CREATED` → `CHECKED_IN`: `Reception accepts late arrival [NO_SHOW not recorded] / record late acceptance and manual queue handling`; `CREATED` → `NO_SHOW`: `ArrivalGroup window ends [no valid check-in] / facility staff records no-show`; `CHECKED_IN` → `IN_SERVICE`: `facility staff records service start`; `CHECKED_IN`/`IN_SERVICE` → `NOT_COMPLETED`: `service cannot be completed / record non-completion`; `IN_SERVICE` → `COMPLETED`: `facility staff records operational completion`; `CHECKED_IN` → `CREATED`: `correct erroneous check-in [before service start] / remove QueueEntry and audit reason`; every outcome → Final: `completion` |
| Approved in-state activity | In `IN_SERVICE`: `do / service in progress` |
| Terminal states | `COMPLETED`, `NOT_COMPLETED`, `NO_SHOW` |
| Forbidden | `WAITING`, `CALLED`, `DONE`, `REMOVED`, `LATE`, `REENTERED`, `REQUEUED`, Appointment cancellation states, `PAID`, and all `NO_SHOW` outgoing arrows |

## STD07_CHECKLIST — QueueEntry

| Item | Contract |
|---|---|
| Title / object | `State Diagram — QueueEntry Lifecycle` / `QueueEntry` |
| Approved states | `WAITING`, `CALLED`, `DONE`, `REMOVED` |
| Initial | `valid or accepted-late check-in / create or activate QueueEntry` → `WAITING` |
| Transitions | `WAITING` → `CALLED`: `call next Patient [entry currently callable]`; `CALLED` → `DONE`: `queue handling completed / mark entry done`; `WAITING`/`CALLED` → `REMOVED`: `audited correction/removal [valid operational reason] / record reason`; each terminal state → Final: `completion` |
| Approved in-state activity | None |
| Terminal states | `DONE`, `REMOVED` |
| Forbidden | `CHECKED_IN`, `IN_SERVICE`, `COMPLETED`, `NO_SHOW`, `LATE`, `MANUAL_HANDLING`, `REENTERED`, `REQUEUED`, `PRIORITY`, `PAID_PRIORITY`, `VIP`, `FAST_TRACK`, and terminal-to-`WAITING` arrows |
| Special rule | Accepted-late `manualHandling` is a mode/flag, not a State; payment provides no priority. |

## Required Lock Criteria for Each Diagram

Before starting the next diagram, validate the model and view; render editable source, SVG, PNG, and vector PDF; open the visual outputs; compare every State and Transition with its contract; audit lecturer notation; correct any issue; rerender; and preserve `awaiting-user-approval` as the visual status.
