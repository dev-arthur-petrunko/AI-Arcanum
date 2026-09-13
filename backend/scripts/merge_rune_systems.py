"""merge_rune_systems.py — разовий фікс: зливає дубль систем «Руны»/«Руни» в одну «Руни».
Колоди футарку й поеми привʼязуються до неї; порожня система видаляється.
Запуск з папки backend/: python scripts/merge_rune_systems.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.models import Deck, System


def run():
    db = SessionLocal()
    try:
        ru = db.query(System).filter_by(name="Руны").first()
        uk = db.query(System).filter_by(name="Руни").first()
        if not ru:
            print("Дубля нема: системи «Руны» не знайдено.")
            return
        if not uk:
            ru.name = "Руни"
            ru.translations = {"ru": {"name": "Руны"}, "en": {"name": "Runes"}}
            db.commit()
            print("Перейменовано «Руны» → «Руни».")
            return
        for deck in db.query(Deck).filter_by(system_id=ru.id).all():
            deck.system_id = uk.id
        uk.translations = {"ru": {"name": "Руны"}, "en": {"name": "Runes"}}
        db.delete(ru)
        db.commit()
        print(f"Злито: колоди тепер у «Руни» (id={uk.id}).")
    finally:
        db.close()


if __name__ == "__main__":
    run()
