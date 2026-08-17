# Aafiatak — Use Case Modeling & Diagram Execution Specification

## 0. Purpose

This file is the approved modeling brief for the **Aafiatak Use Case work**.

It defines three separate deliverable layers, following the lecturer's method and the approved Aafiatak project scope:

1. **Main Use Case Diagram — System Overview** — build this first.
2. **Actor Package Use Case Diagrams** — build these later as separate diagrams to expose detailed operations without overcrowding the main overview.
3. **Use Case Modeling documents** — build these after the diagrams for the important use cases, with scenarios, actors, preconditions, postconditions, and steps.

This document is about **modeling and drawing the system**, not implementing the software.

The implementation agent must not re-extract or redesign Aafiatak requirements. The required content has already been selected here from the authoritative project specification and the lecturer's UML rules.

---

# 1. Authority and Conflict Rules

Use the following precedence whenever anything appears ambiguous:

1. **Aafiatak authoritative project specification at repository root** — product scope, actors, permissions, business rules, current-scope functionality, exclusions.
2. **Lecturer UML PDF at repository root** — academic UML method and notation required for the course.
3. **This file** — approved selection, classification, relationships, and execution plan for the Use Case work.
4. **Repository-local diagrams.net skill and diagram-engineering system** — drawing, layout, rendering, validation, and export mechanics.

If this file contains a genuine contradiction with the authoritative Aafiatak specification, the project specification wins for product truth.

Do not invent a product rule from general UML knowledge.

Do not use any previous Aafiatak Use Case image or old diagram as a source or visual reference.

---

# 2. Lecturer Method Applied to Aafiatak

The lecturer's Use Case method separates the work into distinct stages:

## Stage A — Use Case Diagram

The diagram identifies:

- the **System Boundary**;
- the **Actors**;
- the **Use Cases**;
- the valid **Relationships**.

The Use Case Diagram shows system services and actor interaction. It does **not** show execution chronology.

## Stage B — Packages for a large system

Because Aafiatak contains many operations, detailed actor operations must not all be forced into the first overview image.

After the main Use Case Diagram, create **separate actor-oriented Package Use Case Diagrams** so that each actor's detailed operations can be shown clearly without producing a tangled overview.

These package diagrams are detailed views for Use Case organization. They do not replace the later formal Package Diagram deliverable.

## Stage C — Use Case Modeling

After the diagrams, important use cases are documented textually with:

- Use Case Name;
- Use Case ID;
- Brief Description;
- Primary Actor;
- Secondary Actor(s), when applicable;
- Preconditions;
- Main Success Scenario / Steps;
- Alternative / Failure Scenarios;
- Postconditions.

Do not place these textual details inside the main Use Case Diagram.

---

# 3. Mandatory UML Rules

These rules apply to every Use Case diagram produced from this file.

## 3.1 System Boundary

- Draw one clear **System Boundary** for the main overview.
- Boundary title:

  **Aafiatak Medical Appointment Booking System**

- Every Actor must be **outside** the System Boundary.
- Every Use Case must be **inside** the System Boundary.
- No Actor may overlap or sit on the boundary line.

## 3.2 Use Case naming

- All visible labels are **English**.
- Every Use Case name begins with a **verb**.
- Use the exact names approved in this file.
- Do not silently rename or paraphrase a Use Case while drawing it.
- IDs such as `MUC-01` are traceability metadata; do not place them inside visible ellipses unless the course profile explicitly requires IDs.

## 3.3 Actor association

- Actor–Use Case Association is a plain **solid line**.
- Do not add an arrowhead to a normal Actor–Use Case Association.
- Connect an Actor only to a Use Case in which that Actor directly participates.
- Do not connect an Actor to an internal/helper Use Case simply because the actor benefits indirectly from it.

## 3.4 `<<include>>`

Use a dashed dependency arrow labeled:

`<<include>>`

Direction:

**Base Use Case → mandatory included Use Case**

Only use `include` when the included behavior is mandatory for every execution of the base use case in the modeled context.

## 3.5 `<<extend>>`

Use a dashed dependency arrow labeled:

`<<extend>>`

Direction:

**Conditional extending Use Case → base Use Case**

Use `extend` only for optional/conditional behavior with a defined condition.

## 3.6 Generalization

Do **not** introduce Actor Generalization in the first Aafiatak Use Case work.

In particular:

- Do not make `Patient` a specialization of `Visitor`.
- Do not invent `User`, `Authenticated User`, or `Facility User` actors only to reduce lines.

## 3.7 No chronological arrows

Do not draw arrows to mean:

- then;
- next;
- before;
- after;
- first/second/third.

Execution order belongs to Activity and Sequence diagrams later.

## 3.8 Forbidden implementation elements

Do not place any of the following in a Use Case Diagram:

- Classes;
- Attributes;
- database tables;
- PostgreSQL;
- components;
- APIs as internal implementation boxes;
- screens/pages;
- UI controls;
- implementation objects.

---

# 4. Explicitly Forbidden Actors and Features

## 4.1 Forbidden Actors

Do not create:

- Database;
- PostgreSQL;
- Internal Hospital System / HIS;
- EHR;
- FacilityApplicant;
- Cashier;
- Pharmacy System;
- Laboratory System;
- SMS Provider;
- generic `User`;
- generic `Authenticated User`.

The facility's internal scheduling system is not technically integrated with Aafiatak in the current scope and therefore is not an Actor in these diagrams.

## 4.2 Forbidden / out-of-scope Use Cases

Do not create:

- Forgot Password;
- Reset Password;
- Approve Booking;
- Reject Booking;
- Confirm Booking Manually;
- Pay Deposit;
- Make Partial Payment;
- Increase Published Capacity;
- Restore Withdrawn Capacity;
- Add `+1` Capacity;
- Self Check-in;
- Select Any Arrival Group;
- Auto Requeue Patient;
- Auto Transfer Late Patient;
- Create Phone Booking;
- Create Walk-in Booking;
- Manage Medical Records;
- Record Diagnosis;
- Manage Prescriptions;
- Manage Laboratory Results;
- Manage Insurance;
- Manage Cashier;
- Manage Full Medical Invoices;
- Auto Apply;
- any feature listed as Deferred / Out of Current Scope in the authoritative specification.

Authentication is passwordless WhatsApp OTP, therefore there is no password-recovery workflow.

There is no manual facility approval of valid booking requests.

The patient does not choose the booking policy.

The patient does not choose an arbitrary Arrival Group; Aafiatak allocates the earliest currently bookable group according to the approved rules.

---

# 5. Approved Actors

Use exactly these Actors across the Use Case work.

## Human Actors

### A1 — Visitor
Unauthenticated public user.

### A2 — Patient
Registered patient role using Aafiatak for discovery, booking, payment when required, appointment follow-up, notifications, and queue visibility.

### A3 — Facility Administrator
Highest-privilege user inside the participating facility account.

### A4 — Booking & Reception Staff
Facility operational staff responsible for daily Aafiatak appointments, capacity, patient arrival, queue, visit progress, and operational exceptions within approved permissions.

### A5 — Doctor
Limited operational role. The Doctor views the doctor's own Aafiatak work/waiting patients and may call the next patient, but does not change visit lifecycle states and does not report delay/absence inside the system.

### A6 — Platform Administrator
Aafiatak platform administration role.

## External Service Actors

### A7 — Payment Gateway
External provider used for full online payment verification and refund processing.

### A8 — Notification Service
External service used for approved application/system notification delivery.

### A9 — Map Service
External map/location service.

### A10 — WhatsApp Authentication Provider
Official provider/API used only for WhatsApp OTP authentication and phone verification.

---

# 6. Deliverable 1 — Main Use Case Diagram (BUILD THIS NOW)

## 6.1 Purpose of the main diagram

The first diagram is a **system-level overview**.

It must answer:

- Who interacts with Aafiatak?
- What are the major goals/services exposed by Aafiatak?
- What are the few essential `include` / `extend` relationships needed to understand the system?

It must **not** attempt to display every detailed operation from the project specification.

The remaining detailed operations are preserved in Section 10 for separate Package Use Case Diagrams.

## 6.2 No Package boxes inside the main overview

Do **not** draw UML Package containers inside the first main Use Case Diagram.

Reason:

- the lecturer treats Use Case Diagram and Package organization as separate modeling steps;
- the system is large, so detailed operations will be moved to separate actor-oriented package diagrams;
- this keeps the system overview readable and prevents 50+ ellipses and excessive connector crossings.

You may use spacing/alignment zones for visual organization, but do not draw them as UML Package notation in this first overview.

---

# 7. Main Overview — Approved Use Cases

The following is the complete **render-now** set for the first main diagram.

Do not add detailed operations from Section 10 to this first diagram.

## Public Access & Patient Goals

### MUC-01 — Discover Medical Services
Actors:
- Visitor
- Patient

Represents public discovery of facility/service information, doctors, departments/specialties, service information, and preliminary Aafiatak availability at overview level.

### MUC-02 — View Facility Location
Actors:
- Visitor
- Patient
- Map Service

### MUC-03 — Register Patient
Actor:
- Visitor

### MUC-04 — Log In
Actors:
- Visitor
- Patient
- Facility Administrator
- Booking & Reception Staff
- Doctor
- Platform Administrator

### MUC-05 — Verify WhatsApp OTP
External Actor:
- WhatsApp Authentication Provider

Helper Use Case used by registration and authentication.

### MUC-06 — Book Appointment
Actor:
- Patient

Represents the approved booking goal under the service's configured `FULL_PAYMENT_REQUIRED` or `PAY_AT_FACILITY` policy.

### MUC-07 — Check Bookable Availability
Helper Use Case.

Represents mandatory validation that suitable digital capacity is currently bookable.

### MUC-08 — Create Reservation Hold
Helper Use Case.

Represents mandatory temporary atomic seat protection during a booking attempt.

### MUC-09 — Process Full Payment
Actors:
- Patient
- Payment Gateway

Occurs only when the ServiceOffering uses `FULL_PAYMENT_REQUIRED`.

### MUC-10 — Verify Payment Result
External Actor:
- Payment Gateway

Helper Use Case for trusted gateway verification.

### MUC-11 — Subscribe to Availability Alert
Actor:
- Patient

Used when no currently bookable capacity exists. It grants no reservation and no priority.

### MUC-12 — Manage Patient Appointments
Actor:
- Patient

Overview goal that includes patient-facing viewing/cancellation/reconfirmation details. Those details are shown later in the Patient Package Diagram.

### MUC-13 — Track Visit & Queue
Actor:
- Patient

Overview goal for the patient's own check-in/visit visibility and approximate queue position after facility check-in.

### MUC-14 — Deliver Notifications
Actors:
- Patient
- Facility Administrator
- Booking & Reception Staff
- Notification Service

High-level notification delivery goal. Detailed notification types are moved to actor/package details.

---

## Facility Administrator Goals

### MUC-15 — Manage Facility Configuration
Actor:
- Facility Administrator

Overview goal covering facility/branch data, departments/specialties, doctors, service offerings, prices/instructions, and booking-related policy configuration.

### MUC-16 — Manage Schedules & Availability
Actor:
- Facility Administrator

Overview goal covering doctor schedules, planned exceptions, AvailabilityRelease setup, Arrival Groups, initial digital capacity, publication, and authorized availability management.

### MUC-17 — Manage Facility Staff Accounts
Actor:
- Facility Administrator

### MUC-18 — Review Daily Operations
Actors:
- Facility Administrator
- Booking & Reception Staff

Represents the daily operational oversight supported by the Today Pulse Board without naming the UI screen as a use case.

### MUC-19 — Manage Operational Exceptions
Actors:
- Facility Administrator
- Booking & Reception Staff

Covers approved operational exceptions and their documented resolution at overview level.

---

## Booking & Reception Staff Goals

### MUC-20 — Manage Facility Appointments
Actor:
- Booking & Reception Staff

Overview goal covering appointment search, authorized cancellation, rescheduling after agreement, and appointment operational review.

### MUC-21 — Manage Capacity
Actors:
- Facility Administrator
- Booking & Reception Staff

Overview goal covering only allowed actions: view capacity, one-way withdrawal of remaining capacity, freeze, and close.

It never includes increasing published capacity or restoring withdrawn capacity.

### MUC-22 — Manage Patient Arrival & Queue
Actor:
- Booking & Reception Staff

Overview goal covering check-in, queue activation/management, waiting order, and correction of erroneous arrival/queue registration.

### MUC-23 — Record Visit Outcomes
Actor:
- Booking & Reception Staff

Overview goal covering service start, completion, non-completion, and no-show recording.

### MUC-24 — Handle Late Arrival
Actor:
- Booking & Reception Staff

No automatic group transfer or automatic re-entry is implied.

---

## Doctor Goals

### MUC-25 — View Assigned Appointments & Queue
Actor:
- Doctor

Covers the doctor's own appointments, arrival groups/windows, checked-in/waiting patients, and identification of the next patient.

### MUC-26 — Call Next Patient
Actors:
- Doctor
- Booking & Reception Staff

The Doctor does not change VisitInstance lifecycle states through this use case.

---

## Platform Administrator Goals

### MUC-27 — Manage Facility Onboarding
Actor:
- Platform Administrator

Covers review/request-more-information/approve/reject/activate/suspend at overview level.

There is no FacilityApplicant Actor in the current scope.

### MUC-28 — Manage Platform Reference & Staff Data
Actor:
- Platform Administrator

Overview goal covering public reference lists and controlled Aafiatak platform-staff management.

### MUC-29 — Handle Support & Escalations
Actor:
- Platform Administrator

Covers documented technical support and escalated technical/payment/conflict cases without taking over facility daily operations.

### MUC-30 — Review Audit Logs
Actor:
- Platform Administrator

---

# 8. Main Overview — Actor Association Matrix

This matrix is authoritative for the first main diagram.

Do not add Actor associations not listed here.

| Actor | Direct Main Use Cases |
|---|---|
| Visitor | MUC-01 Discover Medical Services; MUC-02 View Facility Location; MUC-03 Register Patient; MUC-04 Log In |
| Patient | MUC-01 Discover Medical Services; MUC-02 View Facility Location; MUC-04 Log In; MUC-06 Book Appointment; MUC-09 Process Full Payment; MUC-11 Subscribe to Availability Alert; MUC-12 Manage Patient Appointments; MUC-13 Track Visit & Queue; MUC-14 Deliver Notifications |
| Facility Administrator | MUC-04 Log In; MUC-14 Deliver Notifications; MUC-15 Manage Facility Configuration; MUC-16 Manage Schedules & Availability; MUC-17 Manage Facility Staff Accounts; MUC-18 Review Daily Operations; MUC-19 Manage Operational Exceptions; MUC-21 Manage Capacity |
| Booking & Reception Staff | MUC-04 Log In; MUC-14 Deliver Notifications; MUC-18 Review Daily Operations; MUC-19 Manage Operational Exceptions; MUC-20 Manage Facility Appointments; MUC-21 Manage Capacity; MUC-22 Manage Patient Arrival & Queue; MUC-23 Record Visit Outcomes; MUC-24 Handle Late Arrival; MUC-26 Call Next Patient |
| Doctor | MUC-04 Log In; MUC-25 View Assigned Appointments & Queue; MUC-26 Call Next Patient |
| Platform Administrator | MUC-04 Log In; MUC-27 Manage Facility Onboarding; MUC-28 Manage Platform Reference & Staff Data; MUC-29 Handle Support & Escalations; MUC-30 Review Audit Logs |
| Payment Gateway | MUC-09 Process Full Payment; MUC-10 Verify Payment Result |
| Notification Service | MUC-14 Deliver Notifications |
| Map Service | MUC-02 View Facility Location |
| WhatsApp Authentication Provider | MUC-05 Verify WhatsApp OTP |

---

# 9. Main Overview — Approved Relationships

Use only the relationships in this section in the first main diagram.

## `<<include>>`

### INC-01
**Register Patient** `<<include>>` **Verify WhatsApp OTP**

Direction:

MUC-03 → MUC-05

Reason:
Phone verification is mandatory for patient self-registration.

### INC-02
**Log In** `<<include>>` **Verify WhatsApp OTP**

Direction:

MUC-04 → MUC-05

Reason:
Human-account authentication is passwordless and requires valid WhatsApp OTP verification.

### INC-03
**Book Appointment** `<<include>>` **Check Bookable Availability**

Direction:

MUC-06 → MUC-07

Reason:
Every booking attempt requires currently valid bookable capacity.

### INC-04
**Book Appointment** `<<include>>` **Create Reservation Hold**

Direction:

MUC-06 → MUC-08

Reason:
Every booking attempt uses the approved short-lived atomic ReservationHold.

### INC-05
**Process Full Payment** `<<include>>` **Verify Payment Result**

Direction:

MUC-09 → MUC-10

Reason:
Trusted payment verification is mandatory; the user's return from a payment page is not sufficient.

## `<<extend>>`

### EXT-01
**Process Full Payment** `<<extend>>` **Book Appointment**

Direction:

MUC-09 → MUC-06

Condition:

`[Booking policy = FULL_PAYMENT_REQUIRED]`

Reason:
Electronic full payment occurs only for the full-payment booking policy. `PAY_AT_FACILITY` creates no PaymentIntent.

### EXT-02
**Subscribe to Availability Alert** `<<extend>>` **Check Bookable Availability**

Direction:

MUC-11 → MUC-07

Condition:

`[No bookable capacity available]`

Reason:
Notify Me When Available is offered only when suitable capacity is unavailable and does not reserve capacity.

## No other main-overview relationships

Do not add any other `include`, `extend`, generalization, or temporal relationship to the first main diagram.

In particular, do not:

- connect Log In to browsing with `extend`;
- connect Register Patient and Log In to each other;
- connect notification delivery to every operational use case;
- use arrows to show Booking → Payment → Check-in → Service progression;
- make Doctor part of Record Visit Outcomes;
- make Patient part of staff rescheduling/check-in operations;
- make Platform Administrator part of daily facility operations.

---

# 10. Deliverable 2 — Actor Package Use Case Diagrams (BUILD LATER, NOT NOW)

The following detailed operations are preserved for later separate diagrams.

Do not render these as separate ellipses in the first main overview.

Each actor package diagram must still obey the core rule that Actors are outside the use-case container and the actor's detailed Use Cases are inside the relevant diagram/system context.

External service actors appear only in the actor package where they directly participate.

---

## 10.1 Visitor Package

Detailed Use Cases:

- Browse Facility & Service Information
- Search Doctors & Services
- View Available Days & Arrival Groups
- View Facility Location
- Register Patient
- Log In
- Verify WhatsApp OTP — helper / external-provider interaction

External service actors where relevant:

- Map Service
- WhatsApp Authentication Provider

Do not add booking before authentication.

---

## 10.2 Patient Package

Detailed Use Cases:

### Account & discovery
- Log In
- Verify WhatsApp OTP
- Manage Patient Profile
- Browse Facility & Service Information
- Search Doctors & Services
- View Available Days & Arrival Groups
- View Facility Location
- View Service Price & Policies
- View Attendance Instructions

### Booking
- Book Appointment
- Check Bookable Availability
- Create Reservation Hold
- View Reservation Hold Countdown
- Subscribe to Availability Alert

### Appointment follow-up
- View Patient Appointments
- View Booking Number & Verification Code
- Reconfirm Attendance
- Cancel Appointment
- View Arrival Instructions

### Payment
- Process Full Payment
- Verify Payment Result
- View Payment Status
- View Simplified Payment Receipt

### Visit / queue visibility
- View Check-in Status
- View Queue Status
- View Visit Outcome

### Notifications
- Receive Patient Notifications
- Receive Availability Alert

Important restrictions:

- no self-rescheduling;
- no self-check-in;
- no queue-position change;
- no arbitrary group selection;
- no booking-policy selection;
- no partial payment;
- no manual booking approval.

External actors where relevant:

- Payment Gateway
- Notification Service
- Map Service
- WhatsApp Authentication Provider

---

## 10.3 Facility Administrator Package

Detailed Use Cases:

### Facility configuration
- Manage Facility Data
- Manage Branch Display & Contact Data
- Manage Facility Images & Logo
- Associate Departments
- Associate Specialties

### Doctors and services
- Add Doctor
- Edit Doctor
- Add Service Offering
- Edit Service Offering
- Set Service Price
- Set Estimated Service Duration
- Set Attendance Instructions

### Policies
- Set Booking Policy
- Set Cancellation/Refund Policy
- Set No-show Policy
- Configure Attendance Reconfirmation

### Schedules and digital availability
- Manage Doctor Schedules
- Record Planned Schedule Exception
- Create Availability Release
- Configure Arrival Groups
- Set Initial Digital Capacity
- Publish Availability
- View Capacity Status
- Withdraw Remaining Capacity
- Freeze Availability
- Close Availability

### Staff
- Add Facility Staff Account
- Disable Facility Staff Account
- Assign Approved Role
- Provision Doctor Login Access

### Operations and oversight
- Review Daily Operations
- View Aafiatak Appointments
- View Payment Status
- Manage Operational Exceptions
- View Operational Reports

Restrictions:

- no published-capacity increase after publication;
- no restoration of withdrawn capacity;
- no management of another facility;
- no platform-wide settings;
- no deletion of audit history;
- no arbitrary custom permission designer.

---

## 10.4 Booking & Reception Staff Package

Detailed Use Cases:

### Daily operations
- Log In
- Review Daily Operations
- View Today's Doctors & Sessions
- View Arrival Groups
- View Capacity Status
- View Payment Status

### Capacity
- Withdraw Remaining Capacity
- Freeze Availability
- Close Availability

### Appointments
- Search Appointments
- View Appointment Details
- Reschedule Appointment
- Cancel Appointment

### Check-in and queue
- Register Patient Check-in
- Create or Activate Visit
- Create or Activate Queue Entry
- Correct Erroneous Check-in
- Manage Patient Queue
- View Waiting Patients
- Identify Next Patient
- Call Next Patient
- Remove Incorrect Queue Entry

### Visit progress
- Record Service Start
- Complete Visit
- Record Visit Non-completion
- Record No-show

### Late arrival
- Record Late Arrival
- Accept Late Arrival Manually
- Reschedule Late Patient
- Record No-show When Applicable
- Record Visit Non-completion When Applicable

### Operational exceptions
- Record Doctor Delay
- Record Doctor Absence
- Cancel Session
- Record Facility Closure
- Record Capacity Reduction
- Record Power or Connectivity Outage
- Record Booking Conflict
- Notify Affected Patients
- Offer Alternative Appointment
- Cancel Affected Appointment
- Escalate Case
- Resolve Affected Appointments
- Close Operational Exception

Restrictions:

- no doctor creation;
- no facility-core-data modification;
- no price/policy modification;
- no employee-account management;
- no platform settings;
- no arbitrary payment-result overwrite;
- no clinical content;
- no phone/walk-in Aafiatak booking creation;
- no capacity increase or withdrawal restoration.

---

## 10.5 Doctor Package

Detailed Use Cases:

- Log In
- View Today's Appointments
- View Upcoming Appointments
- View Doctor Arrival Groups
- View Waiting Patients
- Identify Next Patient
- Call Next Patient

Restrictions:

- no `IN_SERVICE` update;
- no visit completion/non-completion update;
- no no-show recording;
- no doctor-delay/absence reporting inside the system;
- no payment/refund operations;
- no availability modification;
- no service/price/policy modification;
- no clinical content.

---

## 10.6 Platform Administrator Package

Detailed Use Cases:

### Facility onboarding
- Review Facility Onboarding Request
- Request Additional Information
- Approve Facility
- Reject Facility
- Activate Facility
- Suspend Facility
- Provision Initial Facility Administrator

### Platform reference data
- Manage Cities
- Manage Regions
- Manage Facility Types
- Manage Public Reference Lists

### Platform staff
- Manage Platform Staff Accounts

### Support and oversight
- Review Technical Escalation
- Review Payment Escalation
- Review Conflict Escalation
- Review Audit Logs
- Provide Technical Support
- View Platform Indicators

Restrictions:

- no facility doctor/service management on behalf of the facility;
- no facility schedule/price/policy management;
- no daily booking operation;
- no daily queue operation.

---

# 11. Shared External-Service Detail

These are not separate human-actor packages. They are shown only where relevant.

## Payment Gateway participates in

- Process Full Payment
- Verify Payment Result
- Process Refund

`Process Refund` belongs to detailed financial/exception modeling and is not a separate ellipse in the first main overview.

Refund behavior must remain full amount or zero according to approved rules; no partial refund engine is allowed.

## Notification Service participates in

- Deliver Patient Notifications
- Deliver Facility Notifications
- Deliver Availability Alerts

Do not use WhatsApp for these general notifications in the current scope.

## Map Service participates in

- View Facility Location

## WhatsApp Authentication Provider participates in

- Verify WhatsApp OTP

WhatsApp is used only for authentication/phone verification in the current scope.

---

# 12. Deliverable 3 — Use Case Modeling Template (BUILD LATER)

For every important Use Case selected for detailed modeling, use this structure:

```text
Use Case Name:
Use Case ID:
Brief Description:
Primary Actor:
Secondary Actor(s):
Preconditions:

Main Success Scenario:
1.
2.
3.
...

Alternative / Failure Scenarios:
A1.
A2.
...

Postconditions:
```

Rules:

- Steps describe user/system behavior, not implementation classes or database calls.
- Include realistic success and failure scenarios.
- Preconditions must be actual preconditions from the authoritative specification.
- Postconditions must describe observable system state after the use case.
- Do not invent clinical workflows or deferred functionality.

---

# 13. Main Diagram Layout Specification

## 13.1 Canvas

Use a large landscape technical-document canvas suitable for academic presentation and high-resolution export.

Do not force the drawing into a small slide if readability suffers.

## 13.2 Boundary

- One large System Boundary centered on the canvas.
- All Use Cases inside it.
- All Actors outside it.

## 13.3 Actor placement

Preferred placement:

### Left of boundary
- Visitor
- Patient
- Facility Administrator
- Booking & Reception Staff

### Right of boundary
- Doctor
- Platform Administrator

### External-service actors around their nearest interactions
- WhatsApp Authentication Provider near authentication Use Cases
- Map Service near discovery/location
- Payment Gateway near payment
- Notification Service near notification delivery

No Actor may be placed inside the System Boundary to reduce connector length.

## 13.4 Internal visual organization

Do not draw UML Package boxes in the main overview.

Use spacing and alignment to form clear visual neighborhoods:

1. Access / Patient goals
2. Facility administration
3. Reception operations
4. Doctor operations
5. Platform administration

These are layout neighborhoods only, not UML Packages.

## 13.5 Routing

- Prefer clean orthogonal routing where supported by the prepared diagrams.net system.
- Do not route connectors through use-case ellipses.
- Do not route connectors through Actor labels.
- Minimize crossings.
- Keep `<<include>>` / `<<extend>>` labels readable.
- Do not change semantic relationships merely to make routing easier.

---

# 14. Mandatory Construction Order for the Main Diagram

Build incrementally.

## Phase 1 — Skeleton

Create only:

1. diagram title;
2. System Boundary;
3. all Actors needed by the main diagram;
4. empty internal layout space / neighborhoods.

Verify visually that all Actors are outside the boundary.

Then continue immediately; do not pause for user approval.

## Phase 2 — Public Access and Patient goals

Add MUC-01 through MUC-14 and their approved associations/relationships.

## Phase 3 — Facility Administrator goals

Add MUC-15 through MUC-19.

## Phase 4 — Booking & Reception Staff goals

Add MUC-20 through MUC-24 and the shared MUC-21/MUC-19 associations.

## Phase 5 — Doctor goals

Add MUC-25 and MUC-26.

## Phase 6 — Platform Administrator goals

Add MUC-27 through MUC-30.

## Phase 7 — Routing cleanup

After all elements exist:

- reduce crossings;
- correct spacing;
- separate edge labels;
- ensure no connector passes through a node;
- preserve all approved UML directions.

---

# 15. Fast Execution Rules for the Agent

The diagram-engineering repository has already been bootstrapped.

For this task:

## Do

- use the existing repository architecture;
- use the existing diagrams.net skill;
- use the existing design system;
- use the existing Use Case renderer/layout infrastructure;
- implement only the main overview defined in Sections 6–9;
- render the editable `.drawio`;
- export a high-resolution preview;
- perform only the minimum structural check needed to ensure the file opens and edges are attached;
- perform one focused visual review and fix obvious overlaps/routing/readability problems.

## Do not

- re-bootstrap the repository;
- redesign the engine;
- refactor unrelated infrastructure;
- re-extract the entire project specification;
- create the detailed Actor Package diagrams yet;
- create Use Case Modeling documents yet;
- create Class/Activity/Sequence/State diagrams yet;
- run the full test suite;
- run regression tests;
- increase test coverage;
- create synthetic diagrams;
- create new test files;
- create test fixtures;
- create regression cases;
- create synthetic validation datasets;
- create QA demo diagrams;
- spend time on infrastructure improvements not required to render this diagram.

New test artifacts are out of scope for this task.

Use only the smallest existing structural/visual checks necessary for correct delivery.

---

# 16. Main Diagram Final QA Checklist

## Lecturer/UML compliance

- [ ] One clear System Boundary exists.
- [ ] All Actors are outside the System Boundary.
- [ ] All Use Cases are inside the System Boundary.
- [ ] No UML Package boxes are drawn inside the first overview.
- [ ] All visible labels are English.
- [ ] Every Use Case begins with a verb.
- [ ] Actor Associations are plain solid lines without arrowheads.
- [ ] Every `<<include>>` arrow points from base to mandatory included use case.
- [ ] Every `<<extend>>` arrow points from conditional extending use case to base use case.
- [ ] No temporal-flow arrows exist.
- [ ] No Class/Attribute/database/component is present.
- [ ] No invented Actor Generalization exists.

## Product-scope compliance

- [ ] No old Aafiatak Use Case image was reused.
- [ ] No Database/PostgreSQL Actor exists.
- [ ] No internal HIS/EHR Actor exists.
- [ ] No FacilityApplicant Actor exists.
- [ ] No Forgot/Reset Password exists.
- [ ] No manual booking approval exists.
- [ ] No partial/deposit payment exists.
- [ ] No self check-in exists.
- [ ] No patient self-reschedule exists.
- [ ] No arbitrary Arrival Group selection exists.
- [ ] No published-capacity increase exists.
- [ ] No withdrawal restoration exists.
- [ ] Doctor is not associated with visit-state updates.
- [ ] Doctor is not associated with in-system delay/absence reporting.
- [ ] Reception Staff is not associated with doctor/service/policy administration.
- [ ] Platform Administrator is not associated with facility daily booking/queue operation.
- [ ] WhatsApp is used only for authentication/phone verification.

## Main overview content

- [ ] Exactly MUC-01 through MUC-30 are rendered.
- [ ] Detailed operations from Section 10 are not added as extra ellipses.
- [ ] Actor associations match Section 8 exactly.
- [ ] `include` relationships match Section 9 exactly.
- [ ] `extend` relationships match Section 9 exactly.

## Visual quality

- [ ] No Actor touches/overlaps the boundary.
- [ ] No ellipse crosses the boundary.
- [ ] No clipped text exists.
- [ ] No connector crosses through a use-case ellipse.
- [ ] No connector crosses through an Actor label.
- [ ] Relationship labels are readable.
- [ ] Crossings are minimized.
- [ ] Typography and ellipse geometry are consistent.
- [ ] The exported overview remains readable at presentation/report scale.
- [ ] The `.drawio` remains fully editable.

---

# 17. Review Record

This specification has been restructured to prevent the primary error in the earlier draft: attempting to render 50+ detailed use cases in one overview.

The revised structure was reviewed against:

- the lecturer's distinction between Use Case Diagram, Package organization, and Use Case Modeling;
- the lecturer's Actor / Use Case / Relationship rules;
- the authoritative Aafiatak actor list;
- patient permissions and restrictions;
- Facility Administrator permissions and restrictions;
- Booking & Reception Staff permissions and restrictions;
- Doctor limitations;
- Platform Administrator boundaries;
- external-service scope;
- passwordless WhatsApp OTP authentication;
- booking policy rules;
- ReservationHold rules;
- payment verification rules;
- capacity rules;
- check-in / queue / visit separation;
- operational-exception rules;
- deferred/out-of-scope functionality.

### Approved first-diagram size

- Actors: **10**
- Main overview Use Cases: **30**
- `<<include>>` relationships: **5**
- `<<extend>>` relationships: **2**
- UML Package boxes inside main overview: **0**

This is the approved scope for the first rendered Use Case Diagram.

The detailed actor operations are intentionally preserved in Section 10 for separate diagrams rather than deleted.

---

# 18. Final Instruction to the Implementation Agent

For the next execution task, render **only Deliverable 1 — Main Use Case Diagram** from Sections 6–9 and follow Sections 13–16.

Do not render Section 10 yet.

Do not create Use Case Modeling yet.

Do not create other UML diagrams yet.

Do not add, delete, rename, merge, or reinterpret the approved main actors/use cases/relationships based on personal preference.

If a genuine product contradiction is discovered, verify it against the authoritative Aafiatak specification at repository root. Otherwise execute this file directly.
