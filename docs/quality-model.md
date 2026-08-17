# Quality Model

- Q0: protected source hashes match.
- Q1: model and view schemas, IDs, and references are valid.
- Q2: semantic elements and relationships remain traceable.
- Q3: UML element types and relationship endpoints/directions are valid.
- Q4: SVG/XML parses and represents every selected semantic element and relation exactly once.
- Q5: actors are outside the boundary, use cases are inside, semantic nodes do not overlap, and connectors do not run through unrelated semantic nodes.
- Q6: records `generated`, `internally-reviewed`, `awaiting-user-approval`, or `approved`. A hash identifies the inspected artifact but never certifies beauty.
- Q7: release remains `awaiting-user-approval` until the user explicitly accepts the visual result.
