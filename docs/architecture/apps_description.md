# Apps Description Detailed

This document breaks down the internal responsibilities of each Django application within the platform. **Review this file before attempting to add or modify models to ensure correct separation of concerns.**

## 1. `accounts` App
Manages everything related to identities and authentication.
- **Key Models**: 
  - `CustomUser`: Replaces the default Django User model, using `email` as the unique username instead of a traditional `username` field.
  - `Profile`: Holds auxiliary information (date of birth, nationality).
  - `EmailVerificationCode` & `PasswordResetCode`: Handles TTL (Time-To-Live) tokens for email swaps and password resets.

## 2. `courses` App
The most complex application, managing course structures, enrollments, and student progress.
- **Catalog Models**:
  - `Course`: The core entity, has a price, name, and description.
  - `Enrollment`: Links a `CustomUser` to a `Course`. Has a `source` to define whether it was bought individually or assigned via an org package.
- **Content Models**:
  - `Module`: Groups lessons together.
  - `Lesson`: Contains rich text content and optionally a video URL (YouTube/Vimeo).
- **Assessment Models**:
  - `Question` & `QuestionOption`: Reusable quiz questions (multiple choice, true/false, short answer).
  - `Quiz` & `QuizQuestion`: Assessments inserted into Modules.
  - `QuizAttempt` & `StudentAnswer`: Tracks when a user takes a quiz, what they picked, and if they passed.
- **Tracking**:
  - `StudentProgress`: Links users to either a completed `Lesson` or `Quiz`.

## 3. `cart` App
Handles pre-purchase intent.
- **Key Models**:
  - `Cart`: A one-to-one link to a `CustomUser`.
  - `CartItem`: Links the user's `Cart` to a specific `Course`. Limits users to adding a course only once.

## 4. `checkout` App
Responsible for the transition from `Cart` items to `Enrollment` items.
- *Note:* In the current MVP, this app primarily houses views, forms, and business logic rather than database models. Future iterations may include models like `Order`, `OrderItem`, and `PaymentTransaction`.

## 5. `orgs` App
Encapsulates B2B organization logic, moving away from single-user B2C flows.
- **Key Models**:
  - `Organization`: The top-level company/NGO entity.
  - `OrgMember`: Links a `CustomUser` to an `Organization` with roles like 'admin' or 'member'.
  - `OrgPackage` & `OrgPackageItem`: Represents a bulk purchase containing a set limit of `seat_count` for specific courses.
  - `OrgSeatAssignment`: Represents a consumed seat from a package, linking the user getting the course to the specific organization package.

## 6. `core` App
Houses cross-app infrastructure.
- Does not contain domain models.
- Contains project-wide middleware (e.g., `AuthRequiredMiddleware`), base templates, UI components, and global utilities.
