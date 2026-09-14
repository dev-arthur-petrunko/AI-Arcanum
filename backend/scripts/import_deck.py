"""import_deck.py — універсальний імпорт колоди з Database/cards/*.json.
Формат: {"system": {...}, "deck": {...}, "cards": [...]}. Ідемпотентний (deck+number).
Запуск з папки backend/:
    python scripts/import_deck.py Database/cards/elder_futhark24.json
    python scripts/import_deck.py Database/cards/moon_oracle8.json
    python scripts/import_deck.py Database/cards/moon_oracle8.json --upsert  # оновлює існуючі картки (тільки не-None поля)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Card, Deck, System

CARD_FIELDS = ("number", "name", "arcana_type", "suit", "element", "zodiac_sign",
               "planet", "numerology", "keywords_upright", "keywords_reversed",
               "meaning_general", "meaning_love", "meaning_career", "meaning_health",
               "symbolism", "image_path", "model_3d_path", "translations",
               "category", "theme")


def run(path: str) -> int:
    Base.metadata.create_all(bind=engine)
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    db = SessionLocal()
    try:
        s = data.get("system", {})
        system = db.query(System).filter_by(name=s.get("name")).first()
        if not system:
            system = System(name=s.get("name"), category=s.get("category"),
                            description=s.get("description"), history=s.get("history"),
                            origin_country=s.get("origin_country"),
                            approx_year=s.get("approx_year"),
                            translations=s.get("translations"))
            db.add(system)
            db.flush()
        d = data.get("deck", {})
        deck = db.query(Deck).filter_by(name=d.get("name")).first()
        if not deck:
            deck = Deck(system_id=system.id, name=d.get("name"), author=d.get("author"),
                        publisher=d.get("publisher"), year=d.get("year"),
                        card_count=d.get("card_count"), cover_image=d.get("cover_image"),
                        description=d.get("description"), translations=d.get("translations"))
            db.add(deck)
            db.flush()
        added = 0
        updated = 0
        upsert = "--upsert" in sys.argv
        for item in data.get("cards", []):
            number = item.get("number")
            card = db.query(Card).filter_by(deck_id=deck.id, number=number).first()
            if card is None:
                db.add(Card(deck_id=deck.id, **{k: item.get(k) for k in CARD_FIELDS}))
                added += 1
                continue
            if upsert:
                for k in CARD_FIELDS:
                    if item.get(k) is not None:
                        setattr(card, k, item.get(k))
                updated += 1
        db.commit()
        total = db.query(Card).filter_by(deck_id=deck.id).count()
        print(f"[{deck.name}] нових: {added}, оновлено: {updated}, всього: {total}")
        return added
    finally:
        db.close()


if __name__ == "__main__":
    run(sys.argv[1])
