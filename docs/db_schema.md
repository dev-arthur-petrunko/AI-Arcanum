# Схема БД
См. ТЗ §4. Реализация: `backend/app/models/models.py`.
- `systems` + `translations JSON {uk,en}` (RU — базовые колонки)
- `decks.system_id → systems`
- `cards.deck_id → decks` (+ element, planet, zodiac_sign, suit, numerology, meanings, symbolism, image_path)
- `card_correspondences(card_id_a, card_id_b, relation_type)`
- `spreads` + `spread_positions`
- `quiz_progress(user_id, card_id, correct_count, last_reviewed)`

Поиск: сейчас LIKE + fallback по translations в Python; апгрейд → SQLite FTS5 / Postgres tsvector.
Миграции: Alembic (папка `backend/Database/migrations`), старт — `Base.metadata.create_all`.
Файл БД: `backend/Database/fortune_cards.db`. Все данные (JSON, статьи, кэш, sources_log) — в `backend/Database/`.
