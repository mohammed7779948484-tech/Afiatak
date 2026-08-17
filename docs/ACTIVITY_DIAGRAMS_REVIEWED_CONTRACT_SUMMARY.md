# Aafiatak Activity Diagram Suite — Reviewed Contract Summary

## Source set and reading status

The authoritative source set was extracted from `/home/ubuntu/upload/Aafiatak_Activity_Diagram_16_FINAL_VERIFIED_v2_MD_ONLY(1).zip` into `docs/activity-specs/`. The archive contains exactly 16 Markdown contracts, ordered `AD-01` through `AD-16`, with SHA-256 hashes captured during extraction. Every AD contract was read in full before implementation planning. The general implementation instruction is `/home/ubuntu/upload/Pasted_content_19.txt`; lines 1–1500 were read before this summary was created, and its remaining final section must be read before implementation.

## Non-negotiable common notation and workflow

Every diagram must be one coherent Use Case workflow, with English-only visible labels. Use a filled black Initial Node, rounded verb-led Action nodes, diamond Decision and Merge nodes, solid directed Control Flows, mandatory bracketed guards on outgoing Decision branches, and a bullseye Activity Final. Do not use actors, swimlanes, lifelines, Sequence message numbering, Use Case notation, Class/State notation, architecture components, database/API details, legends, or decorative Fork/Join bars. Each diagram must be implemented sequentially, rendered, visually inspected, audited against the MD, corrected, re-rendered, then locked with `awaiting-user-approval` status before proceeding.

## AD-specific execution contracts

| ID | Use Case | Required semantic highlights |
|---|---|---|
| AD-01 | Register Patient | Visitor context; normalized globally unique phone; WhatsApp-only OTP; branches for existing identity, channel unavailable, and invalid OTP; User + Patient only after OTP success; end-path merge; no SMS/password/clinical data. |
| AD-02 | Log In | Normalized verified phone; WhatsApp OTP only; unavailable/invalid OTP ends without session; post-OTP account/role/access revalidation; disabled/revoked contexts receive no usable privileged session; successful login creates revocable session. |
| AD-03 | Book Appointment | Conflict boundary; system finds earliest bookable ArrivalGroup; no capacity supports Notify Me only; atomic ACTIVE ReservationHold; policy split exactly PAY_AT_FACILITY vs FULL_PAYMENT_REQUIRED; target revalidation; atomic hold consumption + CONFIRMED Appointment; no manual approval/partial payment. |
| AD-04 | Process Full Payment | One permitted PaymentIntent per valid hold; browser return non-authoritative; trusted webhook/query result; failed/expired retry loop only with valid hold; SUCCEEDED financial truth revalidated for booking; safe equivalent recovery, full refund, or UNDER_REVIEW; no partials. |
| AD-05 | Subscribe to Availability Alert | Revalidate capacity; bookable capacity directs to normal booking with no hidden reservation; subscription gives no hold/priority/queue position; approved capacity-return event, system notification, normal booking competition; expiration on booking/session end; duplicate suppression loop. |
| AD-06 | Cancel Appointment | Patient owner eligibility; duplicate-cancellation boundary; saved snapshot refund consequence prior to confirmation; CANCELLED_BY_PATIENT; same-group capacity return only; PAY_AT_FACILITY/no refund versus saved full/zero refund policy; delayed refund does not reverse cancellation. |
| AD-07 | Publish Availability | Only DRAFT can publish; validate references, groups, capacity total, and terms; transition DRAFT to PUBLISHED; freeze terms; capacity upper bound non-increasing; idempotent retry; no capacity increase or reverse transition. |
| AD-08 | Withdraw Remaining Capacity | Approved one-way CapacityWithdrawal only; atomic remaining-capacity validation; positive quantity not above valid remaining; held/confirmed capacity protected; irreversible reduction; audit source/reason/actor/time; no restore/+1/re-import. |
| AD-09 | Reschedule Appointment | Staff-led after agreement; same ServiceOffering and saved terms; secure destination first; failed acquisition preserves original Appointment/capacity; scheduling changes while Appointment remains CONFIRMED; release old capacity only after success; no RESCHEDULED state. |
| AD-10 | Register Patient Check-in | Staff only; validate CONFIRMED intended appointment; late route delegated to AD-12; idempotent duplicate check-in; create/use VisitInstance CHECKED_IN; preserve original group; create/activate QueueEntry; normal ordering by actual check-in then confirmed_at; no payment priority. |
| AD-11 | Record No-show | Staff only; ArrivalGroup window must end; no valid check-in; no existing terminal outcome; terminal VisitInstance NO_SHOW; no reopening; saved full-or-zero policy; PAY_AT_FACILITY has no electronic refund. |
| AD-12 | Handle Late Arrival | Check terminal NO_SHOW first; no reopen; staff selects manual acceptance, reschedule, NO_SHOW, or NOT_COMPLETED; manual acceptance keeps original Appointment/group, uses manualHandling flag only, no automatic numeric position/priority/requeue/other-group capacity. |
| AD-13 | Manage Operational Exceptions | Create OPEN exception; SESSION_CANCELLED makes release non-bookable and releases active holds while preserving confirmed appointments; one-by-one affected appointment loop; approved resolution alternatives are equivalent option, facility cancellation/full refund, or escalation; closure only after documented outcome for every affected appointment. |
| AD-14 | Call Next Patient | Doctor views assigned waiting context; validates callable entry; stale selection refresh loop; successful call sets QueueEntry CALLED and calls patient; Doctor must not change VisitInstance states; no payment priority. |
| AD-15 | Review Facility Onboarding Request | Protected Platform Administrator review; information-sufficiency decision; insufficient path requests information and remains unresolved; sufficient assessment offers separate Approve or Reject Facility use cases; preserve review history; no FacilityApplicant portal/auto-provisioning. |
| AD-16 | Suspend Facility | Platform Administrator suspension; idempotent already-suspended branch; block new holds/bookings/publication; release active holds if applicable; preserve confirmed appointments and history; documented facility operational resolution remains separate; audit and no hard deletion. |

## Global cross-diagram invariants

Payment: FULL_PAYMENT_REQUIRED is full electronic payment; PAY_AT_FACILITY has no PaymentIntent; browser return is not financial truth; trusted verification governs; refunds are full collected amount or zero; no partials or ordinary-facility payment override.

Availability: the system—not the Patient—chooses the earliest bookable ArrivalGroup; capacity may not increase after publication; held/confirmed capacity cannot be withdrawn; CapacityWithdrawal is one-way; no internal-capacity re-import or automatic patient rebalancing.

Arrival/Queue: Patient cannot self-check-in; Appointment, VisitInstance, and QueueEntry stay independent; payment grants no priority; Doctor may call but cannot change VisitInstance states; manualHandling is a flag, not a state; terminal NO_SHOW cannot reopen.

Authentication: WhatsApp is for authentication/phone verification only; no SMS/password/Forgot Password; one normalized verified phone identifies one User; general operational notifications do not use WhatsApp.
