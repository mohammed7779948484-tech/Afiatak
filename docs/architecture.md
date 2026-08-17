# Compiler Architecture

The repository follows one directional pipeline:

```text
authoritative sources
  -> authority and governance
  -> canonical semantic model
  -> diagram view selection
  -> deterministic/type-specific layout
  -> type-specific UML renderer
  -> native uncompressed draw.io XML
  -> Q0-Q6 validation and review
  -> Q7 approved release + manifest
```

## Boundaries

Semantic records define what exists and why. Views select IDs and presentation options. Layout assigns geometry. Renderers translate UML meaning into mxGraph cells. The low-level `engine/drawio/` layer owns XML mechanics only.

Each visual family has a renderer module. Shared behavior lives in `BaseRenderer`; use-case layout is specialized so actors remain outside a true system-boundary container. The generated document uses stable semantic cell IDs, explicit layers, native editable shapes, expanded edge geometry, and uncompressed XML.

Graphviz is optional and reserved for large class/package/component graphs. The repository-local skill remains immutable and is wrapped for structural lint, edge-port assignment, export repair, and browser fallback rather than forked.

Manifests record source, model, design, renderer, QA, and output hashes. `stale` compares those against current inputs.
