# AD-07 Implementation Checklist — Publish Availability

## Source provenance

- Authoritative MD: `../activity-specs/Aafiatak_AD07_Publish_Availability_FINAL_VERIFIED_v2.md`
- SHA-256: `36ddce2a8eb44540dce8c01c6ec68019f028546ae86264aa9188c840bc917acb`
- Package: Facility Administrator Package
- Exact title: Activity Diagram — Publish Availability
- Lock status: `awaiting-user-approval`

## Preconditions

- 1. Facility Administrator is authenticated/authorized.
- 2. Target AvailabilityRelease exists.
- 3. Required branch/doctor/service/date/reception-period and ArrivalGroups are prepared.
- 4. Governing commercial/booking terms are defined.

## Exact node inventory

| ID | UML type | Exact label |
|---|---|---|
| `I` | Initial Node | Start |
| `A01` | Action | Facility Administrator selects AvailabilityRelease for publication |
| `A02` | Action | Display configured session, ArrivalGroups, capacities and governing terms |
| `D01` | Decision | Release lifecycle is DRAFT? |
| `A03` | Action | Reject invalid / duplicate publication and return current lifecycle state |
| `A04` | Action | Validate required references, group windows/sequence, capacity sum and governing terms |
| `D02` | Decision | Publication configuration valid? |
| `A05` | Action | Reject publication and keep release editable in DRAFT |
| `A06` | Action | Facility Administrator confirms Publish Availability |
| `A07` | Action | Transition AvailabilityRelease from DRAFT to PUBLISHED |
| `A08` | Action | Freeze amount / currency / booking / cancellation / no-show terms for this release |
| `A09` | Action | Fix published capacity as non-increasing upper bound and record audit data |
| `A10` | Action | Confirm publication; new holds depend on PUBLISHED release + OPEN/time-eligible ArrivalGroup |
| `MEND` | Merge | End-path merge |
| `F` | Final Node | End |

## Exact control-flow audit

| From | To | Guard | Meaning |
|---|---|---|---|
| `I` | `A01` | — | Begin publish |
| `A01` | `A02` | — | Review current configuration |
| `A02` | `D01` | — | Check lifecycle |
| `D01` | `A03` | [No] | Only DRAFT -> PUBLISHED allowed |
| `A03` | `MEND` | — | No publication |
| `D01` | `A04` | [Yes] | Validate complete draft |
| `A04` | `D02` | — | Configuration decision |
| `D02` | `A05` | [Invalid / group-capacity mismatch / missing terms] | Remain DRAFT |
| `A05` | `MEND` | — | End validation failure |
| `D02` | `A06` | [Valid] | Proceed to confirmation |
| `A06` | `A07` | — | Lifecycle transition |
| `A07` | `A08` | — | Freeze governing terms |
| `A08` | `A09` | — | Fix capacity upper bound and audit |
| `A09` | `A10` | — | Show success |
| `A10` | `MEND` | — | Success ends |
| `MEND` | `F` | — | Activity final |

## Binding rules

- Allowed publication transition is DRAFT -> PUBLISHED.
- Published capacity cannot increase afterward.

## Forbidden content

- PUBLISHED -> PUBLISHED duplicate publish as new release.
- Any +1 capacity action after publication.
- Editing frozen published terms in place.
- Automatic patient booking from a DRAFT release.

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
