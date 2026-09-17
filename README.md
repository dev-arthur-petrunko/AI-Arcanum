# AI-Arcanum — енциклопедія ворожбильних карт

Навчальний ресурс: **Таро, Ленорман, І-Цзин, руни, оракули та езотеричні системи** з 3D-вітриною карт, розкладами та гайдами. Підтримка трьох мов: **UK / RU / EN**.

- Frontend: **Next.js 14 (App Router) + React 18 + React Three Fiber + GSAP + Lenis** — у `frontend/`
- Backend: **FastAPI + SQLAlchemy + SQLite (100% Python)** — у `backend/`
- Графіка карт — **процедурна** (Pillow), згенерована скриптами, без PD-сканів для сучасних колод

---

## Що зроблено (актуальний стан)

### База знань — 33 системи · 38 колод · 912 карт · 45 статей

| Блок | Кількість | Деталі |
|---|---|---|
| Системи | **33** | Таро, Ленорман, І-Цзин, Руни, Оракули, МАК, Астрологічні, Шаманські, Циганські, Гральні, Цолькин, Карти предків, Нумерологія, Зодіак, Огам, Сабіан, Накшатри, Емоції, Чакри, Цінності, Ресурси, Сни, Стихії, Ангели, Афірмації, Бажання, Каббала, Багуа, Іфа, Числа-ангели, Тасеографія, Кристали, Астрологічний довідник |
| Колоди | **38** | Класика (Таро Вейта-Сміт 78, Вісконті-Сфорца 74, Марсель 78, Ленорман 36, І-Цзин 64, Футарк 24, рунічна поема 29) + навчальні колоди-перекази (кожна з `source_url`) |
| Карти | **912** | Усі з `image_path` (процедурні або PD-скани), тримовні тексти (базові поля + блок `translations`) |
| Статті | **45** | Гайди + астрологічний довідник (знаки, планети, доми, аспекти) тримовами |
| Розклади | **2** | Карта дня, Східний шлях (у БД); каталог схем перелічено в UI-й копії розкладів |
| Глосарій | **5** термінів | /glossary |
| Таймлайн історії | **4** епохи | /history |

Позначки колод: `is_partial` (неповний набір: Цолькин, Огам, Сабіан, Цінності), `is_reference_only` (довідковий профіль).

Джерела — суспільне надбання + власний навчальний переказ; повний реєстр джерел і ліцензій у `backend/Database/sources_log.md`.

### Фронтенд — багатосторінковий сайт

Маршрути (усі перевірені — 200 в dev і production-збірці):

| Маршрут | Що це |
|---|---|
| `/` | Головна: hero з живими лічильниками, карта дня, 8 напрямків, тизер історії, hub-посилання |
| `/directions/{slug}` | 8 напрямків-категорій (divination, oracles, therapeutic, astrological, shamanic, calendar, esoteric, numerological): системи + колоди з переходами |
| `/directions/{slug}/spreads` | Розклади обраного напрямку (там, де є) |
| `/directions/{slug}/guides` | Гайди/статті напрямку |
| `/decks/{id}` | Сторінка колоди: вкладки «Значення карт» (сітка арканів за мастями) та «3D-вітрина», пошук, випадкова карта, розбір карти, `?card=` — прямий вхід |
| `/spreads` | Каталог схем розкладів + онлайн-затяжка карт |
| `/articles` | «Гайди і статті» — 45 статей трьома мовами |
| `/history` | Таймлайн історії карт |
| `/glossary` | Глосарій термінів |
| `/quiz` | Флеш-картки-квіз за колодами |

Компоненти: `SiteNav` (шапка + dropdown «Напрямки ▾»), `SideMenu` (бургер-шторка зліва, класи `side-*`), `Scene3D` (3D-віяло, postprocessing Bloom+Vignette), `TarotCard` (переворот, hover-lift), `CardDetail` (повний розбір карти), `DirectionClient/Spreads/Guides`, `DeckClient`, `SpreadsPage`, `ArticlesPage`, `QuizPage`. Анімації: `Reveal` (IntersectionObserver + GSAP), Lenis-скрол.

Дизайн: нічна золота палітра (`--bg #070912`, `--gold #d4a94e`, `--gold-soft #e8c87a`, `--violet #7a5cff`, `--ivory #f2ead8`), Cormorant Garamond + Manrope, теми dark/light (data-theme), без UI-фреймворків.

### Бекенд

Endpoints: `/systems`, `/decks`, `/cards` (фільтри + `?lang=` + пагінація), `/cards/random`, `/cards/daily`, `/cards/{id}`, `/search` (SQLite FTS5 + LIKE-фолбек), `/spreads`, `/glossary`, `/timeline`, `/stats`, `/articles`, `/quiz/*`. Схеми Pydantic v2, CORS, Swagger-доки на `/docs`.

### Інфраструктура та якість

- Дев-стенд: backend `uvicorn` на **:8001**, frontend `next dev` на **:3000**; проксі `/api → 127.0.0.1:8001` у `next.config.js` (CORS не потрібен).
- Продакшн-збірка `next build` — чиста (lint + typecheck у складі збірки); npm-лінт окремо не конфігурований (peer-dep конфлікт eslint@8 vs eslint-config-next@16).
- Базу даних почищено від осиротілих систем і дублів-вигадок (скрипти `backend/scripts/cleanup_*`); бекапи в `backend/Database/*.db`.
- Перевірки після змін: SSR-статуси всіх маршрутів + реальні кліки меню через Chrome DevTools Protocol (dropdown, бургер, розбір карти не «улітає» — `.drawer` лише у розборі карти, шторка — `.side-*`).

---

## Швидкий старт

Backend:
```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/seed_db.py
uvicorn app.main:app --reload --port 8001
# → http://localhost:8001/docs
```

Frontend:
```powershell
cd frontend
npm install
npm run dev -- -p 3000
# → http://localhost:3000
```

---

## Структура репозиторію

```
backend/
  app/            # FastAPI: main, models, routers, schemas, services
  Database/       # fortune_cards.db, бекапи, images/, articles/*.md, sources_log.md
  scripts/        # імпортери, генератори зображень, міграції (усі ідемпотентні)
frontend/
  src/app/        # сторінки Next.js (App Router)
  src/components/ # React-компоненти (3D, розбір, навігація)
  src/lib/        # api.js (pick/getJSON), directions.js, textures.js
  public/assets/  # згенеровані зображення карт
```