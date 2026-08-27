# CMP-01 — Final Visual / UML-Notation Refinement Review

## Scope and canonical artifacts

This report records the **final visual and UML-notation refinement** of CMP-01, the Aafiatak Medical Appointment Booking System Component Diagram. This pass was deliberately restricted to composition, rendering, component-specific visual QA, and editable diagrams.net parity. The semantic model and selected view inventory were not changed.

| Canonical layer | Repository artifact |
|---|---|
| Frozen semantic model | `model/catalog/components/aafiatak-system-component-architecture.yaml` |
| Component ViewSpec | `views/component/aafiatak-system-component-architecture.yaml` |
| Shared visual tokens and composition | `engine/compositions/component_diagram_layouts.py` |
| Direct SVG renderer | `engine/svg/component_diagram.py` |
| Component SVG QA | `qa/component_svg_validation.py` |
| Editable diagrams.net exporter | `engine/component_drawio_export.py` |
| Focused visual regression suite | `tests/unit/test_component_visual_refinement.py` |
| Final SVG / PNG / manifest | `build/final/aafiatak-system-component-architecture.{svg,png,manifest.json}` |
| Final editable file | `build/final/aafiatak-system-component-architecture.drawio` |

## Semantic invariants — unchanged

| Semantic item | Required | Verified |
|---|---:|---:|
| Component diagrams | 1 | 1 |
| Components | 9 | 9 |
| Provided interfaces | 6 | 6 |
| Required interfaces | 7 | 7 |
| Provided-interface realizations | 6 | 6 |
| Assembly connectors | 7 | 7 |
| Component dependencies | 0 | 0 |

The Aafiatak Backend remains one component. The three client components, PostgreSQL, and the four right-side service/provider components remain exactly as modelled. In particular, **Map Service** retains its provided `Map / Location Interface` with no required interface, connector, dependency, or invented technical consumer.

## Actual defects corrected

| ID | Baseline observation | Durable correction | Verification |
|---|---|---|---|
| V-01 | The SVG used two visually floating rectangles rather than a coherent UML component/module glyph. | The renderer now declares `data-component-symbol="uml-module"` and draws two left-boundary-attached module tabs. The exporter uses matching `shape=module` notation. | SVG QA Q4 passed; all component glyphs inspected in final PNG. |
| V-02 | The 16000×9000 layout was too spacious. | The composition was recomposed rather than uniformly scaled, using a 12400×7200 landscape canvas: **22.5% narrower** and **20% shorter**. | Final canvas, full PNG, and all regional tiles inspected. |
| V-03 | Interface labels occupied component bodies and competed with component names. | Shared external label anchors were added for provided lollipops and required sockets. | Q5 label-inside-owner and label/name-collision checks passed. |
| V-04 | Labels were visually detached from their own interface glyphs. | Short attached stems and label-to-glyph distance constraints were added. | Q5 stem-attachment and label-distance checks passed. |
| V-05 | Client paths had overly long/ambiguous shared convergence. | Three separately routed orthogonal ingress lanes terminate at distinct points of the Backend lollipop; the Platform Administration lane uses a near-Backend clearance corridor. | Q5 connector crossing, label-intersection, and shared-segment checks passed. |
| V-06 | Geometry QA did not protect the required visual constraints. | Q5 now evaluates compactness, component-name/glyph clearance, labels, stems, crossings, and shared segments; focused regression tests cover these behaviours. | 9 focused visual tests and full 24-test suite passed. |

## Lecturer-style notation and layout review

The final artwork is a white academic page with restrained dark strokes, sans-serif component names, a lecturer-style title, recognisable UML module component silhouettes, attached lollipops for provided interfaces, attached sockets for required interfaces, and clean orthogonal assembly connectors. It deliberately contains no gradients, shadows, coloured cards, actors, lifelines, cloud symbols, dashboard decoration, legends, or notation from other UML diagram families.

The actual final **8192×4757** PNG was inspected in **12 ordered, overlapping high-resolution tiles**, covering regions A–L: all three clients and their sockets, Backend interfaces and name field, PostgreSQL, WhatsApp Authentication Provider, Payment Gateway, Notification Service, Map Service, the client convergence routes, outer page edges, and full-page title continuity. The review found no clipping, floating component tabs, interface-label collisions, connector-through-label defects, connector crossings, unintended relations, or Map-Service connector.

## SVG / diagrams.net parity

The direct SVG renderer and the editable diagrams.net exporter both derive component boxes, interface placements, connector paths, typography, and visual tokens from `layout_for()` and `TOKENS`. The exported `.drawio` file was structurally validated after final generation with **0 errors**, **0 warnings**, and a routing score of **0**: no through-vertex conditions, crossings, or overlaps.

## Verification record

```text
python3 -m pytest tests/unit/test_component_visual_refinement.py -q
python3 -m engine.cli qa views/component/aafiatak-system-component-architecture.yaml
python3 tools/export_component_drawio.py \
  views/component/aafiatak-system-component-architecture.yaml \
  build/work/aafiatak-system-component-architecture-refined.drawio
python3 .agents/skills/drawio/scripts/validate.py \
  build/work/aafiatak-system-component-architecture-refined.drawio --score
python3 -m pytest -q
python3 -m engine.cli render \
  views/component/aafiatak-system-component-architecture.yaml \
  --output build/work/aafiatak-system-component-architecture-refined.svg
python3 -m engine.cli build views/component/aafiatak-system-component-architecture.yaml
```

Before the final ViewSpec update, Q4 and Q5 passed with no diagnostics, the focused suite passed **9/9**, the complete suite passed **24/24**, and the diagrams.net structural validator returned a clean result. The ViewSpec records the SHA-256 preview hash for the final inspected PNG and keeps `visualReview.status: awaiting-user-approval`; this internal review is not user approval.

Semantic status: verified
Structural QA: passed
Geometry QA: passed
Lecturer-style visual review: passed
Visual status: awaiting-user-approval
