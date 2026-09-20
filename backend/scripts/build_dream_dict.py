# -*- coding: utf-8 -*-
"""build_dream_dict.py — збирає Database/cards/dream_dictionary.json для імпорту сонника.
Дані у scripts/dream_rows_full.py (81 символ сновидінь, переказ своїми словами,
у форматі {system, deck, cards} для scripts/import_deck.py).
Запуск з папки backend/: python scripts/build_dream_dict.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dream_rows_full import ROWS_FULL

ROWS = ROWS_FULL
OUT = Path(__file__).resolve().parents[1] / "Database" / "cards" / "dream_dictionary.json"

SYSTEM = {
    "name": "Сонник",
    "category": "сонники",
    "description": f"Навчальний сонник: {len(ROWS)} символів сновидінь простими словами по всій абетці — від «Автобуса» до «Ящірки». Коротке значення, ключові слова й переклад трьома мовами — щоб легко згадати зміст сну й побачити, про що говорить підсвідомість.",
    "history": "Тлумачення снів — давня практика багатьох культур: від храмових сонників античності до психології XX століття. Ця збірка — сучасний навчальний переказ популярної символіки, без містичних обіцянок: сон найчастіше говорить про почуття й стан сновидця.",
    "origin_country": "Україна",
    "approx_year": 2026,
    "translations": {
        "ru": {
            "name": "Сонник",
            "description": f"Учебный сонник: {len(ROWS)} символов сновидений простыми словами по всей азбуке — от «Автобуса» до «Ящерицы». Короткое значение, ключевые слова и перевод на трёх языках — чтобы легко вспомнить сон и увидеть, о чём говорит подсознание.",
            "history": "Толкование снов — древняя практика многих культур: от храмовых сонников античности до психологии XX века. Эта подборка — современный учебный пересказ популярной символики, без мистических обещаний: сон чаще всего говорит о чувствах и состоянии сновидца.",
        },
        "en": {
            "name": "Dream Dictionary",
            "description": f"Educational dream dictionary: {len(ROWS)} dream symbols in plain words across the whole alphabet, from 'Bus' to 'Lizard'. A short meaning, keywords and a three-language translation — so it is easy to recall a dream and see what the subconscious is saying.",
            "history": "Dream interpretation is an ancient practice of many cultures: from temple dream books of antiquity to 20th-century psychology. This collection is a modern educational retelling of popular symbolism, without mystical promises: a dream most often speaks about the dreamer's feelings and state.",
        },
    },
}

DECK = {
    "name": "Сонник · символи сновидінь (навчальний)",
    "author": "AI-Arcanum",
    "publisher": "AI-Arcanum",
    "year": 2026,
    "card_count": len(ROWS),
    "description": f"{len(ROWS)} карт-символів сновидінь по всій абетці: вода, вогонь, змія, дім, гроші, політ, погоня тощо. Кожна карта — коротке, добре зрозуміле значення українською з перекладом російською й англійською.",
    "translations": {
        "ru": {
            "name": "Сонник · символы сновидений (учебный)",
            "description": f"{len(ROWS)} карт-символов сновидений по всей азбуке: вода, огонь, змея, дом, деньги, полёт, погоня и другие. Каждая карта — короткое, понятное значение на русском и украинском, плюс английский.",
        },
        "en": {
            "name": "Dream Dictionary · dream symbols (educational)",
            "description": f"{len(ROWS)} dream-symbol cards across the whole alphabet: water, fire, snake, house, money, flying, being chased and more. Each card — a short, clear meaning in English plus Ukrainian and Russian.",
        },
    },
}

CARDS = []
for i, (nuk, nru, nen, emoji, sym, kwuk, kwru, kwen, muk, mru, men) in enumerate(ROWS, start=1):
    CARDS.append({
        "number": str(i),
        "name": nuk,
        "arcana_type": "Символ сну",
        "theme": f"{emoji} {nuk}",
        "keywords_upright": kwuk,
        "meaning_general": muk,
        "symbolism": sym,
        "translations": {
            "ru": {"name": nru, "keywords_upright": kwru, "meaning_general": mru},
            "en": {"name": nen, "keywords_upright": kwen, "meaning_general": men},
        },
    })

DATA = {"system": SYSTEM, "deck": DECK, "cards": CARDS}

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(DATA, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[сонник] карт: {len(CARDS)} -> {OUT}")