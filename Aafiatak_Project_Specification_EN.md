# Aafiatak Medical Appointment Booking System
## Authoritative Project Specification

**Document purpose:** This file is a standalone, English-only, deeply reviewed specification for the Aafiatak Medical Appointment Booking System. It consolidates the approved project analysis, scope, actors, permissions, business rules, workflows, states, data concepts, operational rules, technical boundaries, non-functional requirements, exclusions, success metrics, and unresolved implementation decisions required to analyze, model, design, and implement the system consistently.

**Authority rule:** Use this document as the authoritative product reference when producing UML diagrams, use-case models, database analysis, implementation plans, or interface requirements. Do not add a feature merely because it seems reasonable. If a feature is listed under **Explicitly Deferred / Out of Current Scope**, it is not part of the approved project scope. If an item is listed under **Remaining Open Decisions**, it is intentionally unresolved and must not be invented.

**Specification-integrity rule:** This document defines the approved project requirements and boundaries. It does not automatically define UML `<<include>>`, `<<extend>>`, inheritance, class multiplicities, API contracts, database fields, or implementation behavior unless they are explicitly specified here. Those modeling decisions must be derived carefully and must never contradict this specification.

---

# 1. Executive Definition

Aafiatak is a digital medical appointment discovery, booking, arrival, and lightweight operational-coordination platform. It connects patients with health facilities, departments, specialties, doctors, and services without replacing the facility's existing hospital, clinic, or internal scheduling system.

The system is deliberately a **booking and access coordination layer**, not a Hospital Information System (HIS), Electronic Health Record (EHR), cashier system, accounting platform, clinical workflow system, pharmacy system, laboratory system, or full facility queue-management system.

The core operating model is based on a limited digital inventory allocated by the facility to Aafiatak. Aafiatak does **not** mirror or control the facility's complete internal schedule. The facility publishes a bounded digital capacity through an `AvailabilityRelease`, which defines an Aafiatak session, its total reception period, its maximum published capacity, and sequential `ArrivalGroup` windows inside that session.

The system supports exactly two booking policies at the `ServiceOffering` level:

- `FULL_PAYMENT_REQUIRED`: the patient pays the full configured amount electronically, and the appointment becomes confirmed only after trusted payment success is verified while the temporary reservation is still valid.
- `PAY_AT_FACILITY`: the appointment becomes confirmed without an electronic payment, and the patient pays the facility upon arrival.

The patient does not choose between these policies. The facility configures the policy for the `ServiceOffering`.

There is no deposit booking, no partial-payment booking, and no booking request waiting for manual facility approval. Once the policy requirements are satisfied and valid capacity exists, the appointment becomes `CONFIRMED` directly.

---

# 2. Project Objective

The project must demonstrate that Aafiatak can:

1. Display a health facility and its departments, doctors, specialties, and services.
2. Allow the facility to publish a limited digital appointment inventory with one total reception period divided into arrival groups.
3. Prevent double booking through an atomic `ReservationHold` mechanism.
4. Protect the last available seat for the first user who successfully starts the booking process and automatically release it when the user does not complete the process.
5. Re-engage users who missed an available seat through **Notify Me When Available** functionality.
6. Support booking with full online payment through `FULL_PAYMENT_REQUIRED`.
7. Support confirmed booking with payment due at the facility through `PAY_AT_FACILITY`.
8. Allow remaining Aafiatak capacity to be withdrawn to the facility's internal schedule in one direction only, while preventing the reverse direction.
9. Distribute confirmed appointments sequentially across facility-defined arrival groups.
10. Order checked-in patients inside an arrival group by actual check-in time, using appointment confirmation time as the tie-breaker.
11. Provide the doctor with a limited read-and-call interface without allowing the doctor to change visit lifecycle states or report delay/absence inside the system.
12. Keep temporary reservation, appointment, payment, visit, and queue states separate.
13. Process full online payment through an independent, auditable `PaymentIntent` lifecycle.
14. Register patient arrival and create a separate `VisitInstance` representing what actually happens on the service day.
15. Record operational exceptions and require resolution of affected appointments.
16. Operate beside the facility's existing system without becoming an HIS.

---

# 3. Pilot Operating Scope

The pilot operates with:

- One health facility.
- One branch.
- Outpatient services.
- A limited number of departments.
- A limited number of doctors.
- A limited number of services.
- One `FacilityAdministrator`.
- One or a small number of `BookingReceptionStaff` users.
- One doctor account or a limited number of doctor accounts.
- One payment gateway when a provider is selected and approved.

This is the pilot deployment scope, not a permanent architectural restriction. The data design should remain capable of supporting multiple branches later.

---

# 4. Core Product Boundaries

## 4.1 What Aafiatak Is

Aafiatak is responsible for:

1. Displaying facilities, branches, departments, specialties, doctors, and services.
2. Displaying only the digital capacity published to Aafiatak through the `Online Allocation Pool`.
3. Dividing an Aafiatak session into `ArrivalGroup` windows with defined start time, end time, and capacity.
4. Creating a short-lived `ReservationHold` to prevent two users from owning the same capacity unit during booking completion.
5. Confirming an appointment after either full electronic payment or completion of the pay-at-facility flow, depending on the service policy.
6. Managing full electronic payment through an independent `PaymentIntent`.
7. Recording **Notify Me When Available** subscriptions and notifying interested patients when capacity returns.
8. Tracking appointment status and notifications.
9. Registering patient arrival and creating a `VisitInstance` for actual service-day events.
10. Providing a lightweight queue within each Aafiatak arrival group.
11. Recording operational exceptions and their resulting actions.
12. Maintaining historical and audit records for sensitive operations.

## 4.2 What Aafiatak Does Not Manage

The system does not manage:

- The facility cashier or cash register.
- Internal accounting or financial reconciliation.
- Complete medical invoices.
- Pharmacy or inventory.
- Medical records.
- Clinical notes.
- Diagnosis.
- Prescriptions.
- Laboratory results.
- Radiology results.
- Medical insurance.
- Salaries or human-resources management.
- Rooms, beds, devices, or clinical resources.
- The facility's complete internal schedule.
- All patients arriving through all channels.
- Detailed clinical reasons for visits.

Aafiatak stores only the minimum operational information necessary for booking and arrival coordination.

---

# 5. Relationship With the Facility's Existing System

The system does not require technical integration with the facility's existing system and must not assume access to the facility's complete calendar.

The facility allocates a separate, bounded digital inventory to Aafiatak through `AvailabilityRelease` records. At minimum, an availability release identifies:

- Facility branch.
- Doctor.
- `ServiceOffering`.
- Date.
- Total Aafiatak reception-period start and end.
- Arrival groups inside the period.
- Start, end, and capacity for each arrival group.
- Maximum published digital capacity.
- Booking policy.
- Last-updated timestamp.
- Operational validity/lifecycle status.

Once an `AvailabilityRelease` becomes published, its published capacity becomes the maximum capacity for that release.

The facility may:

- Withdraw one seat, multiple seats, or all remaining unused capacity from Aafiatak to its internal schedule.
- Temporarily freeze a release or arrival group.
- Close a release or arrival group.
- View held, confirmed, withdrawn, and remaining capacity.
- Record doctor delay, doctor absence, or session cancellation through facility staff.

The facility may not:

- Increase `published` capacity after publication by using free capacity from its internal schedule.
- Return withdrawn capacity to the same published release.
- Withdraw capacity that is already protected by an active `ReservationHold`.
- Withdraw capacity that is already consumed by a confirmed appointment.
- Use a quick `+1` action or another shortcut to bypass the capacity ceiling.

A withdrawal records only the quantity, source/reason, actor, and time. The system does not require copying the external patient's details from the facility's internal schedule.

Possible withdrawal sources include:

- `PHONE`
- `WALK_IN`
- `INTERNAL_USE`
- `MANUAL_BLOCK`

There is no reverse operation that transfers free internal capacity into Aafiatak after publication.

---

# 6. Problems the System Addresses

## 6.1 Difficulty Finding Reliable Information

Patients may not know:

- Nearby facilities.
- Available departments and services.
- Available doctors and their specialties.
- Working days and hours.
- Service price and approximate duration.
- The nearest day or arrival group available through Aafiatak.
- Whether full payment is required now or payment is due at the facility.
- Cancellation and refund rules.
- Whether the displayed time is an exact service time or an arrival window.

## 6.2 Dependence on Calls, Messaging, and Walk-ins

Traditional booking channels can cause:

- Reception workload.
- Slow responses and missed requests.
- Different information across channels.
- Uncertainty about actual online capacity.
- Conflict between electronic booking and phone/walk-in booking.
- Lack of a clear status the patient can follow.

## 6.3 Patient No-show

The system addresses no-show risk through:

- Reminders.
- Optional attendance reconfirmation requests.
- Full-payment booking for services where the facility needs stronger commitment.
- Explicit cancellation/refund handling and a facility-configured no-show financial policy for fully paid bookings. The selected no-show policy is snapshotted into the confirmed appointment.
- Notify-me-when-available subscriptions that can bring interested patients back when capacity returns.

Failure to respond to an attendance reconfirmation request does **not** automatically cancel a booking under the current scope.

## 6.4 Unclear Booking and Payment States

The system must clearly distinguish:

- Temporary seat hold.
- Confirmed appointment.
- Payment lifecycle.
- Refund lifecycle.
- Actual visit lifecycle.
- Queue state.

A payment can succeed while appointment creation requires review, and an appointment can remain confirmed with payment due at the facility. These states must not be collapsed into one field.

## 6.5 Synchronization Gap Without Facility API Integration

The system avoids pretending to know the facility's complete internal schedule. It instead uses:

- A dedicated digital allocation pool.
- A fixed upper capacity limit after publication.
- One-way withdrawal of remaining capacity to the internal schedule.
- No reverse capacity transfer after publication.
- Atomic `ReservationHold` protection for the last available capacity unit.
- Automatic expiry/release of temporary holds.
- Availability-return notifications without guaranteed priority.
- Availability freshness indicators and fast freeze actions.

## 6.6 Exact Appointment Times Do Not Match the Operational Reality

The system does not promise an exact service-entry time for each patient. The facility defines an Aafiatak reception period and divides it into smaller `ArrivalGroup` windows.

Example:

- Total period: 12:00–15:00.
- Group 1: 12:00–13:00, capacity 3.
- Group 2: 13:00–14:00, capacity 3.
- Group 3: 14:00–15:00, capacity 4.

Groups are filled sequentially. Within a group, actual service order is based on check-in time and, when equal, appointment confirmation time.

There is no automatic transfer or re-entry mechanism between arrival groups.

---

# 7. Value Delivered by the System

## 7.1 Patient Value

- Easier discovery of facilities, doctors, services, and availability.
- Visibility of service price and instructions before booking.
- Visibility of digital capacity actually allocated to Aafiatak.
- Clear indication of whether full payment is required or payment is due at the facility.
- Realistic arrival windows instead of misleading exact service times.
- Temporary seat protection while completing the booking.
- Notify-me-when-available support when capacity is exhausted.
- Separate visibility of appointment and payment states.
- Clear arrival/check-in status and approximate position inside the patient's own group.
- Clear alternatives or refunds when the facility cancels or a conflict occurs.

## 7.2 Facility Value

- An additional electronic booking channel without replacing the existing internal system.
- Direct control over the initial digital capacity assigned to Aafiatak.
- Ability to withdraw unused digital capacity back to the internal schedule in one direction.
- Reduced risk of double selling the same capacity through temporary holds and atomic operations.
- Arrival-group distribution that reduces crowding.
- Reduced reception/call workload.
- Reduced no-show risk through reminders and full payment where needed.
- Auditable handling of operational exceptions.
- Measurable attendance, cancellation, availability accuracy, and availability-alert conversion.

## 7.3 Doctor Value

- Clearer view of Aafiatak appointments.
- Visibility of arrival-group windows and checked-in/waiting patients.
- Ability to know and call the next patient without assuming responsibility for visit status changes or operational exception reporting.

## 7.4 Aafiatak Platform Value

- Build a more trusted network of participating health facilities.
- Provide a unified experience for booking, confirmation, arrival, and lightweight operational coordination.
- Maintain a clear domain/data model that can support future integration.
- Reduce double-booking risk and reduce loss of interested patients when capacity is temporarily full.
- Potential subscription or commission revenue is a future business-model possibility, not part of the approved current scope.

---

# 8. System Components

## 8.1 Patient Application

A Flutter application for Android and iOS used for:

- Phone-number account creation and verification using a one-time code delivered through the official WhatsApp authentication channel.
- Passwordless patient login using a short-lived, single-use WhatsApp OTP.
- Logout and revocation of the current authenticated session.
- Basic profile editing.
- Browsing and search.
- Viewing the facility, branch, map location, contact information, departments, specialties, doctors, and services.
- Viewing prices, optional estimated service duration, instructions, booking policy, and available days/groups from Aafiatak capacity only.
- Clearly indicating that displayed availability is not the facility's complete internal schedule.
- Selecting service/doctor/day.
- Viewing the arrival-group window that the system is about to allocate.
- Creating a `ReservationHold` and displaying its countdown.
- Completing full payment or confirming a pay-at-facility booking according to the service policy.
- Subscribing to Notify Me When Available when capacity is unavailable.
- Viewing appointment and payment status separately.
- Viewing future and past appointments.
- Viewing the unique booking number and QR/verification code generated for a confirmed appointment.
- Viewing appointment, payment, and visit outcomes separately, including completed, not completed, or no-show after the service day.
- Cancelling according to policy.
- Reconfirming attendance when requested.
- Receiving reminders and notifications.
- Viewing check-in state and approximate queue position after facility staff registers arrival.

## 8.2 Facility Web Dashboard

A responsive web dashboard used by:

- `FacilityAdministrator`
- `BookingReceptionStaff`
- `Doctor`

Functions are displayed according to role permissions.

The principal daily operations interface is the **Today Pulse Board**.

## 8.3 Aafiatak Platform Administration Dashboard

A protected web dashboard for `PlatformAdministrator` users to:

- Review facility onboarding requests.
- Request additional information.
- Approve or reject a facility.
- Activate or suspend a facility account.
- Manage public reference data.
- Manage Aafiatak staff accounts.
- Review escalated technical/payment/conflict cases.
- Review audit records where required.
- Provide documented technical support.
- View general booking, payment, and availability-accuracy indicators.

The platform administration dashboard does **not** manage a facility's doctors, services, prices, daily availability, daily bookings, or queues on the facility's behalf.

The current scope requires platform-side intake/review/approval of facility onboarding requests but does **not** require a public self-service facility-applicant portal. Therefore no additional operational `FacilityApplicant` role is assumed for UML unless such a portal is explicitly approved later.

## 8.4 Authentication and Identity

### Unified user identity

- Every human account is anchored to one normalized, verified phone number stored on `User`.
- A verified phone number is globally unique for authentication. The same `User` identity may hold more than one approved role/profile when the real person legitimately acts in more than one context (for example, a doctor who is also a patient).
- Role-specific data remains separated through `Patient`, `FacilityUser`, `Doctor`, and platform-role relationships rather than by creating duplicate user identities.

### Authentication method

- Authentication for `Patient`, `FacilityAdministrator`, `BookingReceptionStaff`, `Doctor`, and `PlatformAdministrator` is passwordless.
- A short-lived, single-use OTP is delivered through the official WhatsApp authentication channel.
- SMS is not used for authentication.
- There is no password-based `Forgot Password` workflow for these roles; a new valid WhatsApp OTP is used whenever authentication is required.
- OTP requests and verification attempts must be rate-limited and protected against brute-force abuse.
- OTPs must expire quickly, be single-use, and must not be stored or logged in plaintext.
- Successful authentication creates a revocable application session/token. Privileged-role sessions must be invalidated when the corresponding facility/platform account is disabled or its permissions are revoked.
- Authentication retries must be idempotent and must not create duplicate user accounts.
- Phone-number normalization and uniqueness must be enforced before account creation or invitation.

### Account provisioning

- A patient may self-register after successfully verifying the phone number through WhatsApp OTP.
- Facility, doctor, and platform roles are **not** self-assigned. They require an existing approved/provisioned account and RBAC assignment.
- After a facility onboarding request is approved, the platform activates the facility and provisions/activates its initial `FacilityAdministrator` identity for the verified facility representative.
- `FacilityAdministrator` provisions or disables `BookingReceptionStaff` accounts and doctor login access for that facility. A doctor login account must be linked to the corresponding `Doctor` profile.
- `PlatformAdministrator` accounts are provisioned through the controlled platform-administration process; they are not created by public registration.

### WhatsApp scope boundary

WhatsApp is in scope **only as the authentication/phone-verification channel**. Appointment confirmations, reminders, availability alerts, queue notifications, operational notifications, and support messaging continue to use in-application/system notifications unless a future scope decision explicitly adds WhatsApp messaging for those purposes.

Authentication delivery must use an approved official WhatsApp Business/provider integration rather than browser automation or an unofficial personal-account workflow.

---

# 9. Approved System Actors

The approved human roles are:

1. `Visitor`
2. `Patient`
3. `FacilityAdministrator`
4. `BookingReceptionStaff`
5. `Doctor`
6. `PlatformAdministrator`

External services used by the system are:

- Payment Gateway.
- Notification Service.
- Map Service.
- Official WhatsApp authentication provider/API for phone verification and authentication of human user accounts.

SMS is not used. WhatsApp is in scope only for authentication/phone verification; general WhatsApp messaging and notification delivery remain outside the current scope.

---

# 10. Actor Permissions and Restrictions

## 10.1 Visitor

A visitor is not authenticated.

A visitor may:

- Browse facilities.
- Search/browse by doctor, department, specialty, or service.
- View general facility information.
- View preliminary available days/groups.
- Register.
- Log in.

A visitor may not create an appointment before authentication.

## 10.2 Patient

A patient may:

- Manage basic account/profile data.
- Search for a facility, doctor, department, specialty, or service.
- View service information, price, optional estimated service duration, instructions, and policies.
- Select a day from the digital inventory published to Aafiatak.
- View the arrival-group window that will be allocated before commitment.
- Create a booking under the service's configured `FULL_PAYMENT_REQUIRED` or `PAY_AT_FACILITY` policy.
- Pay the full amount when full payment is required.
- View the `ReservationHold` countdown and complete the process within the allowed time.
- Subscribe to Notify Me When Available when capacity is full or temporarily held.
- View appointment and payment states separately.
- Reconfirm attendance when requested.
- Cancel an appointment according to the applicable policy.
- View previous and upcoming appointments.
- View the booking number and QR/verification code.
- Receive notifications.
- View approximate queue position inside the patient's own arrival group after check-in.
- View instructions for arrival outside the assigned arrival-group window.

A patient may not:

- Choose a booking policy different from the `ServiceOffering` policy.
- Extend a `ReservationHold` arbitrarily.
- Reserve multiple capacity units through the same booking action.
- Treat an availability alert as a reservation or guaranteed priority.
- self-check-in to the arrival queue under the current scope.
- Change queue position.
- View other patients' information.
- Be automatically moved to another arrival group when late.
- Modify facility policies.

## 10.3 Facility Administrator

The `FacilityAdministrator` is the highest-privilege user inside the facility's Aafiatak account.

The facility administrator may:

- Log in to the facility dashboard.
- Manage facility and pilot-branch display/contact information, including images/logo, address, map location, contact details, and working hours.
- Select departments and specialties from reference lists and associate them with the facility.
- Add and edit doctors.
- Add and edit services/`ServiceOffering` records.
- Set service price, optional estimated service duration, and instructions.
- Set the booking policy for each `ServiceOffering`.
- Configure `FULL_PAYMENT_REQUIRED` or `PAY_AT_FACILITY`.
- Configure cancellation/refund policy and no-show financial policy for fully paid bookings.
- Configure whether attendance reconfirmation is enabled; exact send timing remains an open parameter.
- Define doctor schedule windows and planned schedule exceptions.
- Create `AvailabilityRelease` records.
- Define the total Aafiatak reception period.
- Create `ArrivalGroup` records with start time, end time, sequence, and capacity.
- Set the initial digital capacity before publication.
- Publish an availability release.
- View held, confirmed, withdrawn, and remaining capacity.
- Withdraw remaining capacity to the facility's internal schedule.
- Freeze or close availability.
- Manage operational exceptions.
- Add, disable, and manage facility staff accounts and assign only approved roles/permissions within the defined access-control model; this does not introduce an arbitrary custom-permission designer.
- View Aafiatak bookings, payment states, and operational indicators.

The facility administrator may not:

- Increase published digital capacity after publication by using free capacity from the internal schedule.
- Return withdrawn capacity to the same release.
- Manage another facility.
- Modify platform-wide settings.
- Delete audit history.
- View patient information unrelated to the facility's Aafiatak bookings.

## 10.4 Booking & Reception Staff

Daily work begins from the **Today Pulse Board**.

Booking/reception staff may:

- Log in to the facility dashboard.
- View today's doctors, sessions, and Aafiatak arrival groups.
- View published, held, confirmed, withdrawn, remaining, and stale capacity.
- Withdraw one seat, multiple seats, or all remaining capacity to the internal schedule.
- Freeze or close a session/group without affecting active holds or confirmed appointments.
- Search appointments by booking number, phone number, or patient name.
- Reschedule an appointment after patient communication and agreement.
- Cancel an appointment with a reason.
- View payment state without arbitrarily changing gateway results.
- Register patient arrival.
- Create/activate the actual visit.
- Correct an erroneous check-in/queue registration with a recorded reason.
- Manage the Aafiatak queue inside the arrival group.
- Call the next patient.
- Record service start.
- Record service completion or non-completion.
- Record a no-show decision.
- Record doctor delay, doctor absence, or session cancellation as an `OperationalException` after receiving the information from the doctor or facility management.
- Record a late arrival and make a manual operational decision.
- Execute conflict resolution through an alternative slot, facility cancellation with full refund when applicable, or documented escalation.

Booking/reception staff may not by default:

- Increase published digital capacity.
- Restore withdrawn capacity to Aafiatak.
- Add doctors.
- Modify core facility profile data.
- Modify service price.
- Modify booking/payment/refund policy.
- Manage employee accounts.
- Modify platform settings.
- Enter diagnoses, clinical notes, prescriptions, or internal medical invoices.
- Arbitrarily overwrite payment-gateway outcomes.
- Create new Aafiatak appointments on behalf of phone or walk-in patients. Those channels remain in the facility's internal system and affect Aafiatak capacity only through the documented `CapacityWithdrawal` mechanism.

## 10.5 Doctor

The doctor has a user account linked to the corresponding `Doctor` record.

The doctor may:

- Log in to the simplified doctor interface.
- View the doctor's own upcoming Aafiatak appointments.
- View today's own Aafiatak appointments.
- View the doctor's own arrival groups and windows.
- View checked-in and waiting patients assigned to the doctor through Aafiatak.
- Identify the next patient.
- Call the next patient.

The doctor may not:

- Change a visit to `IN_SERVICE`.
- Complete a visit as `COMPLETED`.
- Mark a visit `NOT_COMPLETED`.
- Record delay or absence inside the system.
- View other doctors' appointments without separate administrative permission.
- Change service prices.
- Change services.
- Change availability.
- Change booking/payment/refund policies.
- Change payment results.
- Execute refunds.
- Enter or view diagnosis, prescriptions, test results, or clinical notes through the doctor interface.
- Manage employee accounts.
- Modify platform settings.

If the doctor is delayed or absent, the doctor contacts reception/facility management directly; facility staff record the operational exception.

## 10.6 Platform Administrator

The `PlatformAdministrator` may:

- Review a facility onboarding request.
- Request additional information.
- Approve or reject the request.
- Activate or suspend the facility account and provision/activate the initial `FacilityAdministrator` identity for an approved facility. A suspended facility cannot accept new holds/bookings or publish new availability; active temporary holds are released, while existing confirmed appointments/history are preserved and require documented operational resolution rather than silent deletion.
- Manage cities, regions, facility types, and public reference lists.
- Manage Aafiatak platform staff accounts.
- View technical issues and escalated payment/conflict cases.
- Review audit logs when required.
- Provide documented technical support.

The platform administrator does not ordinarily:

- Add doctors for a facility.
- Add services for a facility.
- Manage a facility's schedules.
- Modify a facility's prices or booking policies.
- Operate the facility's daily bookings.
- Operate the facility's daily waiting queue.

---

# 11. Data Ownership and Access Boundaries

## 11.1 Patient Data

Includes:

- Account data.
- Phone number.
- Appointments.
- Notifications.
- Payment operations related to the patient's appointments.

The patient sees only the patient's own data.

## 11.2 Facility Data

Includes:

- Facility information.
- Branch information.
- Departments.
- Specialties.
- Doctors.
- Services and prices.
- Schedules.
- Policies.
- Facility staff accounts.

The facility manages this data itself.

## 11.3 Platform Data

Includes:

- Cities and regions.
- Facility types.
- Platform staff accounts.
- Support records.
- Audit log.
- Platform-level configuration/reference data.

## 11.4 Booking Data

An `Appointment` belongs to the patient and facility context but does not contain the complete payment or actual-visit lifecycle inside a single status field. Independent entities represent payment, availability, and visit state.

Records linked to historical transactions must not be hard-deleted when deletion would destroy traceability. Status change, disablement, or archival must be used according to retention policy.

---

# 12. Facility, Branch, Department, Specialty, Service, and Doctor Model

## 12.1 Facility and Branch

The general design supports one facility with one or more branches in the future. The pilot runs with one facility and one branch.

Each appointment is associated with a specific branch.

Basic branch data includes:

- Name.
- City.
- Region.
- Address.
- Map location.
- Contact number.
- Working hours.
- Local time zone used to interpret appointment dates, arrival-group windows, reminders, and audit timestamps.

## 12.2 Department

A department is an organizational unit inside a facility, such as pediatrics, dentistry, internal medicine, obstetrics/gynecology, radiology, or laboratory.

Aafiatak provides public reference lists, while the facility selects the departments that actually apply to the facility.

## 12.3 Specialty

A specialty describes a doctor's specialty, such as pediatrics, cardiology, dermatology, or orthopedic surgery.

Aafiatak provides reference lists, while the facility associates applicable specialties with its own account and doctors.

## 12.4 Medical Service and Service Offering

The patient books a `ServiceOffering` at a specific branch, optionally tied to a specific doctor.

Examples include:

- First consultation.
- Follow-up/review.
- Consultation.
- Approved short procedure.
- Physical therapy session.

Separate service offerings may be used for first consultation and follow-up when price or policy differs.

`ServiceOffering` is the authoritative source for operational booking values including:

- Service name.
- Department and specialty.
- Doctor(s) providing the service.
- Full amount required for the service/booking.
- The facility currency in which that amount is denominated. The pilot uses one configured facility currency and performs no currency conversion.
- Optional estimated service duration in minutes for patient information. This value is informational only; it does not create an exact appointment slot, determine queue priority, or promise doctor-entry time.
- Booking policy: `FULL_PAYMENT_REQUIRED` or `PAY_AT_FACILITY`.
- Patient cancellation/refund policy for full online payment.
- No-show financial policy for fully paid bookings: `NO_SHOW_NON_REFUNDABLE` or `NO_SHOW_FULL_REFUND`.
- Attendance instructions.
- Activation status.

The system does not store a partial amount or remaining-balance concept under the current scope.

The current service scope focuses on outpatient clinics, examinations/first visits, follow-up/review visits, consultations, and other clear short services. Complex laboratory or radiology service pathways are deferred as separate operational flows; listing a laboratory or radiology department does not make its internal operational workflow part of the current scope.

The system does not collect a detailed medical reason for the visit. Any future short description would have to remain optional and limited to booking context rather than diagnosis or clinical record content.

## 12.5 Doctor

Doctor data in the current scope includes:

- Name.
- Photo.
- Specialty.
- Qualification.
- Short biography.
- Department.
- Services provided at the facility.
- Working days.
- Working hours.
- General activation status for display.

Price and booking policy belong to the service offering, not to the doctor's general profile.

The pilot associates doctors with the pilot facility and branch. The architecture should not prevent future multi-facility or multi-branch doctor affiliations, but activating those relationships is not required in the current scope.

---

# 13. Digital Appointment Inventory Model

Aafiatak uses an `Online Allocation Pool`, not the doctor's complete internal calendar.

The core digital-capacity entities are:

- `DoctorSchedule`
- `ScheduleException`
- `AvailabilityRelease`
- `ArrivalGroup`
- `CapacityWithdrawal`
- `ReservationHold`
- `AvailabilityAlertSubscription`

## 13.1 Doctor Schedule

`DoctorSchedule` represents theoretical/basic doctor working windows.

## 13.2 Schedule Exception

`ScheduleException` represents a planned leave, closure, or planned scheduling exception before availability is published.

## 13.3 Availability Release

`AvailabilityRelease` represents the complete digital capacity assigned to Aafiatak for a specific doctor/service/branch/date/session.

It contains or tracks:

- Doctor.
- Service offering.
- Branch.
- Date.
- Aafiatak reception-period start and end.
- Maximum published capacity: `published`.
- Temporarily held capacity: `held`.
- Confirmed capacity: `confirmed`.
- Capacity withdrawn to the facility: `withdrawn_to_facility`.
- Remaining capacity: `remaining`.
- Snapshotted service amount and currency applicable to this release.
- Snapshotted booking policy.
- Snapshotted patient cancellation/refund policy.
- Snapshotted no-show financial policy.
- Last-updated time.
- User who performed the update.
- Lifecycle state.

Lifecycle states:

- `DRAFT`
- `PUBLISHED`
- `FROZEN`
- `CLOSED`
- `CANCELLED`

Derived indicators:

- `EXHAUSTED` when `remaining = 0`.
- `STALE` when the last update exceeds the configured freshness duration.

`EXHAUSTED` and `STALE` are indicators, not lifecycle states.

### Published release term immutability

When an `AvailabilityRelease` transitions to `PUBLISHED`, its commercial and booking terms are frozen for that release: service amount, currency, booking policy, patient cancellation/refund policy, and no-show financial policy. Later changes to the parent `ServiceOffering` apply only to future releases and must not silently rewrite an already published release.

If the facility must change those terms for future bookings, it must freeze or close the affected published release as appropriate and create a new release with the new terms. Existing confirmed appointments always keep their own booking snapshots.

When an availability release becomes stale, staff must be prompted to review/update it. Depending on facility settings, the platform may hide or automatically freeze stale availability rather than continue presenting it as confidently available. An immediate freeze action may also be used at doctor, session/release, or arrival-group level when capacity is doubtful, the doctor is delayed, or an operational problem occurs.

The unified remaining-capacity formula is:

```text
remaining = published - held - confirmed - withdrawn_to_facility
```

For capacity accounting, `held` counts only active holds and `confirmed` counts only appointments that still consume capacity. When a confirmed appointment is cancelled and its seat is released, that unit no longer contributes to `confirmed`; the cancelled appointment record itself remains preserved for history/audit. `EXHAUSTED` describes numeric capacity (`remaining = 0`), while actual patient bookability must additionally satisfy lifecycle and time eligibility.

Mandatory capacity rules:

- `published` may not increase after transition to `PUBLISHED`.
- Normal hold/confirmation accounting changes `remaining` through the capacity formula. Any intentional facility-side reduction of unused remaining capacity after publication is performed only through a documented `CapacityWithdrawal`.
- Capacity values must not become negative.
- A capacity unit must never be counted twice.
- Active held capacity may not be withdrawn.
- Confirmed capacity may not be withdrawn.
- Withdrawn capacity may not return to the same release.
- Full Aafiatak capacity does not authorize the facility to add internal free capacity into the application.

Lifecycle semantics:

- `DRAFT`: configuration is editable and no patient booking attempt may consume capacity from the release.
- `PUBLISHED`: new holds may be created only when the target arrival group is also bookable.
- `FROZEN`: temporarily stops **new** holds/bookings while preserving valid existing holds and confirmed appointments. It may return to `PUBLISHED`.
- `CLOSED`: prevents new holds/bookings after session completion or an administrative decision. It is terminal for new-booking purposes. A valid hold that existed before closure may complete only while its own hold/time validity remains satisfied and the release/group has not been cancelled.
- `CANCELLED`: terminal cancellation of the session. New holds are forbidden, active holds are released, and confirmed appointments must be handled through `OperationalException` resolution.

Allowed release transitions are `DRAFT -> PUBLISHED`, `PUBLISHED <-> FROZEN`, and `PUBLISHED/FROZEN -> CLOSED` or `CANCELLED`. The system must not reopen `CLOSED` or `CANCELLED` releases into a bookable state.

## 13.4 Arrival Group

An `ArrivalGroup` is a smaller arrival window inside an `AvailabilityRelease`.

It includes:

- Group number/sequence.
- Start time.
- End time.
- Allocated capacity.
- Temporarily held count.
- Confirmed count.
- Withdrawn-to-facility count, derived from the group's `CapacityWithdrawal` records.
- Remaining count.
- Group state.

Group states:

- `OPEN`
- `FROZEN`
- `CLOSED`

`OPEN <-> FROZEN` is reversible. `OPEN/FROZEN -> CLOSED` closes the group for new holds and is terminal for new-booking purposes. Closing or freezing a group does not rewrite existing confirmed appointments. A valid pre-existing hold may complete only while its hold/time validity remains satisfied and the parent release has not been cancelled.

The facility defines all groups and their capacities before publication. The sum of arrival-group capacities must equal the published digital capacity.

Group capacity is reconciled by:

```text
group_remaining = group_capacity - group_held - group_confirmed - group_withdrawn_to_facility
```

A group can have positive numeric `group_remaining` while still being **not bookable** because it is frozen/closed, its parent release is not bookable, or its arrival window has already started.

Sequential allocation rules:

1. New booking attempts use the earliest **currently bookable** arrival group.
2. A group is bookable for a new hold only when it has positive remaining capacity, the parent release is `PUBLISHED`, the group is `OPEN`, and enough time remains for the configured hold window to finish before the group starts. A new `ReservationHold` must satisfy `hold_expires_at <= arrival_group.start_at`; no hold is created when the full hold window would extend into or beyond the group start time.
3. The system does not move to the next group while an earlier group remains bookable. Held capacity counts against the earlier group's availability while the hold is active.
4. Creating a `ReservationHold` fixes the selected group and exposes that group's arrival window to the patient. Existing holds and confirmed appointments are never automatically rebalanced between groups.
5. If an earlier group becomes bookable again before its start time because a hold expires/releases or a confirmed seat is validly republished, the **next** new booking attempt returns to that earliest bookable group; existing later-group holds/appointments remain unchanged.
6. The confirmed appointment stores a snapshot of its group, group window, and confirmation time.

An arrival-group window is an arrival period, not an exact guaranteed doctor-entry time.

## 13.5 Capacity Withdrawal

`CapacityWithdrawal` is the only approved mechanism for transferring unused Aafiatak capacity to the facility's internal schedule.

Each withdrawal records:

- Affected `AvailabilityRelease`.
- Affected `ArrivalGroup` where applicable.
- Quantity withdrawn.
- Source/reason.
- Staff member who executed the action.
- Timestamp.

The operation is atomic and succeeds only when the requested quantity is less than or equal to valid remaining capacity.

The facility does not need to enter the internal patient's details into Aafiatak.

There is no reverse `CapacityWithdrawal` operation.

When withdrawing capacity, the preferred behavior is to reduce capacity from the last incomplete group first, preserving earlier group sequencing. Existing active holds or confirmed appointments are never moved between groups because of withdrawal.

## 13.6 Quick Capacity Actions

The Today Pulse Board may provide quick actions to:

- Withdraw one seat.
- Withdraw multiple seats within the remaining capacity.
- Withdraw all remaining capacity.
- Freeze a group or release.
- Close a group or release.

There is no `+1` or equivalent capacity-increase action after publication.

Freeze is reversible; a capacity withdrawal is not reversible inside the same release.

---

# 14. Reservation Hold and Double-Booking Prevention

When a patient starts booking available capacity, the system atomically creates a `ReservationHold` only against a currently bookable arrival group.

The first request that successfully acquires the capacity unit temporarily owns it. Another user attempting to acquire the same last unit must see that capacity is full or temporarily held.

The hold duration is short and configurable within platform-approved values. Three or five minutes are candidate values, but the final default duration and whether facilities may choose between approved values remain open decisions.

`ReservationHold` states:

- `ACTIVE`: the capacity unit is temporarily protected for the patient.
- `CONSUMED`: the hold has been converted exactly once into a confirmed appointment.
- `EXPIRED`: the time limit ended before completion.
- `RELEASED`: the user abandoned/cancelled the operation before completion.

Mandatory rules:

- An active hold prevents another user from owning the same unit.
- The hold identifies the selected arrival group and arrival window.
- A hold expires automatically.
- If the user leaves the process, the seat is released immediately when the event is known or upon hold expiry.
- Under `FULL_PAYMENT_REQUIRED`, the appointment is confirmed only after trusted payment success while the hold remains valid.
- Under `PAY_AT_FACILITY`, the active hold becomes a confirmed `Appointment` after the final booking form is completed.
- Freezing or administratively closing a release/group prevents new holds but does not by itself invalidate a valid hold created earlier. Such a hold may still be consumed before its expiry and before the arrival window starts.
- A hold may never be consumed at or after its arrival-group start time or after the parent release is `CANCELLED`; it must be released/expired instead. If a trusted payment has already succeeded in such an exceptional case, payment reconciliation follows the critical-payment handling rules rather than creating a conflicting appointment.
- Idempotency keys must prevent duplicate appointments caused by retries or poor connectivity.
- The system must prevent a patient from holding or confirming another appointment whose arrival window overlaps an existing active hold or confirmed appointment for that same patient, except inside the controlled atomic rescheduling operation.

---

# 15. Notify Me When Available

When remaining capacity reaches zero, or the last seat is protected by an active `ReservationHold`, the patient application exposes a **Notify Me When Available** action.

The action creates an `AvailabilityAlertSubscription` associated with the patient and the relevant service, doctor, date, or availability release.

An availability subscription:

- Is not a reservation.
- Does not protect capacity.
- Does not guarantee priority.
- Does not create a queue position.

A notification may be sent when capacity changes from zero to a positive value because of:

- `ReservationHold` expiry.
- `ReservationHold` release.
- Cancellation of a confirmed appointment when the released capacity becomes bookable again under the seat-republication rule below.
- A documented technical correction that restores capacity that was incorrectly held.

A notification must **not** be triggered by transferring free capacity from the internal facility schedule to Aafiatak because that reverse transfer is not allowed.

After receiving the alert, users compete for the seat normally. The first user to successfully create a valid `ReservationHold` receives temporary protection.

Subscriptions expire automatically when:

- The session ends.
- The patient successfully books.

The system must prevent repetitive or annoying duplicate availability notifications.

## 15.1 Seat Republication After Confirmed Appointment Cancellation

When a confirmed appointment is cancelled, the consumed capacity is released back to the **same `ArrivalGroup`** from which that appointment was confirmed.

- The cancellation reduces the group's confirmed consumption and therefore returns one unit to `remaining`.
- The returned unit is bookable only when the parent `AvailabilityRelease` is `PUBLISHED`, the original `ArrivalGroup` is `OPEN`, and enough time remains to create a full valid `ReservationHold` whose expiry is no later than the group start time.
- If the release/group state or time makes the group non-bookable, the returned unit remains numerically available but cannot receive a new hold. No new capacity is created and no capacity is transferred from the internal facility schedule.
- For patient cancellation, the returned unit follows these rules automatically. For a facility-side cancellation caused by an operational problem or conflict, the seat must not be re-offered until the system/authorized staff has confirmed that the underlying release/group remains operationally valid; a cancelled session or group never republishes seats for new booking.
- The facility may subsequently withdraw that now-unused unit to its internal schedule through the normal irreversible `CapacityWithdrawal` process.
- The returned unit never moves automatically to another arrival group.
- If the cancellation causes bookable remaining capacity to transition from zero to a positive value, eligible `AvailabilityAlertSubscription` records are notified through the normal idempotent notification process.
- Notification does not reserve the returned unit; users still compete by creating a valid `ReservationHold`.

---

# 16. Booking Policy and Booking Flows

The `ServiceOffering` determines the booking policy. Before the patient commits, the application displays:

- Booking policy.
- Full amount, where applicable.
- Arrival-group window.
- Cancellation/refund policy.
- No-show financial policy when full online payment applies.
- Attendance instructions.

The patient cannot override the service's configured policy.

## 16.1 Full Payment Required — `FULL_PAYMENT_REQUIRED`

Flow:

1. Patient selects the service and day.
2. The system selects the earliest currently bookable arrival group and displays its window.
3. The system atomically creates a `ReservationHold` and starts the countdown.
4. The system creates a `PaymentIntent` for the full configured amount.
5. When trusted payment success is verified before hold expiry, the system creates an `Appointment` with status `CONFIRMED` and consumes the capacity atomically.
6. After successful full payment, Aafiatak does not track a remaining balance for that booking.
7. If payment fails or the hold expires, the hold ends and capacity becomes available again.
8. If payment arrives after hold expiry or appointment creation cannot complete, the system must not create a conflicting appointment. It must offer an alternative, start a full refund when applicable, or move the payment case to `UNDER_REVIEW`.

A fully paid booking does not require manual facility confirmation and does not grant clinical or queue priority.

## 16.2 Pay at Facility — `PAY_AT_FACILITY`

Flow:

1. Patient selects the service and day.
2. The system selects the earliest currently bookable arrival group and displays its window.
3. The system atomically creates a `ReservationHold` and starts the countdown.
4. The patient completes the final booking information and accepts that payment is due at the facility.
5. The system converts the hold into a `CONFIRMED` appointment and consumes capacity atomically.
6. No `PaymentIntent` is created.
7. The user interface displays that payment is due at the facility.
8. If the user abandons the flow or the hold expires, the seat returns to available capacity.

This flow does not require manual facility approval and has no pending-approval state.

## 16.3 Policy Configuration Inputs

The following booking inputs are part of the approved configuration model. The facility controls the service-specific inputs below, except that selection authority for `ReservationHold` duration remains explicitly open:

- Booking model: `FULL_PAYMENT_REQUIRED` or `PAY_AT_FACILITY`.
- Service/booking amount denominated in the pilot facility's configured currency. Under `FULL_PAYMENT_REQUIRED` it is collected electronically; under `PAY_AT_FACILITY` the same snapshotted amount is displayed as due at the facility.
- Optional estimated service duration for patient information only.
- `ReservationHold` duration from platform-approved values; the default value and whether the facility may choose among approved values remain open decisions.
- Cancellation and appointment-change window.
- Refund option: `REFUNDABLE_WITHIN_WINDOW` or `NON_REFUNDABLE`.
- No-show financial policy for fully paid bookings: `NO_SHOW_NON_REFUNDABLE` or `NO_SHOW_FULL_REFUND`, selected by the facility.
- Whether non-binding attendance reconfirmation is enabled. When enabled, the server sends the request automatically according to the configured schedule; the exact timing remains an open parameter. A receptionist does not need to manually trigger each request.
- Attendance instructions for the arrival-group window.

At the availability level, the facility configures:

- Total Aafiatak reception period.
- Number of arrival groups.
- Start time, end time, and capacity of each group.

## 16.4 Appointment Booking Snapshot

When an appointment is confirmed, it preserves the applicable booking conditions so later configuration changes do not rewrite an existing booking. The snapshot includes the branch, doctor, service, amount, currency, booking policy, arrival group, arrival window, cancellation/refund policy, cancellation window where applicable, no-show financial policy, and confirmation time.

## 16.5 Configuration Precedence

To prevent ambiguity when configuration changes over time, the governing values are resolved in this order:

1. `ServiceOffering`/`BookingPolicy` configuration defines the terms used when preparing a **new draft** availability release.
2. When an `AvailabilityRelease` becomes `PUBLISHED`, its snapshotted amount, currency, booking policy, cancellation/refund policy, and no-show policy become the governing terms for **new bookings made from that release**. Later parent-configuration changes do not mutate the published release.
3. When an `Appointment` is confirmed, its own snapshot becomes the governing historical commitment for that appointment. Later release or service changes do not rewrite it.
4. If a facility needs different terms for future bookings, it freezes/closes the affected published release as appropriate and creates a new release; it does not edit historical commitments in place.

This precedence rule applies to UML, database modeling, business logic, and UI display so that price/policy drift cannot occur.

---

# 17. Cancellation, Refund, and Rescheduling Rules

## 17.1 Patient Cancellation and Refund Policy

For fully paid bookings, the facility configures one of two patient-cancellation policies at the `ServiceOffering` level:

- `REFUNDABLE_WITHIN_WINDOW`: the patient receives a full refund if cancellation occurs before the end of the configured cancellation window; after the window, no refund is due.
- `NON_REFUNDABLE`: the patient does not receive a refund after confirmation; this must be displayed clearly before payment.

Refund rules:

- Refund is either the full collected amount or zero.
- There is no multi-percentage or partial refund engine.
- `PAY_AT_FACILITY` has no Aafiatak electronic amount to refund.
- If the facility cancels or a facility-responsible conflict occurs, a full refund starts for any amount paid, regardless of the patient-cancellation policy.
- A failed or cancelled payment before success does not create a settled amount requiring refund.
- The applicable cancellation/refund policy and cancellation window are snapshotted into the appointment when created.
- Later policy changes do not retroactively change an existing booking.
- The application displays the expected cancellation/refund result before the patient confirms cancellation.

Patient self-cancellation is available only while the appointment is still `CONFIRMED`, the patient has not checked in, and the assigned arrival-group window has not started. Once the arrival window starts, arrival/late/no-show operational rules take precedence and the patient cannot use self-cancellation to bypass the recorded no-show policy. Facility-side cancellation remains available when operationally required and is audited.

## 17.2 No-show Financial Policy

For `FULL_PAYMENT_REQUIRED`, the facility defines the no-show financial rule at the `ServiceOffering` level and the selected value is snapshotted into the confirmed appointment. `NO_SHOW` may be recorded only after the assigned arrival-group window has ended without a valid check-in for that appointment:

- `NO_SHOW_NON_REFUNDABLE`: no refund is due when facility staff records `NO_SHOW`.
- `NO_SHOW_FULL_REFUND`: the full collected amount is refunded when facility staff records `NO_SHOW`.

Partial no-show refunds are not supported.

For `PAY_AT_FACILITY`, no Aafiatak electronic refund exists because no `PaymentIntent` was created. The no-show outcome remains an operational `VisitInstance` result.

The no-show policy must be displayed before the patient confirms a fully paid booking. A later change to facility policy must not retroactively change an existing appointment.

## 17.3 Rescheduling

Under the current scope, appointment changes occur after communication and agreement with the facility.

An existing appointment may be rescheduled in place only when the destination capacity belongs to the **same `ServiceOffering` and preserves the same snapshotted financial and booking terms**.

When moving an eligible confirmed appointment:

1. A valid new capacity unit in a currently bookable, not-yet-started arrival group must be secured first.
2. The old capacity unit is released only after the new seat has been secured.
3. The move must be performed atomically to prevent losing both positions or creating duplicated capacity consumption.
4. Previous and new release/group/window details, actor, reason, and history must be recorded.
5. The financial snapshot remains unchanged.

If the patient wants a different service, or the destination uses a different amount, booking policy, cancellation/refund policy, or no-show financial policy, the system does **not** perform an in-place reschedule. The old appointment is cancelled under its saved rules and a completely new booking is created under the new service/release terms. This avoids top-up payments, partial refunds, and mixed financial lifecycles.

There is no automatic rescheduling or automatic transfer because a patient arrives late.

---

# 18. Electronic Payment and Refund Processing

Payment has an independent lifecycle from the appointment.

Electronic payment is used only for `FULL_PAYMENT_REQUIRED`.

For `PAY_AT_FACILITY`, Aafiatak displays payment as due at the facility but creates no `PaymentIntent`.

Possible real-world combinations include:

- Confirmed appointment after successful full payment.
- Confirmed appointment with payment due at the facility.
- Successful payment while appointment creation requires reconciliation/review.
- Cancelled appointment while refund is pending.

## 18.1 Payment Intent

Every electronic payment attempt creates an independent `PaymentIntent` containing or linking to:

- Related `ReservationHold` or appointment.
- Full amount.
- Currency, matching the amount/currency snapshotted for the booking attempt.
- Payment gateway.
- External gateway reference.
- Creation time.
- Expiry time.
- Payment state.
- Idempotency key.
- Related refund lifecycle.

At most one non-terminal `PaymentIntent` may be active for the same `ReservationHold` at a time. Reloading/retrying the client must not automatically create another charge attempt. A new payment attempt after a terminal failure/expiry is allowed only while the hold remains valid and must use idempotent server-side rules.

The system must not rely only on the patient's browser/app returning from the payment gateway. It must verify the gateway result through a trusted webhook or trusted gateway query.

## 18.2 Payment Scope

Includes:

- One payment gateway after provider approval.
- No activation of full-payment booking until trusted verification and a supported refund path are available.
- Temporary protection of the selected seat/group while payment is in progress.
- Recording success, failure, expiry, and under-review states.
- Display of the full paid amount and external reference.
- Simplified payment receipt.
- Full refund initiation after facility cancellation or facility-responsible conflict.
- Application of the saved patient cancellation policy: full refund or no refund.
- Application of the saved no-show policy for fully paid bookings: full refund or no refund.

Does not include:

- Partial payment.
- Remaining-balance tracking.
- Full medical invoicing.
- Cashier functions.
- Multiple gateways.
- Payment splitting.
- Advanced settlement/accounting reconciliation.
- Multi-rule partial refund calculations.

## 18.3 Critical Payment Cases

The system must explicitly handle:

- Payment succeeds but appointment creation fails.
- Payment succeeds but notification delivery fails; the financial result remains recorded and notification retries independently.
- Delayed payment-gateway notification.
- Payment result arrives after `ReservationHold` expiry or after the selected arrival window becomes ineligible for confirmation.
- Duplicate payment-gateway notifications.
- Facility cancellation after payment collection.
- Patient cancellation with the saved refund policy.
- Recorded no-show requiring a full refund under the appointment's saved no-show policy.
- Payment gateway outage.
- Payment remaining `UNDER_REVIEW`.
- Patient presents a receipt while Aafiatak has not yet resolved the gateway result.

Any alternative appointment considered after successful payment without a completed appointment must first secure valid capacity under equivalent snapshotted service/financial terms. The system must not silently move the patient to a different price or policy. If equivalent recovery cannot be completed safely, the payment is refunded or remains `UNDER_REVIEW` through the documented support path.

Reception staff must not arbitrarily overwrite financial outcomes. They see a defined status and use a verification/escalation path.

---

# 19. Independent State Models

The system uses four separate high-level state domains: **temporary reservation**, **appointment**, **payment**, and **visit/queue operations**. Within the visit/queue operational domain, `VisitInstance` and `QueueEntry` have their own distinct status sets. These states must remain separate from appointment status rather than being collapsed into one generic lifecycle.

## 19.1 Reservation Hold Status

- `ACTIVE`
- `CONSUMED`
- `EXPIRED`
- `RELEASED`

## 19.2 Appointment Status

- `CONFIRMED`
- `CANCELLED_BY_PATIENT`
- `CANCELLED_BY_FACILITY`

There is no pending manual approval or rejected-booking-request state under the current scope.

Arrival and service results are not stored as appointment states; they belong to `VisitInstance`.

Rescheduling history is recorded in `AppointmentStatusHistory` with previous/new scheduling data, actor, and reason.

## 19.3 Payment Status

For `PAY_AT_FACILITY`, no `PaymentIntent` exists. The UI may display `DUE_AT_FACILITY` as a presentation state.

For full electronic payment, `PaymentIntent` states are:

- `CREATED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `EXPIRED`
- `UNDER_REVIEW`
- `REFUND_PENDING`
- `REFUNDED`

## 19.4 Visit Instance Status

- `CREATED`: the visit record exists after the first relevant operational event on the service day.
- `CHECKED_IN`: facility staff registered the patient's arrival.
- `IN_SERVICE`: facility staff recorded service start.
- `COMPLETED`: facility staff recorded operational completion of the visit.
- `NOT_COMPLETED`: the patient arrived, but the service was not completed.
- `NO_SHOW`: the patient did not check in and facility staff recorded a no-show decision.

Facility staff, not the doctor, change these states.

## 19.5 Queue Entry Status

- `WAITING`
- `CALLED`
- `DONE`
- `REMOVED`

There is no re-entry/requeue state or automatic re-entry mechanism.

## 19.6 Patient-Facing Status Messages

The application may present simplified messages such as:

- Your seat is temporarily held; complete the process before the countdown ends.
- Capacity is temporarily full; use Notify Me When Available.
- Waiting for full-payment completion.
- Payment is under review.
- Appointment confirmed and payment completed.
- Appointment confirmed; payment due at the facility.
- Your arrival window is 12:00–13:00.
- You have checked in.
- Your turn is approaching inside your arrival group.
- The facility cancelled the appointment and a refund has started.
- Visit completed.
- No-show recorded.

All important changes record timestamp, actor, reason, and source where applicable.

## 19.7 Allowed Transition Summary for Modeling

The following transition rules are binding when State, Activity, or Sequence diagrams are produced:

- `ReservationHold`: `ACTIVE -> CONSUMED | EXPIRED | RELEASED`. `CONSUMED`, `EXPIRED`, and `RELEASED` are terminal for that hold.
- `Appointment`: starts as `CONFIRMED`; it may transition to `CANCELLED_BY_PATIENT` or `CANCELLED_BY_FACILITY`. Rescheduling does **not** create a separate appointment status; a successful in-place reschedule keeps `CONFIRMED` and writes history. Cancellation states are terminal for that appointment.
- `VisitInstance`: normal path is `CREATED -> CHECKED_IN -> IN_SERVICE -> COMPLETED`. `CHECKED_IN -> NOT_COMPLETED` or `IN_SERVICE -> NOT_COMPLETED` is allowed when the visit cannot be completed. `CREATED -> NO_SHOW` is allowed after the arrival window ends without valid check-in. `COMPLETED`, `NOT_COMPLETED`, and `NO_SHOW` are terminal visit outcomes. A genuine erroneous check-in may be corrected from `CHECKED_IN -> CREATED` only before service starts, with an audited correction reason and removal of the associated queue entry.
- `QueueEntry`: normal path is `WAITING -> CALLED -> DONE`. `WAITING` or `CALLED` may transition to `REMOVED` only for an audited operational correction/removal. `DONE` and `REMOVED` are terminal for that queue entry. Manual handling of an accepted late patient is a queue-ordering flag/mode, not a new queue status.
- `PaymentIntent`: the supported statuses remain those listed above. Transitions must follow verified gateway/reconciliation events; ordinary facility users cannot force a financial transition. A successful collected payment may enter `REFUND_PENDING -> REFUNDED` when a full refund is required.

---

# 20. Check-in and Actual Visit

An `Appointment` represents a booking commitment within an arrival window. The actual service-day occurrence is represented separately by `VisitInstance`.

Reception staff search for the appointment using:

- Booking number.
- Patient phone number.
- QR code or verification code.

Check-in is allowed only for the intended appointment context and while the `Appointment` is `CONFIRMED`. A patient cannot check in against an appointment already cancelled by the patient or facility. Late arrival is handled by the explicit late-arrival rules rather than by altering appointment status.

At check-in:

1. The system creates `VisitInstance` if one does not already exist.
2. The system sets the visit to `CHECKED_IN`.
3. Actual arrival time is recorded.
4. The appointment's arrival group is associated with the visit.
5. A `QueueEntry` is created or activated inside that group.
6. The patient may see an approximate position or number of patients ahead inside that group.

If a check-in/queue registration is entered incorrectly, facility staff may correct it only before service starts. The `QueueEntry` is moved to `REMOVED`, the correction reason is audited, and the `VisitInstance` may return from `CHECKED_IN` to `CREATED` so that an accidental check-in does not become a false arrival record.

Facility staff, not the doctor, have permission to record:

- `IN_SERVICE`
- `COMPLETED`
- `NOT_COMPLETED`
- `NO_SHOW`

`VisitInstance` stores operational data only, such as:

- Arrival time.
- Arrival group.
- Queue relation.
- Service start.
- Service end.
- No-show outcome.
- Non-completion outcome.

It does not contain diagnosis, prescriptions, test results, or clinical notes.

Patient self-check-in is not part of the current scope.

---

# 21. Arrival Groups and Lightweight Queue

Aafiatak's reception period is separate from the facility's internal booking/walk-in periods for the purpose of this digital allocation model.

Groups distribute patients so that all Aafiatak patients are not asked to arrive at the beginning of one long period.

Example:

- Total Aafiatak period: 12:00–15:00.
- Digital capacity: 10 patients.
- Group 1: 12:00–13:00, capacity 3.
- Group 2: 13:00–14:00, capacity 3.
- Group 3: 14:00–15:00, capacity 4.

The first three confirmed bookings use Group 1, the fourth begins Group 2, and so on.

Within one arrival group:

1. Service order is based on actual check-in time.
2. If two or more patients check in at the same time, the patient with the earlier `confirmed_at` appointment time comes first.
3. Full online payment does not grant priority over pay-at-facility bookings.
4. Aafiatak does not claim to merge or know the facility's full internal queue.

Facility staff may:

- View checked-in patients by group.
- Identify the next patient.
- Call the next patient.
- Record service start.
- Record service completion.
- Remove an incorrect queue entry with a recorded reason.

The doctor may view the same relevant waiting list, identify the next patient, and call the next patient, but may not change visit states.

The patient may view:

- The patient's arrival-group window.
- Check-in confirmation.
- An approximate number/position of patients ahead inside the patient's own group.
- An approaching-turn notification.

The platform does not promise an exact service-entry time.

---

# 22. Late Arrival Rules

## 22.1 Arrival Inside the Group Window

Patients arriving within their group window enter that group's ordering based on actual check-in time.

## 22.2 Arrival Outside the Group Window

When the group window ends without check-in:

- The appointment appears to facility staff as late.
- The system does not automatically move the patient to a later group.
- The system does not create a new automatic queue position.
- The system does not create a re-entry state.
- The system does not guarantee acceptance or priority.

If a patient arrives late, facility staff manually choose an operational result according to reality:

- Accept the patient operationally under the late-arrival rule below.
- Reschedule after agreement and secure valid new capacity.
- Record `NO_SHOW` or `NOT_COMPLETED` according to what actually occurred and the applicable policy.

### Accepted late-patient rule

When facility staff decides to accept a late patient, that decision must occur before a terminal `NO_SHOW` outcome has been recorded for the visit. Once `NO_SHOW` has been validly recorded, the visit is not reopened as a late check-in; any later accommodation requires a documented reschedule/new operational arrangement rather than reversing the terminal no-show outcome.

For an accepted late patient:

1. The original appointment and original `ArrivalGroup` remain unchanged; the system does not automatically move the patient to another group.
2. Staff records check-in on the `VisitInstance` and marks the visit as a late accepted arrival.
3. A `QueueEntry` is created/activated for operational visibility and flagged for **manual handling**. It is excluded from the automatic queue-position calculation used for on-time patients.
4. The patient is not promised a numeric queue position or priority. The interface states that the late arrival has been accepted and is being handled manually by facility staff.
5. Facility staff calls the patient when operationally appropriate.
6. This manual acceptance does not create a re-entry/requeue state and does not consume capacity from another `ArrivalGroup`.

---

# 23. Operational Exceptions

An `OperationalException` represents an unplanned event after publication or during daily operation.

Supported examples include:

- `DOCTOR_DELAYED`
- `DOCTOR_ABSENT`
- `SESSION_CANCELLED`
- `FACILITY_CLOSED`
- `CAPACITY_REDUCED`
- `POWER_OR_CONNECTIVITY_OUTAGE`
- `CONFLICT_DETECTED`

The exception may be linked to the doctor, session, `AvailabilityRelease`, and affected appointments.

Facility staff record the exception. The doctor does not have an in-system button to report delay or absence.

Possible actions include:

- Freeze new capacity/bookings.
- Notify affected patients.
- Update the expected delay range.
- Offer an alternative appointment/group.
- Cancel from the facility side.
- Start a full refund when payment exists and the facility is responsible.
- Escalate the case to support.

For `SESSION_CANCELLED`, the affected release/session is made non-bookable, active `ReservationHold` records are released, and every confirmed appointment remains preserved but must receive a documented resolution (alternative, facility cancellation/full refund when applicable, or escalation). Session cancellation never silently deletes appointments or capacity history.

An exception must not be closed until the action and outcome for affected appointments are recorded.

## 23.1 Conflict After Confirmation

When a conflict is discovered after confirmation:

1. Create `OperationalException` with type `CONFLICT_DETECTED`.
2. Do not close the exception without a documented decision.
3. Approved resolution paths are:
 - Offer a suitable alternative after communicating with the patient.
 - Cancel from the facility side and start a full refund if an amount was paid.
 - Create a documented support escalation if alternative/refund cannot be completed immediately.

A conflict may not be resolved by pulling additional free capacity from the facility's internal schedule into the same Aafiatak release.

---

# 24. Notifications and Reminders

The primary channel for booking, reminder, availability, queue, and operational notifications is in-application/system notifications. Critical situations may also require manual contact. SMS is not used. WhatsApp is used only for authentication/phone verification and is not used for these general notification flows under the current scope.

## 24.1 Patient Notifications

The system may notify the patient that:

- A seat has been temporarily held and show remaining completion time.
- The temporary hold expired and the seat returned to available capacity.
- Capacity is full and Notify Me When Available can be used.
- Capacity became available for a subscribed service/day.
- A full-payment booking was confirmed.
- A pay-at-facility booking was confirmed.
- A payment operation was created, failed, or moved under review.
- A refund started or completed.
- The arrival-group window is approaching.
- Attendance reconfirmation is requested automatically when the facility has enabled it and the configured schedule is reached.
- Failure to reconfirm does not automatically cancel the appointment.
- The appointment/group was changed after communication and agreement.
- Check-in was recorded.
- The patient's turn is approaching.
- A session was cancelled or the doctor is absent, with the applicable next action.
- A no-show was recorded.
- The visit ended operationally.

## 24.2 Facility Notifications

The system may notify facility users about:

- New confirmed full-payment booking.
- New confirmed pay-at-facility booking.
- Successful payment that did not convert into an appointment and requires review.
- Patient cancellation.
- Patient attendance reconfirmation.
- Patient check-in.
- Patient arrival outside the group window.
- `ReservationHold` expiry returning capacity.
- Growth in availability-alert subscriptions.
- `AvailabilityRelease` becoming stale or exhausted.
- Operational exceptions with unresolved affected appointments.

---

# 25. Search and Filtering

The role definitions allow patient discovery/search across facility, doctor, department, specialty, and service information.

For the one-facility pilot, the minimum required implementation is:

- Browse/search by department.
- Browse/search by doctor.
- Display services.
- Display available appointment days/arrival groups from Aafiatak capacity.
- Select or view the city/branch location when needed.

Advanced ranking by rating or “best” is deferred. This specification must not assume broader advanced filters or ranking behavior unless separately approved.

---

# 26. Facility Data Responsibility

The facility is responsible for adding and maintaining its own operational data, including:

- Facility information.
- Images and logo.
- Address and map location.
- Departments.
- Specialties.
- Doctors.
- Services.
- Prices and the single configured facility currency used for the pilot.
- Optional estimated service durations used for patient information.
- Doctor schedules.
- Aafiatak reception periods.
- Arrival groups and group capacities.
- Initial digital capacity allocated to Aafiatak.
- Booking policy.
- The effective `ReservationHold` duration selected from platform-approved values; whether this is a platform default or facility-selectable remains an open decision.
- Cancellation/refund policy for fully paid bookings.
- No-show financial policy for fully paid bookings.
- Attendance instructions.
- Operational instructions for arrivals outside a group window.
- Facility staff accounts and permissions.

The facility is also responsible for executing one-way withdrawal of unused Aafiatak capacity when needed and understanding that withdrawn capacity does not return to the same release.

Aafiatak platform administration does not manage these daily facility records on the facility's behalf.

Aafiatak support may assist with setup or technical support, but does not become responsible for the correctness of the facility's schedules, prices, doctors, or services.

Any exceptional support-side modification must be authorized and audited.

---

# 27. Today Pulse Board

The **Today Pulse Board** is the principal daily operational interface in the facility dashboard.

For each doctor/session it displays:

- Doctor/session state.
- Total Aafiatak reception period.
- Arrival groups and their windows.
- Published capacity.
- Held capacity.
- Confirmed capacity.
- Withdrawn capacity.
- Remaining capacity.
- Capacity values per group where applicable.
- Confirmed appointments.
- Payment operations that are pending or require review.
- Number of availability-alert subscriptions.
- Checked-in patients.
- Waiting patients inside each group.
- Current doctor delay/operational state as recorded by facility staff.
- Open operational exceptions.

Quick actions include:

- Withdraw one seat.
- Withdraw multiple seats.
- Withdraw all remaining capacity.
- Freeze a group or session.
- Close a group or session.
- Cancel a session through the appropriate operational-exception process.
- Record doctor absence or delay through facility staff.
- Register patient check-in.
- Record no-show.

The board does not provide:

- Capacity increase after publication.
- Restoration of withdrawn capacity.
- Manual approval/rejection of booking requests, because such booking-request states do not exist in the approved system model.

---

# 28. Facility Appointment Management

Facility staff can:

- View today's appointments.
- View upcoming appointments.
- Group appointments by arrival group.
- Search by booking number, phone number, or patient name.
- Reschedule after communication/agreement and after securing new capacity.
- Cancel with a recorded reason.
- View appointment state history.
- View independent payment state.
- View active `ReservationHold` records for operational awareness without arbitrarily extending them.

---

# 29. Simple Reports

The facility dashboard includes simple reports covering:

- Today's bookings.
- Confirmed bookings.
- Completed visits.
- Bookings by arrival group.
- Cancellations.
- No-shows.
- Late arrivals.
- Published capacity.
- Confirmed capacity.
- Withdrawn capacity.
- Remaining capacity.
- Expired temporary holds.
- Availability-alert subscriptions.
- Availability-alert-to-booking conversion.
- Stale availability.
- Conflict cases.
- Payment success.
- Payments requiring review.
- Number of bookings per doctor.

Advanced operational analytics are deferred beyond the current scope.

---

# 30. Security, Permissions, Reliability, and Audit

## 30.1 Access Control

The platform uses RBAC with separation between patient, facility, and platform data.

Core access rules:

- A patient sees only the patient's own data.
- Facility staff see only data for their facility within granted permissions.
- Facility administrators manage their facility's data, policies, staff, and arrival groups.
- Booking/reception staff manage daily capacity, bookings, check-in, visit state, and operational exceptions within granted permissions.
- Doctors see their own Aafiatak appointments and checked-in/waiting patients but do not update visit states or report delay/absence inside the system.
- Platform administration does not run daily facility operations.
- Ordinary users cannot delete audit history.
- Disable/archive mechanisms replace hard deletion for records connected to historical operations.
- Unnecessary clinical information is not stored.

## 30.2 Reliability Requirements

The system must:

- Prevent simultaneous consumption of the same capacity unit using atomic transactions and/or suitable database constraints.
- Use idempotency for appointment creation, payment creation, and payment-gateway webhook processing.
- Automatically expire `ReservationHold` records.
- Prevent stuck holds.
- Revalidate `AvailabilityRelease` and `ArrivalGroup` before final appointment confirmation.
- Prevent published-capacity increase after publication at business-logic and database levels.
- Prevent withdrawal of held or confirmed capacity.
- Make `CapacityWithdrawal` irreversible inside the same release.
- Prevent manual arbitrary payment-state changes without an authorized support/verification path.
- Prevent excessive duplicate availability notifications.
- Record every important change to capacity, policy, or lifecycle state with actor, timestamp, and reason where applicable.
- Handle weak connectivity with safe retries.
- Encrypt network communication and protect accounts.
- Revoke active sessions promptly when a user/facility account is disabled or a privileged role is removed.
- Use opaque/unpredictable QR or verification tokens for appointment lookup; QR content must not expose unnecessary patient data.
- Maintain backups, monitoring, and alerts for critical errors.
- Document APIs and separate business logic from user interfaces.
- Remain scalable for future multi-branch support.
- Store booking snapshots of amount, currency, policy, arrival group, and arrival window.
- Treat all appointment/release/group times in the `FacilityBranch` local time zone and persist time-zone-aware timestamps so future multi-branch operation cannot reinterpret historical times.
- Use one configured facility currency in the pilot and perform no currency conversion inside Aafiatak.
- Avoid storing clinical data that the booking process does not need.
- Avoid claiming exact doctor-entry time or knowledge of the facility's entire queue.

## 30.3 User Experience and Platform Non-Functional Requirements

- The interface is Arabic, clear, and responsive.
- The patient experience supports Android and iOS, while facility/platform administration uses responsive web interfaces.
- The system must remain usable under weak connectivity through safe retry behavior rather than duplicate actions.
- Error states and payment/booking cases requiring review must be communicated clearly.
- Ordinary users must not be able to tamper with audit history.

## 30.4 Audited Operations

Important audited operations include:

- Publishing availability.
- Freezing availability.
- Closing availability.
- Freezing/closing arrival groups.
- Withdrawing capacity.
- Creating, expiring, releasing, or consuming `ReservationHold` records.
- Creating availability-alert subscriptions.
- Sending availability notifications.
- Expiring alert subscriptions.
- Creating an appointment.
- Rescheduling an appointment.
- Cancelling an appointment.
- Creating and verifying payment.
- Starting/completing refunds.
- Registering check-in.
- Recording no-show.
- Starting and completing service by facility staff.
- Opening and closing `OperationalException` records.
- Changing price or policy.
- Changing staff accounts/permissions.

---

# 31. Technical Architecture

## 31.1 Patient Application

- Flutter.
- Android and iOS.
- Connects to a centralized server.

## 31.2 Facility Dashboard

- Responsive web dashboard.
- Works on desktop or tablet.
- Role-dependent functionality.

## 31.3 Platform Administration Dashboard

- Protected web dashboard.
- Used by Aafiatak platform staff.

## 31.4 Server Responsibilities

The server is responsible for:

- Authentication.
- Users and roles.
- Facilities and branches.
- Doctors and services.
- Digital availability.
- Aafiatak reception periods.
- Arrival groups.
- One-way capacity withdrawal.
- Temporary reservation and last-seat race prevention.
- Confirmed appointments.
- Availability-alert subscriptions and notifications.
- Full payment, payment intents, and refunds.
- Actual visits and lightweight group queues.
- Operational exceptions.
- Notifications.
- Permissions.
- Audit history.

## 31.5 Database

- PostgreSQL.

## 31.6 External Services

External services are:

- Notification service.
- Map service.
- One payment gateway when approved.
- Official WhatsApp authentication provider/API for phone verification and authentication of human user accounts.

SMS is not used. General-purpose WhatsApp reminders, alerts, support messaging, and operational notifications are deferred; authentication/phone verification is the only in-scope WhatsApp use.

The final backend technology and web-dashboard technology remain open decisions.

---

# 32. Core Logical Entities for System Modeling

The initial logical modeling set includes:

- `User`
- `Patient`
- `MedicalFacility`
- `FacilityBranch`
- `FacilityUser`
- `Role`
- `Permission`
- `Department`
- `Specialty`
- `FacilityDepartment`
- `Doctor`
- `DoctorFacilityAffiliation`
- `MedicalService`
- `ServiceOffering`
- `DoctorSchedule`
- `ScheduleException`
- `BookingPolicy`
- `AvailabilityRelease`
- `ArrivalGroup`
- `CapacityWithdrawal`
- `ReservationHold`
- `AvailabilityAlertSubscription`
- `Appointment`
- `AppointmentStatusHistory`
- `PaymentIntent`
- `VisitInstance`
- `QueueEntry`
- `OperationalException`
- `Notification`
- `FacilitySettings`
- `AuditLog`

This is an initial logical modeling list, not a final class diagram.

## 32.1 Key Entity Semantics

### `User`

Represents the globally unique human identity anchored to a normalized verified phone number. One user identity may be related to a patient profile and/or approved facility/platform roles without duplicating the identity record. Authentication is performed through official WhatsApp OTP.

### `Patient`

Represents patient-specific profile data associated with a `User`. It does not contain clinical-record data.

### `FacilityUser`

Represents a user's membership and role context inside one facility. It is provisioned/managed by the facility administrator and may link to a `Doctor` profile when the role is Doctor.

### `FacilityDepartment`

Represents the facility's selection/association of a public reference `Department`; it prevents treating the platform's reference catalog as though every department exists at every facility.

### `DoctorFacilityAffiliation`

Represents the doctor's association with a facility/branch. The pilot uses the single facility/branch, while the entity preserves future extensibility.

### `MedicalService` and `ServiceOffering`

`MedicalService` represents the general service concept/catalog entry. `ServiceOffering` represents the actual facility/branch offering that the patient books and carries the operational amount, facility currency, optional estimated display duration, doctor linkage, booking policy, cancellation/refund policy, no-show policy, attendance instructions, and activation state.

### `FacilitySettings`

Represents facility-level operational configuration that is not a historical booking commitment, including the pilot facility currency and other approved configurable behavior. Historical terms are still snapshotted into releases/appointments as specified elsewhere.

### `BookingPolicy`

Represents structured booking-policy configuration. The actual operational values applied to a booking are exposed through the relevant `ServiceOffering`. Patient cancellation/refund policy and no-show financial policy are part of those booking terms. Published releases snapshot the commercial/booking terms that apply to that release, and confirmed appointments snapshot the terms that apply to the individual booking so later configuration changes do not rewrite historical commitments.

### `Appointment`

Stores a snapshot of booking conditions at creation time, including:

- Branch.
- Doctor.
- Service.
- Amount.
- Currency.
- Booking policy.
- Arrival group.
- Arrival window.
- Cancellation/refund policy.
- Cancellation window where applicable.
- No-show financial policy.
- Confirmation time.

Core domain lifecycles must not be flattened into scattered appointment fields when they are modeled as independent entities.

### `AvailabilityRelease`

Represents the complete published digital capacity for a specific Aafiatak session. Published capacity becomes an upper bound after publication. At publication, the release also freezes the applicable service amount, currency, booking policy, patient cancellation/refund policy, and no-show financial policy for bookings made from that release.

### `ArrivalGroup`

Represents a smaller arrival window and capacity segment inside `AvailabilityRelease`. Its capacity accounting includes held, confirmed, withdrawn-to-facility, and remaining quantities; bookability also depends on lifecycle state and time eligibility.

### `CapacityWithdrawal`

Represents documented, irreversible-within-the-release transfer of remaining Aafiatak capacity to the facility's internal schedule.

### `ReservationHold`

Represents a short-lived, exclusive temporary seat protection during booking/payment completion.

### `AvailabilityAlertSubscription`

Represents the patient's request to be informed when capacity returns. It provides no seat protection or priority.

### `OperationalException`

Represents an unplanned operational event and tracks affected appointments, actions, and outcome.

### `PaymentIntent`

Represents a full-payment attempt and its independent financial lifecycle, gateway reference, idempotency, and refund relation.

### `VisitInstance`

Represents what actually happens on the service day: check-in, queue relation, service start/end, no-show, or non-completion. Facility staff change visit states, not doctors.

### `QueueEntry`

Represents the patient's lightweight queue position inside the Aafiatak arrival group after check-in. It may carry a manual-handling indicator for an accepted late patient without introducing a new queue status.

### `Notification`

Represents in-application/system notification records and delivery/retry tracking for approved notification events. It is distinct from WhatsApp OTP authentication delivery.

### `AuditLog`

Represents append-only audit evidence for sensitive actions, including actor, time, action/context, and reason/source where applicable. Ordinary users cannot delete or rewrite audit history.

---

# 33. Success Metrics for the Pilot

Suggested pilot success indicators include:

- Number of published `AvailabilityRelease` records.
- Percentage of published capacity booked.
- Distribution of appointments across `ArrivalGroup` records.
- Compliance with arrival windows.
- Number of double-booking/conflict cases per 100 bookings.
- `ReservationHold` to confirmed-booking conversion rate.
- Number/rate of expired holds.
- Return-to-booking behavior after hold expiry.
- Number of Notify Me When Available subscriptions.
- Availability-alert-to-booking conversion rate.
- Number and quantity of `CapacityWithdrawal` operations.
- Number of rejected attempts to increase capacity after publication.
- Number of confirmed appointments.
- Number of completed visits.
- No-show rate.
- Cancellation rate.
- Rescheduling rate.
- Attendance-reconfirmation rate.
- Payment success rate.
- Number of payments requiring review.
- Time to resolve facility cancellation/refund.
- Number of appointments completed without manual phone communication.
- Reception-staff satisfaction with group/capacity management.
- Patient satisfaction with arrival-window, payment, and waiting transparency.
- Core notification delivery success and retry effectiveness.
- Facility continued use after the pilot.

---

# 34. Explicitly Deferred / Out of Current Scope

The following items must not be treated as current-scope requirements.

## 34.1 Patient Features Deferred

- Advanced family/dependent accounts.
- Verified ratings and reviews.
- Advanced complaint system.
- In-app chat.
- Video calls and teleconsultation.
- Medical record/profile.
- Uploading medical reports.
- Prescriptions and test-result storage.
- Insurance.
- Smart recommendations.
- Medication reminders.

## 34.2 Facility Features Deferred

- Cashier and full medical invoicing.
- Accounting.
- Pharmacy/inventory as an internal operating system.
- Laboratory/radiology as an internal operating system.
- Room, bed, device, and clinical-resource management.
- Payroll and HR.
- Replacing the internal system for all phone/walk-in bookings.
- Full calendar mirroring of the facility schedule.
- Advanced queue covering all facility patients.
- Advanced bulk appointment movement.
- Automatic doctor redistribution.
- Advanced operational analytics.
- Highly granular/custom permission designer.
- General-purpose complex workflow/policy engine.
- Full offline operation.
- Separate advanced doctor mobile application.

## 34.3 Payment Features Deferred

- Multiple gateways/wallets.
- Payment splitting.
- Automated settlements and transfers.
- Multi-rule partial refunds.
- Advanced commission/subscription system.
- Tax/financial invoice engine.
- Advanced payment reconciliation reports.

## 34.4 Arrival Group and Queue Features Deferred

- Minute-level predicted doctor-entry time.
- Merging Aafiatak queue with the facility's complete internal queue.
- Complex automatic priority.
- Clinical priority rules.
- Patient selection among multiple arrival groups instead of sequential filling.
- Historical-data-driven automatic group-capacity optimization.
- Automatic transfer/re-entry of a late patient into another group.

## 34.5 Integrations Deferred

- HIS integration.
- EHR integration.
- Public APIs for facilities.
- Facility webhooks.
- Export of Aafiatak bookings to facility systems.
- Automatic doctor/service/schedule import.
- Attendance/queue synchronization with external systems.
- Insurance/laboratory/pharmacy integration.
- CSV/Excel import workflows.
- Specialized integration with legacy facility systems.

## 34.6 Platform Growth Features Deferred

- Advanced automated subscription/commission model.
- Ranking by ratings.
- Advertising or promoted placement.
- AI recommendations.
- Advanced analytics.
- Multi-language expansion.
- Expansion to additional markets as a current-scope requirement.

## 34.7 Communication Channels Deferred

- SMS.
- WhatsApp for appointment confirmations, reminders, availability alerts, queue notifications, operational notifications, support, or general messaging. **Exception:** official WhatsApp OTP for authentication/phone verification is in scope.
- Advanced email workflows.
- Multi-channel template center.
- Integrated contact center.

---

# 35. Resolved Critical Decisions and Remaining Open Decisions

## 35.1 Resolved Critical Decisions

The following decisions are approved and are part of this specification:

1. **Human-user authentication:** patient, facility, doctor, and platform accounts authenticate passwordlessly using short-lived, single-use OTP codes delivered through an official WhatsApp authentication provider/API. Patients may self-register after verification; privileged roles must be provisioned and assigned through RBAC. SMS is not used. WhatsApp remains out of scope for general notifications and messaging.
2. **Confirmed-seat republication after cancellation:** cancelled confirmed capacity returns to the same `ArrivalGroup`. It becomes bookable when the release is `PUBLISHED` and the group is `OPEN`; a zero-to-positive bookable transition may trigger availability alerts. The seat never moves automatically to another group.
3. **Fully paid no-show finance:** the facility chooses the `ServiceOffering` no-show policy: `NO_SHOW_NON_REFUNDABLE` or `NO_SHOW_FULL_REFUND`. The selected policy is snapshotted into the appointment. No partial no-show refund is supported.
4. **Accepted late patient:** the patient remains associated with the original appointment/group, is marked as a late accepted arrival, and is handled manually outside automatic queue-position calculation. No automatic transfer or re-entry state is created.
5. **Rescheduling financial boundary:** in-place rescheduling is allowed only for the same `ServiceOffering` with the same snapshotted financial and booking terms. A different service or changed financial/policy terms require cancellation of the old appointment and creation of a new booking.
6. **Published-release term stability:** service amount, booking policy, cancellation/refund policy, and no-show policy are frozen for a published `AvailabilityRelease`. Changes to the `ServiceOffering` apply only to future releases.
7. **Phone/walk-in booking boundary:** facility staff do not create Aafiatak appointments for phone/walk-in patients. Those channels stay in the facility's internal system and affect Aafiatak only through `CapacityWithdrawal`.
8. **Duplicate-overlap rule:** a patient may not hold or confirm overlapping arrival windows across active holds/confirmed appointments, except inside the controlled atomic rescheduling operation.
9. **Arrival-group booking cutoff:** a new `ReservationHold` is created only when its full configured hold window can expire no later than the selected arrival-group start time (`hold_expires_at <= group.start_at`). Positive numeric remaining capacity does not imply bookability once time/state eligibility fails.
10. **Patient cancellation cutoff:** patient self-cancellation is disabled once the assigned arrival window starts or a valid check-in exists; late/no-show/visit rules then govern the outcome.
11. **Pilot money model:** the pilot uses one configured facility currency, snapshots currency with monetary commitments, and performs no currency conversion.

## 35.2 Remaining Open Decisions

The following implementation/product parameters remain unresolved. They do **not** block UML analysis of the approved business model and must not be invented in diagrams:

1. Payment-gateway provider name, webhook verification mechanism, and exact refund API/process.
2. Default `ReservationHold` duration: three minutes or five minutes, and whether facilities may choose between approved values.
3. Freshness duration before an `AvailabilityRelease` is marked `STALE`.
4. Exact reminder timings and attendance-reconfirmation timing.
5. User limits and anti-spam thresholds for availability alerts.
6. Legal verification requirements for facilities and doctors.
7. Data-retention policy and retention durations.
8. Final backend and web-dashboard technology choices.
9. Final Aafiatak revenue model.
10. Exact official WhatsApp authentication provider/API/template configuration used to deliver OTPs. The authentication model itself is already fixed; only provider-specific integration details remain open.

Arrival-group times and capacities are **not** centrally unresolved product decisions; the facility defines them for each `AvailabilityRelease`.

Subscription, booking/payment commission, or a combination of both are future business-model possibilities. None is part of the approved current scope, and the system does not require an advanced subscription/commission subsystem.

---

# 36. Non-Negotiable System Invariants

The following 35 rules must not be violated by UML models, implementation, database design, or UI behavior:

1. Aafiatak is a booking and supporting coordination platform, not an HIS or EHR.
2. It does not replace the facility's primary system under the current scope.
3. Aafiatak does not include cashier, medical-record, or internal clinical-operation functionality.
4. The facility is responsible for its doctors, services, prices, policies, and digital capacity.
5. Aafiatak platform administration does not manage the facility's daily data on the facility's behalf.
6. Aafiatak does not expose the facility's complete schedule; it exposes only a limited, dedicated `Online Allocation Pool`.
7. Every published capacity allocation is represented by an auditable `AvailabilityRelease` that can be frozen or closed.
8. Published capacity is an upper limit and cannot be increased after publication.
9. Only remaining capacity may be withdrawn from Aafiatak to the facility's internal schedule; there is no reverse transfer.
10. A `CapacityWithdrawal` never consumes an active temporary hold or a confirmed appointment, and the withdrawal cannot be reversed inside the same release.
11. An Aafiatak session is divided into facility-defined `ArrivalGroup` windows with defined capacities.
12. Arrival groups are filled sequentially according to appointment confirmation allocation.
13. Every booking attempt passes through a short-lived, atomic `ReservationHold`.
14. The first user who obtains the temporary hold for the last seat prevents other users from owning that seat until completion, expiry, or release.
15. Hold expiry or release returns the seat to available capacity.
16. Notify Me When Available does not reserve a seat and does not grant priority.
17. The facility configures exactly one of the two approved booking policies for each `ServiceOffering`, and also configures the fully paid no-show policy that will be snapshotted into the appointment.
18. `FULL_PAYMENT_REQUIRED` does not confirm the appointment until the full amount has been paid and trusted payment success has been verified.
19. `PAY_AT_FACILITY` confirms the appointment without electronic payment and makes payment due at the facility.
20. There is no partial payment and there is no booking request waiting for manual facility approval.
21. Patient cancellation of a fully paid appointment follows the cancellation/refund policy snapshotted for that appointment; a recorded `NO_SHOW` follows the separately snapshotted no-show financial policy.
22. Facility cancellation or a facility-responsible conflict leads to an alternative resolution or a full refund of any amount paid.
23. Appointment status is separate from payment status and visit status.
24. Every electronic payment passes through an independent, auditable `PaymentIntent`.
25. An appointment is not the actual visit; the actual visit is represented independently by `VisitInstance`.
26. A patient does not enter the arrival-group queue before facility staff registers check-in.
27. Queue order inside the arrival group is based on actual check-in time; if equal, earlier appointment confirmation time takes precedence.
28. There is no automatic transfer or re-entry mechanism between arrival groups.
29. Within the approved limited role, the doctor views the doctor's appointments and checked-in/waiting patients and may call the next patient.
30. The doctor does not change the visit to `IN_SERVICE`, `COMPLETED`, or `NOT_COMPLETED`, and does not record delay or absence inside Aafiatak.
31. Facility staff record visit-state changes, doctor delay/absence, and operational exceptions.
32. Full payment does not grant clinical or queue priority.
33. Every sensitive operation is recorded in the audit trail.
34. Any feature not included in the approved scope is deferred.
35. Operational simplicity takes precedence over adding unnecessary screens and functionality.

Additional binding identity and boundary rules:
- Human-user authentication uses official WhatsApp OTP and does not use SMS or account passwords under the approved current model.
- General WhatsApp messaging and notifications remain outside the current scope.
- Facility staff do not create Aafiatak bookings for phone/walk-in patients.
- Published release commercial and booking terms do not mutate after publication.
- In-place rescheduling never crosses into different financial or booking terms.
- New holds are created only when the full configured hold window fits before the target arrival-group start time.
- Patient self-cancellation cannot be used after the arrival window starts or after valid check-in.
- The pilot uses one configured facility currency and performs no currency conversion.

---

# 37. Compact End-to-End System Flow

The canonical end-to-end flow is:

1. Facility configures its facility/service/doctor data.
2. Facility defines doctor working windows and planned schedule exceptions.
3. Facility creates an `AvailabilityRelease` with a total Aafiatak period and initial digital capacity.
4. Facility divides the release into sequential `ArrivalGroup` windows whose total capacity equals the published capacity.
5. Facility publishes the release. Published capacity becomes an immutable upper bound for that release.
6. Visitor/patient discovers the facility, doctor, service, price, policy, and available day.
7. The user authenticates through the approved WhatsApp OTP flow when authentication is required; the patient then selects service/doctor/day.
8. System chooses the earliest currently bookable arrival group and displays its arrival window.
9. System atomically creates a `ReservationHold` and starts the countdown.
10. If policy is `FULL_PAYMENT_REQUIRED`, the system creates a `PaymentIntent`, verifies trusted full-payment success, and confirms the appointment while the hold remains valid.
11. If policy is `PAY_AT_FACILITY`, the patient completes the booking and the system confirms the appointment without creating a `PaymentIntent`.
12. If the hold expires or is released, capacity returns to the pool. If a confirmed appointment is cancelled, its seat returns to the same arrival group and becomes bookable when that release/group is in a bookable state.
13. If no capacity is available, the patient may create an `AvailabilityAlertSubscription`.
14. Facility may withdraw unused remaining capacity to its internal schedule, but cannot add internal capacity back to the same release.
15. Before the appointment, the system sends reminders and may request attendance reconfirmation. Lack of reconfirmation does not auto-cancel.
16. On arrival, facility staff locate the booking and register check-in.
17. The system creates/activates `VisitInstance` and `QueueEntry` for the patient's arrival group.
18. Queue order is based on check-in time, then `confirmed_at` for ties.
19. Doctor and staff can see the next relevant patient; doctor may call the patient but cannot change visit lifecycle state.
20. Facility staff record `IN_SERVICE`, `COMPLETED`, `NOT_COMPLETED`, or `NO_SHOW` as appropriate.
21. Operational disruptions are recorded as `OperationalException` and all affected confirmed appointments require documented resolution.
22. All sensitive capacity, booking, payment, visit, policy, and exception operations are audited.

---

# 38. Final Product Statement

Aafiatak is a focused digital medical appointment booking and arrival-coordination platform. It allows patients to discover facilities, departments, specialties, doctors, and services; choose a day from a limited digital capacity explicitly allocated to Aafiatak; receive a realistic arrival window inside a small sequential group; and confirm the booking either through verified full online payment or payment due at the facility according to the service policy.

The system temporarily protects capacity for the first user who starts completion, automatically returns capacity when the temporary hold expires or is released, and allows other interested patients to subscribe for a notification when capacity returns without guaranteeing the seat.

The facility may withdraw unused Aafiatak capacity into its internal schedule in one direction only and may not increase published Aafiatak capacity from internal free time after publication.

The facility operates daily Aafiatak bookings through the Today Pulse Board, including arrival groups, capacity, confirmed appointments, payment review states, patient check-in, lightweight queue management, and operational exceptions. The doctor has a deliberately limited interface for the doctor's own appointments, checked-in patients, and calling the next patient. Facility staff remain responsible for visit-state changes, doctor delay/absence recording, and operational-exception handling.

The central domain concepts that must remain visible in analysis and modeling are:

- `AvailabilityRelease`
- `ArrivalGroup`
- `CapacityWithdrawal`
- `ReservationHold`
- `AvailabilityAlertSubscription`
- `OperationalException`
- `PaymentIntent`
- `VisitInstance`

`QueueEntry` is a supporting entity for the lightweight arrival-group queue. The eight concepts listed above are the central domain components that must remain especially visible in analysis and modeling.

These concepts have independent responsibilities and lifecycles and must not be collapsed into a single appointment status or generic scheduling object.
