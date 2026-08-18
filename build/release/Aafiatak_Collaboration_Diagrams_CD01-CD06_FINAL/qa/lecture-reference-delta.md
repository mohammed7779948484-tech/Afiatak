# Collaboration Diagram — Reference Delta Audit

## What the lecture reference actually shows

The reference is a compact, hand-drawn academic Collaboration Diagram. It uses a plain white background with no document title and no outer page frame. Participants are simple unfilled rectangular object boxes. Their names are underlined, and self-messages are simple loops immediately above the relevant object box. A single thin communication line connects each pair of participants. Individual message arrows sit directly on that line, while unboxed message text is placed freely beside the line in grouped directional runs. The visual language is deliberately sparse: no panels, grids, label borders, lifelines, activation bars, card-like containers, or dashboard-style spacing.

## Why the current delivery does not match it

The current renderer introduced a centred document title, large outer page border, uniformly sized participant boxes without underlined names, opaque bordered message panels, and broad systematic label corridors. These decisions may be internally readable but are visually incompatible with the lecturer’s compact reference. The current diagrams look like a generated report/network layout rather than the worked Collaboration Diagram example.

## Binding correction rules

1. Remove the title band and external page border from every Collaboration Diagram.
2. Use simple object rectangles only; underline each participant name.
3. Retain one thin structural link per communicating pair, but place arrows and unboxed message labels directly beside each link.
4. Remove all message-label backgrounds, borders, and stacked-card styling.
5. Render self-messages as a small loop above the participant box, with its unboxed label adjacent to the loop.
6. Replace the wide central network template with compact, reference-like four-to-eight-object layouts in which the interaction graph occupies the main page area.
7. Preserve the exact participants, reusable links, message numbers, senders, receivers, labels, and specified self-message sequences; only the visual presentation changes.

## Status

The previous output is rejected for visual non-conformance and must be regenerated before user approval.

## First corrected-render check

The corrected CD-01 SVG was produced successfully after removing title/page-border/message-card primitives. Direct browser viewing begins on a large blank canvas and is not a reliable full-diagram comparison method for this 16,000×10,400 coordinate space. A scaled vector/PDF preview is required for the next visual decision rather than relying on this browser viewport.

## First corrected-render assessment

The first corrected render successfully removed the page frame, title band, and message cards, and moved the self-loop above the object. It is materially closer to the lecture reference. However, the message typography remains too small on an A0 page and the graph occupies too little of the canvas. Before broader regeneration, the message and object typography must be enlarged and the composition must be tightened to produce the compact textbook-like reading scale shown by the reference.

## Approved internal style direction for regeneration

The enlarged CD-01 trial now satisfies the lecture-reference visual language at the family level: unframed white canvas, simple underlined object rectangles, thin grey links, individual directional arrows, free message text, and a loop above the Backend. The remaining layout difference is scenario topology, which must differ because the participants and required messages differ. This renderer direction will be applied to CD-01 through CD-06; it replaces the rejected report/card aesthetic.

## Six-diagram corrected-family check

The refreshed contact sheet was generated from the newly rendered vector PDFs rather than stale PNG previews. It confirms that all six diagrams now share the corrected visual vocabulary: no title bands, no outer frames, no message cards, simple outlined rectangles, thin reusable links, free message text, and only the required self-loops. CD-02 and CD-05 remain the densest diagrams and require individual full-page inspection before their corrected files can replace the final delivery.

## Dense-diagram inspection — CD-02

CD-02, the densest 34-message scenario, was opened from its corrected vector PDF. The long Backend–Data Store interaction is rendered as one reusable vertical link with small directional arrows and an unboxed text group beside it. The other message groups occupy separate surrounding whitespace; no grey cards, title band, external frame, lifelines, or added notation remain. The grouping is the closest valid equivalent to the lecturer example while preserving all 34 binding labels.

## Dense-topology inspection — CD-05

The corrected CD-05 vector PDF was opened independently. Its eight objects remain distinct, the Backend self-loop is above the object as in the reference, and all message groups are free text beside their reusable links. The visual language is now consistent with the lecturer’s Collaboration Diagram rather than the rejected report/card presentation. No label panel, title, frame, lifeline, activation bar, or sequence fragment was observed.

## Final individual check — CD-06

The corrected CD-06 vector PDF was opened. Its seven participant rectangles, six thin reusable links, and 25 free message labels follow the corrected reference style. The largest message group (Backend–Data Store) is unboxed and placed beside the shared link, while the facility, payment, notification, and patient communications are visually separated. This completes the representative individual visual checks of the corrected family.
