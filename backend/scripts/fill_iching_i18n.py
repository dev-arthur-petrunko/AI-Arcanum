"""fill_iching_i18n.py — UK-назви/значення + EN-короткі значення для 64 гексаграм.
Базовий EN-повний текст Легга лишається; UK дає стислий переказ.
Ідемпотентний. Запуск з папки backend/: python scripts/fill_iching_i18n.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.models import Card, Deck

# number: (uk_name, uk_kw, uk_mean, en_mean)
H = {
    "1": ("Цянь · Творчість", "творчість, сила, початок", "Чиста ян-енергія: дій сміливо, час творити.", "Creative force. Act boldly — time to create."),
    "2": ("Кунь · Сприйнятливість", "поступливість, земля", "Приймай і слідуй: сила в мʼякості й терпінні.", "Receptive earth. Yield and follow; strength in gentleness."),
    "3": ("Чжунь · Паросток", "хаос початку", "Початок важкий: шукай помічників, не поспішай.", "Sprouting difficulty. Seek helpers, do not rush."),
    "4": ("Мен · Учень", "недосвідченість, питання", "Незнання — не сором: питай учителя.", "Youthful folly. Ask the teacher; ignorance is no shame."),
    "5": ("Сюй · Очікування", "чекання, гідність", "Чекай слушного моменту з гідністю.", "Waiting with dignity for the right moment."),
    "6": ("Сун · Суперечка", "конфлікт", "Суперечку краще владнати миром, ніж судом.", "Conflict: settle in peace, not in court."),
    "7": ("Ши · Військо", "дисципліна, команда", "Перемога — в порядку й досвідченому проводі.", "The army: victory through discipline and seasoned lead."),
    "8": ("Бі · Єднання", "союз", "Тримайся своїх — разом сила.", "Union: hold together — strength in numbers."),
    "9": ("Сяо-чу · Мала сила", "стриманість", "Малий гальмівний шлях: стримай порив.", "Small restraint: check the impulse."),
    "10": ("Лі · Поступ", "обережність", "Ступай обережно, як по хвосту тигра.", "Treading carefully, as on a tiger's tail."),
    "11": ("Тай · Розквіт", "гармонія", "Небо й земля в згоді: золотий час.", "Peace: heaven and earth in accord — golden time."),
    "12": ("Пі · Занепад", "застій", "Звʼязки рвуться: бережи головне, чекай.", "Standstill: ties break; guard the core, wait."),
    "13": ("Тун-жень · Братерство", "спільнота", "Одна мета єднає різних. Виходь до людей.", "Fellowship: one goal unites. Go out to people."),
    "14": ("Да-ю · Володіння", "достаток", "Велике володіння зобовʼязує ділитися.", "Great possession obliges sharing."),
    "15": ("Цянь · Смиренність", "скромність", "Скромність відкриває всі двері.", "Modesty opens every door."),
    "16": ("Юй · Натхнення", "радість", "Радість запалює інших. Святкуй.", "Enthusiasm ignites others. Celebrate."),
    "17": ("Суй · Слідування", "приклад", "Іди за гідним прикладом.", "Following: walk behind a worthy example."),
    "18": ("Гу · Ремонт", "гниль", "Старі помилки вимагають ремонту. Берися.", "Decay demands repair. Get to it."),
    "19": ("Лінь · Наближення", "весна", "Весна наближається: іди назустріч.", "Approach: spring nears — walk to meet it."),
    "20": ("Гуань · Огляд", "споглядання", "Дивись широко, суди повільно.", "Contemplation: look wide, judge slowly."),
    "21": ("Ши-хо · Прикус", "рішучість", "Перекуси вузол: вирішуй твердо.", "Biting through: cut the knot firmly."),
    "22": ("Бі · Прикраса", "форма", "Краса — в міру; суть важливіша.", "Grace in measure; substance over wrapper."),
    "23": ("Бо · Обвал", "руйнування", "Старе сиплеться: не тримайся за руїну.", "Splitting: the old crumbles — let go."),
    "24": ("Фу · Повернення", "поворот", "Світло повертається: добрий знак.", "Return: light comes back — a good omen."),
    "25": ("У-ван · Щирість", "невинність", "Дій без хитрощів — небо з тобою.", "Innocence: act without guile."),
    "26": ("Да-чу · Накопичення", "запас сил", "Збирай сили для великого стрибка.", "Great restraint: gather force for the leap."),
    "27": ("І · Живлення", "їжа, слова", "Стеж, чим живиш тіло й розум.", "Nourishment: watch what feeds body and mind."),
    "28": ("Да-го · Перегин", "надмір", "Балка гнеться: скинь зайве.", "Great excess: the beam bends — shed load."),
    "29": ("Кань · Безодня", "небезпека", "Вода за водою: тримай серце рівно.", "The abysmal: water on water — hold heart steady."),
    "30": ("Лі · Сяйво", "ясність", "Тримайся світлого: ясність веде.", "Radiance: hold to the light."),
    "31": ("Сянь · Тяжіння", "взаємність", "Серця тягнуться: відповідай.", "Mutual pull: hearts attract — respond."),
    "32": ("Хен · Сталість", "тривалість", "Сталість у доброму — перемога.", "Duration: persist in good — victory."),
    "33": ("Дунь · Відступ", "відхід", "Вчасний відступ — теж перемога.", "Retreat in time is also victory."),
    "34": ("Да-чжуан · Міць", "сила", "Сила без розуму ламає. Спрямуй.", "Great power without mind breaks. Channel it."),
    "35": ("Цзінь · Схід", "прогрес", "Сонце сходить: тебе помітять.", "Progress: the sun rises — you will be noticed."),
    "36": ("Мін-і · Тінь", "затемнення", "Світло приховане: бережися, чекай.", "Darkening: light hidden — take care, wait."),
    "37": ("Цзя-жень · Родина", "дім", "Порядок у домі — порядок у світі.", "Family: order at home, order in world."),
    "38": ("Куй · Розлад", "різниця", "Різні — не вороги. Шукай спільне.", "Opposition: different is not enemy."),
    "39": ("Цзянь · Затор", "перешкода", "Попереду болото: зупинись і подумай.", "Obstruction: swamp ahead — stop and think."),
    "40": ("Цзє · Розвʼязка", "звільнення", "Вузол розвʼязано: рухайся.", "Deliverance: the knot is untied — move."),
    "41": ("Сунь · Жертва", "зменшення", "Віддай мале заради великого.", "Decrease: give small for great."),
    "42": ("І · Приріст", "зростання", "Вітер і грім: час діяти.", "Increase: wind and thunder — act now."),
    "43": ("Гуай · Прорив", "рішучість", "Скажи правду вголос. Без насильства.", "Breakthrough: speak truth aloud, no violence."),
    "44": ("Гоу · Спокуса", "зустріч", "Обережно з чарівним незнайомцем.", "Meeting: beware the charming stranger."),
    "45": ("Цуй · Збори", "єднання", "Збирай людей навколо спільного.", "Gathering: rally people around common cause."),
    "46": ("Шен · Сходження", "ріст", "Дерево росте повільно: крок за кроком.", "Ascending: the tree grows slowly, step by step."),
    "47": ("Кунь · Втома", "виснаження", "Колодязь порожній: відпочинь.", "Exhaustion: the well is empty — rest."),
    "48": ("Цзін · Джерело", "колодязь", "Колодязь незмінний: черпай мудрість.", "The Well: unchanging source — draw wisdom."),
    "49": ("Ге · Злам", "зміни", "Шкіра змії: зміни неминучі.", "Revolution: snakeskin — change is due."),
    "50": ("Дін · Котел", "трансформація", "Священний котел варить нове.", "The Cauldron cooks the new."),
    "51": ("Чжень · Грім", "струс", "Грім лякає, але будить.", "Thunder frightens yet wakes."),
    "52": ("Ген · Гора", "спокій", "Гора стоїть: зупини метушню.", "Stillness: the mountain stands — stop fuss."),
    "53": ("Цзянь · Повільність", "поступовість", "Дикі гуси летять порядком: не поспішай.", "Gradualness: wild geese fly in order."),
    "54": ("Гуй-мей · Нерівня", "нерівний союз", "Не твоя роль — не грай її.", "Marrying maiden: not your role — don't play it."),
    "55": ("Фен · Пік", "достаток", "Південь сонця: пік минає — дій зараз.", "Abundance: solar noon — the peak passes, act now."),
    "56": ("Люй · Чужина", "мандри", "У гостях будь скромним.", "Wanderer: abroad, be modest."),
    "57": ("Сунь · Вітер", "мʼякість", "Вітер точить скелю: мʼяко й наполегливо.", "Gentleness: wind wears rock — soft yet persistent."),
    "58": ("Дуй · Радість", "відкритість", "Відкрите серце притягує друзів.", "Joy: an open heart draws friends."),
    "59": ("Хуань · Туман", "розсіяння", "Туман розходиться: збирай розсипане.", "Dispersion: fog lifts — gather the scattered."),
    "60": ("Цзє · Міра", "межі", "Міра в усьому: встанови ліміт.", "Limitation: measure in all — set limits."),
    "61": ("Чжун-фу · Правда", "щирість", "Внутрішня правда чути здалеку.", "Inner truth is heard from afar."),
    "62": ("Сяо-го · Мале", "обережність", "Малими кроками — велику дорогу.", "Small steps make the long road."),
    "63": ("Цзі-цзі · Кінець", "завершення", "Справу завершено — пильнуй новий початок.", "Completion: work done — mind new beginnings."),
    "64": ("Вей-цзі · Передфінал", "незавершеність", "Ще крок: не розслабляйся завчасно.", "Before completion: one step left — don't relax early."),
}


def run():
    db = SessionLocal()
    try:
        deck = db.query(Deck).filter(Deck.name.like("%Цзин%")).first()
        n = 0
        for number, (uk_name, uk_kw, uk_m, en_m) in H.items():
            c = db.query(Card).filter_by(deck_id=deck.id, number=number).first()
            if not c:
                continue
            tr = dict(c.translations or {})
            uk = dict(tr.get("uk", {}))
            uk.update({"name": uk_name, "keywords_upright": uk_kw, "meaning_general": uk_m})
            tr["uk"] = uk
            en = dict(tr.get("en", {}))
            en["meaning_short"] = en_m
            tr["en"] = en
            c.translations = tr
            n += 1
        db.commit()
        print(f"[iching-i18n] оновлено: {n}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
