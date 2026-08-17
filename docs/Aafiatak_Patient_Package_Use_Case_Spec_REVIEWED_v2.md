# Aafiatak — Patient Package Use Case Diagram Specification

## 0. Document Status

**Deliverable:** Actor Package Use Case Diagram  
**Actor package:** Patient  
**System:** Aafiatak Medical Appointment Booking System  
**Language of visible diagram labels:** English  
**Status:** Reviewed execution specification — ready for diagram implementation

This document defines the approved content and UML semantics for the **Patient Package Use Case Diagram**. It is a detailed actor-oriented view created after the Main Use Case Diagram to expose patient operations without placing all detailed operations in the system overview.

This file is a modeling/drawing specification. It is not a UI specification, workflow implementation, class model, database model, Activity Diagram, or Sequence Diagram.

**Important course distinction:** this deliverable is a **detailed Use Case Diagram organized through the Patient package**, following the lecturer's method for controlling complexity in large systems. It is **not** the later formal UML Package Diagram deliverable. The later formal Package Diagram models packages and their dependencies; the Actor Package Use Case Diagram still uses Use Case notation such as Actor Associations, `<<include>>`, and `<<extend>>`.

---

# 1. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative product truth.
2. Lecturer UML PDF — academic UML rules and notation.
3. `docs/use_case.md` — approved Use Case work structure and previously selected package operations.
4. This Patient Package specification — reviewed execution truth for the Patient Package diagram.
5. Diagram renderer / SVG / draw.io tooling — presentation mechanics only.

If this file ever conflicts with the authoritative project specification, the project specification wins.

Do not invent product behavior from general UML knowledge.

---

# 2. Lecturer Rules Applied to This Diagram

The lecturer's Use Case method requires identification of:

- Actors;
- Use Cases;
- valid Relationships;
- the modeled system/context.

For a large system, detailed operations may be organized through packages so the system overview does not become unreadable.

Mandatory notation rules:

- Actor–Use Case Association: plain solid line, no arrowhead.
- `<<include>>`: dashed dependency, **base use case → mandatory included use case**.
- `<<extend>>`: dashed dependency, **conditional extending use case → base use case**.
- Use Case names must be verb-led.
- Use Case Diagram relationships must not be used to show chronological order.
- Preconditions, detailed steps, alternative scenarios, and postconditions belong to later Use Case Modeling documents rather than inside this diagram.
- Do not place Classes, Attributes, database tables, implementation components, screens, or UI controls in the diagram.

---

# 3. Diagram Scope and Structure

## 3.1 Diagram title

**Patient Package Use Case Diagram — Aafiatak Medical Appointment Booking System**

## 3.2 System boundary

Use one system boundary titled:

**Aafiatak Medical Appointment Booking System**

All Actors remain outside the System Boundary.

## 3.3 Patient package

This package is an organizational container for the detailed Patient Use Cases in the lecturer's Use Case-analysis stage. Its presence must not be interpreted as converting this deliverable into the later formal Package Diagram.

Inside the System Boundary, draw one UML package container titled:

**Patient Package**

All Patient Package Use Cases defined in this document belong inside that package.

Do not create nested UML packages merely for decoration. The functional categories below may be represented with whitespace, alignment, small headings, or subtle non-semantic background grouping.

## 3.4 Primary human actor

Exactly one human actor is primary in this package:

- **Patient**

Do not add Visitor as a second human actor to this package. Public discovery operations that remain available to an authenticated Patient are associated directly with Patient here.

Do not introduce actor generalization between Patient and Visitor.

## 3.5 External actors

Use only these external actors where they directly participate:

- **WhatsApp Authentication Provider**
- **Map Service**
- **Payment Gateway**
- **Notification Service**

Do not add Database, PostgreSQL, HIS/EHR, SMS Provider, Cashier, Facility Internal System, or any other implementation/external actor.

---

# 4. Review Finding Added from the Authoritative Specification

The previously preserved Patient Package list in `docs/use_case.md` omitted one explicit Patient Application capability from the authoritative project specification:

- **Log Out**

The authoritative Patient Application scope explicitly includes logout and revocation of the current authenticated session.

Therefore this reviewed Patient Package adds:

**PUC-03 — Log Out**

This is a **detail-only Patient Package Use Case**. It does not require changing the Main Use Case Overview.

No other new Patient capability has been invented.

---

# 5. Exact Patient Package Use Cases

The package contains exactly **29 Use Cases**.

IDs are traceability metadata. Do not display the `PUC-xx` IDs inside ellipses unless the lecturer explicitly requires IDs.

---

## 5.1 Account & Discovery

### PUC-01 — Log In

**Primary Actor:** Patient

Purpose: authenticate the Patient using the approved passwordless WhatsApp OTP mechanism and establish a valid revocable session.

Restrictions:
- No password login.
- No Forgot Password / Reset Password.
- SMS authentication is not used.

### PUC-02 — Verify WhatsApp OTP

**External Actor:** WhatsApp Authentication Provider  
**Role:** Helper Use Case

Purpose: perform the mandatory OTP verification required by passwordless authentication.

The Patient is **not** given a separate direct Association to this helper use case in the diagram. Patient participates through **Log In**, while the external WhatsApp provider directly participates in OTP verification.

### PUC-03 — Log Out

**Primary Actor:** Patient

Purpose: terminate/revoke the Patient's current authenticated application session.

This Use Case is added from the authoritative Patient Application scope.

### PUC-04 — Manage Patient Profile

**Primary Actor:** Patient

Purpose: view/edit approved basic Patient account/profile data.

Do not expand this into a medical profile or medical-record function.

### PUC-05 — Browse Facility & Service Information

**Primary Actor:** Patient

Purpose: browse public information about facilities/branch, departments, specialties, doctors, services, contact information, and approved public service details.

Do not interpret browsing as access to the facility's complete internal schedule.

### PUC-06 — Search Doctors & Services

**Primary Actor:** Patient

Purpose: search/discover using approved criteria such as doctor, department, specialty, and service.

Do not introduce advanced ratings/ranking or AI recommendations.

### PUC-07 — View Available Days & Arrival Groups

**Primary Actor:** Patient

Purpose: view current/preliminary Aafiatak digital availability, including available days and arrival-group windows.

Rules:
- Shows only capacity published to Aafiatak.
- Does not expose the facility's full internal schedule.
- An Arrival Group is an arrival window, not a guaranteed doctor-entry time.
- Patient does not choose an arbitrary Arrival Group.

### PUC-08 — View Facility Location

**Actors:**
- Patient
- Map Service

Purpose: view facility/branch location through the approved external map service.

### PUC-09 — View Service Price & Policies

**Primary Actor:** Patient

Purpose: view the service's applicable patient-facing booking information before commitment, including:

- configured amount;
- configured facility currency;
- booking policy;
- cancellation/refund policy;
- applicable no-show financial policy for fully paid bookings;
- optional estimated service duration where configured.

Rules:
- Patient cannot choose or override the booking policy.
- No currency conversion is performed by Aafiatak.
- Estimated duration is informational only.

### PUC-10 — View Attendance Instructions

**Primary Actor:** Patient

Purpose: view approved attendance/arrival instructions associated with the selected ServiceOffering / booking terms.

---

## 5.2 Booking & Availability

### PUC-11 — Book Appointment

**Primary Actor:** Patient

Purpose: create a confirmed appointment under the ServiceOffering's configured booking policy.

Exactly two policies exist:

- `FULL_PAYMENT_REQUIRED`
- `PAY_AT_FACILITY`

Rules:
- Patient does not choose the policy.
- There is no manual facility approval.
- There is no deposit or partial-payment booking.
- The system allocates the earliest currently bookable Arrival Group.
- A confirmed appointment stores the applicable booking snapshot.

### PUC-12 — Check Bookable Availability

**Role:** Helper Use Case

Purpose: validate that suitable Aafiatak capacity is currently bookable considering:

- remaining capacity;
- AvailabilityRelease lifecycle;
- ArrivalGroup lifecycle;
- time eligibility;
- ability for a valid hold window to finish before the group starts.

No direct Patient Association is drawn to this helper Use Case.

### PUC-13 — Create Reservation Hold

**Role:** Helper Use Case

Purpose: atomically protect one valid capacity unit during booking completion.

Rules:
- Every booking attempt uses a ReservationHold.
- Hold is short-lived.
- Patient cannot arbitrarily extend it.
- It protects one capacity unit.
- Expiry/release returns the seat when valid.
- It fixes the selected Arrival Group for the attempt.

No direct Patient Association is drawn to this helper Use Case.

### PUC-14 — View Reservation Hold Countdown

**Primary Actor:** Patient

Purpose: view the remaining valid completion time for the active ReservationHold.

This is patient-facing visibility, not a separate capacity-management operation.

### PUC-15 — Subscribe to Availability Alert

**Primary Actor:** Patient

Purpose: create a Notify Me When Available subscription when suitable bookable capacity is unavailable.

Rules:
- Not a reservation.
- No capacity protection.
- No priority.
- No queue position.
- Users compete normally after an alert.

---

## 5.3 Appointment Follow-up

### PUC-16 — View Patient Appointments

**Primary Actor:** Patient

Purpose: view the Patient's own upcoming and previous Aafiatak appointments and their approved high-level states/details.

The Patient sees only the Patient's own data.

### PUC-17 — View Booking Number & Verification Code

**Primary Actor:** Patient

Purpose: view the unique booking number and QR/verification code for a confirmed appointment.

QR/verification content must not expose unnecessary Patient data.

### PUC-18 — Reconfirm Attendance

**Primary Actor:** Patient

Purpose: respond to an attendance reconfirmation request when the facility has enabled reconfirmation.

Rule: failure to reconfirm does **not** automatically cancel the appointment.

### PUC-19 — Cancel Appointment

**Primary Actor:** Patient

Purpose: cancel the Patient's own appointment when self-cancellation is still permitted.

Rules:
- Appointment must still be `CONFIRMED`.
- Patient must not already be checked in.
- Assigned arrival-group window must not have started.
- The application displays the expected cancellation/refund result before confirmation.
- Refund is full amount or zero according to saved terms.
- `PAY_AT_FACILITY` has no Aafiatak electronic refund.
- Patient does not directly execute a Payment Gateway refund Use Case.

### PUC-20 — View Arrival Instructions

**Primary Actor:** Patient

Purpose: view the assigned Arrival Group/window and instructions for arrival, including guidance when arriving outside the assigned window.

Rules:
- No automatic transfer to another Arrival Group.
- No guaranteed late-arrival acceptance or priority.

---

## 5.4 Payment

### PUC-21 — Process Full Payment

**Actors:**
- Patient
- Payment Gateway

Purpose: perform the full electronic payment required only when the booking policy is `FULL_PAYMENT_REQUIRED`.

Rules:
- Full configured amount only.
- No partial/deposit payment.
- One approved gateway.
- Valid ReservationHold must remain eligible for confirmation.
- Full payment does not grant queue/clinical priority.

### PUC-22 — Verify Payment Result

**External Actor:** Payment Gateway  
**Role:** Helper Use Case

Purpose: verify the electronic payment through a trusted gateway webhook/query rather than trusting only the Patient application's return path.

No direct Patient Association is drawn to this helper Use Case.

### PUC-23 — View Payment Status

**Primary Actor:** Patient

Purpose: view payment state separately from appointment state.

Relevant presentation may include:
- payment completed;
- payment failed;
- payment expired;
- payment under review;
- refund pending;
- refunded;
- payment due at facility.

For `PAY_AT_FACILITY`, the UI may show payment due at facility but no `PaymentIntent` exists.

### PUC-24 — View Simplified Payment Receipt

**Primary Actor:** Patient

Purpose: view the simplified electronic-payment receipt where applicable, including the paid amount and external reference.

This is not a full medical invoice, cashier receipt system, or accounting function.

---

## 5.5 Visit & Queue Visibility

### PUC-25 — View Check-in Status

**Primary Actor:** Patient

Purpose: view whether facility staff has registered the Patient's arrival.

Rules:
- Patient cannot self-check-in.
- Facility staff performs check-in.
- Appointment and VisitInstance lifecycles remain separate.

### PUC-26 — View Queue Status

**Primary Actor:** Patient

Purpose: view the Patient's approximate queue position / number of patients ahead inside the Patient's own Arrival Group after valid check-in.

Rules:
- Patient cannot change queue position.
- Patient cannot view other Patients' private information.
- Full payment grants no queue priority.
- Platform does not promise exact service-entry time.
- Accepted late Patients are manually handled and are not promised a numeric automatic queue position.

### PUC-27 — View Visit Outcome

**Primary Actor:** Patient

Purpose: view the Patient's operational visit outcome separately from Appointment and Payment state, including:

- completed;
- not completed;
- no-show.

Do not expose clinical notes, diagnosis, prescriptions, laboratory/radiology results, or other medical-record content.

---

## 5.6 Notifications

### PUC-28 — Receive Patient Notifications

**Actors:**
- Patient
- Notification Service

Purpose: receive approved in-application/system notifications and reminders related to booking, payment/refund, hold expiry, reconfirmation, check-in, approaching turn, operational changes, and visit outcome.

Rule: WhatsApp is not used for these general notifications; WhatsApp scope is authentication/phone verification only.

### PUC-29 — Receive Availability Alert

**Actors:**
- Patient
- Notification Service

Purpose: receive a Notify Me When Available alert after a valid subscription when suitable capacity becomes bookable again.

Rules:
- Alert does not reserve capacity.
- Alert does not guarantee priority.
- Alert does not create queue position.
- Duplicate/annoying alert delivery must be prevented by the system.

---

# 6. Exact Actor–Use Case Association Matrix

## Patient

Associate Patient directly with:

- PUC-01 Log In
- PUC-03 Log Out
- PUC-04 Manage Patient Profile
- PUC-05 Browse Facility & Service Information
- PUC-06 Search Doctors & Services
- PUC-07 View Available Days & Arrival Groups
- PUC-08 View Facility Location
- PUC-09 View Service Price & Policies
- PUC-10 View Attendance Instructions
- PUC-11 Book Appointment
- PUC-14 View Reservation Hold Countdown
- PUC-15 Subscribe to Availability Alert
- PUC-16 View Patient Appointments
- PUC-17 View Booking Number & Verification Code
- PUC-18 Reconfirm Attendance
- PUC-19 Cancel Appointment
- PUC-20 View Arrival Instructions
- PUC-21 Process Full Payment
- PUC-23 View Payment Status
- PUC-24 View Simplified Payment Receipt
- PUC-25 View Check-in Status
- PUC-26 View Queue Status
- PUC-27 View Visit Outcome
- PUC-28 Receive Patient Notifications
- PUC-29 Receive Availability Alert

Do **not** draw direct Patient Associations to helper Use Cases:

- PUC-02 Verify WhatsApp OTP
- PUC-12 Check Bookable Availability
- PUC-13 Create Reservation Hold
- PUC-22 Verify Payment Result

## WhatsApp Authentication Provider

Associate only with:
- PUC-02 Verify WhatsApp OTP

## Map Service

Associate only with:
- PUC-08 View Facility Location

## Payment Gateway

Associate with:
- PUC-21 Process Full Payment
- PUC-22 Verify Payment Result

## Notification Service

Associate with:
- PUC-28 Receive Patient Notifications
- PUC-29 Receive Availability Alert

No other Actor Associations are approved unless a later source review finds explicit authoritative evidence.

---

# 7. Exact UML Relationships

Use only the following `include` / `extend` relationships in the first implementation of this Patient Package diagram.

## `<<include>>`

### PINC-01
**Log In** `<<include>>` **Verify WhatsApp OTP**

Direction: `PUC-01 → PUC-02`

Reason: WhatsApp OTP verification is mandatory for passwordless Patient login.

### PINC-02
**Book Appointment** `<<include>>` **Check Bookable Availability**

Direction: `PUC-11 → PUC-12`

Reason: every booking attempt requires currently valid bookable capacity.

### PINC-03
**Book Appointment** `<<include>>` **Create Reservation Hold**

Direction: `PUC-11 → PUC-13`

Reason: every booking attempt uses the approved atomic ReservationHold.

### PINC-04
**Process Full Payment** `<<include>>` **Verify Payment Result**

Direction: `PUC-21 → PUC-22`

Reason: trusted Payment Gateway verification is mandatory for the electronic payment outcome.

## `<<extend>>`

### PEXT-01
**Process Full Payment** `<<extend>>` **Book Appointment**

Direction: `PUC-21 → PUC-11`

Condition: `[Booking policy = FULL_PAYMENT_REQUIRED]`

Reason: electronic payment occurs only under the full-payment booking policy. `PAY_AT_FACILITY` creates no PaymentIntent.

### PEXT-02
**Subscribe to Availability Alert** `<<extend>>` **Check Bookable Availability**

Direction: `PUC-15 → PUC-12`

Condition: `[No bookable capacity available]`

Reason: Notify Me When Available is offered only when suitable capacity is unavailable.

---

# 8. Relationships Deliberately NOT Added

Do not add extra UML dependencies simply to show navigation or chronology.

In particular:

- Do not connect Browse → Search → Availability → Booking with arrows.
- Do not connect Booking → Payment → Appointment → Check-in → Queue → Visit as chronological arrows.
- Do not make View Reservation Hold Countdown an `include` solely because the countdown is displayed during booking.
- Do not connect Receive Availability Alert to Subscribe to Availability Alert with a temporal arrow.
- Do not connect notifications to every use case that may generate a notification.
- Do not make View Payment Status include View Simplified Payment Receipt.
- Do not make View Patient Appointments include View Booking Number & Verification Code.
- Do not connect View Check-in Status, View Queue Status, and View Visit Outcome with sequence arrows.
- Do not model Patient cancellation as directly including Process Refund; refund execution is not a Patient-initiated gateway operation.
- Do not add actor or use-case generalization merely to reduce association lines.

These details belong in later Use Case Modeling, Activity, Sequence, or State diagrams where appropriate.

---

# 9. Traceability to Main Overview

This Patient Package expands these Main Overview goals:

- `MUC-01 Discover Medical Services`
  - PUC-05 Browse Facility & Service Information
  - PUC-06 Search Doctors & Services
  - PUC-07 View Available Days & Arrival Groups
  - PUC-09 View Service Price & Policies
  - PUC-10 View Attendance Instructions

- `MUC-02 View Facility Location`
  - PUC-08 View Facility Location

- `MUC-04 Log In`
  - PUC-01 Log In
  - PUC-02 Verify WhatsApp OTP

- Detail-only authoritative account operation
  - PUC-03 Log Out

- `MUC-06 Book Appointment`
  - PUC-11 Book Appointment
  - PUC-12 Check Bookable Availability
  - PUC-13 Create Reservation Hold
  - PUC-14 View Reservation Hold Countdown

- `MUC-11 Subscribe to Availability Alert`
  - PUC-15 Subscribe to Availability Alert
  - PUC-29 Receive Availability Alert

- `MUC-12 Manage Patient Appointments`
  - PUC-16 View Patient Appointments
  - PUC-17 View Booking Number & Verification Code
  - PUC-18 Reconfirm Attendance
  - PUC-19 Cancel Appointment
  - PUC-20 View Arrival Instructions

- `MUC-09 Process Full Payment`
  - PUC-21 Process Full Payment
  - PUC-22 Verify Payment Result
  - PUC-23 View Payment Status
  - PUC-24 View Simplified Payment Receipt

- `MUC-13 Track Visit & Queue`
  - PUC-25 View Check-in Status
  - PUC-26 View Queue Status
  - PUC-27 View Visit Outcome

- `MUC-14 Deliver Notifications`
  - PUC-28 Receive Patient Notifications
  - PUC-29 Receive Availability Alert

- Patient account/profile detail
  - PUC-04 Manage Patient Profile

No detailed Patient operation is allowed to silently change the semantics of its Main Overview parent goal.

---

# 10. Explicit Patient Restrictions

The Patient Package must NOT contain or imply:

- patient self-rescheduling;
- patient self-check-in;
- queue-position changes;
- viewing other Patients' private data;
- choosing an arbitrary Arrival Group;
- choosing a booking policy;
- extending a ReservationHold arbitrarily;
- reserving multiple seats through one booking action;
- treating an availability alert as a reservation/priority;
- deposit payment;
- partial payment;
- remaining-balance management;
- manual booking approval;
- Password / Forgot Password / Reset Password flows;
- SMS authentication;
- general WhatsApp reminders/notifications;
- Patient-initiated Payment Gateway refund processing;
- exact guaranteed doctor-entry time;
- automatic late-patient transfer/re-entry;
- medical records;
- diagnoses;
- prescriptions;
- test results;
- insurance;
- family/dependent accounts;
- ratings/reviews;
- advanced complaints;
- in-app chat;
- video consultation;
- AI recommendations;
- medication reminders.

---

# 11. Visual Composition Requirements

The semantic content above is authoritative. Visual implementation may be refined without changing it.

Recommended composition:

- **Patient**: outside left side, vertically centered.
- **WhatsApp Authentication Provider**: outside near Account & Discovery.
- **Map Service**: outside near View Facility Location.
- **Payment Gateway**: outside near Payment.
- **Notification Service**: outside near Notifications.

Inside `Patient Package`, form six clear visual neighborhoods:

1. Account & Discovery
2. Booking & Availability
3. Appointment Follow-up
4. Payment
5. Visit & Queue Visibility
6. Notifications

Use whitespace, alignment, and restrained styling to distinguish neighborhoods.

Do not use chronological arrows between neighborhoods.

Do not use decorative backgrounds as semantic UML nodes.

Association routing should prioritize:

- short local connections;
- no line through ellipse labels;
- no line through Actor labels;
- clear local external-service connections;
- clearly separated dashed `include` / `extend` dependencies.

If one page cannot preserve normal report-scale readability, the implementation may use a multi-sheet presentation **within the same Patient Package deliverable**, but it must not remove or change any approved semantics. A split is a presentation decision only.

---

# 12. Final QA Checklist

## UML compliance

- [ ] Diagram title is correct.
- [ ] System Boundary is present and correctly named.
- [ ] Patient and all external Actors are outside the System Boundary.
- [ ] Patient Package and all Use Cases are inside the System Boundary.
- [ ] Exactly 29 approved Patient Package Use Cases are present.
- [ ] All visible labels are English.
- [ ] All Use Case names begin with verbs.
- [ ] Actor Associations are solid lines without arrowheads.
- [ ] No direct Patient Association exists to PUC-02, PUC-12, PUC-13, or PUC-22.
- [ ] `include` directions match Section 7.
- [ ] `extend` directions match Section 7.
- [ ] No chronological arrows exist.
- [ ] No Actor Generalization exists.
- [ ] No Class/Attribute/database/component/UI-screen element exists.

## Product compliance

- [ ] WhatsApp is used only for OTP authentication/phone verification.
- [ ] No SMS authentication exists.
- [ ] No password recovery exists.
- [ ] Patient cannot choose booking policy.
- [ ] Patient cannot choose arbitrary Arrival Group.
- [ ] Every booking attempt uses ReservationHold.
- [ ] Full electronic payment occurs only for `FULL_PAYMENT_REQUIRED`.
- [ ] `PAY_AT_FACILITY` creates no PaymentIntent.
- [ ] No deposit/partial payment exists.
- [ ] No manual booking approval exists.
- [ ] Availability alert grants no reservation/priority.
- [ ] Patient cannot self-check-in.
- [ ] Patient cannot self-reschedule.
- [ ] Patient cannot change queue position.
- [ ] Patient sees only own data.
- [ ] No exact doctor-entry-time promise exists.
- [ ] Appointment, Payment, Hold, Visit, and Queue concepts remain separate.
- [ ] General notifications do not use WhatsApp.
- [ ] No clinical/deferred features were added.

## Visual quality

- [ ] Functional neighborhoods are immediately understandable.
- [ ] Text is readable at report/presentation scale.
- [ ] External actors are placed near relevant use cases.
- [ ] No unnecessary long connector buses exist.
- [ ] No connector crosses an ellipse or Actor label.
- [ ] `include` / `extend` labels and conditions are readable.
- [ ] Package is not overloaded with false architectural meaning.
- [ ] Final visual remains clearly simpler than the Main Use Case overview.

---

# 13. Review Record

This specification was reviewed in multiple passes:

### Review 1 — Lecturer / UML method
Confirmed Actor, Use Case, Package organization, Association, `include`, `extend`, no chronology, and separation from later Use Case Modeling.

### Review 2 — Authoritative Patient scope
Checked Patient Application capabilities and Patient permissions/restrictions against the root project specification.

### Review 3 — Booking / availability / payment consistency
Checked ReservationHold, sequential Arrival Group allocation, booking policies, trusted payment verification, cancellation/refund, and availability-alert rules.

### Review 4 — Visit / queue / notification consistency
Checked staff-only check-in, Patient queue visibility, visit outcome visibility, late-arrival limitations, and notification-channel boundaries.

### Review 5 — Deferred/out-of-scope scan
Removed/forbade medical records, insurance, ratings, chat/video, family accounts, partial payment, self-check-in, self-rescheduling, arbitrary Arrival Group selection, and other deferred behavior.

### Review 6 — Omission audit
Detected and restored **Log Out** as a detail-only Patient Use Case because the authoritative Patient Application specification explicitly requires logout/session revocation.

### Review 7 — UML relationship audit
Kept only four strongly justified `include` relationships and two strongly justified `extend` relationships. Navigation, chronology, notification causation, and lifecycle progression were deliberately not represented as Use Case dependencies.

### Review 8 — Course-package distinction audit
Confirmed against the lecturer PDF and the supplied lecture notes that package organization is used to control complexity during Use Case analysis, while the later formal Package Diagram remains a separate structural deliverable. This file therefore remains a Use Case diagram specification with one organizational Patient package; it must not be evaluated using the formal Package Diagram rule that package-to-package relationships are Dependencies only.

### Review 9 — Granularity audit
Rechecked the 29 detailed Use Cases against the lecturer's warning against both excessive simplification and meaningless micro-detail. The retained `View ...` and `Receive ...` operations are kept because they are explicitly stated as current-scope Patient capabilities in the authoritative specification and/or the approved Patient Package list; they are not UI-control names or invented implementation steps.

---

# 14. Final Implementation Instruction

When this package is rendered:

- use this file as the execution truth for the Patient Package;
- preserve all 29 Use Cases;
- preserve the exact Actor Association Matrix;
- preserve only the approved six UML dependencies;
- do not infer additional requirements;
- do not reuse old diagrams as semantic sources;
- optimize presentation without modifying product/UML truth.
