# Quality Model

- Q0 Source Integrity: immutable paths and SHA-256 values match.
- Q1 Schema Validation: YAML records and views conform to explicit JSON Schemas; IDs are unique and namespaced.
- Q2 Traceability: elements and relations have source references; derived UML relations have rationale.
- Q3 UML Semantics: type-specific endpoint, direction, ordering, multiplicity, state/activity, and package rules pass.
- Q4 Draw.io Structure: XML parses; roots, IDs, containment, edges, and geometry are valid; the vendored validator passes.
- Q5 Geometry/Routing: structural checks plus centralized warnings for crossings, route length, bends, congestion, occupancy, balance, actor proximity, labels, and size consistency.
- Q6 Rendered Visual QA: a clean width-capped preview is actually inspected; the preview hash and exporter version identify the reviewed image but are not themselves visual approval. Release fails closed when no rendered review is available.
- Q7 Release: the view is approved and every applicable blocking gate passes.

Q6 is reported as unavailable rather than faked when draw.io is missing. Q7 may release editable XML in that environment only when the configured gate marks export-dependent visual QA conditional; image deliverables remain absent and explicitly reported.
