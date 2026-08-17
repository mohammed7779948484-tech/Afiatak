# Aafiatak Diagram Engineering System

This repository turns traceable Aafiatak semantic YAML and a diagram view into a deterministic, human-composed SVG and a local PNG preview.

It is not the Aafiatak application or a replacement for the authoritative product specification. Composition coordinates are presentation data, not business truth.

## Authority

1. `Aafiatak_Project_Specification_EN.md`: product scope and rules.
2. The UML PDF registered in `registry/sources.yaml`: lecturer/course constraints.
3. `docs/use_case.md`: approved complete Use Case operation inventory.
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

`build` writes a clean SVG, PNG, and hash manifest to `build/final/`. SVG is primary; PNG is rasterized locally from that SVG. Visual status remains `awaiting-user-approval` until accepted by the user.

## Repository Map

- `governance/`: authority, course rules, policies, gates, ADRs.
- `registry/`: protected sources, supported diagram types, released artifacts.
- `model/`: future canonical semantic truth and structured use-case models.
- `views/`: diagram selections referencing semantic IDs.
- `design/use_case_theme.yaml`: the small active visual theme.
- `engine/compositions/`: explicit diagram artboards and connector paths.
- `engine/svg/`: the small direct-SVG renderer.
- `qa/`: traceability, UML, and objective SVG structural checks.
- `build/`: generated work; only approved `build/final/` output is trackable.

See `docs/adding-a-diagram.md` before creating the first real view.
