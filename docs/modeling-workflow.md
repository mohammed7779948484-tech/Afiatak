# Modeling Workflow

1. Verify source integrity with `validate-sources` and review authority precedence.
2. Extract only source-supported semantic records into the relevant `model/catalog/` area. Assign stable IDs and precise `sourceRefs`.
3. Record significant ambiguity in an ADR; never resolve an open product decision by assumption.
4. Create structured use-case models and scenarios before dependent activity/interaction views.
5. Create a view that selects canonical IDs and expresses only high-level presentation intent such as zones, roles, rank, side, and proximity.
6. Run `validate-view`, `traceability`, and `render`.
7. Run `qa`; inspect the actual PNG/SVG preview when draw.io is available and record reviewer notes with the matching hash. Correct design, view intent, composition, or routing sources, not only generated XML.
8. Mark the view `approved` only after review, then run `build`.
9. Track approved final artifacts and manifests; rerun `stale` when sources or tooling change.

Dependencies are a graph, not one universal sequence. Actor/use-case work feeds use-case visuals and scenario-based behavior diagrams; domain modeling feeds class/object/state; technical boundaries feed component/deployment.
