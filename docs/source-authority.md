# Source Authority

The product specification, lecturer PDF, and draw.io skill have separate responsibilities and are intentionally not merged.

The product specification is the only authority for Aafiatak scope, actors, permissions, business rules, lifecycles, technical boundaries, exclusions, and open decisions. The lecturer PDF defines required UML families and course-specific notation/content expectations. The vendored skill defines draw.io XML, shapes, routing, validation, and export mechanics. General UML knowledge may supply only compatible mechanics.

Protected paths and hashes are registered in `registry/sources.yaml`. Q0 fails on a missing or changed input. Derived course constraints are in `governance/course-profile.yaml`; broader engineering conventions are in `governance/modeling-policy.yaml` so their provenance remains distinguishable.
