# BSF-Nutrifeed Backend System
> DSHub Internship Program — Track 8: Backend Development | Cohort A 2026

A scalable, data-driven Django REST API powering the BSF-Nutrifeed platform for sustainable poultry feed production. Built in alignment with **SDG 3 — Good Health and Well-Being**.

---

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Framework | Django 4.2 + Django REST Framework |
| Auth | JWT via `djangorestframework-simplejwt` |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Docs | Swagger UI + ReDoc via `drf-yasg` |
| Container | Docker + Docker Compose |
| CORS | `django-cors-headers` |

---

## Project Structure
```
Bsf_Nutrifeed/
├── Bsf_nutrifeed/        # Core config (settings, urls, wsgi)
├── users/                # Custom user model, auth endpoints
├── feed_production/      # Feed batches, production logs, dashboard
├── monitoring/           # Larvae growth records, input/output logs
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── seed_data.py
├── DEBUGGING_REPORT.md
└── .env
```

---

## Quick Start

### 1. Clone & set up environment
```bash
git clone https://github.com/Sjaypeter/BSF-NutriFeed
cd bsf_nutrifeed
cp .env
pip install -r requirements.txt
```

### 2. Run migrations & seed data
```bash
python manage.py migrate
python seed_data.py
```

### 3. Start the server
```bash
python manage.py runserver
```

### 4. Or run with Docker
```bash
docker-compose up --build
```

---

## API Endpoints

### Authentication — `/api/auth/`
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register/` | Register new user | Public |
| POST | `/api/auth/login/` | Obtain JWT tokens | Public |
| POST | `/api/auth/logout/` | Invalidate refresh token | Required |
| GET/PATCH | `/api/auth/profile/` | View or update profile | Required |
| POST | `/api/auth/change-password/` | Change password | Required |
| POST | `/api/auth/token/refresh/` | Refresh access token | Public |
| GET | `/api/auth/users/` | List all users | Admin only |

### Feed Production — `/api/feed/`
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET/POST | `/api/feed/batches/` | List or create feed batches | Required |
| GET/PUT/DELETE | `/api/feed/batches/<id>/` | Manage a specific batch | Owner/Admin |
| POST | `/api/feed/logs/` | Add a production log entry | Required |
| GET | `/api/feed/dashboard/` | Aggregated dashboard metrics | Required |

### Monitoring — `/api/monitoring/`
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET/POST | `/api/monitoring/larvae/` | Larvae growth records | Required |
| GET/PUT/DELETE | `/api/monitoring/larvae/<id>/` | Specific larvae record | Required |
| GET/POST | `/api/monitoring/io-logs/` | Input/output logs | Required |
| GET | `/api/monitoring/summary/` | Monitoring summary stats | Required |

---

## Authentication
All protected endpoints require a `Bearer` token in the `Authorization` header:
```
Authorization: Bearer <access_token>
```

---

## API Documentation
Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/

---

## Demo Credentials (after running seed_data.py)
| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `Admin@1234` |
| Farmer | `farmer_amaka` | `Farmer@1234` |
| Farmer | `farmer_seun` | `Farmer@1234` |

---

## Sample API Requests

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myfarm",
    "email": "me@farm.ng",
    "password": "StrongPass@1",
    "password2": "StrongPass@1",
    "role": "farmer",
    "farm_name": "My Poultry Farm",
    "farm_location": "Lagos, Nigeria"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "farmer_amaka", "password": "Farmer@1234"}'
```

### Create a Feed Batch
```bash
curl -X POST http://localhost:8000/api/feed/batches/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "batch_code": "BSF-2026-099",
    "bsf_larvae_kg": 60,
    "organic_waste_kg": 250,
    "water_liters": 35,
    "production_date": "2026-03-26"
  }'
```

### View Dashboard
```bash
curl http://localhost:8000/api/feed/dashboard/ \
  -H "Authorization: Bearer <token>"
```

---

*Built with purpose for DSHub Internship — Otondo Team | SDG 3*