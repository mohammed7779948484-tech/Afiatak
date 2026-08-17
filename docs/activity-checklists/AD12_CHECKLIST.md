# AD-12 Implementation Checklist — Handle Late Arrival

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD12_Handle_Late_Arrival_FINAL_VERIFIED_v2.md`
- SHA-256: `a525addaf809d2f8164e4451373da9ccda20d6e8e5a410b2b64ce10180cb5318`
- Package: Booking & Reception Staff Package
- Exact title: Activity Diagram — Handle Late Arrival
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Staff is authenticated/authorized.
- 2. Assigned ArrivalGroup window ended without valid normal check-in.
- 3. Appointment is the relevant booking context.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Staff identifies Patient arriving after assigned ArrivalGroup window |
| `D01` | Decision | Terminal NO_SHOW already recorded? |
| `A02` | Action | Do not reopen VisitInstance; require documented reschedule / new operational arrangement |
| `A03` | Action | Staff records late arrival condition |
| `D02` | Decision | Which real operational outcome is chosen? |
| `A04` | Action | Accept Patient manually while keeping original Appointment and ArrivalGroup |
| `A05` | Action | Register check-in / actual arrival and mark late accepted arrival |
| `A06` | Action | Create/activate QueueEntry and set manualHandling flag |
| `A07` | Action | Exclude from automatic numeric queue position; make no priority promise |
| `A08` | Action | Call Patient when operationally appropriate without consuming another group capacity |
| `A09` | Action | Reschedule after Patient agreement using same-service / same-terms atomic rules |
| `A10` | Action | Record terminal NO_SHOW and apply saved no-show financial policy |
| `A11` | Action | Record NOT_COMPLETED when Patient arrived but service was not completed |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin late handling |
| `A01` | `D01` | — | Check terminal boundary |
| `D01` | `A02` | [Yes] | Terminal NO_SHOW cannot reopen |
| `A02` | `MEND` | — | End current late-check-in path |
| `D01` | `A03` | [No] | Record late condition |
| `A03` | `D02` | — | Manual staff outcome decision |
| `D02` | `A04` | [Accept manually] | No automatic reassignment |
| `A04` | `A05` | — | Late accepted check-in |
| `A05` | `A06` | — | Manual queue visibility |
| `A06` | `A07` | — | No numeric priority |
| `A07` | `A08` | — | Operational call |
| `A08` | `MEND` | — | Manual-accept path ends |
| `D02` | `A09` | [Reschedule] | Use AD-09 invariants; secure new capacity first |
| `A09` | `MEND` | — | Reschedule path ends |
| `D02` | `A10` | [NO_SHOW is actual outcome] | Terminal no-show path |
| `A10` | `MEND` | — | No-show path ends |
| `D02` | `A11` | [NOT_COMPLETED is actual outcome] | Non-completion path |
| `A11` | `MEND` | — | Non-completion ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- No automatic move to a later group.
- No re-entry/requeue state.
- No numeric queue priority promise.
- No capacity consumption from another ArrivalGroup for manual acceptance.

## Forbidden content

- LATE / LATE_ACCEPTED as a new Visit/Queue state.
- Automatic next-group assignment.
- Guaranteed priority for late Patient.
- NO_SHOW reopening.
- Platform-created requeue state.

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
