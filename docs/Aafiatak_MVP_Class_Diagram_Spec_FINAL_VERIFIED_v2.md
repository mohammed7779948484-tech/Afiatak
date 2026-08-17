# Aafiatak Medical Appointment Booking System
## MVP Class Diagram — Authoritative Execution Specification
### Final Semantic Verification against Project Specification, Lecturer UML Rules, and Course Notes

**Deliverable:** UML Class Diagram  
**Scope:** Current approved MVP only  
**Visible diagram language:** English only  
**Diagram title:** `Class Diagram — Aafiatak Medical Appointment Booking System (MVP)`  
**Status:** Final semantic specification — ready for diagram implementation

---

# 1. Authority and Conflict Rules

Use this precedence:

1. `Aafiatak_Project_Specification_EN.md` — authoritative product truth.
2. Lecturer UML PDF, especially pages 3–5 — academic Class Diagram notation and course expectations.
3. Lecturer/course notes supplied for this project — additional interpretation rules.
4. Approved Aafiatak Use Case / Actor Package / Use Case Modeling work — behavioral traceability.
5. This file — exact execution contract for the MVP Class Diagram.
6. Drawing/rendering tooling — presentation only.

If a product rule is not supported by the authoritative specification, do not invent it.

Do not add Deferred / Out-of-Scope features.

Do not resolve an item explicitly marked as an open decision.

---

# 2. Lecturer/Class-Diagram Rules Applied

The lecturer treats the Class Diagram as a structural/static model of system information.

A class may contain four compartments:

1. **Class Name**
2. **Attributes**
3. **Operations**
4. **Responsibility**

Use visibility notation in the same spirit as the lecturer examples:

- `+` public
- `-` private
- `#` protected, only if genuinely needed

For this analysis-stage diagram:

- **Do not show programming data types** (`String`, `Integer`, etc.). The lecturer stated that implementation types are not required at the modeling stage.
- Keep attributes conceptual and domain-relevant.
- Use concise operations that express domain behavior, not UI button names.
- Responsibilities are short semantic statements, not paragraphs.
- Show multiplicity at both ends of relationships wherever meaningful.
- Use relationship notation correctly:
  - **Association:** solid line.
  - **Aggregation:** hollow diamond `◇` at the whole.
  - **Composition:** filled diamond `◆` at the lifecycle-owning whole.
  - **Generalization:** solid line with open triangle toward the parent — use only if genuine inheritance exists.
  - **Dependency:** dashed arrow for a temporary/use dependency — do not invent one merely to add variety.
  - **Realization:** dashed line/open triangle only for an actual Interface implementation.

## Important modeling decision

This deliverable is a **domain/entity Class Diagram**, not a UI or implementation class diagram.

The lecturer notes that classes may be Entity, Boundary, Control, or Abstract. For the current project deliverable, the authoritative specification gives a strong domain model, so this diagram focuses on **domain/entity classes**.

Do **not** add:
- Flutter screens;
- web pages;
- controllers;
- API classes;
- repositories;
- database tables as technical boxes;
- Payment Gateway / Notification Service / Map Service / WhatsApp Provider as domain classes.

Those belong to later Sequence / Component / implementation modeling.

---

# 3. Critical Identity Modeling Rule

Do **not** model `Patient`, `FacilityUser`, or `Doctor` as subclasses of `User`.

Reason:

The authoritative project explicitly permits one verified `User` identity to hold more than one legitimate role/profile. Role-specific data is separated through related profile/role records rather than duplicate identities.

Therefore use **Associations**, not inheritance, between `User` and the role/profile classes.

This Class Diagram has:

- **0 approved Generalization relationships**
- **0 approved Realization relationships**

Do not invent inheritance just because Generalization exists in UML.

---

# 4. Exact Class Inventory

Render exactly these **30 classes**.

IDs below are traceability metadata only. Do not display IDs in class boxes.

---

## 4.1 Identity & Access

### C01 — User

**Attributes**
- `- userId`
- `- normalizedPhone`
- `- phoneVerifiedAt`
- `- accountStatus`

**Operations**
- `+ requestOtp()`
- `+ verifyOtp()`
- `+ revokeSession()`

**Responsibility**
Maintain the globally unique verified human identity and authentication state.

---

### C02 — Patient

**Attributes**
- `- patientId`
- `- fullName`
- `- basicProfileData`
- `- active`

**Operations**
- `+ updateProfile()`
- `+ viewOwnAppointments()`

**Responsibility**
Represent Patient-specific non-clinical profile data linked to one User identity.

---

### C03 — FacilityUser

**Attributes**
- `- facilityUserId`
- `- role`
- `- status`
- `- permissions`

**Operations**
- `+ assignApprovedRole()`
- `+ enable()`
- `+ disable()`

**Responsibility**
Represent a provisioned User's role and access inside one participating Facility.

**Constraint**
Approved facility roles include Facility Administrator, Booking & Reception Staff, and Doctor access. This is not an arbitrary custom-role designer.

---

### C04 — PlatformRoleAssignment

**Attributes**
- `- assignmentId`
- `- role`
- `- status`
- `- permissions`

**Operations**
- `+ assignApprovedRole()`
- `+ enable()`
- `+ disable()`

**Responsibility**
Represent a controlled platform-role relationship for a User, including Platform Administrator/platform-staff access.

**Constraints**
- Platform roles are provisioned through the controlled platform-administration process.
- They are not created through public self-registration.
- This class completes the authoritative identity rule that role-specific data is separated through Patient, FacilityUser, Doctor, and platform-role relationships.

---

# 4.2 Platform & Oversight

### C05 — FacilityOnboardingRequest

**Attributes**
- `- requestId`
- `- status`
- `- submittedAt`
- `- decisionAt`

**Operations**
- `+ requestAdditionalInformation()`
- `+ approve()`
- `+ reject()`

**Responsibility**
Preserve the platform-side intake/review decision for facility onboarding.

**Constraint**
No public `FacilityApplicant` portal/actor is introduced.

---

### C06 — AuditRecord

**Attributes**
- `- auditId`
- `- action`
- `- timestamp`
- `- reason`
- `- source`

**Operations**
- `+ recordChange()`

**Responsibility**
Preserve auditable actor/time/reason/source information for important changes.

---

### C07 — Notification

**Attributes**
- `- notificationId`
- `- type`
- `- status`
- `- createdAt`
- `- deliveredAt`

**Operations**
- `+ markDelivered()`
- `+ markFailed()`

**Responsibility**
Represent approved in-application/system notification records.

**Constraint**
General notifications are not WhatsApp/SMS messages in the current scope.

---

# 4.3 Platform Reference Data

### C08 — Region

**Attributes**
- `- regionId`
- `- name`
- `- active`

**Operations**
- `+ activate()`
- `+ deactivate()`

**Responsibility**
Provide platform-level region reference data.

---

### C09 — City

**Attributes**
- `- cityId`
- `- name`
- `- active`

**Operations**
- `+ activate()`
- `+ deactivate()`

**Responsibility**
Provide platform-level city reference data inside a Region.

---

### C10 — FacilityType

**Attributes**
- `- facilityTypeId`
- `- name`
- `- active`

**Operations**
- `+ activate()`
- `+ deactivate()`

**Responsibility**
Classify participating Facilities using platform reference data.

---

# 4.4 Facility & Medical Offering

### C11 — Facility

**Attributes**
- `- facilityId`
- `- name`
- `- status`
- `- contactNumber`
- `- workingHours`

**Operations**
- `+ updateProfile()`
- `+ activate()`
- `+ suspend()`

**Responsibility**
Represent the participating health facility account without replacing its internal HIS/scheduling system.

---

### C12 — FacilityBranch

**Attributes**
- `- branchId`
- `- name`
- `- address`
- `- mapLocation`
- `- contactNumber`
- `- localTimeZone`

**Operations**
- `+ updateContactData()`
- `+ updateWorkingHours()`

**Responsibility**
Represent the branch context in which bookings, releases, and local-time rules are interpreted.

---

### C13 — Department

**Attributes**
- `- departmentId`
- `- name`
- `- active`

**Operations**
- `+ activate()`
- `+ deactivate()`

**Responsibility**
Provide a platform reference Department that Facilities may associate with themselves.

---

### C14 — Specialty

**Attributes**
- `- specialtyId`
- `- name`
- `- active`

**Operations**
- `+ activate()`
- `+ deactivate()`

**Responsibility**
Provide a platform reference Specialty associated with Facilities, Doctors, and services.

---

### C15 — Doctor

**Attributes**
- `- doctorId`
- `- name`
- `- photo`
- `- qualification`
- `- biography`
- `- active`

**Operations**
- `+ updateProfile()`
- `+ linkLoginAccess()`

**Responsibility**
Represent the Doctor's public/operational profile separately from the User authentication identity.

---

### C16 — ServiceOffering

**Attributes**
- `- serviceOfferingId`
- `- serviceName`
- `- amount`
- `- currency`
- `- estimatedDuration`
- `- bookingPolicy`
- `- cancellationPolicy`
- `- cancellationWindow`
- `- noShowPolicy`
- `- reconfirmationEnabled`
- `- attendanceInstructions`
- `- active`

**Operations**
- `+ setAmount()`
- `+ setBookingPolicy()`
- `+ configurePolicies()`
- `+ activate()`

**Responsibility**
Define the authoritative service terms used to prepare new AvailabilityRelease records.

**Constraints**
- booking policy is exactly `FULL_PAYMENT_REQUIRED` or `PAY_AT_FACILITY`;
- no deposit or partial-payment concept exists.

---

# 4.5 Schedule & Digital Availability

### C17 — DoctorSchedule

**Attributes**
- `- scheduleId`
- `- dayOrDate`
- `- startTime`
- `- endTime`
- `- active`

**Operations**
- `+ defineWindow()`
- `+ updateWindow()`

**Responsibility**
Represent theoretical/basic Doctor working windows before digital availability is published.

---

### C18 — ScheduleException

**Attributes**
- `- scheduleExceptionId`
- `- date`
- `- type`
- `- reason`
- `- status`

**Operations**
- `+ recordException()`
- `+ deactivate()`

**Responsibility**
Represent a planned leave, closure, or planned scheduling exception before publication.

---

### C19 — AvailabilityRelease

**Attributes**
- `- releaseId`
- `- date`
- `- receptionPeriod`
- `- published`
- `- held`
- `- confirmed`
- `- withdrawnToFacility`
- `- /remaining`
- `- amountSnapshot`
- `- currencySnapshot`
- `- bookingPolicySnapshot`
- `- cancellationPolicySnapshot`
- `- cancellationWindowSnapshot`
- `- noShowPolicySnapshot`
- `- state`
- `- lastUpdatedAt`

**Operations**
- `+ publish()`
- `+ freeze()`
- `+ close()`
- `+ cancel()`
- `+ calculateRemaining()`

**Responsibility**
Own the bounded digital capacity allocated to Aafiatak for one branch/doctor/service/date/session.

**Constraints**
- `/remaining = published - held - confirmed - withdrawnToFacility`
- `published` cannot increase after publication.
- `DRAFT -> PUBLISHED`
- `PUBLISHED <-> FROZEN`
- `PUBLISHED/FROZEN -> CLOSED | CANCELLED`
- `CLOSED` and `CANCELLED` are terminal for new booking.
- terms are frozen when published.

---

### C20 — ArrivalGroup

**Attributes**
- `- arrivalGroupId`
- `- sequence`
- `- startAt`
- `- endAt`
- `- capacity`
- `- held`
- `- confirmed`
- `- withdrawnToFacility`
- `- /remaining`
- `- state`

**Operations**
- `+ isBookable()`
- `+ freeze()`
- `+ close()`
- `+ calculateRemaining()`

**Responsibility**
Represent one sequential arrival window inside an AvailabilityRelease.

**Constraints**
- sum of group capacities equals the release's published capacity.
- `/remaining = capacity - held - confirmed - withdrawnToFacility`
- states: `OPEN`, `FROZEN`, `CLOSED`.
- an ArrivalGroup is an arrival window, not an exact doctor-entry time.

---

### C21 — CapacityWithdrawal

**Attributes**
- `- withdrawalId`
- `- quantity`
- `- source`
- `- reason`
- `- occurredAt`

**Operations**
- `+ execute()`

**Responsibility**
Record the atomic one-way transfer of valid unused Aafiatak capacity to the Facility's internal schedule.

**Constraints**
- quantity must not exceed valid remaining capacity.
- active held capacity cannot be withdrawn.
- confirmed capacity cannot be withdrawn.
- no reverse withdrawal exists.
- no `+1` capacity increase exists.

---

### C22 — ReservationHold

**Attributes**
- `- reservationHoldId`
- `- state`
- `- createdAt`
- `- expiresAt`
- `- idempotencyKey`

**Operations**
- `+ consume()`
- `+ expire()`
- `+ release()`
- `+ isActive()`

**Responsibility**
Temporarily protect exactly one valid booking capacity unit against double booking.

**Constraints**
- states: `ACTIVE`, `CONSUMED`, `EXPIRED`, `RELEASED`.
- terminal after `CONSUMED`, `EXPIRED`, or `RELEASED`.
- must not be consumed at/after ArrivalGroup start.
- exact default duration remains an open decision and must not be invented.

---

### C23 — AvailabilityAlertSubscription

**Attributes**
- `- subscriptionId`
- `- targetDate`
- `- status`
- `- createdAt`
- `- lastNotifiedAt`

**Operations**
- `+ markNotified()`
- `+ expire()`

**Responsibility**
Record Patient interest in returned availability without reserving capacity or granting priority.

**Constraints**
- not a reservation;
- no capacity protection;
- no queue position;
- no priority.

---

# 4.6 Appointment & Payment

### C24 — Appointment

**Attributes**
- `- appointmentId`
- `- status`
- `- bookingNumber`
- `- verificationToken`
- `- confirmedAt`
- `- amountSnapshot`
- `- currencySnapshot`
- `- bookingPolicySnapshot`
- `- cancellationPolicySnapshot`
- `- cancellationWindowSnapshot`
- `- noShowPolicySnapshot`
- `- arrivalWindowSnapshot`

**Operations**
- `+ cancelByPatient()`
- `+ cancelByFacility()`
- `+ reschedule()`
- `+ reconfirmAttendance()`

**Responsibility**
Represent the confirmed booking commitment and preserve its historical booking terms.

**Constraints**
- states: `CONFIRMED`, `CANCELLED_BY_PATIENT`, `CANCELLED_BY_FACILITY`.
- rescheduling keeps status `CONFIRMED` and writes history.
- no pending manual approval/rejected-booking state.

---

### C25 — AppointmentStatusHistory

**Attributes**
- `- historyId`
- `- previousSchedulingData`
- `- newSchedulingData`
- `- changedAt`
- `- reason`

**Operations**
- `+ recordChange()`

**Responsibility**
Preserve auditable appointment cancellation/rescheduling history without rewriting the original record.

---

### C26 — PaymentIntent

**Attributes**
- `- paymentIntentId`
- `- amount`
- `- currency`
- `- state`
- `- externalReference`
- `- createdAt`
- `- expiresAt`
- `- idempotencyKey`

**Operations**
- `+ markProcessing()`
- `+ verifyResult()`
- `+ markUnderReview()`
- `+ startRefund()`
- `+ markRefunded()`

**Responsibility**
Represent the independent full electronic payment/refund lifecycle for `FULL_PAYMENT_REQUIRED`.

**Constraints**
- no PaymentIntent exists for `PAY_AT_FACILITY`.
- at most one non-terminal PaymentIntent may be active for one ReservationHold.
- states: `CREATED`, `PROCESSING`, `SUCCEEDED`, `FAILED`, `EXPIRED`, `UNDER_REVIEW`, `REFUND_PENDING`, `REFUNDED`.
- refund is full collected amount or zero; no partial refund engine.

---

# 4.7 Visit, Queue & Operational Exceptions

### C27 — VisitInstance

**Attributes**
- `- visitInstanceId`
- `- status`
- `- arrivalTime`
- `- serviceStart`
- `- serviceEnd`
- `- lateAccepted`

**Operations**
- `+ checkIn()`
- `+ startService()`
- `+ complete()`
- `+ markNotCompleted()`
- `+ markNoShow()`
- `+ correctCheckIn()`

**Responsibility**
Represent what actually happens operationally on the service day, separately from Appointment status.

**Constraints**
- states: `CREATED`, `CHECKED_IN`, `IN_SERVICE`, `COMPLETED`, `NOT_COMPLETED`, `NO_SHOW`.
- facility staff, not Doctor, changes visit states.
- terminal outcomes: `COMPLETED`, `NOT_COMPLETED`, `NO_SHOW`.

---

### C28 — QueueEntry

**Attributes**
- `- queueEntryId`
- `- status`
- `- createdAt`
- `- calledAt`
- `- completedAt`
- `- manualHandling`

**Operations**
- `+ call()`
- `+ markDone()`
- `+ remove()`

**Responsibility**
Represent the Patient's lightweight Aafiatak queue presence inside an ArrivalGroup.

**Constraints**
- states: `WAITING`, `CALLED`, `DONE`, `REMOVED`.
- `DONE` and `REMOVED` are terminal.
- accepted late Patient uses `manualHandling`; this is not a new queue status.
- no automatic re-entry/requeue state.

---

### C29 — OperationalException

**Attributes**
- `- operationalExceptionId`
- `- type`
- `- status`
- `- openedAt`
- `- closedAt`
- `- reason`

**Operations**
- `+ open()`
- `+ recordAffectedAppointmentOutcome()`
- `+ close()`

**Responsibility**
Represent an unplanned post-publication/daily-operation event and require documented outcomes for affected appointments.

**Supported types**
- `DOCTOR_DELAYED`
- `DOCTOR_ABSENT`
- `SESSION_CANCELLED`
- `FACILITY_CLOSED`
- `CAPACITY_REDUCED`
- `POWER_OR_CONNECTIVITY_OUTAGE`
- `CONFLICT_DETECTED`

**Constraint**
Do not close until the action/outcome for every affected Appointment has been recorded.

---

### C30 — OperationalExceptionResolution

**Attributes**
- `- resolutionId`
- `- action`
- `- outcome`
- `- recordedAt`
- `- reason`

**Operations**
- `+ recordOutcome()`
- `+ updateOutcome()`

**Responsibility**
Preserve the documented action and outcome for one Appointment affected by one OperationalException.

**Constraints**
- Every affected confirmed Appointment must have a documented resolution before the parent OperationalException can close.
- Approved outcomes may include an agreed equivalent alternative, facility-side cancellation/full refund when applicable, or documented escalation.
- This is a domain resolution record, not a silent delete or an imported internal-capacity workaround.

---

# 5. Exact Relationship Matrix

Render exactly the following semantic relationships unless a purely visual duplicate would repeat the same relation.

Multiplicity notation must be visible.

| ID | Class A | Multiplicity A | Relationship | Class B | Multiplicity B | Meaning |
|---|---|---:|---|---|---:|---|
| R01 | User | 1 | Association | Patient | 0..1 | User may own one Patient profile |
| R02 | User | 1 | Association | FacilityUser | 0..* | User may hold provisioned facility-role records |
| R03 | User | 1 | Association | PlatformRoleAssignment | 0..* | User may hold controlled platform-role assignments |
| R04 | Facility | 1 | Association | FacilityUser | 0..* | Facility owns its provisioned facility memberships |
| R05 | Doctor | 0..1 | Association | FacilityUser | 0..1 | Optional one-to-one Doctor login link; non-Doctor FacilityUser records do not participate |
| R06 | User | 1 | Association | Notification | 0..* | User receives notification records |
| R07 | User | 0..1 | Association | AuditRecord | 0..* | Audit may reference a human actor; system-generated events may have no User actor |
| R08 | FacilityOnboardingRequest | 1 | Association | Facility | 0..1 | Approved request may result in one activated Facility |
| R09 | Region | 1 | Association | City | 0..* | Region contains reference cities |
| R10 | City | 1 | Association | FacilityBranch | 0..* | Branch belongs to one City |
| R11 | FacilityType | 1 | Association | Facility | 0..* | Facility has one platform FacilityType |
| R12 | Facility | 1 | **Composition** | FacilityBranch | 1..* | Branch is a structural part of its Facility |
| R13 | Facility | 0..* | **Aggregation** | Department | 0..* | Facility selects independent Department references |
| R14 | Facility | 0..* | **Aggregation** | Specialty | 0..* | Facility selects independent Specialty references |
| R15 | Facility | 1 | Association | Doctor | 0..* | Pilot Doctors belong to participating Facility context |
| R16 | Specialty | 1 | Association | Doctor | 0..* | Doctor has a Specialty |
| R17 | Department | 1 | Association | Doctor | 0..* | Doctor belongs to a Department in current profile |
| R18 | FacilityBranch | 1 | Association | ServiceOffering | 0..* | ServiceOffering is offered at one Branch |
| R19 | Department | 1 | Association | ServiceOffering | 0..* | ServiceOffering belongs to one Department |
| R20 | Specialty | 1 | Association | ServiceOffering | 0..* | ServiceOffering is classified by one Specialty |
| R21 | Doctor | 0..* | Association | ServiceOffering | 0..* | Doctors may provide multiple services and vice versa |
| R22 | Doctor | 1 | Association | DoctorSchedule | 0..* | Doctor has working windows |
| R23 | FacilityBranch | 1 | Association | DoctorSchedule | 0..* | Schedule is interpreted in Branch context |
| R24 | DoctorSchedule | 0..1 | Association | ScheduleException | 0..* | Planned exception may affect a Doctor schedule |
| R25 | FacilityBranch | 1 | Association | ScheduleException | 0..* | Planned exception belongs to Branch operational context |
| R26 | FacilityBranch | 1 | Association | AvailabilityRelease | 0..* | Release is for one Branch |
| R27 | Doctor | 1 | Association | AvailabilityRelease | 0..* | Release is for one Doctor |
| R28 | ServiceOffering | 1 | Association | AvailabilityRelease | 0..* | Release freezes terms from one ServiceOffering |
| R29 | AvailabilityRelease | 1 | **Composition** | ArrivalGroup | 1..* | ArrivalGroups exist inside one Release |
| R30 | AvailabilityRelease | 1 | **Composition** | CapacityWithdrawal | 0..* | Withdrawal belongs to one Release |
| R31 | ArrivalGroup | 0..1 | Association | CapacityWithdrawal | 0..* | Withdrawal may target a specific group |
| R32 | Patient | 1 | Association | ReservationHold | 0..* | Patient may create holds over time |
| R33 | ArrivalGroup | 1 | Association | ReservationHold | 0..* | Hold fixes exactly one ArrivalGroup |
| R34 | Patient | 1 | Association | AvailabilityAlertSubscription | 0..* | Patient may subscribe to availability |
| R35 | ServiceOffering | 1 | Association | AvailabilityAlertSubscription | 0..* | Subscription is for a service context |
| R36 | Doctor | 0..1 | Association | AvailabilityAlertSubscription | 0..* | Subscription may narrow to one Doctor |
| R37 | AvailabilityRelease | 0..1 | Association | AvailabilityAlertSubscription | 0..* | Subscription may target a specific Release |
| R38 | Patient | 1 | Association | Appointment | 0..* | Patient owns appointments |
| R39 | FacilityBranch | 1 | Association | Appointment | 0..* | Appointment belongs to Branch |
| R40 | Doctor | 1 | Association | Appointment | 0..* | Appointment is assigned to Doctor |
| R41 | ServiceOffering | 1 | Association | Appointment | 0..* | Appointment snapshots one ServiceOffering |
| R42 | ArrivalGroup | 1 | Association | Appointment | 0..* | Appointment is confirmed into one ArrivalGroup |
| R43 | Appointment | 1 | **Composition** | AppointmentStatusHistory | 0..* | History exists as part of Appointment lifecycle |
| R44 | ReservationHold | 1 | Association | PaymentIntent | 0..* | Electronic attempts originate from one hold |
| R45 | Appointment | 0..1 | Association | PaymentIntent | 0..* | Successful/reconciled intent may link to Appointment |
| R46 | Appointment | 1 | **Composition** | VisitInstance | 0..1 | Actual service-day occurrence belongs to Appointment |
| R47 | VisitInstance | 1 | **Composition** | QueueEntry | 0..* | Visit may have historical queue entries; at most one active |
| R48 | ArrivalGroup | 1 | Association | QueueEntry | 0..* | QueueEntry operates inside original ArrivalGroup |
| R49 | Doctor | 0..1 | Association | OperationalException | 0..* | Exception may concern one Doctor |
| R50 | AvailabilityRelease | 0..1 | Association | OperationalException | 0..* | Exception may concern one Release/session |
| R51 | OperationalException | 1 | **Composition** | OperationalExceptionResolution | 0..* | Resolution records are lifecycle-owned by one OperationalException |
| R52 | Appointment | 1 | Association | OperationalExceptionResolution | 0..* | Each resolution documents the outcome for one affected Appointment |

---

# 6. Relationship Decisions That Must NOT Be Changed

## 6.1 No User inheritance tree

Do not draw:

`User <|-- Patient`  
`User <|-- FacilityAdministrator`  
`User <|-- Doctor`  
`User <|-- PlatformAdministrator`

The real identity model allows the same User to hold multiple roles/profiles.

Use Associations/RBAC relationships instead.

## 6.2 No database/ERD foreign-key diagram

This is a conceptual UML Class Diagram.

Do not turn every attribute into:
- `xxxId : UUID`
- PK/FK labels;
- SQL column types;
- junction-table classes solely because a relational database would need them.

The lecturer explicitly distinguishes modeling from later implementation detail.

IDs may remain as conceptual identity attributes, but do not show database key icons or table notation.

## 6.3 Do not model external services as entity classes

Do not create classes for:
- Payment Gateway
- Notification Service
- Map Service
- WhatsApp Authentication Provider

Their interactions are modeled later in Sequence/Component diagrams.

`PaymentIntent` and `Notification` are Aafiatak domain records; the external providers are not.

## 6.4 No false Composition

Use Composition only for lifecycle-owned parts approved in this file:

- Facility ◆ FacilityBranch
- AvailabilityRelease ◆ ArrivalGroup
- AvailabilityRelease ◆ CapacityWithdrawal
- Appointment ◆ AppointmentStatusHistory
- Appointment ◆ VisitInstance
- VisitInstance ◆ QueueEntry
- OperationalException ◆ OperationalExceptionResolution

Do not turn every "has" relationship into Composition.

## 6.5 No false Aggregation

Use Aggregation only for the platform reference relationships explicitly approved here:

- Facility ◇ Department
- Facility ◇ Specialty

These references exist independently of a particular Facility.

---

# 7. Domain Invariants to Display as UML Notes

Add concise UML Notes near the relevant clusters. Do not put these as new classes.

### Note N1 — Identity
`One normalized verified phone identifies one User. The same User may hold multiple approved roles/profiles.`

### Note N2 — Capacity
`remaining = published - held - confirmed - withdrawnToFacility`
`published cannot increase after PUBLISHED.`

### Note N3 — Arrival Groups
`New holds use the earliest currently bookable ArrivalGroup. Patients do not choose an arbitrary group.`

### Note N4 — Hold
`ReservationHold protects one capacity unit and ends as CONSUMED, EXPIRED, or RELEASED. Exact default duration remains open.`

### Note N5 — Booking Policy
`ServiceOffering policy is exactly FULL_PAYMENT_REQUIRED or PAY_AT_FACILITY. No deposit/partial payment.`

### Note N6 — Independent Lifecycles
`ReservationHold, Appointment, PaymentIntent, VisitInstance, and QueueEntry states are independent and must not be collapsed.`

### Note N7 — Payment
`PAY_AT_FACILITY creates no PaymentIntent. Refund is full collected amount or zero.`

### Note N8 — Late Arrival
`Accepted late Patient keeps the original Appointment/ArrivalGroup and uses manual queue handling; no auto-transfer or re-entry.`

### Note N9 — Operational Exception
`OperationalException cannot close until every affected Appointment has a documented action/outcome.`

### Note N10 — Scope
`Aafiatak is not an HIS/EHR/cashier/accounting/full internal scheduling system and stores no clinical record content.`

---

# 8. Explicitly Excluded Classes / Concepts

Do not add classes for:

- MedicalRecord
- Diagnosis
- Prescription
- LaboratoryResult
- RadiologyResult
- Insurance
- Pharmacy
- Cashier
- MedicalInvoice
- Salary / HR
- Bed / Room
- InternalFacilitySchedule
- WalkInBooking
- PhoneBooking
- BookingApprovalRequest
- Deposit
- PartialPayment
- RemainingBalance
- Requeue
- LateArrivalGroupTransfer
- Rating / Review
- Complaint
- Chat
- VideoConsultation
- FamilyAccount
- AIRecommendation
- MedicationReminder
- SMS
- PasswordReset
- FacilityApplicant

These are outside the approved current MVP or explicitly deferred.

---

# 9. Visual Composition Contract

The diagram contains 30 classes with four compartments, so layout quality matters.

## 9.1 Canvas

Use **one A3 landscape master sheet** or an equivalent high-resolution landscape artboard.

Do not split into separate semantic Class Diagrams unless normal report-scale readability proves impossible after a deliberate one-sheet composition attempt.

Title:

`Class Diagram — Aafiatak Medical Appointment Booking System (MVP)`

## 9.2 Non-semantic visual zones

Organize through whitespace/subtle background zones only:

1. Identity & Access
2. Platform & Reference Data
3. Facility & Medical Offering
4. Schedule & Digital Availability
5. Appointment & Payment
6. Visit, Queue & Operational Exceptions

These are **not UML Packages**.

## 9.3 Recommended structural flow

Left/top:
- User
- Patient
- FacilityUser
- PlatformRoleAssignment
- FacilityOnboardingRequest
- AuditRecord
- Notification

Upper/center:
- Region
- City
- FacilityType
- Facility
- FacilityBranch
- Department
- Specialty
- Doctor
- ServiceOffering

Center/right:
- DoctorSchedule
- ScheduleException
- AvailabilityRelease
- ArrivalGroup
- CapacityWithdrawal

Lower/center:
- ReservationHold
- AvailabilityAlertSubscription
- Appointment
- AppointmentStatusHistory
- PaymentIntent

Lower/right:
- VisitInstance
- QueueEntry
- OperationalException
- OperationalExceptionResolution

## 9.4 Relationship routing

- Prefer short orthogonal or clean direct lines.
- Place multiplicities next to the correct relationship ends.
- Put hollow/filled diamonds at the **whole/owner** side.
- Avoid relationship labels or multiplicities over class text.
- Avoid edge buses and excessive crossings.
- Do not route lines through class boxes.
- If two relationships share a corridor, keep enough separation to trace each one.
- Do not use decorative arrows.

## 9.5 Class box style

Match the lecturer's simple technical Class Diagram style:

- rectangular class boxes;
- clear separators between Name / Attributes / Operations / Responsibility;
- bold class name;
- private attributes prefixed `-`;
- public operations prefixed `+`;
- concise responsibility in final compartment;
- no data types;
- no database PK/FK icons.

Use restrained academic colors if desired, but UML semantics and readability dominate.

---

# 10. Semantic Review — 15 Passes

## Pass 1 — Lecturer pages 3–5
Verified the required Class structure, Attributes, Operations, Responsibility compartment, visibility notation, relationships, and multiplicity examples.

## Pass 2 — Course-note interpretation
Applied the supplied rules for Entity/Boundary/Control/Abstract classes, but kept this first deliverable domain/entity-focused to avoid mixing UI/implementation concerns.

## Pass 3 — Scope integrity
Checked every class against the current MVP and removed clinical/HIS/cashier/accounting/deferred concepts.

## Pass 4 — Identity/RBAC
Verified one normalized verified User identity, multi-role capability, FacilityUser provisioning, explicit PlatformRoleAssignment coverage, optional Doctor login linkage, and rejected false User inheritance.

## Pass 5 — Facility/reference model
Verified Facility/Branch, City/Region/FacilityType, Department/Specialty, Doctor, and ServiceOffering ownership boundaries.

## Pass 6 — Service-policy model
Verified amount/currency, exact two booking policies, cancellation/no-show policy ownership, and no partial/deposit concepts.

## Pass 7 — Schedule/availability model
Verified DoctorSchedule, ScheduleException, AvailabilityRelease, ArrivalGroup, lifecycle states, and published-term immutability.

## Pass 8 — Capacity accounting
Verified remaining-capacity formulas, one-way CapacityWithdrawal, no held/confirmed withdrawal, and no reverse/+1 capacity.

## Pass 9 — Hold/concurrency
Verified ReservationHold atomic protection, exact one selected group, idempotency, expiry/release/consume semantics, and unresolved hold-duration default.

## Pass 10 — Availability alerts
Verified subscription is not a reservation/priority/queue position and remains linked to Patient plus booking context.

## Pass 11 — Appointment snapshot
Verified Appointment state set, booking snapshots, cancellation, rescheduling without new status, and AppointmentStatusHistory.

## Pass 12 — Payment
Verified independent PaymentIntent lifecycle, trusted verification, one non-terminal attempt per hold, PAY_AT_FACILITY exclusion, and full-or-zero refund.

## Pass 13 — Visit/queue
Verified VisitInstance and QueueEntry independence, staff-only state changes, queue states/order, correction/removal, and accepted-late manual handling.

## Pass 14 — Operational exceptions/platform oversight
Verified supported exception types, explicit per-Appointment OperationalExceptionResolution records, closure invariant, onboarding request, audit, and notification records.

## Pass 15 — Multiplicity/relationship audit
Rechecked all 52 relationships for direction, multiplicity, aggregation/composition ownership, absence of false Generalization, and consistency with future Object/Sequence/State diagrams.

---

# 10.1 Final Verification Corrections

A second independent semantic audit found and corrected two structural omissions from v1:

1. **PlatformRoleAssignment** was added because the authoritative identity model explicitly separates platform-role relationships from User/FacilityUser/Doctor data. Without it, Platform Administrator/platform-staff access was behaviorally present but structurally missing from the Class Diagram.
2. **OperationalExceptionResolution** was added because the authoritative exception rule requires a documented action/outcome for **each affected Appointment** before an OperationalException may close. A bare many-to-many line could not represent that per-appointment resolution data correctly.

The final audit also made two detail refinements:

- `ServiceOffering` now explicitly includes `cancellationWindow` and `reconfirmationEnabled`.
- `AvailabilityRelease` now shows its frozen commercial/policy snapshot attributes explicitly rather than hiding them inside a generic `bookingTermsSnapshot`.
- `Appointment` now explicitly includes `cancellationWindowSnapshot`.

These corrections improve traceability without adding out-of-scope functionality.

---

# 11. Final QA Checklist

## Classes

- [ ] Exactly 30 classes.
- [ ] All class names exactly match this specification.
- [ ] Every class has Name / Attributes / Operations / Responsibility.
- [ ] No programming data types shown.
- [ ] No database-table notation.

## Relationships

- [ ] Exactly 52 semantic relationships from Section 5.
- [ ] Multiplicity visible at both relevant ends.
- [ ] Composition diamond is filled and on the owner side.
- [ ] Aggregation diamond is hollow and on Facility side.
- [ ] 0 Generalization.
- [ ] 0 Realization.
- [ ] No relationship invented solely for visual convenience.

## Product invariants

- [ ] One User identity can hold multiple profiles/roles.
- [ ] No User inheritance tree.
- [ ] One-way CapacityWithdrawal.
- [ ] No published-capacity increase.
- [ ] ReservationHold protects one capacity unit.
- [ ] Patient does not choose arbitrary ArrivalGroup.
- [ ] Booking policy is exactly FULL_PAYMENT_REQUIRED or PAY_AT_FACILITY.
- [ ] PAY_AT_FACILITY has no PaymentIntent.
- [ ] No partial payment/refund.
- [ ] Appointment/Payment/Visit/Queue/Hold lifecycles remain separate.
- [ ] Doctor does not change visit states.
- [ ] Late acceptance does not move group or create re-entry.
- [ ] OperationalException closure requires documented affected-appointment outcomes.
- [ ] No clinical/deferred classes.

## Visual

- [ ] All 30 classes readable at normal report scale.
- [ ] Relationship lines traceable.
- [ ] No class/multiplicity text collision.
- [ ] No giant connector bus.
- [ ] No semantic grouping represented as fake UML Packages.
- [ ] Notes are concise and placed near relevant domain cluster.
- [ ] Final PNG/SVG/PDF opened and visually inspected before completion.

---

# 12. Implementation Contract

The drawing agent must treat this file as the authoritative execution specification for the MVP Class Diagram.

It may improve coordinates, spacing, typography, and routing.

It may **not**:
- rename classes;
- add/remove classes;
- add/remove relationships;
- alter multiplicities;
- replace Association with Aggregation/Composition or vice versa;
- invent Generalization;
- add external-service classes;
- add database implementation details;
- add deferred features;
- resolve open product decisions.

Final visual status must remain:

`awaiting-user-approval`
