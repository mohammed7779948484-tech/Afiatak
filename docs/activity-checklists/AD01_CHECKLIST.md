# AD-01 Implementation Checklist — Register Patient

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD01_Register_Patient_FINAL_VERIFIED_v2.md`
- SHA-256: `6e957f4c0761a588c2f120c2794d624d7f6953c60e9e21f7609a996824c28e33`
- Package: Visitor Package
- Exact title: Activity Diagram — Register Patient
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Visitor is not authenticated as a Patient.
- 2. A phone number can be normalized and verified.
- 3. Public Patient self-registration is available.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Visitor chooses Register Patient and provides phone number |
| `A02` | Action | Normalize phone number and check global identity uniqueness |
| `D01` | Decision | Existing identity? |
| `A03` | Action | Reject duplicate registration and direct to existing-account login path |
| `A04` | Action | Request short-lived single-use WhatsApp OTP |
| `D02` | Decision | WhatsApp authentication channel available? |
| `A05` | Action | Keep registration incomplete; no fallback authentication |
| `A06` | Action | Visitor receives and submits OTP |
| `A07` | Action | Verify OTP expiry, single-use, rate-limit and brute-force controls |
| `D03` | Decision | OTP valid and permitted? |
| `A08` | Action | Reject verification; create no Patient account |
| `A09` | Action | Visitor provides approved basic Patient profile data and confirms registration |
| `A10` | Action | Validate non-clinical registration data |
| `A11` | Action | Create User + Patient exactly once for verified phone identity |
| `A12` | Action | Establish approved Patient account context without password |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin registration |
| `A01` | `A02` | — | Normalize and check identity |
| `A02` | `D01` | — | Evaluate uniqueness |
| `D01` | `A03` | [Yes — existing identity] | No duplicate identity |
| `A03` | `MEND` | — | Alternative/failure ends |
| `D01` | `A04` | [No — identity available] | Continue verification |
| `A04` | `D02` | — | Evaluate official WhatsApp channel |
| `D02` | `A05` | [Unavailable] | No SMS/password fallback |
| `A05` | `MEND` | — | Incomplete registration ends |
| `D02` | `A06` | [Available] | Continue OTP exchange |
| `A06` | `A07` | — | Verify OTP |
| `A07` | `D03` | — | Evaluate OTP result/security limits |
| `D03` | `A08` | [Invalid / expired / reused / rate-limited] | No verified account |
| `A08` | `MEND` | — | Failed verification ends |
| `D03` | `A09` | [Valid] | Continue profile creation |
| `A09` | `A10` | — | Validate allowed profile data |
| `A10` | `A11` | — | Idempotent identity/profile creation |
| `A11` | `A12` | — | Establish Patient context |
| `A12` | `MEND` | — | Success path ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- One normalized verified phone identifies one User.
- Create Patient profile only after successful phone verification.
- No clinical data in registration.
- OTP exact lifetime is not fixed in this diagram.

## Forbidden content

- Patient as the starting actor label instead of Visitor.
- Creating an UNVERIFIED Patient before OTP success.
- Password, Forgot Password, SMS authentication.
- Actual OTP/secret values in labels.

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
