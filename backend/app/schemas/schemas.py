from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LocalizedMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    translations: dict | None = None

    def localized(self, lang: str, *fields: str) -> dict:
        """Return RU base overlaid with translations[lang] for given fields."""
        data = self.model_dump()
        tr = (data.get("translations") or {}).get(lang, {}) if isinstance(data.get("translations"), dict) else {}
        for f in fields:
            if f in tr and tr[f]:
                data[f] = tr[f]
        return data


class SystemOut(LocalizedMixin):
    id: int
    name: str
    category: str | None = None
    description: str | None = None
    history: str | None = None
    origin_country: str | None = None
    approx_year: int | None = None


class DeckOut(LocalizedMixin):
    id: int
    system_id: int | None = None
    name: str
    author: str | None = None
    publisher: str | None = None
    year: int | None = None
    card_count: int | None = None
    cover_image: str | None = None
    description: str | None = None


class CardOut(LocalizedMixin):
    id: int
    deck_id: int | None = None
    number: str | None = None
    name: str
    arcana_type: str | None = None
    suit: str | None = None
    element: str | None = None
    zodiac_sign: str | None = None
    planet: str | None = None
    numerology: int | None = None
    keywords_upright: str | None = None
    keywords_reversed: str | None = None
    meaning_general: str | None = None
    meaning_love: str | None = None
    meaning_career: str | None = None
    meaning_health: str | None = None
    symbolism: str | None = None
    image_path: str | None = None
    model_3d_path: str | None = None


class SpreadOut(LocalizedMixin):
    id: int
    system_id: int | None = None
    name: str | None = None
    positions_count: int | None = None
    description: str | None = None
    diagram_image: str | None = None


class QuizAnswerIn(BaseModel):
    user_id: int = 0
    card_id: int
    correct: bool


class QuizQuestionOut(BaseModel):
    card: CardOut
    choices: list[str]
    answer_index: int | None = None  # only returned in study mode, not in test mode
