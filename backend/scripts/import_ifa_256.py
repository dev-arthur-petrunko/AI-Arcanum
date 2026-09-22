"""Заміна колоди «Іфа · 16 Оду» на повну «Іфа · 256 Оду» (16 Meji + 240 Omo).

Джерело: ifa-wisdom.com/en/library (вбудований JSON сторінки бібліотеки, 256 записів),
скопійовано в Database/raw/ifa_256_source.json. Поля кожного запису:
  slug, nome, numero (16 meji 1–16, omoluo None), binario (8-біт, 2 стовпці x 4),
  isMeji, significadoNome, sintese, essencia, epiteto, ire, osogbo, filosofia/esse (meji).

Верифіковано: 16 meji + 240 omoluo = 256 унікальних; для omoluo
ire == ire першого батька, osogbo == osogbo другого батька (240/240).
sintese omoluo = шаблон "...strength of A (essA) ... wisdom of B (essB)" (240/240).

Переклад: базові поля укр (власний переказ), EN з сайту, RU — переклад.
Nazви карт — йорубською латиницею (інваріантні для всіх мов).
Для omoluo sintese/essencia збираються тримовно з батьківських meji.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.models.models import Card, Deck, System  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "Database", "raw", "ifa_256_source.json")
DECK_NAME_UK = "Іфа · 256 Оду"
DECK_NAME_EN = "Ifá · 256 Odu"
DECK_NAME_RU = "Ифа · 256 Оду"
SYSTEM_NAME = "Іфа"
SOURCE_URL = "https://www.ifa-wisdom.com/en/library"

# ── 16 Meji: тримовні власні перекази ключових полів ────────────────────────
# Ключ = slug meji. Кожен має: ess (essencia), synth (sintese-скорочена),
# ire, oso (osogbo), epit (короткий афоризм для назви змісту).
MEJI_TRL = {
    "ogbe": {
        "en": {"name": "Eji Ogbe", "ess": "Light, renewal, and open paths",
               "syn": "The first and brightest of the Mejis: light, renewal and leadership, announcing open roads.",
               "ire": "Long-lasting health, victory over adversaries, blessed descendants, and clean paths for great enterprises.",
               "oso": "May bring arrogance, isolation from excessive confidence, or the challenge of not being able to delegate.",
               "epit": "Auspicious, a new dawn, limitless possibilities."},
        "uk": {"name": "Еджі Огбе", "ess": "Світло, оновлення та відкриті шляхи",
               "syn": "Перший і найсвітліший з меджі: світло, оновлення й лідерство; поява обіцяє відкриті дороги.",
               "ire": "Міцне здоров'я, перемога над суперниками, благословенні нащадки й чисті шляхи для великих справ.",
               "oso": "Може принести гординю, ізоляцію від надмірної самовпевненості та невміння делегувати.",
               "epit": "Сприятливий, новий світанок, безмежні можливості."},
        "ru": {"name": "Эджи Огбе", "ess": "Свет, обновление и открытые пути",
               "syn": "Первый и самый светлый из межджи: свет, обновление и лидерство; появление обещает открытые дороги.",
               "ire": "Крепкое здоровье, победа над соперниками, благословенное потомство и чистые пути для больших дел.",
               "oso": "Может принести гордыню, изоляцию от чрезмерной самоуверенности и неумение делегировать.",
               "epit": "Благоприятный, новая заря, безграничные возможности."},
    },
    "oyeku": {
        "en": {"name": "Oyeku Meji", "ess": "Closure, ancestry, and rebirth",
               "syn": "The Odu of closure, mourning and deep transformation: without symbolic death there is no rebirth.",
               "ire": "Protection of the Egungun (ancestors), end of toxic cycles, longevity gained by respecting what needs to die.",
               "oso": "Material losses, encounters with Iku (symbolic death), prolonged sadness if there is no Ebó.",
               "epit": "Contraction, rest, the death required for transformation."},
        "uk": {"name": "Ойєку Межі", "ess": "Завершення, предки та переродження",
               "syn": "Оду завершення, скорботи й глибокої трансформації: без символічної смерті немає переродження.",
               "ire": "Захист предків (Egungun), завершення токсичних циклів, довголіття через повагу до того, що має відійти.",
               "oso": "Матеріальні втрати, зустріч з Іку (символічна смерть), тривала сумовитість без Ебо.",
               "epit": "Стиснення, відпочинок, смерть, потрібна для перетворення."},
        "ru": {"name": "Ойеку Межджи", "ess": "Завершение, предки и перерождение",
               "syn": "Оду завершения, скорби и глубокой трансформации: без символической смерти нет перерождения.",
               "ire": "Защита предков (Egungun), завершение токсичных циклов, долголетие через уважение к тому, что должно уйти.",
               "oso": "Материальные потери, встреча с Ику (символическая смерть), затяжная печаль без Эбо.",
               "epit": "Сжатие, отдых, смерть, необходимая для превращения."},
    },
    "iwori": {
        "en": {"name": "Iwori Meji", "ess": "Inner sight, intuition, and mystery",
               "syn": "The Odu of inner vision and intuition as a guide: trust what you feel even when the world says otherwise.",
               "ire": "Important revelations, awakened spiritual gifts, success in deep studies.",
               "oso": "Mental confusion, heavy dreams, feeling surrounded by envy if one does not strengthen their Orí.",
               "epit": "Sharpness, quick intelligence, shrewd communication."},
        "uk": {"name": "Іворі Межі", "ess": "Внутрішній зір, інтуїція та таємниця",
               "syn": "Оду внутрішнього бачення й інтуїції як провідника: довіряй відчуттям, навіть коли світ каже інакше.",
               "ire": "Важливі одкровення, пробуджені духовні дари, успіх у глибоких навчаннях.",
               "oso": "Плутанина думок, важкі сни, відчуття заздрості навколо, якщо не зміцнювати Орі.",
               "epit": "Гострота, швидкий розум, проникливе спілкування."},
        "ru": {"name": "Ивори Межджи", "ess": "Внутреннее зрение, интуиция и тайна",
               "syn": "Оду внутреннего видения и интуиции как проводника: доверяй ощущениям, даже когда мир говорит иначе.",
               "ire": "Важные откровения, пробуждённые духовные дары, успех в глубоких учениях.",
               "oso": "Спутанность мыслей, тяжёлые сны, ощущение зависти вокруг, если не укреплять Ори.",
               "epit": "Острота, быстрый ум, проницательное общение."},
    },
    "odi": {
        "en": {"name": "Odi Meji", "ess": "Foundation, intimacy, and protection",
               "syn": "The Odu of foundation, home, safety and intimate bonds: all that must be held, protected and nurtured to grow.",
               "ire": "Stable home, fertility (literal and symbolic), lasting unions, family protection.",
               "oso": "Heavy secrets, betrayals in the intimate circle, relationships that become prisons.",
               "epit": "Hard choices, the crossroads on the path of life."},
        "uk": {"name": "Оді Межі", "ess": "Фундамент, близькість і захист",
               "syn": "Оду основи, дому, безпеки й близьких зв'язків: усе, що треба берегти, захищати й плекати для зростання.",
               "ire": "Стабільний дім, родючість (пряма й символічна), тривкі союзи, захист родини.",
               "oso": "Важкі таємниці, зради в близькому колі, стосунки, що стають в'язницею.",
               "epit": "Важкі вибори, роздоріжжя на життєвому шляху."},
        "ru": {"name": "Оди Межджи", "ess": "Фундамент, близость и защита",
               "syn": "Оду основы, дома, безопасности и близких связей: всё, что нужно беречь, защищать и лелеять для роста.",
               "ire": "Стабильный дом, плодородие (прямое и символическое), прочные союзы, защита семьи.",
               "oso": "Тяжёлые тайны, предательства в близком кругу, отношения, ставшие тюрьмой.",
               "epit": "Трудные выборы, перекрёсток на жизненном пути."},
    },
    "irosun": {
        "en": {"name": "Irosun Meji", "ess": "Memory, heritage, and commitment",
               "syn": "The Odu of memory, blood, ancestral heritage and old commitments: what appears here has deep roots.",
               "ire": "Recovery of something lost, return of beloved people, success in just and old causes.",
               "oso": "Spiritual debts, physical symptoms with ancestral origin, family wounds to resolve.",
               "epit": "Fertility, wealth, sensuality and full abundance."},
        "uk": {"name": "Іросун Межі", "ess": "Пам'ять, спадщина та зобов'язання",
               "syn": "Оду пам'яті, крові, спадщини предків і давніх зобов'язань: те, що тут з'являється, має глибоке коріння.",
               "ire": "Повернення втраченого, повернення близьких людей, успіх у справедливих і давніх справах.",
               "oso": "Духовні борги, фізичні симптоми родового походження, родинні рани, які треба загоїти.",
               "epit": "Родючість, багатство, чуттєвість і повна щедрість."},
        "ru": {"name": "Иросун Межджи", "ess": "Память, наследие и обязательства",
               "syn": "Оду памяти, крови, наследия предков и старых обязательств: то, что здесь появляется, имеет глубокие корни.",
               "ire": "Возвращение утраченного, возвращение близких людей, успех в справедливых и давних делах.",
               "oso": "Духовные долги, физические симптомы родового происхождения, семейные раны, которые нужно заживить.",
               "epit": "Плодородие, богатство, чувственность и полное изобилие."},
    },
    "owonrin": {
        "en": {"name": "Owonrin Meji", "ess": "Movement, change, and journey",
               "syn": "The Odu of movement, change, travel (inner and outer) and the inability to stand still.",
               "ire": "Profitable journeys, changes that bring growth, liberation from stagnant situations.",
               "oso": "Restlessness turning into anxiety, hasty decisions, loss of direction from excessive hurry.",
               "epit": "Vanity, illusion, and the mirror that does not reflect truth."},
        "uk": {"name": "Овонрін Межі", "ess": "Рух, зміни та подорож",
               "syn": "Оду руху, змін, подорожей (внутрішніх і зовнішніх) і нездатності стояти на місці.",
               "ire": "Прибуткові подорожі, зміни, що приносять зростання, звільнення від застою.",
               "oso": "Невгамовність, що стає тривогою, поспішні рішення, втрата напрямку через надмірну квапливість.",
               "epit": "Марнославство, ілюзія, дзеркало, що не відображає правди."},
        "ru": {"name": "Овонрин Межджи", "ess": "Движение, перемены и путешествие",
               "syn": "Оду движения, перемен, путешествий (внутренних и внешних) и неспособности стоять на месте.",
               "ire": "Прибыльные поездки, перемены, несущие рост, освобождение от застоя.",
               "oso": "Неугомонность, переходящая в тревогу, поспешные решения, потеря направления из-за спешки.",
               "epit": "Тщеславие, иллюзия, зеркало, не отражающее правды."},
    },
    "obara": {
        "en": {"name": "Obara Meji", "ess": "Abundance, word, and prosperity",
               "syn": "The Odu of abundance, creative speech, prosperity earned through right words and public recognition.",
               "ire": "Material wealth, success in business, recognition for what one says and teaches.",
               "oso": "Empty promises, hurtful words, loss of credibility through exaggeration.",
               "epit": "Authority, power, and the legitimate command of the courageous leader."},
        "uk": {"name": "Обара Межі", "ess": "Достаток, слово та процвітання",
               "syn": "Оду достатку, творчого слова, процвітання через правильні слова та суспільного визнання.",
               "ire": "Матеріальний достаток, успіх у справах, визнання за сказане й навчене.",
               "oso": "Порожні обіцянки, ранячі слова, втрата довіри через перебільшення.",
               "epit": "Авторитет, влада й легітимне керівництво сміливого лідера."},
        "ru": {"name": "Обара Межджи", "ess": "Изобилие, слово и процветание",
               "syn": "Оду изобилия, творческого слова, процветания через правильные слова и общественного признания.",
               "ire": "Материальное богатство, успех в делах, признание за сказанное и наученное.",
               "oso": "Пустые обещания, ранящие слова, потеря доверия из-за преувеличения.",
               "epit": "Авторитет, власть и легитимное руководство смелого лидера."},
    },
    "okanran": {
        "en": {"name": "Okanran Meji", "ess": "Courage, defense, and determination",
               "syn": "The Odu of raw strength, decisions with no turning back and defense against attack.",
               "ire": "Victory in conflicts, protection against enemies, strength to defend what is yours.",
               "oso": "Fights, uncontrolled aggressiveness, wrong decisions made in the heat of the moment.",
               "epit": "Incomplete blessing, success that has not yet reached its end."},
        "uk": {"name": "Оканран Межі", "ess": "Мужність, захист і рішучість",
               "syn": "Оду грубої сили, рішень без шляху назад і захисту від нападу.",
               "ire": "Перемога в конфліктах, захист від ворогів, сила обстоювати своє.",
               "oso": "Сварки, неконтрольована агресивність, неправильні рішення в запалі.",
               "epit": "Неповне благословення, успіх, що ще не дійшов кінця."},
        "ru": {"name": "Оканран Межджи", "ess": "Мужество, защита и решимость",
               "syn": "Оду грубой силы, решений без пути назад и защиты от нападения.",
               "ire": "Победа в конфликтах, защита от врагов, сила отстаивать своё.",
               "oso": "Ссоры, неконтролируемая агрессивность, неверные решения в запале.",
               "epit": "Неполное благословение, успех, ещё не достигший конца."},
    },
    "ogunda": {
        "en": {"name": "Ogunda Meji", "ess": "Work, clearing obstacles, and victory through effort",
               "syn": "Ogum's Odu: hard work, clearing new ground, and victories won by effort.",
               "ire": "Success through work, opening of new fronts, tools and means arrive when needed.",
               "oso": "Cuts, accidents, exhaustion from excess work, conflicts in the professional environment.",
               "epit": "War, necessary conflict, the struggle against evil."},
        "uk": {"name": "Огунда Межі", "ess": "Праця, розчищення перешкод і перемога зусиллям",
               "syn": "Оду Огуна: тяжка праця, розчищення нового ґрунту й перемоги, здобуті зусиллям.",
               "ire": "Успіх через працю, відкриття нових напрямів; інструменти й засоби з'являються вчасно.",
               "oso": "Порізи, нещасні випадки, виснаження від надмірної праці, конфлікти на роботі.",
               "epit": "Війна, необхідний конфлікт, боротьба зі злом."},
        "ru": {"name": "Огунда Межджи", "ess": "Труд, расчистка препятствий и победа усилием",
               "syn": "Оду Огуна: тяжёлый труд, расчистка новой земли и победы, завоёванные усилием.",
               "ire": "Успех через труд, открытие новых фронтов; инструменты и средства приходят вовремя.",
               "oso": "Порезы, несчастные случаи, истощение от переработки, конфликты на работе.",
               "epit": "Война, необходимый конфликт, борьба со злом."},
    },
    "osa": {
        "en": {"name": "Osa Meji", "ess": "Freedom, the feminine, and invisible strength",
               "syn": "The Odu of freedom, the sacred feminine, the Iyami, and strength that comes from knowing how to let go.",
               "ire": "Liberation from bonds, protection of the Iyami, awakened feminine spiritual gifts.",
               "oso": "Conflicts with women in the family, mysterious illnesses, feeling persecuted without visible reason.",
               "epit": "Spirituality, mediation and connection with the ancestral world."},
        "uk": {"name": "Оса Межі", "ess": "Свобода, жіноче начало й невидима сила",
               "syn": "Оду свободи, сакрального жіночого, Іямі та сили, що приходить від уміння відпускати.",
               "ire": "Звільнення від пут, захист Іямі, пробуджені жіночі духовні дари.",
               "oso": "Конфлікти з жінками в родині, незрозумілі хвороби, відчуття переслідування без причини.",
               "epit": "Духовність, медіація та зв'язок зі світом предків."},
        "ru": {"name": "Оса Межджи", "ess": "Свобода, женское начало и невидимая сила",
               "syn": "Оду свободы, сакрального женского начала, Иями и силы, приходящей от умения отпускать.",
               "ire": "Освобождение от уз, защита Иями, пробуждённые женские духовные дары.",
               "oso": "Конфликты с женщинами в семье, непонятные болезни, ощущение преследования без причины.",
               "epit": "Духовность, медиация и связь с миром предков."},
    },
    "ika": {
        "en": {"name": "Ika Meji", "ess": "Complexity, patience, and intelligence",
               "syn": "The Odu of complications and of the intelligence that unties the knot without cutting the cord.",
               "ire": "Intelligent solutions to old problems, success in difficult negotiations.",
               "oso": "Mental confusion, legal processes, situations that complicate the more one moves.",
               "epit": "Death in life, weakening and the need for restoration."},
        "uk": {"name": "Іка Межі", "ess": "Складність, терпіння та інтелект",
               "syn": "Оду ускладнень і розуму, що розв'язує вузол, не перерізаючи нитки.",
               "ire": "Розумні рішення старих проблем, успіх у складних переговорах.",
               "oso": "Плутанина думок, судові процеси, ситуації, що лише ускладнюються від рухів.",
               "epit": "Смерть за життя, ослаблення й потреба відновлення."},
        "ru": {"name": "Ика Межджи", "ess": "Сложность, терпение и интеллект",
               "syn": "Оду осложнений и ума, который распутывает узел, не разрезав нить.",
               "ire": "Умные решения старых проблем, успех в трудных переговорах.",
               "oso": "Спутанность мыслей, судебные процессы, ситуации, усложняющиеся от любых движений.",
               "epit": "Смерть при жизни, ослабление и потребность в восстановлении."},
    },
    "oturupon": {
        "en": {"name": "Oturupon Meji", "ess": "Responsibility, maturity, and quiet strength",
               "syn": "The Odu of the weight of responsibility and strength that grows in those who carry what is theirs without complaint.",
               "ire": "Recognition for seniority, wisdom acquired through experience, positions of spiritual leadership.",
               "oso": "Feeling overwhelmed, illnesses related to the weight of life, depression.",
               "epit": "Necessary sacrifice, the surrender that transforms destiny."},
        "uk": {"name": "Отурепон Межі", "ess": "Відповідальність, зрілість і тиха сила",
               "syn": "Оду тягаря відповідальності й сили, що зростає в тих, хто несе своє без скарг.",
               "ire": "Визнання старшинства, мудрість через досвід, позиції духовного лідерства.",
               "oso": "Відчуття перевантаження, хвороби, пов'язані з тягарем життя, депресія.",
               "epit": "Необхідна жертва, відданість, що перетворює долю."},
        "ru": {"name": "Отурепон Межджи", "ess": "Ответственность, зрелость и тихая сила",
               "syn": "Оду бремени ответственности и силы, растущей в тех, кто несёт своё без жалоб.",
               "ire": "Признание старшинства, мудрость через опыт, позиции духовного лидерства.",
               "oso": "Ощущение перегрузки, болезни, связанные с бременем жизни, депрессия.",
               "epit": "Необходимая жертва, преданность, преображающая судьбу."},
    },
    "otura": {
        "en": {"name": "Otura Meji", "ess": "Purity, faith, and connection with the sacred",
               "syn": "The Odu of purity, faith, authentic spirituality and direct connection with Olódùmarè.",
               "ire": "Renewed faith, strong spiritual protection, success in religious searches and healing missions.",
               "oso": "False religiosity, exploitation by false guides, spiritual deceptions.",
               "epit": "Patience, endurance, and victory won through time."},
        "uk": {"name": "Отура Межі", "ess": "Чистота, віра та зв'язок із сакральним",
               "syn": "Оду чистоти, віри, справжньої духовності й прямого зв'язку з Олодумаре.",
               "ire": "Оновлена віра, сильний духовний захист, успіх у релігійних пошуках і зціленні.",
               "oso": "Фальшива релігійність, експлуатація хибними наставниками, духовні обмани.",
               "epit": "Терпіння, витривалість і перемога, здобута часом."},
        "ru": {"name": "Отура Межджи", "ess": "Чистота, вера и связь со священным",
               "syn": "Оду чистоты, веры, подлинной духовности и прямой связи с Олодумаре.",
               "ire": "Обновлённая вера, сильная духовная защита, успех в религиозных поисках и исцелении.",
               "oso": "Ложная религиозность, эксплуатация ложными наставниками, духовные обманы.",
               "epit": "Терпение, выносливость и победа, завоёванная временем."},
    },
    "irete": {
        "en": {"name": "Irete Meji", "ess": "Perseverance, steadiness, and faith",
               "syn": "The Odu of perseverance, steadiness in discouragement, and faith that endures.",
               "ire": "Victory near after long struggle, recognition of merit, completion of long projects.",
               "oso": "Discouragement, desire to give up, feeling that effort is not worth it.",
               "epit": "Tempest, the storm that purifies and deeply renews."},
        "uk": {"name": "Ірете Межі", "ess": "Наполегливість, витримка та віра",
               "syn": "Оду наполегливості, стійкості у знегоді й віри, що триває.",
               "ire": "Перемога, близька після довгої боротьби, визнання заслуг, завершення довгих проєктів.",
               "oso": "Знеохочення, бажання кинути, відчуття, що зусилля не варті того.",
               "epit": "Буря, що очищає й глибоко оновлює."},
        "ru": {"name": "Ирете Межджи", "ess": "Настойчивость, выдержка и вера",
               "syn": "Оду настойчивости, стойкости в невзгодах и веры, которая длится.",
               "ire": "Победа, близкая после долгой борьбы, признание заслуг, завершение долгих проектов.",
               "oso": "Уныние, желание бросить, ощущение, что усилия не стоят того.",
               "epit": "Буря, очищающая и глубоко обновляющая."},
    },
    "ose": {
        "en": {"name": "Oshe Meji", "ess": "Love, beauty, and healing through waters",
               "syn": "Oxum's Odu: love, beauty, fertility and healing through waters — affection, grace and personal flourishing.",
               "ire": "True love, fertility, prosperity through relationships, recognized inner beauty.",
               "oso": "Excessive vanity, love dependence, fertility problems, conflicts from envy.",
               "epit": "Purification, spiritual cleansing and the healing of what is corrupted."},
        "uk": {"name": "Оше Межі", "ess": "Любов, краса та зцілення через води",
               "syn": "Оду Ошун: любов, краса, родючість і зцілення через води — лагідність, грація й розквіт.",
               "ire": "Справжнє кохання, родючість, процвітання через стосунки, визнана внутрішня краса.",
               "oso": "Надмірне марнославство, любовна залежність, проблеми з родючістю, конфлікти з заздрості.",
               "epit": "Очищення, духовне обмивання, зцілення зіпсованого."},
        "ru": {"name": "Оше Межджи", "ess": "Любовь, красота и исцеление через воды",
               "syn": "Оду Ошун: любовь, красота, плодородие и исцеление водами — нежность, грация и расцвет.",
               "ire": "Настоящая любовь, плодородие, процветание через отношения, признанная внутренняя красота.",
               "oso": "Чрезмерное тщеславие, любовная зависимость, проблемы с плодородием, конфликты из зависти.",
               "epit": "Очищение, духовное омовение, исцеление испорченного."},
    },
    "ofun": {
        "en": {"name": "Ofun Meji", "ess": "Ancient wisdom, longevity, and tradition",
               "syn": "The eldest Odu — 'Olófin', lord of the palace: wisdom, longevity, protection by the elders and respect for tradition.",
               "ire": "Long life, respect conquered, protection of the eldest Orixás (Oxalá, Nanã, Iroko).",
               "oso": "Diseases associated with age, conflicts from disrespect to an elder, isolation.",
               "epit": "Plenitude, totality and the supreme fulfilment of the creative will."},
        "uk": {"name": "Офун Межі", "ess": "Давня мудрість, довголіття та традиція",
               "syn": "Найдавніший Оду — «Олофін», володар палацу: мудрість, довголіття, захист старших і повага до традиції.",
               "ire": "Довге життя, завойована повага, захист найстарших Орішá (Ошала, Нана, Іроко).",
               "oso": "Хвороби, пов'язані з віком, конфлікти через неповагу до старших, ізоляція.",
               "epit": "Повнота, цілісність і вище втілення творчої волі."},
        "ru": {"name": "Офун Межджи", "ess": "Древняя мудрость, долголетие и традиция",
               "syn": "Древнейший Оду — «Олофин», владыка дворца: мудрость, долголетие, защита старших и уважение к традиции.",
               "ire": "Долгая жизнь, завоёванное уважение, защита старейших Оришá (Ошала, Нана, Ироко).",
               "oso": "Болезни, связанные с возрастом, конфликты из-за неуважения к старшим, изоляция.",
               "epit": "Полнота, целостность и высшее воплощение творческой воли."},
    },
}

# Словник для перекладу epiteto omoluo (EN -> UK/RU) — власний переказ.
# 240 унікальних; щоб не генерувати вручну, використаємо шаблон:
# epiteto_uk = "{essensa_першого (uk)} + {essensa_другого (uk)}."
# Це коректно, бо epiteto omoluo описує саме поєднання двох полярностей.
# Додатково збережемо оригінальний EN epiteto у змістовному полі (ese).

# Порядок meji за numero
MEJI_ORDER = ["ogbe", "oyeku", "iwori", "odi", "irosun", "owonrin", "obara",
              "okanran", "ogunda", "osa", "ika", "oturupon", "otura",
              "irete", "ose", "ofun"]


# Короткі корені назв meji для компактних назв omoluo (slug -> [uk, ru]).
ROOT_TRL = {
    "ogbe": ("Огбе", "Огбе"), "oyeku": ("Ойєку", "Ойеку"), "iwori": ("Іворі", "Ивори"),
    "odi": ("Оді", "Оди"), "irosun": ("Іросун", "Иросун"), "owonrin": ("Овонрін", "Овонрин"),
    "obara": ("Обара", "Обара"), "okanran": ("Оканран", "Оканран"), "ogunda": ("Огунда", "Огунда"),
    "osa": ("Оса", "Оса"), "ika": ("Іка", "Ика"), "oturupon": ("Отурепон", "Отурепон"),
    "otura": ("Отура", "Отура"), "irete": ("Ірете", "Ирете"), "ose": ("Оше", "Оше"),
    "ofun": ("Офун", "Офун"),
}


def omoluo_fields(slug):
    """Тримовні поля для omoluo з батьківських meji."""
    a, b = slug.split("-")
    A = MEJI_TRL[a]
    B = MEJI_TRL[b]
    out = {}
    for lang in ("uk", "en", "ru"):
        ig = lang if lang != "en" else "en"
        short_a = a if lang == "en" else ROOT_TRL[a][0 if lang == "uk" else 1]
        short_b = b if lang == "en" else ROOT_TRL[b][0 if lang == "uk" else 1]
        na, nb = A[lang]["name"], B[lang]["name"]
        ea, eb = A[lang]["ess"], B[lang]["ess"]
        stem_en = {"en": "A path that joins the strength of", "uk": "Шлях, що поєднує силу",
                   "ru": "Путь, соединяющий силу"}[lang]
        tail_en = {"en": "with the wisdom of", "uk": "з мудрістю", "ru": "с мудростью"}[lang]
        out[lang] = {
            "name": f"{short_a}–{short_b}",
            "ess": f"{ea} + {eb}",
            "syn": f"{stem_en} {na} ({ea}) {tail_en} {nb} ({eb}).",
            "ire": A[lang]["ire"],
            "oso": B[lang]["oso"],
            "epit": f"Поєднання полярностей: {ea} + {eb}.",
        }
    return out


def build_card(src, idx, trl):
    """Стійкі поля карти з tri-мов даними."""
    lang_pairs = {
        "uk": {"ess": "ess", "syn": "syn", "ire": "ire", "oso": "oso", "epit": "epit"},
        "en": {"ess": "ess", "syn": "syn", "ire": "ire", "oso": "oso", "epit": "epit"},
        "ru": {"ess": "ess", "syn": "syn", "ire": "ire", "oso": "oso", "epit": "epit"},
    }
    nm = {l: trl[l]["name"] for l in ("uk", "en", "ru")}
    ess = {l: trl[l]["ess"] for l in ("uk", "en", "ru")}
    syn = {l: trl[l]["syn"] for l in ("uk", "en", "ru")}
    ire = {l: trl[l]["ire"] for l in ("uk", "en", "ru")}
    oso = {l: trl[l]["oso"] for l in ("uk", "en", "ru")}
    epit = {l: trl[l]["epit"] for l in ("uk", "en", "ru")}

    is_meji = src.get("isMeji", False)
    card = {
        "number": str(idx),  # 1..256 наскрізний порядок сторінки бібліотеки
        "name": nm["uk"],
        "arcana_type": "Оду · Межі" if is_meji else "Оду · Омо",
        "category": "Оду Іфа",
        "suit": src.get("nome", ""),  # йорубська назва
        "suit_code": src.get("binario", ""),  # 8-біт діаграми
        "theme": ess["uk"],
        "keywords_upright": ire["uk"],
        "keywords_reversed": oso["uk"],
        "meaning_general": syn["uk"],
        "meaning_spirituality": epit["uk"],
        "meaning_reversed": oso["uk"],
        "symbolism": f"Бінарний код: {src.get('binario','')} · {src.get('nome','')}\n{src.get('epiteto','') or ''}",
        "translations": {
            "uk": {"name": nm["uk"], "theme": ess["uk"], "keywords_upright": ire["uk"],
                   "keywords_reversed": oso["uk"], "meaning_general": syn["uk"],
                   "meaning_spirituality": epit["uk"], "meaning_reversed": oso["uk"]},
            "en": {"name": nm["en"], "theme": ess["en"], "keywords_upright": ire["en"],
                   "keywords_reversed": oso["en"], "meaning_general": syn["en"],
                   "meaning_spirituality": epit["en"], "meaning_reversed": oso["en"]},
            "ru": {"name": nm["ru"], "theme": ess["ru"], "keywords_upright": ire["ru"],
                   "keywords_reversed": oso["ru"], "meaning_general": syn["ru"],
                   "meaning_spirituality": epit["ru"], "meaning_reversed": oso["ru"]},
        },
    }
    return card


def seed():
    with open(SRC, encoding="utf-8") as f:
        records = json.load(f)
    assert len(records) == 256, f"джерело має {len(records)} записів"
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    n_sys = n_deck = n_card = 0
    try:
        system = db.query(System).filter_by(name=SYSTEM_NAME).first()
        if not system:
            system = System(name=SYSTEM_NAME, category="гадательні",
                            history=("Система ворожіння народу йоруба: 16 головних Оду (Ojú Odù) і "
                                     "240 комбінованих (Omo Odù) — разом 256 знаків опритування."),
                            origin_country="Західна Африка (Нігерія, Куба, Бразилія), orphan",
                            approx_year=None,
                            translations={l: {"name": SYSTEM_NAME} for l in ("uk", "en", "ru")})
            db.add(system)
            db.flush()
            n_sys += 1
        # Ціль — колода з id 41 («Іфа · 16 Оду» замінюється повністю).
        deck = db.get(Deck, 41)
        if deck is None:
            deck = db.query(Deck).filter_by(name=DECK_NAME_UK).first()
        fields = {
            "name": DECK_NAME_UK,
            "system_id": system.id,
            "author": "AI-Arcanum (навчальна колода) · джерело ifa-wisdom.com",
            "publisher": None,
            "year": None,
            "card_count": 256,
            "source_url": SOURCE_URL,
            "directory_group": "Іфа",
            "is_reference_only": False,
            "is_partial": False,
            "description": ("Повна система Іфа: 16 Ojú Odù (меджі) та 240 Omo Odù (омо) — "
                            "усі 256 знаків з бінарними діаграмами, Ire/Osogbo. Тексти — власний тримовний "
                            "переказ джерела ifa-wisdom.com (вказано в профілі)."),
            "translations": {
                "uk": {"name": DECK_NAME_UK, "description": "Повна колода Іфа: 256 Оду (16 меджі + 240 омо)."},
                "en": {"name": DECK_NAME_EN, "description": "Complete Ifá deck: 256 Odu (16 Meji + 240 Omo)."},
                "ru": {"name": DECK_NAME_RU, "description": "Полная колода Ифа: 256 Оду (16 межджи + 240 омо)."},
            },
        }
        if deck:
            for k, v in fields.items():
                setattr(deck, k, v)
        else:
            deck = Deck(name=DECK_NAME_UK, **fields)
            db.add(deck)
            db.flush()
            n_deck += 1
        # видаляємо старі карти (16 Оду), зокрема і з попередніх хвиль
        old = db.query(Card).filter(Card.deck_id == deck.id).all()
        n_old = len(old)
        db.query(Card).filter(Card.deck_id == deck.id).delete()
        db.flush()
        num_to_idx = {}
        # meji йдуть першими за numero, потім omoluo в порядку джерела
        records = (sorted([r for r in records if r.get("isMeji")], key=lambda r: r.get("numero") or 0)
                   + [r for r in records if not r.get("isMeji")])
        idx = 0
        for rec in records:
            idx += 1
            slug = rec["slug"]
            if rec.get("isMeji"):
                trl = MEJI_TRL[slug]
            else:
                trl = omoluo_fields(slug)
            card = build_card(rec, idx, trl)
            db.add(Card(deck_id=deck.id, **card))
            n_card += 1
        db.commit()
        print(f"[ifa-256] систем: {n_sys} нових, колод: {n_deck} нових, старих карт видалено: {n_old}, додано: {n_card}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()