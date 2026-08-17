# Adding a Diagram

1. Read `AGENTS.md`, `governance/authority.yaml`, and the relevant source sections.
2. Add canonical semantic records with stable namespaced IDs and `sourceRefs`. Do not use display names as keys.
3. For textual use-case modeling, conform to `engine/schemas/use-case-model.schema.json`.
4. Add a view under `views/<diagram-type>/` containing only selected IDs, relation IDs, layout profile, targets, and presentation options.
5. Run:

```text
python -m engine.cli validate-view views/<type>/<name>.yaml
python -m engine.cli traceability <model.yaml>
python -m engine.cli render views/<type>/<name>.yaml
python -m engine.cli qa views/<type>/<name>.yaml
```

6. Review the generated preview and editable XML. Feed lasting adjustments back into semantic/view/layout sources.
7. Set `approval: approved` and run `build` only after review.

Never use old screenshots as requirements, infer packages from color regions, infer classes from UI grouping, or preserve an unsupported relationship because it looks visually convenient.
