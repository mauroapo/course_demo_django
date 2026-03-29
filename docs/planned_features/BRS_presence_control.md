# Business Requirements Specification (BRS): Presence Control (Turmas)

## 1. Introduction
### 1.1 Purpose
The purpose of this document is to define the business requirements for the "Presence Control" feature. This feature aims to empower professors to manage class cohorts (Turmas) and systematically track student attendance within the Course Platform.

### 1.2 Scope
This feature includes the creation of classes (Turmas), linking professors and students to these classes, session management by professors, and self-service attendance registration by students. It does not cover advanced grading or automatic check-ins based on geolocation/IP.

## 2. User Roles
- **Professor**: An instructor designated to a specific `Turma`, responsible for opening/closing presence sessions and monitoring which students are attending.
- **Student**: A user enrolled in a `Turma` who needs to mark their presence during an open session.
- **System Administrator**: Has global privileges to create `Turmas`, and define who is the Professor and who are the Students.

## 3. Functional Requirements
### 3.1 Class (Turma) Management
- **FR1**: The system must support `Turmas`, which link a specific Course, a single Professor, and a roster of Students.
- **FR2**: Professors must be able to access a dashboard displaying all `Turmas` they manage.
- **FR3**: Students must be able to view a dashboard with all `Turmas` they are enrolled in.
- **FR4**: Inside a `Turma`, the Professor can see the full roster of students.

### 3.2 Presence Session Management (Professor)
- **FR5**: A Professor must be able to create a new "Presence Session" for any given date (automatically defaulting to the current date).
- **FR6**: A Professor must have a toggle mechanism (e.g., a checkbox) to change a session's status between "Open" (available for check-in) and "Closed".
- **FR7**: A Professor must be able to view a live breakdown of attendance for a specific session: a list of students who have checked in, and a list of those who have not.
- **FR8**: A Professor must be able to see a historical summary table of all past sessions within a `Turma`, detailing the date and total attendance count.

### 3.3 Presence Registration (Student)
- **FR9**: Students must only be prompted to register their presence if the Professor has set the session's status to "Open".
- **FR10**: Students must be able to register their presence with a single click/action.
- **FR11**: The system must ensure a student can only register their presence once per session.

## 4. Non-Functional Requirements
- **NFR1 (Security/Authorization)**: 
  - Students cannot view or modify presence records of other students. 
  - Students can only check into `Turmas` they belong to. 
  - Only the assigned Professor (or an Admin) can manipulate session statuses for their `Turma`.
- **NFR2 (Usability)**: The check-in interface must be highly responsive and mobile-friendly, accommodating students who log in via smartphones during a live class or lecture.
- **NFR3 (Auditability)**: Every presence record must capture the exact timestamp of when the student clicked the check-in button.

## 5. Acceptance Criteria
- **Scenario 1: Opening a Session**
  - *Given* the Professor selects a `Turma` and initiates a "Nova Lista de Presença",
  - *When* they confirm the date and toggle the session to "Open",
  - *Then* the new session is created and immediately becomes visible/actionable for all enrolled students.
  
- **Scenario 2: Registering Presence**
  - *Given* a session is "Open",
  - *When* an enrolled Student navigates to the `Turma` page and clicks "Registrar Presença",
  - *Then* the system records their presence, displays a success message, and removes the prompt so they cannot register again.
  
- **Scenario 3: Monitoring Attendance**
  - *Given* an active session,
  - *When* the Professor views the session details page,
  - *Then* they clearly see two distinct lists indicating exactly which students are "Present" and which are "Absent".

