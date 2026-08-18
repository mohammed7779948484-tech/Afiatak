# CD-05 QA Record — Patient Check-in, Queue & Call Next Patient

| Gate | Verification | Result | Evidence |
|---:|---|---|---|
| 1 | Binding contract reread | Passed | CD-05 verified specification. |
| 2–3 | Participants and reusable links | Passed | 8 participants; 8 links; source-match audit. |
| 4–7 | Message count, numbering, direction, labels | Passed | Exact 30-message source match. |
| 8 | Self-message | Passed | Message 6 loop on Aafiatak Backend. |
| 9–10 | Communication-only notation and lecturer style | Passed | No lifelines/fragments; object boxes and directional messages only. |
| 11–12 | Outputs and visual inspection | Passed | SVG, 8192×5325 PNG, `.drawio`, A0 vector PDF; all 28 tiles, SVG, and PDF opened. |
| 13–15 | Routing, correction, re-render | Passed | Dedicated link-label corridors and final preview hash `7c0a2f1cb67164d41fe97ef6e82ea1d4ecb22a0006990b3e6c0f9db06646ef5a`. |
| 16 | Final source match | Passed | `Aafiatak_CD05_CheckIn_Queue_CallNext_source_match.json`. |

The A0 PDF has no embedded raster-image objects. Visual-review status remains **`awaiting-user-approval`**.
