# GraveyardGfsiDjango

This directory contains:

- `database`: the backend database directory.
- `st_anthony`: the frontend Django application directory.

## Features

### Public search & records
- Home page search across deceased records — full-name/year default search, or filter by First Name, Last Name, Year of Birth, Year of Death, or Date Buried, with dynamic htmx-powered results (no page reload) and inline validation for bad input.
- Detail page per deceased person: personal info, plot info, contact info, payment status, maintenance history, and notes.

### Plot & cemetery map
- Section/plot map with grid layout, including special columbarium (niche) layout logic.
- Individual plot detail view with reservation status, maintenance status, and notes.
- Plot reservation workflow: reserve, cancel reservation, generate a reservation certificate, mark engraving complete, and a `PlotReservationHistory` audit trail.

### Plot & family management (staff-facing, login-required)
- Manage Plots dashboard.
- Add/edit/delete deceased records per plot, including a deceased-specific notes section.
- Add/edit/delete contacts per plot (with primary-contact designation), plus contact payment editing.
- Plot-level notes (add/edit/delete).

### Auth
- Custom `Users` model/auth backend (role-based: Admin/Basic) with login/logout, separate from Django's default user model.

### Public content pages
- About Us — parish write-up, Our Staff / Mass Times / Churches photo cards, Pastoral Care Center block, newsletter signup.
- Contact Us — parish office details, a working contact form (persists to DB, optional email notification), the three churches' full addresses, and the same newsletter signup.

### Data capture (Django-managed tables)
- `ContactMessage` — contact form submissions (table `cemetery_contactmessage`; read them in MySQL Workbench).
- `NewsletterSubscriber` — email signups (table `cemetery_newslettersubscriber`; read them in MySQL Workbench).

The Django admin site (`/admin/`) is disabled.

### Tech stack
- Django 6 + MariaDB/MySQL (mirrors most tables from an existing schema via `managed=False`), Tailwind CSS (pre-built, no Node needed at runtime), htmx for dynamic UI throughout, django-tailwind for styling pipeline.
