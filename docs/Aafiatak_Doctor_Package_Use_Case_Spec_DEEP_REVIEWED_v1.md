# Aafiatak — Doctor Package Use Case Diagram Specification

## 0. Document Status

**Deliverable:** Actor Package Use Case Diagram  
**Actor package:** Doctor  
**System:** Aafiatak Medical Appointment Booking System  
**Language of visible diagram labels:** English  
**Status:** Deep-reviewed execution specification — ready for diagram implementation

This document defines the approved content and UML semantics for the **Doctor Package Use Case Diagram**.

It was rebuilt and reviewed against:

1. the authoritative `Aafiatak_Project_Specification_EN.md`;
2. the lecturer UML PDF and supplied lecturer-course rules;
3. the approved `docs/use_case.md` Use Case work structure;
4. the previously reviewed Actor Package conventions used for Aafiatak.

This is a detailed actor-oriented **Use Case Diagram organized through the Doctor package**.

It is **not**:
- the later formal UML Package Diagram;
- an Activity Diagram;
- a Sequence Diagram;
- a State Diagram;
- a Class Diagram;
- a UI/dashboard specification;
- a database model;
- an implementation/component diagram.

The Doctor role is intentionally narrow. Do not expand it merely to make the diagram look more “complete.”

---

# 1. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative product truth.
2. Lecturer UML PDF and supplied lecturer-course notes — academic UML method and notation.
3. `docs/use_case.md` — approved Use Case work structure and Doctor operation inventory.
4. This reviewed Doctor Package specification — execution truth for the Doctor Package after the review decisions documented below.
5. Rendering/layout tooling — presentation mechanics only.

Rules:

- Never invent a Doctor capability from common hospital/HIS behavior.
- Never add a feature merely because doctors commonly perform it in real clinics.
- If this file conflicts with the authoritative project specification, the project specification wins.
- Do not resolve open implementation/product decisions inside UML.
- Do not use previous diagrams as semantic truth.
- All visible labels must be English.
- Preserve the intentionally limited Doctor permission model.

---

# 2. Lecturer Rules Applied to This Diagram

The lecturer's Use Case method requires:

- Actors;
- Use Cases;
- valid Relationships;
- a clear System Boundary;
- package organization for large systems;
- later textual Use Case Modeling for detailed scenarios.

Mandatory notation:

- **Actor–Use Case Association:** solid plain line, no arrowhead.
- **`<<include>>`:** dashed dependency, direction **base use case → mandatory included use case**.
- **`<<extend>>`:** dashed dependency, direction **conditional extending use case → base use case**.
- **Generalization:** only when genuine inheritance is supported; do not invent it to reduce lines.
- Every visible Use Case name must begin with a verb.
- Do not use arrows to mean:
  - then;
  - next;
  - before;
  - after;
  - first/second/third.
- Preconditions, success/failure flows, exception flows, and postconditions belong to later **Use Case Modeling**.
- Do not place:
  - Classes;
  - Attributes;
  - database tables;
  - PostgreSQL;
  - APIs;
  - screens/pages;
  - buttons;
  - implementation components
  in a Use Case Diagram.

### Course package distinction

The lecturer uses packages to organize Use Cases for large systems, but the later formal **Package Diagram** remains a separate structural deliverable.

Therefore this Doctor deliverable is:

**a Use Case Diagram organized inside `Doctor Package`**

and may contain:
- Actors;
- Use Cases;
- Associations;
- justified `<<include>>` / `<<extend>>`.

It must not be evaluated as though it were the later formal Package Diagram.

### Granularity rule

The lecturer warns against both:
- shallow models with insufficient realistic detail; and
- excessive micro-detail.

The Doctor package is deliberately small because the approved Doctor role is deliberately limited. A small diagram is correct here; it must not be artificially enlarged.

---

# 3. Diagram Scope and Structure

## 3.1 Exact Diagram Title

**Doctor Package Use Case Diagram — Aafiatak Medical Appointment Booking System**

## 3.2 System Boundary

Draw one System Boundary titled:

**Aafiatak Medical Appointment Booking System**

All Actors remain outside the System Boundary.

## 3.3 Doctor Package

Inside the System Boundary, draw one UML package container titled:

**Doctor Package**

All Doctor Use Cases defined in this file belong inside that package.

Do not create nested UML packages merely for decoration.

The visual sections later in this file are presentation neighborhoods only.

## 3.4 Primary Human Actor

Exactly one primary human Actor:

- **Doctor**

Definition:
A provisioned facility user account linked to the corresponding Doctor profile, with a limited read-and-call operational interface.

Do not add:
- Facility Administrator;
- Booking & Reception Staff;
- Patient;
- Platform Administrator;
- Nurse;
- generic `User`;
- `Facility User`;
- `Medical Staff`
as additional human Actors in this package.

Other roles may interact with the same operational domain in their own Actor Package diagrams; that does not make them Actors in the Doctor Package view.

## 3.5 External Actor

Exactly one external Actor is required:

- **WhatsApp Authentication Provider**

It participates only in:

- **Verify WhatsApp OTP**

Do not add:
- Notification Service;
- Payment Gateway;
- Map Service;
- SMS Provider;
- Database/PostgreSQL;
- HIS/EHR;
- facility internal scheduling system.

The approved Doctor scope does not define a separate Doctor general-notification Use Case.

---

# 4. Deep-Review Correction to the Earlier Doctor Inventory

The preserved Doctor Package in `docs/use_case.md` contains:

- Log In
- View Today's Appointments
- View Upcoming Appointments
- View Doctor Arrival Groups
- View Waiting Patients
- Identify Next Patient
- Call Next Patient

This list is substantially correct.

However, one mandatory authentication helper is absent from that detailed list.

## 4.1 Added — Verify WhatsApp OTP

The authoritative authentication rules apply passwordless WhatsApp OTP to:

- Patient
- Facility Administrator
- Booking & Reception Staff
- Doctor
- Platform Administrator

Therefore the Doctor Package adds:

**DUC-02 — Verify WhatsApp OTP**

with:

**Log In `<<include>>` Verify WhatsApp OTP**

The Doctor has **no direct Association** to the helper Use Case; the external WhatsApp Authentication Provider directly participates in OTP verification.

No other Doctor capability was added.

---

# 5. Exact Doctor Package Use Cases

The reviewed Doctor Package contains exactly **8 Use Cases**.

IDs are traceability metadata and must not appear inside visible ellipses unless the lecturer explicitly requires IDs.

---

# 5.1 Authentication

## DUC-01 — Log In

**Primary Actor:** Doctor

Purpose:
Authenticate the already provisioned Doctor account and establish a valid Doctor-interface session.

Rules:

- Doctor role is not public self-registration.
- Doctor login access is provisioned by the Facility Administrator.
- The user account must be linked to the corresponding Doctor profile.
- Authentication is passwordless.
- Authentication uses a short-lived, single-use WhatsApp OTP.
- SMS is not used.
- No Password Use Case exists.
- No Forgot Password / Reset Password flow exists.
- Privileged access must cease when corresponding facility access is disabled/revoked according to the approved session rules.

---

## DUC-02 — Verify WhatsApp OTP

**External Actor:** WhatsApp Authentication Provider  
**Role:** Mandatory helper Use Case

Purpose:
Perform mandatory phone/authentication verification during Doctor login.

Rules:

- official approved WhatsApp authentication/provider integration only;
- short-lived, single-use OTP;
- no general-purpose WhatsApp notifications;
- no SMS;
- no direct Doctor Association to this helper Use Case.

---

# 5.2 Appointment Visibility

## DUC-03 — View Today's Appointments

**Primary Actor:** Doctor

Purpose:
View the Doctor's **own** Aafiatak appointments for the current day.

Rules:

- only appointments assigned to that Doctor within approved facility context;
- no access to other Doctors' appointments without separate administrative permission;
- no appointment cancellation/rescheduling capability is implied;
- no payment/refund manipulation is implied;
- no clinical-record access is implied.

This Use Case expands the Doctor's high-level ability to view assigned appointments.

---

## DUC-04 — View Upcoming Appointments

**Primary Actor:** Doctor

Purpose:
View the Doctor's **own upcoming** Aafiatak appointments.

Rules:

- own assigned Aafiatak appointments only;
- not the facility's complete internal schedule;
- no ability to modify the appointment;
- no ability to change availability.

`View Today's Appointments` and `View Upcoming Appointments` remain separate because both are explicitly preserved in the approved Doctor Package inventory and authoritative Doctor permissions.

Do not merge them merely to reduce the number of ellipses.

---

# 5.3 Arrival Groups & Waiting Queue

## DUC-05 — View Doctor Arrival Groups

**Primary Actor:** Doctor

Purpose:
View the Doctor's own Aafiatak Arrival Groups and their arrival windows relevant to the Doctor's assigned work.

Rules:

- Arrival Groups are Aafiatak arrival windows, not exact guaranteed doctor-entry times.
- This does not give the Doctor permission to:
  - create;
  - edit;
  - freeze;
  - close;
  - withdraw;
  - increase
  availability/capacity.
- It does not expose or control the facility's complete internal schedule.

---

## DUC-06 — View Waiting Patients

**Primary Actor:** Doctor

Purpose:
View checked-in and waiting Patients assigned to the Doctor through Aafiatak.

Rules:

- only relevant Patients assigned to the Doctor;
- lightweight Aafiatak queue context only;
- not the facility's complete internal queue;
- no unrelated Patient data;
- no clinical notes/diagnoses/test results;
- full-payment booking receives no queue priority.

The authoritative project states that the Doctor may view the same relevant waiting list used by facility operations but may not change visit states.

---

## DUC-07 — Identify Next Patient

**Primary Actor:** Doctor

Purpose:
Identify the next Patient according to the relevant Aafiatak waiting/queue context.

Interpretation:

- this is a Doctor-facing operational read/decision capability;
- it does not modify VisitInstance status;
- it does not alter queue ordering;
- it does not grant the Doctor a manual queue-reordering capability.

The approved queue ordering for normal on-time Patients remains:

1. actual check-in time;
2. earlier appointment `confirmed_at` as tie-breaker.

Full electronic payment gives no priority.

---

## DUC-08 — Call Next Patient

**Primary Actor:** Doctor

Purpose:
Call the next Patient from the Doctor's relevant Aafiatak waiting context.

Critical rule:

**Calling the next Patient does NOT change the VisitInstance to `IN_SERVICE`.**

Facility staff, not the Doctor, record:
- `IN_SERVICE`;
- `COMPLETED`;
- `NOT_COMPLETED`;
- `NO_SHOW`.

The Doctor may call but does not own the visit-state lifecycle.

---

# 6. Exact Actor–Use Case Association Matrix

This matrix is authoritative.

## Doctor

Associate Doctor directly with:

- DUC-01 Log In
- DUC-03 View Today's Appointments
- DUC-04 View Upcoming Appointments
- DUC-05 View Doctor Arrival Groups
- DUC-06 View Waiting Patients
- DUC-07 Identify Next Patient
- DUC-08 Call Next Patient

Do **not** directly associate Doctor with:

- DUC-02 Verify WhatsApp OTP

Reason:
OTP verification is a mandatory helper inside Login, not an independent Doctor goal.

Therefore:

**Doctor direct Associations = 7**

## WhatsApp Authentication Provider

Associate only with:

- DUC-02 Verify WhatsApp OTP

Therefore:

**WhatsApp Authentication Provider Associations = 1**

## Total

**Total Actor Associations = 8**

No other Actor Association is approved.

---

# 7. Exact UML Relationships

Use exactly **1 `<<include>>` relationship**.

There are:

- **0 `<<extend>>`**
- **0 Generalization**

## DINC-01

**Log In** `<<include>>` **Verify WhatsApp OTP**

Direction:

`DUC-01 → DUC-02`

Reason:
Every Doctor authentication execution requires successful WhatsApp OTP verification.

---

# 8. Relationships Deliberately NOT Added

The following relationships were explicitly reviewed and rejected.

## 8.1 No `View Waiting Patients → Identify Next Patient`

Do not draw an arrow.

Reason:
The Doctor may view waiting Patients and may identify the next Patient, but drawing an arrow would risk representing workflow/navigation rather than an explicitly established mandatory UML dependency.

The detailed relationship belongs in later Use Case Modeling / Sequence / Activity work where appropriate.

## 8.2 No `Identify Next Patient → Call Next Patient`

Do not draw a chronological arrow.

Do not create `<<include>>` merely because identifying normally precedes calling.

The authoritative source lists them as separate Doctor capabilities. It does not explicitly define one as a reusable mandatory included Use Case of the other.

Preserve them as separate Actor-associated Use Cases.

## 8.3 No appointment progression arrows

Do not draw:

- View Today's Appointments → View Waiting Patients
- View Waiting Patients → Identify Next Patient
- Identify Next Patient → Call Next Patient
- Call Next Patient → Start Service
- Call Next Patient → Complete Visit

The last two operations are not Doctor permissions at all.

## 8.4 No notification relationship

Do not connect Doctor to Notification Service.

The Main Overview's high-level notification Actor associations do not include Doctor, and the authoritative Doctor permissions do not define a separate Doctor notification-delivery goal.

## 8.5 No Actor Generalization

Do not model:

- Doctor → Facility User
- Doctor → User
- Doctor → Booking & Reception Staff
- Doctor → Patient

A single real person may hold more than one approved role/profile, but that identity fact does not establish UML Actor inheritance between these operational roles.

---

# 9. Traceability to Main Overview

The Doctor Package expands the following Main Overview goals.

## `MUC-04 — Log In`

Detailed Doctor Use Cases:

- DUC-01 Log In
- DUC-02 Verify WhatsApp OTP

## `MUC-25 — View Assigned Appointments & Queue`

Detailed Doctor Use Cases:

- DUC-03 View Today's Appointments
- DUC-04 View Upcoming Appointments
- DUC-05 View Doctor Arrival Groups
- DUC-06 View Waiting Patients
- DUC-07 Identify Next Patient

## `MUC-26 — Call Next Patient`

Detailed Doctor Use Case:

- DUC-08 Call Next Patient

The package must not expand MUC-25/MUC-26 into facility-staff responsibilities.

---

# 10. Explicit Doctor Restrictions

The Doctor Package must NOT contain or imply any of the following:

- Register Patient
- Manage Patient Profile
- Book Appointment
- Cancel Appointment
- Reschedule Appointment
- Register Patient Check-in
- Create/Activate Visit
- Create/Activate Queue Entry
- Correct Check-in
- Remove Queue Entry
- Reorder Queue
- Change queue priority
- Record Service Start
- change VisitInstance to `IN_SERVICE`
- Complete Visit
- Record Visit Non-completion
- Record No-show
- Record Doctor Delay
- Record Doctor Absence
- Cancel Session
- Record Operational Exception
- Manage Operational Exception
- Notify Affected Patients as a facility-staff action
- Manage Capacity
- Withdraw Capacity
- Freeze Availability
- Close Availability
- Increase Published Capacity
- Restore Withdrawn Capacity
- Manage Doctor Schedules
- Create Availability Release
- Configure Arrival Groups
- change services
- change service prices
- change booking/payment/refund policies
- change payment results
- execute refunds
- Payment Gateway operations
- employee-account management
- platform settings
- facility-core-data management
- diagnosis
- prescriptions
- test results
- clinical notes
- medical records
- cashier/accounting/full medical invoicing
- SMS authentication
- Password
- Forgot Password
- Reset Password
- general WhatsApp notifications.

If the Doctor is delayed or absent:

**the Doctor contacts reception/facility management outside the Doctor system workflow; facility staff record the OperationalException.**

Do not create:
- `Report Delay`
- `Report Absence`
as Doctor Use Cases.

---

# 11. Critical Domain Rules Relevant to the Doctor View

These rules govern interpretation of the Doctor's read-and-call capabilities.

## 11.1 Doctor sees only the Doctor's assigned Aafiatak context

The Doctor may view:
- own today appointments;
- own upcoming appointments;
- own Arrival Groups/windows;
- checked-in/waiting Patients assigned to that Doctor.

No broad facility-wide administrative access is implied.

## 11.2 Aafiatak is not the facility's full queue

The Doctor sees the relevant Aafiatak waiting list only.

Aafiatak does not claim to know or merge the facility's complete internal queue.

## 11.3 Queue ordering

For normal on-time Patients inside one Arrival Group:

1. actual check-in time;
2. earlier appointment confirmation time when check-in time ties.

Payment policy does not change priority.

## 11.4 Doctor may call, but facility staff control visit states

Doctor:
- can identify next Patient;
- can call next Patient.

Doctor cannot set:
- `IN_SERVICE`;
- `COMPLETED`;
- `NOT_COMPLETED`;
- `NO_SHOW`.

This separation is mandatory.

## 11.5 No clinical scope

The Doctor interface does not become an EHR/clinical workflow.

It does not contain:
- diagnosis;
- prescriptions;
- test results;
- clinical notes.

---

# 12. Granularity Decisions

Potential additions/merges were reviewed.

## 12.1 Keep `View Today's Appointments` and `View Upcoming Appointments` separate

Both are explicitly listed in the authoritative Doctor permission set and approved detailed package inventory.

Therefore they remain two Use Cases.

## 12.2 No separate `View Checked-in Patients`

The authoritative role wording says the Doctor may view checked-in and waiting Patients, while the approved detailed package inventory models this as:

**View Waiting Patients**

This Use Case is defined here to cover the relevant checked-in/waiting Aafiatak list.

Creating another nearly identical ellipse would introduce unnecessary duplication.

## 12.3 No separate `View Arrival Group Windows`

Already represented by:

**View Doctor Arrival Groups**

Its definition explicitly includes the Doctor's own Arrival Groups and windows.

## 12.4 No separate `View Next Patient`

Already represented by:

**Identify Next Patient**

## 12.5 No `Start Visit`

Explicitly forbidden for Doctor.

Facility staff record service start.

## 12.6 No `Report Doctor Delay` / `Report Doctor Absence`

Explicitly forbidden as Doctor in-system operations.

## 12.7 No Doctor notification Use Case

Not explicitly established by the authoritative Doctor scope/Main Overview actor matrix.

Do not add one merely because notifications exist elsewhere in the system.

## 12.8 No Doctor `Log Out`

Unlike the Patient Application scope, the authoritative Doctor/facility-dashboard scope does not explicitly define a standalone user-initiated Doctor logout operation.

Do not invent it as a separate current-scope Use Case.

---

# 13. Visual Composition Requirements

This package is small and should fit comfortably on **one landscape sheet**.

Do not split it into multiple sheets.

Recommended visual neighborhoods:

1. **Authentication**
   - Log In
   - Verify WhatsApp OTP

2. **Appointments**
   - View Today's Appointments
   - View Upcoming Appointments

3. **Arrival Groups & Queue**
   - View Doctor Arrival Groups
   - View Waiting Patients
   - Identify Next Patient
   - Call Next Patient

These are visual neighborhoods only.

Do not create nested UML packages for them.

Recommended Actor placement:

- **Doctor:** outside left, vertically centered near Appointments / Queue.
- **WhatsApp Authentication Provider:** outside near Verify WhatsApp OTP.

Composition rules:

- one rational landscape artboard;
- readable report-scale typography;
- consistent ellipse sizes;
- balanced whitespace;
- short local connectors;
- keep the single `<<include>>` local and obvious;
- no connector through labels;
- no giant empty canvas;
- no decorative clutter;
- no graph-algorithm appearance;
- no fake relationship arrows between queue operations.

Because the Doctor has only 7 direct Associations, one Doctor actor symbol should normally be sufficient. Do not duplicate the Doctor actor unless a genuine readability problem remains.

---

# 14. Final QA Checklist

## UML compliance

- [ ] Correct diagram title.
- [ ] Correct System Boundary title.
- [ ] Doctor outside System Boundary.
- [ ] WhatsApp Authentication Provider outside System Boundary.
- [ ] Doctor Package inside System Boundary.
- [ ] Exactly 8 Use Cases inside Doctor Package.
- [ ] All visible labels are English.
- [ ] Every Use Case name begins with a verb.
- [ ] Doctor has exactly 7 direct Associations.
- [ ] WhatsApp Authentication Provider has exactly 1 Association.
- [ ] Doctor has no direct Association to Verify WhatsApp OTP.
- [ ] Actor Associations are solid lines without arrowheads.
- [ ] Exactly 1 `<<include>>`.
- [ ] Include direction is Log In → Verify WhatsApp OTP.
- [ ] 0 `<<extend>>`.
- [ ] 0 Generalization.
- [ ] No chronological arrows.
- [ ] No Classes/database/components/UI controls.

## Product compliance

- [ ] Doctor account is provisioned, not publicly self-registered.
- [ ] Login is passwordless WhatsApp OTP.
- [ ] SMS/password recovery are absent.
- [ ] View Today's own Aafiatak Appointments is present.
- [ ] View Upcoming own Aafiatak Appointments is present.
- [ ] View Doctor Arrival Groups/windows is present.
- [ ] View relevant checked-in/waiting Patients is represented.
- [ ] Identify Next Patient is present.
- [ ] Call Next Patient is present.
- [ ] No access to other Doctors' appointments is implied.
- [ ] Doctor cannot alter availability/capacity.
- [ ] Doctor cannot reschedule/cancel appointments.
- [ ] Doctor cannot check in Patients.
- [ ] Doctor cannot change VisitInstance states.
- [ ] Doctor cannot record no-show/non-completion.
- [ ] Doctor cannot report delay/absence in-system.
- [ ] Doctor cannot modify service/price/policies.
- [ ] Doctor cannot modify payment/refund states.
- [ ] No clinical content is present.
- [ ] No platform/staff administration is present.
- [ ] Aafiatak queue is not represented as the facility's complete internal queue.
- [ ] Full payment does not create priority.

## Visual compliance

- [ ] One sheet only.
- [ ] Three visual neighborhoods are immediately understandable.
- [ ] WhatsApp provider is local to OTP.
- [ ] No long connector buses.
- [ ] No lines cross labels.
- [ ] No fake workflow arrows.
- [ ] Typography remains readable at normal viewing scale.
- [ ] Diagram looks deliberately composed and academically clean.

---

# 15. Nine-Pass Deep Review Record

## Review 1 — Lecturer / UML Method Audit

Rechecked the lecturer's Use Case and package-method material.

Confirmed:
- Actor + Use Case + Relationship are the core diagram elements;
- packages organize large systems;
- `include` is for mandatory included behavior;
- `extend` is for conditional extension;
- chronological steps do not belong in Use Case relationships;
- detailed scenarios/preconditions/postconditions move to Use Case Modeling;
- the Actor Package Use Case view remains distinct from the later formal Package Diagram.

Result:
The Doctor Package structure is academically consistent with the lecturer's method.

---

## Review 2 — Authoritative Doctor Permission Audit

Rechecked the root project specification's Doctor role.

Confirmed Doctor may:
- log in;
- view own upcoming Aafiatak appointments;
- view today's own Aafiatak appointments;
- view own Arrival Groups/windows;
- view assigned checked-in/waiting Patients;
- identify next Patient;
- call next Patient.

Confirmed Doctor may not:
- change visit states;
- record no-show/non-completion;
- report delay/absence;
- alter services/prices/availability/policies/payment;
- execute refunds;
- use clinical content;
- manage staff/platform settings.

Result:
The approved Doctor operation inventory matches the authoritative role boundary.

---

## Review 3 — Authentication & Identity Audit

Rechecked global identity/authentication rules.

Confirmed:
- Doctor authentication is passwordless;
- WhatsApp OTP is mandatory;
- SMS is absent;
- Doctor role is provisioned, not public self-registration;
- Doctor account links to Doctor profile;
- privileged session/access revocation applies.

Finding:
The earlier Doctor Package inventory omitted the mandatory OTP helper.

Correction:
Added `Verify WhatsApp OTP` and one `Log In <<include>> Verify WhatsApp OTP`.

---

## Review 4 — Appointment Visibility Audit

Compared:
- `View Today's Appointments`;
- `View Upcoming Appointments`;
- Main Overview `View Assigned Appointments & Queue`;
- Doctor access restrictions.

Confirmed:
- both appointment views are explicit and legitimate;
- both are restricted to the Doctor's own Aafiatak appointments;
- neither grants appointment modification rights;
- they should not be merged merely for diagram compactness.

Result:
Both Use Cases retained.

---

## Review 5 — Arrival Group / Queue Audit

Rechecked the lightweight queue rules.

Confirmed:
- Doctor can view own Arrival Groups/windows;
- Doctor can view relevant checked-in/waiting list;
- Doctor can identify next Patient;
- Doctor can call next Patient;
- normal queue ordering is by actual check-in time, then confirmed_at tie-break;
- payment gives no priority;
- Aafiatak does not represent the facility's full queue.

Granularity finding:
A separate `View Checked-in Patients` would duplicate the approved `View Waiting Patients` scope.

Decision:
Keep one `View Waiting Patients` Use Case, explicitly defined to include relevant checked-in/waiting Patients.

---

## Review 6 — Visit-State / Operational Exception Audit

Rechecked `VisitInstance`, QueueEntry, service-day operation, and exception responsibilities.

Confirmed:
- facility staff, not Doctor, change visit states;
- Doctor calling next Patient does not mean `IN_SERVICE`;
- Doctor does not complete/non-complete/no-show a visit;
- Doctor does not record delay or absence;
- delay/absence is communicated outside the Doctor interface to facility/reception staff, who record the OperationalException.

Result:
No visit-state or exception-recording Use Cases were added to Doctor Package.

---

## Review 7 — External Actor / Notification / Deferred-Scope Audit

Reviewed all external services and deferred features.

Confirmed:
- WhatsApp Authentication Provider directly participates in OTP verification.
- Payment Gateway does not directly participate in any Doctor Use Case.
- Map Service does not directly participate.
- Notification Service is not explicitly required for a separate Doctor Use Case.
- SMS is out.
- clinical/EHR content is out.
- payment/refund management is out.

Result:
Exactly one external Actor: WhatsApp Authentication Provider.

---

## Review 8 — UML Relationship Audit

Tested plausible relationships against strict lecturer semantics.

Approved only:
- `Log In <<include>> Verify WhatsApp OTP`

Rejected:
- View Waiting Patients → Identify Next Patient
- Identify Next Patient → Call Next Patient
- View Appointments → Queue
- Call Next Patient → Start Service
- any `extend`
- any Actor Generalization

Reason:
These are either workflow/chronology, not explicitly established reusable mandatory behaviors, or outside Doctor permission scope.

Result:
1 include, 0 extend, 0 Generalization.

---

## Review 9 — Omission / Granularity / Cross-Package / Visual Audit

Compared Doctor Package against:
- Main Overview;
- Booking & Reception Staff Package;
- Facility Administrator Package;
- Patient Package;
- authoritative role restrictions;
- lecturer's granularity guidance.

Checked possible omissions:
- Verify WhatsApp OTP → added;
- Doctor notifications → not explicitly supported as standalone Doctor goal;
- Log Out → not explicitly defined for Doctor;
- View Checked-in Patients → already covered by View Waiting Patients;
- Start Service → explicitly belongs to facility staff;
- Report Delay/Absence → explicitly excluded;
- payment/refund → excluded;
- clinical content → excluded.

Cross-package separation is correct:
- Doctor = read own work + identify/call.
- Reception = check-in + queue management + visit-state updates + exception recording.
- Facility Administrator = configuration/availability/staff administration.
- Platform Administrator = platform administration/support.
- Patient = own booking/appointment/queue visibility.

Final semantic result:

- Primary human Actor: **1**
- External Actors: **1**
- Use Cases: **8**
- Doctor direct Associations: **7**
- Total Actor Associations: **8**
- `<<include>>`: **1**
- `<<extend>>`: **0**
- Generalization: **0**

No unresolved semantic contradiction blocks implementation.

---

# 16. Final Implementation Contract

The implementation agent must:

- use this file as the execution truth for the Doctor Package;
- render exactly the 8 approved Use Cases;
- preserve exactly the Actor Association Matrix;
- render exactly one approved `<<include>>`;
- add no `<<extend>>`, Generalization, or chronological arrows;
- keep both Actors outside the System Boundary;
- keep all Use Cases inside `Doctor Package`;
- preserve the Doctor's deliberately restricted role;
- keep all visible labels English;
- use one clean landscape sheet;
- optimize visual composition without changing semantics;
- leave final visual approval to the user.

