from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Card, Deck, System

router = APIRouter(tags=["reference"])

GLOSSARY = [
    {"term": {"ru": "Аркан", "uk": "Аркан", "en": "Arcana"}, "definition": {"ru": "Тайна/ключевая карта Таро (Старшие — 22, Младшие — 56).", "uk": "Таємниця/ключова карта Таро.", "en": "A core Tarot mystery/card."}},
    {"term": {"ru": "Масть", "uk": "Масть", "en": "Suit"}, "definition": {"ru": "Группа Младших арканов: Жезлы, Кубки, Мечи, Пентакли.", "uk": "Група Молодших арканів.", "en": "Minor Arcana group."}},
    {"term": {"ru": "Реверс", "uk": "Реверс", "en": "Reversal"}, "definition": {"ru": "Перевёрнутое положение: ослабление/тень значения.", "uk": "Перевернуте положення.", "en": "Upside-down: weakened/shadow meaning."}},
    {"term": {"ru": "Оракул", "uk": "Оракул", "en": "Oracle"}, "definition": {"ru": "Свободная колода без жёсткой структуры (в отличие от Таро).", "uk": "Вільна колода без жорсткої структури.", "en": "Free-form deck, no fixed structure."}},
    {"term": {"ru": "Кверент", "uk": "Кверент", "en": "Querent"}, "definition": {"ru": "Тот, для кого делают расклад (учебный).", "uk": "Той, для кого роблять розклад.", "en": "Person a (study) reading is for."}},
]

TIMELINE = [
    {"year": 1440, "ru": "Игральные карты Италии (предки Таро)", "uk": "Гральні карти Італії", "en": "Italian playing cards"},
    {"year": 1781, "ru": "Кур де Жебелен связывает Таро с Египтом", "uk": "Кур де Жебелен пов'язує Таро з Єгиптом", "en": "Court de Gébelin links Tarot to Egypt"},
    {"year": 1799, "ru": "Petit Lenormand", "uk": "Petit Lenormand", "en": "Petit Lenormand"},
    {"year": 1909, "ru": "Колода Уэйта-Смит (public domain)", "uk": "Колода Вейта-Сміт", "en": "Rider-Waite-Smith deck"},
]


@router.get("/glossary")
def glossary():
    return GLOSSARY


@router.get("/timeline")
def timeline():
    return TIMELINE


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    """Живі лічильники для hero-секції фронтенду + розбивка по системах."""
    systems = []
    deck_rows = []
    for s in db.scalars(select(System).order_by(System.id)).all():
        decks = db.scalars(select(Deck).where(Deck.system_id == s.id)).all()
        deck_ids = [d.id for d in decks]
        n_cards = db.scalar(select(func.count()).select_from(Card).where(Card.deck_id.in_(deck_ids))) if deck_ids else 0
        nm = s.translations.get("uk", {}).get("name") if isinstance(s.translations, dict) else None
        for d in decks:
            dn = d.translations.get("uk", {}).get("name") if isinstance(d.translations, dict) else None
            dd = d.translations.get("uk", {}).get("description") if isinstance(d.translations, dict) else None
            first = db.scalar(select(Card.image_path).where(Card.deck_id == d.id).order_by(Card.id).limit(1))
            deck_rows.append({"id": d.id, "system_id": s.id, "name": dn or d.name,
                              "system": nm or s.name, "cover": first or d.cover_image,
                              "author": d.author, "publisher": d.publisher, "year": d.year,
                              "description": dd or d.description,
                              "is_reference_only": bool(d.is_reference_only),
                              "source_url": d.source_url, "buy_url": d.buy_url,
                              "composition": d.composition, "gallery": d.gallery or [],
                              "cards": db.scalar(select(func.count()).select_from(Card).where(Card.deck_id == d.id))})
        systems.append({"id": s.id, "name": nm or s.name, "category": s.category,
                        "decks": len(deck_ids), "cards": n_cards})
    return {
        "systems": len(systems),
        "decks": db.scalar(select(func.count()).select_from(Deck)),
        "cards": db.scalar(select(func.count()).select_from(Card)),
        "by_system": systems,
        "by_deck": deck_rows,
    }
