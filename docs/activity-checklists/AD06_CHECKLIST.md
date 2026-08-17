# AD-06 Implementation Checklist — Cancel Appointment

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD06_Cancel_Appointment_FINAL_VERIFIED_v2.md`
- SHA-256: `ed7b288f5091e4af4907de0304bbd8cf41583c88ac94fc40bba9f2788c03ea66`
- Package: Patient Package
- Exact title: Activity Diagram — Cancel Appointment
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Patient is authenticated and owns the Appointment.
- 2. Appointment is CONFIRMED.
- 3. Patient has not checked in.
- 4. Assigned ArrivalGroup window has not started.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Patient opens Appointment and chooses Cancel Appointment |
| `D00` | Decision | Appointment already terminally cancelled? |
| `A00` | Action | Return existing cancellation/refund result; create no duplicate cancellation or refund |
| `A02` | Action | Load saved cancellation/refund policy, payment state and ArrivalGroup timing |
| `A03` | Action | Revalidate ownership, CONFIRMED state, check-in and group-start conditions |
| `D01` | Decision | Patient self-cancellation still eligible? |
| `A04` | Action | Deny self-cancellation and preserve arrival / late / no-show handling |
| `A05` | Action | Calculate and display expected refund result from saved booking snapshot |
| `A06` | Action | Patient confirms cancellation |
| `A07` | Action | Record CANCELLED_BY_PATIENT and preserve Appointment history |
| `A08` | Action | Return consumed unit to the same ArrivalGroup; expose it as bookable only when release/group/time rules permit |
| `D02` | Decision | Aafiatak electronic amount was collected? |
| `A09` | Action | Create no electronic refund |
| `D03` | Decision | Saved policy says full refund is due? |
| `A10` | Action | Refund due is zero |
| `A11` | Action | Initiate full collected-amount refund |
| `D04` | Decision | Refund completion immediate? |
| `A12` | Action | Keep independent REFUND_PENDING / review status; cancellation remains final |
| `A13` | Action | Record completed full refund |
| `A14` | Action | Display cancelled Appointment and independent payment/refund status |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin cancellation |
| `A01` | `D00` | — | Check duplicate/terminal cancellation boundary |
| `D00` | `A00` | [Yes] | Preserve existing terminal cancellation/result |
| `A00` | `MEND` | — | No duplicate cancellation/refund |
| `D00` | `A02` | [No] | Continue cancellation review |
| `A02` | `A03` | — | Eligibility revalidation |
| `A03` | `D01` | — | Decision |
| `D01` | `A04` | [No] | Self-cancellation denied |
| `A04` | `MEND` | — | End denial branch |
| `D01` | `A05` | [Yes] | Show consequence before commit |
| `A05` | `A06` | — | Patient confirms |
| `A06` | `A07` | — | Cancel Appointment |
| `A07` | `A08` | — | Same-group capacity consequence |
| `A08` | `D02` | — | Evaluate financial branch |
| `D02` | `A09` | [No — PAY_AT_FACILITY / no collected electronic amount] | No Aafiatak refund |
| `A09` | `A14` | — | Show result |
| `D02` | `D03` | [Yes] | Apply saved policy |
| `D03` | `A10` | [Zero refund] | No refund created |
| `A10` | `A14` | — | Show result |
| `D03` | `A11` | [Full refund] | Full amount only |
| `A11` | `D04` | — | Refund status |
| `D04` | `A12` | [Pending / delayed] | Cancellation remains final |
| `A12` | `A14` | — | Show independent states |
| `D04` | `A13` | [Completed] | Record refunded |
| `A13` | `A14` | — | Show result |
| `A14` | `MEND` | — | End |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Refund is exactly full collected amount or zero.
- PAY_AT_FACILITY has no Aafiatak electronic refund.
- No partial refund.
- Appointment state and PaymentIntent state remain independent.

## Forbidden content

- Partial refund percentages.
- Cancellation after check-in through Patient self-service.
- Moving returned seat to another group.
- Reversing cancellation because refund is delayed.

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
