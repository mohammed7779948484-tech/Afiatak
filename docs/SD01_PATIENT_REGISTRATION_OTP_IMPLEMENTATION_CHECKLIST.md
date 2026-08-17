# SD-01 — Patient Registration & WhatsApp OTP Verification

## Authoritative execution checklist

This checklist is derived directly from `Aafiatak_SD01_Patient_Registration_OTP_FINAL_REVIEWED.md` and `Pasted_content_16.txt`. The primary actor is **Visitor**, not Patient. The sequence is confined to the current approved MVP and all visible labels must be English.

| Control area | Required implementation contract |
|---|---|
| Diagram title | `Sequence Diagram — Patient Registration & WhatsApp OTP Verification` |
| Primary actor | `Visitor` |
| Exact lifelines, left to right | Visitor; Patient Application; Aafiatak Backend; Aafiatak Data Store; WhatsApp Authentication Provider |
| Lifeline count | Exactly 5 |
| Main success flow | Exactly 19 chronological messages, top to bottom |
| Request/action notation | Solid horizontal arrows |
| Direct response notation | Dashed horizontal arrows |
| Self-messages | Backend phone normalization/validation; Backend OTP expiry/single-use/security validation |
| Activations | Meaningful short application, backend, data-store, and provider activation bars |
| Alternatives | A1 existing identity; A2 invalid/expired/reused OTP; A3 rate limit; A4 provider unavailable |
| Required UML note | Retries under weak connectivity must not create duplicate User or Patient records |
| Lifecycle rule | Create `User + Patient` atomically only after OTP verification and approved basic profile submission |
| Final review status | `awaiting-user-approval` |

## Mandatory main success messages

| # | Sender | Receiver | Exact visible label | Notation |
|---:|---|---|---|---|
| 1 | Visitor | Patient Application | Enter phone number and choose Register | Solid |
| 2 | Patient Application | Aafiatak Backend | Start patient registration(phone) | Solid |
| 3 | Aafiatak Backend | Aafiatak Backend | Normalize and validate phone number | Solid self-message |
| 4 | Aafiatak Backend | Aafiatak Data Store | Check phone identity uniqueness | Solid |
| 5 | Aafiatak Data Store | Aafiatak Backend | Identity lookup result: available | Dashed |
| 6 | Aafiatak Backend | WhatsApp Authentication Provider | Request short-lived single-use OTP delivery | Solid |
| 7 | WhatsApp Authentication Provider | Aafiatak Backend | OTP delivery request accepted | Dashed |
| 8 | Aafiatak Backend | Patient Application | Verification required | Dashed |
| 9 | WhatsApp Authentication Provider | Visitor | Deliver OTP via official WhatsApp channel | Solid external event |
| 10 | Visitor | Patient Application | Submit OTP | Solid |
| 11 | Patient Application | Aafiatak Backend | Verify OTP attempt | Solid |
| 12 | Aafiatak Backend | Aafiatak Backend | Validate expiry, single-use and security limits | Solid self-message |
| 13 | Aafiatak Backend | Patient Application | OTP verified; request basic Patient profile | Dashed |
| 14 | Visitor | Patient Application | Submit approved basic profile data | Solid |
| 15 | Patient Application | Aafiatak Backend | Create verified Patient account/profile | Solid |
| 16 | Aafiatak Backend | Aafiatak Data Store | Atomically create User + Patient for verified phone | Solid |
| 17 | Aafiatak Data Store | Aafiatak Backend | Account/profile created exactly once | Dashed |
| 18 | Aafiatak Backend | Patient Application | Registration confirmed | Dashed |
| 19 | Patient Application | Visitor | Display Patient registration success | Dashed |

## Explicit exclusion controls

The diagram must not contain SMS, password authentication or reset, Patient Service, Patient Repository, API Gateway, OTP Validator, services/microservices, any clinical information, Payment Gateway, Appointment, ReservationHold, PaymentIntent, Facility, Doctor, Notification Service, or privileged-role provisioning.

No OTP value, secret, token, password, API key, exact OTP duration, or anti-abuse implementation algorithm may be exposed.

## Required final QA

Semantic QA confirms all five exact lifelines, 19 exact main messages with correct senders/receivers and arrow styles, four critical `alt` fragments, Visitor as the primary actor, no invented implementation architecture, and atomic User + Patient creation only after OTP verification. Visual QA checks participant order, message chronology, dashed responses, solid requests, activation alignment, notes, no collisions, no clipped labels, landscape readability, and the required final visual status.
