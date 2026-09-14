"""seed_deck_profiles.py — довідкові профілі РЕАЛЬНИХ видань (без повного набору карт).
Метадані й посилання — лише з перевірених джерел користувача; тексти — власні.
Ідемпотентний (за name). Запуск з папки backend/: python scripts/seed_deck_profiles.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Deck, System

PROFILES = [
    {
        "system": "Шаманські карти", "name": "Mystical Shaman Oracle",
        "author": "Альберто Вільольдо, Колетт Барон-Рід, Марсела Лобос", "publisher": "Hay House",
        "year": 2018, "card_count": 64,
        "description": "Довідковий профіль реального видання: 64 карти шаманської традиції "
                       "(Eagle, Jaguar, Medicine Wheel, Serpent, Coyote та ін.) + гайдбук. "
                       "Повного набору карт у БД нема — лише метадані.",
        "composition": "64 карти + книга-гайд (премʼєра 2018, ISBN 9781401952501; перевидано 2026).",
        "source_url": "https://www.hayhouse.com/mystical-shaman-oracle-cards-card-deck",
        "buy_url": "https://www.hayhouse.com/mystical-shaman-oracle-cards-card-deck",
        "translations": {
            "uk": {"name": "Mystical Shaman Oracle", "description": "Довідковий профіль: 64 карти + гайдбук (Hay House, 2018)."},
            "ru": {"name": "Mystical Shaman Oracle", "description": "Справочный профиль: 64 карты + гайдбук (Hay House, 2018)."}},
    },
    {
        "system": "Шаманські карти", "name": "Спиритический оракул тотемов",
        "author": "Арабо Саргсян", "publisher": "«Весь»",
        "year": 2020, "card_count": 48,
        "description": "Довідковий профіль реального видання: 48 карт-тотемів. "
                       "Повного набору карт у БД нема — лише метадані.",
        "composition": "48 карт (концепція автора — див. превʼю в Google Books).",
        "source_url": "https://www.rozamira-tarot.ru/oracles/spiriticheskiy-orakul-totemov.html",
        "buy_url": "https://www.chitai-gorod.ru/product/spiriticheskiy-orakul-totemov-2986999",
        "translations": {
            "uk": {"name": "Спіритичний оракул тотемів", "description": "Довідковий профіль: 48 карт (вид. «Весь», 2020)."},
            "en": {"name": "Spirit Oracle of Totems", "description": "Reference profile: 48 cards (Ves Publishing, 2020)."}},
    },
    {
        "system": "Шаманські карти", "name": "Shamanic Oracle (Rockpool)",
        "author": "Luis & Magali Tamani (перуанська амазонська традиція)", "publisher": "Rockpool Publishing",
        "year": None, "card_count": 36,
        "description": "Довідковий профіль реального видання: 36 карт у 4 родинах за стихіями "
                       "(Roots Protectors — земля, Wind Arcana — повітря, "
                       "Spirit Messengers — вогонь, Wisdom Watchers — вода). "
                       "Повного набору карт у БД нема — лише метадані.",
        "composition": "36 карт: 4 родини × 9 (за стихіями).",
        "source_url": "https://www.rockpoolpublishing.com/en-us/products/shamanic-oracle",
        "buy_url": "https://us.amazon.com/Shamanic-Oracle-Connect-medicine-Rockpool/dp/1923009001",
        "translations": {
            "uk": {"name": "Shamanic Oracle (Rockpool)", "description": "Довідковий профіль: 36 карт, 4 стихійні родини."},
            "ru": {"name": "Shamanic Oracle (Rockpool)", "description": "Справочный профиль: 36 карт, 4 стихийные семьи."}},
    },
    {
        "system": "МАК", "name": "Cope (оригінальне видання, 88)",
        "author": "Офра Аялон (карти); видавець OH Cards", "publisher": "OH Cards",
        "year": None, "card_count": 88,
        "description": "Довідковий профіль реального видання: 88 карт. Увага: окремих «значень» "
                       "кожної карти не існує навіть у видавця — структура колоди це 6 каналів "
                       "BASIC Ph (див. нашу навчальну колоду «COPE · BASIC Ph»). "
                       "Повного набору карт у БД нема — лише метадані.",
        "composition": "88 карт + методика BASIC Ph (Belief, Affect, Social, Imagination, Cognition, Physiology).",
        "source_url": "https://www.oh-cards-institute.org/wp-content/uploads/2012/06/Ofra-Ayalon-Healing-Trauma-with-Metaphoric-Cards.pdf",
        "buy_url": "https://oh-cards.com/cope/",
        "translations": {
            "uk": {"name": "Cope (оригінальне видання, 88)", "description": "Довідковий профіль: 88 карт, модель BASIC Ph."},
            "en": {"name": "Cope (original edition, 88)", "description": "Reference profile: 88 cards, BASIC Ph model."}},
    },
    {
        "system": "МАК", "name": "OH cards / Persona (оригінальні видання)",
        "author": "Моріц Егетмаєр / Елі Раман (OH); Persona — портретна колода серії",
        "publisher": "OH Cards", "year": None, "card_count": None,
        "description": "Довідковий профіль: класика жанру МАК. OH — образи + слова; "
                       "Persona — портретна колода. Склад — на сторінках видавця. "
                       "Повного набору карт у БД нема — лише метадані.",
        "composition": "OH: образи + слова; Persona: портрети (точний склад — у видавця).",
        "source_url": "https://oh-cards.com",
        "buy_url": None,
        "translations": {
            "uk": {"name": "OH cards / Persona (оригінальні видання)"},
            "ru": {"name": "OH cards / Persona (оригинальные издания)"}},
    },
    {
        "system": "МАК", "name": "Архетипы и Тени (Спеццано, 90)",
        "author": "Чак Спеццано", "publisher": None,
        "year": None, "card_count": 90,
        "description": "Довідковий профіль реального видання: 90 карт — 45 світлих архетипів "
                       "(«Шаман», «Мати-Земля») + 45 темних тіней («Чорна Вдова», «Відьма»). "
                       "Принцип парності: у кожного архетипу є своя тінь. "
                       "Повного набору карт у БД нема — лише метадані.",
        "composition": "90 карт: 45 архетипів + 45 тіней (парні).",
        "source_url": "https://www.taroshop.ru/product/173-arhetipy-i-teni-chak-speccano-petra-kyune",
        "buy_url": "https://www.labirint.ru/books/556798/",
        "translations": {
            "uk": {"name": "Архетипи і Тіні (Спеццано, 90)",
                   "description": "Довідковий профіль: 90 карт — 45 архетипів + 45 тіней (парні)."},
            "en": {"name": "Archetypes and Shadows (Spezzano, 90)"}},
    },
    {
        "system": "Таро", "name": "Visconti-Sforza Tarot",
        "author": "Боніфаціо Бембо та майстерня (Мілан)",
        "publisher": None, "year": 1450, "card_count": 74,
        "description": "Довідковий профіль: найстаріша збережена колода Таро (середина XV ст.). "
                       "Збереглося 74 карти, більшість — у Morgan Library. "
                       "Повного набору карт у БД нема — лише метадані.",
        "composition": "74 збережені карти (зокрема 69 — Morgan Library).",
        "source_url": "https://www.themorgan.org/exhibitions/tarot",
        "buy_url": None,
        "translations": {
            "uk": {"name": "Таро Вісконті-Сфорца",
                   "description": "Довідковий профіль: найстаріша збережена колода (бл. 1450, Мілан)."},
            "ru": {"name": "Таро Висконти-Сфорца",
                   "description": "Справочный профиль: старейшая сохранившаяся колода (ок. 1450, Милан)."}},
    },
    {
        "system": "Таро", "name": "Tarot de Marseille",
        "author": "Традиція (Нобле ~1650, Додаль 1701, Конвер 1760)",
        "publisher": None, "year": 1701, "card_count": 78,
        "description": "Довідковий профіль: марсельський візерунок — канон французького Таро "
                       "XVII–XVIII ст., 78 карт. Повного набору карт у БД нема — лише метадані.",
        "composition": "78 карт: 22 старші + 56 молодших (марсельський візерунок).",
        "source_url": "https://trionfi.com/0/i/",
        "buy_url": None,
        "translations": {
            "uk": {"name": "Марсельське Таро",
                   "description": "Довідковий профіль: канон французького Таро XVII–XVIII ст."},
            "ru": {"name": "Марсельское Таро",
                   "description": "Справочный профиль: канон французского Таро XVII–XVIII вв."}},
    },
    {
        "system": "Таро", "name": "Thoth Tarot",
        "author": "Алістер Кроулі, художник Фріда Гарріс",
        "publisher": "Ordo Templi Orientis / US Games", "year": 1969, "card_count": 78,
        "description": "Довідковий профіль: окультна колода Кроулі–Гарріс (малювалася 1938–1943, "
                       "видана 1969). Зображення під копірайтом — у БД лише метадані.",
        "composition": "78 карт + Книга Тота.",
        "source_url": "https://tarot-heritage.com/history-4/resources",
        "buy_url": None,
        "translations": {
            "uk": {"name": "Таро Тота",
                   "description": "Довідковий профіль: колода Кроулі–Гарріс (видана 1969)."},
            "ru": {"name": "Таро Тота",
                   "description": "Справочный профиль: колода Кроули–Харрис (издана 1969)."}},
    },
    {
        "system": "Астрологічні колоди", "name": "Astrological Oracle (22, огляд Aeclectic)",
        "author": "За оглядом Aeclectic", "publisher": None,
        "year": None, "card_count": 22,
        "description": "Довідковий профіль: астрологічний оракул із 22 карт — 12 знаків зодіаку "
                       "+ 10 планет, із власною системою розкладів (за оглядом). "
                       "Повного набору карт у БД нема — лише метадані.",
        "composition": "22 карти: 12 знаків + 10 планет.",
        "source_url": "https://aeclectic.net/tarot/cards/astrological-oracle",
        "buy_url": None,
        "translations": {
            "uk": {"name": "Астрологічний оракул (22)",
                   "description": "Довідковий профіль: 22 карти — 12 знаків + 10 планет."},
            "ru": {"name": "Астрологический оракул (22)",
                   "description": "Справочный профиль: 22 карты — 12 знаков + 10 планет."}},
    },
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    n = 0
    try:
        for p in PROFILES:
            system = db.query(System).filter_by(name=p["system"]).first()
            if not system:
                print(f"[profiles] нема системи: {p['system']} — пропуск {p['name']}")
                continue
            deck = db.query(Deck).filter_by(name=p["name"]).first()
            fields = {"author": p["author"], "publisher": p["publisher"], "year": p["year"],
                      "card_count": p["card_count"], "description": p["description"],
                      "composition": p["composition"], "source_url": p["source_url"],
                      "buy_url": p["buy_url"], "translations": p["translations"],
                      "is_reference_only": True}
            if deck:
                for k, v in fields.items():
                    setattr(deck, k, v)
            else:
                db.add(Deck(system_id=system.id, name=p["name"], **fields))
                n += 1
        db.commit()
        print(f"[profiles] нових: {n}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
