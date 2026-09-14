"""ensure_schema.py — докручує колонки, яких create_all не вміє додавати в існуючу БД.
Ідемпотентний (SQLite ADD COLUMN, duplicate ігнорується).
Запуск з папки backend/: python scripts/ensure_schema.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import text

from app.core.database import Base, engine

COLUMNS = {
    "suit_code": "VARCHAR(32)",
    "element_code": "VARCHAR(32)",
    "zodiac_sign_code": "VARCHAR(32)",
    "planet_code": "VARCHAR(32)",
    "category": "VARCHAR(64)",
    "theme": "TEXT",
}
DECK_COLUMNS = {
    "is_reference_only": "BOOLEAN DEFAULT 0",
    "source_url": "VARCHAR(512)",
    "buy_url": "VARCHAR(512)",
    "composition": "TEXT",
    "gallery": "JSON",
}


def run() -> None:
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        for col, ddl in COLUMNS.items():
            try:
                conn.execute(text(f"ALTER TABLE cards ADD COLUMN {col} {ddl}"))
                print(f"[schema] cards +{col}")
            except Exception as e:
                if "duplicate column" not in str(e).lower():
                    raise
        for col, ddl in DECK_COLUMNS.items():
            try:
                conn.execute(text(f"ALTER TABLE decks ADD COLUMN {col} {ddl}"))
                print(f"[schema] decks +{col}")
            except Exception as e:
                if "duplicate column" not in str(e).lower():
                    raise
    print("[schema] ok")


if __name__ == "__main__":
    run()
