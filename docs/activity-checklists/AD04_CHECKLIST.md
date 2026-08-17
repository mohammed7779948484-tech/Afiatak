# AD-04 Implementation Checklist — Process Full Payment

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD04_Process_Full_Payment_FINAL_VERIFIED_v2.md`
- SHA-256: `89fbfac2a150495aba87c73b523cd7e4316ac6f0d3736718c211bcb331025adf`
- Package: Patient Package
- Exact title: Activity Diagram — Process Full Payment
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Booking policy is FULL_PAYMENT_REQUIRED.
- 2. An ACTIVE ReservationHold exists.
- 3. Amount/currency are the booking-attempt snapshot values.
- 4. No other non-terminal PaymentIntent is active for the same hold.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Create or safely reuse the one permitted PaymentIntent |
| `A02` | Action | Patient completes approved Payment Gateway interaction |
| `A03` | Action | Treat client/browser return as non-authoritative |
| `A04` | Action | Verify result through trusted webhook or trusted gateway query |
| `D01` | Decision | Trusted payment result available? |
| `A05` | Action | Keep payment unresolved / UNDER_REVIEW as applicable |
| `D02` | Decision | Trusted payment outcome? |
| `A06` | Action | Record FAILED or EXPIRED payment result |
| `D03` | Decision | Patient requests another attempt while hold remains valid? |
| `A07` | Action | Start new idempotent attempt only after terminal failure/expiry |
| `A08` | Action | Persist trusted SUCCEEDED financial result |
| `A09` | Action | Revalidate ReservationHold and release/group/time eligibility |
| `D04` | Decision | Original booking target still eligible? |
| `A10` | Action | Attempt safe equivalent recovery under equivalent snapshotted terms |
| `D05` | Decision | Equivalent recovery completed safely? |
| `A11` | Action | Create / complete confirmed booking under equivalent valid capacity |
| `D06` | Decision | Full refund can be initiated as approved recovery? |
| `A12` | Action | Initiate full refund |
| `A13` | Action | Keep payment case UNDER_REVIEW for documented support path |
| `A14` | Action | Atomically consume hold and create CONFIRMED Appointment |
| `A15` | Action | Show independent payment result, receipt/reference and booking result |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Prepare idempotent payment attempt |
| `A01` | `A02` | — | Gateway interaction |
| `A02` | `A03` | — | Client returns |
| `A03` | `A04` | — | Trusted verification required |
| `A04` | `D01` | — | Check trusted result availability |
| `D01` | `A05` | [Not yet] | Unresolved case |
| `A05` | `MEND` | — | Current activity instance ends in review/unresolved state |
| `D01` | `D02` | [Available] | Classify trusted outcome |
| `D02` | `A06` | [FAILED / EXPIRED] | Record terminal failed attempt |
| `A06` | `D03` | — | Optional retry rule |
| `D03` | `A07` | [Yes — hold still valid] | New attempt allowed under idempotent rules |
| `A07` | `A02` | — | Loop to gateway interaction |
| `D03` | `MEND` | [No] | No confirmed booking from failed payment |
| `D02` | `A08` | [SUCCEEDED] | Persist financial truth |
| `A08` | `A09` | — | Booking eligibility revalidation |
| `A09` | `D04` | — | Check target |
| `D04` | `A14` | [Eligible] | Normal successful confirmation |
| `A14` | `A15` | — | Display result |
| `A15` | `MEND` | — | Success ends |
| `D04` | `A10` | [Ineligible / appointment creation failed] | Critical recovery |
| `A10` | `D05` | — | Evaluate equivalent recovery |
| `D05` | `A11` | [Yes] | Complete safe equivalent booking |
| `A11` | `A15` | — | Show recovered success |
| `D05` | `D06` | [No] | Choose approved financial recovery |
| `D06` | `A12` | [Refund path available] | Full refund only |
| `A12` | `MEND` | — | Refund path ends/pends independently |
| `D06` | `A13` | [Cannot resolve immediately] | Documented UNDER_REVIEW path |
| `A13` | `MEND` | — | Review path ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- At most one non-terminal PaymentIntent per ReservationHold.
- No PaymentIntent for PAY_AT_FACILITY.
- Refund is full amount or zero.
- Ordinary facility users cannot force a financial state.

## Forbidden content

- Client return -> SUCCEEDED directly.
- Partial payment/refund.
- Cashier/accounting lifecycle.
- Multiple gateways.
- Arbitrary Reception payment override.

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
