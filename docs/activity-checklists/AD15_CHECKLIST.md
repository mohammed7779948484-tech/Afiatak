# AD-15 Implementation Checklist — Review Facility Onboarding Request

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD15_Review_Facility_Onboarding_FINAL_VERIFIED_v2.md`
- SHA-256: `1ac72df4f6f8b310025d48288864d31e0f71ba1e84dd0ebf222faed3d10ec1bd`
- Package: Platform Administrator Package
- Exact title: Activity Diagram — Review Facility Onboarding Request
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Platform Administrator is authenticated/authorized.
- 2. A facility onboarding request exists in protected platform intake/review.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Platform Administrator opens pending onboarding request |
| `A02` | Action | Display submitted onboarding information, current review status and prior history |
| `A03` | Action | Platform Administrator evaluates available information |
| `D01` | Decision | Information sufficient for responsible review assessment? |
| `A04` | Action | Record Request Additional Information action and preserve review history |
| `A05` | Action | Keep onboarding unresolved pending additional information |
| `A06` | Action | Platform Administrator records review assessment |
| `D02` | Decision | Assessment outcome? |
| `A07` | Action | Make separate Approve Facility use case available as next permitted action |
| `A08` | Action | Make separate Reject Facility use case available as next permitted action |
| `A09` | Action | Preserve documented review result / history and complete review step |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin review |
| `A01` | `A02` | — | Load review context/history |
| `A02` | `A03` | — | Evaluate |
| `A03` | `D01` | — | Sufficiency decision |
| `D01` | `A04` | [Insufficient] | Request-more-information path |
| `A04` | `A05` | — | Remain unresolved |
| `A05` | `MEND` | — | End current review cycle |
| `D01` | `A06` | [Sufficient] | Record assessment |
| `A06` | `D02` | — | Decision path |
| `D02` | `A07` | [Supports approval] | Next use case is separate Approve Facility |
| `A07` | `A09` | — | Preserve review result |
| `D02` | `A08` | [Supports rejection] | Next use case is separate Reject Facility |
| `A08` | `A09` | — | Preserve review result |
| `A09` | `MEND` | — | Review complete |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Platform administration is a protected internal workflow.
- Review result determines a permitted next action; approval/rejection remain separate Use Cases.

## Forbidden content

- Public FacilityApplicant Actor/portal.
- Automatic activation/provisioning inside Review.
- Silent approval or rejection when information is insufficient.
- Overwriting prior review history without traceability.

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
