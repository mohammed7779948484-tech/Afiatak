# Aafiatak — Facility Administrator Package Use Case Diagram Specification

## 0. Document Status

**Deliverable:** Actor Package Use Case Diagram  
**Actor package:** Facility Administrator  
**System:** Aafiatak Medical Appointment Booking System  
**Language of visible diagram labels:** English  
**Status:** Reviewed execution specification — ready for diagram implementation

This document defines the approved content and UML semantics for the **Facility Administrator Package Use Case Diagram**.

It is a detailed actor-oriented Use Case view created after the Main Use Case Diagram so that Facility Administrator operations can be represented without overloading the system overview.

This file is a modeling/drawing specification. It is not a UI specification, Activity Diagram, Sequence Diagram, Class Diagram, database model, implementation architecture, or the later formal UML Package Diagram.

**Important course distinction:** the lecturer uses Packages during Use Case analysis to organize large systems by actor/functional responsibility. This deliverable is therefore a **Use Case Diagram organized through the Facility Administrator package**. It still uses normal Use Case notation: Actors, Associations, and only evidence-supported `<<include>>` / `<<extend>>` relationships. The later formal Package Diagram remains a separate structural deliverable.

---

# 1. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative product truth.
2. Lecturer UML PDF and supplied lecturer-course notes — academic UML method and notation.
3. `docs/use_case.md` — approved Use Case work structure and preserved Facility Administrator package inventory.
4. This Facility Administrator Package specification — reviewed execution truth for this diagram.
5. Rendering/layout tooling — presentation mechanics only.

Rules:

- Do not invent product behavior from general UML knowledge.
- Do not add common hospital/HIS functions merely because they exist in real facilities.
- If this file conflicts with the authoritative project specification, the project specification wins.
- Do not use an old Aafiatak diagram as semantic truth.
- Visible diagram labels must be English.
- Open implementation/product decisions must remain open; do not resolve them inside UML.

---

# 2. Lecturer Rules Applied to This Diagram

The lecturer's Use Case method requires:

- Actors;
- Use Cases;
- valid Relationships;
- clear system/context boundary;
- package organization when a system contains many operations;
- later textual Use Case Modeling for scenario detail.

Mandatory notation:

- Actor–Use Case Association: **solid plain line**, no arrowhead.
- `<<include>>`: **dashed dependency**, direction **base → mandatory included Use Case**.
- `<<extend>>`: **dashed dependency**, direction **conditional extending Use Case → base Use Case**.
- Generalization only when a genuine inheritance relation is justified.
- Use Case names begin with verbs.
- Use Case Diagram does **not** show chronological execution.
- Detailed success/failure flows, preconditions, postconditions, and step order belong to later Use Case Modeling.
- Do not place Classes, Attributes, PostgreSQL/database tables, components, APIs, UI screens, or buttons in this diagram.

The lecturer also warns against:

- shallow systems with too little realistic detail;
- excessive micro-detail that turns UI actions into meaningless Use Cases.

The Facility Administrator package therefore preserves meaningful administration goals from the approved project scope without modeling screen-level actions.

---

# 3. Diagram Scope and Structure

## 3.1 Exact diagram title

**Facility Administrator Package Use Case Diagram — Aafiatak Medical Appointment Booking System**

## 3.2 System Boundary

Draw one System Boundary titled:

**Aafiatak Medical Appointment Booking System**

All Actors remain outside the System Boundary.

## 3.3 Facility Administrator Package

Inside the System Boundary, draw one UML package container titled:

**Facility Administrator Package**

All Use Cases defined by this specification belong inside that package.

Functional sections below are organization aids only. Do not create nested UML packages unless explicitly approved later. Prefer whitespace, headings, and restrained visual grouping.

## 3.4 Primary human Actor

Exactly one primary human Actor:

- **Facility Administrator**

Definition:
The highest-privilege user inside one participating facility's Aafiatak account.

Do not add:

- Booking & Reception Staff as a co-primary actor;
- Doctor as a co-primary actor;
- Platform Administrator as a co-primary actor;
- generic `User`;
- `Facility User`;
- `Manager`;
- `FacilityApplicant`.

Shared operations may also exist in other actor-package diagrams, but this package is specifically the Facility Administrator view.

## 3.5 External Actors

Use exactly these external Actors where they directly participate:

- **WhatsApp Authentication Provider**
- **Notification Service**

Do not add:

- Payment Gateway;
- Map Service;
- Database/PostgreSQL;
- HIS/EHR;
- facility internal scheduling system;
- SMS Provider;
- Cashier;
- Laboratory/Pharmacy systems.

The Facility Administrator may view payment states, but does not directly control Payment Gateway outcomes; therefore Payment Gateway is not a direct Actor in this package.

---

# 4. Review Findings Added from Authoritative Sources

The preserved Facility Administrator list in `docs/use_case.md` contains the detailed facility-management inventory, but two role-level capabilities required by the authoritative sources were missing from that package list.

## 4.1 Added: Log In

The authoritative Facility Administrator permissions explicitly state that the role may:

**Log in to the facility dashboard.**

The Main Overview also associates Facility Administrator with `MUC-04 — Log In`.

Therefore this package adds:

**FAUC-01 — Log In**

## 4.2 Added helper: Verify WhatsApp OTP

All human-role authentication, including Facility Administrator, is passwordless and requires short-lived single-use WhatsApp OTP verification through the official WhatsApp authentication provider.

Therefore:

**FAUC-01 Log In `<<include>>` FAUC-02 Verify WhatsApp OTP**

The Facility Administrator does not receive a separate direct Association to this helper Use Case.

## 4.3 Added: Receive Facility Notifications

The Main Overview associates Facility Administrator with high-level notification delivery, and the authoritative project specification explicitly defines notifications to facility users for bookings, cancellations, payment-review cases, check-in, stale/exhausted availability, and unresolved operational exceptions.

Therefore this package adds:

**FAUC-38 — Receive Facility Notifications**

with direct participation by:

- Facility Administrator
- Notification Service

These additions restore explicit role capabilities; they do not invent new product features.

No `Log Out` Use Case is added because, unlike the Patient Application scope, the authoritative Facility Administrator scope does not explicitly define a user-initiated logout operation as a separate current-scope capability.

---

# 5. Exact Facility Administrator Package Use Cases

The package contains exactly **38 Use Cases**.

IDs are traceability metadata. Do not display `FAUC-xx` inside ellipses unless the lecturer explicitly requires IDs.

---

# 5.1 Authentication

## FAUC-01 — Log In

**Primary Actor:** Facility Administrator

Purpose:
Authenticate the already provisioned Facility Administrator and establish a valid facility-dashboard session.

Rules:

- Passwordless authentication.
- WhatsApp OTP only.
- No SMS.
- No password.
- No Forgot Password / Reset Password.
- Facility Administrator role is not publicly self-assigned.
- A disabled/suspended privilege context must not retain an active privileged session.

---

## FAUC-02 — Verify WhatsApp OTP

**External Actor:** WhatsApp Authentication Provider  
**Role:** Helper Use Case

Purpose:
Perform the mandatory OTP verification for Facility Administrator authentication.

Rules:

- official approved WhatsApp authentication/provider integration;
- short-lived, single-use OTP;
- not general WhatsApp messaging;
- no direct Facility Administrator Association to this helper.

---

# 5.2 Facility Configuration

## FAUC-03 — Manage Facility Data

**Primary Actor:** Facility Administrator

Purpose:
Maintain approved facility-level public/operational information belonging to the Administrator's own facility.

Boundary:
This does not authorize management of another facility or platform-wide reference data.

---

## FAUC-04 — Manage Branch Display & Contact Data

**Primary Actor:** Facility Administrator

Purpose:
Maintain the pilot branch's approved display/contact/location data such as:

- address;
- map location;
- contact details;
- working hours;
- other approved branch-facing information.

The pilot currently has one facility and one branch, while architecture may support more later.

---

## FAUC-05 — Manage Facility Images & Logo

**Primary Actor:** Facility Administrator

Purpose:
Maintain the facility's approved public images/logo.

Do not interpret this as general media/CMS management.

---

## FAUC-06 — Associate Departments

**Primary Actor:** Facility Administrator

Purpose:
Associate applicable departments from platform-maintained public reference lists with the facility.

The Facility Administrator does not create or modify platform-wide reference catalogs through this Use Case.

---

## FAUC-07 — Associate Specialties

**Primary Actor:** Facility Administrator

Purpose:
Associate applicable specialties from platform-maintained reference lists with the facility/doctors as approved.

The Facility Administrator does not administer the platform's global specialty catalog.

---

# 5.3 Doctors & Services

## FAUC-08 — Add Doctor

**Primary Actor:** Facility Administrator

Purpose:
Add an approved Doctor profile for the facility context.

This creates/manages facility-side doctor information, not the Doctor's authenticated login access.

---

## FAUC-09 — Edit Doctor

**Primary Actor:** Facility Administrator

Purpose:
Edit approved Doctor information within the facility context.

Do not add clinical records or medical notes.

---

## FAUC-10 — Add Service Offering

**Primary Actor:** Facility Administrator

Purpose:
Create a facility/branch `ServiceOffering` that may be booked through Aafiatak.

The `ServiceOffering` represents the actual bookable offering, not a full hospital billing item.

---

## FAUC-11 — Edit Service Offering

**Primary Actor:** Facility Administrator

Purpose:
Edit allowed current ServiceOffering configuration for future applicable use.

Published releases and confirmed appointments preserve their own snapshotted governing terms and must not be silently rewritten by later parent edits.

---

## FAUC-12 — Set Service Price

**Primary Actor:** Facility Administrator

Purpose:
Set the full service/booking amount for the ServiceOffering in the pilot facility's configured currency.

Rules:

- no partial amount;
- no remaining-balance model;
- no currency conversion;
- later changes do not rewrite published-release/appointment snapshots.

---

## FAUC-13 — Set Estimated Service Duration

**Primary Actor:** Facility Administrator

Purpose:
Set the optional estimated service duration shown for patient information.

Rule:
This is informational only; it does not create an exact appointment slot or queue priority.

---

## FAUC-14 — Set Attendance Instructions

**Primary Actor:** Facility Administrator

Purpose:
Configure approved patient-facing attendance/arrival instructions associated with the ServiceOffering.

---

# 5.4 Policies

## FAUC-15 — Set Booking Policy

**Primary Actor:** Facility Administrator

Purpose:
Set the ServiceOffering booking policy.

Exactly two values are supported:

- `FULL_PAYMENT_REQUIRED`
- `PAY_AT_FACILITY`

Rules:

- Patient cannot choose the policy.
- No deposit policy.
- No partial-payment policy.
- No manual approval policy.

---

## FAUC-16 — Set Cancellation/Refund Policy

**Primary Actor:** Facility Administrator

Purpose:
Configure the approved patient-cancellation/refund policy for fully paid bookings.

Supported behavior is full refund or zero according to saved rules; no percentage-based partial-refund engine exists.

---

## FAUC-17 — Set No-show Policy

**Primary Actor:** Facility Administrator

Purpose:
Configure the no-show financial policy for fully paid bookings.

Approved values:

- `NO_SHOW_NON_REFUNDABLE`
- `NO_SHOW_FULL_REFUND`

No partial no-show refund is supported.

---

## FAUC-18 — Configure Attendance Reconfirmation

**Primary Actor:** Facility Administrator

Purpose:
Configure whether attendance reconfirmation is enabled.

Important:
The exact send timing remains an open parameter and must not be invented in this diagram.

Failure by a Patient to reconfirm does not automatically cancel the appointment.

---

# 5.5 Schedules & Digital Availability

## FAUC-19 — Manage Doctor Schedules

**Primary Actor:** Facility Administrator

Purpose:
Define/manage theoretical/basic Doctor schedule windows used in Aafiatak availability planning.

Aafiatak does not become the facility's full internal calendar.

---

## FAUC-20 — Record Planned Schedule Exception

**Primary Actor:** Facility Administrator

Purpose:
Record approved planned schedule exceptions such as planned leave/closure before affected availability is published.

Do not confuse planned schedule exceptions with later unplanned `OperationalException` handling.

---

## FAUC-21 — Create Availability Release

**Primary Actor:** Facility Administrator

Purpose:
Create an Aafiatak `AvailabilityRelease` for a specific doctor/service/branch/date/session.

It defines the bounded digital inventory assigned to Aafiatak rather than the facility's complete schedule.

---

## FAUC-22 — Configure Arrival Groups

**Primary Actor:** Facility Administrator

Purpose:
Define Arrival Groups inside the Aafiatak reception period, including approved window sequencing and capacity allocation.

Rules:

- groups are configured before publication;
- group capacities sum to the release's published digital capacity;
- groups are arrival windows, not guaranteed service-entry times.

---

## FAUC-23 — Set Initial Digital Capacity

**Primary Actor:** Facility Administrator

Purpose:
Set the initial digital capacity allocated to Aafiatak before publication.

Rule:
After publication, `published` becomes the upper bound and cannot be increased.

---

## FAUC-24 — Publish Availability

**Primary Actor:** Facility Administrator

Purpose:
Publish the prepared AvailabilityRelease for new booking attempts.

At publication, applicable commercial/booking terms become frozen for that release.

Do not add an invented manual-approval step.

---

## FAUC-25 — View Capacity Status

**Primary Actor:** Facility Administrator

Purpose:
View the operational Aafiatak capacity state, including where applicable:

- published;
- held;
- confirmed;
- withdrawn to facility;
- remaining;
- exhausted indicator;
- stale indicator;
- per-group values.

This is Aafiatak digital capacity only.

---

## FAUC-26 — Withdraw Remaining Capacity

**Primary Actor:** Facility Administrator

Purpose:
Irreversibly transfer valid unused Aafiatak capacity to the facility's internal schedule through the approved `CapacityWithdrawal` mechanism.

Rules:

- one or more remaining units may be withdrawn;
- active held capacity cannot be withdrawn;
- confirmed capacity cannot be withdrawn;
- withdrawn capacity cannot return to the same release;
- operation must not increase capacity elsewhere in Aafiatak;
- no `+1` capacity shortcut.

---

## FAUC-27 — Freeze Availability

**Primary Actor:** Facility Administrator

Purpose:
Temporarily stop new holds/bookings for an approved release/group while preserving valid existing holds and confirmed appointments according to product rules.

Freeze is not the same as irreversible withdrawal.

---

## FAUC-28 — Close Availability

**Primary Actor:** Facility Administrator

Purpose:
Close an approved release/group for new holds/bookings when operationally required.

Closed/cancelled semantics must not be silently reversed into a new bookable state.

---

# 5.6 Facility Staff Administration

## FAUC-29 — Add Facility Staff Account

**Primary Actor:** Facility Administrator

Purpose:
Provision an approved facility staff identity/context for the Administrator's own facility.

Facility roles are not publicly self-assigned.

---

## FAUC-30 — Disable Facility Staff Account

**Primary Actor:** Facility Administrator

Purpose:
Disable facility staff access when required.

Privileged sessions must be invalidated according to the approved authentication/access rules.

Do not hard-delete historical activity that requires audit traceability.

---

## FAUC-31 — Assign Approved Role

**Primary Actor:** Facility Administrator

Purpose:
Assign only approved facility role/permission context within the defined RBAC model.

Do not create an arbitrary custom permission designer.

Do not assign platform-wide roles through this Use Case.

---

## FAUC-32 — Provision Doctor Login Access

**Primary Actor:** Facility Administrator

Purpose:
Provision/enable Doctor login access linked to the corresponding Doctor profile.

This is distinct from `Add Doctor` / `Edit Doctor`.

The Doctor account remains subject to the restricted Doctor permission model.

---

# 5.7 Operations & Oversight

## FAUC-33 — Review Daily Operations

**Primary Actor:** Facility Administrator

Purpose:
Review facility-level Aafiatak daily operational status, including relevant doctors/sessions, arrivals, capacity, appointments, payment-review indicators, and open operational exceptions.

The Today Pulse Board is a UI implementation supporting this goal; **do not name the screen itself as a Use Case**.

---

## FAUC-34 — View Aafiatak Appointments

**Primary Actor:** Facility Administrator

Purpose:
View Aafiatak appointments belonging to the Administrator's own facility for authorized operational oversight.

Do not expose unrelated Patient information or another facility's data.

---

## FAUC-35 — View Payment Status

**Primary Actor:** Facility Administrator

Purpose:
View independent payment states related to the facility's Aafiatak bookings.

Rules:

- Payment state remains separate from Appointment state.
- Facility Administrator cannot arbitrarily overwrite Payment Gateway outcomes.
- `PAY_AT_FACILITY` has no `PaymentIntent`.

Payment Gateway is not directly associated with this viewing Use Case.

---

## FAUC-36 — Manage Operational Exceptions

**Primary Actor:** Facility Administrator

Purpose:
Manage approved operational exceptions affecting the facility's Aafiatak operation and ensure documented resolution of affected appointments.

Examples may include:

- doctor delay;
- doctor absence;
- session cancellation;
- facility closure;
- capacity reduction;
- power/connectivity outage;
- booking conflict.

Important:
Detailed day-to-day exception-recording/resolution actions are decomposed more deeply in the Booking & Reception Staff package. Do not duplicate every Reception micro-operation here unless the authoritative scope later requires it.

Facility cancellation/conflict may cause a full refund according to approved financial rules, but this does not authorize arbitrary direct manipulation of Payment Gateway results.

---

## FAUC-37 — View Operational Reports

**Primary Actor:** Facility Administrator

Purpose:
View the approved simple facility reports/indicators.

Approved reporting scope may include:

- bookings;
- completed visits;
- cancellations;
- no-shows;
- late arrivals;
- capacity values;
- expired holds;
- availability-alert subscriptions/conversion;
- stale availability;
- conflict cases;
- payment success/review;
- bookings per doctor.

Advanced analytics are deferred.

---

## FAUC-38 — Receive Facility Notifications

**Actors:**
- Facility Administrator
- Notification Service

Purpose:
Receive approved in-application/system facility notifications.

Examples include notifications about:

- new confirmed bookings;
- payment cases requiring review;
- Patient cancellation/reconfirmation/check-in;
- late arrivals;
- hold expiry returning capacity;
- availability-alert growth;
- stale/exhausted availability;
- unresolved operational exceptions.

Rules:

- general notifications are not delivered through WhatsApp in current scope;
- SMS is not used;
- WhatsApp remains authentication/phone-verification only.

---

# 6. Exact Actor–Use Case Association Matrix

This matrix is authoritative for this Facility Administrator Package.

## Facility Administrator

Associate directly with:

- FAUC-01 Log In
- FAUC-03 Manage Facility Data
- FAUC-04 Manage Branch Display & Contact Data
- FAUC-05 Manage Facility Images & Logo
- FAUC-06 Associate Departments
- FAUC-07 Associate Specialties
- FAUC-08 Add Doctor
- FAUC-09 Edit Doctor
- FAUC-10 Add Service Offering
- FAUC-11 Edit Service Offering
- FAUC-12 Set Service Price
- FAUC-13 Set Estimated Service Duration
- FAUC-14 Set Attendance Instructions
- FAUC-15 Set Booking Policy
- FAUC-16 Set Cancellation/Refund Policy
- FAUC-17 Set No-show Policy
- FAUC-18 Configure Attendance Reconfirmation
- FAUC-19 Manage Doctor Schedules
- FAUC-20 Record Planned Schedule Exception
- FAUC-21 Create Availability Release
- FAUC-22 Configure Arrival Groups
- FAUC-23 Set Initial Digital Capacity
- FAUC-24 Publish Availability
- FAUC-25 View Capacity Status
- FAUC-26 Withdraw Remaining Capacity
- FAUC-27 Freeze Availability
- FAUC-28 Close Availability
- FAUC-29 Add Facility Staff Account
- FAUC-30 Disable Facility Staff Account
- FAUC-31 Assign Approved Role
- FAUC-32 Provision Doctor Login Access
- FAUC-33 Review Daily Operations
- FAUC-34 View Aafiatak Appointments
- FAUC-35 View Payment Status
- FAUC-36 Manage Operational Exceptions
- FAUC-37 View Operational Reports
- FAUC-38 Receive Facility Notifications

Do **not** directly associate Facility Administrator with:

- FAUC-02 Verify WhatsApp OTP

because FAUC-02 is the mandatory helper included by Log In.

## WhatsApp Authentication Provider

Associate only with:

- FAUC-02 Verify WhatsApp OTP

## Notification Service

Associate only with:

- FAUC-38 Receive Facility Notifications

No other direct Actor Associations are approved.

**Association totals:**
- Facility Administrator: 37
- WhatsApp Authentication Provider: 1
- Notification Service: 1
- Total direct Actor Associations: **39**

---

# 7. Exact UML Relationships

Use exactly **one `<<include>>` relationship**.

There are **no approved `<<extend>>` relationships** in this package.

There is **no Generalization**.

## FINC-01

**Log In** `<<include>>` **Verify WhatsApp OTP**

Direction:

`FAUC-01 → FAUC-02`

Reason:
Facility Administrator authentication is passwordless and requires successful WhatsApp OTP verification.

---

# 8. Relationships Deliberately NOT Added

Do not add dependencies simply because operations are logically related or often occur near each other.

Specifically:

- Do not connect `Manage Facility Data` to its detail operations with invented `include`.
- Do not make `Add Doctor <<include>> Provision Doctor Login Access`; a Doctor profile and login access are distinct and not every profile operation necessarily provisions authentication at the same moment.
- Do not make `Add Facility Staff Account <<include>> Assign Approved Role` unless a later authoritative modeling decision explicitly requires that dependency.
- Do not connect `Add Service Offering` to every price/policy/instruction operation using `include`.
- Do not connect `Create Availability Release` to `Configure Arrival Groups` using `include`.
- Do not connect `Create Availability Release` to `Set Initial Digital Capacity` using `include`.
- Do not connect `Configure Arrival Groups` → `Publish Availability` with a chronological arrow.
- Do not connect `View Capacity Status` → `Withdraw Remaining Capacity` / `Freeze Availability` / `Close Availability` as sequence arrows.
- Do not connect `Review Daily Operations` to every operational Use Case.
- Do not connect `Manage Operational Exceptions` to Notification Service merely because exception handling may trigger notifications.
- Do not add `Process Refund` as a direct Facility Administrator financial-control Use Case in this package.
- Do not connect `View Payment Status` to Payment Gateway.
- Do not use `extend` to represent optional policy values.
- Do not use Actor Generalization to merge Facility Administrator with Booking & Reception Staff or Doctor.
- Do not show chronological progress such as configure → publish → monitor → withdraw.

Those flows belong to later Use Case Modeling, Activity, Sequence, or State diagrams when relevant.

---

# 9. Traceability to Main Overview

This package expands the following Main Overview goals.

## `MUC-04 — Log In`

- FAUC-01 Log In
- FAUC-02 Verify WhatsApp OTP

## `MUC-15 — Manage Facility Configuration`

- FAUC-03 Manage Facility Data
- FAUC-04 Manage Branch Display & Contact Data
- FAUC-05 Manage Facility Images & Logo
- FAUC-06 Associate Departments
- FAUC-07 Associate Specialties
- FAUC-08 Add Doctor
- FAUC-09 Edit Doctor
- FAUC-10 Add Service Offering
- FAUC-11 Edit Service Offering
- FAUC-12 Set Service Price
- FAUC-13 Set Estimated Service Duration
- FAUC-14 Set Attendance Instructions
- FAUC-15 Set Booking Policy
- FAUC-16 Set Cancellation/Refund Policy
- FAUC-17 Set No-show Policy
- FAUC-18 Configure Attendance Reconfirmation

## `MUC-16 — Manage Schedules & Availability`

- FAUC-19 Manage Doctor Schedules
- FAUC-20 Record Planned Schedule Exception
- FAUC-21 Create Availability Release
- FAUC-22 Configure Arrival Groups
- FAUC-23 Set Initial Digital Capacity
- FAUC-24 Publish Availability
- FAUC-25 View Capacity Status
- FAUC-27 Freeze Availability
- FAUC-28 Close Availability

## `MUC-21 — Manage Capacity`

- FAUC-25 View Capacity Status
- FAUC-26 Withdraw Remaining Capacity
- FAUC-27 Freeze Availability
- FAUC-28 Close Availability

## `MUC-17 — Manage Facility Staff Accounts`

- FAUC-29 Add Facility Staff Account
- FAUC-30 Disable Facility Staff Account
- FAUC-31 Assign Approved Role
- FAUC-32 Provision Doctor Login Access

## `MUC-18 — Review Daily Operations`

- FAUC-33 Review Daily Operations
- FAUC-34 View Aafiatak Appointments
- FAUC-35 View Payment Status
- FAUC-37 View Operational Reports

## `MUC-19 — Manage Operational Exceptions`

- FAUC-36 Manage Operational Exceptions

## `MUC-14 — Deliver Notifications`

- FAUC-38 Receive Facility Notifications

No detailed Facility Administrator Use Case may silently expand the role into Platform Administrator or Booking & Reception Staff responsibilities beyond the authoritative permission boundary.

---

# 10. Explicit Facility Administrator Restrictions

The package must NOT contain or imply:

- increasing published capacity after publication;
- restoring withdrawn capacity to the same release;
- `+1` capacity action;
- withdrawing active-held capacity;
- withdrawing confirmed capacity;
- managing another facility;
- editing platform-wide settings;
- managing global cities/regions/facility types/reference catalogs;
- deleting or rewriting audit history;
- arbitrary custom-permission designer;
- assigning unapproved roles;
- public self-registration of Facility Administrator;
- facility applicant portal;
- password login;
- Forgot Password / Reset Password;
- SMS authentication;
- general WhatsApp notifications;
- arbitrary Payment Gateway outcome changes;
- partial/deposit payment;
- partial refund engine;
- cashier/accounting/full invoice functions;
- clinical records;
- diagnosis;
- prescriptions;
- laboratory/radiology workflow;
- insurance;
- facility-wide HIS/EHR behavior;
- copying phone/walk-in patients into Aafiatak as new bookings merely to reconcile capacity;
- importing free internal capacity back into a published Aafiatak release;
- guaranteed exact doctor-entry times;
- management of another facility's Patient data;
- advanced analytics beyond approved simple reports.

---

# 11. Important Domain Rules That Must Remain Visible in Modeling

These rules govern interpretation of the Use Cases even when they are not drawn as extra ellipses.

## 11.1 Facility owns its operational data

The facility maintains its own:

- facility/branch information;
- departments/specialties associations;
- doctors;
- services;
- prices;
- schedules;
- Aafiatak reception periods;
- Arrival Groups;
- capacity;
- booking/cancellation/no-show policies;
- attendance instructions;
- staff accounts.

Platform Administration does not run those records on the facility's behalf.

## 11.2 Published capacity is an upper bound

After publication:

- `published` cannot increase;
- only valid remaining capacity may be withdrawn;
- withdrawal is one-way;
- no restoration into the same release.

## 11.3 Published terms are immutable for that release

When a release becomes `PUBLISHED`, its applicable amount/currency/policies are snapshotted.

Later ServiceOffering changes apply to future releases, not silently to the already published release.

Confirmed Appointments preserve their own booking snapshot.

## 11.4 Payment state is independent

Facility Administrator may view Payment status but may not force a gateway outcome.

## 11.5 Operational exceptions are audited

Exception resolution must be documented; session cancellation/conflict does not silently delete existing confirmed appointments/history.

## 11.6 Role provisioning is controlled

Facility Administrator manages facility-side staff roles only within approved RBAC boundaries.

---

# 12. Granularity Decisions

Potential additional Use Cases were reviewed and deliberately not added.

## 12.1 No separate `Set Facility Currency`

The specification identifies a single configured facility currency, but does not unambiguously assign a separate Facility Administrator currency-setting operation. Do not invent it as a standalone Use Case.

## 12.2 No separate `Set Reservation Hold Duration`

Whether facilities may choose among platform-approved hold durations remains an explicit open decision. Do not resolve that uncertainty by inventing a Facility Administrator Use Case.

## 12.3 No separate `Define Reception Period`

This configuration is part of preparing an AvailabilityRelease and its Arrival Groups in the approved package inventory. It is not promoted to another standalone ellipse.

## 12.4 No separate `Reopen Availability`

Release lifecycle rules allow `PUBLISHED <-> FROZEN`, but do not justify a generic reopening Use Case for CLOSED/CANCELLED releases. Closed/cancelled releases must not be reopened into a bookable state.

## 12.5 No separate `Process Refund`

Refund may result from approved cancellation/exception rules, but Facility Administrator must not directly manipulate gateway outcomes. Detailed financial recovery belongs to appropriate financial/exception modeling.

## 12.6 No separate operational-exception micro-actions

The Reception package contains the deeper day-to-day exception decomposition. Facility Administrator retains the high-level `Manage Operational Exceptions` goal rather than duplicating all Reception operations.

## 12.7 No separate report for every metric

The approved simple indicators remain grouped under `View Operational Reports`; each report row is not a separate Use Case.

---

# 13. Visual Composition Requirements

This package is substantially larger than Visitor and Patient, so visual organization is important.

Use one primary Facility Administrator package but organize the content into **seven visual neighborhoods**:

1. Authentication
2. Facility Configuration
3. Doctors & Services
4. Policies
5. Schedules & Digital Availability
6. Facility Staff Administration
7. Operations & Oversight

These are visual neighborhoods only; do not create nested UML packages unless separately approved.

Recommended Actor placement:

- **Facility Administrator:** outside left, aligned with the package's center/major management areas.
- **WhatsApp Authentication Provider:** outside near Log In / Verify WhatsApp OTP.
- **Notification Service:** outside near Receive Facility Notifications.

Design priorities:

- relationship locality before decorative symmetry;
- short actor connections where practical;
- strong visual grouping by whitespace/alignment;
- readable normal report-scale typography;
- no long global routing buses;
- no lines through Actor labels or Use Case labels;
- `<<include>>` kept local between Log In and Verify WhatsApp OTP;
- no fake UML relations between neighboring configuration actions.

Because there are many direct Facility Administrator Associations, the renderer may use a **clearly repeated visual representation of the same Facility Administrator actor** only if necessary to avoid unreadable connector buses, provided:
- every repeated symbol has the exact same label `Facility Administrator`;
- it is explicitly treated as a presentation duplicate of the same UML Actor, not a new Actor;
- semantic Actor count remains one;
- no different permissions are implied.

Prefer one-sheet composition first. If a single sheet cannot maintain normal report-scale readability without tiny text, the same semantic Facility Administrator package may be presented across coordinated sheets, but no Use Case may be removed and no new semantic package may be invented merely for layout.

Do not enlarge the canvas merely to claim higher resolution. SVG is vector.

---

# 14. Final QA Checklist

## UML compliance

- [ ] Correct diagram title.
- [ ] Correct System Boundary title.
- [ ] Facility Administrator outside System Boundary.
- [ ] WhatsApp Authentication Provider outside System Boundary.
- [ ] Notification Service outside System Boundary.
- [ ] Facility Administrator Package inside System Boundary.
- [ ] Exactly 38 Use Cases are present.
- [ ] All visible labels are English.
- [ ] Every Use Case name begins with a verb.
- [ ] Facility Administrator has exactly 37 direct Associations.
- [ ] WhatsApp Authentication Provider has exactly 1 Association.
- [ ] Notification Service has exactly 1 Association.
- [ ] Facility Administrator is not directly associated with Verify WhatsApp OTP.
- [ ] Associations are solid plain lines without arrowheads.
- [ ] Exactly 1 `<<include>>`.
- [ ] 0 `<<extend>>`.
- [ ] 0 Generalization.
- [ ] No chronological arrows.
- [ ] No Classes/Attributes/database/components/UI-screen elements.

## Product compliance

- [ ] Facility Administrator is limited to own facility.
- [ ] Login is passwordless WhatsApp OTP.
- [ ] SMS/password recovery is absent.
- [ ] Facility data/branch/images are manageable.
- [ ] Departments/specialties are associated from reference lists, not globally administered.
- [ ] Doctor profile management is separated from Doctor login provisioning.
- [ ] Service amount/policies belong to ServiceOffering.
- [ ] Booking policy supports exactly two approved values.
- [ ] No deposit/partial payment.
- [ ] Cancellation/no-show policies match approved scope.
- [ ] Reconfirmation timing remains unresolved, not invented.
- [ ] AvailabilityRelease / Arrival Groups / initial digital capacity are present.
- [ ] Published capacity cannot increase.
- [ ] Withdrawal is one-way.
- [ ] Held/confirmed capacity cannot be withdrawn.
- [ ] Freeze and close are not confused with withdrawal.
- [ ] Staff roles are limited to approved RBAC.
- [ ] No arbitrary custom-permission designer.
- [ ] Payment outcomes cannot be arbitrarily overwritten.
- [ ] Operational exceptions remain documented/audited.
- [ ] Simple reports only; no advanced analytics.
- [ ] General facility notifications use Notification Service, not WhatsApp.
- [ ] No deferred clinical/HIS/cashier functions exist.

## Visual quality

- [ ] Seven visual neighborhoods are immediately understandable.
- [ ] Authentication connections remain local.
- [ ] Notification connections remain local.
- [ ] No giant actor-association bus dominates the figure.
- [ ] Typography is readable at normal presentation/report scale.
- [ ] No connector crosses Actor labels or ellipse labels.
- [ ] The package does not look like a UI/dashboard.
- [ ] Visual grouping does not introduce false UML semantics.
- [ ] Artboard is content-driven rather than arbitrarily huge.

---

# 15. Nine-Pass Review Record

## Review 1 — Lecturer / UML Method

Checked lecturer PDF and supplied course rules for:

- Actor / Use Case / Relationship identification;
- Association;
- `<<include>>`;
- `<<extend>>`;
- Generalization;
- package organization for large systems;
- separation between diagram and later Use Case Modeling;
- avoidance of chronological arrows;
- meaningful rather than microscopic Use Cases.

Result:
This remains a detailed Use Case Diagram organized by the Facility Administrator package, not the later formal Package Diagram.

---

## Review 2 — Facility Administrator Permission Audit

Checked the authoritative Facility Administrator permission block.

Confirmed authority to:

- log in;
- manage own facility/branch display/contact data;
- manage images/logo;
- associate departments/specialties;
- add/edit doctors;
- add/edit ServiceOfferings;
- set prices/duration/instructions/policies;
- manage schedules/planned exceptions;
- create/publish AvailabilityRelease/Arrival Groups/capacity;
- view/withdraw/freeze/close capacity;
- manage operational exceptions;
- manage facility staff accounts/roles;
- view appointments/payment/operational indicators.

Confirmed prohibitions on:

- published-capacity increase;
- withdrawal restoration;
- another facility;
- platform-wide settings;
- audit deletion;
- unrelated Patient data.

Result:
The detailed package inventory is strongly grounded in explicit role permissions.

---

## Review 3 — Authentication & Identity Audit

Checked global authentication/account-provisioning rules.

Confirmed:

- Facility Administrator authentication is passwordless;
- WhatsApp OTP is mandatory;
- SMS is absent;
- password recovery is invalid;
- Facility Administrator is provisioned after approved onboarding, not self-registered;
- the Facility Administrator provisions/disables BookingReceptionStaff and Doctor login access;
- privileged sessions are invalidated when access is revoked.

Finding:
`docs/use_case.md` Facility Administrator package omitted Login/OTP detail.

Correction:
Added FAUC-01 Log In and FAUC-02 Verify WhatsApp OTP with one `<<include>>`.

---

## Review 4 — Facility Configuration / Doctor / Service / Policy Audit

Checked facility-data responsibility and ServiceOffering semantics.

Confirmed:

- facility owns its own operational data;
- public reference lists are platform-owned but facility associations are facility-controlled;
- Doctor profile management is facility-controlled;
- ServiceOffering contains amount, booking policy, cancellation/no-show policy, instructions, optional estimated duration;
- published release and Appointment snapshots prevent later configuration drift.

Result:
Configuration Use Cases retained with distinct scopes; no platform reference-data administration was imported.

---

## Review 5 — Schedule / Availability / Capacity Audit

Checked AvailabilityRelease, ArrivalGroup, CapacityWithdrawal, lifecycle and accounting rules.

Confirmed:

- bounded Online Allocation Pool only;
- initial capacity before publication;
- published capacity is upper bound;
- one-way withdrawal;
- no withdrawal of held/confirmed units;
- freeze/close are distinct from withdrawal;
- no reverse transfer from facility internal schedule;
- no `+1`;
- stale/exhausted are indicators, not lifecycle states.

Result:
Availability/capacity Use Cases are correct and restrictions are explicit.

---

## Review 6 — Staff / Operations / Notifications / Reports Audit

Checked RBAC, Today Pulse Board, Facility Notifications, Operational Exceptions and Simple Reports.

Confirmed:

- Facility Administrator controls facility staff accounts/approved roles;
- Today Pulse Board is a UI supporting `Review Daily Operations`, not itself a Use Case;
- Administrator may view appointments and payment states;
- Administrator may manage Operational Exceptions;
- Facility users receive approved operational notifications;
- simple reports are in scope;
- advanced analytics are deferred.

Finding:
The preserved package inventory omitted an explicit facility-notification Use Case despite Main Overview and project specification support.

Correction:
Added FAUC-38 Receive Facility Notifications with Notification Service.

---

## Review 7 — Omission / Open-Decision Audit

Reviewed possible missing capabilities and unresolved configuration.

Checked:

- Log Out;
- facility currency;
- ReservationHold duration;
- reception period;
- refunds;
- reopening availability;
- audit viewing;
- platform-wide references.

Decisions:

- no Facility Admin `Log Out`: not explicitly specified as a separate facility-dashboard capability;
- no `Set Facility Currency`: actor authority for a separate standalone operation is not explicit enough;
- no `Set Reservation Hold Duration`: selection authority remains an open decision;
- no standalone `Define Reception Period`: retained within approved availability setup granularity;
- no direct `Process Refund`: financial outcomes cannot be arbitrarily controlled;
- no `Reopen Closed Availability`;
- no platform-wide reference administration;
- no `Review Audit Logs` Use Case for Facility Admin because the explicit Platform Administrator role owns that overview responsibility and ordinary facility users cannot delete history; the source does not establish a distinct Facility Administrator audit-log review goal.

Result:
Open decisions remain open; no speculative operations added.

---

## Review 8 — UML Relationship Audit

Tested plausible dependencies against strict UML semantics.

Approved:

- Log In `<<include>>` Verify WhatsApp OTP

Rejected as unjustified or chronological:

- Add Doctor → Provision Doctor Login Access
- Add Staff → Assign Role
- Add ServiceOffering → price/policy operations
- Create AvailabilityRelease → Configure Arrival Groups
- Create AvailabilityRelease → Set Initial Digital Capacity
- Configure → Publish
- View Capacity → Withdraw/Freeze/Close
- Operational Exception → Notification
- View Payment Status → Payment Gateway
- any Generalization among human roles

Result:
Exactly 1 `include`, 0 `extend`, 0 Generalization.

---

## Review 9 — Granularity / Cross-Package / Visual Audit

Compared Facility Administrator responsibilities with:

- Main Overview;
- Booking & Reception Staff package;
- Doctor package;
- Platform Administrator package.

Confirmed:

- Facility Administrator owns configuration, availability setup, facility staff administration and oversight.
- Reception retains deeper daily appointment/check-in/queue/visit/exception execution.
- Doctor retains limited read-and-call operations.
- Platform Administrator retains onboarding/platform reference/platform staff/support/audit responsibilities.

The 38 retained Use Cases are meaningful actor goals/configuration responsibilities, not UI buttons or database operations.

Visual density was also assessed. Because one Actor participates in many detailed operations, the implementation must solve density through deliberate composition/presentation rather than inventing semantic generalization or deleting associations.

Final semantic result:

- Primary human Actor: **1**
- External Actors: **2**
- Use Cases: **38**
- Facility Administrator direct Associations: **37**
- Total Actor Associations: **39**
- `<<include>>`: **1**
- `<<extend>>`: **0**
- Generalization: **0**

No unresolved semantic contradiction blocks diagram implementation.

---

# 16. Final Implementation Contract

The implementation agent must:

- use this file as execution truth for the Facility Administrator Package;
- preserve exactly the 38 approved Use Cases;
- preserve exactly the Actor Association Matrix;
- render exactly 1 approved `<<include>>`;
- add no unapproved `extend`, Generalization, or chronological relationship;
- keep all Actors outside the System Boundary;
- keep all Use Cases inside `Facility Administrator Package`;
- keep all visible labels English;
- preserve all Aafiatak role restrictions and open decisions;
- use direct, professional, relationship-aware composition;
- optimize visual quality without modifying UML/product truth;
- leave final visual approval to the user.

