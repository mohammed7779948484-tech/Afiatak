# AD-05 Implementation Checklist — Subscribe to Availability Alert

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD05_Subscribe_Availability_Alert_FINAL_VERIFIED_v2.md`
- SHA-256: `406c9945e37c9a5f83e202d4124192745e37bfd39b42deeb332de56bbff5293a`
- Package: Patient Package
- Exact title: Activity Diagram — Subscribe to Availability Alert
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Patient is authenticated.
- 2. Relevant service/doctor/date/release context is selected.
- 3. Suitable capacity is currently unavailable or protected by another ACTIVE hold.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Patient chooses Notify Me When Available |
| `A02` | Action | Revalidate current Aafiatak bookability |
| `D01` | Decision | Capacity now bookable? |
| `A03` | Action | Direct Patient to normal booking; create no hidden reservation |
| `A04` | Action | Create AvailabilityAlertSubscription for Patient/context |
| `A05` | Action | Confirm subscription as interest only — no hold / queue / priority |
| `A06` | Action | Wait for approved capacity-return event, successful Patient booking, or session end |
| `D02` | Decision | Which source-supported event occurs? |
| `A07` | Action | Expire corresponding subscription after successful Patient booking |
| `A08` | Action | Expire subscription when session ends |
| `A09` | Action | Detect zero-to-positive bookable capacity from approved Aafiatak event |
| `A10` | Action | Notify eligible subscriptions through Notification Service |
| `A11` | Action | Patient competes through normal booking; first valid ReservationHold wins |
| `D03` | Decision | Patient successfully books? |
| `A12` | Action | Keep subscription lifecycle subject to duplicate-notification suppression until booking/session end |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin subscription |
| `A01` | `A02` | — | Revalidate availability |
| `A02` | `D01` | — | Check race with returning capacity |
| `D01` | `A03` | [Yes] | Normal booking opportunity; no alert reservation |
| `A03` | `MEND` | — | Subscription not required |
| `D01` | `A04` | [No] | Create subscription |
| `A04` | `A05` | — | Confirm non-reserving semantics |
| `A05` | `A06` | — | Wait for lifecycle event |
| `A06` | `D02` | — | Classify event |
| `D02` | `A07` | [Patient books successfully] | Expire subscription |
| `A07` | `MEND` | — | Ends |
| `D02` | `A08` | [Session ends] | Expire subscription |
| `A08` | `MEND` | — | Ends |
| `D02` | `A09` | [Approved capacity returns] | Eligible alert event |
| `A09` | `A10` | — | Send in-app/system alert |
| `A10` | `A11` | — | No priority; normal race |
| `A11` | `D03` | — | Booking outcome |
| `D03` | `A07` | [Booked] | Expire after booking |
| `D03` | `A12` | [Not booked] | Subscription remains governed by lifecycle/duplicate-suppression rules |
| `A12` | `A06` | — | Return to waiting lifecycle |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Subscription expires on session end or successful relevant booking.
- After an alert, normal ReservationHold competition applies.
- General alert notifications use Notification Service/system channel, not WhatsApp.

## Forbidden content

- Reservation/priority semantics for alert.
- Automatic capacity import from internal facility schedule.
- Queue position created by alert.
- WhatsApp general alert delivery.

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
