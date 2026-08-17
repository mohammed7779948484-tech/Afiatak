# AD-02 Implementation Checklist — Log In

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD02_Log_In_FINAL_VERIFIED_v2.md`
- SHA-256: `8450894b77c2eb9520f2b6540ed0efa415375212017a321a7ac3b19e15fc27f4`
- Package: Shared Authentication
- Exact title: Activity Diagram — Log In
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. A verified normalized phone identity exists.
- 2. Requested privileged role/profile is approved/provisioned when applicable.
- 3. Relevant account/facility/platform access has not been revoked.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Actor provides verified phone number and requests Log In |
| `A02` | Action | Normalize phone and locate existing identity / requested role context |
| `A03` | Action | Request short-lived single-use WhatsApp OTP |
| `D01` | Decision | WhatsApp authentication channel available? |
| `A04` | Action | Keep login incomplete; provide no SMS/password fallback |
| `A05` | Action | Actor submits OTP |
| `A06` | Action | Verify OTP expiry, single-use, rate-limit and brute-force controls |
| `D02` | Decision | OTP valid and permitted? |
| `A07` | Action | Deny authentication; create no session |
| `A08` | Action | Revalidate account / role / facility access |
| `D03` | Decision | Requested role context enabled and authorized? |
| `A09` | Action | Deny privileged access and issue no usable privileged session |
| `A10` | Action | Create revocable authenticated session/token |
| `A11` | Action | Expose only functions permitted to the approved role |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin login |
| `A01` | `A02` | — | Resolve identity/role context |
| `A02` | `A03` | — | Request OTP |
| `A03` | `D01` | — | Check official channel |
| `D01` | `A04` | [Unavailable] | Login remains incomplete |
| `A04` | `MEND` | — | End unavailable-provider branch |
| `D01` | `A05` | [Available] | Submit OTP |
| `A05` | `A06` | — | Verify OTP |
| `A06` | `D02` | — | Evaluate verification |
| `D02` | `A07` | [Invalid / expired / reused / rate-limited] | No session |
| `A07` | `MEND` | — | End failed-auth branch |
| `D02` | `A08` | [Valid] | Check authorization after OTP |
| `A08` | `D03` | — | Evaluate role/account status |
| `D03` | `A09` | [Disabled / revoked / unauthorized] | Deny role context |
| `A09` | `MEND` | — | End access-denied branch |
| `D03` | `A10` | [Enabled and authorized] | Create session |
| `A10` | `A11` | — | Apply role functions |
| `A11` | `MEND` | — | Success path ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- All human accounts use passwordless official WhatsApp OTP.
- Role-specific privileges remain separated.
- Successful authentication creates a revocable session/token.

## Forbidden content

- Password login/Forgot Password.
- SMS OTP.
- Public self-assignment of Facility/Doctor/Platform roles.
- Session creation before role/access revalidation.

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
