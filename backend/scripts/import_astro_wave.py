"""import_astro_wave.py — третя хвиля (астрологічна): 6 систем / 6 колод / 287 карт.

    5 навчальних колод за структурою комерційних (Scott Gross · Weatherstone,
    Williamson «An Astrological Year», Goodchild «The Arcana of Astrology»,
    Sutton «Oracle of the Radiant Sun», Waller «The Philosophy of Astrology»)
    + 1 довідкова колода-референс (russellcottrell, is_reference_only=1).

Усі значення — ВЛАСНИЙ навчальний переказ (гадальні словники й міфи),
не копіпаст текстів/сканів. Ідемпотентний (за name системи/колоди).
Запуск з папки backend/:  python scripts/import_astro_wave.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Card, Deck, System

from astro_wave import decks as DW

# Джерело-надихач (структура/обсяг реальної колоди; тексти не копіюємо)
SRC_WEATHER = "https://www.weatherstonegroup.com/"
SRC_WILLIAMSON = "https://www.selfstudydaily.com/"
SRC_GOODCHILD = "https://www.thearcanaofastrology.com/"
SRC_RADIANT = "https://www.hayhouse.com/oracle-of-the-radiant-sun"
SRC_WALLER = "https://www.musingmystical.com/free-astrology-oracle-deck/"
SRC_REF = "https://russellcottrell.com/astrology/"


DESCR_LEARNING = ("Навчальна колода за структурою класичного астрологічного оракула: "
                  "повні значення в БД, формулювання — власний навчальний переказ. "
                  "Джерело-надихач зазначено в профілі.")

DECKS = [
    {"system": "Астрологія · Ар-нуво", "sys_cat": "астрологічні",
     "sys_history": ("Власні образи колоди Weatherstone: знаки й планети подано як персонажів "
                     "міфу та їхні правила. 22 карти: 12 знаків зодіаку + 10 планет; кожен знак "
                     "пов'язаний зі своєю планетою-управителем."),
     "sys_origin": "США",
     "deck": "Астрологічний оракул «Ар-нуво» (навчальний)",
     "deck_en": "Astrology Art-Nouveau Oracle (learning)",
     "deck_ru": "Астрологический оракул «Ар-нуво» (обучающий)",
     "kind": "weatherstone", "src": SRC_WEATHER, "ref": False,
     "composition": ("22 карти: 12 знаків (знак + управитель + стихія) і 10 планет. "
                     "Розклад «Круг домів»: перша карта — знак, друга — планета-управитель.")},
    {"system": "Астрологічний рік", "sys_cat": "астрологічні",
     "sys_history": ("Навчальний переказ колоди Williamson «An Astrological Year»: річний цикл "
                     "від знаків і планет до домів, фаз Місяця, стихій і поворотних точок року."),
     "sys_origin": "Канада",
     "deck": "Астрологічний рік · Цикли (навчальний)",
     "deck_en": "The Astrological Year · Cycles (learning)",
     "deck_ru": "Астрологический год · Циклы (обучающий)",
     "kind": "williamson", "src": SRC_WILLIAMSON, "ref": False,
     "composition": ("50 карт: 12 знаків + 10 планет + 12 домів + 8 фаз Місяця + 4 стихії "
                     "+ 4 сонцестояння/рівнодення. Розклад «Річне коло»: 12 позицій по місяцях.")},
    {"system": "Аркани астрології", "sys_cat": "астрологічні",
     "sys_history": ("Навчальний переказ колоди Goodchild «The Arcana of Astrology»: знаки, "
                     "доми, планети, фази Місяця, астероїди та затемнення як 54 аркани-уроки."),
     "sys_origin": "Велика Британія",
     "deck": "Аркани астрології (навчальні)",
     "deck_en": "Arcana of Astrology (learning)",
     "deck_ru": "Арканы астрологии (обучающие)",
     "kind": "goodchild", "src": SRC_GOODCHILD, "ref": False,
     "composition": ("54 карти: 12 знаків + 12 домів + 10 планет + 8 фаз + 10 астероїдів "
                     "+ 2 затемнення. Розклад «Колесо аркан»: 3 карти — знак, дім, планета.")},
    {"system": "Сяюче Сонце", "sys_cat": "астрологічні",
     "sys_history": ("Навчальний переказ колоди Sutton «Oracle of the Radiant Sun»: 7 небесних "
                     "тіл-мастей (Сонце, Місяць, Меркурій, Венера, Марс, Юпітер, Сатурн) у "
                     "12 знаках — 84 карти щоденної поради."),
     "sys_origin": "Велика Британія",
     "deck": "Астрологічний оракул «Сяюче Сонце» (навчальний)",
     "deck_en": "Astrological Oracle of the Radiant Sun (learning)",
     "deck_ru": "Астрологический оракул «Сияющее Солнце» (обучающий)",
     "kind": "radiant_sun", "src": SRC_RADIANT, "ref": False,
     "composition": ("84 карти: 7 мастей-світил × 12 знаків. Розклад «Світило дня»: одна карта "
                     "показує, яке з семи тіл активне сьогодні і в якому знаку.")},
    {"system": "Архетипічна астрологія", "sys_cat": "астрологічні",
     "sys_history": ("Навчальний переказ колоди Waller «The Philosophy of Astrology»: 10 планет-"
                     "архетипів + 45 планетарних пар, що описують діалоги енергій у людині."),
     "sys_origin": "Австралія",
     "deck": "Астрологічні архетипи · Планети і пари (навчальний)",
     "deck_en": "Astrological Archetypes · Planets & Pairs (learning)",
     "deck_ru": "Астрологические архетипы · Планеты и пары (обучающий)",
     "kind": "waller", "src": SRC_WALLER, "ref": False,
     "composition": ("55 карт: 10 планет-архетипів (подарунок) і 45 пар (діалог, співзвучність "
                     "або творча напруга). Розклад «Діалог»: пара показує внутрішню рівновагу.")},
    {"system": "Астрологічний довідник", "sys_cat": "астрологічні",
     "sys_history": ("Довідкова система за відкритим веб-посібником russellcottrell: короткі "
                     "рольові значення 10 планет (енергія) і 12 знаків (як енергія пофарбована) "
                     "для швидкого читання натальної карти."),
     "sys_origin": "США",
     "deck": "Астрологічний довідник · Планети і знаки (референс)",
     "deck_en": "Astrology Reference · Planets & Signs",
     "deck_ru": "Астрологический справочник · Планеты и знаки (справочная)",
     "kind": "reference", "src": SRC_REF, "ref": True,
     "composition": ("22 карти: 10 планет (енергії) + 12 знаків (колір енергії). Розклад «3 карти»: "
                     "планета (що діє) + знак (як діє) + позиція-дім (де діє).")},
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    n_sys = n_deck = n_card = 0
    try:
        for d in DECKS:
            system = db.query(System).filter_by(name=d["system"]).first()
            if not system:
                system = System(name=d["system"], category=d["sys_cat"],
                                history=d["sys_history"],
                                origin_country=d["sys_origin"], approx_year=None,
                                description="Астрологічна система: навчальні колоди в БД.",
                                translations={"uk": {"name": d["system"]},
                                              "en": {"name": d["system"]},
                                              "ru": {"name": d["system"]}})
                db.add(system)
                db.flush()
                n_sys += 1
            deck = db.query(Deck).filter_by(name=d["deck"]).first()
            rows = DW.build(d["kind"])
            fields = {
                "system_id": system.id, "author": "AI-Arcanum (навчальна колода)",
                "publisher": None, "year": None, "card_count": len(rows),
                "source_url": d["src"], "is_reference_only": d["ref"],
                "composition": d["composition"], "gallery": None,
                "description": (DESCR_LEARNING if not d["ref"]
                                else "Довідкова колода-референс: 22 базові карти (планети і знаки) "
                                     "для швидкої орієнтації; повна карта рекомендацій читається "
                                     "розкладом «3 карти» (планета + знак + дім-позиція)."),
                "translations": {
                    "uk": {"name": d["deck"], "description": "Навчальний переказ структури колоди."},
                    "en": {"name": d["deck_en"], "description": "Learning deck, own paraphrase."},
                    "ru": {"name": d["deck_ru"], "description": "Обучающая колода, свой пересказ."}},
            }
            if deck:
                for k, v in fields.items():
                    setattr(deck, k, v)
            else:
                deck = Deck(name=d["deck"], **fields)
                db.add(deck)
                db.flush()
                n_deck += 1
            db.query(Card).filter_by(deck_id=deck.id).delete()
            db.flush()
            for i, card in enumerate(rows):
                card["number"] = str(i + 1)
                db.add(Card(deck_id=deck.id, **card))
                n_card += 1
        db.commit()
        print(f"[astro-wave] систем: {n_sys} нових, колод: {n_deck} нових, карт: {n_card}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()