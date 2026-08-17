# Aafiatak Sequence Diagram Suite — Visual and Semantic Audit Summary

The six sequence diagrams were reworked into one consistent lecturer-style family. Across SD-01 through SD-06, the rendered outputs use the same white background, dark navy/charcoal linework, vertical lifelines, compact activation bars, solid request arrows, dashed return arrows, and chronological numbered labels.

The corrected SD-01 now shows only the numbered main success flow from 1 to 19. All previously visible combined fragments, visible retry/failure notes, and participant stereotypes were removed from both the main SVG rendering path and the editable diagrams.net source.

SD-02 presents the `FULL_PAYMENT_REQUIRED` booking scenario only, with trusted gateway verification occurring after browser return and before confirmed Appointment creation. SD-03 presents the successful eligible cancellation and full refund scenario only. SD-04 preserves the same-service, same-terms rescheduling invariant and keeps the Appointment in `CONFIRMED` state. SD-05 preserves queue-order semantics so the checked-in Patient is not implied to be automatically next, and the Doctor call changes `QueueEntry` only. SD-06 presents the representative `CONFLICT_DETECTED` operational-exception scenario with facility-side cancellation, full refund where payment exists, notification, and verified closure, without introducing Platform Administrator.

Cross-diagram review confirmed that shared participant names remain stable wherever reused, especially `Aafiatak Backend`, `Aafiatak Data Store`, `Payment Gateway`, and `Notification Service`. The visible notation is consistent across the full suite, no combined fragments remain anywhere, every main flow is sequentially numbered from 1 without skips inside its own diagram, and all final PDFs remain A3 landscape vector outputs without embedded raster images.

Final suite status remains `awaiting-user-approval`.
