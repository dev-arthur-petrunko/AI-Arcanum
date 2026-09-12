from fastapi import APIRouter

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
