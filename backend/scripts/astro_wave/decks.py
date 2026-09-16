# -*- coding: utf-8 -*-
"""decks.py — збірка 6 астрологічних навчальних колод (wave-4).

Кожна функція повертає список карт у форматі, готовому для Card(**card):
  number, name(uk), arcana_type, category, element, element_code,
  planet, planet_code, zodiac_sign, zodiac_sign_code, suit, suit_code,
  theme, symbolism, keywords_upright, meaning_general, translations{uk,en,ru}.

Тексти — власний навчальний переказ (гадальні словники), не копіпаст.
"""
from .common import (SIGNS, PLANETS, HOUSES, MOON_PHASES, ELEMENTS, SEASONS,
                     ASTEROIDS, ECLIPSES, ELEMENT_OF, PLANET_OF, PLANET_CODE,
                     PLANET_EL, SIGN_CODE, ELEMENT_UK, ELEMENT_CODE)
from .pairs import PAIRS, KIND

SHORT_PLANETS = ["Сонце", "Місяць", "Меркурій", "Венера", "Марс",
                 "Юпітер", "Сатурн", "Уран", "Нептун", "Плутон"]


def _find(lst, name):
    for r in lst:
        if r[1] == name:
            return r
    return None


def _el_name(code):
    return ELEMENT_UK.get(code, "Стихія")


def _tr(lg, name, kw, mean, theme=None):
    d = {"name": name, "keywords_upright": kw, "meaning_general": mean}
    if theme:
        d["theme"] = theme
    return d


def i18n(row):
    """row = запис common (num, uk, en, ru, kw_uk, kw_en, kw_ru, mean_uk, mean_en, mean_ru)."""
    return {"uk": _tr("uk", row[1], row[4], row[7]),
            "en": _tr("en", row[2], row[5], row[8]),
            "ru": _tr("ru", row[3], row[6], row[9])}


def _sign_card(row, sign_cls="Знак зодіаку", theme_fmt=None):
    name = row[1]
    elc = ELEMENT_OF[name]
    plc = PLANET_OF[name]
    pname = _find(PLANETS, [p for p in SHORT_PLANETS if PLANET_CODE.get(p) == plc][0])[1]
    theme = theme_fmt.format(planets=pname) if theme_fmt else f"Володар: {pname}"
    return {"number": row[0], "name": name, "arcana_type": sign_cls,
            "category": "знак зодіаку", "element": _el_name(elc), "element_code": elc,
            "planet": pname, "planet_code": plc,
            "zodiac_sign": name, "zodiac_sign_code": SIGN_CODE[name],
            "theme": theme, "keywords_upright": row[4], "meaning_general": row[7],
            "translations": i18n(row)}


def _planet_card(row, cls="Планета"):
    name = row[1]
    plc = PLANET_CODE[name]
    return {"number": row[0], "name": name, "arcana_type": cls,
            "category": "планета", "element": _el_name(PLANET_EL[name]),
            "element_code": PLANET_EL[name], "planet": name, "planet_code": plc,
            "zodiac_sign": None, "zodiac_sign_code": None,
            "theme": "Бог-покровитель у своєму міфі", "keywords_upright": row[4],
            "meaning_general": row[7], "translations": i18n(row)}


# ── 1. Weatherstone-style: 12 знаків + 10 планет (ар-нуво, Круг Домів) ──
def weatherstone():
    cards = [_sign_card(r, theme_fmt="Керує планета: {planets}") for r in SIGNS]
    cards += [_planet_card(r) for r in PLANETS]
    return cards


# ── 2. Williamson-style «Річний цикл»: 12+10+12+8+4+4 = 50 ──────────
def williamson():
    cards = [_sign_card(r, theme_fmt="Річний цикл починає: {planets}") for r in SIGNS]
    cards += [_planet_card(r) for r in PLANETS]
    cards += [{"number": r[0], "name": r[1], "arcana_type": "Астрологічний дім",
               "category": "двір життя", "theme": "Сфера: " + r[4],
               "suit_code": "house" + r[0], "keywords_upright": r[4],
               "meaning_general": r[7], "translations": i18n(r)} for r in HOUSES]
    cards += [{"number": r[0], "name": r[1], "arcana_type": "Фаза Місяця",
               "category": "місячний цикл", "theme": "Пора циклу: " + r[4],
               "suit_code": "phase" + r[0], "keywords_upright": r[4],
               "meaning_general": r[7], "translations": i18n(r)} for r in MOON_PHASES]
    cards += [{"number": r[0], "name": r[1], "arcana_type": "Стихія",
               "category": "первісна стихія", "element": r[1], "element_code": ELEMENT_CODE[r[1]],
               "theme": "Якість: " + r[4], "keywords_upright": r[4],
               "meaning_general": r[7], "translations": i18n(r)} for r in ELEMENTS]
    cards += [{"number": r[0], "name": r[1], "arcana_type": "Пора року",
               "category": "поворотна точка року", "theme": "Точка: " + r[4],
               "suit_code": "season" + r[0], "keywords_upright": r[4],
               "meaning_general": r[7], "translations": i18n(r)} for r in SEASONS]
    return cards


# ── 3. Goodchild-style «Аркани астрології»: 12+12+10+8+10+2 = 54 ────
def goodchild():
    cards = [_sign_card(r, theme_fmt="Аркан знаку: {planets}") for r in SIGNS]
    cards += [{"number": r[0], "name": r[1], "arcana_type": "Дім гороскопа",
               "category": "сфера життя", "theme": "Двір: " + r[4],
               "suit_code": "house" + r[0], "keywords_upright": r[4],
               "meaning_general": r[7], "translations": i18n(r)} for r in HOUSES]
    cards += [_planet_card(r) for r in PLANETS]
    cards += [{"number": r[0], "name": r[1], "arcana_type": "Фаза Місяця",
               "category": "місячний цикл", "theme": "Фаза: " + r[4],
               "suit_code": "phase" + r[0], "keywords_upright": r[4],
               "meaning_general": r[7], "translations": i18n(r)} for r in MOON_PHASES]
    cards += [{"number": r[0], "name": r[1], "arcana_type": "Астероїд",
               "category": "мала планета", "planet": r[1], "planet_code": "asteroid_" + r[0],
               "theme": "Голос: " + r[4], "keywords_upright": r[4],
               "meaning_general": r[7], "translations": i18n(r)} for r in ASTEROIDS]
    cards += [{"number": r[0], "name": r[1], "arcana_type": "Затемнення",
               "category": "небесна подія", "theme": "Подія: " + r[4],
               "keywords_upright": r[4], "meaning_general": r[7],
               "translations": i18n(r)} for r in ECLIPSES]
    return cards


# ── 4. Radiant Sun-style: 7 мастей × 12 знаків = 84 ────────────────
SUITS = [  # масть => (uk, en, ru, essence_uk, essence_en, essence_ru)
    ("Сонце", "Sun", "Солнце", "живильне світло", "nurturing light", "живительный свет"),
    ("Місяць", "Moon", "Луна", "мінливий відблиск почуттів", "shifting reflection of feeling", "изменчивый отблеск чувств"),
    ("Меркурій", "Mercury", "Меркурий", "гостра думка", "sharp thought", "острая мысль"),
    ("Венера", "Venus", "Венера", "м'яка краса", "soft beauty", "мягкая красота"),
    ("Марс", "Mars", "Марс", "полум'яний порив", "fiery impulse", "пламенный порыв"),
    ("Юпітер", "Jupiter", "Юпитер", "щедрий розмах", "generous sweep", "щедрый размах"),
    ("Сатурн", "Saturn", "Сатурн", "терпляча форма", "patient form", "терпеливая форма"),
]

SIGN_LOC = [  # (uk_lok, en_pre, ru_pre, outcome_uk, outcome_en, outcome_ru)
    ("В Овні", "In Aries", "В Овне", "прямота й рішучість", "directness and resolve", "прямота и решимость"),
    ("у Тельці", "In Taurus", "В Тельце", "повільність і вкорінення", "slowness and rootedness", "медленность и укоренённость"),
    ("у Близнюках", "In Gemini", "В Близнецах", "розмаїття тем", "a spread of themes", "множество тем"),
    ("у Раку", "In Cancer", "В Раке", "турбота і тепло дому", "care and home warmth", "забота и тепло дома"),
    ("у Леві", "In Leo", "Во Льве", "сцена і сяйво", "the stage and its glow", "сцена и сияние"),
    ("у Діві", "In Virgo", "В Деве", "увага до деталей", "attention to details", "внимание к деталям"),
    ("у Терезах", "In Libra", "В Весах", "рівновага краси", "the balance of beauty", "равновесие красоты"),
    ("у Скорпіоні", "In Scorpio", "В Скорпионе", "глибина без дна", "bottomless depth", "глубина без дна"),
    ("у Стрільці", "In Sagittarius", "В Стрельце", "правда обрію", "the truth of the horizon", "правда горизонта"),
    ("у Козерозі", "In Capricorn", "В Козероге", "справа часу", "the matter of time", "дело времени"),
    ("у Водолії", "In Aquarius", "В Водолее", "рамки для всіх", "frames lifted for all", "рамки для всех"),
    ("у Рибах", "In Pisces", "В Рыбах", "розчинення у мрії", "dissolution in a dream", "растворение в мечте"),
]


def radiant_sun():
    cards, n = [], 1
    for suit_uk, suit_en, suit_ru, ess_uk, ess_en, ess_ru in SUITS:
        for (srow, (sl_uk, sl_en, sl_ru, out_uk, out_en, out_ru)) in zip(SIGNS, SIGN_LOC):
            loc_uk = sl_uk[0].lower() + sl_uk[1:] if sl_uk else "в " + srow[1]
            if not loc_uk[0:1].isalpha():
                loc_uk = sl_uk
            name_uk = f"{suit_uk} {loc_uk}".replace("  ", " ")
            loc_ru = sl_ru[0].lower() + sl_ru[1:] if sl_ru and sl_ru[0].isalpha() else sl_ru
            name_en, name_ru = (f"{suit_en} in {srow[2]}", f"{suit_ru} {loc_ru}".replace("  ", " "))
            kw_uk, kw_en, kw_ru = (f"{srow[4]} · {out_uk}", f"{srow[5]} · {out_en}",
                                   f"{srow[6]} · {out_ru}")
            mean_uk = f"{suit_uk} — {ess_uk}. {sl_uk}: {out_uk}."
            mean_en = f"{suit_en} is {ess_en}. {sl_en}: {out_en}."
            mean_ru = f"{suit_ru} — {ess_ru}. {sl_ru}: {out_ru}."
            elc = ELEMENT_OF[srow[1]]
            cards.append({
                "number": str(n), "name": name_uk, "arcana_type": "Планета у знаку",
                "category": f"масть {suit_uk.lower()}", "suit": suit_uk,
                "suit_code": PLANET_CODE[suit_uk], "element": _el_name(elc),
                "element_code": elc, "planet": suit_uk, "planet_code": PLANET_CODE[suit_uk],
                "zodiac_sign": srow[1], "zodiac_sign_code": SIGN_CODE[srow[1]],
                "theme": f"{suit_uk} · {srow[1]}", "keywords_upright": kw_uk,
                "meaning_general": mean_uk,
                "translations": {"uk": _tr("uk", name_uk, kw_uk, mean_uk),
                                 "en": _tr("en", name_en, kw_en, mean_en),
                                 "ru": _tr("ru", name_ru, kw_ru, mean_ru)}})
            n += 1
    return cards


# ── 5. Waller-style «Архетипний астрологічний оракул»: 10 + 45 = 55 ──
def waller():
    cards = [_planet_card(r, cls="Планета") for r in PLANETS]
    n = 11
    for a, b, kw_uk, kw_en, kw_ru, m_uk, m_en, m_ru in PAIRS:
        pa, pb = SHORT_PLANETS[a], SHORT_PLANETS[b]
        kind = KIND.get((a, b), "harmony")
        gist = "творча напруга" if kind == "stimulus" else "співзвучність"
        cards.append({
            "number": str(n), "name": f"{pa} — {pb}", "arcana_type": "Планетарна пара",
            "category": "архетип пари", "planet": pa, "planet_code": PLANET_CODE[pa],
            "suit": pb, "suit_code": PLANET_CODE[pb],
            "element": None, "element_code": None,
            "zodiac_sign": None, "zodiac_sign_code": None,
            "theme": f"{pa} · {pb} — {gist}", "keywords_upright": kw_uk,
            "meaning_general": m_uk,
            "translations": {"uk": _tr("uk", f"{pa} — {pb}", kw_uk, m_uk),
                             "en": _tr("en", f"{PLANET_CODE[pa].title()}–{PLANET_CODE[pb].title()}",
                                       kw_en, m_en),
                             "ru": _tr("ru", f"{PB_RU[a]} — {PB_RU[b]}", kw_ru, m_ru)}})
        n += 1
    return cards


PB_RU = ["Солнце", "Луна", "Меркурий", "Венера", "Марс",
         "Юпитер", "Сатурн", "Уран", "Нептун", "Плутон"]


# ── 6. russellcottrell-style референс: 10 планет + 12 знаків = 22 ──
def reference():
    cards = [_planet_card(r, cls="Планета") for r in PLANETS]
    cards += [_sign_card(r, theme_fmt="Знак фарбує енергію: {planets}") for r in SIGNS]
    return cards


BUILDERS = {
    "weatherstone": weatherstone,
    "williamson": williamson,
    "goodchild": goodchild,
    "radiant_sun": radiant_sun,
    "waller": waller,
    "reference": reference,
}


def build(kind):
    return BUILDERS[kind]()


def total():
    return {k: len(BUILDERS[k]()) for k in BUILDERS}