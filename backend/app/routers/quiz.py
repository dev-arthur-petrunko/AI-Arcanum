import random
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Card, QuizProgress
from ..schemas import CardOut, QuizAnswerIn

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/question", response_model=dict)
def quiz_question(deck_id: int | None = None, choices: int = 4, db: Session = Depends(get_db)):
    stmt = select(Card)
    if deck_id is not None:
        stmt = stmt.where(Card.deck_id == deck_id)
    cards = db.scalars(stmt).all()
    if len(cards) < choices:
        return {"detail": "not enough cards"}
    card = random.choice(cards)
    others = random.sample([c for c in cards if c.id != card.id], choices - 1)
    options = others + [card]
    random.shuffle(options)
    return {
        "card_id": card.id,
        "prompt": "Что означает эта карта в прямом положении?",
        "image_path": card.image_path,
        "choices": [{"id": c.id, "name": c.name} for c in options],
        # correct hidden in real test mode; returned here for study mode simplicity
        "answer_id": card.id,
        "hint": (card.keywords_upright or "")[:120],
    }


@router.post("/answer")
def quiz_answer(payload: QuizAnswerIn, db: Session = Depends(get_db)):
    row = db.scalar(select(QuizProgress).where(QuizProgress.user_id == payload.user_id, QuizProgress.card_id == payload.card_id))
    if row is None:
        row = QuizProgress(user_id=payload.user_id, card_id=payload.card_id, correct_count=0)
        db.add(row)
    if payload.correct:
        row.correct_count += 1
    row.last_reviewed = datetime.now(timezone.utc)
    db.commit()
    return {"ok": True, "correct_count": row.correct_count}
