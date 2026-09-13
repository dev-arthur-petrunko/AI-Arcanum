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
    if suit:
        stmt = stmt.where(Card.suit == suit)
    if element:
        stmt = stmt.where(Card.element == element)
    if planet:
        stmt = stmt.where(Card.planet == planet)
    if zodiac_sign:
        stmt = stmt.where(Card.zodiac_sign == zodiac_sign)
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
