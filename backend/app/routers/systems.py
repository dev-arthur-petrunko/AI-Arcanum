from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import System
from ..schemas import SystemOut

router = APIRouter(prefix="/systems", tags=["systems"])


@router.get("", response_model=list[SystemOut])
def list_systems(db: Session = Depends(get_db)):
    return db.scalars(select(System)).all()
