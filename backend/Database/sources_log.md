# Журнал джерел (етика/атрибуція)
- A.E. Waite, Pictorial Key to the Tarot (1911) — суспільне надбання; база трактовок RWS (переказ).
- sacred-texts.com/tarot — архів, скани RWS.
- Wikimedia Commons — зображення RWS 1909 (суспільне надбання).
- Biddy Tarot / Labyrinthos / learntarot.com — лише як довідка, переписувати своїми словами.
- Сучасні оракули/МАК — лише переказ концепції + посилання на офіційну книжку колоди.
- Старший Футарк (24), Місячний оракул (8), МАК «Архетипи» (12), Астрологічний оракул (26),
  Шаманські тотеми (12), Циганські карти (36), Гральні карти 36 (фольклор),
  Цолькин (20 печаток + 13 тонів; структура Дрімспел — факти, описи свої),
  Карти роду (12), Нумерологія (12): **оригінальні навчальні тексти AI-Arcanum** (UK-база + RU/EN).
  Сучасні авторські сайти (biddy, labyrinthos, astro.com, lenormand.io, 13moon) НЕ скрейпились —
  лише структура/факти + власний переказ із зазначенням джерела.
- UK/EN keywords+meaning для RWS-старших і Ленорман: власні формулювання (`scripts/fill_translations.py`).

## Автоматичний імпорт (scripts/import_public_domain_sources.py, перевірено 2026-09-12)
- Waite 1911, EN-текст старших арканов → `translations.en.meaning_general_waite1911`:
  archive.org/download/A.EWaiteThePictorialKeyToTheTarot (OCR, 1 запрос, кэш backend/Database/_pd_cache/).
  УВАГА: sacred-texts pktNN.htm мертві (404, сайт став SPA); Gutenberg #43548 — це де Лоранс 1918, НЕ Уейт.
- RWS-скани (PD): Commons API, категорія "Rider-Waite-Smith tarot deck (TaionWC)", файли "RWS Tarot NN …".
  upload.wikimedia.org вимагає браузерний UA (ботовий дає 403); тротлінг 429 лікується паузою+ретраєм.
- Ленорман: скани прадіда — Das Spiel der Hofnung (Й. К. Гехтель, Нюрнберг, 1799, PD),
  нарізка `scripts/cut_game_of_hope.py` 6×6 (сировинний аркуш: `Database/raw/lenormand/`).
  Повного PD-сету сучасного Ленорман на Commons нема (лише 3 файли).
- Цолькин: гліфи днів DaySign (Wikimedia Commons, Public domain) — вмонтовано в карти;
  тони — нумерали мая. Gypsy Witch 1903 на archive.org НЕ знайдено (лише сторонні книги) —
  сучасні перевидання (US Games 1989+) під копірайтом, тому циганські лишилися процедурними.
- МАК розширено до 20: 4 пари «архетип—тінь» у дусі Спеццано (своя графіка, не копії).
- Процедурні ілюстрації (`scripts/generate_deck_images.py`, власний код, не фото):
  гексаграми — лінії розібрано з тексту Легга (NINE/SIX, перевірено якорі 111111/000000);
  руни (Segoe UI Historic)/астрознаки/масті (Segoe UI Symbol, Arial) — системні шрифти;
  фази місяця, нумерали мая, кольори печаток — автентичні умовні позначення;
  Ленорман — 36 контурних іконок + гральні відповідності; шамани/предки — по іконці на карту;
  МАК — дуальність світло/тінь. Покриття БД: 432/432.
- И-Цзин, пер. James Legge (1899), 64 гексаграммы: sacred-texts.com/ich/icNN.htm (legacy .htm живы).
- Англосаксонская руническая поэма, 29 строф (OE + пер. Bruce Dickins, 1915, PD):
  en.wikisource.org/wiki/Runic_and_Heroic_Poems…/The_Anglo-Saxon_Runic_Poem
  (sacred-texts neu/ascp/a12.htm — только JS-оболочка, в статике пусто).
- Ручне введення сучасних джерел: прочитати → переписати своїми словами →
  CSV з обовʼязковим source_reference → scripts/import_from_csv.py
- Значення Таро (фон, НЕ скрейпінг): labyrinthos.co/blogs/tarot-card-meanings-list,
  purplegarden.co/blog/list-of-tarot-cards-with-pictures, tarostarot.com/tarot-card-meanings,
  alittlesparkofjoy.com/tarot-cards-list — тексти авторські, взято лише структуру
  (масті/стихії/знаки) як фон для власних формулювань.
- Деканати молодших арканів: традиція Золотої Зорі (халдейський порядок) — факти,
  `scripts/fill_minors.py`.
- Галереї колод (довідкові профілі, без копіювання карт): aeclectic.net (каталог тисяч колод),
  trionfi.com/0/i/ (~200 колод), tarot-heritage.com/history-4/resources (музеї:
  British Museum, Yale, BnF), waitesmith.org, themorgan.org/exhibitions/tarot,
  vam.ac.uk/articles/tarot-cards, museum-tarot.org, tarotmuseumbelgium.com.
  Профілі: Вісконті-Сфорца (~1450, 74 карти), Марсель (Додаль 1701), Тот (Кроулі–Гарріс, вид. 1969).
- Астроджерела: astro.com, cafeastrology.com, horoscopes.astro-seek.com,
  astrowl.ai/en/dictionary; огляди астроколод: aeclectic.net/tarot/cards/astrology.shtml,
  aeclectic.net/tarot/cards/astrological-oracle (оракул 22: 12 знаків + 10 планет),
   astrology.com/article/oracle-vs-tarot, askastrology.com (oracle-decks).
- Visconti-Sforza Tarot (deck 23, 74 карт): Пірпонт Морґан-Берґамо, ~1450.
  Зображення 500px: Wikimedia Commons (Public Domain); мінуси XV (Диявол) та XVI (Вежа).
  Файли `images/23/`, `assets/23/`; метадані `pd_map_23.json`; кэш URL `pd_urls_23.json`.
- Tarot de Marseille (deck 24, 78 карт): репринт 1970 р., Philippe Camoin.
  Зображення 500px: `File:MarseilleTarot.jpg` (Wikimedia Commons, Public Domain).
  Файли `images/24/`, `assets/24/`; метадані `pd_map_24.json`; кэш URL `pd_urls_24.json`.
- Тексти карт Visconti/Marseille — з RWS (deck 1), gen_pd_cards.py з урахуванням VIII=Justice, XI=Strength.

## Друга хвиля: 14 колод / 13 систем (scripts/import_second_wave.py, 2026-09-15)
Карти 31–44, згенеровано графіку `generate_deck_images.py` (процедурні малюнки, без копірайту). Джерела значень — відкриті довідники:
- Цінності (Шварц, 12): simplypsychology.org/values.html (теорія базових цінностей).
- Ресурс (12): positivepsychology.com/resilience/ (сутність і вправи психологічної стійкості).
- Сни (20): dreammoods.com/dreamdictionary/ (типові символи сновидінь).
- Стихії (5): en.wikipedia.org/wiki/Classical_element (класичний набір Вогонь/Вода/Повітря/Земля + ефір/квінтесенція).
- Архангели (7): en.wikipedia.org/wiki/Archangel.
- Афірмації · карта дня (20): pubmed.ncbi.nlm.nih.gov/24602760/ (ефективність афірмацій).
- Бажання (16): developgoodhabits.com/vision-board-ideas/ (теми для дошки бажань).
- Каббала: сфіроти (10) + 22 шляхи — en.wikipedia.org/wiki/Tree_of_life_(Kabbalah).
- Багуа · 8 триграм: en.wikipedia.org/wiki/Bagua.
- Іфа · 16 Оду: en.wikipedia.org/wiki/Ifá.
- Числа-ангели (12): mindbodygreen.com/articles/angel-number-meaning.
- Тасеографія · чайні листки (20): tealeafreading.com/.
- Кристали · оракул самоцвітів (16): energymuse.com/crystal-guide.
Шрифтова частина: огамові гліфи — `seguihis.ttf` (Segoe UI Historic, U+1680–169F); деванагарі (биджа `लं वं रं यं हं ॐ`) — `arial.ttf`; карти Playing Cards (U+1F0A1+) — `seguisym.ttf`; емодзі-силуети (зодіак, емоції, сни) — `seguiemj.ttf` (монохромно, fill-колір); ієрогліфи триграм — `msyh.ttc`; іврит (шляхи) — `arial.ttf`.

## Третя хвиля — астрологічні оракули (scripts/import_astro_wave.py, 2026-09-15)
Карти 45–50 (системи 34–39, категорія «астрологічні»), 287 карт. Тексти — власний навчальний переказ (UK-база + EN/RU), графіка — процедурна (`generate_deck_images.py`, без копірайту). Колоди лише «навчальні аналоги» комерційних (структура/концепція + посилання-надихач у профілі):
- Weatherstone Astrology Oracle — deck 45 (22): weatherstonegroup.com.
- Astrological Year (Донна Вудвелл) — deck 46 (50): selfstudydaily.com.
- Arcana of Astrology (Донна Вудвелл) — deck 47 (54): thearcanaofastrology.com.
- Oracle of the Radiant Sun (Керолайн Сміт та Джон Астор) — deck 48 (84, 7 мастей × 12 знаків): hayhouse.com/oracle-of-the-radiant-sun.
- Musing Mystical Astrology (Джилл Вінтерстайн) — deck 49 (55, 10 планет + 45 пар): musingmystical.com/free-astrology-oracle-deck.
- Astrology Reference (референс, БД-, єдиний `is_reference_only=1`) — deck 50 (22): russellcottrell.com/astrology/ (факти).
Факти (управителі знаків, стихії, домени планет, фази, астероїди, затемнення) — загальновідомі астрологічні відомості. Значення карт — оригінальні формулювання AI-Arcanum, співзвучні навчальній концепції колод-надихачів.

## Четверта хвиля — 5 навчальних таро-колод (scripts/import_tarot_wave.py, 2026-09-16)
Система «Таро» (id 1), колоди **51–55**, 390 карт (5 × 78). Тексти — ВЛАСНИЙ навчальний переказ поверх нашої бази RWS (deck 1), тематичні ключі кожної колоди (UK-база + EN/RU); глибокі значення (любов/кар'єра/здоров'я/духовність/перевернуте) копіюються з deck 1. Колоди — «навчальні аналоги» комерційних (структура 78 = 22+56, концепція + source_url-надихач; скани/тексти НЕ копіюються):
- Angel Tarot (Travis McHenry, Rockpool Publishing) — deck 51: rockpoolpublishing.com.au/angel-tarot (72 ангели Шемхамфорашу).
- Tarot Neocolonial de las Americas (Patrick McGrath Muniz, U.S. Games, 2022) — deck 52: usgamesinc.com/tarot-neocolonial-de-las-americas (традиція Вейта).
- Fablemaker's Animated Tarot (Misty Bourne, US Games, 2022) — deck 53: usgamesinc.com/the-fablemakers-animated-tarot.
- Alice in Wonderland Tarot (Lisa Vannini, Insight Editions, 2022) — deck 54: insighteditions.com/products/alice-in-wonderland-tarot-deck.
- Vision Quest Tarot (Gayan S. Winter, AGMuller 1998/2016) — deck 55: agmuller.net/vision-quest-tarot (традиція Тота; у нас масті перейменовано: Стріли/Чаші/Пера/Плоди).
Графіка — процедурна вітка «навчальн»+«таро» у `generate_deck_images.py` (5 палітр, старші — сяйво + номер, молодші — піпки/двір); файли `images/51…55/`, `assets/51…55/`; покриття 390/390 (0 пропусків).

## П'ята хвиля — ще 2 навчальні таро-колоди (scripts/import_tarot_wave.py, 2026-09-16)
Та сама система «Таро» (id 1), колоди **56–57**, +156 карт (2 × 78). Той самий шаблон «навчальний аналог»: власний переказ поверх RWS (deck 1), тематичні ключі, глибокі тексти з deck 1, процедурна графіка, скани НЕ копіюються:
- Golden Black Cat Tarot (Helena de Almeida, Königsfurt-Urania, 2022) — deck 56: usgamesinc.com/golden-black-cat-tarot (традиція Вейта; образ — чорний кіт із золотом).
- Folklore Tarot (Rowan Ortins, U.S. Games, 2023) — deck 57: usgamesinc.com/folklore-tarot (традиція Вейта; тема — міфологія народів світу).
Графіка — та сама вітка «навчальн»+«таро» (додано 2 палітри: `goldencat`, `folklore`); файли `images/56…57/`, `assets/56…57/`; покриття 156/156 (0 пропусків). Разом: 50 колод / 1723 карти / 38 систем.

## UI-зміни (навігація / сітка арканів / каталог розкладів / стаття-гайд, 2026-09-16)
- Навігація: єдині вкладки на всіх сторінках — Значення карт / Види розкладів / Гайди і статті / Квіз.
- Сторінка колоди `/decks/*`: вкладка «Значення карт» (за замовчуванням для таро-колод) — сітка Старших (0–XXI, номер+назва+ключ) + Молодші по мастях (Жезли/Кубки/Мечі/Пентаклі ×14).
- Сторінка `/spreads`: каталог із 11 схем розкладів (назва, рівень, час, призначення) + онлайн-інструмент випадкового розтягу.
- Стаття 45 (`45-tarot-spreads`, UK/EN/RU): «Види розкладів Таро» — описи 11 схем. Джерела: власні навчальні матеріали + Waite (1911, public domain). Класифікація розкладів (Кельтський хрест, Подкова, тощо) — загальновідомі в тарологічній традиції.
