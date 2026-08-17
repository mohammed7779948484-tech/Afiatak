# MVP Class Diagram Implementation Checklist

## Authoritative contract

- Title: `Class Diagram — Aafiatak Medical Appointment Booking System (MVP)`.
- Exactly 30 domain/entity classes, 52 semantic relationships, and 10 UML notes.
- Visible labels remain English.
- Status remains `awaiting-user-approval`.
- One A3-equivalent landscape master sheet is required unless readability demonstrably fails.

## Structural rules

- Every class has name, attributes, operations, and responsibility compartments.
- Attributes are private (`-`); operations are public (`+`); no programming data types or ERD/PK/FK notation.
- Relationships use the R01–R52 matrix exactly, with multiplicity at both ends.
- Exactly 7 compositions with filled diamond at the lifecycle-owning whole.
- Exactly 2 aggregations with hollow diamond at Facility.
- Generalization = 0; Realization = 0.
- Exactly 10 approved UML notes N1–N10.

## Critical semantic safeguards

- `User` has associations, not inheritance, to Patient, FacilityUser, and PlatformRoleAssignment.
- `PlatformRoleAssignment` is mandatory.
- `OperationalExceptionResolution` is mandatory and composed by OperationalException while associated to Appointment.
- ReservationHold, Appointment, PaymentIntent, VisitInstance, and QueueEntry remain separate lifecycles.
- No external service classes, clinical/HIS/cashier/accounting entities, or deferred MVP concepts.

## Presentation and QA

- Use six whitespace-only zones: Identity & Access; Platform & Reference Data; Facility & Medical Offering; Schedule & Digital Availability; Appointment & Payment; Visit, Queue & Operational Exceptions.
- Do not render the zones as UML packages.
- Open the rendered PNG/SVG/PDF and complete semantic, relationship, routing, and page-composition checks.
- Deliver SVG, high-resolution PNG, editable draw.io source, and updated vector PDF.
