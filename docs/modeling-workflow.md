# Modeling Workflow

1. Verify protected sources and authority precedence.
2. Preserve complete product behavior in the canonical semantic model.
3. Select only lecturer-correct overview content in the view; map remaining behavior to actor-package detail or Use Case Modeling.
4. Compose the diagram explicitly in `engine/compositions/`.
5. Run `validate-view`, `render`, and `preview`.
6. Open the actual PNG, refine the composition, and record its hash.
7. Run `build`; keep visual status `awaiting-user-approval` until the user accepts it.
