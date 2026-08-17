# AD-16 Implementation Checklist — Suspend Facility

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD16_Suspend_Facility_FINAL_VERIFIED_v2.md`
- SHA-256: `370423b6b59539f17a7539818271daf798a521afd0f883be986d9297190e321b`
- Package: Platform Administrator Package
- Exact title: Activity Diagram — Suspend Facility
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Platform Administrator is authenticated/authorized.
- 2. Target facility account exists and is eligible for suspension.
- 3. A suspension reason/decision has been established through approved platform process.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Platform Administrator selects facility and chooses Suspend Facility |
| `A02` | Action | Display current platform status and operational impact |
| `D01` | Decision | Facility already suspended? |
| `A03` | Action | Return current suspended status without duplicate destructive effects |
| `A04` | Action | Platform Administrator confirms suspension decision |
| `A05` | Action | Mark facility suspended for new Aafiatak activity |
| `A06` | Action | Block new ReservationHolds / bookings and new availability publication |
| `D02` | Decision | ACTIVE ReservationHolds exist? |
| `A07` | Action | Release active temporary holds according to suspension rule and preserve audit/capacity history |
| `A08` | Action | Preserve all existing CONFIRMED Appointments and historical records |
| `D03` | Decision | Any existing CONFIRMED Appointments require documented operational resolution? |
| `A09` | Action | Require documented facility operational resolution through proper workflow; do not delete commitments |
| `A10` | Action | Record platform suspension audit trail |
| `A11` | Action | Confirm suspension without taking over daily facility booking / queue handling |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin suspension |
| `A01` | `A02` | — | Show impact |
| `A02` | `D01` | — | Idempotent current-state check |
| `D01` | `A03` | [Yes] | No duplicate effects |
| `A03` | `MEND` | — | End repeated request |
| `D01` | `A04` | [No] | Confirm suspension |
| `A04` | `A05` | — | Suspend facility |
| `A05` | `A06` | — | Block new activity |
| `A06` | `D02` | — | Check active holds |
| `D02` | `A07` | [Yes] | Release holds |
| `A07` | `A08` | — | Preserve confirmed commitments |
| `D02` | `A08` | [No] | Continue preservation |
| `A08` | `D03` | — | Check operational commitments |
| `D03` | `A09` | [Yes] | Require facility resolution |
| `A09` | `A10` | — | Audit |
| `D03` | `A10` | [No] | Audit |
| `A10` | `A11` | — | Confirm platform action |
| `A11` | `MEND` | — | Success ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Suspended facility cannot accept new holds/bookings or publish new availability.
- Existing confirmed commitments/history remain auditable.
- Platform audit trail is preserved.

## Forbidden content

- Hard-delete confirmed Appointments/history.
- Platform Administrator daily queue operation.
- Platform Administrator directly resolving every facility Appointment.
- Leaving active holds stuck under suspension.
- Duplicate suspension side effects.

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
