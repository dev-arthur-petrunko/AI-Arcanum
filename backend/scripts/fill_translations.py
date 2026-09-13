"""fill_translations.py — дописує UK/EN keywords+meaning для RWS-старших (22),
Ленорман-36 та шаблонно для молодших арканів. Ідемпотентний (merge у translations).
Запуск з папки backend/: python scripts/fill_translations.py
Тексти — власні навчальні формулювання (не копіпаст).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.models import Card, Deck

# number: (uk_up, uk_rev, uk_mean, en_up, en_rev, en_mean)
MAJORS = {
    "0": ("нові починання, спонтанність, довіра", "безглуздя, ризик, легковажність",
          "Початок шляху з відкритим серцем. Прямо — довіра життю; перевернуто — необачний ризик.",
          "new beginnings, spontaneity, trust", "recklessness, risk, naivety",
          "A path begins with an open heart. Upright — trust life; reversed — reckless risk."),
    "I": ("воля, майстерність, концентрація", "маніпуляція, нерішучість",
          "Маг перетворює задум на дію: усі інструменти вже на столі.",
          "will, mastery, focus", "manipulation, indecision",
          "The Magician turns intent into action: all tools are already on the table."),
    "II": ("інтуїція, таємниця, внутрішнє знання", "приглушена інтуїція, приховані мотиви",
           "Жриця слухає тишу за словами. Відповідь — усередині, не зовні.",
           "intuition, mystery, inner knowledge", "muted intuition, hidden motives",
           "The Priestess hears the silence behind words. The answer is within, not outside."),
    "III": ("достаток, турбота, природа", "залежність, творчий блок",
            "Імператриця плекає: проєкти, людей, тіло. Дозволь собі рости.",
            "abundance, care, nature", "dependence, creative block",
            "The Empress nurtures: projects, people, body. Allow yourself to grow."),
    "IV": ("структура, влада, стабільність", "ригідність, контроль",
           "Імператор тримає форму: правила й межі, що захищають справу.",
           "structure, authority, stability", "rigidity, control",
           "The Emperor holds the frame: rules and borders that protect the work."),
    "V": ("традиція, наставництво, віра", "догматизм, бунт проти правил",
          "Ієрофант передає перевірене знання. Шануй школу — або свідомо йди геть.",
          "tradition, mentorship, faith", "dogmatism, rebellion",
          "The Hierophant passes proven knowledge. Honor the school — or leave it consciously."),
    "VI": ("вибір серцем, союз, гармонія", "дисгармонія, хибний вибір",
           "Закохані — це вибір цінностей, не лише людей. Серце вже знає.",
           "heartfelt choice, union, harmony", "disharmony, wrong choice",
           "The Lovers mean a choice of values, not only of people. The heart already knows."),
    "VII": ("рух, перемога, самоконтроль", "втрата напряму, агресія",
            "Колісниця їде, коли протилежності тягнуть в один бік. Тримай віжки.",
            "motion, victory, self-control", "lost direction, aggression",
            "The Chariot moves when opposites pull together. Hold the reins."),
    "VIII": ("мужність, терпіння, мʼяка сила", "сумніви, вигоряння",
             "Сила — це лагідність, що приборкує лева. Терпіння сильніше за тиск.",
             "courage, patience, gentle strength", "doubt, burnout",
             "Strength is gentleness taming the lion. Patience beats pressure."),
    "IX": ("пошук, мудрість, усамітнення", "ізоляція, застій",
           "Відлюдник світить ліхтарем усередину. Побудь наодинці — відповідь дозріє.",
           "quest, wisdom, solitude", "isolation, stagnation",
           "The Hermit turns the lantern inward. Be alone a while — the answer will ripen."),
    "X": ("зміни, цикл, вдача", "невдалий період, опір змінам",
          "Колесо крутиться: підйоми й спади — сезони, а не вирок.",
          "change, cycles, fortune", "rough patch, resisting change",
          "The Wheel turns: ups and downs are seasons, not sentences."),
    "XI": ("чесність, баланс, відповідальність", "несправедливість, упередженість",
           "Справедливість зважує вчинки, не наміри. Відповідай за свій бік терезів.",
           "honesty, balance, accountability", "injustice, bias",
           "Justice weighs deeds, not intentions. Answer for your side of the scales."),
    "XII": ("пауза, зміна ракурсу, прозріння", "застрягання, марна жертва",
            "Повішений бачить світ догори дриґом — і саме так знаходить сенс. Зупинись.",
            "pause, new angle, insight", "stuck, vain sacrifice",
            "The Hanged Man sees the world upside down — and finds meaning. Pause."),
    "XIII": ("трансформація, завершення, оновлення", "опір кінцю, застій",
             "Смерть зрізає відмерле, щоб живе росло. Відпусти — місце звільниться.",
             "transformation, ending, renewal", "resisting closure, stagnation",
             "Death cuts the withered so the living grows. Let go — space will free up."),
    "XIV": ("баланс, алхімія, помірність", "крайнощі, дисбаланс",
            "Помірність змішує вогонь і воду в золото. Малі дози щодня.",
            "balance, alchemy, temperance", "extremes, imbalance",
            "Temperance blends fire and water into gold. Small doses daily."),
    "XV": ("привʼязаність, тінь, спокуса", "звільнення, розрив ланцюгів",
           "Диявол показує ланцюги, які ти сам тримаєш. Назви залежність — і вона слабне.",
           "attachment, shadow, temptation", "liberation, breaking chains",
           "The Devil shows the chains you hold yourself. Name the dependence — it weakens."),
    "XVI": ("раптові зміни, прозріння, крах ілюзій", "затяжна криза, страх змін",
            "Вежа бʼє блискавкою по хибному. Те, що вціліє, — справжнє.",
            "sudden change, insight, falling illusions", "lingering crisis, fear of change",
            "The Tower strikes the false. What survives is real."),
    "XVII": ("надія, натхнення, зцілення", "втрата віри, зневіра",
             "Зірка світить після бурі: тиха надія й повільне зцілення.",
             "hope, inspiration, healing", "lost faith, gloom",
             "The Star shines after the storm: quiet hope and slow healing."),
    "XVIII": ("ілюзії, сни, підсвідоме", "прояснення, вихід з туману",
              "Місяць плете тіні: не все те, чим здається. Перевіряй факти.",
              "illusions, dreams, subconscious", "clearing, out of fog",
              "The Moon weaves shadows: not all is as it seems. Check the facts."),
    "XIX": ("радість, ясність, успіх", "тимчасове затемнення",
            "Сонце гріє всіх: ясність, здоровʼя, заслужений успіх.",
            "joy, clarity, success", "brief eclipse",
            "The Sun warms all: clarity, health, earned success."),
    "XX": ("пробудження, прощення, покликання", "самобичування, втрачений поклик",
           "Суд будить: підсумуй минуле й підіймайся. Другий шанс — зараз.",
           "awakening, forgiveness, calling", "self-blame, missed call",
           "Judgement wakes: sum up the past and rise. The second chance is now."),
    "XXI": ("завершення циклу, цілісність, тріумф", "незавершеність",
            "Світ замикає коло: справа доведена до кінця. Святкуй і починай нове.",
            "completion, wholeness, triumph", "loose ends",
            "The World closes the circle: work brought to completion. Celebrate, begin anew."),
}

# number: (uk_up, uk_mean, en_up, en_mean)
LENORMAND = {
    "1": ("новини, гість, рух", "Вершник мчить із звісткою: рух і свіжі новини.", "news, visitor, motion", "The Rider rushes in with news: motion and fresh tidings."),
    "2": ("удача, дрібниця, шанс", "Конюшина — мала вдача на короткий строк. Хапай момент.", "luck, small thing, chance", "Clover is small short-term luck. Seize the moment."),
    "3": ("подорож, рух, далечінь", "Корабель пливе далеко: дорога, переїзд, торгівля.", "journey, motion, distance", "The Ship sails far: travel, relocation, trade."),
    "4": ("дім, родина, стабільність", "Дім тримає: родина, побут, опора.", "home, family, stability", "The House holds: family, household, support."),
    "5": ("здоровʼя, сила, природа", "Дерево росте повільно: здоровʼя й коріння.", "health, vitality, nature", "The Tree grows slowly: health and roots."),
    "6": ("неясність, тимчасові труднощі", "Хмари закрили сонце ненадовго. Перечекай.", "ambiguity, brief trouble", "Clouds cover the sun briefly. Wait it out."),
    "7": ("хитрість, обережність", "Змія попереджає: поруч хитрість. Дивись у деталі.", "cunning, caution", "The Snake warns: cunning is near. Check details."),
    "8": ("завершення, межа", "Труна закриває главу. Кінець — теж відповідь.", "ending, limit", "The Coffin closes a chapter. An ending is also an answer."),
    "9": ("радість, запрошення", "Букет — приємність і увага. Приймай з вдячністю.", "joy, invitation", "The Bouquet is pleasure and attention. Accept gratefully."),
    "10": ("рішення, розтин, раптовість", "Коса ріже швидко: рішення або розрив. Не зволікай.", "decision, cut, suddenness", "The Scythe cuts fast: a decision or a break. Do not delay."),
    "11": ("розмова, очищення", "Мітла мете сміття: розмова начистоту й прибирання.", "talk, cleansing", "The Whip sweeps trash: plain talk and cleanup."),
    "12": ("переговори, хвилювання", "Сови цвірінькають: дзвінки, листи, метушня.", "talks, bustle", "The Birds chatter: calls, letters, bustle."),
    "13": ("дитина, початок, щирість", "Дитина — нове й щире. Почни з чистого аркуша.", "child, beginning, sincerity", "The Child is new and sincere. Start from a blank page."),
    "14": ("робота, вигода, обережність", "Лис полює на роботі: будь розумнішим за хитрих.", "work, gain, caution", "The Fox hunts at work: outsmart the cunning."),
    "15": ("покровитель, фінанси, сила", "Ведмідь тримає гроші й владу. Шукай сильного союзника.", "patron, finances, strength", "The Bear holds money and power. Find a strong ally."),
    "16": ("надія, плани", "Зорі світять далеко: мрій і плануй.", "hope, plans", "The Stars shine far: dream and plan."),
    "17": ("зміни, переїзд", "Лелека несе зміни: переїзд або новий етап.", "changes, relocation", "The Stork brings change: relocation or a new stage."),
    "18": ("друг, вірність", "Собака — вірний друг. Довірся перевіреним.", "friend, loyalty", "The Dog is a loyal friend. Trust the proven."),
    "19": ("межі, офіційність", "Вежа — правила й інстанції. Грай за процедурою.", "borders, formality", "The Tower is rules and offices. Follow procedure."),
    "20": ("суспільство, публічність", "Сад — люди й вихід у світ. Покажися.", "society, public", "The Garden is people and going out. Show up."),
    "21": ("перешкода, затримка", "Гора стоїть на шляху: обхід або чекання.", "obstacle, delay", "The Mountain blocks the path: detour or wait."),
    "22": ("вибір, рішення", "Роздоріжжя: обери й іди, не озираючись.", "choice, decision", "The Crossroads: choose and walk, do not look back."),
    "23": ("втрати, стрес", "Щури гризуть запаси: дрібні втрати й нерви.", "losses, stress", "The Mice gnaw supplies: small losses and nerves."),
    "24": ("кохання, почуття", "Серце — про почуття. Слухай його.", "love, feelings", "The Heart is about feelings. Listen to it."),
    "25": ("союз, договір", "Каблучка скріплює: союз або угода.", "union, contract", "The Ring seals: a union or a deal."),
    "26": ("знання, таємниця", "Книга закрита: вчися або чекай розкриття.", "knowledge, secret", "The Book is closed: study or await reveal."),
    "27": ("лист, документ", "Лист несе звістку на папері. Читай уважно.", "letter, document", "The Letter carries paper news. Read carefully."),
    "28": ("чоловік, партнер", "Чоловік — кверент або важливий чоловік.", "man, partner", "The Man is the querent or a key man."),
    "29": ("жінка, партнерка", "Жінка — кверентка або важлива жінка.", "woman, partner", "The Woman is the querent or a key woman."),
    "30": ("чистота, покровительство", "Лілії — чистота й повага старших.", "purity, patronage", "The Lilies are purity and eldersʼ respect."),
    "31": ("успіх, ясність", "Сонце Ленорман: удача й тепло.", "success, clarity", "The Sun of Lenormand: luck and warmth."),
    "32": ("інтуїція, цикли", "Місяць — сни й цикли. Звіряйся з ритмом.", "intuition, cycles", "The Moon is dreams and cycles. Mind the rhythm."),
    "33": ("рішення, відкриття", "Ключ відмикає: відповідь уже в руках.", "solution, opening", "The Key unlocks: the answer is in hand."),
    "34": ("гроші, потік", "Риби пливуть у грошах: потік і прибуток.", "money, flow", "The Fish swim in money: flow and profit."),
    "35": ("стабільність, робота", "Якір тримає: стабільна робота й опора.", "stability, work", "The Anchor holds: steady work and support."),
    "36": ("урок, доля", "Хрест — випробування долі. Неси гідно.", "lesson, fate", "The Cross is fateʼs trial. Bear it with dignity."),
}


def merge(card, lang, **fields):
    tr = dict(card.translations or {})
    block = dict(tr.get(lang, {}))
    block.update({k: v for k, v in fields.items() if v})
    tr[lang] = block
    card.translations = tr


def run():
    db = SessionLocal()
    try:
        rws = db.query(Deck).filter(Deck.name.contains("Уэйта")).first()
        n = 0
        if rws:
            for number, (uk_up, uk_rev, uk_m, en_up, en_rev, en_m) in MAJORS.items():
                c = db.query(Card).filter_by(deck_id=rws.id, number=number).first()
                if not c:
                    continue
                merge(c, "uk", keywords_upright=uk_up, keywords_reversed=uk_rev, meaning_general=uk_m)
                merge(c, "en", keywords_upright=en_up, keywords_reversed=en_rev, meaning_general=en_m)
                n += 1
            # молодші — шаблонні UK/EN (дзеркало RU-структури)
            minors = db.query(Card).filter_by(deck_id=rws.id, arcana_type="Младший аркан").all()
            for c in minors:
                uk_name = (c.translations or {}).get("uk", {}).get("name", "")
                en_name = (c.translations or {}).get("en", {}).get("name", "")
                if uk_name:
                    merge(c, "uk", keywords_upright=f"навчальне значення {uk_name} (прямо)",
                          keywords_reversed=f"навчальне значення {uk_name} (перевернуто)",
                          meaning_general=f"{uk_name}: молодший аркан. Базова трактовка для заучування.")
                if en_name:
                    merge(c, "en", keywords_upright=f"study meaning of {en_name} (upright)",
                          keywords_reversed=f"study meaning of {en_name} (reversed)",
                          meaning_general=f"{en_name}: a minor arcana card. Basic study meaning.")
                n += 1
        plen = db.query(Deck).filter(Deck.name.contains("Lenormand")).first()
        if plen:
            for number, (uk_up, uk_m, en_up, en_m) in LENORMAND.items():
                c = db.query(Card).filter_by(deck_id=plen.id, number=number).first()
                if not c:
                    continue
                merge(c, "uk", keywords_upright=uk_up, meaning_general=uk_m)
                merge(c, "en", keywords_upright=en_up, meaning_general=en_m)
                n += 1
        db.commit()
        print(f"[i18n] оновлено карток: {n}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
