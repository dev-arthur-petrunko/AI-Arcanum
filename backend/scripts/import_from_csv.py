"""import_from_csv.py — ручний редакторський імпорт (для сучасних джерел).

Процес: прочитати джерело → переписати СВОЇМИ СЛОВАМИ → заповнити CSV →
імпортувати сюди. Масовий скрейпінг авторських сайтів заборонено.

CSV-колонки: deck, number, name, meaning_general[, meaning_love, meaning_career,
keywords_upright, keywords_reversed, symbolism, source_reference, lang]
  - deck: точна назва колоди (має існувати) або "System | Deck" для автостворення.
  - source_reference: обовʼязкове (URL/книга для атрибуції).
  - lang: ru (за замовчуванням, збігається з базовими колонками БД) | uk | en — для uk/en пише в translations, не затираючи базу.

Запуск (из папки backend/):
    python scripts/import_from_csv.py Database/raw/oracles/my_deck.csv --dry-run
    python scripts/import_from_csv.py Database/raw/oracles/my_deck.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Card, Deck, System


def get_or_create_deck(db, spec: str) -> Deck:
    deck = db.query(Deck).filter_by(name=spec).first()
    if deck:
        return deck
    if "|" in spec:
        sys_name, deck_name = [s.strip() for s in spec.split("|", 1)]
        system = db.query(System).filter_by(name=sys_name).first()
        if not system:
            system = System(name=sys_name, category="оракулы")
            db.add(system)
            db.flush()
        deck = Deck(system_id=system.id, name=deck_name, card_count=0)
        db.add(deck)
        db.flush()
        return deck
    raise ValueError(f"Колоди '{spec}' не знайдено (або вкажіть 'Система | Колода')")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    added = updated = 0
    try:
        with open(args.csv_path, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                if not row.get("source_reference"):
                    raise ValueError(f"Немає source_reference у рядку: {row.get('name')}")
                deck = get_or_create_deck(db, row["deck"].strip())
                lang = (row.get("lang") or "ru").strip().lower()
                number = (row.get("number") or "").strip() or None
                card = None
                if number:
                    card = db.query(Card).filter_by(deck_id=deck.id, number=number).first()
                if not card:
                    card = db.query(Card).filter_by(deck_id=deck.id, name=row["name"].strip()).first()
                fields = {k: (row.get(k) or "").strip() or None
                          for k in ("meaning_general", "meaning_love", "meaning_career",
                                    "keywords_upright", "keywords_reversed", "symbolism")}
                if lang == "ru":
                    if not card:
                        card = Card(deck_id=deck.id, number=number, name=row["name"].strip(), **fields)
                        db.add(card)
                        added += 1
                    else:
                        for k, v in fields.items():
                            if v:
                                setattr(card, k, v)
                        updated += 1
                    card.symbolism = ((card.symbolism or "") + f"\nИсточник: {row['source_reference']}").strip()
                else:
                    if not card:
                        raise ValueError(f"Для {lang}-перекладу картка має існувати: {row['name']}")
                    tr = dict(card.translations or {})
                    block = dict(tr.get(lang, {}))
                    block.update({k: v for k, v in fields.items() if v})
                    block["source_reference"] = row["source_reference"]
                    tr[lang] = block
                    card.translations = tr
                    updated += 1
        if args.dry_run:
            db.rollback()
            print(f"[dry-run] було б: added={added} updated={updated}")
        else:
            db.commit()
            print(f"[OK] added={added} updated={updated}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
