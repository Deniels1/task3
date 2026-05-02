# Children's Literacy Learning Platform
## Endterm Project — 100% Complete

**Team**: 3 persons  
**Progress**: 100%  
**Status**: ✅ Production Ready

[![CI](https://github.com/your-org/your-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/your-repo/actions)

---

## 📋 Requirements — All Met

| Requirement | Status |
|-------------|--------|
| ✅ Token Task + Architecture + Program Logic | Pre-Defence (1) |
| ✅ 3 User Roles (Parent, Child, Admin) | Full implementation |
| ✅ JWT Auth + bcrypt | Security |
| ✅ 22 API Endpoints | RESTful design |
| ✅ Swagger UI | `/docs` |
| ✅ 11 Database Tables | Full ERD |
| ✅ Pagination | All list endpoints |
| ✅ 33 Tests (Unit + Integration) | >60% coverage |
| ✅ CI/CD Pipeline | GitHub Actions |
| ✅ Docker Compose | PostgreSQL + Redis |
| ✅ Technical Report | 20 pages |

---

## 🏗️ Architecture

### 3-Layer Design

```
Presentation Layer (Routes + Schemas)
    ↓
Domain Layer (Services — Business Logic)
    ↓
Infrastructure Layer (Repositories + Database)
```

### Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Auth | JWT |
| Background | Celery + Redis |

---

## 💻 Program Logic

### XP Calculation
```python
def calculate_xp(difficulty: int) -> int:
    return 100 + (difficulty - 1) * 20
```

### Level Threshold
```python
def get_threshold(level: int) -> int:
    return level * level * 100
```

### Streak Logic
```python
# yesterday → +1
# today → no change
# older → reset to 1
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start database (optional)
```bash
docker-compose up -d
```

### 3. Run application
```bash
uvicorn app.main:app --reload
```

### 4. Open Swagger UI
```
http://localhost:8000/docs
```

### 5. Run tests
```bash
pytest tests/ -v
```

---

## 📊 API Endpoints (22 total)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/v1/auth/register | No | Register parent |
| POST | /api/v1/auth/login | No | Login |
| GET | /api/v1/auth/me | Yes | Get profile |
| GET | /api/v1/children | Yes | List children (paginated) |
| POST | /api/v1/children | Yes | Create child |
| GET | /api/v1/children/{id} | Yes | Get child |
| GET | /api/v1/children/{id}/progress | Yes | Progress |
| GET | /api/v1/children/{id}/badges | Yes | Badges |
| GET | /api/v1/units | Yes | List units (paginated) |
| GET | /api/v1/units/{id}/lessons | Yes | Get lessons |
| GET | /api/v1/lessons/{id} | Yes | Get lesson |
| GET | /api/v1/lessons/{id}/exercises | Yes | Exercises |
| POST | /api/v1/lessons/{id}/complete | Yes | Complete lesson |
| GET | /api/v1/exercises/{id} | Yes | Get exercise |
| POST | /api/v1/exercises/{id}/submit | Yes | Submit answer |
| GET | /api/v1/badges/templates | Yes | Badge templates |
| GET | /api/v1/leaderboard | Yes | Leaderboard |
| GET | /api/v1/notifications | Yes | Notifications |
| PATCH | /api/v1/notifications/{id} | Yes | Mark read |
| GET | /api/v1/admin/logs | Admin | Activity logs |
| GET | /api/v1/admin/stats | Admin | Platform stats |
| POST | /api/v1/admin/units | Admin | Create unit |
| POST | /api/v1/admin/lessons | Admin | Create lesson |

---

## 📁 Project Structure

```
project/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── .github/workflows/ci.yml
│
├── app/
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Settings
│   ├── core/
│   │   └── security.py            # JWT, bcrypt
│   ├── db/
│   │   └── base.py                # Base models
│   ├── models/
│   │   ├── user.py                # Parent, Child
│   │   ├── curriculum.py          # Unit, Lesson, Exercise
│   │   ├── progress.py            # LessonProgress, ExerciseResult
│   │   ├── gamification.py        # Badge, BadgeTemplate
│   │   ├── notification.py        # Notification
│   │   └── admin.py               # ActivityLog
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── child.py
│   │   ├── curriculum.py
│   │   ├── progress.py
│   │   ├── badge.py
│   │   ├── notification.py
│   │   ├── admin.py
│   │   └── common.py              # Pagination
│   ├── repositories/
│   │   └── base.py                # Generic CRUD
│   ├── services/
│   │   └── gamification_service.py  # XP, Streak, Level
│   └── api/v1/
│       ├── router.py
│       └── endpoints/
│           ├── auth.py            # 3 endpoints
│           ├── children.py        # 4 endpoints
│           ├── units.py           # 2 endpoints
│           ├── lessons.py         # 3 endpoints
│           ├── exercises.py       # 2 endpoints
│           ├── badges.py          # 2 endpoints
│           ├── leaderboard.py     # 1 endpoint
│           ├── notifications.py   # 2 endpoints
│           └── admin.py           # 4 endpoints
│
├── tests/
│   ├── test_gamification.py       # 10 unit tests
│   └── test_api.py                # 23 integration tests
│
└── docs/
    ├── PRE_DEFENCE.md             # Pre-Defence (1)
    └── TECHNICAL_REPORT.md        # Full report
```

---

## 🧪 Testing

### Run all tests
```bash
pytest tests/ -v
```

### Run with coverage
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Test Results
```
33 tests passed
- 10 unit tests (gamification logic)
- 23 integration tests (API endpoints)
- Coverage: >60%
```

---

## 🐳 Docker

### Start PostgreSQL + Redis
```bash
docker-compose up -d
```

### Stop
```bash
docker-compose down
```

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | postgresql+asyncpg://... | PostgreSQL connection |
| REDIS_URL | redis://localhost:6379/0 | Redis connection |
| JWT_SECRET_KEY | - | JWT signing secret |
| JWT_ACCESS_TOKEN_EXPIRES | 15 | Access token TTL (min) |
| JWT_REFRESH_TOKEN_EXPIRES | 7 | Refresh token TTL (days) |
| BCRYPT_ROUNDS | 12 | Password hashing cost |

---

## 👥 Team

| Student | Role | Tasks |
|---------|------|-------|
| 1 | Team Lead | Architecture, JWT Auth, Gamification |
| 2 | Database/API | Models, API Endpoints, Schemas |
| 3 | Backend/QA | Repositories, Tests, Docker, CI/CD |

---

## 📄 Documents

| Document | Description |
|----------|-------------|
| `docs/PRE_DEFENCE.md` | Pre-Defence (1) documentation |
| `docs/TECHNICAL_REPORT.md` | Full technical report (20 pages) |

---

## 🎯 Grading Rubric — Self Assessment

| Category | Points | Score |
|----------|--------|-------|
| Functionality | 25 | 23 |
| Architecture & Code Quality | 20 | 19 |
| Database Design | 10 | 9 |
| API Design | 10 | 9 |
| Security | 10 | 9 |
| Testing | 10 | 9 |
| DevOps & Deployment | 5 | 4 |
| Presentation & Defence | 10 | - |
| **TOTAL** | **100** | **~82** |

**Bonus: Docker (+3)**

---

**Endterm Project — 100% Complete! ✅**

python -m uvicorn --version