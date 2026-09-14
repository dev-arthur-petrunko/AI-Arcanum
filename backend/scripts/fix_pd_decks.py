"""fix_pd_decks.py — скидає is_reference_only, оновлює cover_image для колод 23/24."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core.database import SessionLocal, engine, Base
from app.models import Deck

Base.metadata.create_all(bind=engine)
db = SessionLocal()
for did in [23, 24]:
    d = db.query(Deck).filter_by(id=did).first()
    if not d: continue
    d.is_reference_only = False
    d.cover_image = f"/assets/{did}/0.jpg"
    d.source_url = None
    d.buy_url = None
    d.composition = None
    d.gallery = None
    print(f"deck {did} ({d.name}): is_reference_only=0, cover={d.cover_image}, cards={d.card_count}")
db.commit()
db.close()
print("OK")
