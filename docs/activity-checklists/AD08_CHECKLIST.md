# AD-08 Implementation Checklist — Withdraw Remaining Capacity

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD08_Withdraw_Remaining_Capacity_FINAL_VERIFIED_v2.md`
- SHA-256: `94397afa130946339a8d3c0b386c7027e0e0f4a311feaa6ccb0837e30c11d84a`
- Package: Facility Administrator + Booking & Reception Staff
- Exact title: Activity Diagram — Withdraw Remaining Capacity
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Authorized facility actor is authenticated.
- 2. Target release/group has valid remaining unused Aafiatak capacity.
- 3. Requested quantity is positive and must not exceed valid remaining capacity.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Actor opens target release/group capacity |
| `A02` | Action | Display published, held, confirmed, withdrawn and remaining capacity |
| `A03` | Action | Actor selects capacity action, quantity and approved source/reason |
| `D00` | Decision | Requested action is an approved one-way CapacityWithdrawal? |
| `A00` | Action | Reject restore / +1 / published-capacity increase request |
| `A04` | Action | Atomically revalidate current valid remaining capacity |
| `D01` | Decision | Requested quantity is positive and <= valid remaining capacity? |
| `A05` | Action | Reject stale/invalid quantity; protect held and confirmed units |
| `A06` | Action | Create irreversible CapacityWithdrawal |
| `A07` | Action | Reduce Aafiatak remaining capacity without moving held/confirmed units |
| `A08` | Action | Record release/group, quantity, source/reason, actor and timestamp |
| `A09` | Action | Display updated capacity |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin withdrawal |
| `A01` | `A02` | — | View capacity composition |
| `A02` | `A03` | — | Choose capacity action / quantity / reason |
| `A03` | `D00` | — | Enforce one-way withdrawal boundary |
| `D00` | `A00` | [Restore / +1 / increase] | Reject forbidden reverse/increase operation |
| `A00` | `MEND` | — | Capacity remains unchanged |
| `D00` | `A04` | [Approved withdrawal] | Revalidate at commit time |
| `A04` | `D01` | — | Atomic validity decision |
| `D01` | `A05` | [No] | Concurrent change/excess quantity is rejected |
| `A05` | `MEND` | — | No withdrawal |
| `D01` | `A06` | [Yes] | Create one auditable withdrawal |
| `A06` | `A07` | — | Apply one-way capacity reduction |
| `A07` | `A08` | — | Audit |
| `A08` | `A09` | — | Show result |
| `A09` | `MEND` | — | Success ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- One, multiple, or all remaining seats may be withdrawn when valid.
- Internal Patient details are not required to perform the transfer.
- Withdrawal is the only approved bridge from unused Aafiatak capacity to internal schedule.

## Forbidden content

- Restore/+1 capacity.
- Withdraw held capacity.
- Withdraw confirmed capacity.
- Move existing Patients between groups because of withdrawal.
- Import internal capacity back to same release.

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
