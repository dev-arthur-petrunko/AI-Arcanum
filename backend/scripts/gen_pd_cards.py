"""gen_pd_cards.py — Генерує JSON-файли карт для колод 23 (Visconti, 74) та 24 (Marseille, 78).
Тексти беруться з RWS (deck 1) з урахуванням порядку Сила/Справедливость (Marseille: VIII=Justice, XI=Force).
Запуск з папки backend/: python scripts/gen_pd_cards.py
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core.database import SessionLocal, engine, Base
from app.models import Card, Deck

Base.metadata.create_all(bind=engine)
db = SessionLocal()

RWS = {c.number: c for c in db.query(Card).filter_by(deck_id=1).all()}
deck7 = db.query(Deck).filter_by(id=7).first()
if deck7:
    deck7.card_count = 20
    print(f"[fix] deck 7 card_count 12 -> 20")
db.commit()

ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]

MAJORS_23 = ["0","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XVII","XVIII","XIX","XX","XXI"]
MAJORS_24 = ROMAN

SUIT_MAP = {
    "Wands": ("wands", "wands"), "Cups": ("cups", "cups"),
    "Swords": ("swords", "swords"), "Pentacles": ("pentacles", "pentacles"),
}


def rws_card(number):
    c = RWS.get(number)
    if not c: return None
    return {
        "number": c.number, "name": c.name, "arcana_type": c.arcana_type,
        "suit": c.suit, "element": c.element, "zodiac_sign": c.zodiac_sign,
        "planet": c.planet, "numerology": c.numerology,
        "suit_code": c.suit_code, "element_code": None,
        "zodiac_sign_code": None, "planet_code": None,
        "keywords_upright": c.keywords_upright, "keywords_reversed": c.keywords_reversed,
        "meaning_general": c.meaning_general, "meaning_love": c.meaning_love,
        "meaning_career": c.meaning_career, "meaning_health": c.meaning_health,
        "symbolism": c.symbolism, "image_path": None,
        "category": None, "theme": None,
        "translations": json.loads(c.translations) if isinstance(c.translations, str) else (c.translations or {}),
    }


def build_card(deck_id, number, img_slot, rws_data, extra_name=None, extra_translations=None):
    card = dict(rws_data)
    card["number"] = number
    card["image_path"] = f"/assets/{deck_id}/{img_slot}.jpg"
    if extra_name:
        card["name"] = extra_name
    if extra_translations:
        for lang in ["uk", "ru", "en"]:
            if lang in extra_translations:
                card.setdefault("translations", {}).setdefault(lang, {}).update(extra_translations[lang])
    return card


def gen(deck_id, majors, suffix):
    cards = []
    # Мажорні аркани
    for roman in majors:
        n = ROMAN.index(roman)
        rws_num = roman
        # Marseille/Visconti: VIII=Justice (RWS XI), XI=Strength (RWS VIII)
        if roman == "VIII":
            rws_num = "XI"  # Справедливость
        elif roman == "XI":
            rws_num = "VIII"  # Сила
        r = rws_card(rws_num)
        if not r: continue
        extra = {}
        if roman == "VIII":
            extra = {"name": "Справедливость", "translations": {
                "uk": {"name": "Справедливість"}, "ru": {"name": "Справедливость"}, "en": {"name": "Justice"}
            }}
        elif roman == "XI":
            extra = {"name": "Сила", "translations": {
                "uk": {"name": "Сила"}, "ru": {"name": "Сила"}, "en": {"name": "Strength"}
            }}
        cards.append(build_card(deck_id, roman, roman, r, extra_name=extra.get("name"),
                                extra_translations=extra.get("translations")))
    # Мінорні аркани
    for rws in ["Wands", "Cups", "Swords", "Pentacles"]:
        rws_suit = rws.lower()
        for i in range(1, 15):
            rws_num = f"{rws}-{i:02d}"
            r = rws_card(rws_num)
            if not r: continue
            slot = f"{rws_suit}-{i:02d}"
            cards.append(build_card(deck_id, rws_num, slot, r))
    return cards


# --- Marseille (deck 24) ---
cards_24 = gen(24, MAJORS_24, "24")
print(f"Marseille: {len(cards_24)} карт")

# --- Visconti (deck 23) ---
VISCONTI_SKIP = {"XV", "XVI"}  # Диявол, Башта — відсутні в Morgan
VISCONTI_MINOR_SKIP = {"Cups-14", "Pentacles-12"}  # відсутні
cards_23 = []
for roman in MAJORS_23:
    if roman in VISCONTI_SKIP: continue
    n = ROMAN.index(roman)
    rws_num = roman
    if roman == "VIII":
        rws_num = "XI"
    elif roman == "XI":
        rws_num = "VIII"
    r = rws_card(rws_num)
    if not r: continue
    extra = {}
    if roman == "VIII":
        extra = {"name": "Справедливість", "translations": {
            "uk": {"name": "Справедливість"}, "ru": {"name": "Справедливость"}, "en": {"name": "Justice"}
        }}
    elif roman == "XI":
        extra = {"name": "Сила", "translations": {
            "uk": {"name": "Сила"}, "ru": {"name": "Сила"}, "en": {"name": "Strength"}
        }}
    cards_23.append(build_card(23, roman, roman, r, extra_name=extra.get("name"),
                                extra_translations=extra.get("translations")))
for rws in ["Wands", "Cups", "Swords", "Pentacles"]:
    rws_suit = rws.lower()
    for i in range(1, 15):
        rws_num = f"{rws}-{i:02d}"
        if rws_num in VISCONTI_MINOR_SKIP: continue
        r = rws_card(rws_num)
        if not r: continue
        slot = f"{rws_suit}-{i:02d}"
        cards_23.append(build_card(23, rws_num, slot, r))
print(f"Visconti: {len(cards_23)} карт")

# Зберігаємо JSON
out = Path(__file__).resolve().parents[1] / "Database" / "cards"
out.mkdir(parents=True, exist_ok=True)

for did, name, cards, desc_uk, desc_ru in [
    (24, "Tarot de Marseille", cards_24,
     "Канон французького Таро XVII–XVIII ст. Навчальна модель з переказом Уейта.",
     "Канон французского Таро XVII–XVIII вв."),
    (23, "Visconti-Sforza Tarot", cards_23,
     "Найстаріша збережена колода (бл. 1450). Morgan Library, Нью-Йорк. 74 карти з 78.",
     "Старейшая сохранившаяся колода (ок. 1450). Morgan Library, Нью-Йорк."),
]:
    path = out / f"pd{did}_tarot.json"
    data = {
        "system": {
            "name": "Таро", "category": "гадательні",
            "description": "Загальносвітова система гадальних карт зі Старшими та Молодшими арканами.",
            "history": "XV ст., Італія → Франція → світ.",
            "origin_country": "Італія / Франція", "approx_year": 1450,
            "translations": {"ru": {"name": "Таро"}, "en": {"name": "Tarot"}, "uk": {"name": "Таро"}}
        },
        "deck": {
            "name": name, "author": "Традиція (навчальний переказ)",
            "year": None, "card_count": len(cards),
            "cover_image": f"/assets/{did}/0.jpg",
            "description": desc_uk,
            "translations": {
                "uk": {"name": name, "description": desc_uk},
                "ru": {"name": name, "description": desc_ru},
            }
        },
        "cards": cards,
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Збережено: {path} ({len(cards)} карт)")

db.close()
print("Готово.")