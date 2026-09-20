# ✦ AI-Arcanum — жива енциклопедія ворожильних карт

> Інтерактивна 3D-енциклопедія Таро, Ленорман, І-Цзин, рун та оракулів.
> Світ символів — із процедурною графікою, розкладами, довідником снів і гайдами — трьома мовами: **UK · RU · EN**.

---

## Що це

**AI-Arcanum** — навчально-довідковий проєкт, у якому карти **не скани і не фото**, а **процедурно згенеровані твори**: кожен аркан складається кодом (Python + Pillow) і показується в інтерактивній **3D-вітрині** з перегортанням, світінням та частинками.

Уся база — власний дослідницький переказ: **28 езотеричних систем**, класичні та авторські колоди, розбори значень, алфавітний словник снів. Тексти написані своїми словами (навчальні аналоги, без копіпасту захищених джерел).

```
        ✦ AI-ARCANUM ✦
   ┌─────────────────────────────┐
   │  Таро · Ленорман · І-Цзин    │
   │  Руни · Оракули · Кристали   │
   │  Сонник · Сабіан · Каббала   │
   └─────────────────────────────┘
     1000+ карт · 3D · 3 мови
```

---

## Можливості

- **1004 карти** в 32 колодах і 28 системах — кожну можна перегорнути в 3D, подивитися зображення та повний розбір значення.
- **8 напрямків-категорій**: ворожіння, оракули, терапевтика, астрологія, шаманізм, календарі, езотерика, нумерологія.
- **3D-вітрина** (React Three Fiber): віяло карт, місяць, стіл із золотими кільцями, зірки, bloom і віньєтка.
- **Повний розбір карти**: переклад, ключові значення (пряме і перевернуте), теми, символи, карта дня.
- **Сонник** — алфавітний словник із **113 символів сновидінь** (UK/RU/EN): пошук, фільтр за буквою, асоціації та самостійна інтерпретація.
- **Розклади** (11 схем), карта дня, випадкова карта колоди, прямий вхід через `?card=`.
- **Три мови інтерфейсу й контенту** — перемикання в один клік.
- **Темна (нічне золото) та світла (пергамент) теми**.
- **45 статей і гайдів**, глосарій, таймлайн історії карт, флеш-квіз.
- Повнотекстовий пошук по базі (SQLite FTS5).

---

## Технології

| Шар | Стек |
|---|---|
| Frontend | **Next.js 14** (App Router) · React 18 · React Three Fiber · GSAP · Lenis |
| Backend | **FastAPI** · SQLAlchemy · SQLite (100% Python) |
| Графіка | процедурна генерація карт на **Pillow** |
| Стилі | чистий CSS, дизайн-система «Нічне золото», без UI-фреймворків |

### API

`/systems` · `/decks` · `/cards` (+ `?deck_id`, `?lang`, пошук) · `/cards/random` · `/cards/daily` · `/search` (FTS5) · `/spreads` · `/articles` · `/quiz/*`

Інтерактивні Swagger-документи — на `http://localhost:8001/docs`.

---

## Маршрути сайту

| Маршрут | Що це |
|---|---|
| `/` | Головна: живий лічильник систем/колод/карт, карта дня, напрямки |
| `/directions/{slug}` | 8 напрямків: усі карти колод напрямку одразу, згруповані за колодами |
| `/directions/{slug}/spreads` · `/guides` | Розклади й гайди напрямку |
| `/decks/{id}` | Сторінка колоди: значення карт (за мастями) і 3D-вітрина |
| `/spreads` | Каталог схем розкладів + онлайн-розклад |
| `/articles` | 45 статей трьома мовами |
| `/history` · `/glossary` · `/quiz` | Таймлайн, глосарій, флеш-квіз |

---

## Швидкий старт

### Backend (`http://localhost:8001`)

```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/seed_db.py
uvicorn app.main:app --reload --port 8001
```

### Frontend (`http://localhost:3000`)

```powershell
cd frontend
npm install
node node_modules\next\dist\bin\next dev
```

Запити `/api/*` проксуються на backend у `next.config.js`.

> Примітка: не запускайте `npm run build`, поки працює dev-сервер — вони ділять `.next` і можуть зламати один одного. Спершу зупиніть dev-сервер.

---

## База знань

- **28 систем**: Таро, Ленорман, І-Цзин, руни, оракули, МАК, астрологія, шаманізм, циганські, гральні, Цолькин, нумерологія, зодіак, Огам, Сабіан, накшатри, чакри, карти снів, стихії, ангели, Каббала, Багуа, Іфа, числа-ангели, тасеографія, кристали, астрологічний довідник, терапевтичні карти, сонник.
- **32 колоди**: класика (Вейт-Сміт 78, Марсель 78, Вісконті-Сфорца 74, Ленорман 36, І-Цзин 64, Футарк 24, рунічна поема 29) + навчальні колоди-перекази із зазначенням `source_url`.
- **1004 карти** (891 із процедурним або PD-зображенням) — тримовні тексти.
- **Сонник**: 113 символів, відсортованих за українським алфавітом, з перекладами RU/EN.

_Повний реєстр джерел і ліцензій — у `backend/Database/sources_log.md`._

---

## Структура репозиторію

```
backend/
  app/            # FastAPI: main.py, models, routers, schemas, services
  Database/       # fortune_cards.db, бекапи, images/, cards/*.json, articles/*.md, sources_log.md
  scripts/        # імпортери, генератори зображень, скрипти збірки даних
frontend/
  src/app/        # сторінки Next.js (App Router)
  src/components/ # React-компоненти: 3D-сцена, розбір карти, навігація, словник снів
  src/lib/        # api.js, directions.js, textures.js, dreams/* (статичний фолбек сонника)
  public/assets/  # згенеровані зображення карт
```

---

## Якість

- Продакшен-збірка `next build` — чиста.
- SSR-статуси всіх маршрутів перевіряються після кожної хвилі змін.
- База очищена від сирітських систем і дублів; сторінки сонника працюють від БД із статичним фолбеком.

---

**✦ AI-Arcanum · енциклопедія ворожильних карт ✦**

---

# ✦ AI-Arcanum — living encyclopedia of divination cards

> Interactive 3D encyclopedia of Tarot, Lenormand, I-Ching, runes and oracles.
> A world of symbols — with procedural graphics, spreads, a dream dictionary and guides — in three languages: **UK · RU · EN**.

---

## What it is

**AI-Arcanum** is an educational and reference project where the cards are **not scans or photos**, but **procedurally generated works**: every card is built by code (Python + Pillow) and presented in an interactive **3D showcase** with flipping, glow and particles.

The whole database is an original educational retelling: **28 esoteric systems**, classic and author decks, in-depth meanings, and an alphabetical dream dictionary. All texts are written in our own words (educational analogs, no copy-paste of protected sources).

---

## Features

- **1,004 cards** in 32 decks and 28 systems — flip each one in 3D, view the image and a full meaning breakdown.
- **8 direction categories**: divination, oracles, therapeutic, astrology, shamanism, calendars, esoterica, numerology.
- **3D showcase** (React Three Fiber): a fan of cards, the moon, a table with golden rings, stars, bloom and vignette.
- **Full card breakdown**: translation, key meanings (upright and reversed), themes, symbols, card of the day.
- **Dream dictionary** — an alphabetical glossary of **113 dream symbols** (UK/RU/EN): search, letter filter, associations and guided self-interpretation.
- **Spreads** (11 layouts), card of the day, random card, deep link via `?card=`.
- **Three interface and content languages** — switch in one click.
- **Dark (night gold) and light (parchment) themes**.
- **45 articles and guides**, glossary, history timeline, flash quiz.
- Full-text search over the database (SQLite FTS5).

---

## Tech stack

| Layer | Stack |
|---|---|
| Frontend | **Next.js 14** (App Router) · React 18 · React Three Fiber · GSAP · Lenis |
| Backend | **FastAPI** · SQLAlchemy · SQLite (100% Python) |
| Graphics | procedural card generation with **Pillow** |
| Styles | plain CSS, "Night Gold" design system, no UI framework |

### API

`/systems` · `/decks` · `/cards` (+ `?deck_id`, `?lang`, search) · `/cards/random` · `/cards/daily` · `/search` (FTS5) · `/spreads` · `/articles` · `/quiz/*`

Interactive Swagger docs at `http://localhost:8001/docs`.

---

## Site routes

| Route | What it is |
|---|---|
| `/` | Home: live counter of systems/decks/cards, card of the day, directions |
| `/directions/{slug}` | 8 directions: all cards of the direction's decks at once, grouped by deck |
| `/directions/{slug}/spreads` · `/guides` | Direction spreads and guides |
| `/decks/{id}` | Deck page: card meanings (by suit) and 3D showcase |
| `/spreads` | Spread layouts catalog + online layout |
| `/articles` | 45 articles in three languages |
| `/history` · `/glossary` · `/quiz` | Timeline, glossary, flash quiz |

---

## Quick start

### Backend (`http://localhost:8001`)

```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/seed_db.py
uvicorn app.main:app --reload --port 8001
```

### Frontend (`http://localhost:3000`)

```powershell
cd frontend
npm install
node node_modules\next\dist\bin\next dev
```

Requests to `/api/*` are proxied to the backend in `next.config.js`.

> Note: do not run `npm run build` while the dev server is running — they share `.next` and can break each other. Stop the dev server first.

---

## Knowledge base

- **28 systems**: Tarot, Lenormand, I-Ching, runes, oracles, MAC, astrology, shamanism, gypsy, playing, Tzolkin, numerology, zodiac, Ogham, Sabian, nakshatras, chakras, dream cards, elements, angels, Kabbalah, Bagua, Ifa, angel numbers, tasseography, crystals, astrological reference, therapeutic cards, dream dictionary.
- **32 decks**: classics (Waite-Smith 78, Marseille 78, Visconti-Sforza 74, Lenormand 36, I-Ching 64, Futhark 24, rune poem 29) + educational retellings with `source_url`.
- **1,004 cards** (891 with procedural or public-domain images) — trilingual texts.
- **Dream dictionary**: 113 symbols sorted by the Ukrainian alphabet, with RU/EN translations.

_Full source & license registry — in `backend/Database/sources_log.md`._

---

## Repository structure

```
backend/
  app/            # FastAPI: main.py, models, routers, schemas, services
  Database/       # fortune_cards.db, backups, images/, cards/*.json, articles/*.md, sources_log.md
  scripts/        # importers, image generators, data build scripts
frontend/
  src/app/        # Next.js pages (App Router)
  src/components/ # React components: 3D scene, card meaning, navigation, dream dictionary
  src/lib/        # api.js, directions.js, textures.js, dreams/* (static sonnik fallback)
  public/assets/  # generated card images
```

---

## Quality

- Production `next build` — clean.
- SSR status for every route is re-checked after each change wave.
- Database cleaned of orphan systems and duplicates; dream pages run from the DB with a static fallback.

---

**✦ AI-Arcanum · encyclopedia of divination cards ✦**