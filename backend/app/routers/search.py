"""FTS5-пошук картками (SQLite) з LIKE-фолбеком + фільтри.
Таблиця cards_fts перебудовується з cards; тригери тримають її в синхроні.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Card
from ..schemas import CardOut

router = APIRouter(prefix="/search", tags=["search"])
_FTS_READY = False


def ensure_fts(db: Session):
    global _FTS_READY
    if _FTS_READY:
        return
    db.execute(text(
        "CREATE VIRTUAL TABLE IF NOT EXISTS cards_fts USING fts5("
        "name, keywords_upright, keywords_reversed, meaning_general, symbolism, "
        "element, planet, zodiac_sign, suit, content='cards', content_rowid='id')"
    ))
    db.execute(text(
        "CREATE TRIGGER IF NOT EXISTS cards_ai AFTER INSERT ON cards BEGIN "
        "INSERT INTO cards_fts(rowid, name, keywords_upright, keywords_reversed, meaning_general, "
        "symbolism, element, planet, zodiac_sign, suit) VALUES "
        "(new.id, new.name, new.keywords_upright, new.keywords_reversed, new.meaning_general, "
        "new.symbolism, new.element, new.planet, new.zodiac_sign, new.suit); END"
    ))
    db.execute(text("INSERT OR IGNORE INTO cards_fts(cards_fts) VALUES('rebuild')"))
    db.commit()
    _FTS_READY = True


def _matches_translations(card: Card, q: str) -> bool:
    ql = q.lower()
    for lang_block in (card.translations or {}).values():
        if isinstance(lang_block, dict):
            for v in lang_block.values():
                if isinstance(v, str) and ql in v.lower():
                    return True
    return False


@router.get("", response_model=list[CardOut])
def search(
    q: str = Query(..., min_length=2),
    element: str | None = None,
    planet: str | None = None,
    zodiac_sign: str | None = None,
    suit: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    ensure_fts(db)
    ids: list[int] = []
    try:
        rows = db.execute(
            text("SELECT rowid FROM cards_fts WHERE cards_fts MATCH :m LIMIT :lim"),
            {"m": q, "lim": limit * 2},
        ).fetchall()
        ids = [r[0] for r in rows]
    except Exception:
        ids = []
    stmt = select(Card)
    if ids:
        stmt = stmt.where(Card.id.in_(ids))
    else:
        like = f"%{q}%"
        stmt = stmt.where(
            (Card.name.ilike(like)) | (Card.keywords_upright.ilike(like))
            | (Card.keywords_reversed.ilike(like)) | (Card.meaning_general.ilike(like))
            | (Card.symbolism.ilike(like)) | (Card.planet.ilike(like))
            | (Card.zodiac_sign.ilike(like)) | (Card.element.ilike(like))
        )
    if element:
        stmt = stmt.where(Card.element == element)
    if planet:
        stmt = stmt.where(Card.planet == planet)
    if zodiac_sign:
        stmt = stmt.where(Card.zodiac_sign == zodiac_sign)
    if suit:
        stmt = stmt.where(Card.suit == suit)
    base = list(db.scalars(stmt.limit(limit * 2)).all())
    if len(base) < limit:
        extra = db.scalars(select(Card).limit(500)).all()
        seen = {c.id for c in base}
        for c in extra:
            if c.id not in seen and _matches_translations(c, q):
                base.append(c)
            if len(base) >= limit:
                break
    return base[:limit]
