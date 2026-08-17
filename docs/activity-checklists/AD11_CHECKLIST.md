# AD-11 Implementation Checklist — Record No-show

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD11_Record_No_Show_FINAL_VERIFIED_v2.md`
- SHA-256: `3ab9b5868eae3e0713f4080158fcb9bf36088aaa52a70c35e3be2fd168f867ad`
- Package: Booking & Reception Staff Package
- Exact title: Activity Diagram — Record No-show
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Staff is authenticated/authorized.
- 2. Appointment is relevant to the service-day context.
- 3. Assigned ArrivalGroup window should have ended.
- 4. A valid check-in must not exist.
- 5. No terminal VisitInstance outcome may already exist.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Staff selects overdue Appointment / visit and chooses Record No-show |
| `A02` | Action | Validate ArrivalGroup time, check-in state and existing terminal outcome |
| `D01` | Decision | ArrivalGroup window ended? |
| `A03` | Action | Reject premature NO_SHOW |
| `D02` | Decision | Valid check-in exists? |
| `A04` | Action | Reject NO_SHOW; use actual checked-in Visit path |
| `D03` | Decision | Terminal outcome already recorded? |
| `A05` | Action | Return existing terminal outcome; do not reopen or duplicate |
| `A06` | Action | Staff confirms no-show decision |
| `A07` | Action | Create/use permitted VisitInstance context and record terminal NO_SHOW |
| `A08` | Action | Record actor, timestamp and audit information |
| `D04` | Decision | Booking has collected electronic payment? |
| `A09` | Action | Create no Aafiatak electronic refund |
| `D05` | Decision | Saved no-show financial policy? |
| `A10` | Action | Apply NO_SHOW_NON_REFUNDABLE — refund due = zero |
| `A11` | Action | Initiate full collected-amount refund under NO_SHOW_FULL_REFUND |
| `A12` | Action | Display terminal Visit outcome and independent payment/refund state |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin no-show |
| `A01` | `A02` | — | Validate conditions |
| `A02` | `D01` | — | Time decision |
| `D01` | `A03` | [No] | Too early |
| `A03` | `MEND` | — | End rejected |
| `D01` | `D02` | [Yes] | Check arrival |
| `D02` | `A04` | [Yes] | Patient did arrive |
| `A04` | `MEND` | — | End rejected |
| `D02` | `D03` | [No] | Check terminality |
| `D03` | `A05` | [Yes] | No duplicate/reopen |
| `A05` | `MEND` | — | End existing-result branch |
| `D03` | `A06` | [No] | Record no-show |
| `A06` | `A07` | — | Terminal visit outcome |
| `A07` | `A08` | — | Audit |
| `A08` | `D04` | — | Financial branch |
| `D04` | `A09` | [No / PAY_AT_FACILITY] | No electronic refund |
| `A09` | `A12` | — | Show result |
| `D04` | `D05` | [Yes] | Use saved policy |
| `D05` | `A10` | [NO_SHOW_NON_REFUNDABLE] | Zero refund |
| `A10` | `A12` | — | Show result |
| `D05` | `A11` | [NO_SHOW_FULL_REFUND] | Full refund lifecycle |
| `A11` | `A12` | — | Show result/pending status |
| `A12` | `MEND` | — | End |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Facility staff, not Doctor, records NO_SHOW.
- Appointment state remains separate; NO_SHOW belongs to VisitInstance.
- Refund status remains independent.

## Forbidden content

- Premature NO_SHOW.
- NO_SHOW when valid check-in exists.
- Doctor recording NO_SHOW.
- Appointment status = NO_SHOW.
- Partial no-show refund.
- NO_SHOW -> CHECKED_IN reopening.

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
