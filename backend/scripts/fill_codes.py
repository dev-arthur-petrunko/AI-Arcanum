"""fill_codes.py — проставляє мовно-незалежні коди (suit/element/zodiac/planet_code)
за текстовими полями (RU або UK). Ідемпотентний.
Запуск з папки backend/: python scripts/fill_codes.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Card

ELEMENTS = {"огонь": "fire", "вогонь": "fire", "вода": "water",
            "воздух": "air", "повітря": "air", "земля": "earth"}
SUITS = {"жезлы": "wands", "кубки": "cups", "мечи": "swords", "пентакли": "pentacles",
         "чирва": "hearts", "черви": "hearts", "бубна": "diamonds", "бубны": "diamonds",
         "трефа": "clubs", "трефы": "clubs", "піка": "spades", "пика": "spades",
         "піки": "spades", "пики": "spades"}
ZODIAC = {"овен": "aries", "телець": "taurus", "телец": "taurus",
          "близнюки": "gemini", "близнецы": "gemini", "рак": "cancer",
          "лев": "leo", "діва": "virgo", "дева": "virgo", "терези": "libra",
          "весы": "libra", "скорпіон": "scorpio", "скорпион": "scorpio",
          "стрілець": "sagittarius", "стрелец": "sagittarius",
          "козеріг": "capricorn", "козерог": "capricorn", "водолій": "aquarius",
          "водолей": "aquarius", "риби": "pisces", "рыбы": "pisces"}
PLANETS = {"сонце": "sun", "солнце": "sun", "місяць": "moon", "луна": "moon",
           "меркурій": "mercury", "меркурий": "mercury", "венера": "venus",
           "марс": "mars", "юпітер": "jupiter", "юпитер": "jupiter",
           "сатурн": "saturn",
           "уран": "uranus", "нептун": "neptune", "плутон": "pluto",
           "овен": "aries"}


def code(mapping: dict, value: str | None) -> str | None:
    if not value:
        return None
    return mapping.get(value.strip().lower())


def run() -> None:
    Base.metadata.create_all(bind=engine)
    # create_all не вміє ALTER: докручуємо нові колонки вручну (SQLite)
    from sqlalchemy import text
    with engine.begin() as conn:
        for col in ("suit_code", "element_code", "zodiac_sign_code", "planet_code"):
            try:
                conn.execute(text(f"ALTER TABLE cards ADD COLUMN {col} VARCHAR(32)"))
            except Exception as e:
                if "duplicate column" not in str(e).lower():
                    raise
    db = SessionLocal()
    n = 0
    try:
        for c in db.query(Card).all():
            c.element_code = code(ELEMENTS, c.element)
            c.suit_code = code(SUITS, c.suit)
            c.zodiac_sign_code = code(ZODIAC, c.zodiac_sign)
            c.planet_code = code(PLANETS, c.planet)
            n += 1
        db.commit()
        print(f"[codes] проставлено: {n}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
