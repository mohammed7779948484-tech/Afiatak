# Aafiatak Diagram Engineering Map

This repository compiles traceable semantic UML models and view specifications into editable draw.io artifacts. It does not treat `.drawio` coordinates or styling as product truth.

## Authority

1. `Aafiatak_Project_Specification_EN.md` defines product truth.
2. The root UML PDF registered in `registry/sources.yaml` defines course submission constraints.
3. `.agents/skills/drawio/SKILL.md` and its references define draw.io mechanics.
4. General UML knowledge fills only non-conflicting technical gaps.

Never invent an Aafiatak requirement. Record genuine ambiguity in `governance/decisions/`.

## Map

- Protected inputs: paths marked immutable in `registry/sources.yaml`; do not edit them.
- Semantic truth: `model/catalog/`, `model/scenarios/`, `model/use-case-models/`.
- Diagram selections: `views/<diagram-type>/`.
- Visual rules: `design/` and `design/profiles/`.
- Compiler: `engine/`; QA rules: `qa/`; generated work: `build/`.
- Use the repository-local draw.io skill for all draw.io generation/export work.

## Commands

- Install: `python -m pip install -e ".[dev]"`
- Validate: `python -m engine.cli validate`
- Render: `python -m engine.cli render <view.yaml>`
- QA: `python -m engine.cli qa <view.yaml>`
- Build/release: `python -m engine.cli build <view.yaml>`
- Tests: `python -m pytest`
- Tool check: `python -m engine.cli doctor`

## Done

A diagram is done only when source integrity, schema, traceability, UML semantics, draw.io structure, geometry, preview review, and release gates pass. Generated `.drawio` may be manually refined, but changes must be represented back in semantic/view/layout sources before they become permanent truth.

## Visual Diagram Engineering Rules

- Semantic correctness and visual quality are separate requirements; structural QA passing does not imply visual quality.
- `design/` is the single visual source of truth. Renderers must not contain arbitrary diagram-specific colors, font sizes, or geometry values.
- Views select semantics and express high-level presentation intent; they must not become collections of manually authored edge waypoints.
- Layout engines own node placement, routing engines own connector paths, and type-specific composition planners may be used when generic layout is insufficient.
- Generated diagrams must be visually inspected from an actual PNG or SVG render.
- Manual refinement is allowed only when represented back in canonical layout or design configuration.
- No web app, frontend, backend, server, database, diagrams.net plugin, hosted platform, or unrelated product is required.
- The system remains a small local diagram-generation workspace producing editable `.drawio`, SVG, and PNG artifacts.

## Main Use Case Diagram Execution

- `docs/use case.md` (stored at `docs/use_case.md`) is the approved execution specification for the Main Use Case Diagram.
- The authoritative Aafiatak MVP/project specification at the repository root is the mandatory product-truth reference.
- The lecturer's UML document at the repository root is the mandatory academic/UML-rule reference.
- The local draw.io skill under `.agents/skills/` governs diagrams.net authoring, rendering, routing, and structural mechanics.
- Never use any previous Aafiatak Use Case image or old diagram.
- Never invent actors, use cases, permissions, relationships, or product behavior.
- All Actors, including external-system actors, must be outside the System Boundary. All Use Cases must be inside it.
- Follow the exact Main Use Cases, actor associations, `<<include>>`, and `<<extend>>` relationships defined in `docs/use case.md` (`docs/use_case.md`).
- `<<include>>`: base use case to mandatory included use case. `<<extend>>`: extending/conditional use case to base use case.
- Do not use arrows to represent chronological order.
- Do not introduce Classes, Attributes, Database entities, Components, or deferred features.
- Every visible label must be English. Every Use Case name must begin with a verb.
- Do not redesign or re-bootstrap the existing diagram-engineering system.
- Do not create test files, fixtures, regression cases, synthetic diagrams, test datasets, or test infrastructure.
- Do not run full test suites, regression suites, coverage work, or unrelated validation.
- Use only the smallest existing structural validation needed to ensure the `.drawio` is valid and editable.
- Prioritize fast, correct, visually professional execution today.
