"""check_images.py — звіряє image_path карт із файлами у frontend/public.
Биті шляхи зануляє (фронт покаже процедурний фолбек замість 404).
Запуск з папки backend/: python scripts/check_images.py [--fix]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Card

PUBLIC = Path(__file__).resolve().parents[2] / "frontend" / "public"


def run(fix: bool = False) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ok = broken = 0
        for c in db.query(Card).filter(Card.image_path.isnot(None)).all():
            if (PUBLIC / c.image_path.lstrip("/")).exists():
                ok += 1
            else:
                broken += 1
                if fix:
                    c.image_path = None
        if fix:
            db.commit()
        print(f"[images] ok={ok} broken={broken} {'(занулено)' if fix else '(dry-run)'}")
    finally:
        db.close()


if __name__ == "__main__":
    run("--fix" in sys.argv)
