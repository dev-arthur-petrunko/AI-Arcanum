# -*- coding: utf-8 -*-
"""enrich_small.py — збагачення текстів 3 колод: moon_oracle8, ancestors12, numerology12.
Основна мова — українська; повні переклади en/ru. Стиль — власний навчальний переказ.
Формат входу для кожної карти:
  (kw_u_uk, kw_r_uk, gen_uk, sym_uk,
   kw_u_en, kw_r_en, gen_en, sym_en,
   kw_u_ru, kw_r_ru, gen_ru, sym_ru)
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CARDS_DIR = Path(__file__).resolve().parents[1] / "Database" / "cards"

# ============================ MOON ORACLE 8 ============================
MOON = {
    "1": (
        "початок, намір", "порожнеча",
        "Молодик — темний диск, чистий аркуш місяця. Енергії майже нема, і це дар: нічого не заважає задуматися про цілі. Найкращий час, щоб тихо сформулювати намір і посіяти перше насіння справи — без поспіху й суєти.",
        "Невидимий диск, злитий із нічним небом; крапля-насіння в темряві землі.",
        "beginning, intent", "emptiness",
        "Dark Moon is a blank sheet: energy is low and that is a gift — nothing distracts from planning. Best time to quietly set an intention and plant the first seed of a venture, unhurried.",
        "The invisible disc merging with the night sky; a seed in the dark soil.",
        "начало, намерение", "пустота",
        "Новолуние — тёмный диск, чистый лист. Энергии почти нет, и это дар: ничто не мешает подумать о целях. Лучшее время тихо сформулировать намерение и посеять первое семя дела — без спешки.",
        "Невидимый диск, слитый с ночным небом; семя во тьме земли.",
    ),
    "2": (
        "ріст, надія", "сумніви",
        "Молодий серп — перший промінь надії: справа почалася і тепер потребує щоденної уваги, як паросток води. Не квап події — дивись, куди спрямовані ріжки серпа: у зростаючій фазі вони «вказують» на шлях росту.",
        "Срібний серп на заході одразу після заходу сонця; паросток, що пробиває землю.",
        "growth, hope", "doubts",
        "The waxing crescent is the first ray of hope: the venture has begun and needs daily attention like a sprout needs water. Do not rush events; tend the growth.",
        "A silver crescent in the western sky right after sunset; a sprout breaking the soil.",
        "рост, надежда", "сомнения",
        "Молодой серп — первый луч надежды: дело началось и теперь требует ежедневного внимания, как росток воды. Не торопи события — ухаживай за ростом.",
        "Серебряный серп на западе сразу после заката; росток, пробивающий землю.",
    ),
    "3": (
        "дія, рішення", "тиск",
        "Перша чверть — півдиска світла: час від задумів переходити до дії. Перша перешкода — це водночас перший іспит характеру, що відсіває несуттєве. Ухвали рішення й рухайся, навіть якщо видно лише половину шляху.",
        "Півколо світла й півколо тіні; роздоріжжя, де вибір стає дією.",
        "action, decision", "pressure",
        "First quarter is a half disc of light: time to move from ideas to action. The first obstacle is also the first test. Decide and move even if only half the path is visible.",
        "Half circle of light and half of shadow; a crossroads where choice becomes action.",
        "действие, решение", "давление",
        "Первая четверть — полудиск света: пора от замыслов переходить к действию. Первое препятствие — это и первый экзамен характера. Прими решение и двигайся, даже если видна лишь половина пути.",
        "Полукруг света и полукруг тени; перекрёсток, где выбор становится действием.",
    ),
    "4": (
        "розгін, віра", "нетерплячка",
        "Зростаючий місяць (майже повня) — час найбільшого розгону перед кульмінацією. Ідеї перевірені, ресурси зібрані; тепер головне — тримати темп і не зірватися від нетерпіння. Довірся процесу.",
        "Опуклий диск, майже повний; хвиля, що набирає висоту перед гребнем.",
        "momentum, faith", "impatience",
        "The waxing gibbous brings the greatest momentum before the climax. Ideas are tested, resources gathered; the key is to keep the pace and not break from impatience. Trust the process.",
        "A convex disc, almost full; a wave rising before its crest.",
        "разгон, вера", "нетерпение",
        "Прибывающая луна (почти полнолуние) — время наибольшего разгона перед кульминацией. Идеи проверены, ресурсы собраны; главное — держать темп и не сорваться от нетерпения. Доверься процессу.",
        "Выпуклый диск, почти полный; волна, набирающая высоту перед гребнем.",
    ),
    "5": (
        "кульмінація, ясність", "перегрів",
        "Повня — пік циклу: усе видно при повному світлі, приховане стає явним. Результати дозріли — пожинай і дякуй. Остерігайся перегріву емоцій: велика ясність іноді спокушає на надмірності.",
        "Повне коло світла, що відбиває сонце; дзеркало, у якому видно суть.",
        "culmination, clarity", "overheat",
        "The Full Moon is the peak: everything is visible in full light and the hidden becomes clear. The results are ripe — harvest and give thanks. Beware of overheated emotions; great clarity can tempt excess.",
        "A full circle of light mirroring the sun; a mirror that shows the essence.",
        "кульминация, ясность", "перегрев",
        "Полнолуние — пик цикла: всё видно при полном свете, скрытое становится явным. Результаты созрели — пожинай и благодари. Остерегайся перегрева эмоций: большая ясность иногда соблазняет на излишества.",
        "Полный круг света, отражающий солнце; зеркало, в котором видна суть.",
    ),
    "6": (
        "ділення, вдячність", "чутки",
        "Спадаючий місяць — світло зменшується, але не зникає: час ділитися плодами й досвідом. Розкажи, чому навчився, віддай частину отриманого. Це фаза вдячності й передачі естафети.",
        "Тануча тінь на диску; простягнута долоня, що віддає.",
        "sharing, gratitude", "gossip",
        "The waning gibbous: light decreases but does not disappear — time to share fruits and experience. Tell what you learned, give part of what you received. A phase of gratitude and passing the baton.",
        "A shrinking shadow on the disc; an open palm giving out.",
        "деление, благодарность", "слухи",
        "Убывающая луна — свет убывает, но не исчезает: пора делиться плодами и опытом. Расскажи, чему научился, верни часть полученного. Фаза благодарности и передачи эстафеты.",
        "Тающая тень на диске; открытая ладонь, отдающая.",
    ),
    "7": (
        "відпускання, прощення", "самокритика",
        "Остання чверть — стала половина тіні: час свідомо відпускати все зайве, що тягне назад. Пробач борги — собі й іншим — і дозволь циклу завершитися. Це фаза очищення, а не самоїдства.",
        "Півдиск тіні; мітла, що вимітає старе з дому.",
        "release, forgiveness", "self-criticism",
        "Last quarter is a steady half-shadow: time to consciously release what pulls back. Forgive debts — to yourself and others — and let the cycle end. A phase of cleansing, not self-criticism.",
        "A half disc of shadow; a broom sweeping the old out of the house.",
        "отпускание, прощение", "самокритика",
        "Последняя четверть — ровная половина тени: пора сознательно отпускать всё лишнее. Прости долги — себе и другим — и позволь циклу завершиться. Это фаза очищения, а не самокритики.",
        "Полудиск тени; метла, выметающая старое из дома.",
    ),
    "8": (
        "тиша, відпочинок", "застрягання в минулому",
        "Старий серп — тонка смужка світла перед новим колом: час тиші, відпочинку й підбиття підсумків. Закрий стару сторінку вдячно, забравши уроки, і не чіпляйся за минуле.",
        "Згасаючий серп на світанку; колиска, у якій готується новий цикл.",
        "stillness, rest", "stuck in the past",
        "The balsamic crescent is a thin strip of light before a new cycle: time for stillness, rest and summing up. Close the chapter gratefully, taking the lessons, and do not cling to the past.",
        "A fading crescent at dawn; a cradle preparing a new cycle.",
        "тишина, отдых", "застревание в прошлом",
        "Старый серп — тонкая полоска света перед новым кругом: пора тишины, отдыха и подведения итогов. Закрой главу с благодарностью, забрав уроки, и не цепляйся за прошлое.",
        "Затухающий серп на рассвете; колыбель, готовящая новый цикл.",
    ),
}

# ============================ ANCESTORS 12 ============================
KIN = {
    "1": (
        "мати, прийняття", "гіперопіка",
        "Архетип матері в роді — безумовне прийняття: перша груди, що годує, і перші руки, що тримають. Запитай себе: у чому в мені просить тепла, а я відповідаю суворістю? Дай собі те, що зазвичай даєш іншим.",
        "Колиска як перша чаша роду; круглі форми захисту й годування.",
        "mother, acceptance", "overprotection",
        "The mother archetype in the lineage is unconditional acceptance — the first breast and the first arms. Ask yourself: where in me asks for warmth while I answer with severity? Give yourself what you usually give others.",
        "The cradle as the first chalice of the kin; round forms of care and feeding.",
        "мать, принятие", "гиперопека",
        "Архетип матери в роду — безусловное принятие: первая грудь и первые руки. Спроси себя: что во мне просит тепла, а я отвечаю строгостью? Дай себе то, что обычно даёшь другим.",
        "Колыбель как первая чаша рода; округлые формы защиты и кормления.",
    ),
    "2": (
        "батько, опора", "авторитаризм",
        "Архетип батька — межа й опора: те, на що можна спертися, і те, що говорить «до тут, а не далі». Здоровий батьківський принцип захищає простір для росту, а не душить правилами. На що в твоєму житті реально можна спертися?",
        "Дах і затвор; вертикальний стовп, що тримає перекриття роду.",
        "father, support", "authoritarianism",
        "The father archetype is boundary and support: the backbone to lean on. A healthy father-principle protects space for growth instead of suffocating with rules. What in your life can you really lean on?",
        "Roof and gate; the vertical pillar holding up the kin's ceiling.",
        "отец, опора", "авторитаризм",
        "Архетип отца — граница и опора: то, на что можно опереться. Здоровое отцовское начало защищает пространство для роста, а не душит правилами. На что в твоей жизни реально можно опереться?",
        "Крыша и ворота; вертикальный столб, держащий перекрытие рода.",
    ),
    "3": (
        "бабуся, тепло", "образи",
        "Бабуся — тепло рук і памʼять смаку: через неї рід зберігає рецепти, пісні й обряди. Якщо карта прийшла, згадай, чий запах чи смак дитинства гріє найбільше, і повернися до нього — це ресурс, а не ностальгія.",
        "Пироги на столі; руки, що замішують тісто — передача тепла через практику.",
        "grandmother, warmth", "grudges",
        "Grandmother is the warmth of hands and the memory of taste; through her the kin keeps recipes, songs and rites. If this card appears, recall which childhood flavour warms you most — return to it as a resource, not nostalgia.",
        "Pies on the table; hands kneading dough — warmth passed through practice.",
        "бабушка, тепло", "обиды",
        "Бабушка — тепло рук и память вкуса: через неё род хранит рецепты, песни и обряды. Если карта пришла, вспомни, какой запах детства греет сильнее всего, и вернись к нему — это ресурс, а не ностальгия.",
        "Пироги на столе; руки, месящие тесто — передача тепла через практику.",
    ),
    "4": (
        "дідусь, майстерність", "суворість",
        "Дідусь — ремесло й історії: руки, що знають справу, і голос, що зберіг минуле. Карта нагадує, що навички роду передаються не словами, а спільною справою. Яке ремесло чи історія твого роду чекають, щоб їх продовжили?",
        "Верстак та інструмент; дерево́, з якого роблять надовго.",
        "grandfather, mastery", "severity",
        "Grandfather is craft and stories: hands that know the work and a voice that kept the past. Skills of the kin pass not by words but by shared labor. Which family craft or story is waiting to be continued?",
        "Workbench and a tool; slow-growing wood meant to last.",
        "дедушка, мастерство", "строгость",
        "Дедушка — ремесло и истории: руки, знающие дело, и голос, сохранивший прошлое. Навыки рода передаются не словами, а общим делом. Какое ремесло или история твоего рода ждут продолжения?",
        "Верстак и инструмент; медленно растущее дерево, сделанное надолго.",
    ),
    "5": (
        "дитина, початок", "дитячі рани",
        "Внутрішня дитина — джерело свіжості, допитливості й гри в будь-якому віці. Якщо вона вийшла, вона проситься назад у твоє життя. Дозволь собі радість без «дорослої» причини — і заодно поглянь, які дитячі рани ще сумують за увагою.",
        "Мʼяч, що підстрибує; обличчя, яке дивиться на світ уперше.",
        "child, beginning", "childhood wounds",
        "The inner child is a source of freshness, curiosity and play at any age. If it appears, it is asking back into your life. Allow joy without an 'adult' reason — and see which childhood wounds still long for attention.",
        "A bouncing ball; a face seeing the world for the first time.",
        "ребёнок, начало", "детские раны",
        "Внутренний ребёнок — источник свежести, любопытства и игры в любом возрасте. Если он вышел, он просится обратно в твою жизнь. Позволь радость без «взрослого» повода — и посмотри, какие детские раны всё ещё ждут внимания.",
        "Прыгающий мяч; лицо, впервые видящее мир.",
    ),
    "6": (
        "рід, належність", "розрив звʼязків",
        "Рід — сотні плечей за спиною, навіть коли ти їх не бачиш. Приналежність дає безпеку: ти не починаєш з нуля, за тобою покоління. Карта просить відчути опору роду й повернути собі місце в його історії.",
        "Гіллясте дерево з одним стовбуром; ланцюг рук, що не розмикається.",
        "kin, belonging", "broken ties",
        "The kin is hundreds of shoulders behind you, even unseen. Belonging is safety: you do not start from zero. This card asks you to feel the support of your lineage and take your place in its story.",
        "A branching tree with a single trunk; an unbroken chain of hands.",
        "род, принадлежность", "разрыв связей",
        "Род — сотни плеч за спиной, даже когда ты их не видишь. Принадлежность даёт безопасность: ты начинаешь не с нуля. Карта просит ощутить опору рода и вернуть себе место в его истории.",
        "Ветвистое дерево с одним стволом; неразмыкающаяся цепь рук.",
    ),
    "7": (
        "дім, затишок", "бездомність душі",
        "Дім — це не стіни, а місце відновлення, де душа знімає маску. Карта питає: чи існує в твоєму житті тиха кімната без боргів, обовʼязків і чужих очікувань? Якщо ні — почни хоча б із маленького кута.",
        "Поріг, за яким починається безпека; вогник у вікні.",
        "home, shelter", "homelessness of the soul",
        "Home is not walls but a place of renewal where the soul takes off its mask. Does a quiet room without debts and other people's expectations exist in your life? If not, start with a small corner.",
        "A threshold where safety begins; a light in the window.",
        "дом, уют", "бездомность души",
        "Дом — это не стены, а место восстановления, где душа снимает маску. Есть ли в твоей жизни тихая комната без долгов и чужих ожиданий? Если нет — начни хотя бы с маленького угла.",
        "Порог, за которым начинается безопасность; огонёк в окне.",
    ),
    "8": (
        "спадок, дар", "тягар минулого",
        "Спадок — не лише речі й гроші, а сила, погляди та здібності, отримані безкоштовно. Одне й те саме минуле можна нести як дар або як тягар. Карта пропонує чесно розділити: що з отриманого береш із вдячністю, а що лишаєш далі?",
        "Скриня, що відчиняється з двох боків — віддавати й отримувати.",
        "inheritance, gift", "burden of the past",
        "Inheritance is not only objects: it is strength, views and talents received for free. The same past can be carried as a gift or a burden. Decide honestly: what do you take with gratitude and what do you leave behind?",
        "A chest opening from both sides — to give and to receive.",
        "наследство, дар", "груз прошлого",
        "Наследство — не только вещи, но и сила, взгляды и способности, полученные даром. Одно и то же прошлое можно нести как дар или как груз. Что ты берёшь с благодарностью, а что оставляешь дальше?",
        "Сундук, открывающийся с двух сторон — отдавать и получать.",
    ),
    "9": (
        "коріння, стійкість", "відрив від коренів",
        "Коріння тримає в бурю: людина без роду легко зноситься вітром обставин. Карта просить згадати своїх людей, мову, місця — те, що дає вертикаль, коли колише горизонтально. Хто твої люди, до яких можна повернутися?",
        "Коріння дуба, що йдуть глибше за крону; живлюща вода під землею.",
        "roots, resilience", "uprootedness",
        "Roots hold in a storm; a person without kin is easily blown by circumstances. Recall your people, language and places — what gives a vertical anchorage when life sways. Who are your people to return to?",
        "Oak roots going deeper than the crown; lifegiving water underground.",
        "корни, устойчивость", "отрыв от корней",
        "Корни держат в бурю: человек без рода легко сносится ветром обстоятельств. Вспомни своих людей, язык, места — то, что даёт вертикаль, когда качает по горизонтали. Кто твои люди, к которым можно вернуться?",
        "Корни дуба, идущие глубже кроны; живительная вода под землёй.",
    ),
    "10": (
        "крила, свобода", "страх висоти",
        "Крила ростуть із довіри: рід дає не лише коріння, а й дозвіл летіти. Карта просить не підмінювати свободу відірваністю — можна мати міцне коріння й сміливо літати. Куди ти не дозволяєш собі полетіти?",
        "Пірʼя, підхоплене вітром; птах, що повертається до гнізда, але високо.",
        "wings, freedom", "fear of heights",
        "Wings grow from trust: the kin gives not only roots but permission to fly. Do not trade freedom for detachment — you can have strong roots and fly boldly. Where do you not allow yourself to go?",
        "Feathers caught by the wind; a bird returning to the nest, yet high.",
        "крылья, свобода", "страх высоты",
        "Крылья растут из доверия: род даёт не только корни, но и разрешение лететь. Не подменяй свободу оторванностью — можно иметь крепкие корни и смело летать. Куда ты себе не позволяешь полететь?",
        "Перья, подхваченные ветром; птица, возвращающаяся к гнезду, но высоко.",
    ),
    "11": (
        "прощення", "помста",
        "Прощення розвʼязує вузли роду: непрощена образа передається далі мовчки, як естафета болю. Пробачити — не виправдати, а зняти з себе вантаж несення чужої рани. Кого в твоїй історії час відпустити?",
        "Розвʼязаний вузол, який перетворюється на пряму нитку.",
        "forgiveness", "revenge",
        "Forgiveness unties the knots of the lineage: an unforgiven offence passes on in silence, like a relay of pain. To forgive is not to justify, but to unburden yourself from carrying another's wound. Whom is it time to release?",
        "An untied knot becoming a straight thread.",
        "прощение", "месть",
        "Прощение развязывает узлы рода: непрощённая обида передаётся дальше молча, как эстафета боли. Простить — не оправдать, а снять с себя ношу несения чужой раны. Кого в твоей истории пора отпустить?",
        "Развязанный узел, ставший прямой нитью.",
    ),
    "12": (
        "коло, цілісність", "розімкнене коло",
        "Коло — знак завершеності: кожна роль роду на своєму місці, ніщо не тягне назад. Коли коло замикається, стає видно цілу картину. Подякуй усім, кому зобовʼязаний, — і займи своє місце в колі без почуття провини.",
        "Вінок без початку й кінця; хоровод, де кожен і за себе, і за всіх.",
        "circle, wholeness", "broken circle",
        "The circle marks completion: every role of the kin in its place, nothing pulls back. When the circle closes, the whole picture becomes visible. Thank everyone you owe — and take your place without guilt.",
        "A wreath without beginning or end; a round dance where each is for all.",
        "круг, целостность", "разомкнутый круг",
        "Круг — знак завершённости: каждая роль рода на своём месте, ничто не тянет назад. Когда круг замыкается, видна целая картина. Поблагодари всех, кому обязан, — и займи своё место без чувства вины.",
        "Венок без начала и конца; хоровод, где каждый и за себя, и за всех.",
    ),
}

# ============================ NUMEROLOGY 12 ============================
NUM = {
    "1": (
        "початок, лідерство", "егоїзм",
        "Одиниця — точка відліку, воля й ініціатива. Усе велике починається з одного кроку, з імпульсу «я можу». Зараз час діяти самостійно, не чекаючи дозволу. Лідерство тут — не тиск, а готовність іти першим і підніматися після падінь.",
        "Крапка як початок координат; стовп, що зʼєднує небо і землю.",
        "beginning, leadership", "egoism",
        "One is the starting point: will and initiative. Everything great begins with a single step, with the impulse 'I can'. Now is the time to act independently, without waiting for permission. Leadership means the readiness to go first and rise after falls.",
        "A point as the origin of coordinates; a pillar joining heaven and earth.",
        "начало, лидерство", "эгоизм",
        "Единица — точка отсчёта, воля и инициатива. Всё великое начинается с одного шага, с импульса «я могу». Сейчас время действовать самостоятельно, не ожидая разрешения. Лидерство — готовность идти первым и подниматься после падений.",
        "Точка как начало координат; столб, соединяющий небо и землю.",
    ),
    "2": (
        "пара, баланс", "залежність",
        "Двійка — пара, баланс і дипломатія: бачити обидва береги, згладжувати кути без втрати себе. Сила — у співпраці й терпінні. Остережись другого полюса: залежності від чужої думки. Домовляйся, але не розчиняйся.",
        "Дві крапки в ряд; шальки терезів, що шукають рівноваги.",
        "pair, balance", "dependence",
        "Two is the pair: balance and diplomacy — seeing both banks and smoothing corners without losing yourself. Your strength is cooperation and patience. Beware dependence on others' opinions: negotiate, but do not dissolve.",
        "Two points in a row; the pans of a scale seeking equilibrium.",
        "пара, баланс", "зависимость",
        "Двойка — пара, баланс и дипломатия: видеть оба берега, сглаживать углы, не теряя себя. Сила — в сотрудничестве и терпении. Остерегайся зависимости от чужого мнения: договаривайся, но не растворяйся.",
        "Две точки в ряд; чаши весов, ищущие равновесия.",
    ),
    "3": (
        "творчість, радість", "балакучість",
        "Трійка — творчий вибух, радість і самовираження: енергія, що рветься назовні словом, пензлем чи жестом. Блоки спадають, коли починаєш творити вголос, а не в чернетках. Стережися порожньої балаканини, що маскує страх бути незрозумілим.",
        "Трикутник — стійка форма; три іскри одного вогню.",
        "creativity, joy", "chatter",
        "Three is a creative burst: joy and self-expression, energy breaking outward through word, brush or gesture. Blocks fall when you begin to create aloud rather than in drafts. Beware idle chatter that masks the fear of being misunderstood.",
        "A triangle — a stable form; three sparks of one fire.",
        "творчество, радость", "болтливость",
        "Тройка — творческий взрыв, радость и самовыражение: энергия рвётся наружу словом, кистью или жестом. Блоки спадают, когда начинаешь творить вслух. Остерегайся пустой болтовни, маскирующей страх быть непонятым.",
        "Треугольник — устойчивая форма; три искры одного огня.",
    ),
    "4": (
        "фундамент, порядок", "застій",
        "Четвірка — фундамент, порядок і надійність: те, що стоїть на чотирьох кутах. Краса результату — у твердій основі, а не в блиску фасаду. Якщо справи хитаються, перевір фундамент: режим, дім, регулярність. Але не застигай у формі заради самої форми.",
        "Квадрат — перша замкнена форма; чотири стіни дому, чотири сторони світу.",
        "foundation, order", "stagnation",
        "Four is the foundation: order and reliability, what stands on four corners. Beauty lies in a solid base, not a shiny facade. If things wobble, check the foundation — routine, home, regularity — but do not freeze into form for its own sake.",
        "A square — the first closed form; four walls of a home, four directions.",
        "фундамент, порядок", "застой",
        "Четвёрка — фундамент, порядок и надёжность: то, что стоит на четырёх углах. Красота результата — в твёрдой основе. Если дела шатаются, проверь фундамент: режим, дом, регулярность. Но не застывай в форме ради формы.",
        "Квадрат — первая замкнутая форма; четыре стены дома, четыре стороны света.",
    ),
    "5": (
        "зміни, свобода", "хаос",
        "Пʼятірка — вітер змін і спрага свободи: коли старі форми тісні, а нові ще не виткані. Це не хаос, а перехідний стан, у якому важливо не вчепитися за поручні старого причалу. Довірся рухові — він несе туди, де простір.",
        "Пентаграма — зірка, окреслена з пʼяти рис; двері, прочинені вітром.",
        "change, freedom", "chaos",
        "Five is the wind of change and the thirst for freedom — when old forms are tight and new ones not yet woven. This is not chaos but a transition: do not cling to the old pier. Trust the movement; it carries you toward space.",
        "A pentagram drawn in five strokes; a door opened by the wind.",
        "перемены, свобода", "хаос",
        "Пятёрка — ветер перемен и жажда свободы: старые формы тесны, новые ещё не сотканы. Это не хаос, а переходное состояние: не цепляйся за перила старого причала. Доверься движению — оно несёт туда, где простор.",
        "Пентаграмма, начертанная пятью линиями; дверь, распахнутая ветром.",
    ),
    "6": (
        "гармонія, дім", "ідеалізм",
        "Шістка — гармонія, турбота й дім: відповідальність за близьких і краса в повсякденному. Мири там, де можливо, бережи тих, хто поруч. Тінь шістки — ідеалізм, що перетворює чуже життя на проєкт. Дозволь іншим бути недосконалими.",
        "Шестикутник — комірка стільника; дім, де кожен на своєму місці.",
        "harmony, home", "idealism",
        "Six is harmony, care and home: responsibility for those close and beauty in the everyday. Reconcile where possible; protect those near. The shadow of six is idealism that turns others' lives into a project — allow imperfection.",
        "A hexagon — a honeycomb cell; a home where each is in their place.",
        "гармония, дом", "идеализм",
        "Шестёрка — гармония, забота и дом: ответственность за близких и красота в повседневном. Мири, где возможно, береги тех, кто рядом. Тень шестёрки — идеализм, превращающий чужую жизнь в проект. Позволь другим быть несовершенными.",
        "Шестиугольник — ячейка сот; дом, где каждый на своём месте.",
    ),
    "7": (
        "аналіз, дух", "ізоляція",
        "Сімка — аналіз, тиша й пошук сенсу: відійти від шуму, щоб побачити глибше. Це час дослідження, а не рішень поспіхом. Самотність тут — ресурс мудреця, але бережися її перетворення на ізоляцію. Питай, копай, не на все відповідай зараз.",
        "Сім зірок Великої Ведмедиці; внутрішня кімната без дверей.",
        "analysis, spirit", "isolation",
        "Seven is analysis, stillness and the search for meaning: step away from noise to see deeper. Time for study, not hasty decisions. Solitude is a sage's resource, but beware it turning into isolation. Question and dig — not everything needs an answer now.",
        "The seven stars of the Big Dipper; an inner room without doors.",
        "анализ, дух", "изоляция",
        "Семёрка — анализ, тишина и поиск смысла: отойти от шума, чтобы увидеть глубже. Время исследования, а не поспешных решений. Одиночество — ресурс мудреца, но берегись изоляции. Вопрошай, копай, не на всё отвечай сейчас.",
        "Семь звёзд Большой Медведицы; внутренняя комната без дверей.",
    ),
    "8": (
        "сила, гроші", "трудоголізм",
        "Вісімка — матеріальна сила, влада й результат: енергія, що вміє примножуватися через справу. Успіх приходить через масштаб і дисципліну, а не через випадковість. Тінь числа — трудоголізм, коли праця стає втечею. Працюй як майстер, відпочивай як господар.",
        "Знак нескінченності — два кільця, замкнені в одному коловороті.",
        "power, money", "workaholism",
        "Eight is material power and result: energy that multiplies through labor. Success comes through scale and discipline, not chance. Its shadow is workaholism — work as a master, rest as an owner.",
        "The sign of infinity — two rings locked in one turn.",
        "сила, деньги", "трудоголизм",
        "Восьмёрка — материальная сила, власть и результат: энергия, умеющая приумножаться через дело. Успех приходит через масштаб и дисциплину. Тень — трудоголизм. Работай как мастер, отдыхай как хозяин.",
        "Знак бесконечности — два кольца в одном обороте.",
    ),
    "9": (
        "мудрість, завершення", "жертовність",
        "Девʼятка — завершення циклу й мудрість досвіду: час збирати підсумки, а не нові проєкти. Це фінальна щедрість — віддати накопичене, щоб коло замкнулося. Тінь числа — жертовність заради гасіння провини. Відпускай із вдячністю, а не з порожнечею.",
        "Коло, що замикає себе; урожай, знятий до останнього колоса.",
        "wisdom, completion", "self-sacrifice",
        "Nine is the completion of a cycle and the wisdom of experience: time to sum up, not open new projects. Final generosity — give what was accumulated so the circle closes. Its shadow is sacrifice meant to quiet guilt. Let go with gratitude, not emptiness.",
        "A circle closing on itself; a harvest reaped to the last ear.",
        "мудрость, завершение", "жертвенность",
        "Девятка — завершение цикла и мудрость опыта: время подводить итоги, а не открывать новые проекты. Финальная щедрость — отдать накопленное, чтобы круг замкнулся. Тень — жертвенность ради успокоения вины. Отпускай с благодарностью, не с пустотой.",
        "Круг, замыкающий себя; урожай, снятый до последнего колоса.",
    ),
    "11": (
        "натхнення, канал", "нервовість",
        "Одинадцять — майстер-число натхнення: двійка, піднесена до рівня каналу. Тонке сприйняття відкриває ідеї, що приходять нізвідки. Це час високих прозрінь і нервового напруження: не все, що «спустилося», треба втілювати цього дня. Записуй осяяння й обирай зріло.",
        "Два стовпи, зʼєднані перекладиною; антена, що ловить невидимі хвилі.",
        "inspiration, channel", "nervousness",
        "Eleven is the master number of inspiration: a two raised to a channel. Fine perception opens ideas that come from nowhere. A time of insight and tension: not everything that 'descends' must be realized today. Write revelations down and choose maturely.",
        "Two pillars joined by a lintel; an antenna catching invisible waves.",
        "вдохновение, канал", "нервозность",
        "Одиннадцать — мастер-число вдохновения: двойка, поднятая до уровня канала. Тонкое восприятие открывает идеи из ниоткуда. Время прозрений и нервного напряжения. Записывай озарения и выбирай зрело.",
        "Два столба, соединённые перекладиной; антенна, ловящая невидимые волны.",
    ),
    "22": (
        "будівництво", "мегаломанія",
        "Двадцять два — майстер-будівничий: найвища практична сила, здатна втілювати великі мрії. Тут поєднуються бачення й земля — починай з креслення, але доводь до цегли. Тінь числа 22 — велич, що втратила контакт із реальністю. Мрій масштабно, будуй по цеглині.",
        "Храм на міцній основі; сходи між небом і землею.",
        "master builder", "megalomania",
        "Twenty-two is the master builder: the highest practical power that turns great dreams into form. Vision meets the ground — start with a blueprint, but reach the brick. Its shadow is greatness that lost contact with reality. Dream big, build brick by brick.",
        "A temple on a firm base; a ladder between heaven and earth.",
        "строитель", "мегаломания",
        "Двадцать два — мастер-строитель: высшая практическая сила, воплощающая большие мечты. Ясновидение встречает землю — начинай с чертежа, но доводи до кирпича. Тень — величие, потерявшее связь с реальностью. Мечтай масштабно, строй по кирпичу.",
        "Храм на прочном основании; лестница между небом и землёй.",
    ),
    "33": (
        "служіння, любов", "жертовність",
        "Тридцять три — майстер-число служіння: любов, що піднімається до рівня щоденної практики. Давати іншим — природний стан цього числа, і віддача повертається сторицею. Тінь — самозгоряння заради чужих проєктів. Памʼятай: добро, що не шкодить джерелу, — єдине стійке.",
        "Серце, що гріє, не згасаючи; три кола опіки в кожному ширшому.",
        "service, love", "self-sacrifice",
        "Thirty-three is the master number of service: love raised to daily practice. Giving is natural for this number, and return comes hundredfold. Its shadow is self-immolation for others' projects. Remember: the good that does not harm its source is the only lasting kind.",
        "A heart that warms without fading; three circles of care, each wider.",
        "служение, любовь", "жертвенность",
        "Тридцать три — мастер-число служения: любовь, поднятая до ежедневной практики. Отдавать — естественно для этого числа, и отдача возвращается сторицей. Тень — самосгорание ради чужих проектов. Помни: добро, не вредящее источнику, — единственное устойчивое.",
        "Сердце, греющее не угасая; три круга заботы, каждый шире.",
    ),
}


def main():
    for fname, enrich, keep_fields in (
        ("moon_oracle8.json", MOON, ("element", "arcana_type")),
        ("ancestors12.json", KIN, ("arcana_type",)),
        ("numerology12.json", NUM, ("arcana_type", "numerology")),
    ):
        p = CARDS_DIR / fname
        data = json.loads(p.read_text(encoding="utf-8"))
        for c in data["cards"]:
            num = str(c["number"])
            e = enrich[num]
            c["keywords_upright"], c["keywords_reversed"] = e[0], e[1]
            c["meaning_general"], c["symbolism"] = e[2], e[3]
            t = c.get("translations", {})
            t["en"].update({
                "keywords_upright": e[4], "keywords_reversed": e[5],
                "meaning_general": e[6], "symbolism": e[7],
            })
            t["ru"].update({
                "keywords_upright": e[8], "keywords_reversed": e[9],
                "meaning_general": e[10], "symbolism": e[11],
            })
            c["translations"] = t
            # упорядкований порядок ключів для читабельності дифів
            ordered = {k: c[k] for k in
                       ("number", "name", "arcana_type", "element", "planet", "numerology",
                        "keywords_upright", "keywords_reversed", "meaning_general",
                        "meaning_love", "meaning_career", "meaning_health", "symbolism",
                        "image_path", "model_3d_path", "translations") if k in c}
            data["cards"][data["cards"].index(c)] = ordered
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] {fname}: {len(data['cards'])} карт збагачено")


if __name__ == "__main__":
    main()