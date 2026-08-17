# Aafiatak — Platform Administrator Package Use Case Diagram Specification

## 0. Document Status

**Deliverable:** Actor Package Use Case Diagram  
**Actor package:** Platform Administrator  
**System:** Aafiatak Medical Appointment Booking System  
**Language of visible diagram labels:** English  
**Status:** Deep-reviewed execution specification — ready for diagram implementation

This document defines the approved content and UML semantics for the **Platform Administrator Package Use Case Diagram**.

It was rebuilt and reviewed against:

1. `Aafiatak_Project_Specification_EN.md` — current authoritative product truth;
2. the lecturer UML PDF and supplied lecturer-course rules;
3. `docs/use_case.md` — approved Use Case work structure and Platform Administrator inventory;
4. the established reviewed Actor Package conventions used across Aafiatak.

This is a detailed actor-oriented **Use Case Diagram organized through the Platform Administrator package**.

It is **not**:
- the later formal UML Package Diagram;
- an Activity Diagram;
- a Sequence Diagram;
- a State Diagram;
- a Class Diagram;
- a UI/dashboard specification;
- a database model;
- an implementation/component diagram.

The Platform Administrator role is powerful at the **platform level**, but deliberately separated from daily facility operations.

---

# 1. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative product truth.
2. Lecturer UML PDF and supplied lecturer-course notes — academic UML method and notation.
3. `docs/use_case.md` — approved Use Case work structure and preserved Platform Administrator inventory.
4. This reviewed Platform Administrator Package specification — execution truth for this package after the documented review decisions below.
5. Rendering/layout tooling — presentation mechanics only.

Rules:

- Do not invent Platform Administrator powers from generic SaaS/admin expectations.
- Do not turn platform support into authority over facility daily operations.
- Do not add a public `FacilityApplicant` Actor; the current scope explicitly excludes a self-service facility-applicant portal.
- Do not infer a Payment Gateway Actor merely because payment escalations can be reviewed.
- Do not infer Notification Service participation merely because support/escalation information may be communicated.
- If this file conflicts with the authoritative project specification, the project specification wins.
- All visible diagram labels must be English.
- Open implementation/product decisions must remain open.

---

# 2. Lecturer Rules Applied to This Diagram

The lecturer's Use Case method requires:

- Actors;
- Use Cases;
- valid Relationships;
- a clear System Boundary;
- package organization where needed;
- later textual Use Case Modeling for detailed scenarios.

Mandatory notation:

- **Actor–Use Case Association:** solid plain line, no arrowhead.
- **`<<include>>`:** dashed dependency, direction **base Use Case → mandatory included Use Case**.
- **`<<extend>>`:** dashed dependency, direction **conditional extending Use Case → base Use Case**.
- **Generalization:** only when genuine inheritance is supported; do not invent it to reduce lines.
- Use Case names must begin with verbs.
- Use Case Diagram relationships must not show chronological execution.
- Do not use arrows to mean:
  - then;
  - next;
  - before;
  - after;
  - first/second/third.
- Preconditions, main success scenarios, alternative/failure scenarios, and postconditions belong to later **Use Case Modeling**.
- Do not place:
  - Classes;
  - Attributes;
  - database tables;
  - PostgreSQL;
  - APIs;
  - screens/pages;
  - buttons;
  - implementation components
  in this Use Case Diagram.

## 2.1 Lecturer Package Distinction

The lecturer explicitly demonstrates organizing large systems through Packages for actor-related Use Cases, then detailing each Use Case separately through Use Case Modeling.

Therefore this deliverable is:

**a Use Case Diagram organized inside `Platform Administrator Package`**

It is not the later structural Package Diagram.

The later formal Package Diagram will model packages and package dependencies separately.

## 2.2 Granularity Rule

The lecturer warns against both:

- oversimplifying a realistic system;
- turning every tiny UI/implementation action into a separate Use Case.

The Platform Administrator package therefore keeps meaningful platform-level goals and actions while avoiding buttons, fields, screens, database operations, or internal technical steps.

---

# 3. Diagram Scope and Structure

## 3.1 Exact Diagram Title

**Platform Administrator Package Use Case Diagram — Aafiatak Medical Appointment Booking System**

## 3.2 System Boundary

Draw one System Boundary titled:

**Aafiatak Medical Appointment Booking System**

All Actors remain outside the System Boundary.

## 3.3 Platform Administrator Package

Inside the System Boundary, draw one UML package container titled:

**Platform Administrator Package**

All Use Cases defined by this file belong inside that package.

Do not create nested UML packages merely for decoration.

Functional sections below are visual neighborhoods only.

## 3.4 Primary Human Actor

Exactly one primary human Actor:

- **Platform Administrator**

Definition:
An approved/provisioned Aafiatak platform-level administrative user responsible for onboarding, platform reference/staff data, support/escalation oversight, audit review, and platform indicators.

Do not add:

- Facility Administrator
- Booking & Reception Staff
- Doctor
- Patient
- Visitor
- Facility Applicant
- generic `User`
- generic `Admin`
- `Support Agent`

as additional human Actors in this package.

The `Platform Administrator` represents the approved platform-admin role itself.

## 3.5 External Actor

Exactly one external Actor is required:

- **WhatsApp Authentication Provider**

It participates only in:

- **Verify WhatsApp OTP**

Do not add:

- Payment Gateway
- Notification Service
- Map Service
- Database/PostgreSQL
- HIS/EHR
- Facility Internal System
- SMS Provider

to this package.

A Payment escalation is a **review/support activity**, not a direct Payment Gateway operation.

---

# 4. Deep-Review Corrections to the Preserved Package Inventory

The preserved `docs/use_case.md` Platform Administrator inventory contains 18 detailed operations and is largely correct.

However, it omits the authentication detail already present in the Main Overview and authoritative product specification.

## 4.1 Added — Log In

The Main Overview directly associates Platform Administrator with:

**Log In**

The authoritative authentication rules explicitly include `PlatformAdministrator` among the passwordless human roles.

Therefore add:

**PAUC-01 — Log In**

## 4.2 Added — Verify WhatsApp OTP

Platform Administrator authentication requires short-lived, single-use WhatsApp OTP verification through the official authentication provider.

Therefore add helper:

**PAUC-02 — Verify WhatsApp OTP**

with:

**Log In `<<include>>` Verify WhatsApp OTP**

The Platform Administrator does not receive a separate direct Association to this helper Use Case.

## 4.3 No other new platform capability added

The deep review did not justify:

- Log Out
- Receive Platform Notifications
- Configure Global Booking Policies
- Manage Facility Doctors/Services
- Operate Facility Bookings
- Manage Daily Queue
- Directly Process Refund
- Directly Change Payment Result
- Public Facility Applicant registration
- Delete Audit History

as additional Platform Administrator Use Cases.

---

# 5. Exact Platform Administrator Package Use Cases

The reviewed package contains exactly **20 Use Cases**.

IDs are traceability metadata. Do not display `PAUC-xx` inside visible ellipses unless the lecturer explicitly requires IDs.

---

# 5.1 Authentication

## PAUC-01 — Log In

**Primary Actor:** Platform Administrator

Purpose:
Authenticate an already provisioned Platform Administrator account and establish a valid protected platform-administration session.

Rules:

- passwordless authentication;
- official WhatsApp OTP;
- no SMS;
- no password;
- no Forgot Password / Reset Password;
- Platform Administrator accounts are not created through public registration;
- access requires controlled platform-side provisioning/RBAC;
- privileged sessions must be invalidated if platform permissions/access are revoked.

---

## PAUC-02 — Verify WhatsApp OTP

**External Actor:** WhatsApp Authentication Provider  
**Role:** Mandatory helper Use Case

Purpose:
Perform mandatory OTP verification for Platform Administrator login.

Rules:

- official approved WhatsApp Business/provider integration;
- short-lived;
- single-use;
- no plaintext OTP logging/storage;
- WhatsApp is authentication/phone verification only;
- no direct Platform Administrator Association to this helper.

---

# 5.2 Facility Onboarding

## PAUC-03 — Review Facility Onboarding Request

**Primary Actor:** Platform Administrator

Purpose:
Review a facility onboarding request using the approved platform-side intake/review process.

Important scope rule:

There is **no public self-service `FacilityApplicant` portal** in the current scope.

Therefore do not draw a `FacilityApplicant` Actor.

---

## PAUC-04 — Request Additional Information

**Primary Actor:** Platform Administrator

Purpose:
Request additional information when the onboarding material is insufficient for a platform decision.

This is an onboarding action, but do not model it as an `extend` of Review merely to show an optional branch. The detailed decision path belongs to later Use Case Modeling.

---

## PAUC-05 — Approve Facility

**Primary Actor:** Platform Administrator

Purpose:
Approve an eligible facility onboarding request.

Approval is a platform onboarding decision.

Do not automatically collapse this Use Case into:
- Activate Facility;
- Provision Initial Facility Administrator.

Those are separately approved platform operations.

---

## PAUC-06 — Reject Facility

**Primary Actor:** Platform Administrator

Purpose:
Reject a facility onboarding request when the approved criteria are not satisfied.

Do not connect Approve and Reject with sequence/branch arrows inside this Use Case Diagram.

---

## PAUC-07 — Activate Facility

**Primary Actor:** Platform Administrator

Purpose:
Activate an approved facility account for participation in Aafiatak.

Initial onboarding rules include provision/activation of the initial Facility Administrator identity for the verified facility representative.

However, no `<<include>>` is drawn to `Provision Initial Facility Administrator`, because `Activate Facility` may also represent later re-activation contexts where the initial administrator identity already exists. The product source does not establish that provisioning is mandatory in every possible activation execution.

---

## PAUC-08 — Suspend Facility

**Primary Actor:** Platform Administrator

Purpose:
Suspend a facility account when platform-level suspension is required.

Mandatory consequences under the authoritative product rules:

- the suspended facility cannot accept new holds/bookings;
- it cannot publish new availability;
- active temporary holds are released;
- existing confirmed appointments/history are preserved;
- affected confirmed appointments require documented operational resolution;
- suspension does not silently delete booking/history records.

Critical boundary:

Platform Administrator does **not** thereby take over the facility's daily appointment/queue operation.

---

## PAUC-09 — Provision Initial Facility Administrator

**Primary Actor:** Platform Administrator

Purpose:
Provision/activate the initial `FacilityAdministrator` identity for an approved facility representative.

Rules:

- facility roles are not self-assigned;
- verified phone/user identity rules apply;
- this is initial facility-administrator provisioning;
- later facility staff and Doctor login access are handled by the Facility Administrator, not the Platform Administrator.

---

# 5.3 Platform Reference Data

## PAUC-10 — Manage Cities

**Primary Actor:** Platform Administrator

Purpose:
Manage platform-level city reference data used by Aafiatak.

This is platform data, not a facility-specific city-edit permission.

---

## PAUC-11 — Manage Regions

**Primary Actor:** Platform Administrator

Purpose:
Manage platform-level region reference data.

---

## PAUC-12 — Manage Facility Types

**Primary Actor:** Platform Administrator

Purpose:
Manage approved platform-level facility-type reference data.

---

## PAUC-13 — Manage Public Reference Lists

**Primary Actor:** Platform Administrator

Purpose:
Manage other approved public reference lists maintained at platform level.

Granularity note:

Cities, Regions, and Facility Types remain explicit Use Cases because the approved detailed package inventory explicitly preserves them separately.

`Manage Public Reference Lists` represents the broader/residual approved platform reference-list responsibility and must not be used as a pretext to create or modify facility-owned doctors, services, schedules, prices, or policies.

---

# 5.4 Platform Staff

## PAUC-14 — Manage Platform Staff Accounts

**Primary Actor:** Platform Administrator

Purpose:
Manage controlled Aafiatak platform-staff accounts through the platform administration process.

Rules:

- this is platform staff, not facility staff;
- Facility Administrator manages its own facility-side staff accounts;
- Platform Administrator does not become a generic custom-permission designer;
- historical/audited records must not be silently destroyed by account changes.

Do not split this into Add/Edit/Delete/Assign Role micro-use-cases unless the authoritative scope explicitly expands later.

---

# 5.5 Support & Oversight

## PAUC-15 — Review Technical Escalation

**Primary Actor:** Platform Administrator

Purpose:
Review a documented technical escalation that requires platform-level support/oversight.

This does not make Platform Administrator the operator of the facility's daily booking/queue workflow.

---

## PAUC-16 — Review Payment Escalation

**Primary Actor:** Platform Administrator

Purpose:
Review an escalated payment case requiring platform-level verification/support.

Important rules:

- PaymentIntent state remains independent;
- ordinary facility users cannot force payment transitions;
- Platform Administrator reviewing an escalation does not imply arbitrary manual rewriting of gateway truth;
- do not add Payment Gateway as an Actor to this Use Case without an explicitly defined direct interaction.

---

## PAUC-17 — Review Conflict Escalation

**Primary Actor:** Platform Administrator

Purpose:
Review an escalated booking/conflict case when facility-level resolution cannot be safely completed.

The facility/reception side owns normal operational resolution.

Platform review/support does not authorize pulling extra internal facility capacity into an already published Aafiatak release.

---

## PAUC-18 — Review Audit Logs

**Primary Actor:** Platform Administrator

Purpose:
Review audit records when required.

Important:

- important operational changes are audited with actor/time/reason where applicable;
- Platform Administrator may review audit records;
- ordinary users cannot tamper with audit history;
- this Use Case does **not** imply permission to delete/rewrite audit history.

---

## PAUC-19 — Provide Technical Support

**Primary Actor:** Platform Administrator

Purpose:
Provide documented technical support for approved platform/facility issues.

Boundary:

Aafiatak support may assist with setup or technical support, but does not become responsible for the correctness of facility:

- schedules;
- prices;
- doctors;
- services;
- daily bookings;
- daily queue.

Any exceptional support-side modification must be authorized and audited.

---

## PAUC-20 — View Platform Indicators

**Primary Actor:** Platform Administrator

Purpose:
View approved general platform indicators.

The authoritative platform dashboard specifically supports general:

- booking indicators;
- payment indicators;
- availability-accuracy indicators.

Do not expand this into unrestricted advanced analytics/BI unless separately approved.

---

# 6. Exact Actor–Use Case Association Matrix

This matrix is authoritative for the Platform Administrator Package.

## Platform Administrator

Associate directly with:

- PAUC-01 Log In
- PAUC-03 Review Facility Onboarding Request
- PAUC-04 Request Additional Information
- PAUC-05 Approve Facility
- PAUC-06 Reject Facility
- PAUC-07 Activate Facility
- PAUC-08 Suspend Facility
- PAUC-09 Provision Initial Facility Administrator
- PAUC-10 Manage Cities
- PAUC-11 Manage Regions
- PAUC-12 Manage Facility Types
- PAUC-13 Manage Public Reference Lists
- PAUC-14 Manage Platform Staff Accounts
- PAUC-15 Review Technical Escalation
- PAUC-16 Review Payment Escalation
- PAUC-17 Review Conflict Escalation
- PAUC-18 Review Audit Logs
- PAUC-19 Provide Technical Support
- PAUC-20 View Platform Indicators

Do **not** directly associate Platform Administrator with:

- PAUC-02 Verify WhatsApp OTP

because PAUC-02 is a mandatory helper included by Log In.

Therefore:

**Platform Administrator direct Associations = 19**

## WhatsApp Authentication Provider

Associate only with:

- PAUC-02 Verify WhatsApp OTP

Therefore:

**WhatsApp Authentication Provider Associations = 1**

## Total Actor Associations

**20**

No other direct Actor Associations are approved.

---

# 7. Exact UML Relationships

Use exactly **one `<<include>>` relationship**.

There are:

- **0 `<<extend>>`**
- **0 Generalization**

## PAINC-01

**Log In** `<<include>>` **Verify WhatsApp OTP**

Direction:

`PAUC-01 → PAUC-02`

Reason:
Every Platform Administrator authentication execution requires valid passwordless WhatsApp OTP verification.

---

# 8. Relationships Deliberately NOT Added

Every plausible relationship below was reviewed against the lecturer's UML rules.

## 8.1 No onboarding workflow arrows

Do not draw:

- Review Request → Request Additional Information
- Review Request → Approve Facility
- Review Request → Reject Facility
- Approve Facility → Activate Facility
- Activate Facility → Provision Initial Facility Administrator

as ordinary sequence arrows.

They describe workflow/progression and belong to later Use Case Modeling / Activity / Sequence work.

## 8.2 No `Request Additional Information <<extend>> Review Facility Onboarding Request`

Although requesting more information is conditional during review, modeling it as `extend` would primarily express an onboarding decision branch rather than a separately established extension relationship.

The approved detailed inventory treats both as meaningful Platform Administrator operations.

Keep them separate.

## 8.3 No `Approve Facility <<include>> Activate Facility`

Approval and activation are explicitly distinct actions in the authoritative scope.

A facility may be approved before activation/provisioning is completed.

Do not collapse them.

## 8.4 No `Activate Facility <<include>> Provision Initial Facility Administrator`

Initial onboarding normally involves both activation and initial admin provisioning.

However, the product model does not prove that **every** execution of `Activate Facility` must provision a brand-new initial administrator, especially after a later suspension/reactivation.

Therefore `include` would be too strong.

## 8.5 No Generalization between admin roles

Do not model:

- Platform Administrator → Facility Administrator
- Platform Administrator → Admin
- Facility Administrator → Platform Administrator

These are different operational roles with different authority boundaries, not Actor inheritance.

## 8.6 No Payment Gateway relation to Review Payment Escalation

`Review Payment Escalation` is platform support/oversight.

It is not equivalent to:
- Verify Payment Result;
- Process Full Payment;
- Process Refund.

Those gateway interactions belong to financial/system modeling.

## 8.7 No cross-package operational relationships

Do not connect Platform Administrator directly to:
- Cancel Appointment;
- Reschedule Appointment;
- Manage Queue;
- Record Visit State;
- Manage Facility Availability;
- Add Doctor;
- Edit Service Offering.

Those belong to facility roles.

---

# 9. Traceability to Main Overview

This detailed package expands the approved Main Overview Platform Administrator goals.

## `MUC-04 — Log In`

- PAUC-01 Log In
- PAUC-02 Verify WhatsApp OTP

## `MUC-27 — Manage Facility Onboarding`

- PAUC-03 Review Facility Onboarding Request
- PAUC-04 Request Additional Information
- PAUC-05 Approve Facility
- PAUC-06 Reject Facility
- PAUC-07 Activate Facility
- PAUC-08 Suspend Facility
- PAUC-09 Provision Initial Facility Administrator

## `MUC-28 — Manage Platform Reference & Staff Data`

- PAUC-10 Manage Cities
- PAUC-11 Manage Regions
- PAUC-12 Manage Facility Types
- PAUC-13 Manage Public Reference Lists
- PAUC-14 Manage Platform Staff Accounts

## `MUC-29 — Handle Support & Escalations`

- PAUC-15 Review Technical Escalation
- PAUC-16 Review Payment Escalation
- PAUC-17 Review Conflict Escalation
- PAUC-19 Provide Technical Support
- PAUC-20 View Platform Indicators

`View Platform Indicators` is retained under support/oversight in the detailed package while remaining a platform-level oversight capability.

## `MUC-30 — Review Audit Logs`

- PAUC-18 Review Audit Logs

---

# 10. Explicit Platform Administrator Restrictions

The package must NOT contain or imply:

- `FacilityApplicant` Actor;
- public facility self-service registration portal;
- public Platform Administrator self-registration;
- password login;
- Forgot Password / Reset Password;
- SMS authentication;
- general WhatsApp messaging/notifications;
- facility doctor creation on behalf of a facility;
- facility service creation/editing on behalf of a facility;
- facility schedule management;
- facility AvailabilityRelease creation;
- Arrival Group management;
- facility capacity withdrawal/freeze/close as daily operations;
- facility price changes;
- facility booking/payment/refund policy changes;
- facility staff-account management;
- daily appointment search/reschedule/cancellation operation;
- daily check-in;
- daily queue operation;
- visit-state updates;
- no-show recording;
- Doctor calling/queue operation;
- arbitrary Payment Gateway outcome overwrite;
- direct refund fabrication;
- partial-refund engine;
- delete/tamper with audit history;
- clinical content;
- diagnosis;
- prescriptions;
- medical records;
- laboratory/radiology operational workflow;
- insurance workflow;
- unrestricted advanced analytics.

---

# 11. Critical Domain Rules Relevant to Platform Administration

## 11.1 Platform/facility separation

Platform Administration owns:

- onboarding;
- platform reference data;
- platform staff;
- support/escalation oversight;
- audit review;
- platform indicators.

Facilities own their:

- doctors;
- services;
- prices;
- policies;
- schedules;
- availability;
- facility staff;
- daily bookings;
- daily queue.

## 11.2 Suspension preserves history

Suspending a facility:

- blocks new holds/bookings;
- blocks new availability publication;
- releases active temporary holds;
- preserves confirmed appointments/history;
- requires documented operational resolution of existing confirmed appointments;
- does not silently delete historical operations.

## 11.3 Platform support does not replace facility ownership

Aafiatak support may help with setup/technical issues.

It does not become responsible for facility data correctness.

Exceptional support-side modifications must be:
- authorized;
- audited.

## 11.4 Audit integrity

Platform Administrator may review audit logs.

Important changes to:
- capacity;
- policies;
- appointments;
- payments/refunds;
- visits;
- operational exceptions;
- staff accounts/permissions

are auditable.

Review authority does not mean deletion/rewrite authority.

## 11.5 Payment escalation remains controlled

Payment states follow verified payment/reconciliation events.

Platform support may review/escalate exceptional cases but must not treat an ordinary manual edit as equivalent to trusted gateway truth.

---

# 12. Granularity Decisions

Potential additions/merges were reviewed.

## 12.1 Keep Approve and Reject separate

Both are explicitly preserved in the approved detailed inventory and represent distinct platform administrator decisions.

## 12.2 Keep Activate and Suspend separate

They have materially different platform effects and are explicitly preserved.

## 12.3 Keep Cities, Regions, Facility Types, and Public Reference Lists separate

The approved detailed inventory explicitly lists all four.

`Manage Public Reference Lists` must therefore be understood as the broader/residual public-reference responsibility rather than collapsing the named categories.

## 12.4 Do not split Manage Platform Staff Accounts into CRUD micro-use-cases

The authoritative scope only establishes the aggregate platform-staff management responsibility.

Do not invent:
- Add Platform Staff
- Edit Platform Staff
- Disable Platform Staff
- Assign Platform Role
as separate ellipses unless future scope explicitly approves this detail.

## 12.5 No separate `Reactivate Facility`

The authoritative operation is `Activate Facility`.

Do not invent another lifecycle Use Case merely for a possible post-suspension scenario.

## 12.6 No separate `Delete Facility`

Not supported.

Suspension/disable/archive and audit preservation are the governing safety patterns.

## 12.7 No separate `Process Refund`

Platform Administrator may review Payment Escalation but the detailed financial execution belongs to trusted payment/refund processing, not an arbitrary admin action.

## 12.8 No separate `Receive Escalation`

The actor's meaningful goal is modeled as reviewing the specific escalation types.

A system-delivery/messaging micro-step is not promoted to another Use Case.

## 12.9 No `Log Out`

The authoritative Platform Administration scope does not explicitly define a separate user-initiated logout Use Case.

Do not invent it solely for symmetry with Patient.

---

# 13. Visual Composition Requirements

This package contains 20 Use Cases and should normally fit on **one well-composed landscape sheet**.

Unlike Booking & Reception Staff, it does not require multiple sheets by default.

Use five visual neighborhoods:

1. **Authentication**
2. **Facility Onboarding**
3. **Platform Reference Data**
4. **Platform Staff**
5. **Support & Oversight**

These are visual neighborhoods only.

Do not create nested UML packages.

Recommended placement:

- **Platform Administrator:** outside left, vertically centered.
- **WhatsApp Authentication Provider:** outside near Authentication / Verify WhatsApp OTP.

Visual priorities:

- onboarding neighborhood receives the largest area;
- reference data should be compact and aligned;
- support/escalation items should be grouped together;
- keep Log In / OTP local;
- Actor Associations should remain readable;
- no giant connector bus;
- no line through labels;
- no chronology arrows;
- no decorative arrows between onboarding actions.

Because Platform Administrator has 19 direct Associations, a repeated visual symbol of the **same Platform Administrator actor** may be used only if necessary to prevent an unreadable line fan, provided:

- the exact label `Platform Administrator` is repeated;
- it remains one semantic Actor;
- no different permissions are implied;
- repetition is presentation-only.

Prefer one actor symbol first and use careful attachment-point distribution.

---

# 14. Final QA Checklist

## UML Compliance

- [ ] Correct diagram title.
- [ ] Correct System Boundary title.
- [ ] Platform Administrator outside System Boundary.
- [ ] WhatsApp Authentication Provider outside System Boundary.
- [ ] Platform Administrator Package inside System Boundary.
- [ ] Exactly 20 Use Cases.
- [ ] All visible labels are English.
- [ ] Every Use Case name begins with a verb.
- [ ] Platform Administrator has exactly 19 direct Associations.
- [ ] WhatsApp Authentication Provider has exactly 1 Association.
- [ ] Platform Administrator has no direct Association to Verify WhatsApp OTP.
- [ ] Actor Associations are solid plain lines without arrowheads.
- [ ] Exactly 1 `<<include>>`.
- [ ] Include direction is Log In → Verify WhatsApp OTP.
- [ ] 0 `<<extend>>`.
- [ ] 0 Generalization.
- [ ] No chronological arrows.
- [ ] No Class/database/API/component/UI-screen elements.

## Product Compliance

- [ ] Platform Admin account is controlled/provisioned, not public self-registration.
- [ ] Login uses passwordless WhatsApp OTP.
- [ ] SMS/password recovery are absent.
- [ ] No FacilityApplicant Actor.
- [ ] Review/request-more-info/approve/reject are present.
- [ ] Activate Facility is present.
- [ ] Suspend Facility is present.
- [ ] Provision Initial Facility Administrator is present.
- [ ] Suspension blocks new holds/bookings/publication.
- [ ] Suspension releases active holds but preserves confirmed appointments/history.
- [ ] Cities/Regions/Facility Types/Public Reference Lists are present.
- [ ] Platform Staff management is present.
- [ ] Technical/Payment/Conflict escalation reviews are present.
- [ ] Audit-log review is present.
- [ ] Technical support is present.
- [ ] Platform indicators are present.
- [ ] No facility doctors/services management.
- [ ] No facility schedules/prices/policies management.
- [ ] No daily booking/queue operation.
- [ ] No arbitrary payment-result overwrite.
- [ ] No audit deletion/tampering.
- [ ] No clinical/deferred features.

## Visual Compliance

- [ ] One landscape sheet is readable.
- [ ] Five visual neighborhoods are immediately understandable.
- [ ] Authentication relationship is local and obvious.
- [ ] No fake onboarding-flow arrows.
- [ ] No giant actor-association fan dominates the page.
- [ ] No connector crosses labels/ellipses.
- [ ] Typography is readable at report/presentation scale.
- [ ] Diagram looks like an academic UML Use Case figure, not a platform dashboard UI.

---

# 15. Nine-Pass Deep Review Record

## Review 1 — Lecturer / UML Method Audit

Re-read the lecturer's Use Case/Package pages.

Confirmed:
- Use Case Diagram contains Actors, Use Cases, and Relationships;
- the lecturer defines/uses `include`, `extend`, and Generalization;
- the lecturer instructs defining system boundary, actors, Use Cases, and each Use Case separately;
- detailed scenarios use Actors, Preconditions, Postconditions, and steps in later Use Case Modeling;
- the lecturer demonstrates creating Packages for actors in a large restaurant example.

Result:
The Platform Administrator deliverable correctly remains a detailed Use Case Diagram organized through an actor package, not the later formal Package Diagram.

---

## Review 2 — Authoritative Platform Administrator Permission Audit

Rechecked the root product specification's Platform Administrator permissions and dashboard scope.

Confirmed explicit authority to:
- review onboarding requests;
- request additional information;
- approve/reject;
- activate/suspend;
- provision initial Facility Administrator;
- manage cities/regions/facility types/public reference lists;
- manage platform staff;
- review technical/payment/conflict escalations;
- review audit logs;
- provide technical support;
- view platform indicators.

Confirmed prohibitions on:
- facility doctor/service management;
- facility schedules;
- facility prices/policies;
- daily bookings;
- daily queue.

Result:
The preserved platform inventory is strongly grounded in authoritative role permissions.

---

## Review 3 — Authentication & Identity Audit

Rechecked unified identity and authentication rules.

Confirmed:
- Platform Administrator is one of the explicitly passwordless human roles;
- WhatsApp OTP is mandatory;
- SMS is not used;
- Platform Administrator account is provisioned through controlled platform administration;
- it is not publicly registered;
- privileged sessions must be revocable.

Finding:
`docs/use_case.md` Platform Administrator detailed list omitted Login/OTP.

Correction:
Added:
- PAUC-01 Log In
- PAUC-02 Verify WhatsApp OTP
- one `<<include>>`.

---

## Review 4 — Facility Onboarding Lifecycle Audit

Rechecked:
- onboarding dashboard functions;
- approve/reject;
- activate/suspend;
- initial Facility Administrator provisioning;
- absence of FacilityApplicant portal.

Confirmed:
- no FacilityApplicant Actor;
- approval and activation are distinct;
- suspension blocks new holds/bookings/publication;
- suspension releases active holds;
- confirmed appointments/history survive and need documented operational resolution.

Relationship finding:
No onboarding sequence/branch was promoted to UML dependency because the source defines operational progression, not mandatory reusable sub-use-cases for every execution.

Result:
Seven onboarding Use Cases retained with no invented `include`/`extend`.

---

## Review 5 — Platform Reference Data & Staff Audit

Rechecked platform data ownership.

Confirmed platform owns:
- Cities;
- Regions;
- Facility Types;
- public reference data;
- Platform Staff Accounts;
- support records;
- audit log.

Confirmed facility owns:
- doctors;
- services;
- prices;
- schedules;
- facility staff.

Granularity decision:
Keep the four reference-data Use Cases because the approved package inventory explicitly lists them individually.

Do not split Platform Staff management into speculative CRUD operations.

---

## Review 6 — Support / Payment / Conflict Audit

Rechecked support and operational-exception boundaries.

Confirmed:
- Platform Administrator may review technical/payment/conflict escalations;
- platform support may assist but does not take over facility daily operations;
- facility conflict resolution remains primarily facility operational work;
- payment-result transitions remain controlled by verified gateway/reconciliation events;
- no arbitrary admin payment overwrite.

External-actor finding:
`Payment Gateway` is not directly required for `Review Payment Escalation`.

Result:
No Payment Gateway Actor added.

---

## Review 7 — Audit / Indicators / Deferred-Scope Audit

Rechecked audit/security/platform dashboard details.

Confirmed:
- Review Audit Logs is explicit;
- audit history integrity must be preserved;
- platform dashboard may view general booking/payment/availability-accuracy indicators;
- unrestricted advanced analytics are not established;
- clinical features remain out of scope.

Confirmed no:
- audit deletion;
- facility operational takeover;
- clinical content;
- public FacilityApplicant portal;
- general WhatsApp notifications.

---

## Review 8 — UML Relationship Audit

Tested plausible dependencies against lecturer semantics.

Approved only:

**Log In `<<include>>` Verify WhatsApp OTP**

Rejected:
- Review → Request Additional Information
- Review → Approve/Reject
- Approve → Activate
- Activate → Provision Initial Facility Administrator
- escalation workflow arrows
- Payment Gateway association to Review Payment Escalation
- Actor Generalization among admin roles

Important judgment:
`Activate Facility <<include>> Provision Initial Facility Administrator` was rejected because provisioning is mandatory in the initial approved-onboarding path, but not proven mandatory for every possible later activation/reactivation execution.

Result:
- 1 include
- 0 extend
- 0 Generalization

---

## Review 9 — Omission / Granularity / Cross-Package / Visual Audit

Compared Platform Administrator against all other Actor Packages and Main Overview.

Checked possible omissions:
- Log In → added;
- Verify WhatsApp OTP → added;
- Log Out → not explicitly supported;
- platform notifications → not explicit as standalone Platform Admin goal;
- direct refund operation → not supported;
- FacilityApplicant → explicitly excluded;
- direct facility operations → explicitly excluded;
- advanced analytics → not approved.

Cross-package separation confirmed:

- Patient → personal discovery/booking/appointment/visit visibility.
- Facility Administrator → own facility configuration, availability, staff, oversight.
- Booking & Reception Staff → daily bookings/check-in/queue/visit/exceptions.
- Doctor → own appointments/waiting list + call next.
- Platform Administrator → onboarding, platform data/staff, escalations/support, audit, indicators.

Final semantic result:

- Primary human Actor: **1**
- External Actors: **1**
- Use Cases: **20**
- Platform Administrator direct Associations: **19**
- Total Actor Associations: **20**
- `<<include>>`: **1**
- `<<extend>>`: **0**
- Generalization: **0**

No unresolved semantic contradiction blocks diagram implementation.

---

# 16. Final Implementation Contract

The implementation agent must:

- use this file as execution truth for the Platform Administrator Package;
- render exactly 20 approved Use Cases;
- preserve exactly the Actor Association Matrix;
- render exactly one approved `<<include>>`;
- add no `<<extend>>`, Generalization, or chronological arrows;
- keep all Actors outside the System Boundary;
- keep all Use Cases inside `Platform Administrator Package`;
- do not add `FacilityApplicant`;
- preserve strict platform-vs-facility responsibility separation;
- keep all visible labels English;
- use a clean professional one-sheet landscape composition;
- optimize layout without changing UML/product truth;
- leave final visual approval to the user.

