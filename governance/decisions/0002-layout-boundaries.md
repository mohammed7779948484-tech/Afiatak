# ADR-0002: Deterministic Layout with Optional Graphviz

- Status: accepted
- Date: 2026-08-16
- Authority impact: modeling-only

## Decision

Use deterministic constraint-based layouts by default. Permit the vendored Graphviz-backed `autolayout.py` only for large class, package, and component graphs. Sequence geometry remains deterministic; Graphviz is never allowed to define semantics.
