"""Страж цілісності БД: жоден скрипт не має права мовчки зменшити колекцію.
Запуск з папки backend/: pytest tests/ -q
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.models import Card, Deck, System

# system_name: мінімально допустима кількість карт (зростає разом із проєктом)
EXPECTED_MIN = {
    "Таро": 78,
    "Ленорман": 36,
    "І-Цзин": 64,
    "Руни": 53,
    "Оракули": 8,
    "МАК": 20,
    "Астрологічні колоди": 26,
    "Шаманські карти": 12,
    "Циганські карти": 36,
    "Гральні карти": 36,
    "Цолькин": 33,
    "Карти предків": 12,
    "Нумерологія": 12,
}


def _counts():
    db = SessionLocal()
    try:
        out = {}
        for s in db.query(System).all():
            deck_ids = [d.id for d in db.query(Deck).filter_by(system_id=s.id).all()]
            n = db.query(Card).filter(Card.deck_id.in_(deck_ids)).count() if deck_ids else 0
            out[s.name] = n
        return out
    finally:
        db.close()


def test_no_system_lost_cards():
    counts = _counts()
    for name, minimum in EXPECTED_MIN.items():
        assert name in counts, f"зникла система: {name}"
        assert counts[name] >= minimum, f"{name}: {counts[name]} < {minimum} — колода втрачена?"


def test_total_grows_only():
    counts = _counts()
    assert sum(counts.values()) >= sum(EXPECTED_MIN.values())
