from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Deck
from ..schemas import DeckOut

router = APIRouter(prefix="/decks", tags=["decks"])


@router.get("", response_model=list[DeckOut])
def list_decks(system_id: int | None = None, db: Session = Depends(get_db)):
    q = select(Deck)
    if system_id is not None:
        q = q.where(Deck.system_id == system_id)
    return db.scalars(q).all()


@router.get("/{deck_id}", response_model=DeckOut)
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    return db.get(Deck, deck_id)
