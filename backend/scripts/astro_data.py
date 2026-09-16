# -*- coding: utf-8 -*-
"""Астрологическая энциклопедия: знаки, планеты, дома, аспекты.

ASTRO = {slug: {"glyph": str, "ru": {"title", "body"}, "uk": {...}, "en": {...}}}
Тексты — собственные учебные формулировки по мотивам энциклопедий
astro.com и Cafe Astrology (система «Астрология», system='Астрология').
"""

ASTRO = {
    # ---------- ЗНАКИ ----------
    "astrology-aries": {
        "glyph": "♈",
        "ru": {"title": "Овен", "body": "Первый знак зодиака, стихия Огонь, управитель Марс (21.03–19.04). Овен открывает годовой цикл: инициатива, смелость, прямота и умение стартовать. Его энергия импульсивна и соревновательна — это воин, который любит быть первым. Сильные стороны: решительность, самостоятельность, запал. Уязвимости: нетерпеливость, вспыльчивость, склонность бросать дело на полпути, когда азарт угасает."},
        "uk": {"title": "Овен", "body": "Перший знак зодіаку, стихія Вогонь, управитель Марс (21.03–19.04). Овен відкриває річний цикл: ініціатива, сміливість, прямота й уміння стартувати. Його енергія імпульсивна й змагальна — це воїн, який любить бути першим. Сильні сторони: рішучість, самостійність, запал. Уразливості: нетерплячість, запальність, схильність кидати справу на півдорозі, коли азарт згасає."},
        "en": {"title": "Aries", "body": "The first sign of the zodiac, element Fire, ruled by Mars (Mar 21 – Apr 19). Aries opens the yearly cycle: initiative, courage, directness and the skill of starting. Its energy is impulsive and competitive — a warrior who loves to be first. Strengths: decisiveness, independence, drive. Vulnerabilities: impatience, temper, quitting halfway once the thrill fades."},
    },
    "astrology-taurus": {
        "glyph": "♉",
        "ru": {"title": "Телец", "body": "Второй знак, стихия Земля, управитель Венера (20.04–20.05). Телец ценит стабильность, комфорт и чувственную красоту мира. Это строитель и хранитель: упорный, надёжный, щедрый к своим. Сильные стороны: терпение, практичность, верность. Уязвимости: упрямство, сопротивление переменам, привязанность к удобству и обладанию."},
        "uk": {"title": "Телець", "body": "Другий знак, стихія Земля, управитель Венера (20.04–20.05). Телець цінує стабільність, комфорт і чуттєву красу світу. Це будівничий і хранитель: наполегливий, надійний, щедрий до своїх. Сильні сторони: терпіння, практичність, вірність. Уразливості: впертість, опір змінам, прив'язаність до зручності й володіння."},
        "en": {"title": "Taurus", "body": "The second sign, element Earth, ruled by Venus (Apr 20 – May 20). Taurus values stability, comfort and the sensual beauty of the world. A builder and keeper: patient, reliable, generous to its own. Strengths: patience, practicality, loyalty. Vulnerabilities: stubbornness, resistance to change, attachment to comfort and possession."},
    },
    "astrology-gemini": {
        "glyph": "♊",
        "ru": {"title": "Близнецы", "body": "Третий знак, стихия Воздух, управитель Меркурий (21.05–20.06). Близнецы живут информацией: общение, любопытство, переключение между ролями. Это изменчивый ум, который схватывает быстро и скучает от рутины. Сильные стороны: адаптивность, остроумие, многогранность. Уязвимости: поверхностность, раздвоенность, неспособность усидеть в одной теме."},
        "uk": {"title": "Близнюки", "body": "Третій знак, стихія Повітря, управитель Меркурій (21.05–20.06). Близнюки живуть інформацією: спілкування, цікавість, перемикання між ролями. Це мінливий розум, який хапає швидко й нудьгує від рутини. Сильні сторони: адаптивність, дотепність, багатогранність. Уразливості: поверховість, роздвоєність, нездатність усидіти в одній темі."},
        "en": {"title": "Gemini", "body": "The third sign, element Air, ruled by Mercury (May 21 – Jun 20). Gemini lives on information: communication, curiosity, switching between roles. A mutable mind that grasps quickly and bores of routine. Strengths: adaptability, wit, versatility. Vulnerabilities: superficiality, split focus, inability to stick to one subject."},
    },
    "astrology-cancer": {
        "glyph": "♋",
        "ru": {"title": "Рак", "body": "Четвёртый знак, стихия Вода, управитель Луна (21.06–22.07). Рак — знак дома, памяти и эмоциональной глубины. Он чувствует мир через привязанности и защищает тех, кого любит, с интуицией матери. Сильные стороны: забота, эмпатия, преданность. Уязвимости: уязвимость к обидам, опека сверх меры, уход в раковину при стрессе."},
        "uk": {"title": "Рак", "body": "Четвертий знак, стихія Вода, управитель Місяць (21.06–22.07). Рак — знак дому, пам'яті та емоційної глибини. Він відчуває світ через прив'язаності й захищає тих, кого любить, інтуїцією матері. Сильні сторони: турбота, емпатія, відданість. Уразливості: вразливість до образ, опіка понад міру, ухід у мушлю при стресі."},
        "en": {"title": "Cancer", "body": "The fourth sign, element Water, ruled by the Moon (Jun 21 – Jul 22). Cancer is the sign of home, memory and emotional depth. It senses the world through attachments and protects those it loves with a mother's intuition. Strengths: care, empathy, devotion. Vulnerabilities: vulnerability to hurt, over-protection, retreating into a shell under stress."},
    },
    "astrology-leo": {
        "glyph": "♌",
        "ru": {"title": "Лев", "body": "Пятый знак, стихия Огонь, управитель Солнце (23.07–22.08). Лев — это творчество, достоинство и сердечная щедрость. Он сияет в центре сцены, любит признание и защищает своих людей с королевской пышностью. Сильные стороны: харизма, верность, созидательность. Уязвимости: гордыня, потребность в похвале, драматизм."},
        "uk": {"title": "Лев", "body": "П'ятий знак, стихія Вогонь, управитель Сонце (23.07–22.08). Лев — це творчість, гідність і сердечна щедрість. Він сяє в центрі сцени, любить визнання й захищає своїх людей із королівською пишністю. Сильні сторони: харизма, вірність, творчість. Уразливості: гординя, потреба в похвалі, драматизм."},
        "en": {"title": "Leo", "body": "The fifth sign, element Fire, ruled by the Sun (Jul 23 – Aug 22). Leo is creativity, dignity and generosity of heart. It shines at the centre of the stage, loves recognition and protects its people with royal pomp. Strengths: charisma, loyalty, creativity. Vulnerabilities: pride, craving praise, drama."},
    },
    "astrology-virgo": {
        "glyph": "♍",
        "ru": {"title": "Дева", "body": "Шестой знак, стихия Земля, управитель Меркурий (23.08–22.09). Дева приносит в мир порядок: точность, анализ, служение. Она видит детали, которые упускают другие, и доводит вещи до совершенства. Сильные стороны: практичность, надёжность, ум. Уязвимости: перфекционизм, самокритика, тревожность за результат."},
        "uk": {"title": "Діва", "body": "Шостий знак, стихія Земля, управитель Меркурій (23.08–22.09). Діва приносить у світ лад: точність, аналіз, служіння. Вона бачить деталі, яких інші не помічають, і доводить речі до досконалості. Сильні сторони: практичність, надійність, розум. Уразливості: перфекціонізм, самокритика, тривожність за результат."},
        "en": {"title": "Virgo", "body": "The sixth sign, element Earth, ruled by Mercury (Aug 23 – Sep 22). Virgo brings order to the world: precision, analysis, service. It sees details others miss and perfects things. Strengths: practicality, reliability, intellect. Vulnerabilities: perfectionism, self-criticism, anxiety over outcomes."},
    },
    "astrology-libra": {
        "glyph": "♎",
        "ru": {"title": "Весы", "body": "Седьмой знак, стихия Воздух, управитель Венера (23.09–22.10). Весы рождены для гармонии и отношений: дипломатичность, вкус, стремление к равновесию. Они взвешивают обе стороны и строят мосты там, где другие воюют. Сильные стороны: справедливость, обаяние, партнёрство. Уязвимости: нерешительность, конфликтность, зависимость от чужого мнения."},
        "uk": {"title": "Терези", "body": "Сьомий знак, стихія Повітря, управитель Венера (23.09–22.10). Терези народжені для гармонії та стосунків: дипломатичність, смак, прагнення рівноваги. Вони зважують обидві сторони та будують мости там, де інші воюють. Сильні сторони: справедливість, чарівність, партнерство. Уразливості: нерішучість, конфлікти, залежність від чужої думки."},
        "en": {"title": "Libra", "body": "The seventh sign, element Air, ruled by Venus (Sep 23 – Oct 22). Libra is born for harmony and relationships: diplomacy, taste, the pursuit of balance. It weighs both sides and builds bridges where others fight. Strengths: fairness, charm, partnership. Vulnerabilities: indecision, conflict-aversion, dependence on others' opinions."},
    },
    "astrology-scorpio": {
        "glyph": "♏",
        "ru": {"title": "Скорпион", "body": "Восьмой знак, стихия Вода, соуправители Марс и Плутон (23.10–21.11). Скорпион идёт в глубину: страсть, интенсивность, трансформация. Он не боится тайны, кризиса и перерождения — управляет силами, которых другие страшатся. Сильные стороны: сила воли, проницательность, преданность. Уязвимости: ревность, скрытность, желание тотального контроля."},
        "uk": {"title": "Скорпіон", "body": "Восьмий знак, стихія Вода, співуправителі Марс і Плутон (23.10–21.11). Скорпіон іде в глибину: пристрасть, інтенсивність, трансформація. Він не боїться таємниці, кризи й переродження — керує силами, яких інші страхаються. Сильні сторони: сила волі, проникливість, відданість. Уразливості: ревнощі, скритність, бажання тотального контролю."},
        "en": {"title": "Scorpio", "body": "The eighth sign, element Water, co-ruled by Mars and Pluto (Oct 23 – Nov 21). Scorpio dives deep: passion, intensity, transformation. It does not fear mystery, crisis or rebirth — it masters forces others dread. Strengths: willpower, insight, loyalty. Vulnerabilities: jealousy, secrecy, craving total control."},
    },
    "astrology-sagittarius": {
        "glyph": "♐",
        "ru": {"title": "Стрелец", "body": "Девятый знак, стихия Огонь, управитель Юпитер (22.11–21.12). Стрелец — философ и путешественник: поиск смысла, горизонты, вера в лучшее. Он целится высоко и расширяет границы — знаний, стран и мечты о свободе. Сильные стороны: оптимизм, честность, широта. Уязвимости: тактичность в минусе, непостоянство, обещания без деталей."},
        "uk": {"title": "Стрілець", "body": "Дев'ятий знак, стихія Вогонь, управитель Юпітер (22.11–21.12). Стрілець — філософ і мандрівник: пошук сенсу, горизонти, віра в краще. Він цілиться високо й розширює межі — знань, країн і мрії про свободу. Сильні сторони: оптимізм, чесність, широта. Уразливості: брак такту, непостійність, обіцянки без деталей."},
        "en": {"title": "Sagittarius", "body": "The ninth sign, element Fire, ruled by Jupiter (Nov 22 – Dec 21). Sagittarius is the philosopher-traveller: seeking meaning, horizons, faith in the best. It aims high and expands borders — of knowledge, places and the dream of freedom. Strengths: optimism, honesty, breadth. Vulnerabilities: tactlessness, instability, promises without details."},
    },
    "astrology-capricorn": {
        "glyph": "♑",
        "ru": {"title": "Козерог", "body": "Десятый знак, стихия Земля, управитель Сатурн (22.12–19.01). Козерог строит вершину долго и верно: дисциплина, ответственность, амбиция. Он не ждёт быстрых даров — он управляет временем и пожинает зрелые плоды. Сильные стороны: надёжность, стратегия, выдержка. Уязвимости: жёсткость к себе, работа без меры, пессимизм тона."},
        "uk": {"title": "Козеріг", "body": "Десятий знак, стихія Земля, управитель Сатурн (22.12–19.01). Козеріг будує вершину довго й вірно: дисципліна, відповідальність, амбіція. Він не чекає швидких дарів — він керує часом і пожинає зрілі плоди. Сильні сторони: надійність, стратегія, витримка. Уразливості: жорсткість до себе, праця без міри, песимізм тону."},
        "en": {"title": "Capricorn", "body": "The tenth sign, element Earth, ruled by Saturn (Dec 22 – Jan 19). Capricorn builds its summit slowly and surely: discipline, responsibility, ambition. It does not await quick gifts — it governs time and reaps mature fruit. Strengths: reliability, strategy, endurance. Vulnerabilities: harshness toward self, overwork, a pessimistic tone."},
    },
    "astrology-aquarius": {
        "glyph": "♒",
        "ru": {"title": "Водолей", "body": "Одиннадцатый знак, стихия Воздух, соуправители Сатурн и Уран (20.01–18.02). Водолей — знак будущего: независимость, оригинальность, дружба с идеями. Он смотрит на мир со стороны и видит, каким мир мог бы стать. Сильные стороны: гуманизм, интеллект, свобода. Уязвимости: отстранённость, бунтарство без причины, холод в личном."},
        "uk": {"title": "Водолій", "body": "Одинадцятий знак, стихія Повітря, співуправителі Сатурн і Уран (20.01–18.02). Водолій — знак майбутнього: незалежність, оригінальність, дружба з ідеями. Він дивиться на світ збоку й бачить, яким світ міг би стати. Сильні сторони: гуманізм, інтелект, свобода. Уразливості: відстороненість, бунт без причини, холод в особистому."},
        "en": {"title": "Aquarius", "body": "The eleventh sign, element Air, co-ruled by Saturn and Uranus (Jan 20 – Feb 18). Aquarius is the sign of the future: independence, originality, friendship with ideas. It views the world from aside and sees what it could become. Strengths: humanism, intellect, freedom. Vulnerabilities: detachment, needless rebellion, emotional coolness."},
    },
    "astrology-pisces": {
        "glyph": "♓",
        "ru": {"title": "Рыбы", "body": "Двенадцатый знак, стихия Вода, соуправители Юпитер и Нептун (19.02–20.03). Рыбы завершают цикл: эмпатия, воображение, связь с невидимым. Они растворяются в чувствах и искусстве, чутко улавливая настроения мира. Сильные стороны: сострадание, интуиция, творчество. Уязвимости: безграничность, уход от реальности, жертвенность."},
        "uk": {"title": "Риби", "body": "Дванадцятий знак, стихія Вода, співуправителі Юпітер і Нептун (19.02–20.03). Риби завершують цикл: емпатія, уява, зв'язок із невидимим. Вони розчиняються в почуттях і мистецтві, чутно вловлюючи настрої світу. Сильні сторони: співчуття, інтуїція, творчість. Уразливості: безмежність, ухід від реальності, жертовність."},
        "en": {"title": "Pisces", "body": "The twelfth sign, element Water, co-ruled by Jupiter and Neptune (Feb 19 – Mar 20). Pisces closes the cycle: empathy, imagination, connection with the unseen. It dissolves into feelings and art, keenly sensing the world's moods. Strengths: compassion, intuition, creativity. Vulnerabilities: boundlessness, escapism, self-sacrifice."},
    },
    # ---------- ПЛАНЕТЫ ----------
    "astrology-sun": {
        "glyph": "☉",
        "ru": {"title": "Солнце", "body": "Центр личности: суть, жизненная сила, осознанное «я». Солнце управляет Львом и показывает, где мы светим и что придаёт нам смысл. В гороскопе знак Солнца — это ядро характера и творческая идентичность."},
        "uk": {"title": "Сонце", "body": "Центр особистості: суть, життєва сила, усвідомлене «я». Сонце керує Левом і показує, де ми сяємо й що надає нам сенсу. У гороскопі знак Сонця — це ядро характеру й творча ідентичність."},
        "en": {"title": "The Sun", "body": "The centre of personality: essence, life force, the conscious self. The Sun rules Leo and shows where we shine and what gives us meaning. In the chart the Sun sign is the core of character and creative identity."},
    },
    "astrology-moon": {
        "glyph": "☽",
        "ru": {"title": "Луна", "body": "Чувства и подсознание: потребности, инстинкты, память. Луна управляет Раком и описывает эмоциональную природу и привычки. Это то, что нам нужно для внутреннего комфорта и безопасности."},
        "uk": {"title": "Місяць", "body": "Почуття й підсвідомість: потреби, інстинкти, пам'ять. Місяць керує Раком і описує емоційну природу та звички. Це те, що потрібно нам для внутрішнього комфорту й безпеки."},
        "en": {"title": "The Moon", "body": "Feelings and the subconscious: needs, instincts, memory. The Moon rules Cancer and describes emotional nature and habits. It is what we need for inner comfort and security."},
    },
    "astrology-mercury": {
        "glyph": "☿",
        "ru": {"title": "Меркурий", "body": "Ум и коммуникация: мышление, речь, обмен информацией. Меркурий управляет Близнецами и Девой и описывает наш стиль обучения и общения. Он близок к Солнцу и поэтому быстр в повседневных делах."},
        "uk": {"title": "Меркурій", "body": "Розум і комунікація: мислення, мовлення, обмін інформацією. Меркурій керує Близнюками та Дівою й описує наш стиль навчання та спілкування. Він близький до Сонця, тому швидкий у повсякденних справах."},
        "en": {"title": "Mercury", "body": "Mind and communication: thinking, speech, exchanging information. Mercury rules Gemini and Virgo and describes our style of learning and talking. Close to the Sun, it is quick in everyday affairs."},
    },
    "astrology-venus": {
        "glyph": "♀",
        "ru": {"title": "Венера", "body": "Любовь, красота и ценности: как мы любим, что ценим и чем наслаждаемся. Венера управляет Тельцом и Весами. Она описывает притягательность, вкус, гармонию и способы привлекать и дарить нежность."},
        "uk": {"title": "Венера", "body": "Любов, краса й цінності: як ми любимо, що цінуємо й чим насолоджуємося. Венера керує Тельцем і Терезами. Вона описує привабливість, смак, гармонію та способи притягувати й дарувати ніжність."},
        "en": {"title": "Venus", "body": "Love, beauty and values: how we love, what we value and enjoy. Venus rules Taurus and Libra. It describes attraction, taste, harmony and how we draw in and give tenderness."},
    },
    "astrology-mars": {
        "glyph": "♂",
        "ru": {"title": "Марс", "body": "Энергия действия: воля, агрессия, желание и мужество. Марс управляет Овном (и классически Скорпионом). Его положение показывает, как мы боремся, добиваемся и расходуем свою силу."},
        "uk": {"title": "Марс", "body": "Енергія дії: воля, агресія, бажання й мужність. Марс керує Овном (і класично Скорпіоном). Його положення показує, як ми боремося, досягаємо й витрачаємо свою силу."},
        "en": {"title": "Mars", "body": "The energy of action: will, aggression, desire and courage. Mars rules Aries (and classically Scorpio). Its placement shows how we fight, achieve and spend our force."},
    },
    "astrology-jupiter": {
        "glyph": "♃",
        "ru": {"title": "Юпитер", "body": "Расширение и удача: рост, смысл, вера и изобилие. Юпитер управляет Стрельцом (и классически Рыбами). Он показывает, где жизнь щедра к нам и где мы склонны к большим жестам и открытиям."},
        "uk": {"title": "Юпітер", "body": "Розширення й удача: зростання, сенс, віра й достаток. Юпітер керує Стрільцем (і класично Рибами). Він показує, де життя щедре до нас і де ми схильні до великих жестів і відкриттів."},
        "en": {"title": "Jupiter", "body": "Expansion and luck: growth, meaning, faith and abundance. Jupiter rules Sagittarius (and classically Pisces). It shows where life is generous to us and where we favour grand gestures and discoveries."},
    },
    "astrology-saturn": {
        "glyph": "♄",
        "ru": {"title": "Сатурн", "body": "Структура и границы: время, ответственность, уроки и зрелость. Сатурн управляет Козерогом (и классически Водолеем). Его положение показывает, где жизнь требует дисциплины и где со временем приходит мастерство."},
        "uk": {"title": "Сатурн", "body": "Структура й межі: час, відповідальність, уроки й зрілість. Сатурн керує Козерогом (і класично Водолієм). Його положення показує, де життя вимагає дисципліни й де з часом приходить майстерність."},
        "en": {"title": "Saturn", "body": "Structure and boundaries: time, responsibility, lessons and maturity. Saturn rules Capricorn (and classically Aquarius). Its placement shows where life demands discipline and where mastery grows over time."},
    },
    "astrology-uranus": {
        "glyph": "♅",
        "ru": {"title": "Уран", "body": "Перелом и свобода: инновации, бунт, внезапные прозрения. Уран управляет Водолеем. Его положение указывает, где мы стремимся к независимости и где судьба может преподнести неожиданный разворот."},
        "uk": {"title": "Уран", "body": "Перелом і свобода: інновації, бунт, раптові прозріння. Уран керує Водолієм. Його положення вказує, де ми прагнемо незалежності й де доля може піднести несподіваний розворот."},
        "en": {"title": "Uranus", "body": "Breakthrough and freedom: innovation, rebellion, sudden insight. Uranus rules Aquarius. Its placement points to where we seek independence and where fate may deliver an unexpected turn."},
    },
    "astrology-neptune": {
        "glyph": "♆",
        "ru": {"title": "Нептун", "body": "Трансцендентность и воображение: мечты, мистика, растворение. Нептун управляет Рыбами. Его положение описывает, где мы идеализируем, вдохновляемся и рискуем потерять границы реальности."},
        "uk": {"title": "Нептун", "body": "Трансцендентність і уява: мрії, містика, розчинення. Нептун керує Рибами. Його положення описує, де ми ідеалізуємо, надихаємось і ризикуємо втратити межі реальності."},
        "en": {"title": "Neptune", "body": "Transcendence and imagination: dreams, mysticism, dissolution. Neptune rules Pisces. Its placement describes where we idealise, find inspiration and risk losing the borders of reality."},
    },
    "astrology-pluto": {
        "glyph": "♇",
        "ru": {"title": "Плутон", "body": "Глубинная трансформация: власть, кризис, перерождение. Плутон управляет Скорпионом. Его положение показывает, где мы проходим через «умирание и возрождение», обретая внутреннюю силу."},
        "uk": {"title": "Плутон", "body": "Глибинна трансформація: влада, криза, переродження. Плутон керує Скорпіоном. Його положення показує, де ми проходимо через «умирання й відродження», здобуваючи внутрішню силу."},
        "en": {"title": "Pluto", "body": "Deep transformation: power, crisis, rebirth. Pluto rules Scorpio. Its placement shows where we undergo dying and being reborn, gaining inner power."},
    },
    # ---------- ДОМА ----------
    "astrology-house-1": {
        "glyph": "Ⅰ",
        "ru": {"title": "I дом", "body": "Личность и внешность: как мир видит нас, наша маска и стартовый импульс. Начинается Асцендентом и описывает характер в проявлении."},
        "uk": {"title": "I дім", "body": "Особистість і зовнішність: як світ бачить нас, наша маска й стартовий імпульс. Починається Асцендентом і описує характер у прояві."},
        "en": {"title": "1st House", "body": "Personality and appearance: how the world sees us, our mask and initial impulse. It begins at the Ascendant and describes character in expression."},
    },
    "astrology-house-2": {
        "glyph": "Ⅱ",
        "ru": {"title": "II дом", "body": "Ценности и ресурсы: деньги, имущество, самооценка. Показывает, как мы зарабатываем, накапливаем и ощущаем собственную ценность."},
        "uk": {"title": "II дім", "body": "Цінності й ресурси: гроші, майно, самооцінка. Показує, як ми заробляємо, накопичуємо й відчуваємо власну цінність."},
        "en": {"title": "2nd House", "body": "Values and resources: money, possessions, self-worth. Shows how we earn, accumulate and feel our own value."},
    },
    "astrology-house-3": {
        "glyph": "Ⅲ",
        "ru": {"title": "III дом", "body": "Общение и окружение: ум, речь, братья-сёстры, короткие поездки. Описывает повседневный обмен информацией и ближний круг."},
        "uk": {"title": "III дім", "body": "Спілкування й оточення: розум, мовлення, брати-сестри, короткі поїздки. Описує щоденний обмін інформацією та ближнє коло."},
        "en": {"title": "3rd House", "body": "Communication and surroundings: mind, speech, siblings, short trips. Describes daily information exchange and the immediate circle."},
    },
    "astrology-house-4": {
        "glyph": "Ⅳ",
        "ru": {"title": "IV дом", "body": "Дом и корни: семья, родители, прошлое, приватность. Управляется Нижним Небом (IC) и описывает внутренний фундамент души."},
        "uk": {"title": "IV дім", "body": "Дім і коріння: сім'я, батьки, минуле, приватність. Керується Нижнім Небом (IC) і описує внутрішній фундамент душі."},
        "en": {"title": "4th House", "body": "Home and roots: family, parents, the past, privacy. Governed by the IC, it describes the inner foundation of the soul."},
    },
    "astrology-house-5": {
        "glyph": "Ⅴ",
        "ru": {"title": "V дом", "body": "Творчество и радость: игры, любовь, дети, самовыражение. Здесь мы зажигаем огонь, который любим бескорыстно, и показываем талант."},
        "uk": {"title": "V дім", "body": "Творчість і радість: ігри, кохання, діти, самовираження. Тут ми запалюємо вогонь, який любимо безкорисливо, і показуємо талант."},
        "en": {"title": "5th House", "body": "Creativity and joy: games, love, children, self-expression. Here we light a fire we love selflessly and reveal talent."},
    },
    "astrology-house-6": {
        "glyph": "Ⅵ",
        "ru": {"title": "VI дом", "body": "Работа и здоровье: повседневный труд, служение, привычки тела. Описывает бытовой порядок и то, что мы делаем каждый день для своей формы."},
        "uk": {"title": "VI дім", "body": "Робота й здоров'я: повсякденна праця, служіння, звички тіла. Описує побутовий лад і те, що ми робимо щодня для своєї форми."},
        "en": {"title": "6th House", "body": "Work and health: daily labour, service, bodily habits. Describes everyday order and what we do each day for our form."},
    },
    "astrology-house-7": {
        "glyph": "Ⅶ",
        "ru": {"title": "VII дом", "body": "Партнёрство и брак: «другие», союзы, контракты и враги явные. Управляется Десцендентом и показывает, с кем мы объединяемся на равных."},
        "uk": {"title": "VII дім", "body": "Партнерство й шлюб: «інші», союзи, контракти й явні вороги. Керується Десцендентом і показує, з ким ми об'єднуємось на рівних."},
        "en": {"title": "7th House", "body": "Partnership and marriage: others, unions, contracts and open enemies. Governed by the Descendant, it shows with whom we unite as equals."},
    },
    "astrology-house-8": {
        "glyph": "Ⅷ",
        "ru": {"title": "VIII дом", "body": "Трансформация и чужие ресурсы: секс, смерть, наследство, совместные деньги. Зона глубины, в которой мы меняемся через кризисы и связи."},
        "uk": {"title": "VIII дім", "body": "Трансформація й чужі ресурси: секс, смерть, спадщина, спільні гроші. Зона глибини, у якій ми змінюємось через кризи й зв'язки."},
        "en": {"title": "8th House", "body": "Transformation and shared resources: sex, death, inheritance, joint money. A depth zone where we change through crises and bonds."},
    },
    "astrology-house-9": {
        "glyph": "Ⅸ",
        "ru": {"title": "IX дом", "body": "Смысл и горизонты: философия, религия, дальние страны, высшее образование. Здесь мы ищем ответы большего масштаба и истину поверх границ."},
        "uk": {"title": "IX дім", "body": "Сенс і горизонти: філософія, релігія, далекі країни, вища освіта. Тут ми шукаємо відповіді більшого масштабу й істину понад межі."},
        "en": {"title": "9th House", "body": "Meaning and horizons: philosophy, religion, far countries, higher education. Here we seek larger answers and truth beyond borders."},
    },
    "astrology-house-10": {
        "glyph": "Ⅹ",
        "ru": {"title": "X дом", "body": "Призвание и карьера: статус, публичное лицо, цель жизни. Управляется Серединой Неба (MC) и описывает наш вклад в мир."},
        "uk": {"title": "X дім", "body": "Покликання й кар'єра: статус, публічне обличчя, мета життя. Керується Серединою Неба (MC) і описує наш внесок у світ."},
        "en": {"title": "10th House", "body": "Vocation and career: status, public face, life's purpose. Governed by the MC, it describes our contribution to the world."},
    },
    "astrology-house-11": {
        "glyph": "Ⅺ",
        "ru": {"title": "XI дом", "body": "Сообщества и мечты: друзья, группы, будущее, надежды. Здесь мы связаны с людьми общими идеалами и строим коллективную мечту."},
        "uk": {"title": "XI дім", "body": "Спільноти й мрії: друзі, групи, майбутнє, надії. Тут ми пов'язані з людьми спільними ідеалами й будуємо колективну мрію."},
        "en": {"title": "11th House", "body": "Communities and dreams: friends, groups, the future, hopes. Here we connect with people over shared ideals and build collective dreams."},
    },
    "astrology-house-12": {
        "glyph": "Ⅻ",
        "ru": {"title": "XII дом", "body": "Тайное и трансцендентное: подсознание, уединение, духовность, скрытые враги. Дом завершения цикла и связи с тем, что больше нас."},
        "uk": {"title": "XII дім", "body": "Таємне й трансцендентне: підсвідомість, самотність, духовність, приховані вороги. Дім завершення циклу й зв'язку з тим, що більше за нас."},
        "en": {"title": "12th House", "body": "The hidden and transcendent: the subconscious, solitude, spirituality, hidden enemies. The house of ending a cycle and connecting with what is greater than us."},
    },
    # ---------- АСПЕКТЫ ----------
    "astrology-aspects-intro": {
        "glyph": "✦",
        "ru": {"title": "Аспекты в астрологии", "body": "Аспекты — это углы между планетами в гороскопе, описывающие их диалог. Основные: соединение (0°), секстиль (60°), квадрат (90°), трин (120°) и оппозиция (180°). Гармоничные аспекты (секстиль, трин) дают потоки поддержки, напряжённые (квадрат, оппозиция) — энергию роста через трудность."},
        "uk": {"title": "Аспекти в астрології", "body": "Аспекти — це кути між планетами в гороскопі, що описують їхній діалог. Основні: сполучення (0°), секстиль (60°), квадрат (90°), трин (120°) й опозиція (180°). Гармонійні аспекти (секстиль, трин) дають потоки підтримки, напружені (квадрат, опозиція) — енергію зростання через труднощі."},
        "en": {"title": "Aspects in astrology", "body": "Aspects are the angles between planets in a chart, describing their dialogue. The main ones: conjunction (0°), sextile (60°), square (90°), trine (120°) and opposition (180°). Harmonious aspects (sextile, trine) stream support; tense ones (square, opposition) fuel growth through difficulty."},
    },
    "astrology-aspect-conjunction": {
        "glyph": "☌",
        "ru": {"title": "Соединение (0°)", "body": "Планеты сливаются в одну силу: их энергии работают вместе, усиливая друг друга. Характер точного соединения зависит от участвующих планет — это сплав качеств, который трудно разделить."},
        "uk": {"title": "Сполучення (0°)", "body": "Планети зливаються в одну силу: їхні енергії працюють разом, підсилюючи одна одну. Характер точного сполучення залежить від планет — це сплав якостей, який важко розділити."},
        "en": {"title": "Conjunction (0°)", "body": "The planets fuse into one force: their energies work together, amplifying each other. The exact character depends on the planets involved — a blend of qualities hard to separate."},
    },
    "astrology-aspect-sextile": {
        "glyph": "⚹",
        "ru": {"title": "Секстиль (60°)", "body": "Лёгкая гармония — планеты сотрудничают как союзники и предлагают удобные возможности. Секстиль даёт талант к использованию шансов, если проявить немного инициативы."},
        "uk": {"title": "Секстиль (60°)", "body": "Легка гармонія — планети співпрацюють як союзники й пропонують зручні можливості. Секстиль дає талант користуватися шансами, якщо проявити трохи ініціативи."},
        "en": {"title": "Sextile (60°)", "body": "Gentle harmony — the planets cooperate as allies and offer convenient opportunities. A sextile gives talent for seizing chances, provided a little initiative is shown."},
    },
    "astrology-aspect-square": {
        "glyph": "□",
        "ru": {"title": "Квадрат (90°)", "body": "Напряжение и трение — планеты «спорят» между собой. Квадраты создают препятствия и мотивацию: это мотор роста, который вознаграждает тех, кто решает сквозь трудность."},
        "uk": {"title": "Квадрат (90°)", "body": "Напруження й тертя — планети «сперечаються» між собою. Квадрати створюють перешкоди й мотивацію: це мотор зростання, який винагороджує тих, хто йде крізь труднощі."},
        "en": {"title": "Square (90°)", "body": "Tension and friction — the planets argue. Squares create obstacles and motivation: a growth engine that rewards those who push through difficulty."},
    },
    "astrology-aspect-trine": {
        "glyph": "△",
        "ru": {"title": "Трин (120°)", "body": "Плавный поток талантов — планеты в стихийном согласии. Трин даёт естественные дары, работающие «сами собой», и потому требует осознанности, чтобы не остаться в ленивой зоне комфорта."},
        "uk": {"title": "Трин (120°)", "body": "Плавний потік талантів — планети в стихійній згоді. Трин дає природні дари, що працюють «самі собою», і тому потребує усвідомленості, щоб не лишитися в лінивій зоні комфорту."},
        "en": {"title": "Trine (120°)", "body": "A smooth flow of talents — planets in elemental accord. A trine grants gifts that work on their own, so it calls for awareness to avoid lapsing into comfortable laziness."},
    },
    "astrology-aspect-opposition": {
        "glyph": "☍",
        "ru": {"title": "Оппозиция (180°)", "body": "Две силы «смотрят друг на друга»: противоположности, которые нужно примирить. Оппозиция проецирует конфликт вовне и зреет через признание в «другом» части себя."},
        "uk": {"title": "Опозиція (180°)", "body": "Дві сили «дивляться одна на одну»: протилежності, які треба примирити. Опозиція проєктує конфлікт назовні й дозріває через визнання в «іншому» частини себе."},
        "en": {"title": "Opposition (180°)", "body": "Two forces face each other: opposites to be reconciled. An opposition projects conflict outward and matures by recognising a part of yourself in the other."},
    },
}