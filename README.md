# 🪲 BSF-Nutrifeed Backend System

> A scalable REST API backend powering sustainable poultry feed production using Black Soldier Fly (BSF) larvae — built in alignment with **UN SDG 3: Good Health and Well-Being**.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?style=flat-square&logo=django)
![DRF](https://img.shields.io/badge/DRF-3.14-red?style=flat-square)
![JWT](https://img.shields.io/badge/Auth-JWT-purple?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📖 About

BSF-Nutrifeed is a data-driven platform that supports farmers in managing sustainable poultry feed production from Black Soldier Fly larvae. This backend system handles all server-side logic — from user management and feed batch tracking to larvae growth monitoring and real-time farm metrics.

Built as part of the **DSHub Internship Program — Cohort A 2026** under the Otondo Team, Track 8: Backend Development.

---

## ✨ Features

- 🔐 **JWT Authentication** — secure login, registration, token refresh, and logout
- 👥 **Role-Based Access** — farmer and admin roles with scoped data permissions
- 🌾 **Feed Batch Management** — full lifecycle tracking from input to harvested feed
- 🐛 **Larvae Growth Monitoring** — stage-by-stage growth records with environmental data
- 📦 **Input/Output Logging** — material tracking with cost logging in Nigerian Naira
- 📊 **Dashboard Metrics** — aggregated farm statistics (feed produced, protein content, conversion ratio)
- 📄 **API Documentation** — interactive Swagger UI and ReDoc
- 🐳 **Docker Ready** — containerized with multi-stage Dockerfile and Docker Compose

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | Django 4.2 + Django REST Framework |
| Authentication | JWT via `djangorestframework-simplejwt` |
| Database | SQLite (development) / PostgreSQL (production) |
| API Docs | Swagger UI + ReDoc via `drf-yasg` |
| Containerization | Docker + Docker Compose |
| CORS | `django-cors-headers` |

---

## 📁 Project Structure

```
bsf_nutrifeed/
├── bsf_nutrifeed/          # Core config — settings, urls, wsgi
├── users/                  # Custom user model, auth endpoints
├── feed_production/        # Feed batches, production logs, dashboard
├── monitoring/             # Larvae growth records, input/output logs
├── seed_data.py            # Demo data seeder
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- pip
- Docker (optional)

### 1. Clone the repository

```bash
git clone https://github.com/Sjaypeter/BSF-NutriFeed.git
cd BSF-NutriFeed/Bsf_nutrifeed
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed demo data (optional)

```bash
python seed_data.py
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## 🐳 Running with Docker

```bash
docker-compose up --build
```

This starts the Django app alongside a PostgreSQL database container.

---

## 📡 API Endpoints

### Authentication — `/api/auth/`

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/auth/register/` | Register a new user | Public |
| POST | `/api/auth/login/` | Obtain JWT tokens | Public |
| POST | `/api/auth/logout/` | Invalidate refresh token | Protected |
| GET/PATCH | `/api/auth/profile/` | View or update profile | Protected |
| POST | `/api/auth/change-password/` | Change password | Protected |
| POST | `/api/auth/token/refresh/` | Refresh access token | Public |
| GET | `/api/auth/users/` | List all users | Admin only |

### Feed Production — `/api/feed/`

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET/POST | `/api/feed/batches/` | List or create feed batches | Protected |
| GET/PUT/DELETE | `/api/feed/batches/<id>/` | Manage a specific batch | Owner/Admin |
| POST | `/api/feed/logs/` | Add a production log entry | Protected |
| GET | `/api/feed/dashboard/` | Aggregated farm dashboard metrics | Protected |

### Monitoring — `/api/monitoring/`

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET/POST | `/api/monitoring/larvae/` | Larvae growth records | Protected |
| GET/PUT/DELETE | `/api/monitoring/larvae/<id>/` | Specific larvae record | Protected |
| GET/POST | `/api/monitoring/io-logs/` | Input/output material logs | Protected |
| GET | `/api/monitoring/summary/` | Monitoring summary stats | Protected |

---

## 🔑 Authentication

All protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

Tokens are obtained from `/api/auth/login/`. Access tokens expire after **2 hours**; use the refresh endpoint to get a new one.

---

## 📚 API Documentation

With the server running, visit:

- **Swagger UI** — http://127.0.0.1:8000/swagger/
- **ReDoc** — http://127.0.0.1:8000/redoc/

---

## 🧪 Demo Credentials

After running `seed_data.py`:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `Admin@1234` |
| Farmer | `farmer_amaka` | `Farmer@1234` |
| Farmer | `farmer_seun` | `Farmer@1234` |

---

## 📬 Sample Requests

### Register a new farmer

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
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

### Login and get token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "farmer_amaka", "password": "Farmer@1234"}'
```

### Create a feed batch

```bash
curl -X POST http://127.0.0.1:8000/api/feed/batches/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "batch_code": "BSF-2026-099",
    "bsf_larvae_kg": 60,
    "organic_waste_kg": 250,
    "water_liters": 35,
    "production_date": "2026-03-29"
  }'
```

### View dashboard metrics

```bash
curl http://127.0.0.1:8000/api/feed/dashboard/ \
  -H "Authorization: Bearer <token>"
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🏫 Acknowledgements

Built as part of the **DSHub Internship Program — Cohort A 2026**
Case Partner: **Otondo Team by DSHub**
Focus SDG: **SDG 3 — Good Health and Well-Being**

> *"Behind every seamless experience is a system built with structure, security, and purpose."*
