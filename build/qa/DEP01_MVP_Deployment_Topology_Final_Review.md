# DEP-01 — MVP Deployment Topology: Final Review

## Review scope and conclusion

DEP-01 is the **first and only approved UML Deployment Diagram** for the current Aafiatak MVP. It was implemented through the repository's ordinary semantic-model → ViewSpec → deterministic composition → SVG → PNG → manifest pipeline. The result uses simple, monochrome UML deployment nodes with contained runtime/component labels and seven unarrowed communication paths. It does **not** claim a cloud, host, operating system, reverse proxy, container platform, or database-hosting arrangement.

> **Visual-review boundary.** The SVG and final PNG were actually reviewed by Manus AI, but the visual-review record deliberately remains `awaiting-user-approval`. Artifact review is not user approval.

| Item | Final value |
|---|---|
| Diagram ID | `DEP-01` |
| View ID | `aafiatak-mvp-deployment` |
| Reviewed execution spec | `docs/deployment-specs/Aafiatak_DEP01_MVP_Deployment_Topology_FINAL_REVIEWED.md` |
| Registered source identity | `dep01-mvp-deployment-reviewed-spec` |
| Execution-spec SHA-256 | `22239ffb7d1bb2e790301c6657a702aa9f13a1aecb757dfddc471ce36b68975c` |
| SVG / PNG final-review hash | `3c1a8d45eda58a797e75823c8fa9efe79e24edf1542121066a318732c4ec572d` / `2e88efceb968389e2f171f7cd61831ca53f572fbcd2d833573d56eba40dd7deb` |
| Visual-review status | `awaiting-user-approval` |

## Verified DEP-01 inventory

| Contract item | Required | Verified result |
|---|---:|---:|
| Deployment Diagrams | 1 | 1 |
| Top-level Deployment Nodes | 9 | 9 |
| Communication Paths | 7 | 7 |
| Internal software components mapped | 5 | 5 |
| External service Nodes | 4 | 4 |
| Map Service Communication Paths | 0 | 0 |
| Invented infrastructure nodes | 0 | 0 |

The nine selected nodes are Patient Mobile Device, Facility Client Device, Platform Administrator Client Device, Aafiatak Centralized Server, PostgreSQL Database Environment, WhatsApp Authentication Provider, Payment Gateway, Notification Service, and Map Service. The canonical semantic model includes only the required seven communication-path relations. The Map Service is included as a visible node but is intentionally excluded from all path endpoints.

## Nine-pass review record

| Pass | Checked evidence | Finding | Result |
|---:|---|---|---|
| 1. Authority and source integrity | Registered reviewed specification, product specification, governance hierarchy, and lecturer PDF | The execution specification is copied under `docs/`, registered with its real hash, and every DEP-01 node/path has source references. | Passed |
| 2. Exact nine-node inventory | Semantic model, ViewSpec, SVG Q4 inventory | All and only N01–N09 are selected/rendered exactly once. | Passed |
| 3. Component-to-node mapping | CMP-01 model and node `componentMapping` / `accessFor` metadata | Patient Application, Facility Web Dashboard, Platform Administration Dashboard, Aafiatak Backend, and PostgreSQL Database map to logical deployment representations without creating microservices. | Passed |
| 4. Exact communication paths and no arrowheads | Seven semantic relations, SVG Q4, actual PNG/SVG | CP01–CP07 have the mandated endpoint pairs, are solid, unnumbered, unlabeled, and unarrowed. | Passed |
| 5. Cross-diagram consistency | Main Use Case, sequence/collaboration stable boundaries, CMP-01, contradiction-only class/state/activity check | Only approved client/backend, persistence, WhatsApp, Payment, and Notification boundaries were promoted. Scenario participants were not turned into deployment nodes. | Passed |
| 6. Open-decision and no-invention audit | Node metadata, visible subtitles, forbidden-content QA | Map caller and DB physical placement remain unresolved. No cloud, VPS, OS, framework, proxy, container, cache, broker, HIS/EHR, SMS, or similar infrastructure was added. | Passed |
| 7. Lecturer notation audit | Actual lecturer deployment reference and final SVG/PNG | The final uses the reference's simple academic style: 3D deployment nodes, contained items, and plain solid communication paths. | Passed |
| 8. Geometry and readability audit | DEP-01 Q5 and diagrams.net structural lint | No node overlap, label clipping/collision, path through an unrelated node, page clipping, arrowhead, or machine-detectable crossing remains. Draw.io lint: 0 errors, 0 warnings, 0 crossings, 0 overlaps. | Passed |
| 9. Final actual-render inspection | Final SVG plus 8192×4757 PNG viewed in twelve ordered overlapping tiles | All nine nodes, contained labels, paths, PostgreSQL wording, and the visibly unresolved Map node were inspected. | Passed |

## Implemented quality gates

The DEP-01 artifact validator separates **structural correctness** from **geometry/readability**. Q4 confirms the diagram ID/title, exact selected inventory, node notation, contained items, endpoints, unique identifiers, registered source references, absence of forbidden UML/technology content, Map Service's zero paths, and no arrowheads. Q5 validates safe page bounds, non-overlap of nodes and labels, containment of deployed items, title clearance, endpoint attachment, and avoidance of unrelated nodes, labels, and crossings by communication paths.

| Gate / check | Final result |
|---|---|
| `validate-sources` | Passed |
| DEP-01 model validation | Passed |
| DEP-01 ViewSpec validation | Passed |
| DEP-01 traceability | 16/16 records covered |
| DEP-01 focused tests | 5 passed |
| Full regression suite | 29 passed |
| DEP-01 Q4 structural QA | Passed |
| DEP-01 Q5 geometry QA | Passed |
| CMP-01 QA after shared changes | Passed |
| Editable diagrams.net structural lint | 0 errors; 0 warnings; score 0 |

## Renderer, composition, and editable-source parity

The deterministic composition places the three approved client devices on the left, the Aafiatak Centralized Server in the centre, PostgreSQL below the server, and the four approved external-service nodes on the right. The direct SVG renderer and the diagrams.net exporter both read the same composition and visual-token source. The editable export pins edge endpoints to their respective node boundaries rather than node centres; this correction eliminated the first lint run's false route-through-contained-item warnings and produced a clean final lint result.

The only implementation-level defects found before acceptance were missing SVG title-bound metadata needed by Q5, and initially unpinned editable-edge endpoints. Both were corrected in canonical source code before final regeneration. **No generated SVG, PNG, or `.drawio` file was manually patched.**

## Actual visual inspection

The final SVG was opened directly. The final PNG was inspected at 8192×4757 pixels as twelve ordered overlapping tiles. The inspection confirmed that the client device labels and contained runtimes are readable; the central server contains exactly the three required software blocks; the PostgreSQL environment describes only logical deployment and its unresolved physical placement; the right-side provider nodes are legible; and Map Service visibly communicates its unresolved caller status without appearing accidentally omitted.

The presentation is intentionally light and academic: a white page, dark neutral outlines, serif page heading, sans-serif node content, no gradient, no shadow, no vendor icon, and no DevOps/cloud-infographic treatment. This is consistent with the lecturer's page-11 deployment notation rather than a production cloud-design diagram.

## Preserved unresolved decisions

| Decision | DEP-01 treatment |
|---|---|
| Map Service technical caller | Explicitly unresolved; Map Service has no communication path. |
| PostgreSQL physical co-location or separation from N04 | Explicitly unresolved; no physical-server claim is made. |
| Backend/web technology | Unspecified; no framework, web server, or proxy is shown. |
| Provider, operating system, cloud, container, and host topology | Unresolved; no vendor or deployment-infrastructure node is invented. |

Semantic status: verified

Structural QA: passed

Geometry QA: passed

Visual status: awaiting-user-approval
