# Layout Backends

`deterministic.py` is the default constraint/grid backend. Large class, package, or component views may be adapted to the immutable skill's `autolayout.py` when `doctor` reports Graphviz available. Layout output never changes semantic relationships.

Use-case profiles with `composition: curated-editorial` call
`LayoutEngine.curated_editorial(elements, profile=..., design_geometry=..., intent=...)`.
The intent describes functional `zones`, `visualRoles`, preferred rows/columns/sides,
and actor `near`/`proximity` targets. The result supplies page-space canvas, title,
boundary, and actor geometry plus boundary-relative heading and use-case geometry.
It creates no package containers and does not route relationships.

`LayoutEngine.plan_use_case(...)` is the renderer-facing adapter. It consumes the
loaded model, view, profile, design system, selected actors/use cases, and relations;
non-curated profiles return `None`. Curated output is `UseCaseComposition`, with
`canvas`, `title`, `boundary`, `headings`, raw `actors`/`use_cases` geometry maps,
`case_roles`, `placement_metadata`, and an empty `route_overrides` map for the
separate routing stage.
