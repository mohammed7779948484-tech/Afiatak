# Bootstrap Report

Date: 2026-08-16
Status: ready for semantic extraction

## Built

- Explicit product/course/tool authority model and SHA-256 registry, including whole-tree integrity for the immutable draw.io skill.
- Machine-readable lecturer course profile covering all ten required visual UML families plus structured textual use-case modeling.
- Typed semantic/view records, JSON Schemas, stable ID policy, provenance/rationale validation, and dependency registry.
- Central academic design system with palette, typography, geometry, routing, named layers, and executable per-type profiles.
- Deterministic uncompressed mxGraph document layer with native editable cells, containment, labels, ports, orthogonal routes, waypoints, and XML escaping.
- Distinct renderers for use case, package, class, object, activity, sequence, communication, state, component, and deployment diagrams.
- Structured use-case-model YAML to Markdown generation through the CLI.
- Q0-Q7 pipeline: source, schema, traceability, UML, structure, geometry/routing, visual-review state, approval/release.
- Manifest and staleness checks for sources, model, view, governance, design, compiler, vendored skill, requested targets, and outputs.
- Draw.io preview/final export adapter, editable embedded exports, PNG repair, browser fallback, and vendored edge-port/structural validation integration.
- Synthetic Example Library fixtures, negative fixtures, and unit/integration/regression coverage.

## Decisions

- YAML is canonical for human-authored semantic/view inputs; JSON Schema validates contracts.
- `.drawio` remains generated and editable, never canonical business truth.
- Deterministic layout is the default; Graphviz remains optional for future large graph-assisted views and is not allowed to define semantics.
- The vendored skill is wrapped, not forked.
- Q6 requires a review record whose preview hash matches the current render when draw.io is available. It is explicitly non-applicable when the CLI is unavailable; requested image outputs still fail rather than being silently omitted.
- Models marked `testData` cannot pass Q7 release.

## Verification

- `python -m pytest`: 36 passed after final gate additions.
- `ruff check .`: passed.
- `python -m engine.cli validate`: passed, including all protected hashes.
- Vendored draw.io validator: exercised through every synthetic renderer; route warnings are promoted through Q5 where applicable.
- Determinism: repeated synthetic use-case output bytes match.
- Negative gates: missing provenance, dangling relations, invalid parents, overlap, connector-through-node, invalid message order, unreachable state, incompatible component connector, path traversal, missing export tooling, and synthetic release attempts are rejected.
- Synthetic Q7 release, manifest, `CURRENT` staleness, and artifact registration were exercised and then removed.
- `git diff --check`: passed.

## Review Passes

- A Architecture: compiler boundaries, typed interfaces, and output determinism reviewed.
- B Skill compliance: all skill files/resources audited; XML, routing, export, repair, and validation conventions integrated.
- C UML infrastructure: all required families and textual use-case modeling reviewed; missing notation and graph invariants repaired.
- D Design system: tokens/profiles centralized; inert profile fields removed or executed.
- E Validation: broken synthetic fixtures and targeted negative tests confirmed rejection.
- F Rendering: all synthetic families render and pass structural/geometry gates; native image export could not run locally.
- G Agent UX: `AGENTS.md`, README, CLI, and workflow documentation reviewed from a new-agent perspective.
- H Cleanup: generated work, QA reports, test release artifacts, and registry entries removed.

## Tool Availability

- Python 3.14.3: available.
- Vendored draw.io scripts: available and integrity-verified.
- Native draw.io desktop CLI: unavailable on PATH and at the standard Windows installation path.
- Graphviz `dot`: unavailable.

## Limitations

- PNG/SVG/PDF/JPG export and image-based visual inspection were not executable in this environment. `doctor` reports this, Q6 records it explicitly, and requested image builds fail cleanly.
- Optional Graphviz-assisted layout is documented but unavailable locally; deterministic type-specific layouts are fully functional.
- No CI workflow was added because the local bootstrap requirement is satisfied by the reproducible CLI/test suite; CI can invoke the same commands later.

## Readiness

No real Aafiatak actor, use case, class, state, scenario, component, deployment node, or diagram was created. `model/` and `views/` contain guidance/placeholders only. All executable domain content is visibly marked synthetic test data.

The repository is ready for the next task: **Build the Aafiatak Use Case Diagram.**
