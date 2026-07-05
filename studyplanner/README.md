# Study Planner

A Django + Django REST Framework project for managing subjects, tasks,
study sessions, and notes — built with both a server-rendered template UI
and a token-authenticated JSON API.

## Group Members
- Kainazar Nurdaulet
- Almaskhanov Abylay
- Baigaliyev Dastan

## Features

### Front-end (Django Templates)
- Login / logout / registration
- Dashboard with task filtering by subject (`{% if %}` / `{% for %}`)
- ModelForms: Subject, Task, Note, Register
- Event handlers: mark task done/undo, delete task, filter dropdown, submit forms
- Custom template tag (`overdue_count`) + custom context processor (`pending_task_count`)
- Flash messages for success/error states, custom 404 page

### Back-end (Django + DRF)
- 4 models: `Subject`, `Task` (custom manager), `StudySession`, `Note`
- 2 ForeignKey relationships: `Task → Subject`, `StudySession → Task`
- Serializers: 2x `ModelSerializer` (Subject, Task), 2x `Serializer` (StudySession, Note)
- Views: 2x FBV with `@api_view` (`task_list_create`, `task_detail`), 2x CBV `APIView`
  (`SubjectListCreateView`, `StudySessionView`, plus extras)
- Token authentication (`/api/auth/login/`, `/api/auth/logout/`)
- Full CRUD on `Task`
- CORS enabled via `django-cors-headers`

## Setup

```bash
python -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the template UI and
`http://127.0.0.1:8000/admin/` for the Django admin.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/login/` | Get auth token |
| POST | `/api/auth/logout/` | Invalidate token |
| GET/POST | `/api/tasks/` | List / create tasks |
| GET/PUT/DELETE | `/api/tasks/<id>/` | Retrieve / update / delete a task |
| GET/POST | `/api/subjects/` | List / create subjects |
| GET/PUT/DELETE | `/api/subjects/<id>/` | Retrieve / update / delete a subject |
| GET/POST | `/api/sessions/` | List / create study sessions |
| GET/POST | `/api/notes/` | List / create notes |

Send `Authorization: Token <your_token>` header for authenticated requests.

## Postman
Import `postman_collection.json` from the repo root — it contains example
requests and captured example responses for every endpoint above.
