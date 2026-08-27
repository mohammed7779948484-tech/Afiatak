# DEP-01 Implementation Checklist

This checklist tracks the implementation of the single approved UML Deployment Diagram for the current Aafiatak MVP. It is operational documentation only; the reviewed DEP-01 specification remains the semantic and visual execution authority.

- [x] Verify authority hierarchy, product evidence, CMP-01 boundary, cross-diagram stable communications, and lecturer deployment notation.
- [x] Inspect the actual lecturer deployment page/reference visually.
- [x] Copy and register the reviewed DEP-01 execution specification with its SHA-256 source hash.
- [x] Create the canonical deployment semantic model with exactly nine deployment nodes and seven communication paths.
- [x] Create the DEP-01 ViewSpec with exact selection and invariant counts.
- [x] Add `deployment` support to the ViewSpec schema, type registry, pipeline render/QA dispatch, and generic build flow.
- [x] Write focused DEP-01 tests and observe expected RED failure before production implementation. The initial run failed for the expected missing `deployment` ViewSpec type and missing deployment composition module.
- [x] Implement deterministic deployment composition and standard UML 3D node rendering.
- [x] Render contained runtime/component labels and unarrowed communication paths.
- [x] Implement deployment-specific structural and geometry QA.
- [x] Generate a parity-aligned editable diagrams.net file from the same semantic/layout source. Structural lint: 0 errors, 0 warnings, 0 crossings, and 0 overlaps.
- [x] Run source/model/view/traceability validation, scoped tests, regression tests, QA, preview, and build. Final result: 29 tests passed; source/model/view validation passed; traceability 16/16; DEP-01 Q4/Q5 passed; CMP-01 QA rerun.
- [x] Inspect the actual generated SVG and PNG, correcting only canonical source/composition/renderer code. The final 8192×4757 PNG was reviewed as 12 ordered overlapping tiles, and the final SVG was opened independently.
- [x] Perform and document the nine required final review passes. See `build/qa/DEP01_MVP_Deployment_Topology_Final_Review.md`.
- [x] Update final preview hash while retaining `awaiting-user-approval`. The recorded hash matches the inspected final PNG.
- [x] Commit and push the validated DEP-01 update to `main` as `da3daa2 feat(uml): add DEP-01 deployment topology`.

## UML notation refinement — 2026-08-27

- [x] Inspect the current DEP-01 renderer, composition, QA, SVG, PNG, editable draw.io artifact, final review, and actual lecturer deployment example.
- [x] Write and observe RED tests for runtime/device-context/artifact visual distinctions, logical execution-environment node stereotypes, QA enforcement, and SVG/draw.io parity.
- [x] Add shared contained-item visual kinds: `execution-environment`, `deployed-artifact`, and `device-context`; retain the frozen topology and all routes.
- [x] Render secondary `«device»` and `«executionEnvironment»` node markers where approved, 3D execution-environment content, and folded-corner `«artifact»` deployed software.
- [x] Extend DEP-01 Q4 notation/duplicate checks while retaining Q5 containment, collision, path, and clipping checks.
- [x] Regenerate and inspect final SVG plus fit-to-page and twelve-tile PNG review; update the matching preview hash while retaining `awaiting-user-approval`.
- [x] Validate source/model/view/traceability, DEP-01 QA, full regression, CMP-01 regression QA, and diagrams.net strict lint. Final result: 34 tests passed; draw.io 0 errors, 0 warnings, score 0.
- [x] Commit and push the DEP-01 UML notation refinement to `main` as `e86c2d9 refine(uml): improve DEP-01 deployment notation`.
- [ ] Commit and push the compact line-and-design refinement to `main` after final artifact and PDF verification.
