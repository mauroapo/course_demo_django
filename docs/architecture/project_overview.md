# Project Architecture Overview

This document provides a high-level overview of the ONG Course Platform architecture. **Please ensure to review these descriptions before proceeding with major changes to the codebase.**

## Technology Stack
- **Backend Framework**: Django 4.2+ (Python) with Django REST Framework (DRF) for API endpoints when needed.
- **Database**: PostgreSQL 15, managed through Django ORM.
- **Web Server / Reverse Proxy**: Nginx (serves static/media files and proxies to Gunicorn on port 80).
- **Application Server**: Gunicorn (runs Django WSGI on port 8001 internally).
- **Environment Management**: Docker and Docker Compose orchestrate `web`, `db`, and `nginx` services. Variables are loaded via `.env` (using `python-decouple`).

## Core Business Domain
The platform serves two primary business models:
1. **B2C (Individual Consumers)**: End-users register with their emails, browse the course catalog, add items to their cart, proceed through checkout, and start studying their acquired courses. Progress and quiz results are actively tracked.
2. **B2B (Organizations)**: NGOs/companies can purchase bulk "packages" with a specific seat count. Organization members or administrators can assign these purchased course seats to specific employees/members within their organization.

## Key Integration Points
- **Course Area Integration**: The platform interacts with an external course application (`COURSE_AREA_BASE_URL`) through signed tokens for actual video/lesson delivery when separated from the monolithic flow.
- **Emails**: Uses standard Django email backends in development (`console`) and configurable SMTP settings for production (or external transactional email APIs like Resend).
- **CORS/CSRF Protection**: Heavily configured in `settings.py` for a tight set of trusted origins, accommodating local development, proxy servers, frontend single-page apps (if any), and remote environments like Cloudflare and Nginx.

## Folder Structure Summary
- `accounts/`: Authentication, User models (custom `CustomUser`), Profile, and password/email verification codes.
- `cart/`: Shopping cart functionality logic (adding courses before checkout).
- `checkout/`: Processing flows for turning a cart into a purchased enrollment.
- `core/`: Global utilities, middleware (e.g., `AuthRequiredMiddleware`), base templates, and common generic logic not tied to a specific domain.
- `courses/`: The heart of the platform. Handles the course catalog, modules, lessons, quizzes, questions, enrollments, and student progress tracking.
- `orgs/`: B2B logical grouping, handling organization members, course packages, and seat allocation to users.
- `ong_platform/`: Core Django settings (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).
- `nginx/`: Docker-integrated Nginx configurations.
