# -*- coding: utf-8 -*-
"""import_rws_deep.py — глубокая проработка 78 карт RWS.

RU — в колонки cards (meaning_reversed, meaning_love, meaning_career,
meaning_health, meaning_spirituality); uk/en — в translations JSON.
Идемпотентный: только дозаполнение пустых/замена заполненных при --overwrite.
Запуск из папки backend/: python scripts/import_rws_deep.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.models import Card, Deck

from rws_deep.majors import MAJORS
from rws_deep.wands import WANDS
from rws_deep.cups import CUPS
from rws_deep.swords import SWORDS
from rws_deep.pents import PENTACLES

DATA = {**MAJORS, **WANDS, **CUPS, **SWORDS, **PENTACLES}
COLUMNS = ("reversed", "love", "career", "health", "spirituality")
MAP = {"reversed": "meaning_reversed", "love": "meaning_love", "career": "meaning_career",
       "health": "meaning_health", "spirituality": "meaning_spirituality"}


def run(overwrite: bool = False) -> int:
    db = SessionLocal()
    n = 0
    try:
        deck = db.query(Deck).filter(Deck.name.ilike("%Уэйта%") | Deck.name.ilike("%Waite%")).first()
        if not deck:
            deck = db.query(Deck).filter_by(id=1).first()
        print(f"[rws_deep] deck: id={deck.id} name={deck.name}")
        cards = {c.number: c for c in db.query(Card).filter(Card.deck_id == deck.id).all()}
        for number, langs in DATA.items():
            card = cards.get(number)
            if not card:
                print(f"[rws_deep] !! не найдена карта number={number}")
                continue
            ru = langs["ru"]
            changed = False
            for short, col in MAP.items():
                val = ru[short]
                if val and (overwrite or not (getattr(card, col) or "").strip()):
                    setattr(card, col, val)
                    changed = True
            tr = dict(card.translations or {})
            for lg in ("uk", "en"):
                block = dict(tr.get(lg) or {})
                for short in COLUMNS:
                    val = langs[lg][short]
                    if val and (overwrite or not (block.get(MAP[short]) or "").strip()):
                        block[MAP[short]] = val
                if block:
                    tr[lg] = block
            cur = card.translations or {}
            if tr != cur:
                card.translations = tr
                changed = True
            if changed:
                n += 1
        db.commit()
        print(f"[rws_deep] обновлено карт: {n}/78")
        return n
    finally:
        db.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Глубокая проработка значений RWS")
    ap.add_argument("--overwrite", action="store_true",
                    help="перезаписать уже заполненные поля (по умолчанию только пустые)")
    args = ap.parse_args()
    run(overwrite=args.overwrite)