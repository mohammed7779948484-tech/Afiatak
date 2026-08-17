# AD-14 Implementation Checklist — Call Next Patient

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD14_Call_Next_Patient_FINAL_VERIFIED_v2.md`
- SHA-256: `a7a6858af8f81b9021237e78db232a36e717a33e773ece23abb8479f1c537b17`
- Package: Doctor Package
- Exact title: Activity Diagram — Call Next Patient
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Doctor is authenticated through approved account linked to Doctor profile.
- 2. Doctor sees only assigned Aafiatak waiting context.
- 3. A callable QueueEntry may exist, or an accepted-late Patient may be manually selected.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Doctor reviews assigned Aafiatak waiting list |
| `A02` | Action | System applies approved queue ordering / manual late handling context |
| `D01` | Decision | Callable relevant Patient exists? |
| `A03` | Action | Perform no call action; refresh current waiting state |
| `A04` | Action | Doctor identifies / selects next relevant Patient |
| `A05` | Action | Doctor chooses Call Next Patient |
| `A06` | Action | Revalidate selected QueueEntry callable state |
| `D02` | Decision | Selected QueueEntry still callable? |
| `A07` | Action | Reject stale call and refresh waiting state |
| `A08` | Action | Doctor confirms call |
| `A09` | Action | Record queue call and set QueueEntry = CALLED where applicable |
| `A10` | Action | Call / notify Patient to proceed |
| `A11` | Action | Leave VisitInstance state unchanged by Doctor |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin call-next |
| `A01` | `A02` | — | Prepare waiting context |
| `A02` | `D01` | — | Availability decision |
| `D01` | `A03` | [No] | Nothing callable |
| `A03` | `MEND` | — | End no-call path |
| `D01` | `A04` | [Yes] | Select next/manual accepted-late Patient |
| `A04` | `A05` | — | Choose call |
| `A05` | `A06` | — | Revalidate |
| `A06` | `D02` | — | Stale-state decision |
| `D02` | `A07` | [No] | Reject stale selection |
| `A07` | `A01` | — | Refresh and reconsider waiting list |
| `D02` | `A08` | [Yes] | Confirm |
| `A08` | `A09` | — | QueueEntry call transition |
| `A09` | `A10` | — | Patient called |
| `A10` | `A11` | — | Enforce Doctor boundary |
| `A11` | `MEND` | — | Success ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Full payment grants no queue priority.
- Doctor cannot reorder the facility complete internal queue.

## Forbidden content

- Doctor setting VisitInstance IN_SERVICE/COMPLETED/NOT_COMPLETED/NO_SHOW.
- Payment-based priority.
- Automatic numeric priority for accepted late Patient.
- Calling a stale REMOVED/DONE QueueEntry.

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
