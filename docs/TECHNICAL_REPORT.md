# Children's Literacy Learning Platform
## Technical Report

**Team**: 3 students  
**Date**: 2024  
**Repository**: [GitHub URL]  
**Deployment**: [Live URL]

---

## 1. Project Overview

A production-grade backend for a children's literacy learning platform inspired by Duolingo ABC. The platform teaches children to read through phonics, handwriting, sight words, and vocabulary using a gamified, curriculum-driven approach.

### Tech Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Backend | FastAPI | Async support, automatic OpenAPI docs, Pydantic validation |
| Database | PostgreSQL | JSONB support, ACID transactions, production-ready |
| ORM | SQLAlchemy 2.0 | Modern async ORM, type-safe queries |
| Auth | JWT (python-jose) | Stateless auth with refresh tokens |
| Background | Celery + Redis | Async task processing |
| Testing | pytest + httpx | Unit and integration testing |
| CI/CD | GitHub Actions | Automated testing on PR |

---

## 2. Architecture

### 2.1 Layered Architecture

```
┌─────────────────────────────────────────────────────┐
│              Presentation Layer                      │
│         FastAPI Routes + Pydantic Schemas           │
│  /auth, /children, /lessons, /units, /leaderboard   │
└────────────────────────┬────────────────────────────┘
                         │ HTTP Request/Response
┌────────────────────────▼────────────────────────────┐
│              Domain Layer (Business Logic)           │
│              Services: XP, Streak, Badges            │
│     GamificationService, AuthService, etc.          │
└────────────────────────┬────────────────────────────┘
                         │ Service Calls
┌────────────────────────▼────────────────────────────┐
│              Infrastructure Layer                    │
│     Repositories + PostgreSQL + Redis               │
│     BaseRepository, ChildRepository, etc.           │
└─────────────────────────────────────────────────────┘
```

### 2.2 Key Design Decisions

1. **Strict Separation of Concerns**: Controllers handle HTTP only, Services contain business logic, Repositories manage data access.
2. **Dependency Injection**: Services and repositories injected via FastAPI dependencies.
3. **Async-First**: All I/O operations use async/await for scalability.
4. **RBAC**: Role-based access control at route level.
5. **Child Data Isolation**: Parent can only access their own children via ownership checks.

---

## 3. Database Design (ERD)

```
PARENT (1) ────────────< CHILD (N)
    │                        │
    │                        ├────< LESSON_PROGRESS (N)
    │                        │              │
    │                        │              └────< EXERCISE_RESULT (N)
    │                        │
    │                        └────< BADGE (N)
    │                                  │
    │                                  └──── BADGE_TEMPLATE (1)
    │
    ├────< NOTIFICATION (N)
    │
    └────< ACTIVITY_LOG (N)

UNIT (1) ────────────< LESSON (N) ────────────< EXERCISE (N)
```

### Tables (11 total)

| Table | Description |
|-------|-------------|
| `parents` | Parent/guardian accounts |
| `children` | Child learner profiles |
| `units` | Curriculum units |
| `lessons` | Lessons within units |
| `exercises` | Exercises within lessons |
| `lesson_progress` | Child's progress on lessons |
| `exercise_results` | Results of exercise attempts |
| `badge_templates` | Badge definitions |
| `badges` | Badges earned by children |
| `notifications` | Parent notifications |
| `activity_logs` | Admin action audit trail |

### Indexes

- `parents.email` (unique)
- `children.parent_id` (foreign key)
- `children.xp_total` (leaderboard queries)
- `children.streak_last_activity_date` (streak evaluation)
- `lessons.unit_id` (foreign key)
- `lessons.published` (filtering)
- `exercises.lesson_id` (foreign key)
- `lesson_progress.child_id`, `lesson_progress.lesson_id` (composite)
- `badges.child_id` (foreign key)
- `notifications.parent_id` (foreign key)

---

## 4. API Design

### RESTful Conventions

- Resource-based URLs: `/api/v1/children`, `/api/v1/lessons/{id}`
- Correct HTTP methods: GET, POST, PUT, PATCH, DELETE
- Consistent error format: `{"error": {"code": "...", "message": "..."}}`
- Versioned: `/api/v1/`

### Endpoints (22 total)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/auth/register` | POST | No | Parent registration |
| `/auth/login` | POST | No | Login |
| `/auth/me` | GET | Yes | Current user profile |
| `/children` | GET | Yes | List children (paginated) |
| `/children` | POST | Yes | Create child profile |
| `/children/{id}` | GET | Yes | Get child |
| `/children/{id}/progress` | GET | Yes | Child progress |
| `/children/{id}/badges` | GET | Yes | Child badges |
| `/units` | GET | Yes | List units (paginated) |
| `/units/{id}/lessons` | GET | Yes | Unit lessons |
| `/lessons/{id}` | GET | Yes | Get lesson |
| `/lessons/{id}/exercises` | GET | Yes | Lesson exercises |
| `/lessons/{id}/complete` | POST | Yes | Complete lesson |
| `/exercises/{id}` | GET | Yes | Get exercise |
| `/exercises/{id}/submit` | POST | Yes | Submit answer |
| `/badges/templates` | GET | Yes | Badge templates |
| `/leaderboard` | GET | Yes | XP leaderboard |
| `/notifications` | GET | Yes | List notifications |
| `/notifications/{id}` | PATCH | Yes | Mark read/unread |
| `/admin/logs` | GET | Admin | Activity logs |
| `/admin/stats` | GET | Admin | Platform stats |
| `/admin/units` | POST | Admin | Create unit |
| `/admin/lessons` | POST | Admin | Create lesson |

### Pagination

All list endpoints support:
- `page` (default: 1)
- `page_size` (default: 10, max: 100)

Response format:
```json
{
  "items": [...],
  "total": 50,
  "page": 1,
  "page_size": 10,
  "total_pages": 5
}
```

---

## 5. Gamification Logic

### 5.1 XP Calculation

```python
XP = BASE_XP + (difficulty - 1) × DIFFICULTY_BONUS

Where:
  BASE_XP = 100
  DIFFICULTY_BONUS = 20

Examples:
  Difficulty 1 → 100 XP
  Difficulty 2 → 120 XP
  Difficulty 3 → 140 XP
```

### 5.2 Level System

```python
Threshold = level² × 100

Level 1 → 2: 100 XP  (1² × 100)
Level 2 → 3: 400 XP  (2² × 100)
Level 3 → 4: 900 XP  (3² × 100)
Level 4 → 5: 1600 XP (4² × 100)
```

### 5.3 Streak Logic

```
If last_activity == today:
    streak unchanged
Elif last_activity == yesterday:
    streak += 1
Else:
    streak = 1 (reset)
```

### 5.4 Badge System

| Badge | Condition |
|-------|-----------|
| First Lesson | Complete 1 lesson |
| XP 100 | Earn 100 XP total |
| XP 500 | Earn 500 XP total |
| Streak 3 | 3-day streak |
| Streak 7 | 7-day streak |
| Lessons 10 | Complete 10 lessons |

---

## 6. Security Implementation

### 6.1 Authentication

- **JWT Access Token**: 15 minutes expiry
- **JWT Refresh Token**: 7 days expiry
- **Algorithm**: HS256
- **Password Hashing**: bcrypt with cost factor 12

### 6.2 Authorization

- **RBAC**: Parent, Child, Admin roles
- **Child Data Isolation**: `WHERE parent_id = current_user.id`
- **Admin Only**: `/admin/*` endpoints

### 6.3 Input Validation

- All inputs validated via Pydantic schemas
- SQL injection protection via SQLAlchemy parameterization
- XSS protection via output encoding

---

## 7. Async Features

### 7.1 Background Jobs (Celery)

| Task | Trigger | Description |
|------|---------|-------------|
| `evaluate_badges` | After lesson completion | Check and award badges |
| `check_stale_streaks` | Daily at 00:00 UTC | Reset broken streaks |
| `generate_weekly_reports` | Weekly (Monday 9:00) | Send progress summaries |

### 7.2 Why Celery?

- Badge evaluation can be slow (multiple checks)
- Streak evaluation must run reliably even if server restarts
- Weekly reports are time-consuming to generate
- Keeps API response times fast (< 200ms)

---

## 8. Testing

### 8.1 Test Structure

```
tests/
├── test_gamification.py    # Unit tests (10 tests)
└── test_api.py             # Integration tests (23 tests)
```

### 8.2 Unit Tests

- XP calculation for different difficulties
- Level threshold calculation
- Level-up detection
- Streak logic (first activity, continue, same day)

### 8.3 Integration Tests

- Auth flow (register, login, me)
- Child CRUD operations
- Curriculum browsing
- Lesson completion
- Exercise submission
- Badge retrieval
- Notification management
- Admin endpoints

### 8.4 Coverage

- **Line Coverage**: >60%
- **Test Count**: 33 tests
- **All tests passing**: ✅

---

## 9. DevOps

### 9.1 CI/CD Pipeline (GitHub Actions)

```yaml
Trigger: Push/PR to main/develop
Steps:
  1. Checkout code
  2. Setup Python 3.12
  3. Install dependencies
  4. Syntax check (py_compile)
  5. Run tests with coverage (≥60%)
  6. Upload coverage report
```

### 9.2 Docker Compose

```yaml
Services:
  - postgres: PostgreSQL 15
  - redis: Redis 7
```

### 9.3 Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `JWT_SECRET_KEY` | JWT signing secret |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token TTL (minutes) |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh token TTL (days) |
| `BCRYPT_ROUNDS` | Password hashing cost |
| `ENVIRONMENT` | development/staging/production |

---

## 10. Known Limitations

1. **No real database connection**: Models use SQLAlchemy but API returns mock data for demo purposes.
2. **No email service**: Notifications are stored in DB but not sent via email.
3. **No WebSocket**: Real-time notifications planned for future.
4. **No adaptive difficulty**: Exercise difficulty is static.

## 11. Future Improvements

1. **Real database integration**: Connect to PostgreSQL with migrations
2. **WebSocket notifications**: Real-time parent notifications
3. **Adaptive difficulty**: Adjust exercise difficulty based on performance
4. **Content management**: Admin dashboard for curriculum editing
5. **Caching**: Redis cache for leaderboard and curriculum map
6. **Rate limiting**: Per-user rate limits on auth endpoints
7. **Audit logging**: Immutable audit trail for all admin actions

---

## 12. Team Members

| Role | Responsibilities |
|------|-----------------|
| Team Lead | Architecture, JWT Auth, Gamification |
| Database/API | Models, API Endpoints, Schemas |
| Backend/QA | Repositories, Tests, Docker, CI/CD |

---

**End of Technical Report**
