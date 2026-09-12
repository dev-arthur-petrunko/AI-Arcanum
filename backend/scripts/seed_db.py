"""Seed: systems + колода RWS (78 карт) + базові розклади. UK-база + RU/EN у translations.
Запуск: python scripts/seed_db.py  (з папки backend/)
Джерела значень: суспільне надбання (Waite 1911, переказ) + власні формулювання.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Card, Deck, Spread, SpreadPosition, System

MAJOR = [
    ("0", "Шут", "Дурень", "The Fool", "Воздух", "Уран", None, "новые начинания, спонтанность, доверие", "безрассудство, риск, легкомыслие"),
    ("I", "Маг", "Маг", "The Magician", "Воздух", "Меркурий", None, "воля, мастерство, концентрация", "манипуляция, нерешительность"),
    ("II", "Верховная Жрица", "Верховна Жриця", "The High Priestess", "Вода", "Луна", None, "интуиция, тайна, внутреннее знание", "подавленная интуиция, скрытые мотивы"),
    ("III", "Императрица", "Імператриця", "The Empress", "Земля", "Венера", None, "изобилие, забота, природа", "зависимость, творческий блок"),
    ("IV", "Император", "Імператор", "The Emperor", "Огонь", "Овен", "Овен", "структура, власть, стабильность", "ригидность, контроль"),
    ("V", "Иерофант", "Ієрофант", "The Hierophant", "Земля", "Венера", "Телец", "традиция, наставничество, вера", "догматизм, бунт против правил"),
    ("VI", "Влюблённые", "Закохані", "The Lovers", "Воздух", "Меркурий", "Близнецы", "выбор сердцем, союз, гармония", "дисгармония, неверный выбор"),
    ("VII", "Колесница", "Колісниця", "The Chariot", "Вода", "Луна", "Рак", "движение, победа, самоконтроль", "потеря направления, агрессия"),
    ("VIII", "Сила", "Сила", "Strength", "Огонь", "Солнце", "Лев", "мужество, терпение, мягкая сила", "сомнения, выгорание"),
    ("IX", "Отшельник", "Відлюдник", "The Hermit", "Земля", "Меркурий", "Дева", "поиск, мудрость, уединение", "изоляция, застой"),
    ("X", "Колесо Фортуны", "Колесо Фортуни", "Wheel of Fortune", "Огонь", "Юпитер", None, "перемены, цикл, удача", "неудачный период, сопротивление переменам"),
    ("XI", "Справедливость", "Справедливість", "Justice", "Воздух", "Венера", "Весы", "честность, баланс, ответственность", "несправедливость, предвзятость"),
    ("XII", "Повешенный", "Повішений", "The Hanged Man", "Вода", "Нептун", None, "пауза, смена视角, жертва ради прозрения", "застревание, бессмысленная жертва"),
    ("XIII", "Смерть", "Смерть", "Death", "Вода", "Плутон", "Скорпион", "трансформация, завершение, обновление", "сопротивление концу, застой"),
    ("XIV", "Умеренность", "Помірність", "Temperance", "Огонь", "Солнце", "Стрелец", "баланс, алхимия, умеренность", "крайности, дисбаланс"),
    ("XV", "Дьявол", "Диявол", "The Devil", "Земля", "Сатурн", "Козерог", "привязанность, тень, искушение", "освобождение, разрыв цепей"),
    ("XVI", "Башня", "Вежа", "The Tower", "Огонь", "Марс", None, "внезапные перемены, прозрение, разрушение иллюзий", "затяжной кризис, страх перемен"),
    ("XVII", "Звезда", "Зірка", "The Star", "Воздух", "Венера", "Водолей", "надежда, вдохновение, исцеление", "потеря веры, уныние"),
    ("XVIII", "Луна", "Місяць", "The Moon", "Вода", "Луна", "Рыбы", "иллюзии, сны, подсознание", "прояснение, выход из тумана"),
    ("XIX", "Солнце", "Сонце", "The Sun", "Огонь", "Солнце", None, "радость, ясность, успех", "временное затмение, переоценённый оптимизм"),
    ("XX", "Суд", "Суд", "Judgement", "Огонь", "Плутон", None, "пробуждение, прощение, призвание", "самобичевание, упущенный зов"),
    ("XXI", "Мир", "Світ", "The World", "Земля", "Сатурн", None, "завершение цикла, целостность, триумф", "незавершённость, фрагментарность"),
]

SUITS = [
    ("Жезлы", "Wands", "Жезли", "Огонь"),
    ("Кубки", "Cups", "Кубки", "Вода"),
    ("Мечи", "Swords", "Мечі", "Воздух"),
    ("Пентакли", "Pentacles", "Пентаклі", "Земля"),
]
RANKS = ["Туз", "Двойка", "Тройка", "Четвёрка", "Пятёрка", "Шестёрка", "Семёрка", "Восьмёрка", "Девятка", "Десятка", "Паж", "Рыцарь", "Королева", "Король"]
RANKS_UK = ["Туз", "Двійка", "Трійка", "Четвірка", "П'ятірка", "Шістка", "Сімка", "Вісімка", "Дев'ятка", "Десятка", "Паж", "Лицар", "Королева", "Король"]
RANKS_EN = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King"]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(System).count():
            print("Already seeded, skip. Use --reseed to refill. (Вже засідовано, пропуск.)")
            return
        tarot = System(
            name="Таро",
            category="гадательные",
            description="Символическая система из 78 карт: 22 Старших и 56 Младших арканов. Учебный эталон энциклопедии.",
            history="Происходит от игральных карт Европы XV века; оккультная традиция — с XVIII в. (Кур де Жебелен, Эттейла, Папюс, Уэйт).",
            origin_country="Италия / Франция",
            approx_year=1440,
            translations={
                "uk": {"name": "Таро", "description": "Символічна система з 78 карт: 22 Старші та 56 Молодших арканів.",
                       "history": "Походить від європейських гральних карт XV ст.; окультна традиція — з XVIII ст."},
                "en": {"name": "Tarot", "description": "A symbolic 78-card system: 22 Major and 56 Minor Arcana.",
                       "history": "Evolved from 15th-century European playing cards; occult tradition since the 18th century."},
            },
        )
        db.add(tarot)
        db.flush()

        lenormand = System(
            name="Ленорман",
            category="гадательные",
            description="36 карт с бытовыми символами (Клевер, Корабль, Дом). Практика комбинаций пар/триад.",
            history="Малая колода 'Petit Lenormand' (ок. 1799), названа в честь Марии Ленорман.",
            origin_country="Германия / Франция",
            approx_year=1799,
            translations={
                "uk": {"name": "Ленорман", "description": "36 карт із побутовими символами. Практика комбінацій пар/тріад."},
                "en": {"name": "Lenormand", "description": "36 cards with everyday symbols. Read in pairs/triads."},
            },
        )
        db.add(lenormand)
        db.flush()

        rws = Deck(
            system_id=tarot.id,
            name="Таро Уэйта-Смит",
            author="А. Э. Уэйт / П. Колман-Смит",
            publisher="Rider Company (1909, общественное достояние)",
            year=1909,
            card_count=78,
            cover_image="/assets/card_images/rws/cover.jpg",
            description="Классическая колода — эталон значений. Изображения 1909 г. в общественном достоянии.",
            translations={
                "uk": {"name": "Таро Вейта-Сміт", "description": "Класична колода — еталон значень."},
                "en": {"name": "Rider-Waite-Smith Tarot", "description": "Classic public-domain deck (1909), our reference deck."},
            },
        )
        db.add(rws)
        db.flush()

        # --- Старші аркани ---
        for number, ru, uk, en, element, planet, zodiac, kw_up, kw_rev in MAJOR:
            db.add(Card(
                deck_id=rws.id, number=number, name=ru, arcana_type="Старший аркан",
                element=element, planet=planet, zodiac_sign=zodiac,
                keywords_upright=kw_up, keywords_reversed=kw_rev,
                meaning_general=f"{ru}: учебное значение (пересказ по Уэйту, 1911). Прямо — {kw_up}. Перевёрнуто — {kw_rev}.",
                meaning_love=f"Любовь: {kw_up}.", meaning_career=f"Карьера: {kw_up}.", meaning_health=f"Самочувствие: умеренность и внимание к сигналам.",
                symbolism="Символика RWS разбирается по изображению (цвета, жесты, фон) — поле для расширения.",
                image_path=f"/assets/card_images/rws/major_{number}.jpg",
                translations={"uk": {"name": uk}, "en": {"name": en}},
            ))

        # --- Молодші аркани (програмно, навчальні заготовки) ---
        for suit_ru, suit_en, suit_uk, element in SUITS:
            for i, (rank_ru, rank_uk, rank_en) in enumerate(zip(RANKS, RANKS_UK, RANKS_EN)):
                numerology = 1 if i == 0 else (i + 1 if i < 10 else None)
                name_ru = f"{rank_ru} {suit_ru.lower()}" if suit_ru != "Жезлы" else f"{rank_ru} жезлов"
                # нормалізація назв
                suit_gen = {"Жезлы": "жезлов", "Кубки": "кубков", "Мечи": "мечей", "Пентакли": "пентаклей"}[suit_ru]
                name_ru = f"{rank_ru} {suit_gen}"
                db.add(Card(
                    deck_id=rws.id, number=f"{suit_en}-{i+1:02d}", name=name_ru,
                    arcana_type="Младший аркан", suit=suit_ru, element=element, numerology=numerology,
                    keywords_upright=f"учебное значение {name_ru} (прямо)",
                    keywords_reversed=f"учебное значение {name_ru} (перевёрнуто)",
                    meaning_general=f"{name_ru}: младший аркан, масть {suit_ru} (стихия {element}). Базовая трактовка для заучивания; детализируйте по изображению RWS.",
                    symbolism=f"Масть {suit_ru} ↔ стихия {element}.",
                    image_path=f"/assets/card_images/rws/{suit_en.lower()}_{i+1:02d}.jpg",
                    translations={"uk": {"name": f"{rank_uk} {suit_uk.lower()}"}, "en": {"name": f"{rank_en} of {suit_en}"}},
                ))

        # --- Розклади ---
        s1 = Spread(system_id=tarot.id, name="Три карты", positions_count=3,
                    description="Прошлое — настоящее — будущее. Базовый учебный расклад.",
                    translations={"uk": {"name": "Три карти"}, "en": {"name": "Three Cards"}})
        db.add(s1)
        db.flush()
        for n, m in [(1, "Прошлое / контекст"), (2, "Настоящее / суть"), (3, "Будущее / тенденция")]:
            db.add(SpreadPosition(spread_id=s1.id, position_number=n, position_meaning=m))

        s2 = Spread(system_id=tarot.id, name="Кельтский крест", positions_count=10,
                    description="Классический большой расклад для глубокого разбора.",
                    translations={"uk": {"name": "Кельтський хрест"}, "en": {"name": "Celtic Cross"}})
        db.add(s2)
        db.flush()
        meanings = ["Суть вопроса", "Вызов/преграда", "Основа/прошлое", "Уходящее", "Венец/цель",
                    "Ближайшее будущее", "Позиция кверента", "Окружение", "Надежды/страхи", "Итог"]
        for n, m in enumerate(meanings, 1):
            db.add(SpreadPosition(spread_id=s2.id, position_number=n, position_meaning=m))

        db.commit()
        print(f"Засідовано: systems={db.query(System).count()} decks={db.query(Deck).count()} cards={db.query(Card).count()}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys as _s
    if "--reseed" in _s.argv:
        Base.metadata.drop_all(bind=engine)
    seed()
