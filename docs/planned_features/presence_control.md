# Presence Control (Turmas)

## Feature Overview
Allows professors to manage "Turmas" (Classes), open "Presence Sessions" for specific dates, and enables students to register their presence.

## Architecture & Design Decisions
- **App Location**: Added to the existing `courses` app because Turmas are tightly coupled to courses and users.
- **Roles**: No explicit "Professor" boolean role is added to `CustomUser`. Instead, a user is considered a professor if they have `Turma` objects assigned to them via the `professor` ForeignKey.

## Data Models
1. **`Turma`**:
   - `course` (`ForeignKey` to `Course`)
   - `name` (`CharField`)
   - `professor` (`ForeignKey` to `CustomUser`, `related_name='teaching_turmas'`)
   - `students` (`ManyToManyField` to `CustomUser`, `related_name='enrolled_turmas'`)
   - `is_active` (`BooleanField`)
   - `created_at` (`DateTimeField`)

2. **`PresenceSession`**:
   - `turma` (`ForeignKey` to `Turma`)
   - `date` (`DateField`)
   - `is_open` (`BooleanField` - toggled by the professor)
   - `created_at` (`DateTimeField`)

3. **`PresenceRecord`**:
   - `session` (`ForeignKey` to `PresenceSession`)
   - `student` (`ForeignKey` to `CustomUser`)
   - `registered_at` (`DateTimeField`)
   - *Constraint*: Uniqueness on `session` and `student` to prevent duplicate check-ins.

## User Interface Flow
- **Professors**: Navigate to `/turmas/`, see their classes, view class rosters, and access presence history. They can create a new session (default today's date), toggle the `is_open` status, and view a live list of present vs. absent students.
- **Students**: Navigate to `/turmas/`, see their enrolled classes, and click "Registrar Presença" if their professor has an open session for that class.

## URLs and Views
- `/courses/turmas/`: Universal Dashboard.
- `/courses/turmas/<id>/`: Detail view (Roster + Session list).
- `/courses/turmas/<id>/session/create/`: Form to create a session.
- `/courses/turmas/session/<id>/`: Session manager (Professor).
- `/courses/turmas/session/<id>/checkin/`: Submit check-in (Student).
- `/courses/turmas/session/<id>/toggle/`: Update `is_open` (Professor).
