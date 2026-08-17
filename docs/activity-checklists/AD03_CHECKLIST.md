# AD-03 Implementation Checklist — Book Appointment

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD03_Book_Appointment_FINAL_VERIFIED_v2.md`
- SHA-256: `b64bb9519b5e28792d34bdcc25439448f4b34892ac0d5f1ccc2ef99eb3f5af47`
- Package: Patient Package
- Exact title: Activity Diagram — Book Appointment
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Patient is authenticated.
- 2. Selected ServiceOffering and facility/branch context are valid/active.
- 3. A published AvailabilityRelease exists for the selected service/day.
- 4. Patient has no prohibited overlapping active hold/confirmed Appointment.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Patient selects service / doctor context and day |
| `D00` | Decision | Conflicting overlapping ACTIVE ReservationHold or CONFIRMED Appointment exists? |
| `A00` | Action | Reject conflicting new booking attempt; preserve existing booking/hold |
| `A02` | Action | Find earliest currently bookable ArrivalGroup |
| `D01` | Decision | Currently bookable ArrivalGroup available? |
| `A03` | Action | Offer Notify Me When Available; create no hold |
| `A04` | Action | Display arrival window and governing snapshotted terms |
| `A05` | Action | Patient confirms intent to proceed |
| `A06` | Action | Atomically acquire one ACTIVE ReservationHold and start countdown |
| `D02` | Decision | Hold acquisition succeeded? |
| `A07` | Action | Report capacity full / temporarily held; create no Appointment |
| `D03` | Decision | Governing booking policy? |
| `A08` | Action | Patient completes final booking information and accepts payment due at facility |
| `A09` | Action | Revalidate hold, release, group and time eligibility |
| `D04` | Decision | Hold / target still eligible? |
| `A10` | Action | Expire or release hold; create no Appointment |
| `A11` | Action | Atomically consume hold and create one CONFIRMED Appointment |
| `A12` | Action | Display booking confirmation and payment due at facility |
| `A13` | Action | Run Process Full Payment activity for full snapshotted amount |
| `D05` | Decision | Trusted full-payment result supports confirmation while target remains eligible? |
| `A14` | Action | Do not create conflicting Appointment; follow payment recovery/refund/UNDER_REVIEW rules |
| `A15` | Action | Atomically consume hold and create one CONFIRMED Appointment with booking snapshot |
| `A16` | Action | Display confirmed Appointment and paid payment state separately |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin booking |
| `A01` | `D00` | — | Check overlap boundary |
| `D00` | `A00` | [Yes] | UCM overlapping-booking failure boundary |
| `A00` | `MEND` | — | No conflicting booking created |
| `D00` | `A02` | [No] | Continue capacity allocation |
| `A02` | `D01` | — | Evaluate availability |
| `D01` | `A03` | [No] | No capacity path |
| `A03` | `MEND` | — | No booking created |
| `D01` | `A04` | [Yes] | Show proposed group/terms |
| `A04` | `A05` | — | Patient reviews/accepts |
| `A05` | `A06` | — | Atomic last-seat protection |
| `A06` | `D02` | — | Check hold acquisition |
| `D02` | `A07` | [Failed / concurrent winner] | No double booking |
| `A07` | `MEND` | — | End concurrency failure |
| `D02` | `D03` | [Succeeded] | Branch by authoritative policy |
| `D03` | `A08` | [PAY_AT_FACILITY] | No PaymentIntent path |
| `A08` | `A09` | — | Final revalidation |
| `A09` | `D04` | — | Eligibility decision |
| `D04` | `A10` | [Invalid / expired / started / cancelled] | No Appointment |
| `A10` | `MEND` | — | End invalid-target path |
| `D04` | `A11` | [Valid] | Confirm pay-at-facility booking |
| `A11` | `A12` | — | Show success |
| `A12` | `MEND` | — | Pay-at-facility success ends |
| `D03` | `A13` | [FULL_PAYMENT_REQUIRED] | Invoke payment workflow |
| `A13` | `D05` | — | Evaluate trusted payment/booking result |
| `D05` | `A14` | [No] | Critical-payment handling; no conflicting Appointment |
| `A14` | `MEND` | — | Payment recovery branch ends/continues outside booking |
| `D05` | `A15` | [Yes] | Atomic confirmation |
| `A15` | `A16` | — | Show success |
| `A16` | `MEND` | — | Full-payment success ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Patient does not choose arbitrary ArrivalGroup; system uses earliest currently bookable group.
- One booking action protects/consumes one capacity unit.
- PAY_AT_FACILITY creates no PaymentIntent.
- FULL_PAYMENT_REQUIRED confirms only from trusted payment success while booking target remains valid.
- Arrival window is not an exact doctor-entry time.

## Forbidden content

- Deposit/partial payment.
- Manual facility approval/pending approval.
- Arbitrary group selection.
- Duplicate Appointment or hold on retry.
- Exact unresolved ReservationHold default duration.

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
