# Adding a Diagram

1. Read `AGENTS.md`, `governance/authority.yaml`, and the relevant source sections.
2. Add canonical semantic records with stable namespaced IDs and `sourceRefs`. Do not use display names as keys.
3. For textual use-case modeling, conform to `engine/schemas/use-case-model.schema.json`.
4. Add a view containing selected semantic IDs and relation IDs.
5. Add an explicit composition under `engine/compositions/` and render it through the small direct-SVG module.
6. Run:

```text
python -m engine.cli validate-view views/<type>/<name>.yaml
python -m engine.cli traceability <model.yaml>
python -m engine.cli render views/<type>/<name>.yaml
python -m engine.cli qa views/<type>/<name>.yaml
```

7. Open the generated PNG and feed lasting visual adjustments back into the composition.
8. Run `build`; keep visual status `awaiting-user-approval` until the user accepts the artifact.

Never use old screenshots as requirements, infer packages from color regions, infer classes from UI grouping, or preserve an unsupported relationship because it looks visually convenient.
