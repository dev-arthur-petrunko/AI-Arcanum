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


def _either(col, code_col, value: str | None):
    if not value:
        return None
    return (col == value) | (code_col == value)


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
    conds = [c for c in (_either(Card.suit, Card.suit_code, suit),
                          _either(Card.element, Card.element_code, element),
                          _either(Card.planet, Card.planet_code, planet),
                          _either(Card.zodiac_sign, Card.zodiac_sign_code, zodiac_sign))
             if c is not None]
    base: list[Card] = []
    if ids:
        stmt = select(Card).where(Card.id.in_(ids))
        for cond in conds:
            stmt = stmt.where(cond)
        base = list(db.scalars(stmt.limit(limit * 2)).all())
        # топ-ап з перекладів (FTS індексує базові поля; translations — ні)
        if len(base) < limit:
            seen = {c.id for c in base}
            for c in db.scalars(select(Card)).all():
                if c.id not in seen and _matches_translations(c, q):
                    base.append(c)
                if len(base) >= limit:
                    break
    else:
        # SQLite LIKE/ILIKE не вміє Cyrillic-casefold — скануємо в Python (БД мала)
        needle = q.casefold()
        wants = {"suit": suit, "element": element, "planet": planet, "zodiac_sign": zodiac_sign}
        for c in db.scalars(select(Card)).all():
            hay = " ".join(x for x in (
                c.name, c.keywords_upright, c.keywords_reversed,
                c.meaning_general, c.symbolism, c.planet,
                c.zodiac_sign, c.element) if x).casefold()
            if needle not in hay and not _matches_translations(c, q):
                continue
            ok = True
            for field, want in wants.items():
                if want and want != getattr(c, field) and want != getattr(c, f"{field}_code", None):
                    ok = False
                    break
            if ok:
                base.append(c)
            if len(base) >= limit * 2:
                break
    return base[:limit]
