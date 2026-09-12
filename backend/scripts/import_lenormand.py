"""Импорт Ленорман-36 из content/lenormand/lenormand36.json. Идемпотентный (по deck+number).
Запуск: python scripts/import_lenormand.py  (из папки backend/)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Card, Deck, System

SRC = Path(__file__).resolve().parents[2] / "content" / "lenormand" / "lenormand36.json"


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        system = db.query(System).filter_by(name="Ленорман").first()
        if not system:
            system = System(name="Ленорман", category="гадательные",
                            description="36 карт с бытовыми символами; чтение парами/триадами.",
                            origin_country="Германия / Франция", approx_year=1799,
                            translations={"uk": {"name": "Ленорман"}, "en": {"name": "Lenormand"}})
            db.add(system)
            db.flush()
        deck = db.query(Deck).filter_by(name="Petit Lenormand (учебная)").first()
        if not deck:
            deck = Deck(system_id=system.id, name="Petit Lenormand (учебная)",
                        author="учебная сводка по исторической колоде ~1799",
                        year=1799, card_count=36, cover_image="/assets/card_images/lenormand/cover.jpg",
                        description="Учебные пересказы значений 36 карт. Не копипаст современных ГБК.",
                        translations={"uk": {"name": "Petit Lenormand (навчальна)"},
                                      "en": {"name": "Petit Lenormand (study)"}})
            db.add(deck)
            db.flush()
        data = json.loads(SRC.read_text(encoding="utf-8"))
        added = 0
        for item in data:
            exists = db.query(Card).filter_by(deck_id=deck.id, number=item["number"]).first()
            if exists:
                continue
            db.add(Card(
                deck_id=deck.id, number=item["number"], name=item["name"],
                arcana_type="Оракул Ленорман", suit=item.get("suit"), element=item.get("element"),
                keywords_upright=item.get("keywords_upright"), keywords_reversed=item.get("keywords_reversed"),
                meaning_general=f"{item['name']}: {item.get('keywords_upright', '')}. Учебный пересказ; читайте в связке с соседями.",
                symbolism="Бытовой символ; значение раскрывается в паре/триаде.",
                image_path=f"/assets/card_images/lenormand/{int(item['number']):02d}.jpg",
                translations=item.get("translations"),
            ))
            added += 1
        db.commit()
        total = db.query(Card).filter_by(deck_id=deck.id).count()
        print(f"Lenormand: added {added}, total in deck {total}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
