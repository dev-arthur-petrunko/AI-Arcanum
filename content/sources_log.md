# Журнал источников (этика/атрибуция)
- A.E. Waite, Pictorial Key to the Tarot (1911) — public domain; база трактовок RWS (пересказ).
- sacred-texts.com/tarot — архив, сканы RWS.
- Wikimedia Commons — изображения RWS 1909 (public domain).
- Biddy Tarot / Labyrinthos / learntarot.com — только как справка, переписывать своими словами.
- Современные оракулы/МАК — только пересказ концепции + ссылка на официальную книжку колоды.

## Автоматический импорт (scripts/import_public_domain_sources.py, проверено 2026-09-12)
- Waite 1911, EN-текст старших арканов → `translations.en.meaning_general_waite1911`:
  archive.org/download/A.EWaiteThePictorialKeyToTheTarot (OCR, 1 запрос, кэш content/_pd_cache/).
  ВНИМАНИЕ: sacred-texts pktNN.htm мертвы (404, сайт стал SPA); Gutenberg #43548 — это де Лоранс 1918, НЕ Уэйт.
- RWS-сканы (PD): Commons API, категория "Rider-Waite-Smith tarot deck (TaionWC)", файлы "RWS Tarot NN …".
  upload.wikimedia.org требует браузерный UA (ботовий даёт 403).
- И-Цзин, пер. James Legge (1899), 64 гексаграммы: sacred-texts.com/ich/icNN.htm (legacy .htm живы).
- Англосаксонская руническая поэма, 29 строф (OE + пер. Bruce Dickins, 1915, PD):
  en.wikisource.org/wiki/Runic_and_Heroic_Poems…/The_Anglo-Saxon_Runic_Poem
  (sacred-texts neu/ascp/a12.htm — только JS-оболочка, в статике пусто).
- Ручной ввод современных источников: прочитать → переписать своими словами →
  CSV с обязательным source_reference → scripts/import_from_csv.py
