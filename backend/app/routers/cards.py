import random
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Card
from ..schemas import CardOut

router = APIRouter(prefix="/cards", tags=["cards"])


LOCALIZABLE = ("name", "keywords_upright", "keywords_reversed", "meaning_general",
                 "meaning_love", "meaning_career", "meaning_health", "symbolism")


def _either(col, code_col, value: str | None):
    """Фільтр приймає і код (fire), і текст (Огонь/Вогонь) — для зворотної сумісності."""
    if not value:
        return None
    return (col == value) | (code_col == value)


def localize(card: Card, lang: str | None) -> Card:
    """Накладає translations[lang] поверх базових полів для видачі (?lang=uk|ru|en)."""
    if not lang or lang not in ("uk", "ru", "en"):
        return card
    block = (card.translations or {}).get(lang, {})
    for f in LOCALIZABLE:
        if block.get(f):
            setattr(card, f, block[f])
    return card


@router.get("", response_model=list[CardOut])
def list_cards(
    deck_id: int | None = None,
    arcana_type: str | None = None,
    suit: str | None = None,
    element: str | None = None,
    planet: str | None = None,
    zodiac_sign: str | None = None,
    q: str | None = None,
    lang: str | None = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    stmt = select(Card)
    if deck_id is not None:
        stmt = stmt.where(Card.deck_id == deck_id)
    if arcana_type:
        stmt = stmt.where(Card.arcana_type == arcana_type)
    for cond in (_either(Card.suit, Card.suit_code, suit),
                 _either(Card.element, Card.element_code, element),
                 _either(Card.planet, Card.planet_code, planet),
                 _either(Card.zodiac_sign, Card.zodiac_sign_code, zodiac_sign)):
        if cond is not None:
            stmt = stmt.where(cond)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            (Card.name.ilike(like))
            | (Card.keywords_upright.ilike(like))
            | (Card.meaning_general.ilike(like))
            | (Card.symbolism.ilike(like))
        )
    stmt = stmt.offset(offset).limit(limit)
    return [localize(c, lang) for c in db.scalars(stmt).all()]


@router.get("/random", response_model=CardOut)
def random_card(deck_id: int | None = None, db: Session = Depends(get_db)):
    """Випадкова карта (для «Мені пощастить»); deck_id звужує до колоди."""
    stmt = select(Card)
    if deck_id is not None:
        stmt = stmt.where(Card.deck_id == deck_id)
    ids = db.scalars(stmt.with_only_columns(Card.id)).all()
    if not ids:
        return None
    return db.get(Card, random.choice(ids))


@router.get("/daily", response_model=CardOut)
def card_of_day(deck_id: int | None = None, lang: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Card)
    if deck_id is not None:
        stmt = stmt.where(Card.deck_id == deck_id)
    cards = db.scalars(stmt).all()
    if not cards:
        return None
    # детерміновано за датою, щоб «карта дня» не змінювалась протягом доби
    import datetime
    seed = int(datetime.date.today().strftime("%Y%m%d"))
    return localize(random.Random(seed).choice(cards), lang)


@router.get("/{card_id}", response_model=CardOut)
def get_card(card_id: int, lang: str | None = None, db: Session = Depends(get_db)):
    card = db.get(Card, card_id)
    return localize(card, lang) if card else None
