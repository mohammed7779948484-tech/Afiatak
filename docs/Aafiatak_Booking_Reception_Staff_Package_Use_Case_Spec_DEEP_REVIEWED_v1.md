# Aafiatak — Booking & Reception Staff Package Use Case Diagram Specification

## 0. Document Status

**Deliverable:** Actor Package Use Case Diagram  
**Actor package:** Booking & Reception Staff  
**System:** Aafiatak Medical Appointment Booking System  
**Language of visible diagram labels:** English  
**Status:** Deep-reviewed execution specification — ready for diagram implementation

This document defines the approved content and UML semantics for the **Booking & Reception Staff Package Use Case Diagram**.

It was rebuilt from the authoritative Aafiatak project specification, the lecturer's UML PDF/course notes, and the approved `docs/use_case.md` inventory. It is not a blind transcription of the earlier package list: duplicated context-specific operations were normalized, missing explicitly supported operations were restored, and every proposed UML relationship was re-tested against the lecturer's `Association` / `<<include>>` / `<<extend>>` rules.

This is a detailed actor-oriented **Use Case Diagram organized through a package**. It is **not** the later formal UML Package Diagram, Activity Diagram, Sequence Diagram, Class Diagram, database model, UI specification, or implementation architecture.

---

# 1. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative product truth.
2. Lecturer UML PDF and supplied lecturer-course notes — academic UML rules and notation.
3. `docs/use_case.md` — approved Use Case work structure and detailed-operation inventory.
4. This reviewed Booking & Reception Staff specification — execution truth for this package after the documented review/normalization decisions below.
5. Rendering/layout tooling — presentation only.

Rules:

- Never invent product behavior from general UML knowledge.
- Never add normal hospital/HIS functionality merely because it seems realistic.
- Do not resolve open product decisions inside UML.
- If a product contradiction exists, the root project specification wins.
- All visible diagram labels must be English.
- Do not use old Aafiatak diagrams as semantic truth.

---

# 2. Lecturer Rules Applied

The lecturer's method requires:

- Actors;
- Use Cases;
- valid Relationships;
- System Boundary;
- packages to organize detailed operations in large systems;
- later textual Use Case Modeling for success/failure scenarios, preconditions, steps, and postconditions.

Mandatory notation:

- **Association:** solid plain line, no arrowhead.
- **`<<include>>`:** dashed dependency, direction **base use case → mandatory included use case**.
- **`<<extend>>`:** dashed dependency, direction **conditional extending use case → base use case**.
- Generalization only when genuine inheritance is supported.
- Use Case names begin with verbs.
- Do not use arrows to mean "then", "next", "after", or workflow order.
- Do not place Classes, Attributes, PostgreSQL/database tables, APIs, screens, buttons, or implementation components in a Use Case Diagram.

The lecturer also warns against both:
- shallow modeling; and
- meaningless micro-detail.

This specification therefore keeps meaningful operational goals but removes duplicate Use Cases that represented the same operation only under a different scenario label.

---

# 3. Diagram Scope and Structure

## 3.1 Exact Diagram Title

**Booking & Reception Staff Package Use Case Diagram — Aafiatak Medical Appointment Booking System**

## 3.2 System Boundary

Use one System Boundary titled:

**Aafiatak Medical Appointment Booking System**

All Actors stay outside the System Boundary.

## 3.3 Package

Inside the System Boundary, draw one UML package titled:

**Booking & Reception Staff Package**

All Use Cases in this file belong inside that package.

Functional sections below are **visual neighborhoods only**, not nested UML packages.

## 3.4 Primary Human Actor

Exactly one primary human Actor:

- **Booking & Reception Staff**

This role performs Aafiatak daily operational work for its own facility.

Do not introduce:
- Receptionist
- Cashier
- Facility User
- generic User
- Nurse
- Facility Applicant
- Hospital System
as additional actors.

## 3.5 External Actors

Use exactly these external Actors where they directly participate:

- **WhatsApp Authentication Provider**
- **Notification Service**

Do **not** add:
- Payment Gateway as a direct actor in this package;
- Map Service;
- SMS Provider;
- Database/PostgreSQL;
- HIS/EHR;
- facility internal scheduling system.

Reason:
Reception may **view** payment state and perform approved cancellation/conflict actions, but may not directly dictate or overwrite Payment Gateway outcomes. Financial gateway processing remains an independent system/payment concern.

---

# 4. Deep-Review Corrections to the Earlier Package Inventory

The previous `docs/use_case.md` package list is the starting inventory, but deep review found both omissions and duplicate context labels.

## 4.1 Restored — Verify WhatsApp OTP

`Log In` is explicitly a Reception capability, while all human-account authentication is passwordless WhatsApp OTP.

Added:

**BRUC-02 — Verify WhatsApp OTP**

Relationship:

**Log In `<<include>>` Verify WhatsApp OTP**

Reception has no separate direct Association to the helper.

## 4.2 Restored — Receive Facility Notifications

The Main Overview associates Booking & Reception Staff with notification delivery, and the authoritative specification explicitly defines facility-user notifications.

Added:

**BRUC-09 — Receive Facility Notifications**

Actors:
- Booking & Reception Staff
- Notification Service

## 4.3 Restored — View Active Reservation Holds

The authoritative Facility Appointment Management section explicitly allows facility staff to view active `ReservationHold` records for operational awareness without arbitrarily extending them.

Added:

**BRUC-08 — View Active Reservation Holds**

This is distinct from aggregate `View Capacity Status`.

## 4.4 Normalized — Late-arrival duplicate operations

The earlier detailed list separately contained:

- Reschedule Late Patient
- Record No-show When Applicable
- Record Visit Non-completion When Applicable

These are not new system services. They are the **same existing operations**:

- Reschedule Appointment
- Record No-show
- Record Visit Non-completion

used as alternative outcomes of a late-arrival scenario.

They are therefore **not duplicated as extra ellipses**.

Their late-arrival conditions must be documented later in Use Case Modeling / Activity modeling.

## 4.5 Normalized — Cancel Affected Appointment

The earlier operational-exception list contained `Cancel Affected Appointment`.

This is not a distinct cancellation mechanism. It is the existing:

**Cancel Appointment**

used under a facility-responsible exception/conflict path, where a full refund is started when applicable.

Therefore it is not duplicated as another ellipse.

**No product behavior was deleted.**  
The four normalized context labels remain explicitly preserved as scenario contexts in Sections 10 and 11 of this file.

---

# 5. Exact Use Cases

The reviewed package contains exactly **43 Use Cases**.

IDs are traceability metadata; do not show them inside visible ellipses unless the lecturer explicitly requires IDs.

---

# 5.1 Authentication

## BRUC-01 — Log In

**Primary Actor:** Booking & Reception Staff

Purpose:
Authenticate the provisioned staff account and establish a valid facility-dashboard session.

Rules:
- Passwordless.
- WhatsApp OTP.
- No SMS.
- No password.
- No Forgot Password / Reset Password.
- Staff role is provisioned by Facility Administrator; it is not public self-registration.

---

## BRUC-02 — Verify WhatsApp OTP

**External Actor:** WhatsApp Authentication Provider  
**Role:** Helper Use Case

Purpose:
Perform mandatory OTP verification for Login.

No direct Reception Association is drawn to this helper.

---

# 5.2 Daily Operations

## BRUC-03 — Review Daily Operations

**Primary Actor:** Booking & Reception Staff

Purpose:
Review the current Aafiatak operational situation for the facility.

The **Today Pulse Board** is the UI supporting this goal. Do not model "Open Dashboard" or "Open Today Pulse Board" as a Use Case.

May expose relevant operational information such as:
- sessions/doctors;
- arrival groups;
- capacity;
- confirmed appointments;
- payment-review indicators;
- checked-in/waiting patients;
- operational exceptions.

---

## BRUC-04 — View Today's Doctors & Sessions

**Primary Actor:** Booking & Reception Staff

Purpose:
View today's facility doctors/sessions relevant to Aafiatak operations.

---

## BRUC-05 — View Arrival Groups

**Primary Actor:** Booking & Reception Staff

Purpose:
View Aafiatak Arrival Groups and windows for current operations.

Rules:
- Groups are Aafiatak arrival windows, not exact doctor-entry times.
- Staff must not treat them as the facility's complete internal queue/calendar.

---

## BRUC-06 — View Capacity Status

**Primary Actor:** Booking & Reception Staff

Purpose:
View capacity information such as:

- published;
- held;
- confirmed;
- withdrawn;
- remaining;
- stale/exhausted indicators;
- group-level capacity where relevant.

Rule:
This is Aafiatak digital capacity only.

---

## BRUC-07 — View Payment Status

**Primary Actor:** Booking & Reception Staff

Purpose:
View independent payment state for relevant appointments.

Rules:
- Payment state remains separate from Appointment state.
- Staff cannot arbitrarily overwrite gateway outcomes.
- `PAY_AT_FACILITY` creates no `PaymentIntent`.
- Payment Gateway is not directly associated with this viewing operation.

---

## BRUC-08 — View Active Reservation Holds

**Primary Actor:** Booking & Reception Staff

Purpose:
View active ReservationHold records for operational awareness.

Rules:
- Staff cannot arbitrarily extend a hold.
- A hold is not an Appointment.
- A held capacity unit cannot be withdrawn.

---

## BRUC-09 — Receive Facility Notifications

**Actors:**
- Booking & Reception Staff
- Notification Service

Purpose:
Receive approved system/in-application facility notifications, including where applicable:

- new confirmed bookings;
- payment requiring review;
- Patient cancellation/reconfirmation/check-in;
- late arrival;
- hold expiry returning capacity;
- stale/exhausted availability;
- unresolved operational exceptions.

Rules:
- General notifications are not sent through WhatsApp in current scope.
- SMS is not used.

---

# 5.3 Capacity Operations

## BRUC-10 — Withdraw Remaining Capacity

**Primary Actor:** Booking & Reception Staff

Purpose:
Withdraw one, several, or all valid remaining Aafiatak capacity units to the facility's internal schedule.

Rules:
- one-way only;
- no restoration to same release;
- no withdrawal of active held capacity;
- no withdrawal of confirmed capacity;
- no published-capacity increase;
- no `+1`.

---

## BRUC-11 — Freeze Availability

**Primary Actor:** Booking & Reception Staff

Purpose:
Temporarily stop new holds/bookings for an approved release/group.

Rules:
- freeze is not withdrawal;
- existing valid holds and confirmed appointments are preserved according to the approved lifecycle;
- freeze may later return to bookable state where lifecycle rules allow.

---

## BRUC-12 — Close Availability

**Primary Actor:** Booking & Reception Staff

Purpose:
Close the applicable release/group for new holds/bookings.

Rules:
- does not silently delete confirmed appointments/history;
- does not restore withdrawn capacity;
- closed/cancelled lifecycle must not be reopened contrary to domain rules.

---

# 5.4 Appointment Operations

## BRUC-13 — Search Appointments

**Primary Actor:** Booking & Reception Staff

Purpose:
Search relevant facility appointments using approved identifiers such as:

- booking number;
- Patient phone number;
- Patient name.

At check-in, QR/verification code may also be used to identify the intended appointment; this is handled within check-in modeling rather than as another standalone Use Case.

---

## BRUC-14 — View Appointment Details

**Primary Actor:** Booking & Reception Staff

Purpose:
View authorized operational details of an Aafiatak appointment.

May include:
- appointment state;
- arrival group/window;
- booking snapshot;
- relevant history;
- independent payment state reference.

Do not expose unnecessary clinical information.

---

## BRUC-15 — Reschedule Appointment

**Primary Actor:** Booking & Reception Staff

Purpose:
Reschedule a confirmed appointment **after communication and agreement**.

Mandatory domain rules:

- secure valid new capacity first;
- in-place reschedule only for the **same ServiceOffering** and same snapshotted financial/booking terms;
- old seat released only after new seat is secured;
- operation is atomic;
- history/reason recorded;
- financial snapshot remains unchanged.

If the requested destination has different service/price/policy terms:
- do not perform in-place reschedule;
- existing appointment follows its cancellation rules;
- a new booking must use the normal Patient booking flow.

Reception must not create a new Aafiatak booking on behalf of a phone/walk-in Patient.

---

## BRUC-16 — Cancel Appointment

**Primary Actor:** Booking & Reception Staff

Purpose:
Cancel an appointment with a recorded reason when authorized.

This Use Case also covers the facility-side cancellation action used in operational-exception/conflict resolution.

Rules:
- facility-responsible cancellation starts a full refund when an electronic amount was paid;
- staff does not manually force a Payment Gateway result;
- cancellation/history remains auditable;
- no silent deletion.

---

# 5.5 Check-in & Queue

## BRUC-17 — Register Patient Check-in

**Primary Actor:** Booking & Reception Staff

Purpose:
Register arrival for the intended valid `CONFIRMED` Appointment.

Check-in identification may use:
- booking number;
- Patient phone number;
- QR/verification code.

Rules:
- Patient self-check-in is out of scope.
- Cancelled Appointment cannot be checked in.
- Late arrivals follow explicit late-arrival handling.
- Valid check-in records actual arrival time and activates service-day operational state.

---

## BRUC-18 — Create or Activate Visit

**Primary Actor:** Booking & Reception Staff

Purpose:
Create/activate the `VisitInstance` representing the actual service-day occurrence.

Rules:
- Appointment and VisitInstance are separate lifecycles.
- VisitInstance contains operational, not clinical, data.

---

## BRUC-19 — Create or Activate Queue Entry

**Primary Actor:** Booking & Reception Staff

Purpose:
Create/activate the Patient's `QueueEntry` inside the booked Arrival Group.

QueueEntry remains separate from VisitInstance and Appointment status.

---

## BRUC-20 — Correct Erroneous Check-in

**Primary Actor:** Booking & Reception Staff

Purpose:
Correct a genuine erroneous check-in/queue registration.

Rules:
- allowed only before service starts;
- recorded/audited reason required;
- associated QueueEntry is removed;
- VisitInstance may return from `CHECKED_IN` to `CREATED` when valid.

---

## BRUC-21 — Manage Patient Queue

**Primary Actor:** Booking & Reception Staff

Purpose:
Manage Aafiatak's lightweight queue inside an Arrival Group.

Rules:
- not the facility's complete internal queue;
- on-time order uses actual check-in time;
- ties use earlier `confirmed_at`;
- full payment grants no priority.

---

## BRUC-22 — View Waiting Patients

**Primary Actor:** Booking & Reception Staff

Purpose:
View checked-in/waiting Patients in the approved Aafiatak queue context.

Only relevant operational Patient information may be shown.

---

## BRUC-23 — Identify Next Patient

**Primary Actor:** Booking & Reception Staff

Purpose:
Identify the next Patient according to the approved queue order/manual handling rules.

---

## BRUC-24 — Call Next Patient

**Primary Actor:** Booking & Reception Staff

Purpose:
Call the next/selected waiting Patient.

This operation is also available to Doctor in the Doctor Package.

Do not imply that calling the Patient automatically changes VisitInstance to `IN_SERVICE`.

---

## BRUC-25 — Remove Incorrect Queue Entry

**Primary Actor:** Booking & Reception Staff

Purpose:
Remove an incorrect queue entry with a recorded reason.

QueueEntry transitions to `REMOVED`; this is an audited operational correction, not requeue/re-entry.

---

# 5.6 Visit Progress

## BRUC-26 — Record Service Start

**Primary Actor:** Booking & Reception Staff

Purpose:
Change the authorized VisitInstance to `IN_SERVICE`.

Doctor is not authorized to perform this state change.

---

## BRUC-27 — Complete Visit

**Primary Actor:** Booking & Reception Staff

Purpose:
Record operational completion of the VisitInstance.

This is not clinical documentation.

---

## BRUC-28 — Record Visit Non-completion

**Primary Actor:** Booking & Reception Staff

Purpose:
Record `NOT_COMPLETED` when the Patient arrived but service was not completed according to actual circumstances.

This same Use Case may be one late-arrival outcome where applicable; do not duplicate a late-specific ellipse.

---

## BRUC-29 — Record No-show

**Primary Actor:** Booking & Reception Staff

Purpose:
Record a `NO_SHOW` outcome when valid.

Rules:
- normally only after assigned Arrival Group window ends without valid check-in;
- terminal visit outcome;
- may trigger the saved no-show financial rule for fully paid bookings;
- staff does not manually fabricate/reforce gateway state.

This same Use Case may be a late-arrival outcome where applicable; do not duplicate a late-specific ellipse.

---

# 5.7 Late Arrival

## BRUC-30 — Record Late Arrival

**Primary Actor:** Booking & Reception Staff

Purpose:
Record that the Patient arrived outside the assigned Arrival Group window and begin the documented manual operational decision.

Rules:
- no automatic transfer to a later group;
- no automatic re-entry;
- no automatic queue position;
- no guaranteed acceptance/priority.

---

## BRUC-31 — Accept Late Arrival Manually

**Primary Actor:** Booking & Reception Staff

Purpose:
Accept a late Patient operationally when staff decides this is appropriate.

Rules:
- decision must occur before terminal `NO_SHOW`;
- original Appointment and original Arrival Group remain unchanged;
- staff records check-in;
- QueueEntry is created/activated for operational visibility;
- Patient is flagged for manual handling;
- excluded from normal automatic queue-position calculation;
- no numeric priority promise;
- does not consume capacity from another Arrival Group.

Other late-arrival outcomes use the already defined:
- BRUC-15 Reschedule Appointment;
- BRUC-28 Record Visit Non-completion;
- BRUC-29 Record No-show.

They are scenario alternatives, not duplicated Use Cases.

---

# 5.8 Operational Exceptions

## BRUC-32 — Record Doctor Delay

**Primary Actor:** Booking & Reception Staff

Purpose:
Record `DOCTOR_DELAYED` after information is received from Doctor/facility management.

Doctor does not report delay through an in-system Doctor action.

---

## BRUC-33 — Record Doctor Absence

**Primary Actor:** Booking & Reception Staff

Purpose:
Record `DOCTOR_ABSENT` after information is received from the Doctor/facility management.

---

## BRUC-34 — Cancel Session

**Primary Actor:** Booking & Reception Staff

Purpose:
Record/execute the approved session-cancellation operational action.

Rules:
- affected release/session becomes non-bookable;
- active ReservationHolds are released;
- confirmed appointments/history remain preserved;
- every affected confirmed appointment requires documented resolution.

---

## BRUC-35 — Record Facility Closure

**Primary Actor:** Booking & Reception Staff

Purpose:
Record a `FACILITY_CLOSED` operational exception when applicable.

---

## BRUC-36 — Record Capacity Reduction

**Primary Actor:** Booking & Reception Staff

Purpose:
Record a `CAPACITY_REDUCED` operational exception.

This does not authorize an increase in published capacity or restoration of withdrawn capacity.

---

## BRUC-37 — Record Power or Connectivity Outage

**Primary Actor:** Booking & Reception Staff

Purpose:
Record the approved power/connectivity operational exception.

---

## BRUC-38 — Record Booking Conflict

**Primary Actor:** Booking & Reception Staff

Purpose:
Create/record the `CONFLICT_DETECTED` operational exception for a confirmed-booking conflict.

The conflict cannot be resolved by importing free internal capacity into the same published Aafiatak release.

---

## BRUC-39 — Notify Affected Patients

**Actors:**
- Booking & Reception Staff
- Notification Service

Purpose:
Initiate approved system notification of affected Patients during an operational exception.

Rules:
- Notification Service handles approved delivery.
- WhatsApp is not the general notification channel.
- critical manual contact may exist operationally but is not modeled as a new messaging Actor.

---

## BRUC-40 — Offer Alternative Appointment

**Primary Actor:** Booking & Reception Staff

Purpose:
Offer a suitable alternative after communication with the affected Patient.

Any actual reschedule must obey BRUC-15 rules and secure valid capacity first.

---

## BRUC-41 — Escalate Case

**Primary Actor:** Booking & Reception Staff

Purpose:
Create a documented support escalation when technical/payment/conflict resolution cannot be safely completed at facility level.

The Platform Administrator handles the receiving/review side in the Platform Administrator Package; do not duplicate that actor into this package merely to show handoff chronology.

---

## BRUC-42 — Resolve Affected Appointments

**Primary Actor:** Booking & Reception Staff

Purpose:
Record a documented outcome/action for every appointment affected by an OperationalException.

Approved outcomes may include:
- suitable alternative/reschedule where valid;
- facility-side cancellation/full refund when applicable;
- documented escalation.

No silent deletion is allowed.

---

## BRUC-43 — Close Operational Exception

**Primary Actor:** Booking & Reception Staff

Purpose:
Close an OperationalException only after required actions/outcomes for affected appointments are recorded.

**Important UML interpretation:**  
`Resolve Affected Appointments` is a **precondition for closure**, not automatically an `<<include>>` relationship. Do not convert a precondition into an include arrow merely because it must be true before closure.

---

# 6. Exact Actor–Use Case Association Matrix

## Booking & Reception Staff

Directly associate with every Use Case **except** BRUC-02 Verify WhatsApp OTP.

Therefore Reception has exactly **42 direct Associations**.

## WhatsApp Authentication Provider

Associate only with:

- BRUC-02 Verify WhatsApp OTP

## Notification Service

Associate with:

- BRUC-09 Receive Facility Notifications
- BRUC-39 Notify Affected Patients

No other external Actor associations are approved.

**Total direct Actor Associations: 45**

---

# 7. Exact UML Relationships

Use exactly **5 `<<include>>` relationships**.

There are **0 approved `<<extend>>` relationships** in this package.

There is **0 Generalization**.

## BRINC-01
**Log In** `<<include>>` **Verify WhatsApp OTP**

Direction:
`BRUC-01 → BRUC-02`

Reason:
OTP verification is mandatory for passwordless login.

## BRINC-02
**Register Patient Check-in** `<<include>>` **Create or Activate Visit**

Direction:
`BRUC-17 → BRUC-18`

Reason:
Valid check-in creates/activates the VisitInstance.

## BRINC-03
**Register Patient Check-in** `<<include>>` **Create or Activate Queue Entry**

Direction:
`BRUC-17 → BRUC-19`

Reason:
Valid check-in creates/activates the queue entry inside the assigned Arrival Group.

## BRINC-04
**Correct Erroneous Check-in** `<<include>>` **Remove Incorrect Queue Entry**

Direction:
`BRUC-20 → BRUC-25`

Reason:
The approved correction explicitly removes the associated erroneous QueueEntry.

## BRINC-05
**Accept Late Arrival Manually** `<<include>>` **Register Patient Check-in**

Direction:
`BRUC-31 → BRUC-17`

Reason:
An accepted late Patient must still be checked in by facility staff; the late-specific distinction is manual handling rather than a different automatic queue lifecycle.

---

# 8. Why No `<<extend>>` Was Added

Several situations are conditional, but they are better represented as alternative/failure flows in Use Case Modeling rather than `extend` arrows here.

Do **not** add:

- `Reschedule Appointment <<extend>> Record Late Arrival`
- `Record No-show <<extend>> Record Late Arrival`
- `Record Visit Non-completion <<extend>> Record Late Arrival`
- `Accept Late Arrival Manually <<extend>> Record Late Arrival`
- `Escalate Case <<extend>> Record Booking Conflict`

Reason:
These represent alternative operational decisions after conditions/events, but the current detailed Use Cases are independently meaningful goals. Adding `extend` would risk using Use Case relationships as workflow branching, which the lecturer prohibits.

The branching logic belongs in the later Activity / Use Case Modeling for **Handle Late Arrival** and **Manage Operational Exceptions**.

---

# 9. Relationships Deliberately NOT Added

Do not draw arrows for:

- Login → Review Daily Operations
- Review Daily Operations → View Capacity Status
- View Capacity Status → Withdraw / Freeze / Close
- Search Appointment → View Appointment Details
- View Appointment Details → Reschedule / Cancel
- Identify Next Patient → Call Next Patient
- Call Next Patient → Record Service Start
- Record Service Start → Complete Visit
- OperationalException type → Notify / Alternative / Cancel / Escalate / Close
- Late Arrival → any outcome
- Notify Affected Patients → Receive Facility Notifications

These are chronological, navigational, scenario, or causal relationships rather than approved Use Case dependencies.

Do not add:
- Actor Generalization;
- package Dependency arrows inside this actor package;
- Payment Gateway relations to View Payment Status;
- Doctor relations to Visit Progress;
- Doctor relations to delay/absence recording.

---

# 10. Traceability to Main Overview

## `MUC-04 — Log In`
- BRUC-01 Log In
- BRUC-02 Verify WhatsApp OTP

## `MUC-14 — Deliver Notifications`
- BRUC-09 Receive Facility Notifications
- BRUC-39 Notify Affected Patients (exception context)

## `MUC-18 — Review Daily Operations`
- BRUC-03 Review Daily Operations
- BRUC-04 View Today's Doctors & Sessions
- BRUC-05 View Arrival Groups
- BRUC-06 View Capacity Status
- BRUC-07 View Payment Status
- BRUC-08 View Active Reservation Holds

## `MUC-20 — Manage Facility Appointments`
- BRUC-13 Search Appointments
- BRUC-14 View Appointment Details
- BRUC-15 Reschedule Appointment
- BRUC-16 Cancel Appointment

## `MUC-21 — Manage Capacity`
- BRUC-06 View Capacity Status
- BRUC-10 Withdraw Remaining Capacity
- BRUC-11 Freeze Availability
- BRUC-12 Close Availability

## `MUC-22 — Manage Patient Arrival & Queue`
- BRUC-17 Register Patient Check-in
- BRUC-18 Create or Activate Visit
- BRUC-19 Create or Activate Queue Entry
- BRUC-20 Correct Erroneous Check-in
- BRUC-21 Manage Patient Queue
- BRUC-22 View Waiting Patients
- BRUC-23 Identify Next Patient
- BRUC-25 Remove Incorrect Queue Entry

## `MUC-23 — Record Visit Outcomes / Progress`
- BRUC-26 Record Service Start
- BRUC-27 Complete Visit
- BRUC-28 Record Visit Non-completion
- BRUC-29 Record No-show

## `MUC-24 — Handle Late Arrival`
- BRUC-30 Record Late Arrival
- BRUC-31 Accept Late Arrival Manually
- uses BRUC-15 / BRUC-28 / BRUC-29 as alternative scenario outcomes where applicable

## `MUC-26 — Call Next Patient`
- BRUC-23 Identify Next Patient
- BRUC-24 Call Next Patient

## `MUC-19 — Manage Operational Exceptions`
- BRUC-32 through BRUC-43

---

# 11. Preserved Scenario Contexts After Normalization

The following source operations were intentionally normalized rather than deleted:

### Earlier label: `Reschedule Late Patient`
Use:
**BRUC-15 Reschedule Appointment**

Late-arrival condition:
Patient is late, staff and Patient agree to reschedule, and valid new capacity is secured.

### Earlier label: `Record No-show When Applicable`
Use:
**BRUC-29 Record No-show**

Late-arrival condition:
The arrival window ended without valid check-in and `NO_SHOW` is the correct actual outcome.

### Earlier label: `Record Visit Non-completion When Applicable`
Use:
**BRUC-28 Record Visit Non-completion**

Late-arrival condition:
The Patient arrived but the service was not completed and `NOT_COMPLETED` is the correct actual outcome.

### Earlier label: `Cancel Affected Appointment`
Use:
**BRUC-16 Cancel Appointment**

Operational-exception condition:
Facility cancellation/conflict requires facility-side cancellation; if payment was collected, the approved full-refund path starts.

This normalization follows the lecturer's granularity rule: do not create two Use Cases for the same service only because it is invoked under different scenarios.

---

# 12. Explicit Restrictions

The package must NOT contain or imply:

- creation of doctors;
- modification of core facility profile;
- service price changes;
- booking/payment/refund policy changes;
- employee account management;
- platform settings;
- platform-wide reference data management;
- published-capacity increase;
- restoration of withdrawn capacity;
- `+1` capacity;
- withdrawal of held capacity;
- withdrawal of confirmed capacity;
- arbitrary gateway-result overwrite;
- manual charge/refund state fabrication;
- clinical notes;
- diagnosis;
- prescriptions;
- laboratory/radiology results;
- medical invoice/cashier/accounting;
- phone/walk-in Aafiatak booking creation;
- self-check-in by Patient;
- exact guaranteed doctor-entry time;
- automatic late-patient group transfer;
- automatic re-entry/requeue;
- queue priority from full payment;
- Doctor visit-state updates;
- Doctor in-system delay/absence reporting;
- SMS authentication/notifications;
- general WhatsApp notifications;
- Password/Forgot Password/Reset Password;
- deletion of audit history.

---

# 13. Critical Domain Invariants for This Package

## Capacity

`remaining = published - held - confirmed - withdrawn_to_facility`

- no negative capacity;
- no double consumption;
- active holds cannot be withdrawn;
- confirmed capacity cannot be withdrawn;
- withdrawal does not reverse;
- internal free capacity cannot be imported into a published release.

## Queue

For normal on-time queue:
1. actual check-in time;
2. earlier appointment `confirmed_at` as tie-breaker.

Full electronic payment gives no priority.

## Visit states

Only facility staff may record:
- `CHECKED_IN`
- `IN_SERVICE`
- `COMPLETED`
- `NOT_COMPLETED`
- `NO_SHOW`

Doctor may call the next Patient but does not update those visit states.

## Late arrival

Accepted late Patient:
- stays linked to original Appointment/Arrival Group;
- manual handling;
- no automatic numerical queue position;
- no re-entry status;
- no other Arrival Group capacity consumption.

## Operational Exceptions

Supported examples:
- `DOCTOR_DELAYED`
- `DOCTOR_ABSENT`
- `SESSION_CANCELLED`
- `FACILITY_CLOSED`
- `CAPACITY_REDUCED`
- `POWER_OR_CONNECTIVITY_OUTAGE`
- `CONFLICT_DETECTED`

Exception closure requires documented outcome/action for affected appointments.

---

# 14. Granularity Decisions

## No separate `Identify Booking`

Appointment identification for ordinary search belongs to `Search Appointments`; check-in identifiers are part of `Register Patient Check-in` modeling. A standalone extra ellipse is not required.

## No separate `View Appointment History`

History is part of `View Appointment Details`.

## No separate `Process Refund`

Reception does not manually control gateway financial outcomes. Facility-responsible cancellation may trigger the system's approved full-refund path, but `Process Refund` is not a Reception-controlled gateway Use Case.

## No duplicate late-arrival reschedule/no-show/non-completion

See Section 11.

## No duplicate operational-exception cancellation

See Section 11.

## No separate Use Case for every Today Pulse Board field

The board is UI. Its data belongs to the approved actor goals such as Review Daily Operations / View Capacity Status / View Payment Status.

---

# 15. Visual Composition Requirements

This is the most complex Actor Package so far. Do not solve it with a giant auto-layout canvas or spaghetti routing.

Use **eight visual neighborhoods**:

1. Authentication
2. Daily Operations
3. Capacity Operations
4. Appointment Operations
5. Check-in & Queue
6. Visit Progress
7. Late Arrival
8. Operational Exceptions

These are visual neighborhoods only — **not nested UML packages**.

Recommended actor placement:

- **Booking & Reception Staff:** outside left, near the central operational neighborhoods.
- **WhatsApp Authentication Provider:** outside near Login/OTP.
- **Notification Service:** outside near Receive Facility Notifications / Notify Affected Patients.

Because Reception has many direct Associations, a repeated visual symbol of the **same Booking & Reception Staff actor** may be used only as a presentation technique if necessary to avoid a giant line bus, provided:
- the label is identical;
- semantic actor count remains one;
- no different permissions are implied;
- the repeated symbols are clearly presentation duplicates.

Prefer local routing and deliberate composition.

Do not:
- shrink text to force everything onto one huge artboard;
- create long edge buses;
- route through labels/ellipses;
- invent actor generalization to reduce lines;
- add fake UML dependencies just to organize the drawing.

If one normal report-scale sheet cannot remain legible, a coordinated multi-sheet presentation of the **same semantic package** is acceptable as a presentation decision, but do not remove Use Cases or create false semantic subpackages.

---

# 16. Final QA Checklist

## UML

- [ ] Correct diagram title.
- [ ] Correct System Boundary title.
- [ ] Booking & Reception Staff outside boundary.
- [ ] WhatsApp Authentication Provider outside boundary.
- [ ] Notification Service outside boundary.
- [ ] Booking & Reception Staff Package inside boundary.
- [ ] Exactly 43 Use Cases.
- [ ] All visible labels English.
- [ ] Every Use Case name starts with a verb.
- [ ] Reception has exactly 42 direct Associations.
- [ ] WhatsApp Provider has exactly 1 Association.
- [ ] Notification Service has exactly 2 Associations.
- [ ] Exactly 5 `<<include>>`.
- [ ] 0 `<<extend>>`.
- [ ] 0 Generalization.
- [ ] No chronological arrows.
- [ ] No database/classes/components/UI controls.

## Authentication

- [ ] Login uses WhatsApp OTP.
- [ ] No direct Reception Association to Verify WhatsApp OTP.
- [ ] No SMS/password recovery.

## Capacity

- [ ] No increase after publication.
- [ ] No withdrawal restoration.
- [ ] No held/confirmed withdrawal.
- [ ] Freeze/close distinct from withdrawal.

## Appointment

- [ ] Search / View / Reschedule / Cancel present.
- [ ] Reschedule requires agreement and new seat first.
- [ ] Same ServiceOffering/same financial terms for in-place reschedule.
- [ ] No staff-created phone/walk-in Aafiatak booking.
- [ ] No arbitrary gateway overwrite.

## Check-in / Queue / Visit

- [ ] Patient cannot self-check-in.
- [ ] Check-in includes Visit + QueueEntry creation/activation.
- [ ] Queue ordering rules correct.
- [ ] Full payment gives no priority.
- [ ] Doctor does not change visit states.
- [ ] Erroneous check-in correction removes incorrect queue entry.
- [ ] No requeue/re-entry state.

## Late Arrival

- [ ] No automatic group transfer.
- [ ] Accepted late Patient remains original group.
- [ ] Manual handling is explicit.
- [ ] Existing Reschedule / No-show / Non-completion Use Cases are reused, not duplicated.

## Operational Exceptions

- [ ] All approved exception types represented.
- [ ] Doctor delay/absence recorded by facility staff, not Doctor.
- [ ] Session cancellation preserves history and requires resolution.
- [ ] Notification Service associated with Notify Affected Patients.
- [ ] Escalation exists.
- [ ] Exception cannot close before documented outcomes.
- [ ] No internal free capacity imported to resolve conflict.

## Visual

- [ ] Eight neighborhoods are understandable.
- [ ] Text is readable at normal report scale.
- [ ] No giant association bus dominates.
- [ ] External Actors are local to their interactions.
- [ ] No connector crosses labels/ellipses.
- [ ] Include relations are clearly readable.
- [ ] Diagram looks like a deliberate academic UML figure, not a dashboard or routing benchmark.

---

# 17. Nine-Pass Deep Review Record

## Review 1 — Lecturer / UML Method

Rechecked the lecturer PDF pages covering Use Case Diagram, package organization, and Use Case Modeling.

Confirmed:
- Actor / Use Case / Relationship first;
- packages organize large-operation sets;
- `include` is mandatory behavior;
- `extend` is conditional behavior;
- no chronological arrows;
- scenario/precondition/postcondition detail moves to Use Case Modeling;
- package-by-actor organization is explicitly demonstrated in the lecturer's restaurant example.

Result:
This deliverable remains a detailed Use Case Diagram organized through the Booking & Reception Staff package.

---

## Review 2 — Authoritative Role Permission Audit

Compared every proposed operation against the authoritative Booking & Reception Staff permission block.

Confirmed authority for:
- login;
- daily doctors/sessions/groups;
- capacity monitoring/withdraw/freeze/close;
- appointment search/reschedule/cancel;
- payment-state viewing;
- check-in;
- VisitInstance/queue operations;
- visit progress/no-show;
- delay/absence/session cancellation recording;
- late arrival;
- conflict resolution/escalation.

Confirmed prohibitions on:
- doctor creation;
- facility core data;
- price/policies;
- staff accounts;
- platform settings;
- clinical content;
- gateway overwrite;
- phone/walk-in Aafiatak booking creation.

---

## Review 3 — Authentication / External-Service Audit

Checked global authentication and notification-channel rules.

Findings:
- `Log In` requires WhatsApp OTP.
- earlier package inventory omitted the OTP helper.
- facility users receive system notifications.
- Notification Service is the general notification service.
- WhatsApp is authentication only.
- Payment Gateway must not become a direct Reception-control actor.

Corrections:
- added Verify WhatsApp OTP;
- added Receive Facility Notifications;
- associated Notification Service with Receive Facility Notifications and Notify Affected Patients.

---

## Review 4 — Capacity / Appointment / Payment Audit

Checked:
- AvailabilityRelease capacity accounting;
- irreversible CapacityWithdrawal;
- freeze/close lifecycle;
- active holds;
- appointment management;
- rescheduling rules;
- payment independence.

Finding:
Facility Appointment Management explicitly grants viewing active ReservationHolds, which was absent from the earlier package inventory.

Correction:
Added `View Active Reservation Holds`.

Confirmed:
- no published-capacity increase;
- no reverse withdrawal;
- no withdrawal of held/confirmed capacity;
- no direct Reception payment-result mutation;
- in-place rescheduling only under same ServiceOffering/financial terms.

---

## Review 5 — Check-in / Queue / Visit-State Audit

Checked service-day rules in detail.

Confirmed:
- check-in only against valid CONFIRMED Appointment;
- Patient cannot self-check-in;
- check-in creates/activates VisitInstance and QueueEntry;
- erroneous check-in correction is audited and removes QueueEntry;
- queue order is check-in time, then confirmed_at;
- full payment gives no priority;
- facility staff changes VisitInstance states;
- Doctor may call but not change VisitInstance state.

Result:
Approved four mandatory include relationships in this area:
- Check-in → Visit
- Check-in → QueueEntry
- Correct Check-in → Remove QueueEntry
- Accepted Late Arrival → Check-in

---

## Review 6 — Late-Arrival Audit

Checked the final accepted-late-patient rules.

Confirmed:
- no automatic transfer;
- no re-entry status;
- no automatic queue position;
- original group unchanged;
- manual-handling flag/mode;
- terminal NO_SHOW cannot be reopened.

Granularity finding:
Earlier package list duplicated Reschedule / No-show / Non-completion with late-specific names.

Correction:
Normalized these to the existing reusable Use Cases and preserved the late conditions as scenario contexts.

---

## Review 7 — Operational-Exception / Notification / Escalation Audit

Checked:
- supported exception types;
- session cancellation;
- conflict handling;
- affected-appointment resolution;
- patient notification;
- refund boundary;
- support escalation.

Granularity finding:
`Cancel Affected Appointment` duplicated the already-approved `Cancel Appointment` service.

Correction:
Reused `Cancel Appointment` for facility-responsible exception scenarios.

Confirmed:
- no direct gateway manipulation;
- no silent deletion;
- exception closure requires documented affected-appointment outcomes;
- conflict cannot be solved by importing internal free capacity.

---

## Review 8 — UML Relationship Audit

Tested every plausible relation against the lecturer's definitions.

Approved only:
1. Log In → Verify WhatsApp OTP
2. Register Patient Check-in → Create/Activate Visit
3. Register Patient Check-in → Create/Activate Queue Entry
4. Correct Erroneous Check-in → Remove Incorrect Queue Entry
5. Accept Late Arrival Manually → Register Patient Check-in

Rejected:
- daily-operation flow arrows;
- queue chronology;
- service-progress chronology;
- late-arrival outcome arrows;
- exception-resolution chronology;
- payment-view → gateway;
- artificial Actor Generalization.

Also determined that:
`Resolve Affected Appointments` before `Close Operational Exception`
is a **precondition**, not an `include`.

Result:
5 include, 0 extend, 0 generalization.

---

## Review 9 — Omission / Duplication / Cross-Package / Visual Audit

Compared this package against:
- Main Overview;
- Facility Administrator package;
- Doctor package;
- Platform Administrator package;
- Patient package;
- authoritative deferred scope.

Confirmed role separation:
- Reception handles daily operations.
- Facility Administrator owns configuration/staff/service/policy setup.
- Doctor has limited read-and-call role.
- Platform Administrator receives escalations/support but does not run daily queue.
- Patient does not self-check-in/reschedule.

Final normalized semantic set:

- Primary human Actor: **1**
- External Actors: **2**
- Use Cases: **43**
- Reception direct Associations: **42**
- Total Actor Associations: **45**
- `<<include>>`: **5**
- `<<extend>>`: **0**
- Generalization: **0**

No unresolved semantic contradiction blocks implementation.

---

# 18. Final Implementation Contract

The implementation agent must:

- use this file as execution truth;
- render exactly 43 approved Use Cases;
- preserve the exact Association Matrix;
- render exactly 5 approved `<<include>>`;
- add no `extend`, Generalization, or chronological arrows;
- keep all Actors outside the System Boundary;
- keep all Use Cases inside `Booking & Reception Staff Package`;
- preserve the normalization decisions in Section 11;
- preserve all Aafiatak restrictions and invariants;
- optimize visual composition without altering semantics;
- leave final visual approval to the user.

