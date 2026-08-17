# Design System

`design/palette.yaml`, `typography.yaml`, `geometry.yaml`, and `routing.yaml` are canonical visual tokens. Per-type files under `design/profiles/` constrain orientation and notation emphasis.

`DesignSystem` compiles tokens into mxGraph style properties. Renderer code chooses semantic roles and structural shapes but does not carry arbitrary colors or font sizes. The baseline is restrained, high-contrast, print-friendly, and mostly grayscale-legible: no default gradients, shadows, remote fonts, or decorative effects.

The layer convention is `01 Background`, `02 Containers`, `03 Nodes`, `04 Relationships`, `05 Labels`, `06 Notes`, and `99 QA Guides`. QA guides are omitted from approved output unless explicitly needed and hidden.

CSS is reserved for future HTML QA reports. Native draw.io shapes are styled through mxGraph properties, not browser CSS.
