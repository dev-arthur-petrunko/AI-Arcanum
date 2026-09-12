from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Article
from ..schemas import ArticleOut

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=list[ArticleOut])
def list_articles(system: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Article).order_by(Article.id)
    if system:
        stmt = stmt.where(Article.system == system)
    return db.scalars(stmt).all()


@router.get("/{slug}", response_model=ArticleOut)
def get_article(slug: str, db: Session = Depends(get_db)):
    return db.scalar(select(Article).where(Article.slug == slug))
