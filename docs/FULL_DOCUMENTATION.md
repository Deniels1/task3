# Children's Literacy Learning Platform
# Полная документация проекта

**Версия**: 1.0.0  
**Дата**: 2024  
**Команда**: 3 студента  
**Статус**: ✅ Готов к защите

---

## Содержание

1. [Обзор проекта](#1-обзор-проекта)
2. [Архитектура](#2-архитектура)
3. [База данных](#3-база-данных)
4. [API Reference](#4-api-reference)
5. [Бизнес-логика](#5-бизнес-логика)
6. [Безопасность](#6-безопасность)
7. [Тестирование](#7-тестирование)
8. [DevOps](#8-devops)
9. [Установка и запуск](#9-установка-и-запуск)
10. [Команда](#10-команда)
11. [Чеклист защиты](#11-чеклист-защиты)

---

## 1. Обзор проекта

### 1.1 Описание

Backend для платформы обучения детей чтению, вдохновлённой Duolingo ABC. Платформа обучает детей чтению через фонетику, почерк, зрительные слова и словарный запас, используя геймифицированный подход с учебной программой.

### 1.2 Технологический стек

| Компонент | Технология | Почему выбрали |
|-----------|-----------|----------------|
| Backend | FastAPI | Async, автоматическая генерация Swagger, Pydantic валидация |
| Database | PostgreSQL | JSONB для упражнений, ACID транзакции, индексы |
| ORM | SQLAlchemy 2.0 | Современный async ORM, type-safe запросы |
| Auth | JWT (python-jose) | Stateless, масштабируемый |
| Background Jobs | Celery + Redis | Асинхронная обработка задач |
| Testing | pytest + httpx | Unit и integration тесты |
| CI/CD | GitHub Actions | Автоматическое тестирование на PR |

### 1.3 Прогресс

```
✅ Архитектура (100%)
✅ База данных — 11 таблиц (100%)
✅ Модели SQLAlchemy (100%)
✅ JWT Authentication (100%)
✅ API Endpoints — 22 endpoints (100%)
✅ Геймификация (100%)
✅ Тесты — 33 теста (100%)
✅ CI/CD Pipeline (100%)
✅ Docker Compose (100%)
✅ Документация (100%)
```

---

## 2. Архитектура

### 2.1 Слоистая архитектура (3 уровня)

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│              FastAPI Routes + Pydantic Schemas              │
│                                                             │
│  POST /api/v1/auth/register                                 │
│  GET  /api/v1/children                                      │
│  POST /api/v1/lessons/{id}/complete                         │
│                                                             │
│  Ответственность: HTTP запросы/ответы, валидация input      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              DOMAIN LAYER (Business Logic)                  │
│                      Services                               │
│                                                             │
│  GamificationService                                        │
│    ├── calculate_xp()                                       │
│    ├── check_level_up()                                     │
│    ├── update_streak()                                      │
│    └── process_lesson_complete()                            │
│                                                             │
│  Ответственность: бизнес-логика, расчёты, правила          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              INFRASTRUCTURE LAYER                           │
│         Repositories + PostgreSQL + Redis                   │
│                                                             │
│  BaseRepository                                             │
│    ├── get_by_id()                                          │
│    ├── create()                                             │
│    └── delete()                                             │
│                                                             │
│  Ответственность: доступ к данным, SQL запросы              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Принципы архитектуры

1. **Разделение ответственности** — каждый слой делает одно дело
2. **No fat controllers** — контроллеры не содержат бизнес-логику
3. **Dependency Injection** — сервисы и репозитории через FastAPI dependencies
4. **Async-first** — все I/O операции через async/await
5. **RBAC** — проверка ролей на уровне endpoint

### 2.3 Project Structure

```
project/
├── README.md                           # Обзор проекта
├── requirements.txt                    # Зависимости Python
├── docker-compose.yml                  # PostgreSQL + Redis
├── .env.example                        # Пример переменных окружения
│
├── app/                                # Основное приложение
│   ├── main.py                         # Точка входа FastAPI
│   ├── config.py                       # Конфигурация (pydantic-settings)
│   │
│   ├── core/                           # Ядро системы
│   │   └── security.py                 # JWT, bcrypt хэширование
│   │
│   ├── db/                             # База данных
│   │   ├── base.py                     # Base, UUIDMixin, TimestampMixin
│   │   └── __init__.py
│   │
│   ├── models/                         # SQLAlchemy модели (11 таблиц)
│   │   ├── __init__.py
│   │   ├── user.py                     # Parent, Child
│   │   ├── curriculum.py               # Unit, Lesson, Exercise
│   │   ├── progress.py                 # LessonProgress, ExerciseResult
│   │   ├── gamification.py             # Badge, BadgeTemplate
│   │   ├── notification.py             # Notification
│   │   └── admin.py                    # ActivityLog
│   │
│   ├── schemas/                        # Pydantic схемы (8 файлов)
│   │   ├── __init__.py
│   │   ├── auth.py                     # Login, Register, Token
│   │   ├── child.py                    # Child CRUD
│   │   ├── curriculum.py               # Unit, Lesson, Exercise
│   │   ├── progress.py                 # Complete lesson, Leaderboard
│   │   ├── badge.py                    # Badge, BadgeTemplate
│   │   ├── notification.py             # Notification
│   │   ├── admin.py                    # ActivityLog, Stats
│   │   └── common.py                   # Pagination
│   │
│   ├── repositories/                   # Доступ к данным
│   │   ├── __init__.py
│   │   └── base.py                     # Generic CRUD repository
│   │
│   ├── services/                       # Бизнес-логика
│   │   └── gamification_service.py     # XP, Streak, Level, Badges
│   │
│   └── api/v1/                         # API версия 1
│       ├── router.py                   # Главный роутер
│       └── endpoints/                  # Endpoint handlers
│           ├── __init__.py
│           ├── auth.py                 # 3 endpoints
│           ├── children.py             # 4 endpoints
│           ├── units.py                # 2 endpoints
│           ├── lessons.py              # 3 endpoints
│           ├── exercises.py            # 2 endpoints
│           ├── badges.py               # 2 endpoints
│           ├── leaderboard.py          # 1 endpoint
│           ├── notifications.py        # 2 endpoints
│           └── admin.py                # 4 endpoints
│
├── tests/                              # Тесты
│   ├── __init__.py
│   ├── test_gamification.py            # 10 unit тестов
│   └── test_api.py                     # 23 integration тестов
│
├── docs/                               # Документация
│   ├── PRE_DEFENCE.md                  # Pre-Defence (1)
│   ├── TECHNICAL_REPORT.md             # Технический отчёт (20 стр.)
│   └── FULL_DOCUMENTATION.md           # Этот файл
│
└── .github/workflows/                  # CI/CD
    └── ci.yml                          # GitHub Actions pipeline
```

---

## 3. База данных

### 3.1 ER-диаграмма

```
                    ┌─────────────┐
                    │   PARENT    │
                    │─────────────│
                    │ id (PK)     │
                    │ email (UQ)  │
                    │ password    │
                    │ first_name  │
                    │ last_name   │
                    │ is_admin    │
                    └──────┬──────┘
                           │ 1
                           │
                           │ N
                    ┌──────▼──────┐
                    │    CHILD    │
                    │─────────────│
                    │ id (PK)     │
                    │ parent_id   │◄────┐
                    │ name        │     │
                    │ age         │     │
                    │ xp_total    │     │
                    │ level_number│     │
                    │ streak_*    │     │
                    └──────┬──────┘     │
                           │            │
           ┌───────────────┼────────────┘
           │               │
           │ N             │ N
    ┌──────▼──────┐ ┌──────▼──────┐
    │LESSON_PROG..│ │    BADGE    │
    │─────────────│ │─────────────│
    │ id (PK)     │ │ id (PK)     │
    │ child_id(FK)│ │ child_id(FK)│
    │ lesson_id(FK)││ template_id │
    │ status      │ │ earned_at   │
    │ xp_earned   │ └─────────────┘
    └──────┬──────┘
           │ 1
           │
           │ N
    ┌──────▼──────┐
    │EXERCISE_RES.│
    │─────────────│
    │ id (PK)     │
    │ progress_id │
    │ exercise_id │
    │ correct     │
    │ time_spent  │
    └─────────────┘

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    UNIT     │────<│   LESSON    │────<│  EXERCISE   │
│─────────────│ 1:N │─────────────│ 1:N │─────────────│
│ id (PK)     │     │ id (PK)     │     │ id (PK)     │
│ title       │     │ unit_id(FK) │     │ lesson_id   │
│ description │     │ title       │     │ type        │
│ published   │     │ difficulty  │     │ content     │
└─────────────┘     │ published   │     │ difficulty  │
                    └─────────────┘     └─────────────┘

┌─────────────┐     ┌─────────────┐
│BADGE_TEMPL. │────<│   BADGE     │
│─────────────│ 1:N │─────────────│
│ id (PK)     │     │ id (PK)     │
│ name        │     │ child_id    │
│ description │     │ template_id │
│ trigger_type│     │ earned_at   │
│ conditions  │     └─────────────┘
└─────────────┘

┌─────────────┐
│ NOTIFICATION│
│─────────────│
│ id (PK)     │
│ parent_id   │
│ title       │
│ message     │
│ type        │
│ is_read     │
└─────────────┘

┌─────────────┐
│ ACTIVITY_LOG│
│─────────────│
│ id (PK)     │
│ admin_id    │
│ action      │
│ resource    │
│ before      │
│ after       │
└─────────────┘
```

### 3.2 Таблицы (11 штук)

#### parents
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX |
| password_hash | VARCHAR(255) | NOT NULL |
| first_name | VARCHAR(100) | NOT NULL |
| last_name | VARCHAR(100) | NOT NULL |
| is_active | BOOLEAN | DEFAULT true |
| is_admin | BOOLEAN | DEFAULT false |
| created_at | TIMESTAMP | DEFAULT now() |
| updated_at | TIMESTAMP | auto-update |

#### children
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| parent_id | UUID | FK → parents.id, NOT NULL, INDEX |
| name | VARCHAR(100) | NOT NULL |
| age | INTEGER | NOT NULL, INDEX |
| xp_total | INTEGER | DEFAULT 0, INDEX |
| level_number | INTEGER | DEFAULT 1 |
| streak_current | INTEGER | DEFAULT 0 |
| streak_best | INTEGER | DEFAULT 0 |
| streak_last_activity_date | VARCHAR(10) | |
| lessons_completed | INTEGER | DEFAULT 0 |
| accuracy_rate | INTEGER | DEFAULT 0 |
| last_activity_at | TIMESTAMP | INDEX |

#### units
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| title | VARCHAR(255) | NOT NULL, INDEX |
| description | TEXT | |
| order_index | INTEGER | DEFAULT 0, INDEX |
| published | BOOLEAN | DEFAULT false, INDEX |

#### lessons
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| unit_id | UUID | FK → units.id, NOT NULL, INDEX |
| title | VARCHAR(255) | NOT NULL |
| exercise_type | VARCHAR(50) | NOT NULL, INDEX |
| difficulty | INTEGER | DEFAULT 1 |
| order_index | INTEGER | DEFAULT 0, INDEX |
| published | BOOLEAN | DEFAULT false, INDEX |

#### exercises
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| lesson_id | UUID | FK → lessons.id, NOT NULL, INDEX |
| type | VARCHAR(50) | NOT NULL, INDEX |
| content | TEXT | NOT NULL (JSON) |
| difficulty | INTEGER | DEFAULT 1 |
| order_index | INTEGER | DEFAULT 0 |

#### lesson_progress
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| child_id | UUID | FK → children.id, NOT NULL, INDEX |
| lesson_id | UUID | FK → lessons.id, NOT NULL, INDEX |
| status | VARCHAR(20) | DEFAULT 'in_progress' |
| xp_earned | INTEGER | DEFAULT 0 |
| completed_at | TIMESTAMP | |

#### exercise_results
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| progress_id | UUID | FK → lesson_progress.id, NOT NULL, INDEX |
| exercise_id | UUID | FK → exercises.id, NOT NULL, INDEX |
| correct | BOOLEAN | NOT NULL |
| time_spent_seconds | INTEGER | DEFAULT 0 |
| answer_data | TEXT | (JSON) |

#### badge_templates
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| name | VARCHAR(100) | UNIQUE, NOT NULL |
| description | TEXT | NOT NULL |
| icon_url | VARCHAR(500) | |
| trigger_type | VARCHAR(50) | NOT NULL |
| trigger_conditions | TEXT | NOT NULL (JSON) |
| xp_reward | INTEGER | DEFAULT 0 |
| display_order | INTEGER | DEFAULT 0 |
| active | BOOLEAN | DEFAULT true |

#### badges
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| child_id | UUID | FK → children.id, NOT NULL, INDEX |
| badge_template_id | UUID | FK → badge_templates.id, NOT NULL, INDEX |
| earned_at | VARCHAR(10) | NOT NULL |

#### notifications
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| parent_id | UUID | FK → parents.id, NOT NULL, INDEX |
| title | VARCHAR(255) | NOT NULL |
| message | TEXT | NOT NULL |
| notification_type | VARCHAR(50) | DEFAULT 'general' |
| is_read | BOOLEAN | DEFAULT false |

#### activity_logs
| Колонка | Тип | Constraints |
|---------|-----|-------------|
| id | UUID | PK |
| admin_id | UUID | FK → parents.id, INDEX |
| action | VARCHAR(50) | NOT NULL, INDEX |
| resource_type | VARCHAR(50) | NOT NULL |
| resource_id | VARCHAR(36) | NOT NULL |
| before_snapshot | TEXT | |
| after_snapshot | TEXT | |

### 3.3 Индексы

| Таблица | Колонка | Почему |
|---------|---------|--------|
| parents | email | Уникальность, быстрый login |
| children | parent_id | Изоляция данных (WHERE parent_id = ?) |
| children | xp_total | Leaderboard сортировка |
| children | streak_last_activity_date | Проверка streak |
| lessons | unit_id | Загрузка уроков юнита |
| lessons | published | Фильтрация опубликованных |
| exercises | lesson_id | Загрузка упражнений урока |
| lesson_progress | child_id, lesson_id | Проверка прогресса |
| badges | child_id | Загрузка бейджей ребёнка |
| notifications | parent_id | Загрузка уведомлений |

---

## 4. API Reference

### 4.1 Базовый URL

```
http://localhost:8000/api/v1
```

### 4.2 Swagger UI

```
http://localhost:8000/docs
```

### 4.3 Аутентификация

Все endpoints (кроме `/auth/register` и `/auth/login`) требуют JWT токен:

```
Authorization: Bearer <access_token>
```

### 4.4 Endpoints

#### Auth

| Method | Endpoint | Auth | Описание |
|--------|----------|------|----------|
| POST | `/auth/register` | Нет | Регистрация родителя |
| POST | `/auth/login` | Нет | Вход, получение токенов |
| GET | `/auth/me` | Да | Профиль текущего пользователя |

**Request — POST /auth/register:**
```json
{
  "email": "parent@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response — 200 OK:**
```json
{
  "id": "uuid",
  "email": "parent@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe"
}
```

**Request — POST /auth/login:**
```json
{
  "email": "parent@example.com",
  "password": "password123"
}
```

**Response — 200 OK:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

#### Children

| Method | Endpoint | Auth | Описание |
|--------|----------|------|----------|
| GET | `/children` | Да | Список детей (paginated) |
| POST | `/children` | Да | Создать профиль ребёнка |
| GET | `/children/{id}` | Да | Получить ребёнка |
| GET | `/children/{id}/progress` | Да | Прогресс ребёнка |
| GET | `/children/{id}/badges` | Да | Бейджи ребёнка |

**Request — POST /children:**
```json
{
  "name": "Alice",
  "age": 6
}
```

**Response — GET /children (paginated):**
```json
{
  "items": [
    {
      "id": "child-1",
      "name": "Alice",
      "age": 6,
      "xp_total": 350,
      "level_number": 2,
      "streak_current": 5,
      "streak_best": 12,
      "lessons_completed": 8
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

---

#### Curriculum — Units

| Method | Endpoint | Auth | Описание |
|--------|----------|------|----------|
| GET | `/units` | Да | Список юнитов (paginated) |
| GET | `/units/{id}/lessons` | Да | Уроки юнита |

**Response — GET /units:**
```json
{
  "items": [
    {
      "id": "unit-1",
      "title": "Phonics Level 1",
      "description": "Learn basic letter sounds",
      "order_index": 1,
      "published": true
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

---

#### Curriculum — Lessons

| Method | Endpoint | Auth | Описание |
|--------|----------|------|----------|
| GET | `/lessons/{id}` | Да | Получить урок |
| GET | `/lessons/{id}/exercises` | Да | Упражнения урока |
| POST | `/lessons/{id}/complete` | Да | Завершить урок |

**Response — GET /lessons/{id}:**
```json
{
  "id": "lesson-1",
  "unit_id": "unit-1",
  "title": "Letter A",
  "exercise_type": "phonics",
  "difficulty": 1,
  "order_index": 1,
  "published": true
}
```

**Request — POST /lessons/{id}/complete:**
```json
{
  "child_id": "child-1",
  "lesson_id": "lesson-1",
  "correct_answers": 5,
  "total_attempts": 5
}
```

**Response — 200 OK:**
```json
{
  "xp_earned": 100,
  "total_xp": 450,
  "new_level": 2,
  "level_up": false,
  "new_streak": 6,
  "streak_updated": true,
  "badges_earned": ["first_lesson"]
}
```

---

#### Exercises

| Method | Endpoint | Auth | Описание |
|--------|----------|------|----------|
| GET | `/exercises/{id}` | Да | Получить упражнение |
| POST | `/exercises/{id}/submit` | Да | Отправить ответ |

**Response — GET /exercises/{id}:**
```json
{
  "id": "ex-1",
  "lesson_id": "lesson-1",
  "type": "match",
  "content": "{\"question\": \"Match A to /a/\"}",
  "difficulty": 1,
  "order_index": 1
}
```

**Request — POST /exercises/{id}/submit:**
```json
{
  "answer": "A"
}
```

**Response — 200 OK:**
```json
{
  "exercise_id": "ex-1",
  "correct": true,
  "xp_earned": 10,
  "feedback": "Correct!"
}
```

---

#### Badges

| Method | Endpoint | Auth | Описание |
|--------|----------|------|----------|
| GET | `/badges/templates` | Да | Шаблоны бейджей |
| GET | `/badges/children/{child_id}` | Да | Бейджи ребёнка |

**Response — GET /badges/templates:**
```json
[
  {
    "id": "bt-1",
    "name": "First Lesson",
    "description": "Complete your first lesson",
    "icon_url": null,
    "trigger_type": "milestone",
    "xp_reward": 50
  }
]
```

---

#### Leaderboard

| Method | Endpoint | Auth | Описание |
|--------|----------|------|----------|
| GET | `/leaderboard` | Да | Таблица лидеров |

**Response — 200 OK:**
```json
[
  {
    "child_id": "child-1",
    "name": "Alice",
    "xp_total": 350,
    "level_number": 2,
    "streak_current": 5,
    "rank": 1
  },
  {
    "child_id": "child-2",
    "name": "Bob",
    "xp_total": 200,
    "level_number": 1,
    "streak_current": 3,
    "rank": 2
  }
]
```

---

#### Notifications

| Method | Endpoint | Auth | Описание |
|--------|----------|------|----------|
| GET | `/notifications` | Да | Список уведомлений |
| PATCH | `/notifications/{id}` | Да | Отметить прочитанным |

**Response — GET /notifications:**
```json
[
  {
    "id": "notif-1",
    "title": "Milestone!",
    "message": "Alice completed her first lesson!",
    "notification_type": "milestone",
    "is_read": false,
    "created_at": "2024-01-15T10:00:00"
  }
]
```

---

#### Admin

| Method | Endpoint | Auth | Описание |
|--------|----------|------|----------|
| GET | `/admin/logs` | Admin | Логи активности |
| GET | `/admin/stats` | Admin | Статистика платформы |
| POST | `/admin/units` | Admin | Создать юнит |
| POST | `/admin/lessons` | Admin | Создать урок |

**Response — GET /admin/stats:**
```json
{
  "total_parents": 150,
  "total_children": 230,
  "total_lessons_completed": 1200,
  "total_exercises_completed": 8500,
  "average_accuracy": 78.5,
  "active_streaks": 45
}
```

---

## 5. Бизнес-логика

### 5.1 XP Calculation

```python
def calculate_xp(self, lesson_difficulty: int) -> int:
    BASE_XP = 100
    DIFFICULTY_BONUS = 20
    return BASE_XP + (lesson_difficulty - 1) * DIFFICULTY_BONUS
```

**Примеры:**
| Сложность | XP |
|-----------|-----|
| 1 | 100 |
| 2 | 120 |
| 3 | 140 |
| 4 | 160 |
| 5 | 180 |

### 5.2 Level System

```python
def get_level_threshold(self, level: int) -> int:
    return level * level * 100

def check_level_up(self, current_level: int, current_xp: int, xp_to_add: int) -> Tuple[int, bool]:
    total_xp = current_xp + xp_to_add
    threshold = self.get_level_threshold(current_level + 1)
    
    if total_xp >= threshold:
        return current_level + 1, True  # Level up!
    return current_level, False  # No change
```

**Таблица уровней:**
| Уровень | Порог XP | Всего XP |
|---------|----------|----------|
| 1 → 2 | 400 | 400 |
| 2 → 3 | 900 | 1300 |
| 3 → 4 | 1600 | 2900 |
| 4 → 5 | 2500 | 5400 |
| 5 → 6 | 3600 | 9000 |

### 5.3 Streak Logic

```python
def update_streak(self, child: Child) -> Tuple[int, bool]:
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    
    # Already active today
    if child.streak_last_activity_date == today:
        return child.streak_current, False
    
    # Active yesterday - continue streak
    if child.streak_last_activity_date == yesterday:
        new_streak = child.streak_current + 1
        return new_streak, True
    
    # First time or streak broken
    return 1, True
```

**Правила:**
- Активность сегодня → streak без изменений
- Активность вчера → streak + 1
- Пропуск дня → streak = 1 (сброс)

**Пример:**
```
День 1: streak = 1
День 2: streak = 2 (вчера был)
День 3: streak = 3 (вчера был)
День 4: пропустил
День 5: streak = 1 (сброс)
```

### 5.4 Badge System

**Типы бейджей:**

| Бейдж | Условие | XP Reward |
|-------|---------|-----------|
| First Lesson | lessons_completed >= 1 | 50 |
| XP 100 | xp_total >= 100 | 0 |
| XP 500 | xp_total >= 500 | 0 |
| Streak 3 | streak_current >= 3 | 50 |
| Streak 7 | streak_current >= 7 | 100 |
| Lessons 10 | lessons_completed >= 10 | 100 |

**Проверка условий:**
```python
BADGES = {
    "first_lesson": lambda child: child.lessons_completed >= 1,
    "xp_100": lambda child: child.xp_total >= 100,
    "xp_500": lambda child: child.xp_total >= 500,
    "streak_3": lambda child: child.streak_current >= 3,
    "streak_7": lambda child: child.streak_current >= 7,
    "lessons_10": lambda child: child.lessons_completed >= 10,
}
```

### 5.5 Lesson Completion Flow

```
1. Child completes all exercises in lesson
2. POST /lessons/{id}/complete
3. Backend:
   a. Calculate XP (based on difficulty)
   b. Add XP to child.xp_total
   c. Check level up
   d. Update streak
   e. Check badges
   f. Create notification for parent
4. Return result with XP, level, streak, badges
```

---

## 6. Безопасность

### 6.1 Аутентификация (JWT)

**Access Token:**
- TTL: 15 минут
- Payload: `{sub, email, role, exp, type: "access"}`
- Алгоритм: HS256

**Refresh Token:**
- TTL: 7 дней
- Payload: `{sub, email, exp, type: "refresh"}`

### 6.2 Хэширование паролей

```python
import bcrypt

# Хэширование
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Проверка
bcrypt.checkpw(password.encode(), password_hash)
```

- Алгоритм: bcrypt
- Cost factor: 12 (рекомендуется >= 10)
- Никогда не храним в открытом виде!

### 6.3 RBAC (Role-Based Access Control)

| Роль | Доступ |
|------|--------|
| Anonymous | Только /auth/register, /auth/login |
| Parent | Свои дети, свои уведомления, curriculum |
| Admin | Всё + /admin/* endpoints |

### 6.4 Изоляция данных детей

```python
# Каждый запрос к child проверяет владельца
WHERE parent_id = current_user.id

# Parent может видеть только своих детей
# Admin может видеть всех
```

### 6.5 Валидация входных данных

- Все inputs проходят через Pydantic schemas
- SQL injection защита через SQLAlchemy параметризацию
- XSS защита через output encoding

---

## 7. Тестирование

### 7.1 Структура тестов

```
tests/
├── test_gamification.py     # 10 unit тестов
└── test_api.py              # 23 integration тестов
```

### 7.2 Unit Tests (Gamification)

| Тест | Что проверяет |
|------|---------------|
| test_xp_difficulty_1 | XP за сложность 1 = 100 |
| test_xp_difficulty_2 | XP за сложность 2 = 120 |
| test_xp_difficulty_3 | XP за сложность 3 = 140 |
| test_level_1_to_2 | Порог 2 уровня = 400 |
| test_level_2_to_3 | Порог 3 уровня = 900 |
| test_no_level_up | Не повышаем уровень без XP |
| test_level_up | Повышаем уровень при достижении порога |
| test_first_activity | Первая активность = streak 1 |
| test_continue_streak | Продолжение streak |
| test_same_day | Активность сегодня = без изменений |

### 7.3 Integration Tests (API)

| Класс | Тесты | Endpoint |
|-------|-------|----------|
| TestAuthEndpoints | 3 | /auth/* |
| TestChildrenEndpoints | 4 | /children/* |
| TestCurriculumEndpoints | 4 | /units/*, /lessons/* |
| TestGamificationEndpoints | 4 | /lessons/*/complete, /leaderboard, /badges |
| TestExerciseEndpoints | 2 | /exercises/* |
| TestNotificationEndpoints | 2 | /notifications/* |
| TestAdminEndpoints | 2 | /admin/* |
| TestHealthEndpoint | 2 | /health, / |

### 7.4 Запуск тестов

```bash
# Все тесты
python -m pytest tests/ -v

# С покрытием
python -m pytest tests/ -v --cov=app --cov-report=term-missing

# Только unit
python -m pytest tests/test_gamification.py -v

# Только integration
python -m pytest tests/test_api.py -v
```

### 7.5 Результаты

```
============================= 33 passed =============================
- 10 unit tests (gamification logic)
- 23 integration tests (API endpoints)
- Coverage: >60%
```

---

## 8. DevOps

### 8.1 CI/CD Pipeline (GitHub Actions)

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: python -m py_compile app/main.py
      - run: pytest tests/ -v --cov=app --cov-fail-under=60
```

### 8.2 Docker Compose

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: literacy_user
      POSTGRES_PASSWORD: literacy_pass
      POSTGRES_DB: literacy_db
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### 8.3 Environment Variables

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| DATABASE_URL | PostgreSQL connection string | Да |
| REDIS_URL | Redis connection string | Да |
| JWT_SECRET_KEY | JWT signing secret | Да |
| JWT_ACCESS_TOKEN_EXPIRES | Access token TTL (мин) | Нет (default: 15) |
| JWT_REFRESH_TOKEN_EXPIRES | Refresh token TTL (дни) | Нет (default: 7) |
| BCRYPT_ROUNDS | bcrypt cost factor | Нет (default: 12) |
| ENVIRONMENT | development/staging/production | Нет (default: development) |

---

## 9. Установка и запуск

### 9.1 Требования

- Python 3.11+
- PostgreSQL 15+ (опционально для demo)
- Redis 7+ (опционально для demo)

### 9.2 Установка

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd childrens-literacy-platform

# 2. Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить переменные окружения
cp .env.example .env
# Редактировать .env

# 5. Запустить (опционально)
docker-compose up -d
```

### 9.3 Запуск приложения

```bash
# Разработка (с авто-перезагрузкой)
python -m uvicorn app.main:app --reload

# Продакшн
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 9.4 Проверка

```
Swagger UI: http://localhost:8000/docs
Health:     http://localhost:8000/health
```

### 9.5 Запуск тестов

```bash
python -m pytest tests/ -v
```

---

## 10. Команда

| Студент | Роль | Зоны ответственности |
|---------|------|---------------------|
| 1 | Team Lead | Архитектура, JWT Auth, Gamification algorithms |
| 2 | Database/API | ERD, Models, API Endpoints, Pydantic Schemas |
| 3 | Backend/QA | Repositories, Tests, Docker, CI/CD |

---

## 11. Чеклист защиты

### 11.1 Перед защитой

```
[ ] Swagger открывается на localhost:8000/docs
[ ] Все 33 теста проходят: python -m pytest tests/ -v
[ ] Demo flow отработан 3 раза
[ ] Каждый член команды знает свои формулы
[ ] ERD нарисована/распечатана
[ ] Technical Report распечатан
[ ] Полная документация готова
```

### 11.2 Demo Flow (7 минут)

```
0:00 — Открыть Swagger (/docs)
0:30 — POST /auth/register (родитель)
1:00 — POST /auth/login (токены)
1:30 — POST /children (создать ребёнка)
2:00 — GET /units (учебный план)
2:30 — POST /lessons/{id}/complete (XP + streak)
3:30 — GET /children/{id}/badges (бейдж)
4:00 — GET /notifications (уведомление)
4:30 — GET /leaderboard (таблица лидеров)
5:00 — Показать код: gamification_service.py
5:30 — Показать тесты: pytest tests/ -v
6:00 — Показать CI: .github/workflows/ci.yml
6:30 — Заключение
```

### 11.3 Топ-10 вопросов

| # | Вопрос | Ответ (кратко) |
|---|--------|----------------|
| 1 | Архитектура? | 3 слоя: Routes → Services → Repositories |
| 2 | XP формула? | 100 + (difficulty-1)×20 |
| 3 | Level формула? | level² × 100 |
| 4 | Streak логика? | yesterday→+1, today→no change, older→reset |
| 5 | Защита детей? | WHERE parent_id = current_user.id |
| 6 | Почему PostgreSQL? | JSONB для exercises, ACID, индексы |
| 7 | JWT? | Access 15min + Refresh 7days, HS256 |
| 8 | bcrypt? | Cost factor 12, никогда не plaintext |
| 9 | Тесты? | 33 теста: 10 unit + 23 integration |
| 10 | CI/CD? | GitHub Actions: lint → test → coverage |

### 11.4 Распределение на защите

| Время | Кто | Что |
|-------|-----|-----|
| 0:00-1:00 | Все | Приветствие, обзор проекта |
| 1:00-3:00 | Студент 1 | Demo: Swagger → register → login → complete lesson |
| 3:00-4:00 | Студент 1 | Gamification: формулы XP, Level, Streak |
| 4:00-5:00 | Студент 2 | Database: ERD, модели, связи |
| 5:00-6:00 | Студент 2 | API: 22 endpoints, REST, Swagger |
| 6:00-7:00 | Студент 3 | Security: JWT, bcrypt, RBAC |
| 7:00-8:00 | Студент 3 | Tests + DevOps: 33 теста, CI/CD, Docker |
| 8:00-20:00 | Все | Q&A |

---

## 12. Самооценка по Rubric

| Категория | Макс | Наша оценка | Комментарий |
|-----------|------|-------------|-------------|
| Functionality | 25 | 23 | Все фичи работают, demo готов |
| Architecture | 20 | 19 | 3-layer, чистый код |
| Database Design | 10 | 9 | 11 таблиц, нормализована |
| API Design | 10 | 9 | 22 endpoints, REST, Swagger |
| Security | 10 | 9 | JWT, bcrypt, RBAC, изоляция |
| Testing | 10 | 9 | 33 теста, coverage >60% |
| DevOps | 5 | 4 | CI + Docker |
| Defence | 10 | ? | Зависит от выступления |
| **ИТОГО** | **100** | **~82** | **+3 бонус Docker** |

---

**Документация завершена. Проект готов к защите! ✅**
