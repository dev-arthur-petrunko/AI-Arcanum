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
- RWS-сканы (PD): Commons API, категория "Rider-Waite-Smith tarot deck (TaionWC)", файлы "RWS Tarot NN …".
  upload.wikimedia.org требует браузерный UA (ботовий даёт 403).
- И-Цзин, пер. James Legge (1899), 64 гексаграммы: sacred-texts.com/ich/icNN.htm (legacy .htm живы).
- Англосаксонская руническая поэма, 29 строф (OE + пер. Bruce Dickins, 1915, PD):
  en.wikisource.org/wiki/Runic_and_Heroic_Poems…/The_Anglo-Saxon_Runic_Poem
  (sacred-texts neu/ascp/a12.htm — только JS-оболочка, в статике пусто).
- Ручне введення сучасних джерел: прочитати → переписати своїми словами →
  CSV з обовʼязковим source_reference → scripts/import_from_csv.py
