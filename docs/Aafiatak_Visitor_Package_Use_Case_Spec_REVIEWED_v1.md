# Aafiatak — Visitor Package Use Case Diagram Specification

## 0. Document Status

**Deliverable:** Actor Package Use Case Diagram  
**Actor package:** Visitor  
**System:** Aafiatak Medical Appointment Booking System  
**Language of visible diagram labels:** English  
**Status:** Reviewed execution specification — ready for diagram implementation

This document defines the approved content and UML semantics for the **Visitor Package Use Case Diagram**.

It is a detailed actor-oriented Use Case view created after the Main Use Case Diagram to expose the unauthenticated Visitor's approved operations without overloading the system overview.

This is a modeling/drawing specification. It is not:

- a UI specification;
- a workflow/activity specification;
- a Sequence Diagram;
- a Class Diagram;
- a database model;
- the later formal UML Package Diagram.

**Important course distinction:** the lecturer uses Packages during Use Case analysis to organize large systems and group related Use Cases. This deliverable is therefore a **Use Case Diagram organized through the Visitor package**. It still uses normal Use Case notation: Actors, Associations, `<<include>>`, and where justified `<<extend>>`. The later formal Package Diagram remains a separate structural deliverable.

---

# 1. Authority and Conflict Rules

Use the following precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative product truth.
2. Lecturer UML PDF and supplied lecturer-course notes — academic UML rules and notation.
3. `docs/use_case.md` — approved Use Case work structure and preserved Visitor Package inventory.
4. This Visitor Package specification — reviewed execution truth for this diagram.
5. Rendering/layout tooling — presentation mechanics only.

Rules:

- Do not invent product behavior from general UML knowledge.
- Do not add a Use Case merely because it is common in similar systems.
- If this file conflicts with the authoritative project specification, the project specification wins.
- Do not use an old Aafiatak diagram as semantic truth.
- Visible diagram labels must be English.

---

# 2. Lecturer Rules Applied to This Diagram

The lecturer's Use Case method requires:

- identification of Actors;
- extraction of user-facing Use Cases;
- a clear System Boundary;
- valid UML relationships;
- separation between high-level overview and detailed package work for large systems.

Mandatory notation:

- Actor–Use Case Association: **solid plain line**, no arrowhead.
- `<<include>>`: **dashed dependency**, direction **base → mandatory included Use Case**.
- `<<extend>>`: **dashed dependency**, direction **conditional extending Use Case → base Use Case**.
- Generalization is used only when a genuine inheritance relation is justified. It must not be invented to reduce lines.
- Use Case names begin with verbs.
- Use Case Diagram does **not** show execution chronology.
- Detailed success/failure scenarios, preconditions, postconditions, and flow steps belong to later **Use Case Modeling**.
- Do not place Classes, Attributes, database tables, PostgreSQL, components, APIs, pages, screens, or UI controls inside this Use Case Diagram.

The lecturer also warns against both extremes:

- oversimplifying a realistic system;
- turning every tiny UI action or implementation step into a separate Use Case.

This Visitor Package therefore keeps only meaningful Visitor goals explicitly supported by the approved sources.

---

# 3. Diagram Scope and Structure

## 3.1 Exact diagram title

**Visitor Package Use Case Diagram — Aafiatak Medical Appointment Booking System**

## 3.2 System Boundary

Draw one System Boundary titled:

**Aafiatak Medical Appointment Booking System**

All Actors remain outside the System Boundary.

## 3.3 Visitor Package

Inside the System Boundary, draw one UML package container titled:

**Visitor Package**

This package is an organizational container for the Visitor's detailed Use Cases during the lecturer's Use Case-analysis stage.

Do not interpret this as the later formal UML Package Diagram.

Do not create nested UML packages for the small Visitor scope. If visual grouping is useful, use whitespace/alignment only.

## 3.4 Primary human Actor

Exactly one primary human Actor:

- **Visitor**

Definition:
An unauthenticated public user interacting with Aafiatak before an authenticated Patient session exists.

Do not add `Patient` as a second human Actor in this package.

Do not create:

- `User`;
- `Guest`;
- `Public User`;
- `New Patient`;
- `Existing Patient`;
- `Authenticated User`.

Do not introduce Visitor → Patient Generalization.

## 3.5 External Actors

Exactly these external Actors appear where they directly participate:

- **Map Service**
- **WhatsApp Authentication Provider**

Do not add:

- Payment Gateway;
- Notification Service;
- SMS Provider;
- Database;
- PostgreSQL;
- HIS/EHR;
- Facility Internal System;
- Cashier;
- any deferred external service.

Payment and general notifications are outside the unauthenticated Visitor package.

---

# 4. Exact Visitor Package Use Cases

The Visitor Package contains exactly **7 Use Cases**.

IDs are traceability metadata and should not appear inside visible ellipses unless explicitly required by the lecturer.

---

## VUC-01 — Browse Facility & Service Information

**Primary Actor:** Visitor

Purpose:
Allow the unauthenticated Visitor to browse approved public information about Aafiatak facilities and their offered medical-service context.

Supported scope includes public information such as:

- facility/branch information;
- departments;
- specialties;
- doctors;
- services;
- contact/general public information.

Boundary:

- This does not expose the facility's complete internal schedule.
- This does not expose private Patient information.
- This does not create a booking.
- This does not introduce medical records, diagnosis, prescriptions, laboratory results, insurance, or other deferred clinical content.

---

## VUC-02 — Search Doctors & Services

**Primary Actor:** Visitor

Purpose:
Allow public search/browse using approved discovery criteria.

Supported search concepts include:

- doctor;
- department;
- specialty;
- service.

Do not add:

- AI recommendations;
- advanced ratings/ranking;
- reviews;
- insurance filtering;
- clinical-condition recommendation logic.

---

## VUC-03 — View Available Days & Arrival Groups

**Primary Actor:** Visitor

Purpose:
Allow the Visitor to view **preliminary Aafiatak digital availability** such as available days and Arrival Group windows.

Mandatory interpretation:

- This is visibility into capacity published to Aafiatak only.
- It is not the facility's complete internal schedule.
- An Arrival Group is an **arrival window**, not a guaranteed doctor-entry time.
- The Visitor does not reserve capacity through this Use Case.
- The Visitor cannot choose/lock an arbitrary Arrival Group.
- Booking requires authentication and belongs to the Patient Package.

---

## VUC-04 — View Facility Location

**Actors:**
- Visitor
- Map Service

Purpose:
Display the facility/branch location through the approved external Map Service.

This is the only Visitor Use Case with direct Map Service participation.

Do not model the Map Service as an internal Aafiatak component.

---

## VUC-05 — Register Patient

**Primary Actor:** Visitor

Purpose:
Allow an unauthenticated Visitor to create the approved Patient identity/profile after mandatory phone verification through WhatsApp OTP.

Rules:

- Patient self-registration is permitted.
- Phone number must be normalized/verified according to the product rules.
- Registration is passwordless.
- SMS is not used.
- No password is created.
- No `Forgot Password` / `Reset Password` Use Case exists.
- Retried registration must not create duplicate identities.

Successful registration establishes the approved Patient account/profile context; do not draw a chronological arrow from `Register Patient` to later Patient operations.

---

## VUC-06 — Log In

**Primary Actor:** Visitor

Purpose:
Allow an unauthenticated Visitor who already has an approved account/role to initiate passwordless authentication and establish a valid application session.

Rules:

- Authentication uses WhatsApp OTP.
- No password authentication.
- No SMS authentication.
- No Forgot Password / Reset Password flow.
- Login does not itself imply booking or any later operation.

Although authenticated roles may also use Log In in other actor-package diagrams, this Visitor Package shows the unauthenticated entry action from the Visitor perspective only.

---

## VUC-07 — Verify WhatsApp OTP

**External Actor:** WhatsApp Authentication Provider  
**Role:** Helper Use Case

Purpose:
Perform the mandatory OTP verification required for:

- Patient self-registration;
- passwordless login.

Rules:

- Uses the approved official WhatsApp authentication/provider integration.
- WhatsApp is used here only for authentication / phone verification.
- General reminders, booking notifications, queue notifications, and availability alerts are not part of this Visitor helper Use Case.
- SMS is not used.

**Important Association rule:**  
Do not draw a direct Visitor Association to `Verify WhatsApp OTP`.

The Visitor directly initiates `Register Patient` or `Log In`; those base Use Cases obligatorily include OTP verification. The external WhatsApp Authentication Provider directly participates in `Verify WhatsApp OTP`.

---

# 5. Exact Actor–Use Case Association Matrix

This matrix is authoritative for the Visitor Package.

## Visitor

Associate Visitor directly with:

- VUC-01 Browse Facility & Service Information
- VUC-02 Search Doctors & Services
- VUC-03 View Available Days & Arrival Groups
- VUC-04 View Facility Location
- VUC-05 Register Patient
- VUC-06 Log In

Do **not** associate Visitor directly with:

- VUC-07 Verify WhatsApp OTP

Reason:
VUC-07 is a mandatory helper invoked through registration/login rather than an independent Visitor goal.

## Map Service

Associate only with:

- VUC-04 View Facility Location

## WhatsApp Authentication Provider

Associate only with:

- VUC-07 Verify WhatsApp OTP

No other direct Actor Associations are approved.

---

# 6. Exact UML Relationships

Use exactly **2 `<<include>>` relationships**.

There are **no `<<extend>>` relationships** in the Visitor Package.

There is **no Generalization**.

---

## VINC-01

**Register Patient** `<<include>>` **Verify WhatsApp OTP**

Direction:

`VUC-05 → VUC-07`

Reason:
Verified phone ownership through the approved WhatsApp OTP mechanism is mandatory for Patient self-registration.

---

## VINC-02

**Log In** `<<include>>` **Verify WhatsApp OTP**

Direction:

`VUC-06 → VUC-07`

Reason:
Human-account authentication is passwordless and requires successful WhatsApp OTP verification.

---

# 7. Relationships Deliberately NOT Added

Do not add relationships merely to show navigation, order, or similarity.

Specifically:

- Do not connect `Browse Facility & Service Information` → `Search Doctors & Services` with an arrow.
- Do not connect `Search Doctors & Services` → `View Available Days & Arrival Groups` with an arrow.
- Do not connect `View Available Days & Arrival Groups` → `Register Patient`.
- Do not connect `View Available Days & Arrival Groups` → `Log In`.
- Do not connect `Register Patient` → `Log In`.
- Do not connect `Register Patient` → any Patient booking Use Case.
- Do not add `Log In <<extend>> Browse...`.
- Do not add `Register Patient <<extend>> Log In`.
- Do not use Generalization between Visitor and Patient.
- Do not introduce an `Authentication` generic Use Case merely to reduce lines.
- Do not connect Map Service to Browse/Search unless a direct approved interaction is explicitly modeled later.
- Do not use chronological arrows to show "browse, then register, then login, then book."

Those are workflow/navigation concerns and belong in later Activity/Sequence/Use Case Modeling where relevant.

---

# 8. Traceability to Main Overview

The Visitor Package expands the following Main Overview content:

## `MUC-01 — Discover Medical Services`

Detailed Visitor Use Cases:

- VUC-01 Browse Facility & Service Information
- VUC-02 Search Doctors & Services
- VUC-03 View Available Days & Arrival Groups

## `MUC-02 — View Facility Location`

Detailed Visitor Use Case:

- VUC-04 View Facility Location

## `MUC-03 — Register Patient`

Detailed Visitor Use Cases:

- VUC-05 Register Patient
- VUC-07 Verify WhatsApp OTP

## `MUC-04 — Log In`

Detailed Visitor Use Cases:

- VUC-06 Log In
- VUC-07 Verify WhatsApp OTP

No Visitor Package operation expands Main booking/payment/appointment/queue/notification goals because those require the Patient role or other authenticated roles.

---

# 9. Explicit Visitor Restrictions

The Visitor Package must NOT contain or imply:

- Book Appointment
- Check Bookable Availability as a booking helper
- Create Reservation Hold
- View Reservation Hold Countdown
- Subscribe to Availability Alert
- Receive Availability Alert
- Process Full Payment
- Verify Payment Result
- View Payment Status
- View Simplified Payment Receipt
- Manage/View Patient Appointments
- Cancel Appointment
- Reconfirm Attendance
- View Booking Number / QR
- self-rescheduling
- self-check-in
- queue visibility
- queue-position change
- visit outcome
- general Patient notifications
- choosing booking policy
- choosing arbitrary Arrival Group
- deposit payment
- partial payment
- manual booking approval
- Password
- Forgot Password
- Reset Password
- SMS authentication
- general WhatsApp messaging
- medical records
- diagnoses
- prescriptions
- insurance
- family/dependent accounts
- ratings/reviews
- complaints
- chat
- video consultation
- AI recommendations
- any platform/facility administration operation.

Key rule:

**The Visitor may discover information and begin account access, but may not create an appointment before authentication.**

---

# 10. Granularity Decisions

The following potential operations were reviewed and deliberately **not** split into extra Visitor Use Cases.

## 10.1 No separate `View Departments`

Departments are part of public discovery/browsing and search scope. Creating a separate Use Case would add unnecessary micro-detail without a distinct Visitor goal justified by the approved package list.

## 10.2 No separate `View Specialties`

Handled within browsing/search.

## 10.3 No separate `View Doctor Profile`

Doctor information belongs within approved public facility/service discovery unless a later authoritative package specification explicitly promotes it to a standalone Use Case.

## 10.4 No separate `View Service Price & Policies`

The approved Visitor Package inventory does not define this as a separate Visitor Use Case. Do not silently import the Patient Package's richer authenticated service-detail decomposition into Visitor.

Where public service information is exposed, it remains within `Browse Facility & Service Information` unless the authoritative scope is explicitly revised.

## 10.5 No separate `Select Arrival Group`

Explicitly forbidden. The system chooses the earliest currently bookable Arrival Group during Patient booking; the Visitor only views preliminary availability.

## 10.6 No separate `Request OTP`

OTP request/delivery/verification is modeled at this abstraction level through `Verify WhatsApp OTP`; do not fragment authentication into UI-level micro-actions.

---

# 11. Visual Composition Requirements

This diagram is intentionally small and should be significantly cleaner than the Main Use Case Diagram.

Recommended composition:

### Left exterior
- Visitor

### Inside Visitor Package — Discovery neighborhood
- Browse Facility & Service Information
- Search Doctors & Services
- View Available Days & Arrival Groups
- View Facility Location

### Inside Visitor Package — Access neighborhood
- Register Patient
- Log In
- Verify WhatsApp OTP

### Exterior near location
- Map Service

### Exterior near authentication
- WhatsApp Authentication Provider

Visual rules:

- Keep all Actors outside System Boundary.
- Keep all 7 Use Cases inside `Visitor Package`.
- Use one restrained visual treatment; do not create unnecessary nested package/card structure.
- Position `Verify WhatsApp OTP` close to `Register Patient` and `Log In`.
- Position Map Service close to `View Facility Location`.
- Position WhatsApp Authentication Provider close to `Verify WhatsApp OTP`.
- Use short, local association lines.
- Render both `<<include>>` dependencies clearly and locally.
- Do not use long routing buses.
- Do not use arrows between discovery items.
- Text must be readable at normal report/presentation scale.
- Decorative background elements must not be interpreted as UML semantics.

Because the package is small, a single landscape page should be sufficient. Do not enlarge the artboard unnecessarily.

---

# 12. Final QA Checklist

## UML compliance

- [ ] Correct diagram title.
- [ ] Correct System Boundary title.
- [ ] Visitor outside System Boundary.
- [ ] Map Service outside System Boundary.
- [ ] WhatsApp Authentication Provider outside System Boundary.
- [ ] Visitor Package inside System Boundary.
- [ ] Exactly 7 Use Cases inside Visitor Package.
- [ ] All visible labels are English.
- [ ] Every Use Case name begins with a verb.
- [ ] Visitor has exactly 6 direct Associations.
- [ ] Map Service has exactly 1 direct Association.
- [ ] WhatsApp Authentication Provider has exactly 1 direct Association.
- [ ] Visitor is not directly associated with Verify WhatsApp OTP.
- [ ] Associations are solid lines with no arrowheads.
- [ ] Exactly 2 `<<include>>` relationships.
- [ ] No `<<extend>>`.
- [ ] No Generalization.
- [ ] No chronological arrows.
- [ ] No Classes/Attributes/database/components/UI controls.

## Product compliance

- [ ] Visitor is unauthenticated.
- [ ] Visitor may browse facility/service information.
- [ ] Visitor may search by doctor/department/specialty/service.
- [ ] Visitor may view preliminary available days/groups.
- [ ] Visitor may view facility location.
- [ ] Visitor may register.
- [ ] Visitor may initiate login.
- [ ] Registration requires WhatsApp OTP.
- [ ] Login requires WhatsApp OTP.
- [ ] SMS is absent.
- [ ] Password recovery is absent.
- [ ] No booking occurs before authentication.
- [ ] No ReservationHold appears in Visitor Package.
- [ ] No Payment Gateway appears.
- [ ] No Notification Service appears.
- [ ] No availability alert appears.
- [ ] No Patient appointment/queue/private-data operation appears.
- [ ] Availability is only Aafiatak's published digital availability.
- [ ] Arrival Groups are not exact service-entry times.
- [ ] Visitor cannot select/reserve an Arrival Group.
- [ ] No deferred feature was added.

## Visual quality

- [ ] Diagram is visibly simpler than Main Overview.
- [ ] Discovery and Access areas are understandable immediately.
- [ ] External Actors sit next to their relevant Use Cases.
- [ ] No unnecessary long connectors.
- [ ] `<<include>>` labels are clearly readable.
- [ ] No line crosses an Actor label or Use Case label.
- [ ] Artboard is not oversized.
- [ ] Typography is readable at normal scale.

---

# 13. Nine-Pass Review Record

## Review 1 — Lecturer / UML Method

Checked the supplied lecturer rules for:

- Actor extraction;
- Use Case extraction;
- System Boundary;
- Association;
- `<<include>>`;
- `<<extend>>`;
- Generalization;
- no execution chronology;
- Package organization for large systems;
- separation from Use Case Modeling.

Result:
The deliverable remains a Use Case Diagram organized by the Visitor package, not the later formal Package Diagram.

---

## Review 2 — Authoritative Visitor Permission Audit

Checked the authoritative `Visitor` permissions.

Confirmed Visitor may:

- browse facilities;
- search/browse by doctor, department, specialty, or service;
- view general facility information;
- view preliminary available days/groups;
- register;
- log in.

Confirmed Visitor may **not create an appointment before authentication**.

Result:
The 6 direct Visitor goals match the authoritative role boundary.

---

## Review 3 — Authentication & Identity Audit

Checked unified identity and authentication rules.

Confirmed:

- Patient may self-register only after successful phone verification.
- Login is passwordless.
- WhatsApp OTP is the approved authentication channel.
- SMS is not used.
- Forgot/Reset Password is invalid.
- The same helper OTP verification is mandatory for registration and login.
- Facility/doctor/platform role provisioning must not be imported into Visitor self-registration.

Result:
`Register Patient` and `Log In` both `<<include>> Verify WhatsApp OTP`.

---

## Review 4 — Discovery & Availability Audit

Checked public discovery and digital-availability rules.

Confirmed:

- browsing/search are public Visitor capabilities;
- preliminary availability may be visible;
- availability refers only to the Online Allocation Pool published to Aafiatak;
- Arrival Groups are arrival windows, not exact service times;
- booking allocation/hold rules belong to Patient booking, not Visitor discovery.

Result:
`View Available Days & Arrival Groups` remains informational only.

---

## Review 5 — External Actor Boundary Audit

Reviewed all approved external services:

- Map Service;
- WhatsApp Authentication Provider;
- Payment Gateway;
- Notification Service.

Result:

Visitor Package needs only:

- Map Service → View Facility Location
- WhatsApp Authentication Provider → Verify WhatsApp OTP

Payment Gateway and Notification Service are excluded because no Visitor Use Case directly invokes them in the approved scope.

---

## Review 6 — Deferred / Forbidden Scope Audit

Scanned the authoritative deferred/out-of-scope list and lecturer restrictions.

Confirmed exclusion of:

- medical records;
- insurance;
- ratings/reviews;
- chat/video;
- AI recommendations;
- family/dependent accounts;
- SMS;
- password recovery;
- self-check-in;
- booking before authentication;
- payment;
- queue;
- facility/platform administration;
- database/internal implementation actors.

Result:
No deferred or implementation feature appears in the package.

---

## Review 7 — Omission Audit

Compared:

- authoritative Visitor permissions;
- Main Overview Visitor associations;
- `docs/use_case.md` Visitor Package inventory;
- public discovery/authentication requirements.

Checked potential omissions such as:

- Log Out
- Manage Profile
- View Service Price & Policies
- Receive Notifications
- Availability Alert

Result:

These are **not Visitor Package omissions**:

- `Log Out` belongs to an authenticated Patient/session context, not an unauthenticated Visitor package.
- `Manage Patient Profile` belongs to Patient.
- richer service-price/policy decomposition is retained in Patient Package; it is not an explicitly approved standalone Visitor Use Case.
- notifications/alerts require Patient context.
- booking/payment/appointment operations require authentication.

Therefore no additional Visitor Use Case is added.

---

## Review 8 — UML Relationship Audit

Tested every plausible relation against UML semantics.

Approved only:

1. Register Patient `<<include>>` Verify WhatsApp OTP
2. Log In `<<include>>` Verify WhatsApp OTP

Rejected:

- browsing/search chronological arrows;
- Register → Login;
- Login → booking;
- discovery `include` relationships;
- Visitor–Patient Generalization;
- authentication generalization;
- any artificial `extend`.

Result:
Exactly 2 `include`, 0 `extend`, 0 Generalization.

---

## Review 9 — Granularity / Package / Visual Audit

Rechecked the lecturer's warning against both over-detail and oversimplification.

Confirmed the final 7 Use Cases are meaningful Visitor goals/helper behavior rather than:

- buttons;
- pages;
- fields;
- internal services;
- implementation steps.

Also confirmed:

- one Visitor Package container is sufficient;
- no nested packages are needed;
- the diagram should fit cleanly on one normal landscape artboard;
- routing can remain local and simple.

Final result:

**Visitor Package approved semantic set:**
- 1 primary human Actor
- 2 external Actors
- 7 Use Cases
- 8 direct Actor Associations total
- 2 `<<include>>`
- 0 `<<extend>>`
- 0 Generalization

No unresolved semantic issue remains for diagram implementation.

---

# 14. Final Implementation Contract

The implementation agent must:

- use this file as the execution truth for the Visitor Package;
- render exactly the 7 approved Use Cases;
- preserve the exact Actor Association Matrix;
- render exactly the 2 approved `<<include>>` relationships;
- add no other `include`, `extend`, Generalization, or chronological relationship;
- keep all Actors outside the System Boundary;
- keep all Use Cases inside Visitor Package;
- keep all labels English;
- preserve Aafiatak's product boundaries;
- optimize visual composition without changing semantics;
- leave final visual approval to the user.

