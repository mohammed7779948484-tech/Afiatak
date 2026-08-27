# CMP-01 — Aafiatak System Component Architecture

## Final implementation review

This report records the end-to-end implementation and review of **CMP-01**, the single UML Component Diagram for the approved Aafiatak MVP. The canonical execution contract is the preserved reviewed specification, supported by the project MVP specification and the lecturer notation reference. The diagram is generated reproducibly from semantic YAML through the Component ViewSpec, central composition, dedicated SVG renderer, component-specific QA, preview generation, generic build path, artifact manifest, and editable diagrams.net export.

| Canonical layer | Repository artifact |
|---|---|
| Semantic model | `model/catalog/components/aafiatak-system-component-architecture.yaml` |
| View | `views/component/aafiatak-system-component-architecture.yaml` |
| Composition | `engine/compositions/component_diagram_layouts.py` |
| Renderer | `engine/svg/component_diagram.py` |
| Component QA | `qa/component_svg_validation.py` |
| Final SVG | `build/final/aafiatak-system-component-architecture.svg` |
| Final PNG | `build/final/aafiatak-system-component-architecture.png` |
| Manifest | `build/final/aafiatak-system-component-architecture.manifest.json` |
| Editable draw.io | `build/final/aafiatak-system-component-architecture.drawio` |

## Exact final counts

| Semantic item | Required | Verified |
|---|---:|---:|
| Component Diagrams | 1 | 1 |
| Components | 9 | 9 |
| Provided Interfaces | 6 | 6 |
| Required Interfaces | 7 | 7 |
| Assembly Connectors | 7 | 7 |
| Provided-Interface Realizations | 6 | 6 |
| Component Dependencies | 0 | 0 |

## Nine-pass review record

| Pass | Actual review performed | Result |
|---:|---|---|
| 1 | Ran `validate-sources`; preserved and registered the reviewed CMP-01 specification with SHA-256 `c7c8edee23d547c41f14459aa24a6053cb609747c756463a6125ba0d04ff8c1f`. Reviewed the product specification, governance records, and lecturer PDF pages 10–11. | Passed |
| 2 | Counted all semantic records and compared the rendered `data-kind=component` inventory with the selected ViewSpec inventory. Confirmed no forbidden application or microservice split. | Passed |
| 3 | Counted six provided and seven required interfaces. Verified each provided interface has one realization from its provider and each required interface declares one visible `metadata.ownerComponent`. | Passed |
| 4 | Verified the seven rendered assembly connectors and their Required→Provided endpoints against the canonical connector relations. No component dependency relation is selected or rendered. | Passed |
| 5 | Searched existing model and view artifacts for Patient Application, Backend, Payment Gateway, Notification Service, WhatsApp Authentication Provider, and Map Service. The Component model is consistent with approved interaction boundaries without promoting scenario participants into components. | Passed |
| 6 | Audited the model and SVG for forbidden technology labels, invented services, SMS/password elements, direct patient-to-payment connection, and a Map Service consumer. The Map Service lollipop remains intentionally unconnected. | Passed |
| 7 | Inspected the lecturer Component-Diagram reference and checked the final render for simple white background, dark standard component rectangles and glyphs, lollipops, sockets, and assembly connectors. No actors, lifelines, messages, classes, states, decisions, cloud icons, shadows, gradients, or decorative cards are present. | Passed |
| 8 | Ran Component SVG QA. Q5 checked page safe bounds, component-body intersections, interface-label intersections, glyph placement, connector attachment, and connector-through-unrelated-component errors. | Passed |
| 9 | Opened the actual final SVG and inspected all 28 ordered overlapping PNG tiles at source resolution. Checked labels, glyphs, title, client routes, Backend centrality, persistence route, external routes, artboard edges, and the unconnected Map Service. | Passed |

## Defects found and corrected

The first Component QA run exposed one geometry defect: the `Aafiatak Application Interface` label inside Backend overlapped the `Payment Interface` label. The correction was made in the canonical component composition by moving the provided-interface label into the free upper interior lane of Backend. After regeneration, Q4 and Q5 both passed. The diagrams.net command-line export initially lacked a repository-root import path when invoked from `tools`; this was corrected in the reusable export tool before the final editable file was generated.

## Mandatory boundary confirmations

The central Backend remains a single component. `Facility Web Dashboard` remains a single component for Facility Administrator, Booking & Reception Staff, and Doctor roles. PostgreSQL is shown only as a persistence component, not as an ERD. WhatsApp Authentication Provider is connected only through the authentication interface, while general system notification delivery is connected to Notification Service. Backend and web-dashboard technologies are not asserted. `Map Service` has its provided `Map / Location Interface` but no required interface, assembly connector, dependency, or invented technical caller.

## Verification commands executed

```text
python3 -m engine.cli validate-sources
python3 -m engine.cli validate-model model/catalog/components/aafiatak-system-component-architecture.yaml
python3 -m engine.cli validate-view views/component/aafiatak-system-component-architecture.yaml
python3 -m engine.cli traceability model/catalog/components/aafiatak-system-component-architecture.yaml
python3 -m pytest -q
python3 -m engine.cli render views/component/aafiatak-system-component-architecture.yaml --output build/work/aafiatak-system-component-architecture.svg
python3 -m engine.cli qa views/component/aafiatak-system-component-architecture.yaml
python3 -m engine.cli build views/component/aafiatak-system-component-architecture.yaml
python3 tools/export_component_drawio.py views/component/aafiatak-system-component-architecture.yaml build/final/aafiatak-system-component-architecture.drawio
python3 .agents/skills/drawio/scripts/validate.py build/final/aafiatak-system-component-architecture.drawio
```

The Component SVG QA has no diagnostics, with Q4 = `pass` and Q5 = `pass`. The output manifest records `result = pass` and Q7 = `awaiting-user-approval`. The diagrams.net structural linter found zero errors; its 49 warnings are expected containment reports for the white page rectangle and interface labels deliberately placed inside their owner/provider Component boxes, not overlap defects in the generated SVG. The semantic SVG/PNG outputs are the primary assessed artifacts.

Semantic status: verified
Structural QA: passed
Geometry QA: passed
Visual status: awaiting-user-approval
