# Rendering Architecture

```text
authoritative sources
  -> canonical semantic model
  -> Main Overview view
  -> explicit Aafiatak composition
  -> direct SVG
  -> local PNG
```

The semantic model defines what exists. The view selects the overview subset. `engine/compositions/aafiatak_main_use_case.py` is an intentional artboard containing presentation coordinates and simple connector paths. `engine/svg/use_case.py` translates that artboard into lightweight, self-contained SVG.

The Main Use Case path does not use the legacy draw.io renderer, use-case grid planner, path-search router, or visual scoring metrics. Those use-case-specific components were retired. `.drawio` is optional and is not produced by the current build.
