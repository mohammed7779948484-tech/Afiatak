# ADR-0001: Compiler Architecture and Canonical Sources

- Status: accepted
- Date: 2026-08-16
- Authority impact: modeling-only

## Context

Editable draw.io files must not become the only location of requirements or relationships.

## Decision

Use human-readable YAML semantic catalogs and views validated by JSON Schema. Typed Python compiles them into deterministic uncompressed draw.io XML. Generated coordinates and style are downstream artifacts.

## Consequences

Manual visual changes must be represented back in view/layout sources. Stable semantic IDs permit traceability and diffing.
