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
