# ReForge Backend

FastAPI backend for ReForge.

## Run

```bash
uvicorn app.main:app --reload
```

API documentation is available at:

- Swagger UI: `/docs`
- Scalar: `/scalar`

Run database migrations before using the API:

```bash
alembic upgrade head
```

## Authentication

- `POST /auth/register`
- `GET /auth/confirm-email?token=...`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/signout`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`

Login returns an access token. Send it in the `Authorization` header:

```text
Authorization: Bearer <access_token>
```

The refresh token is stored in an HTTP-only cookie.

## Profile

- `POST /profile`
- `GET /profile`
- `PATCH /profile`

Example profile:

```json
{
  "name": "Sarmad",
  "date_of_birth": "2006-01-01",
  "gender": "male",
  "height_cm": 178,
  "current_weight_kg": 78,
  "activity_level": "moderate",
  "training_frequency": "3–4 days",
  "experience_level": "intermediate",
  "preferred_units": "metric"
}
```

## Goals

- `POST /goals`
- `GET /goals/current`
- `PATCH /goals/current`

Example goal:

```json
{
  "goal_type": "gain_muscle",
  "target_weight_kg": 85,
  "target_date": "2027-03-01"
}
```
