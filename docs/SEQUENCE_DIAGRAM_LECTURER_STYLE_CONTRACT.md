# Aafiatak Sequence Diagrams — Lecturer-Style Contract

## Purpose and precedence

This contract operationalizes `Pasted_content_17.txt` for SD-01 through SD-06. It overrides earlier execution approaches that showed combined fragments, visible alternative/failure boxes, stereotypes, explanatory notes, or unnumbered interactions. The reviewed SD specifications remain authoritative for participant names, selected successful semantics, states, lifecycle rules, and prohibited behavior; their alternative paths are retained only as invisible QA constraints.

## Visible notation contract

| Aspect | Required implementation |
|---|---|
| Diagram type | UML Sequence Diagram only |
| Human participants | Stick-figure human actor with vertical lifeline |
| System participants | Simple named object/system box with vertical lifeline; name only |
| Time | Strictly top to bottom |
| Action or request | Solid horizontal arrow with closed arrowhead |
| Direct response | Dashed horizontal arrow with open arrowhead |
| Activations | Narrow bars only while meaningful work is active |
| Visible labels | English only; each message begins with one chronological integer followed by a period |
| Page | Single A3 landscape-equivalent sheet, clean white/light background, dark navy/charcoal UML linework |

## Absolute visible prohibitions

| Do not render | Do not render |
|---|---|
| `alt`, `opt`, `loop`, `break`, `par`, `critical`, or `ref` | Any Combined Fragment frame |
| Failure, alternative, exception, or policy boxes | Legend |
| Participant stereotypes | Large explanatory/retry/failure notes |
| Use-case, class, ERD, or inheritance notation | Invented services, gateways, repositories, controllers, or microservices |

## Mandatory per-diagram QA

Each final diagram must have the exact participant order and selected successful flow approved in `Pasted_content_17.txt`; use message numbering from `1` without skips or duplicates; show solid requests/actions and dashed returns; include only meaningful self-messages; and respect all domain constraints while showing no unapproved architecture. The SVG, PNG, and PDF must each be opened and inspected before the diagram is locked as `awaiting-user-approval`.

## Cross-diagram consistency controls

`Aafiatak Backend`, `Aafiatak Data Store`, `Payment Gateway`, and `Notification Service` must retain identical names whenever present. Appointment states must remain limited to `CONFIRMED`, `CANCELLED_BY_PATIENT`, and `CANCELLED_BY_FACILITY`. ReservationHold, PaymentIntent, VisitInstance, and QueueEntry must remain independent lifecycles. WhatsApp is authentication-only; neither partial payment nor partial refund is permitted; Doctor and Reception permissions remain bounded by the selected sequence semantics.
