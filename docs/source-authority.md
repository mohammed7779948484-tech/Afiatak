# Source Authority

The product specification, lecturer PDF, approved use-case work, and rendering implementation have separate responsibilities and are intentionally not merged.

The product specification is the only authority for Aafiatak scope, actors, permissions, business rules, lifecycles, technical boundaries, exclusions, and open decisions. The lecturer PDF defines required UML families and course-specific notation/content expectations. `docs/use_case.md` preserves the approved complete Use Case inventory. Direct SVG composition is implementation only. The vendored draw.io skill applies only when an optional `.drawio` artifact is requested.

Protected paths and hashes are registered in `registry/sources.yaml`. Q0 fails on a missing or changed input. Derived course constraints are in `governance/course-profile.yaml`; broader engineering conventions are in `governance/modeling-policy.yaml` so their provenance remains distinguishable.
