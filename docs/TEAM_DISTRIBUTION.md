# Распределение проекта на 3 человека
## Children's Literacy Learning Platform

**Цель**: Каждый студент знает СВОИ файлы, СВОИ формулы, СВОЮ зону ответственности. На защите каждый отвечает только за свою часть.

---

## 👥 Общее распределение

| Студент | Роль | Файлы | Зона ответственности | Время на защите |
|---------|------|-------|---------------------|-----------------|
| **#1** | Team Lead / Architect | `main.py`, `config.py`, `core/security.py`, `services/gamification_service.py`, `models/user.py`, `schemas/auth.py`, `schemas/child.py`, `schemas/progress.py`, `api/v1/endpoints/auth.py`, `api/v1/endpoints/children.py`, `api/v1/endpoints/leaderboard.py` | Архитектура, JWT Auth, Gamification (XP/Level/Streak), Child profiles, Demo flow | 6 минут |
| **#2** | Database / API Designer | `db/base.py`, `models/curriculum.py`, `models/progress.py`, `models/gamification.py`, `models/notification.py`, `models/admin.py`, `schemas/curriculum.py`, `schemas/badge.py`, `schemas/notification.py`, `schemas/admin.py`, `schemas/common.py`, `api/v1/endpoints/units.py`, `api/v1/endpoints/lessons.py`, `api/v1/endpoints/exercises.py`, `api/v1/endpoints/badges.py`, `api/v1/endpoints/notifications.py`, `api/v1/endpoints/admin.py`, `api/v1/router.py` | ERD, 11 таблиц БД, Curriculum API, Admin API, Pagination, Swagger | 6 минут |
| **#3** | Backend / QA / DevOps | `repositories/base.py`, `tests/test_gamification.py`, `tests/test_api.py`, `docker-compose.yml`, `.github/workflows/ci.yml`, `.env.example`, `requirements.txt`, `docs/*.md` | Repositories, 33 теста, Docker, CI/CD, Документация | 6 минут |

---

## Студент #1 — Team Lead / Architect

### 📁 Его файлы (11 штук)

```
app/
├── main.py                           ← Точка входа FastAPI
├── config.py                         ← Настройки приложения
├── core/
│   └── security.py                   ← JWT + bcrypt
├── services/
│   └── gamification_service.py       ← XP, Level, Streak, Badges
├── models/
│   └── user.py                       ← Parent, Child
├── schemas/
│   ├── auth.py                       ← Login, Register, Token
│   ├── child.py                      ← Child CRUD
│   └── progress.py                   ← Complete lesson, Leaderboard
└── api/v1/endpoints/
    ├── auth.py                       ← 3 endpoints
    ├── children.py                   ← 4 endpoints
    └── leaderboard.py                ← 1 endpoint
```

---

### 🔐 app/core/security.py — JWT + bcrypt

**Зачем нужен**: Безопасность. Любое приложение с пользователями ДОЛЖНО иметь аутентификацию и хэширование паролей.

**Что работает**:

```python
import bcrypt
from jose import jwt
from datetime import datetime, timedelta

# 1. Хэширование пароля
# Почему bcrypt? Потому что это стандарт де-факто для Python.
# Почему rounds=12? Чем больше rounds, тем медленнее подбор.
# 12 — баланс между безопасностью и скоростью.
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# 2. Проверка пароля
# Почему checkpw? bcrypt сам сравнивает с salt, ничего не храним отдельно.
def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash)

# 3. Создание JWT токена
# Почему JWT? Stateless — сервер не хранит сессии, масштабируется.
# Почему HS256? Достаточно для студенческого проекта, простой ключ.
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

**На защите сказать**:
> "Мы используем JWT для stateless аутентификации. Access token живёт 15 минут, refresh — 7 дней. Пароли хэшируем bcrypt с cost factor 12. Это industry standard."

---

### 🎮 app/services/gamification_service.py — СЕРДЦЕ проекта

**Зачем нужен**: Вся бизнес-логика геймификации. Без этого файла проект превращается в обычный CRUD.

**Что работает и почему**:

#### Формула XP

```python
def calculate_xp(self, lesson_difficulty: int) -> int:
    BASE_XP = 100
    DIFFICULTY_BONUS = 20
    return BASE_XP + (lesson_difficulty - 1) * DIFFICULTY_BONUS
```

**Почему именно такая формула**:
- `BASE_XP = 100` — ребёнок ВСЕГДА получает награду, даже за простой урок. Психология: positive reinforcement.
- `DIFFICULTY_BONUS = 20` — небольшой бонус за сложность. Не 50, чтобы не было огромного разрыва между уровнями. Не 10, чтобы было заметно.
- `(difficulty - 1)` — за сложность 1 бонуса нет. Зачем? Чтобы первый урок был доступен всем.

**Примеры**:
| Сложность | XP | Почему |
|-----------|-----|--------|
| 1 | 100 | Базовая награда |
| 2 | 120 | +20 за чуть сложнее |
| 3 | 140 | +40 за средний |
| 5 | 180 | +80 за сложный |

**На защите сказать**:
> "Формула линейная: 100 + (difficulty-1)×20. Мы выбрали линейную, а не экспоненциальную, потому что дети должны ВИДЕТЬ прогресс. Если XP растёт слишком быстро — ребёнок запутается."

---

#### Формула Level

```python
def get_level_threshold(self, level: int) -> int:
    return level * level * 100  # level² × 100
```

**Почему именно квадратичная**:
- `level²` — прогресс замедляется. Уровень 1→2 легко, 10→11 очень сложно.
- `× 100` — масштабируем с BASE_XP. 100 XP = 1 урок сложности 1.
- Почему не `2^level`? Было бы СЛИШКОМ медленно. Ребёнок уйдёт.
- Почему не `level × 100`? Было бы линейно, неинтересно.

**Таблица уровней**:
| Уровень | Порог XP | Всего XP | Уроков (diff=1) |
|---------|----------|----------|-----------------|
| 1→2 | 400 | 400 | 4 |
| 2→3 | 900 | 1300 | 9 |
| 3→4 | 1600 | 2900 | 16 |
| 4→5 | 2500 | 5400 | 25 |

**На защите сказать**:
> "Квадратичная прогрессия: level² × 100. Ребёнок быстро достигает уровня 3-4 (мотивация), но дальше нужно больше усилий (вовлечённость)."

---

#### Логика Streak

```python
def update_streak(self, child: Child) -> Tuple[int, bool]:
    today = date.today().isoformat()      # "2024-01-15"
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    
    if child.streak_last_activity_date == today:
        return child.streak_current, False  # Уже сегодня активен
    
    if child.streak_last_activity_date == yesterday:
        return child.streak_current + 1, True  # Продолжаем streak
    
    return 1, True  # Сброс, начинаем заново
```

**Почему именно такая логика**:
- `today` → no change: ребёнок может завершить 5 уроков за день, streak не должен расти на 5.
- `yesterday` → +1: классическая streak механика (Duolingo, GitHub).
- `older` → 1: если пропустил день — сброс. Это создаёт FOMO (fear of missing out), мотивирует возвращаться.

**На защите сказать**:
> "Streak механика как в Duolingo: вчера → +1, сегодня → без изменений, пропуск → сброс. Это создаёт привычку ежедневных занятий."

---

#### Полный flow завершения урока

```python
async def process_lesson_complete(self, child: Child, lesson: Lesson, result: LessonCompleteRequest):
    # 1. Сколько XP за урок
    xp_earned = self.calculate_xp(lesson.difficulty)
    
    # 2. Обновляем streak
    new_streak, streak_updated = self.update_streak(child)
    
    # 3. Проверяем level up
    new_level, level_up = self.check_level_up(child.level_number, child.xp_total, xp_earned)
    
    # 4. Проверяем бейджи
    badges_earned = self.evaluate_badges(child)
    
    return {
        "xp_earned": xp_earned,
        "total_xp": child.xp_total + xp_earned,
        "new_level": new_level,
        "level_up": level_up,
        "new_streak": new_streak,
        "streak_updated": streak_updated,
        "badges_earned": badges_earned
    }
```

**Почему именно такой порядок**:
1. Сначала XP — это база для всего остального.
2. Потом streak — зависит только от даты, не от XP.
3. Потом level up — зависит от нового total XP.
4. Потом badges — зависят от ВСЕХ предыдущих значений.

---

### 👨‍👩‍👧 app/models/user.py — Parent + Child

**Зачем нужен**: Хранение пользователей. Без этого нет авторизации, нет профилей детей.

**Почему Parent отдельно от Child**:
- Родитель регистрируется (email, password).
- Ребёнок — это ПРОФИЛЬ, не отдельный пользователь. У ребёнка нет пароля.
- Один родитель → много детей (1:N).

```python
class Parent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "parents"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # RBAC: admin flag
    
    children = relationship("Child", back_populates="parent")

class Child(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "children"
    
    parent_id = Column(UUID(as_uuid=True), ForeignKey("parents.id"), index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False, index=True)
    xp_total = Column(Integer, default=0, index=True)  # Индекс для leaderboard!
    level_number = Column(Integer, default=1)
    streak_current = Column(Integer, default=0)
    streak_best = Column(Integer, default=0)
    streak_last_activity_date = Column(String(10))
    lessons_completed = Column(Integer, default=0)
    
    parent = relationship("Parent", back_populates="children")
```

**Почему `is_admin` в Parent**:
- Админ — это тоже родитель, но с расширенными правами.
- Не делаем отдельную таблицу Admin — избыточно.
- Проверка: `if current_user.is_admin: ...`

**Почему `xp_total` с индексом**:
- Leaderboard сортирует по `xp_total DESC`. Без индекса — полный scan таблицы.
- С индексом — O(log n) вместо O(n).

---

### 🔑 app/api/v1/endpoints/auth.py — 3 endpoints

```python
@router.post("/register")
async def register_parent(data: ParentRegister):
    # Почему хэшируем здесь? Чтобы в БД не попал plaintext.
    password_hash = hash_password(data.password)
    # Создаём Parent...

@router.post("/login")
async def login(data: LoginRequest):
    # Проверяем bcrypt
    if not verify_password(data.password, parent.password_hash):
        raise HTTPException(401, "Invalid credentials")
    # Выдаём токены
    access_token = create_access_token({"sub": str(parent.id), "email": parent.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_me(current_user: Parent = Depends(get_current_user)):
    # Depends — dependency injection FastAPI.
    # Автоматически проверяет JWT из Authorization: Bearer header.
    return current_user
```

**Почему Depends**: FastAPI сам извлекает токен из заголовка, декодирует JWT, находит пользователя. Мы не пишем это руками.

---

### 👶 app/api/v1/endpoints/children.py — 4 endpoints

**Зачем**: CRUD для детей + прогресс + бейджи.

```python
@router.get("")
async def get_children(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    # Pagination через Query параметры.
    # ge=1 — page не может быть 0 или отрицательным.
    # le=100 — защита от DDoS (не запросят page_size=1000000).
    return paginate(items, total, page, page_size)
```

**Почему пагинация**: Без неё при 10000 детях API вернёт гигантский JSON и упадёт по памяти.

---

### 📊 app/api/v1/endpoints/leaderboard.py

```python
@router.get("")
async def get_leaderboard(limit: int = Query(10, ge=1, le=100)):
    # Сортировка по xp_total DESC.
    # LIMIT защищает от перегрузки.
    return [
        {"child_id": "1", "name": "Alice", "xp_total": 350, "rank": 1},
        {"child_id": "2", "name": "Bob", "xp_total": 200, "rank": 2},
    ]
```

**Почему DESC**: Топ — это максимум XP, не минимум.

---

## Студент #2 — Database / API Designer

### 📁 Его файлы (17 штук)

```
app/
├── db/
│   └── base.py                       ← Base, UUIDMixin, TimestampMixin
├── models/
│   ├── curriculum.py                 ← Unit, Lesson, Exercise
│   ├── progress.py                   ← LessonProgress, ExerciseResult
│   ├── gamification.py               ← Badge, BadgeTemplate
│   ├── notification.py               ← Notification
│   └── admin.py                      ← ActivityLog
├── schemas/
│   ├── curriculum.py                 ← Unit, Lesson, Exercise schemas
│   ├── badge.py                      ← Badge, BadgeTemplate schemas
│   ├── notification.py               ← Notification schemas
│   ├── admin.py                      ← ActivityLog, Stats schemas
│   └── common.py                     ← Pagination
└── api/v1/endpoints/
    ├── units.py                      ← 2 endpoints
    ├── lessons.py                    ← 3 endpoints
    ├── exercises.py                  ← 2 endpoints
    ├── badges.py                     ← 2 endpoints
    ├── notifications.py              ← 2 endpoints
    ├── admin.py                      ← 4 endpoints
    └── router.py                     ← Главный роутер
```

---

### 🗄️ app/db/base.py — Базовые классы

**Зачем нужен**: Все модели наследуются отсюда. DRY (Don't Repeat Yourself).

```python
class Base(DeclarativeBase):
    pass

class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4  # Автогенерация UUID4
    )

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow  # Автоматически при создании
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow  # Автоматически при обновлении
    )
```

**Почему UUID, не int auto-increment**:
- UUID нельзя угадать. `id=1`, `id=2` — предсказуемо. UUID — случайный.
- Можно генерировать на клиенте до отправки на сервер.
- Нет конфликтов при репликации БД.

**Почему TimestampMixin**:
- Каждая таблица ДОЛЖНА знать, когда создана запись. Для аудита, для отладки, для аналитики.
- Не пишем `created_at` в каждой модели — наследуем.

---

### 📚 app/models/curriculum.py — Unit, Lesson, Exercise

**Зачем нужен**: Учебный план. Без этого нет структуры обучения.

```python
class Unit(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "units"
    
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    order_index = Column(Integer, default=0, index=True)  # Порядок: 1, 2, 3...
    published = Column(Boolean, default=False, index=True)  # Черновик / Опубликовано
    
    lessons = relationship("Lesson", back_populates="unit")
```

**Почему `order_index`**:
- Уроки должны идти в определённом порядке (фонетика → слова → предложения).
- Нельзя полагаться на `created_at` — админ может создать урок 5 раньше урока 3.

**Почему `published`**:
- Админ создаёт урок в черновике, проверяет, потом публикует.
- Дети видят ТОЛЬКО `published=True`.

```python
class Lesson(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "lessons"
    
    unit_id = Column(UUID, ForeignKey("units.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    exercise_type = Column(String(50), nullable=False, index=True)
    # phonics, sight_words, handwriting, vocabulary, comprehension
    difficulty = Column(Integer, default=1)  # 1-5
    order_index = Column(Integer, default=0, index=True)
    published = Column(Boolean, default=False, index=True)
    
    unit = relationship("Unit", back_populates="lessons")
    exercises = relationship("Exercise", back_populates="lesson")
```

**Почему `exercise_type` с index**:
- Фильтрация по типу: "покажи все уроки фонетики".
- Без индекса — полный scan.

```python
class Exercise(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "exercises"
    
    lesson_id = Column(UUID, ForeignKey("lessons.id"), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    # match, trace, select, type, listen, speak
    content = Column(Text, nullable=False)  # JSON строка
    difficulty = Column(Integer, default=1)
    order_index = Column(Integer, default=0)
    
    lesson = relationship("Lesson", back_populates="exercises")
```

**Почему `content` — Text, не JSONB**:
- Для demo используем Text с JSON строкой. В production — JSONB (PostgreSQL) для индексации и валидации.
- Разные типы упражнений имеют РАЗНУЮ структуру JSON. JSONB позволяет хранить любую структуру.

**Пример content**:
```json
// match exercise
{"question": "Match A to /a/", "options": ["A", "B", "C"], "correct": "A"}

// trace exercise
{"letter": "A", "trace_path": "M 10 80 L 40 10 L 70 80"}
```

---

### 📊 app/models/progress.py — LessonProgress + ExerciseResult

**Зачем нужен**: Отслеживание прогресса. Без этого не знаем, что ребёнок прошёл.

```python
class LessonProgress(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "lesson_progress"
    
    child_id = Column(UUID, ForeignKey("children.id"), nullable=False, index=True)
    lesson_id = Column(UUID, ForeignKey("lessons.id"), nullable=False, index=True)
    status = Column(String(20), default="in_progress")  # in_progress | completed
    xp_earned = Column(Integer, default=0)
    completed_at = Column(DateTime)
    
    # Уникальность: один ребёнок — один прогресс на урок
    __table_args__ = (
        UniqueConstraint("child_id", "lesson_id", name="uix_child_lesson"),
    )
```

**Почему `UniqueConstraint(child_id, lesson_id)`**:
- Ребёнок не может иметь ДВА прогресса на один урок.
- Без этого — дублирование данных, некорректная статистика.

```python
class ExerciseResult(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "exercise_results"
    
    progress_id = Column(UUID, ForeignKey("lesson_progress.id"), nullable=False, index=True)
    exercise_id = Column(UUID, ForeignKey("exercises.id"), nullable=False, index=True)
    correct = Column(Boolean, nullable=False)
    time_spent_seconds = Column(Integer, default=0)
    answer_data = Column(Text)  # Что именно ответил ребёнок
```

**Почему `answer_data`**:
- Храним НЕ только correct/incorrect, но и сам ответ.
- Для аналитики: "ребёнок часто путает B и D".

---

### 🏅 app/models/gamification.py — Badge + BadgeTemplate

**Зачем**: Система достижений. Мотивирует детей учиться.

```python
class BadgeTemplate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "badge_templates"
    
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    icon_url = Column(String(500))
    trigger_type = Column(String(50), nullable=False)  # milestone | streak | xp
    trigger_conditions = Column(Text, nullable=False)  # JSON: {"min_lessons": 1}
    xp_reward = Column(Integer, default=0)
    display_order = Column(Integer, default=0)
    active = Column(Boolean, default=True)

class Badge(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "badges"
    
    child_id = Column(UUID, ForeignKey("children.id"), nullable=False, index=True)
    badge_template_id = Column(UUID, ForeignKey("badge_templates.id"), nullable=False, index=True)
    earned_at = Column(String(10), nullable=False)  # "2024-01-15"
```

**Почему BadgeTemplate отдельно от Badge**:
- Template = "определение" бейджа (название, условия).
- Badge = "экземпляр" (какой ребёнок получил, когда).
- Один template → много badges (1:N).

**Почему `trigger_conditions` — JSON**:
- Условия разные: `{"min_lessons": 10}` или `{"min_streak": 7}` или `{"min_xp": 500}`.
- JSON позволяет хранить ЛЮБУЮ структуру условий.

---

### 🔔 app/models/notification.py

**Зачем**: Родители должны знать, что ребёнок делает.

```python
class Notification(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "notifications"
    
    parent_id = Column(UUID, ForeignKey("parents.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="general")  # milestone | streak | system
    is_read = Column(Boolean, default=False)
```

**Почему `is_read`**: Родитель может прочитать уведомление позже. Не удаляем — храним историю.

---

### 📋 app/models/admin.py — ActivityLog

**Зачем**: Аудит действий админа. Кто что изменил и когда.

```python
class ActivityLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "activity_logs"
    
    admin_id = Column(UUID, ForeignKey("parents.id"), index=True)
    action = Column(String(50), nullable=False, index=True)  # create | update | delete
    resource_type = Column(String(50), nullable=False)  # unit | lesson | exercise
    resource_id = Column(String(36), nullable=False)
    before_snapshot = Column(Text)  # JSON: что было ДО
    after_snapshot = Column(Text)   # JSON: что стало ПОСЛЕ
```

**Почему `before_snapshot` и `after_snapshot`**:
- Админ случайно удалил урок. Мы видим, что было до удаления.
- Админ изменил сложность. Мы видим старое и новое значение.
- Это immutable audit trail — нельзя подделать.

---

### 📄 app/schemas/common.py — Pagination

**Зачем**: Все list endpoints возвращают одинаковую структуру.

```python
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
```

**Почему Generic[T]**:
- `PaginatedResponse[UnitResponse]` — список юнитов.
- `PaginatedResponse[ChildResponse]` — список детей.
- Один класс для ВСЕХ типов. DRY.

---

### 🔌 app/api/v1/router.py — Главный роутер

```python
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(children.router)
api_router.include_router(units.router)
# ... все endpoints
```

**Почему prefix="/api/v1"**:
- Версионирование API. Когда выйдет v2 — добавим `/api/v2`.
- Старые клиенты продолжат работать с `/api/v1`.

---

### 📚 app/api/v1/endpoints/units.py

```python
@router.get("", response_model=PaginatedResponse[UnitResponse])
async def get_units(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    # response_model=PaginatedResponse — FastAPI сам валидирует ответ.
    # Query(ge=1) — page не может быть 0 или отрицательным.
    # le=100 — защита от слишком большого запроса.
```

---

### 📖 app/api/v1/endpoints/lessons.py

```python
@router.post("/{lesson_id}/complete", response_model=LessonCompleteResponse)
async def complete_lesson(lesson_id: str, data: LessonCompleteRequest):
    # Вызываем gamification_service — бизнес-логика в сервисе, не здесь!
    result = await gamification_service.process_lesson_complete(child, lesson, data)
    return result
```

**Почему lesson_id в Path, а child_id в Body**:
- `lesson_id` — идентифицирует ресурс (REST convention).
- `child_id` — данные запроса (кто завершает урок).

---

### 🛠️ app/api/v1/endpoints/admin.py

```python
@router.get("/logs")
async def get_logs(current_user: Parent = Depends(get_current_admin)):
    # Depends(get_current_admin) — только админы!
    # Если обычный родитель — 403 Forbidden автоматически.
```

---

## Студент #3 — Backend / QA / DevOps

### 📁 Его файлы (9 штук)

```
app/
└── repositories/
    └── base.py                       ← Generic CRUD

tests/
├── test_gamification.py              ← 10 unit тестов
└── test_api.py                       ← 23 integration тестов

.github/workflows/
└── ci.yml                            ← CI pipeline

docker-compose.yml                    ← PostgreSQL + Redis
.env.example                          ← Переменные окружения
requirements.txt                      ← Зависимости
docs/
├── PRE_DEFENCE.md                    ← Pre-Defence док
├── TECHNICAL_REPORT.md               ← Технический отчёт
└── FULL_DOCUMENTATION.md             ← Полная документация
```

---

### 🗃️ app/repositories/base.py — Generic CRUD

**Зачем нужен**: DRY. Все репозитории делают одно и то же: create, read, update, delete.

```python
class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    
    async def get_by_id(self, db: AsyncSession, id: uuid.UUID) -> T | None:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
    
    async def create(self, db: AsyncSession, obj_in: dict) -> T:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: uuid.UUID) -> bool:
        obj = await self.get_by_id(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return True
        return False
```

**Почему Generic[T]**:
- `BaseRepository[Child]` — репозиторий для детей.
- `BaseRepository[Lesson]` — репозиторий для уроков.
- Один класс — все таблицы.

**Почему async**:
- `await db.execute(...)` — не блокируем event loop.
- Можем обрабатывать 1000 запросов одновременно.

---

### 🧪 tests/test_gamification.py — 10 unit тестов

**Зачем**: Тестируем бизнес-логику изолированно, без запуска сервера.

```python
class TestXPCalculation:
    def test_xp_difficulty_1(self):
        service = GamificationService()
        assert service.calculate_xp(1) == 100
        # Почему 100? Это BASE_XP. Ребёнок всегда получает награду.
    
    def test_xp_difficulty_2(self):
        assert service.calculate_xp(2) == 120
        # 100 + (2-1)*20 = 120. Проверяем бонус за сложность.
    
    def test_xp_difficulty_3(self):
        assert service.calculate_xp(3) == 140
        # 100 + (3-1)*20 = 140. Линейная прогрессия.
```

**Почему unit тесты**:
- Быстрые (< 1 мс каждый).
- Не требуют БД, Redis, сервера.
- Проверяем математику: формулы должны быть точными.

```python
class TestLevelUp:
    def test_no_level_up(self):
        service = GamificationService()
        new_level, level_up = service.check_level_up(1, 0, 50)
        assert new_level == 1
        assert level_up is False
        # 0 + 50 = 50. Порог для level 2 = 400. Не хватает.
    
    def test_level_up(self):
        new_level, level_up = service.check_level_up(1, 350, 100)
        assert new_level == 2
        assert level_up is True
        # 350 + 100 = 450 >= 400. Level up!
```

```python
class TestStreak:
    def test_first_activity(self):
        # streak_last_activity_date = None
        # Сегодня первый раз → streak = 1
    
    def test_continue_streak(self):
        # streak_last_activity_date = yesterday
        # Был вчера → streak + 1
    
    def test_same_day(self):
        # streak_last_activity_date = today
        # Уже сегодня активен → без изменений
```

---

### 🌐 tests/test_api.py — 23 integration тестов

**Зачем**: Тестируем endpoint'ы как "чёрный ящик". Отправляем HTTP запрос, проверяем ответ.

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAuthEndpoints:
    def test_register_parent(self):
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "Parent"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        # Почему 200, не 201? Для простоты demo используем 200.
        # В production — 201 Created для POST create.
```

**Почему TestClient**:
- Не запускает реальный сервер.
- Отправляет запросы "внутри" Python процесса.
- Быстро и надёжно.

```python
class TestGamificationEndpoints:
    def test_complete_lesson(self):
        response = client.post("/api/v1/lessons/lesson-1/complete", json={
            "child_id": "child-1",
            "lesson_id": "lesson-1",
            "correct_answers": 5,
            "total_attempts": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert "xp_earned" in data
        assert "new_level" in data
        assert "new_streak" in data
        # Проверяем структуру ответа — все ключи на месте.
```

---

### 🐳 docker-compose.yml

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    # Почему alpine? Минимальный размер (~100MB vs ~400MB).
    environment:
      POSTGRES_USER: literacy_user
      POSTGRES_PASSWORD: literacy_pass
      POSTGRES_DB: literacy_db
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    # Почему Redis? Для Celery background jobs и кэша.
    ports:
      - "6379:6379"
```

**Почему Docker**:
- Разработчик не устанавливает PostgreSQL локально.
- `docker-compose up -d` — и БД готова.
- Одинаковое окружение у всех разработчиков.

---

### ⚙️ .github/workflows/ci.yml — CI Pipeline

```yaml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

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

**Почему CI**:
- Каждый push проверяется автоматически.
- Если тесты падают — PR не принимается.
- `--cov-fail-under=60` — покрытие не должно падать ниже 60%.

---

### 📋 requirements.txt

```
fastapi==0.109.0          # Web framework
uvicorn[standard]==0.27.0 # ASGI server
pydantic==2.5.3           # Data validation
pydantic-settings==2.1.0  # Config from env
sqlalchemy[asyncio]==2.0.25 # ORM
asyncpg==0.29.0           # PostgreSQL async driver
python-jose[cryptography]==3.3.0 # JWT
passlib[bcrypt]==1.7.4    # Password hashing
python-multipart==0.0.6   # Form data (for OAuth2)
pytest==7.4.4             # Testing
pytest-asyncio==0.23.3    # Async tests
pytest-cov==4.1.0         # Coverage
httpx==0.26.0             # HTTP client (for TestClient)
```

**Почему именно эти версии**:
- Зафиксированы (`==`) — reproducible builds. У всех одинаковые версии.
- FastAPI 0.109 — последняя стабильная на момент разработки.
- SQLAlchemy 2.0 — современный async ORM. 1.x не поддерживает async.
- asyncpg — единственный production-ready async драйвер для PostgreSQL.

---

### 📄 Документация (docs/)

| Файл | Зачем | Для кого |
|------|-------|----------|
| PRE_DEFENCE.md | Pre-Defence (1) задание | Преподаватель |
| TECHNICAL_REPORT.md | Полный отчёт (20 стр.) | Экзаменаторы |
| FULL_DOCUMENTATION.md | Вся документация | Команда |
| TEAM_DISTRIBUTION.md | Этот файл | Команда |

---

## 🎤 Распределение на защите (18 минут)

### Тайминг

| Время | Студент | Тема | Что показывать |
|-------|---------|------|----------------|
| 0:00-0:30 | Все | Вступление | Название, stack, команда |
| 0:30-2:30 | **#1** | Demo | Swagger → register → login → child → complete lesson → badges |
| 2:30-3:30 | **#1** | Gamification | Формулы XP, Level, Streak. Почему именно такие. |
| 3:30-4:30 | **#2** | Database | ERD. 11 таблиц. Связи. Индексы. Почему UUID. |
| 4:30-5:30 | **#2** | API | 22 endpoints. REST conventions. Pagination. Swagger. |
| 5:30-6:30 | **#3** | Security | JWT, bcrypt, RBAC. Почему Depends. |
| 6:30-7:30 | **#3** | Testing | 33 теста. Unit vs Integration. Coverage. |
| 7:30-8:30 | **#3** | DevOps | CI/CD, Docker, .env. |
| 8:30-18:00 | Все | Q&A | Каждый отвечает на вопросы по СВОЕЙ зоне |

---

## ❓ Кто отвечает на какие вопросы

### Студент #1 (Gamification + Auth)

| Вопрос | Ответ (1 предложение) |
|--------|----------------------|
| Формула XP? | 100 + (difficulty-1)×20, линейная для видимости прогресса |
| Формула Level? | level²×100, квадратичная для замедления прогрессии |
| Streak логика? | Вчера→+1, сегодда→без изменений, пропуск→сброс |
| Почему bcrypt? | Industry standard, salt автоматически, cost factor регулирует скорость |
| Почему JWT? | Stateless, масштабируется, не храним сессии на сервере |
| Почему 15 минут access token? | Баланс безопасности и удобства. Короче — частый re-login, дольше — риск |

### Студент #2 (Database + API)

| Вопрос | Ответ (1 предложение) |
|--------|----------------------|
| Почему 11 таблиц? | 3 roles + curriculum 3-level + progress 2 + gamification 2 + notification + audit |
| Почему UUID? | Не предсказуем, нет конфликтов при репликации, генерируется на клиенте |
| Почему JSONB (Text)? | Разные структуры упражнений, гибкость без миграций |
| Почему published flag? | Черновик → проверка → публикация. Дети видят только published |
| Почему pagination? | Защита от DDoS и переполнения памяти при больших списках |
| Почему /api/v1? | Версионирование. v2 добавим позже, v1 останется работать |

### Студент #3 (Tests + DevOps)

| Вопрос | Ответ (1 предложение) |
|--------|----------------------|
| Сколько тестов? | 33: 10 unit (логика) + 23 integration (API) |
| Почему pytest? | Стандарт для Python, fixtures, параметризация, плагины |
| Почему coverage ≥60%? | Минимум для production. Мы покрываем критичные пути |
| Почему Docker? | Одинаковое окружение, не ставим PostgreSQL локально |
| Почему GitHub Actions? | Бесплатно, интеграция с GitHub, запускается на каждый PR |
| Что если CI упадёт? | PR блокируется, нельзя сломить main ветку |

---

## ✅ Финальный чеклист перед защитой

### Студент #1
- [ ] Знаю формулу XP наизусть
- [ ] Знаю формулу Level наизусть
- [ ] Знаю логику Streak наизусть
- [ ] Могу объяснить, почему JWT, а не sessions
- [ ] Могу объяснить, почему bcrypt, а не md5/sha256
- [ ] Demo flow отработан 3 раза

### Студент #2
- [ ] Могу нарисовать ERD на доске/бумаге
- [ ] Знаю все 11 таблиц и их связи
- [ ] Могу объяснить, почему UUID
- [ ] Могу объяснить, почему JSONB для exercises
- [ ] Знаю все 22 endpoints
- [ ] Могу объяснить pagination

### Студент #3
- [ ] Знаю, что 33 теста, все проходят
- [ ] Могу запустить `pytest tests/ -v` live
- [ ] Могу объяснить разницу unit и integration тестов
- [ ] Знаю, что в docker-compose.yml
- [ ] Могу объяснить CI pipeline
- [ ] Знаю, что в .env.example

---

**Готовьтесь к защите! Удачи! 🎓**
