"""import_tarot_wave.py — навчальні таро: 7 колод / 546 карт.

Навчальні аналоги 7 комерційних колод (Angel Tarot, Tarot Neocolonial de
las Americas, Fablemaker's Animated Tarot, Alice in Wonderland Tarot,
Vision Quest Tarot, Golden Black Cat Tarot, Folklore Tarot). Усі значення —
ВЛАСНИЙ переказ поверх базових навчальних формулювань RWS (base_texts.BASE);
глибокі тексти (love/career/health/spirituality/reversed) копіюються з
першої колоди (deck 1) — нашої ж бази RWS. Ілюстрації процедурні, скани
не копіюємо.

Ідемпотентний: оновлює колоду за name, перевикористовує систему «Таро».
Запуск з папки backend/:  python scripts/import_tarot_wave.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Card, Deck, System

from tarot_wave import DECKS, build

SRC = {
    "angel": "https://www.rockpoolpublishing.com.au/angel-tarot",
    "neocolonial": "https://www.usgamesinc.com/tarot-neocolonial-de-las-americas",
    "fablemaker": "https://www.usgamesinc.com/the-fablemakers-animated-tarot",
    "alice": "https://www.insighteditions.com/products/alice-in-wonderland-tarot-deck",
    "visionquest": "https://www.agmuller.net/vision-quest-tarot",
    "goldencat": "https://www.usgamesinc.com/golden-black-cat-tarot",
    "folklore": "https://www.usgamesinc.com/folklore-tarot",
}


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    n_deck = n_card = 0
    try:
        system = db.query(System).filter_by(name="Таро").first()
        if not system:
            system = System(name="Таро", category="таро", history="Класичні карти Таро.",
                            origin_country=None, description="Система Таро.",
                            translations={"uk": {"name": "Таро"}, "en": {"name": "Tarot"},
                                          "ru": {"name": "Таро"}})
            db.add(system)
            db.flush()

        # Перша колода (RWS) — джерело глибоких навчальних текстів.
        deck1 = db.query(Deck).filter_by(id=1).first()
        deep = {}
        if deck1:
            for c in db.query(Card).filter_by(deck_id=deck1.id).all():
                deep[c.number] = c

        for kind, th in DECKS.items():
            deck = db.query(Deck).filter_by(name=th["name_uk"]).first()
            rows = build(kind)
            fields = {
                "system_id": system.id, "author": th["author"],
                "publisher": th["publisher"], "year": th["year"],
                "card_count": len(rows), "cover_image": None,
                "source_url": th.get("source", SRC.get(kind)),
                "is_reference_only": False,
                "composition": th["composition"], "gallery": None,
                "description": th["description"],
                "translations": {
                    "uk": {"name": th["name_uk"], "description": th["description"]},
                    "en": {"name": th["name_en"], "description": th["description"]},
                    "ru": {"name": th["name_ru"], "description": th["description"]}},
            }
            if deck:
                for k, v in fields.items():
                    setattr(deck, k, v)
            else:
                deck = Deck(name=th["name_uk"], **fields)
                db.add(deck)
                db.flush()
                n_deck += 1
            db.query(Card).filter_by(deck_id=deck.id).delete()
            db.flush()

            for card in rows:
                num = card["number"]
                d1 = deep.get(num)
                item = dict(card)
                # глибокі переклади — з першої колоди (наші тексти)
                tr = dict(card.get("translations", {}))
                if d1 is not None and d1.translations:
                    for lang, langs in d1.translations.items():
                        d = tr.setdefault(lang, {})
                        for f in ("meaning_love", "meaning_career", "meaning_health",
                                  "meaning_spirituality", "meaning_reversed",
                                  "keywords_reversed"):
                            if langs.get(f):
                                d[f] = langs[f]
                item["translations"] = tr
                # base-мова колоди — українська: карткові поля теж українською
                u = tr.get("uk", {})
                for f in ("meaning_love", "meaning_career", "meaning_health",
                          "meaning_spirituality", "meaning_reversed",
                          "keywords_reversed"):
                    item[f] = u.get(f) if d1 is not None else None
                db.add(Card(deck_id=deck.id, **item))
                n_card += 1
        db.commit()
        print(f"[tarot-wave] колод: {n_deck} нових, карт: {n_card}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()