# Fortune-telling Cards — энциклопедия гадательных карт (RU/UK/EN)

Образовательный ресурс: Таро, Ленорман, оракулы, МАК, руны. 3D-полка колод (Next.js + React Three Fiber + GSAP + Lenis), API на FastAPI.

## Быстрый старт

Backend:
```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/seed_db.py
uvicorn app.main:app --reload
# → http://localhost:8000/docs
```

Frontend:
```powershell
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

## Структура
См. ТЗ в `docs/`. RWS 1909 — public domain; современные колоды — только пересказ + атрибуция в `content/sources_log.md`.
