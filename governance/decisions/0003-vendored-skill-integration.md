# ADR-0003: Wrap, Do Not Fork, the Vendored Draw.io Skill

- Status: accepted
- Date: 2026-08-16
- Authority impact: tooling-only

## Decision

Keep `.agents/skills/drawio/` immutable. The engine invokes its `validate.py`, `edgeports.py`, `repair_png.py`, and browser URL fallback through adapters. Project-specific semantic and UML validation remains in this repository.
