# Aafiatak Diagram Engineering System

This repository is a compiler-style UML modeling toolchain for Aafiatak. It turns traceable semantic YAML and view specifications into deterministic, editable draw.io XML, validates the result through Q0-Q7, and releases approved artifacts with manifests.

It is not the Aafiatak application, a drawing-only folder, or a replacement for the authoritative product specification. `.drawio` files are generated editable artifacts, not business truth.

## Authority

1. `Aafiatak_Project_Specification_EN.md`: product scope and rules.
2. The UML PDF registered in `registry/sources.yaml`: lecturer/course constraints.
3. `.agents/skills/drawio/`: draw.io mechanics and vendored tooling.
4. General UML knowledge: non-conflicting technical gaps only.

See `docs/source-authority.md` and `governance/authority.yaml`.

## Quick Start

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
.venv\Scripts\python -m engine.cli doctor
.venv\Scripts\python -m engine.cli validate
.venv\Scripts\python -m pytest
```

On shells where the environment is activated, use `python` directly.

## Commands

```text
python -m engine.cli validate [view.yaml]
python -m engine.cli validate-sources
python -m engine.cli validate-model model.yaml
python -m engine.cli validate-view view.yaml
python -m engine.cli traceability model.yaml
python -m engine.cli render view.yaml
python -m engine.cli render-use-case-model use-case-model.yaml
python -m engine.cli preview view.yaml
python -m engine.cli qa view.yaml
python -m engine.cli build view.yaml
python -m engine.cli stale build/final/name.manifest.json
python -m engine.cli doctor
python -m engine.cli list-diagram-types
```

`build` requires `approval: approved`, passes all applicable gates, and writes `.drawio` plus a hash manifest to `build/final/`. Preview/image export is conditional on the native draw.io desktop CLI; XML rendering and structural QA remain available without it.

## Repository Map

- `governance/`: authority, course rules, policies, gates, ADRs.
- `registry/`: protected sources, supported diagram types, released artifacts.
- `model/`: future canonical semantic truth and structured use-case models.
- `views/`: diagram selections referencing semantic IDs.
- `design/`: centralized palette, typography, geometry, routing, and profiles.
- `engine/`: schemas, layout, draw.io XML, renderers, export, manifests, CLI.
- `qa/`: traceability, UML, structural, geometry, and visual-review gates.
- `tests/fixtures/`: explicitly synthetic test data only.
- `build/`: generated work; only approved `build/final/` output is trackable.

See `docs/adding-a-diagram.md` before creating the first real view.
