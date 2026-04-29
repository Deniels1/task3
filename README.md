# Children's Literacy Platform
## Pre-Defence (1) ✅

**Команда**: 3 человека  
**Прогресс**: 40%+
**Статус**: ✅ ВСЕ ФАЙЛЫ РАБОТАЮТ

---

## 1. TOKEN TASK

```
EPIC 1: Foundation (20%)
  - Database design ✅
  - Models (Parent, Child, Lesson) ✅
  - Authentication (JWT) ✅

EPIC 2: Core Features (40%)
  - Child profile management ✅
  - Lesson completion ✅
  - XP & Streak calculation ✅

EPIC 3: Gamification (20%)
  - Badge system 🔄
  - Level-up logic ✅

EPIC 4: Async & Testing (20%)
  - Background jobs (Celery) ⏳
  - Tests ⏳
  - Docker ⏳
```

**Прогресс**: 40%+ 

---

## 2. ARCHITECTURE DESIGN

### 3-Layer Architecture

```
┌─────────────────────────────┐
│  Routes (FastAPI)           │  ← HTTP requests
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Services (Business Logic)  │  ← XP, Streak, Level
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Repositories + Database    │  ← PostgreSQL
└─────────────────────────────┘
```

**Почему так?**
- Разделение ответственности
- Легко тестировать
- Стандарт индустрии

### ER-Diagram

```
PARENT (1) ────────< CHILD (N)
                        │
                        ├────< LESSON_PROGRESS
                        │
                        └────< BADGE

UNIT (1) ────────< LESSON (N) ────────< EXERCISE (N)
```

### Tech Stack

| Компонент | Технология |
|-----------|------------|
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT |
| Background | Celery + Redis |

---

## 3. PROGRAM LOGIC

### 3.1 XP Calculation

```python
# Формула: 100 + (difficulty - 1) × 20
def calculate_xp(difficulty: int) -> int:
    return 100 + (difficulty - 1) * 20

# Пример: Урок сложности 3 = 100 + 40 = 140 XP
```

### 3.2 Level System

```python
# Формула: level² × 100
def get_threshold(level: int) -> int:
    return level * level * 100

# 1→2: 100 XP
# 2→3: 400 XP
# 3→4: 900 XP
```

### 3.3 Streak Logic

```python
# yesterday → +1
# today → no change
# older → reset to 1

def update_streak(last_activity, streak):
    if last_activity == today:
        return streak
    elif last_activity == yesterday:
        return streak + 1
    else:
        return 1
```

### 3.4 Badges

```python
BADGES = {
    "first_lesson": lessons >= 1,
    "xp_100": xp >= 100,
    "streak_3": streak >= 3,
    "streak_7": streak >= 7,
    "lessons_10": lessons >= 10,
}
```

---

## 4. SECURITY

**JWT**: Access (15 min) + Refresh (7 days)  
**Passwords**: bcrypt (cost=12)  
**Child Isolation**: `WHERE parent_id = current_user.id`

---

## 5. PROJECT STRUCTURE

```
project/
├── README.md              # Этот файл
├── app/
│   ├── main.py            # FastAPI app ✅
│   ├── config.py          # Settings ✅
│   ├── core/security.py   # JWT, bcrypt ✅
│   ├── db/
│   │   └── base.py        # Base models ✅
│   ├── models/
│   │   ├── user.py        # Parent, Child ✅
│   │   └── curriculum.py  # Unit, Lesson, Exercise ✅
│   └── services/
│       └── gamification_service.py  # XP, Streak, Level ✅
```

---

## 6. TEAM (3 persons)

| Student | Role | Tasks |
|---------|------|-------|
| 1 | Team Lead | Architecture, Gamification |
| 2 | Database/API | Models, API |
| 3 | Backend/QA | Repositories, Tests |

---

## 7. Q&A

| Вопрос | Ответ |
|--------|-------|
| Архитектура? | 3 слоя: Routes → Services → Repositories |
| XP формула? | 100 + (difficulty-1)×20 |
| Level формула? | level² × 100 |
| Streak? | yesterday→+1, older→reset |
| Защита детей? | WHERE parent_id = user.id |

---

## 8. VERIFICATION ✅

```bash
# Все файлы компилируются
python -m py_compile app/main.py
python -m py_compile app/services/gamification_service.py

# Все импорты работают
python -c "from app.main import app; print('OK')"

# Запуск приложения
uvicorn app.main:app --reload
python -m uvicorn app.main:app --reload

# Swagger UI
http://localhost:8000/docs
```

---

**Pre-Defence (1) Ready! ✅**

python -m uvicorn --version