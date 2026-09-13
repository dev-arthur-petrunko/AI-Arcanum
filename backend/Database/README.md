# Database — все данные проекта в одном месте (бэкенд, 100% Python)

```
Database/
├── fortune_cards.db      # SQLite: системы, колоды, карты, расклады, статьи, квиз-прогресс
├── migrations/           # Alembic-миграции (при росте — PostgreSQL)
├── cards/                # готові JSON: lenormand36, elder_futhark24, moon_oracle8, mak_archetypes12, astro_oracle26, shaman_totems12
├── images/               # фотоархів: rws/ (78 PD-сканів) + згенеровані 01–15 (340, див. scripts/generate_deck_images.py)
├── backups/              # ротація копій БД (scripts/backup_db.py, останні 10)
├── articles/             # статьи энциклопедии (markdown + импорт в таблицу articles)
├── raw/                  # сырые материалы до импорта: tarot/ lenormand/ oracles/ mak/ astrology_decks/
├── _pd_cache/            # кэш public-domain текстов (Waite OCR с archive.org)
└── sources_log.md        # откуда взят каждый текст (этика/атрибуция)
```

Правила:
- Никаких секретов (`.env` живёт в `backend/`, не здесь).
- Современные авторские тексты — только пересказ своими словами + `source_reference`.
- Импорт: `python scripts/seed_db.py`, `import_lenormand.py`, `import_public_domain_sources.py`,
  `import_from_csv.py`, `seed_articles.py` (статьи из `articles/*.md`).
