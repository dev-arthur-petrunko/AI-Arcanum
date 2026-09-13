# AI-Arcanum — енциклопедія ворожбильних карт (UK/RU/EN)

Навчальний ресурс: Таро, Ленорман, І-Цзин, руни, оракули. 3D-вітрина (Next.js + React Three Fiber + GSAP + Lenis), API на FastAPI (100% Python).

> Порти локального стенду: бекенд — **8001** (8000 зайнятий іншим проєктом на цій машині), фронтенд — **3100** (3000 зайнятий).

## Швидкий старт

Backend:
```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/seed_db.py
python scripts/import_lenormand.py
python scripts/import_deck.py Database/cards/elder_futhark24.json
python scripts/import_deck.py Database/cards/moon_oracle8.json
python scripts/fill_translations.py
uvicorn app.main:app --reload --port 8001
# → http://localhost:8001/docs
```

Frontend:
```powershell
cd frontend
npm install
$env:NEXT_PUBLIC_API_URL="http://localhost:8001"; npm run dev -- --port 3100
# → http://localhost:3100
```


## Структура
Див. `docs/` і `backend/Database/README.md`. RWS 1909 — суспільне надбання; сучасні колоди — лише переказ + атрибуція в `backend/Database/sources_log.md`. Усі дані — в `backend/Database/` (239 карт, 6 систем).
