# CD-03 QA Record — Cancel Appointment — Full Refund Required

| Gate | Verification | Result | Evidence |
|---:|---|---|---|
| 1 | Binding specification reread | Passed | CD-03 verified Markdown contract. |
| 2 | Participants | Passed | 6/6; source-match audit. |
| 3 | Structural links | Passed | 5/5 L01–L05; source-match audit. |
| 4 | Messages | Passed | 18/18; `Q4` passed. |
| 5 | Numbering | Passed | Global 1–18 sequence. |
| 6 | Directions | Passed | Source and target audited per message. |
| 7 | Exact labels | Passed | Message-by-message source-match audit. |
| 8 | Self-message | Passed | Message 5 loop on Aafiatak Backend. |
| 9 | Communication-only notation | Passed | No lifelines, activations, or fragments. |
| 10 | Lecturer visual language | Passed | Rectangles, reusable links, directional numbered messages. |
| 11 | Outputs | Passed | SVG, 8192×5325 PNG, `.drawio`, A0 vector PDF. |
| 12 | Actual output opening | Passed | PNG tiles, SVG, and PDF opened. |
| 13 | Routing | Passed | Dedicated label corridors and participant-boundary connections. |
| 14 | Correction check | Passed | No routing defect requiring a semantic change was found. |
| 15 | Re-render | Passed | Preview hash `b8b5e4e5c6cf02669b9edb8925c3d17a1808ceae8f6ec88d41a0e227d47d8ef8`. |
| 16 | Final source match | Passed | `Aafiatak_CD03_Cancel_Appointment_Full_Refund_source_match.json`. |

The A0 PDF has no embedded raster image objects. Visual status remains **`awaiting-user-approval`**; QA does not self-approve the deliverable.
