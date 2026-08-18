# Aafiatak Collaboration / Communication Diagrams — CD-01 to CD-06

## Delivery Contents

This release contains the six final academic UML Collaboration/Communication Diagrams for the Aafiatak Medical Appointment Booking System. Each individual diagram is supplied as an editable `.drawio` source, vector SVG, 8192×5325 PNG preview, and one-page A0 landscape vector PDF. The package also includes one merged six-page A0 vector PDF and complete QA evidence.

| Diagram | Scenario | Participants | Links | Messages | Self-messages |
|---|---|---:|---:|---:|---:|
| CD-01 | Patient Registration & WhatsApp OTP Verification | 5 | 5 | 19 | 2 |
| CD-02 | Book Appointment — FULL_PAYMENT_REQUIRED Success | 6 | 7 | 34 | 0 |
| CD-03 | Cancel Appointment — Full Refund Required | 6 | 5 | 18 | 1 |
| CD-04 | Reschedule Appointment | 6 | 5 | 18 | 0 |
| CD-05 | Patient Check-in, Queue & Call Next Patient | 8 | 8 | 30 | 1 |
| CD-06 | Resolve Operational Exception — Facility Cancellation & Full-Refund Initiation | 7 | 6 | 25 | 0 |

## Review Status

All six diagrams have passed source-match, structural QA, rendering checks, high-resolution visual inspection, and vector-PDF verification. Their declared status is **`awaiting-user-approval`**; automated checks do not replace your final visual approval.

## Quality Guarantees

Every diagram uses the lecturer-required Collaboration/Communication visual language: plain participant rectangles, one reusable structural link for each communicating pair, globally numbered directional messages, and small self-message loops only where the binding specification requires them. The diagrams deliberately contain no lifelines, activation bars, sequence fragments, use-case notation, state notation, or invented participants/messages.

All individual PDFs and the merged PDF use A0 landscape pages (3370.39×2383.94 pt). `pdfimages -list` reported **zero embedded raster-image objects**, so the diagram linework and text remain vector content.

## Directory Guide

| Directory | Contents |
|---|---|
| `final/` | The ready-to-submit SVG, PNG, `.drawio`, individual PDF, and merged six-page PDF files. |
| `qa/` | Per-diagram QA records, source-match JSON results, visual-inspection notes, and the cross-suite audit. |
| `source/` | Semantic models, Views, layout composition, SVG renderer, diagrams.net exporter, and the supporting export/audit scripts required to reproduce the delivery. |

Open any `.drawio` file in [diagrams.net](https://app.diagrams.net/) or draw.io Desktop to edit the source. The vector SVG and PDF files are appropriate for high-resolution report insertion and printing.
