import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Card, Deck

DROP_NAMES = [
    "Mystical Shaman Oracle",
    "Спиритический оракул тотемов",
    "Shamanic Oracle (Rockpool)",
    "Cope (оригінальне видання, 88)",
    "OH cards / Persona (оригінальні видання)",
    "Архетипы и Тени (Спеццано, 90)",
    "Thoth Tarot",
    "Astrological Oracle (22, огляд Aeclectic)",
]

BASE = Path(__file__).resolve().parents[1] / "Database"
DROP_DIR_IDS = [17, 18, 19, 20, 21, 22, 25, 26]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for deck_id in DROP_DIR_IDS:
            removed = 0
            for root_dir in (BASE / "images", Path(__file__).resolve().parents[2] / "frontend" / "public" / "assets"):
                p = root_dir / f"ref_{deck_id}"
                if p.exists():
                    shutil.rmtree(p, ignore_errors=True)
                    removed += 1
            print(f"[drop-dirs] ref_{deck_id}: dirs={removed}")
        for name in DROP_NAMES:
            deck = db.query(Deck).filter_by(name=name).first()
            if not deck:
                print(f"[drop] не знайдено: {name}")
                continue
            n_cards = db.query(Card).filter(Card.deck_id == deck.id).delete()
            db.delete(deck)
            db.commit()
            print(f"[drop] видалено: {name} (id={deck.id}, карт={n_cards})")
    finally:
        db.close()


if __name__ == "__main__":
    run()