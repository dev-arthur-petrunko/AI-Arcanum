"""Аудит повноти колод: еталонні списки номерів, пропуски, дублі, картинки.
Запуск з папки backend/: pytest tests/test_deck_completeness.py -q
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.models import Card, Deck

ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]
MINORS = [f"{s}-{i:02d}" for s in ("Wands", "Cups", "Swords", "Pentacles") for i in range(1, 15)]
PLAY = [f"{s}-{r}" for s in ("H", "D", "C", "S") for r in ("A", "K", "Q", "J", "10", "9", "8", "7", "6")]

EXPECTED = {
    "Таро Уэйта-Смит": ROMAN + MINORS,
    "Petit Lenormand (учебная)": [str(i) for i in range(1, 37)],
    "И-Цзин (Легг, 1899)": [str(i) for i in range(1, 65)],
    "Англосаксонская руническая поэма": [str(i) for i in range(1, 30)],
    "Старший Футарк (навчальний)": [str(i) for i in range(1, 25)],
    "Оракул місячних фаз (навчальний)": [str(i) for i in range(1, 9)],
    "Астрологічний оракул (навчальний)": [str(i) for i in range(1, 27)],
    "Шаманський оракул тотемів (навчальний)": [str(i) for i in range(1, 13)],
    "Циганські карти (навчальні)": [str(i) for i in range(1, 37)],
    "Гральні карти 36 (навчальні)": PLAY,
    "Цолькин (навчальний)": [f"S{i:02d}" for i in range(1, 21)] + [f"T{i:02d}" for i in range(1, 14)],
    "Нумерологія (навчальна)": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "22", "33"],
    "Терапевтична колода 85 · Сили, канали, потреби (навчальна)": (
        [str(i) for i in range(1, 25)]  # VIA 24
        + [f"{l}{n}" for l in "BASICP" for n in range(1, 7)]  # BASIC Ph 36
        + [f"M{i}" for i in range(1, 26)]  # Маслоу 25
    ),
}

def _snapshot():
    db = SessionLocal()
    try:
        snap = {}
        for deck_name, exp in EXPECTED.items():
            deck = db.query(Deck).filter_by(name=deck_name).first()
            cards = db.query(Card).filter_by(deck_id=deck.id).all() if deck else []
            got = [c.number for c in cards]
            snap[deck_name] = {
                "deck": deck, "exp": exp, "cards": cards, "got": got,
                "dupes": [k for k, v in Counter(got).items() if v > 1],
                "missing": [n for n in exp if n not in got],
                "extra": [n for n in got if n not in exp],
                "noname": sum(1 for c in cards if not (c.name or "").strip()),
                "noimg": sum(1 for c in cards if not c.image_path),
            }
        total = db.query(Card).count()
        return snap, total
    finally:
        db.close()


def test_all_decks_present_and_complete():
    snap, _ = _snapshot()
    for name, s in snap.items():
        assert s["deck"] is not None, f"нема колоди: {name}"
        assert len(s["cards"]) == len(s["exp"]), f"{name}: {len(s['cards'])} != {len(s['exp'])}"
        assert not s["missing"], f"{name}: пропуски {s['missing']}"
        assert not s["dupes"], f"{name}: дублі {s['dupes']}"
        assert not s["extra"], f"{name}: зайві {s['extra']}"


def test_all_cards_named_and_illustrated():
    snap, _ = _snapshot()
    for name, s in snap.items():
        assert s["noname"] == 0, f"{name}: без назви {s['noname']}"
        assert s["noimg"] == 0, f"{name}: без картинки {s['noimg']}"


def test_total():
    """Сума карт у БД = сума карт по всіх колодах (консистентність каскадів)."""
    _, total = _snapshot()
    db = SessionLocal()
    try:
        rows = db.query(Deck.id, Card.id)\
            .outerjoin(Card, Card.deck_id == Deck.id).all()
        orphan = sum(1 for _, cid in rows if cid is None)
        sum_cards = db.query(Card).count()
    finally:
        db.close()
    assert total == sum_cards
    assert orphan == 0, f"колод без карт (сиріт): {orphan}"
