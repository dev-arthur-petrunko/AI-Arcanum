from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Spread, SpreadPosition
from ..schemas import SpreadOut

router = APIRouter(prefix="/spreads", tags=["spreads"])


@router.get("", response_model=list[SpreadOut])
def list_spreads(db: Session = Depends(get_db)):
    return db.scalars(select(Spread)).all()


@router.get("/{spread_id}")
def get_spread(spread_id: int, db: Session = Depends(get_db)):
    spread = db.get(Spread, spread_id)
    positions = db.scalars(select(SpreadPosition).where(SpreadPosition.spread_id == spread_id).order_by(SpreadPosition.position_number)).all()
    return {
        "spread": SpreadOut.model_validate(spread).model_dump() if spread else None,
        "positions": [{"position_number": p.position_number, "position_meaning": p.position_meaning} for p in positions],
    }
