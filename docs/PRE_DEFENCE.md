# Pre-Defence (1) — Children's Literacy Platform

## Token Task + Architecture Design + Program Logic

**Progress: 40%+** | **Team: 3 persons**

---

## 1. Token Task (Декомпозиция)

```
EPIC 1: Foundation (20%)         ✅ DONE
  ├── Database design
  ├── Models (Parent, Child, Lesson)
  └── Authentication (JWT)

EPIC 2: Core Features (40%)      ✅ DONE
  ├── Child profile management
  ├── Lesson completion
  └── XP & Streak calculation

EPIC 3: Gamification (20%)       🔄 IN PROGRESS
  ├── Badge system
  └── Level-up logic

EPIC 4: Async & Testing (20%)    ⏳ PLANNED
  ├── Background jobs (Celery)
  ├── Tests
  └── Docker deployment
```

---

## 2. Architecture Design

### 3-Layer Architecture

```
┌─────────────────────────────────────┐
│  PRESENTATION LAYER                 │
│  FastAPI Routes + Pydantic Schemas  │
│  /api/v1/auth, /children, /lessons  │
└──────────────┬──────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────┐
│  DOMAIN LAYER (Business Logic)      │
│  Services: XP, Streak, Level, Auth  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  INFRASTRUCTURE LAYER               │
│  Repositories + PostgreSQL          │
└─────────────────────────────────────┘
```

### ER-Diagram

```
PARENT (1) ────────< CHILD (N)
    │                    │
    │                    ├────< LESSON_PROGRESS (N)
    │                    │
    │                    └────< BADGE (N)
    │
    └────< NOTIFICATION (N)

UNIT (1) ────────< LESSON (N) ────────< EXERCISE (N)
```

### Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| Backend | FastAPI | Async, auto Swagger |
| Database | PostgreSQL | JSONB, ACID |
| ORM | SQLAlchemy | Standard for Python |
| Auth | JWT | Stateless, scalable |
| Background | Celery + Redis | Async tasks |

---

## 3. Program Logic

### 3.1 XP Calculation

```python
def calculate_xp(difficulty: int) -> int:
    return 100 + (difficulty - 1) * 20

# Examples:
# Difficulty 1 → 100 XP
# Difficulty 2 → 120 XP
# Difficulty 3 → 140 XP
```

### 3.2 Level System

```python
def get_threshold(level: int) -> int:
    return level * level * 100

# Level 1 → 2: 100 XP (1² × 100)
# Level 2 → 3: 400 XP (2² × 100)
# Level 3 → 4: 900 XP (3² × 100)
```

### 3.3 Streak Logic

```python
# Rules:
# - If active today → no change
# - If active yesterday → streak + 1
# - Otherwise → reset to 1

def update_streak(last_activity, streak):
    if last_activity == today:
        return streak          # No change
    elif last_activity == yesterday:
        return streak + 1      # Continue
    else:
        return 1               # Reset
```

---

## 4. API Endpoints

```
POST /api/v1/auth/register          ✅ Register parent
POST /api/v1/auth/login             ✅ Login
GET  /api/v1/auth/me                ✅ Get profile

GET  /api/v1/children               ✅ List children
POST /api/v1/children               ✅ Create child
GET  /api/v1/children/{id}          ✅ Get child
GET  /api/v1/children/{id}/progress ✅ Get progress

GET  /api/v1/units                  ✅ List units
GET  /api/v1/units/{id}/lessons     ✅ Get lessons

GET  /api/v1/lessons/{id}           ✅ Get lesson
GET  /api/v1/lessons/{id}/exercises ✅ Get exercises
POST /api/v1/lessons/{id}/complete  ✅ Complete lesson

GET  /api/v1/leaderboard            ✅ Leaderboard
```

---

## 5. Project Structure

```
project/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── .env.example
│
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── core/
│   │   └── security.py      # JWT, bcrypt
│   ├── db/
│   │   └── base.py          # Base models
│   ├── models/
│   │   ├── user.py          # Parent, Child
│   │   └── curriculum.py    # Unit, Lesson, Exercise
│   ├── services/
│   │   └── gamification_service.py  # XP, Streak, Level
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── child.py
│   │   ├── curriculum.py
│   │   └── progress.py
│   ├── repositories/
│   │   └── base.py          # Generic CRUD
│   └── api/v1/
│       ├── router.py
│       └── endpoints/
│           ├── auth.py
│           ├── children.py
│           ├── units.py
│           ├── lessons.py
│           └── leaderboard.py
│
├── tests/
│   └── test_gamification.py
│
└── docs/
    └── PRE_DEFENCE.md
```

---

## 6. Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start PostgreSQL and Redis
docker-compose up -d

# 3. Run application
uvicorn app.main:app --reload

# 4. Open Swagger
http://localhost:8000/docs

# 5. Run tests
pytest tests/ -v
```

---

## 7. Team Distribution (3 persons)

| Student | Role | Tasks |
|---------|------|-------|
| 1 | Team Lead | Architecture, JWT Auth, Gamification |
| 2 | Database/API | Models, API Endpoints, Schemas |
| 3 | Backend/QA | Repositories, Tests, Docker |

---

## 8. Q&A Preparation

| Question | Answer |
|----------|--------|
| Architecture? | 3 layers: Routes → Services → Repositories |
| XP formula? | `100 + (difficulty - 1) × 20` |
| Level formula? | `level² × 100` |
| Streak logic? | yesterday→+1, today→no change, older→reset |
| Child protection? | `WHERE parent_id = current_user.id` |
| Why PostgreSQL? | JSONB for exercises, ACID transactions |
| Why FastAPI? | Async, automatic Swagger, Pydantic validation |

---

**Pre-Defence (1) Ready! ✅**
