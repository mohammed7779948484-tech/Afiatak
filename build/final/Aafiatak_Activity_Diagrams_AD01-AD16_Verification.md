# Aafiatak Activity Diagrams AD-01–AD-16 — Verification Record

## Scope

This record covers the complete UML Activity Diagram suite for the **Aafiatak Medical Appointment Booking System**, from **AD-01 Register Patient** through **AD-16 Suspend Facility**.

| Check | Result |
|---|---:|
| Activity diagrams in suite | 16 |
| Cross-suite structural and delivery audit | Pass: 16 / 16 |
| Required visual-review state | `awaiting-user-approval` for every diagram |
| Merged PDF pages | 16 |
| Raster images embedded in merged PDF | None (`pdfimages -list` has an empty image table) |

## Cross-Suite Controls

The audit verifies the declared node and control-flow counts against each semantic model; equality of model/View inclusion sets; lecturer-style Activity notation; the absence of fork, join, object-flow, association, generalization, and aggregation notation; the availability of SVG, PNG, editable `.drawio`, PDF, QA, and semantic-audit artifacts; and a non-placeholder preview hash matching the current preview.

All 16 Activity Diagrams passed these checks. The suite remains **awaiting user approval**; the recorded review hashes identify the inspected preview artifacts and do not constitute user approval.

## Merged PDF

`Aafiatak_Activity_Diagrams_AD01-AD16.pdf` preserves the original vector pages in the required sequence AD-01 to AD-16. `pdfinfo` reports exactly 16 pages. The `pdfimages -list` output contains only the header and separator rows, confirming that no raster images were embedded. A visual spot check of page 1 confirmed the AD-01 opening page is present and legible; a visual spot check of page 13 confirmed the large AD-13 operational-exceptions composition is present, non-blank, and retained in the merged file; and a visual spot check of page 16 confirmed that AD-16 Suspend Facility is the final page in the required sequence.

## Key Visual Findings for Recently Completed Diagrams

| Diagram | Visual finding |
|---|---|
| AD-14 Call Next Patient | The normal call path is vertically dominant; both the no-call and stale QueueEntry paths are visible and resolve safely without changing VisitInstance state. |
| AD-15 Review Facility Onboarding Request | The insufficient-information path records the request and keeps onboarding unresolved; approval and rejection are explicitly represented as subsequent separate use cases. |
| AD-16 Suspend Facility | Already-suspended idempotency, active-hold release, preservation of confirmed appointments, documented resolution, audit trail, and platform-boundary steps are distinct and readable. |

## Status

**Final status: `awaiting-user-approval`.**

## Arrowhead Endpoint Correction

The Activity SVG renderer was corrected after a magnified visual review of all 19 AD-16 control-flow endpoints. The prior marker was stroke-width-scaled and visually oversized at node borders. The corrected marker uses a fixed user-space viewBox, a smaller 48×42 geometry, and `refX=16`, which anchors the arrow tip exactly to each authored terminal path coordinate. All 16 Activity Diagrams were regenerated, their preview hashes refreshed, and their semantic and cross-suite audits passed again (16/16). The AD-16 final vector PDF was opened after re-export and visually confirms the corrected arrowhead treatment in the deliverable.
