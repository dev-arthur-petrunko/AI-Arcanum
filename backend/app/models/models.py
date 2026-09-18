"""Моделі SQLAlchemy. Базові поля + `translations` JSON {uk: {...}, en: {...}, ru: {...}} для тримовного UI."""
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core.database import Base


class System(Base):
    __tablename__ = "systems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)  # базова мова (сідовано RU); переклади — у translations
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    history: Mapped[str | None] = mapped_column(Text, nullable=True)
    origin_country: Mapped[str | None] = mapped_column(String(128), nullable=True)
    approx_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    translations: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    decks: Mapped[list["Deck"]] = relationship(back_populates="system", cascade="all, delete-orphan")


class Deck(Base):
    __tablename__ = "decks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    system_id: Mapped[int | None] = mapped_column(ForeignKey("systems.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    author: Mapped[str | None] = mapped_column(String(256), nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(256), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    card_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    translations: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # Довідковий профіль реального видання (без повного набору карт в БД)
    is_reference_only: Mapped[bool] = mapped_column(default=False)
    # Умовна/часткова колода: БД містить не повний еталонний набір (наприклад, 36 із 360 сабіанських символів)
    is_partial: Mapped[bool] = mapped_column(default=False)
    # Розділ-«конструктор» системи (наприклад, Багуа як будівельний блок І-Цзин):
    # не показується на вітрині напрямку як самостійна колода, але лишається в БД
    is_shown_in_directory: Mapped[bool] = mapped_column(default=True)
    # Необов'язкова назва групи для вітрини напрямку (наприклад, «Руни та Огам»):
    # колоди з однаковим значенням виводяться під спільним підзаголовком
    directory_group: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # Дочірня/будівельна колода цієї колоди (наприклад, І-Цзин → Багуа):
    # картки цієї колоди показуються окремим блоком на сторінці «батьківської»
    related_deck_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    buy_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    composition: Mapped[str | None] = mapped_column(Text, nullable=True)
    gallery: Mapped[list | None] = mapped_column(JSON, nullable=True)  # превʼю видання (не карти БД)

    system: Mapped[System | None] = relationship(back_populates="decks")
    cards: Mapped[list["Card"]] = relationship(back_populates="deck", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deck_id: Mapped[int | None] = mapped_column(ForeignKey("decks.id"), nullable=True)
    number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    arcana_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    suit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    element: Mapped[str | None] = mapped_column(String(64), nullable=True)
    zodiac_sign: Mapped[str | None] = mapped_column(String(64), nullable=True)
    planet: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Мовно-незалежні коди для фільтрів (UI шле коди, БД не залежить від мови відображення)
    suit_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    element_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    zodiac_sign_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    planet_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    # Терапевтичні колоди (COPE): категорія методики + тема (див. BASIC Ph)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    theme: Mapped[str | None] = mapped_column(Text, nullable=True)
    numerology: Mapped[int | None] = mapped_column(Integer, nullable=True)
    keywords_upright: Mapped[str | None] = mapped_column(Text, nullable=True)
    keywords_reversed: Mapped[str | None] = mapped_column(Text, nullable=True)
    meaning_general: Mapped[str | None] = mapped_column(Text, nullable=True)
    meaning_love: Mapped[str | None] = mapped_column(Text, nullable=True)
    meaning_career: Mapped[str | None] = mapped_column(Text, nullable=True)
    meaning_health: Mapped[str | None] = mapped_column(Text, nullable=True)
    meaning_spirituality: Mapped[str | None] = mapped_column(Text, nullable=True)
    meaning_reversed: Mapped[str | None] = mapped_column(Text, nullable=True)
    symbolism: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    model_3d_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    translations: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    deck: Mapped[Deck | None] = relationship(back_populates="cards")


class CardCorrespondence(Base):
    __tablename__ = "card_correspondences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    card_id_a: Mapped[int | None] = mapped_column(ForeignKey("cards.id"), nullable=True)
    card_id_b: Mapped[int | None] = mapped_column(ForeignKey("cards.id"), nullable=True)
    relation_type: Mapped[str | None] = mapped_column(String(64), nullable=True)


class Spread(Base):
    __tablename__ = "spreads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    system_id: Mapped[int | None] = mapped_column(ForeignKey("systems.id"), nullable=True)
    name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    positions_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    diagram_image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    translations: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    positions: Mapped[list["SpreadPosition"]] = relationship(back_populates="spread", cascade="all, delete-orphan")


class SpreadPosition(Base):
    __tablename__ = "spread_positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    spread_id: Mapped[int | None] = mapped_column(ForeignKey("spreads.id"), nullable=True)
    position_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    position_meaning: Mapped[str | None] = mapped_column(Text, nullable=True)

    spread: Mapped[Spread | None] = relationship(back_populates="positions")


class QuizProgress(Base):
    __tablename__ = "quiz_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    card_id: Mapped[int | None] = mapped_column(ForeignKey("cards.id"), nullable=True)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    last_reviewed: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class Article(Base):
    """Стаття енциклопедії (markdown з Database/articles/, front-matter → колонки)."""

    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    system: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lang: Mapped[str] = mapped_column(String(8), default="ru")
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    translations: Mapped[dict | None] = mapped_column(JSON, nullable=True)
