# AD-10 Implementation Checklist — Register Patient Check-in

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD10_Register_Patient_Checkin_FINAL_VERIFIED_v2.md`
- SHA-256: `1edc547eacd357807237acdaf35f6479d699220a5b93f9f65e4ba188085ebca7`
- Package: Booking & Reception Staff Package
- Exact title: Activity Diagram — Register Patient Check-in
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Staff is authenticated/authorized.
- 2. Intended Appointment can be identified by booking number, phone, QR, or verification code.
- 3. Appointment is CONFIRMED and not cancelled.
- 4. Normal check-in applies only in the valid normal arrival context; late arrivals use AD-12.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Staff searches/scans Appointment identifier |
| `A02` | Action | Retrieve intended Appointment and validate facility/state/arrival context |
| `D01` | Decision | Correct intended Appointment and state = CONFIRMED? |
| `A03` | Action | Reject check-in; create no valid Visit/Queue arrival state |
| `D02` | Decision | Arrival eligible for normal check-in? |
| `A04` | Action | Route to Handle Late Arrival activity; do not auto-transfer group |
| `D03` | Decision | Valid check-in already exists from retry? |
| `A05` | Action | Return existing VisitInstance / QueueEntry state idempotently |
| `A06` | Action | Staff confirms Patient arrival |
| `A07` | Action | Create VisitInstance if needed and set CHECKED_IN |
| `A08` | Action | Record actual arrival time and original ArrivalGroup |
| `A09` | Action | Create / activate one QueueEntry inside original ArrivalGroup |
| `A10` | Action | Apply normal queue ordering by check-in time; earlier confirmed_at only as tie-breaker |
| `A11` | Action | Show check-in confirmation and approximate own-group position/number ahead |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin staff check-in |
| `A01` | `A02` | — | Resolve booking |
| `A02` | `D01` | — | Context/state decision |
| `D01` | `A03` | [No] | Wrong/cancelled context |
| `A03` | `MEND` | — | Rejected |
| `D01` | `D02` | [Yes] | Evaluate arrival timing |
| `D02` | `A04` | [Late / outside normal context] | Use late-arrival workflow |
| `A04` | `MEND` | — | Normal check-in ends |
| `D02` | `D03` | [Normal arrival] | Check duplicate retry |
| `D03` | `A05` | [Existing valid check-in] | Idempotent return |
| `A05` | `MEND` | — | No duplicate |
| `D03` | `A06` | [No existing check-in] | Register arrival |
| `A06` | `A07` | — | Visit state |
| `A07` | `A08` | — | Arrival data |
| `A08` | `A09` | — | Queue entry |
| `A09` | `A10` | — | Ordering |
| `A10` | `A11` | — | Patient-facing confirmation |
| `A11` | `MEND` | — | Success |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Appointment remains CONFIRMED; check-in is represented in VisitInstance.
- Queue position is approximate and only within Patient own group.
- Full payment grants no queue priority.

## Forbidden content

- Patient self-check-in.
- Appointment state = CHECKED_IN.
- Automatic late transfer.
- Payment-based queue priority.
- Exposure of other Patients private data.

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
