# AD-09 Implementation Checklist — Reschedule Appointment

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD09_Reschedule_Appointment_FINAL_VERIFIED_v2.md`
- SHA-256: `f351f96afe6dddcc663c14782d4f459807f6f3237d1a429f78a4f96e131d565b`
- Package: Booking & Reception Staff Package
- Exact title: Activity Diagram — Reschedule Appointment
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Staff is authenticated/authorized.
- 2. Appointment is CONFIRMED.
- 3. Patient and facility communicated and agreed to the change.
- 4. Candidate destination must belong to the same ServiceOffering and preserve saved terms.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Staff selects CONFIRMED Appointment and chooses Reschedule Appointment |
| `A02` | Action | Display current booking snapshot / history and permitted destination context |
| `A03` | Action | Staff selects agreed new day / group / session |
| `A04` | Action | Validate Appointment state, same ServiceOffering, same saved terms and destination bookability |
| `D01` | Decision | Appointment still CONFIRMED and destination uses same ServiceOffering / terms? |
| `A05` | Action | Reject in-place reschedule; use saved cancellation + normal new-booking path for different terms |
| `A06` | Action | Staff confirms proposed move and records reason |
| `A07` | Action | Atomically secure valid destination capacity first |
| `D02` | Decision | Destination acquisition succeeded? |
| `A08` | Action | Abort move and preserve original Appointment / old capacity |
| `A09` | Action | Update scheduling/group details while Appointment remains CONFIRMED |
| `A10` | Action | Release old capacity only after destination is secured |
| `A11` | Action | Record previous/new scheduling data, actor, reason and history |
| `A12` | Action | Show successfully rescheduled CONFIRMED Appointment and unchanged financial snapshot |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin reschedule |
| `A01` | `A02` | — | Review saved context |
| `A02` | `A03` | — | Select agreed destination |
| `A03` | `A04` | — | Validate destination |
| `A04` | `D01` | — | Terms/state decision |
| `D01` | `A05` | [No] | No mixed-term in-place reschedule |
| `A05` | `MEND` | — | End rejected in-place path |
| `D01` | `A06` | [Yes] | Confirm move |
| `A06` | `A07` | — | Secure destination first |
| `A07` | `D02` | — | Atomic acquisition result |
| `D02` | `A08` | [Failed / concurrent winner] | Old seat remains |
| `A08` | `MEND` | — | Safe failure |
| `D02` | `A09` | [Succeeded] | Commit scheduling update |
| `A09` | `A10` | — | Release old only now |
| `A10` | `A11` | — | Audit history |
| `A11` | `A12` | — | Show success |
| `A12` | `MEND` | — | Success ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Financial snapshot remains unchanged.

## Forbidden content

- Release old seat before new seat is secured.
- Top-up/partial refund/mixed financial lifecycle.
- Automatic late reassignment.
- Patient self-reschedule.
- RESCHEDULED status.

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
