# AD-13 Implementation Checklist — Manage Operational Exceptions

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD13_Manage_Operational_Exceptions_FINAL_VERIFIED_v2.md`
- SHA-256: `8d6b6737664b154e7709c71f3108b8dcdbec7f8f0b732ccaeff909631044d7c1`
- Package: Facility Administrator + Booking & Reception Staff
- Exact title: Activity Diagram — Manage Operational Exceptions
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Authorized facility actor is authenticated.
- 2. Supported unplanned event occurs after publication/during daily operation.
- 3. Event can be classified in approved exception scope and affected context can be identified.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Facility actor records operational event and doctor/session/release context |
| `A02` | Action | Create OPEN OperationalException with approved type and link affected context |
| `D01` | Decision | Exception type = SESSION_CANCELLED? |
| `A03` | Action | Make affected session/release non-bookable and release active ReservationHolds |
| `A04` | Action | Preserve all confirmed Appointments and identify affected unresolved set |
| `A05` | Action | Present affected Appointments and relevant hold/capacity state |
| `A06` | Action | Select one unresolved affected Appointment |
| `D02` | Decision | Approved resolution path? |
| `A07` | Action | Offer / secure suitable equivalent alternative after Patient communication using reschedule invariants |
| `A08` | Action | Cancel Appointment from facility side and preserve history |
| `D03` | Decision | Electronic amount collected? |
| `A09` | Action | Initiate full collected-amount refund |
| `A10` | Action | Record facility-cancellation outcome with no electronic refund |
| `A11` | Action | Create documented support escalation for later Platform review |
| `A12` | Action | Record completed resolution action / outcome for affected Appointment |
| `A17` | Action | Keep OperationalException OPEN pending escalated resolution; do not close |
| `D04` | Decision | More affected Appointments unresolved? |
| `A13` | Action | Notify affected Patients through Notification Service when required |
| `A14` | Action | Facility actor requests Close Operational Exception |
| `D05` | Decision | Every affected Appointment has a completed documented action/outcome? |
| `A15` | Action | Reject closure and identify remaining resolution requirement |
| `A16` | Action | Close OperationalException and preserve audit trail |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin exception |
| `A01` | `A02` | — | Open exception |
| `A02` | `D01` | — | Special session-cancel handling |
| `D01` | `A03` | [Yes] | Session becomes non-bookable; release active holds |
| `A03` | `A04` | — | Confirmed Appointments preserved |
| `D01` | `A04` | [No] | Identify affected set |
| `A04` | `A05` | — | Review impact |
| `A05` | `A06` | — | Process affected Appointments one-by-one |
| `A06` | `D02` | — | Choose approved resolution |
| `D02` | `A07` | [Equivalent alternative] | Same-service/same-terms safe path |
| `A07` | `A12` | — | Record completed outcome |
| `D02` | `A08` | [Facility cancellation] | Cancel by facility |
| `A08` | `D03` | — | Refund decision |
| `D03` | `A09` | [Paid] | Full refund only |
| `A09` | `A12` | — | Record completed outcome |
| `D03` | `A10` | [No electronic payment] | No electronic refund |
| `A10` | `A12` | — | Record completed outcome |
| `D02` | `A11` | [Escalation] | Document support escalation |
| `A11` | `A17` | — | Escalation is not a completed resolution |
| `A17` | `MEND` | — | End current activity with exception still OPEN |
| `A12` | `D04` | — | Check remaining unresolved set |
| `D04` | `A06` | [Yes] | Loop to next affected Appointment |
| `D04` | `A13` | [No] | All completed outcomes documented; notify if required |
| `A13` | `A14` | — | Request closure |
| `A14` | `D05` | — | Strict closure gate |
| `D05` | `A15` | [No] | Cannot close |
| `A15` | `A06` | — | Return to unresolved Appointment handling |
| `D05` | `A16` | [Yes] | Close and audit |
| `A16` | `MEND` | — | Closed-success path ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Doctor does not record delay/absence through Doctor interface; facility staff records the OperationalException.
- Platform Administrator appears only in later escalation review, not daily operational handling.
- Facility-responsible paid cancellation starts full refund.

## Forbidden content

- Silent deletion of affected Appointments/history.
- Reverse import of internal capacity.
- Partial refund.
- Doctor as exception-recording actor.
- Platform Administrator running daily facility resolution.
- Closing with unresolved affected Appointment.

## Required lock-gate evidence

- [ ] 1. Verify the exact Use Case title and scope.
- [ ] 2. Verify the Initial Node exists and has no incoming flow.
- [ ] 3. Verify the Activity Final exists and has no outgoing flow.
- [ ] 4. Verify every Action is source-supported and verb-led.
- [ ] 5. Verify every Decision has meaningful guarded outgoing flows.
- [ ] 6. Verify every Merge is used only to reunite alternatives, not as decoration.
- [ ] 7. Verify Fork/Join is absent unless true parallelism is explicitly required.
- [ ] 8. Verify all arrows are Control Flows unless an Object Flow is explicitly specified.
- [ ] 9. Verify no Association/Generalization/Aggregation/Use-Case relationship appears.
- [ ] 10. Verify no Sequence lifeline/message notation appears.
- [ ] 11. Verify actor permissions and product boundaries.
- [ ] 12. Verify independent lifecycle states are not collapsed into one generic status.
- [ ] 13. Verify all rendered branch guards are mutually understandable and not contradictory.
- [ ] 14. Render SVG/PNG/PDF; open every actual output and inspect it visually.
- [ ] 15. Compare the render against this MD item-by-item and correct semantic, notation, routing, and readability issues.
- [ ] 16. Final status must be `awaiting-user-approval`.
