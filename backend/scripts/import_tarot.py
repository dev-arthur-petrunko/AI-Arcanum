"""Импорт Таро из content/tarot/*.md|.json в БД. Формат: см. content/tarot/README."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core.database import SessionLocal
from app.models import Card, Deck

def run(path: str, deck_id: int):
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    db = SessionLocal()
    try:
        for item in data:
            db.add(Card(deck_id=deck_id, **item))
        db.commit()
        print(f"Imported {len(data)} cards from {path}")
    finally:
        db.close()

if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]))
