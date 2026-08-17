# ADR 0004: Main Use Case Overview Scope

## Status

Accepted for the corrected Main Overview composition.

## Context

The canonical model contains 10 actors, 30 approved use cases, 44 actor associations, five `include` relations, and two `extend` relations. Rendering that complete operation inventory as one system-level picture produced an unreadable wiring diagram.

The higher-authority lecturer document separates three modeling levels on pages 6-8:

1. a Use Case Diagram identifying the system, actors, principal use cases, and relationships;
2. actor-oriented Package organization for detailed operations;
3. textual Use Case Modeling for steps, actors, preconditions, postconditions, and alternatives.

The product specification requires every operation but does not require every operation to be a first-overview ellipse. Its compact flow and role definitions support separating major actor goals from internal validation steps, conditional scenarios, and package-level operations.

`docs/use_case.md` is registered as an immutable source. It is therefore not edited. This decision records the evidence-based correction transparently while preserving its complete operation inventory in the canonical semantic model and its detailed package lists.

## Decision

The Main Overview renders 22 major goals/services. The canonical model retains all 30 use cases and all 51 relationships.

### Main Overview: category A

- MUC-01 Discover Medical Services
- MUC-02 View Facility Location
- MUC-03 Register Patient
- MUC-04 Log In
- MUC-05 Verify WhatsApp OTP
- MUC-06 Book Appointment
- MUC-09 Process Full Payment
- MUC-11 Subscribe to Availability Alert
- MUC-12 Manage Patient Appointments
- MUC-13 Track Visit & Queue
- MUC-14 Deliver Notifications
- MUC-15 Manage Facility Configuration
- MUC-16 Manage Schedules & Availability
- MUC-19 Manage Operational Exceptions
- MUC-20 Manage Facility Appointments
- MUC-21 Manage Capacity
- MUC-22 Manage Patient Arrival & Queue
- MUC-25 View Assigned Appointments & Queue
- MUC-26 Call Next Patient
- MUC-27 Manage Facility Onboarding
- MUC-28 Manage Platform Reference & Staff Data
- MUC-29 Handle Support & Escalations

### Actor Package Detail: category B

| Use Case | Preserved Detail |
|---|---|
| MUC-17 Manage Facility Staff Accounts | Facility Administrator package: add/disable staff, assign approved role, provision doctor access |
| MUC-18 Review Daily Operations | Facility Administrator and Reception package daily-operation views |
| MUC-23 Record Visit Outcomes | Reception package: start service, complete, non-complete, and no-show |
| MUC-30 Review Audit Logs | Platform Administrator package oversight operation |

### Use Case Modeling: category C

| Use Case | Preserved Under |
|---|---|
| MUC-07 Check Bookable Availability | MUC-06 mandatory validation and no-capacity alternative |
| MUC-08 Create Reservation Hold | MUC-06 successful-flow atomic hold step and expiry/release alternatives |
| MUC-10 Verify Payment Result | MUC-09 trusted gateway verification with Payment Gateway as secondary actor |
| MUC-24 Handle Late Arrival | MUC-22 conditional late-arrival alternatives and restrictions |

### Visible Main Overview Associations

- Visitor: MUC-01, MUC-02, MUC-03, MUC-04.
- Patient: MUC-04, MUC-06, MUC-09, MUC-11, MUC-12, MUC-13.
- Facility Administrator: MUC-15, MUC-16, MUC-19, MUC-21.
- Booking & Reception Staff: MUC-19, MUC-20, MUC-21, MUC-22, MUC-26.
- Doctor: MUC-25, MUC-26.
- Platform Administrator: MUC-27, MUC-28, MUC-29.
- Payment Gateway: MUC-09.
- Notification Service: MUC-14.
- Map Service: MUC-02.
- WhatsApp Authentication Provider: MUC-05.

Role-specific login, discovery, and notification associations omitted from the overview remain in the appropriate actor package. Payment Gateway participation in trusted result verification remains in MUC-09 modeling. No permission or operation is deleted.

### Visible Main Overview Dependencies

- MUC-03 `include` MUC-05: registration requires WhatsApp OTP verification.
- MUC-04 `include` MUC-05: login requires WhatsApp OTP verification.
- MUC-09 `extend` MUC-06 when `[Booking policy = FULL_PAYMENT_REQUIRED]`.

The former overview dependencies involving MUC-07, MUC-08, and MUC-10 are preserved as mandatory textual behavior. The availability-alert condition remains a MUC-11 precondition/alternative rather than a replacement chronological arrow.

## Consequences

- Main Overview: 10 actors, 22 use cases, 28 actor associations, two includes, and one extend.
- Canonical inventory: unchanged at 10 actors, 30 use cases, and 51 relationships.
- No package boxes appear in the Main Overview.
- Detailed package diagrams and Use Case Modeling remain required for complete traceability.
