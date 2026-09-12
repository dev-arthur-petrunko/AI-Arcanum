"""import_public_domain_sources.py
Скрипт наповнення БД матеріалами у СУСПІЛЬНОМУ НАДБАННІ.

Джерела (перевірено 2026-09-12, усі public domain):
  1. A.E. Waite "The Pictorial Key to the Tarot" (1911) — повний OCR-текст ОДНИМ
     запитом з archive.org (старого шаблону sacred-texts pktNN.htm більше нема — 404,
     сайт переїхав на SPA; Gutenberg #43548 — це НЕ Уейт, а де Лоранс 1918, не використовувати).
  2. Скани колоди Rider-Waite-Smith (1909/1910, PD) — Commons API, файли "RWS Tarot NN ...".
  3. І-Цзин, переклад James Legge (1899) — sacred-texts /ich/icNN.htm (legacy .htm ще віддаються).
  4. Англосаксонська рунічна поема (оригінал + пер. Bruce Dickins, 1915) — Wikisource.

НЕ завантажується автоматично: сучасні авторські сайти (Labyrinthos, Biddy Tarot,
astro.com тощо) — див. import_modern_source_manually() і scripts/import_from_csv.py.

Запуск (з папки backend/):
    pip install -r requirements.txt
    python scripts/import_public_domain_sources.py --only waite --dry-run
    python scripts/import_public_domain_sources.py --only runes
    python scripts/import_public_domain_sources.py --only iching --limit 3
    python scripts/import_public_domain_sources.py --only images --limit 5
    python scripts/import_public_domain_sources.py   # все цілком (78 картинок + 64 гексаграми)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
BACKEND = HERE.parents[1]
ROOT = HERE.parents[2]
sys.path.insert(0, str(BACKEND))

import requests
from bs4 import BeautifulSoup

from app.core.database import Base, SessionLocal, engine
from app.models import Card, Deck, System

HEADERS = {
    "User-Agent": "FortuneCardsEncyclopediaBot/1.0 "
                  "(educational, non-commercial; contact: admin@example.com)"
}
# Бінарні файли upload.wikimedia.org ріжуть ботовий UA (403) — для самих картинок
# звичайний браузерний UA (затримка DELAY зберігається, навантаження те саме).
IMAGE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}
DELAY = 1.5

try:  # Windows-консоль (cp1251) падає на â/ê/— поза ASCII: перемикаємо stdout на UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CACHE_DIR = BACKEND / "Database" / "_pd_cache"
IMAGES_DIR = ROOT / "frontend" / "src" / "assets" / "card_images" / "rws"

WAITE_TXT_URL = (
    "https://archive.org/download/A.EWaiteThePictorialKeyToTheTarot/"
    "A.%20E%20Waite%20-%20The%20Pictorial%20Key%20to%20the%20Tarot_djvu.txt"
)
WAITE_REF = "A.E. Waite, The Pictorial Key to the Tarot (1911), public domain (via Internet Archive)"
LEGGE_REF = "James Legge, The Yi King (Sacred Books of the East, 1899), public domain"
RUNE_REF = ("Bruce Dickins, Runic and Heroic Poems of the Old Teutonic Peoples (1915), "
            "public domain (via Wikisource); Old English original 8th–9th c.")

# Порядок маркерів у §3 ч.III Уейта ("Greater Arcana and their Divinatory Meanings").
WAITE_MARKERS = [
    ("0", "Шут", ["THE FOOL"]),
    ("I", "Маг", ["THE MAGICIAN", "THE MAGUS"]),
    ("II", "Верховная Жрица", ["HIGH PRIESTESS"]),
    ("III", "Императрица", ["THE EMPRESS"]),
    ("IV", "Император", ["THE EMPEROR"]),
    ("V", "Иерофант", ["HIEROPHANT"]),
    ("VI", "Влюблённые", ["THE LOVERS"]),
    ("VII", "Колесница", ["THE CHARIOT"]),
    ("VIII", "Сила", ["FORTITUDE", "STRENGTH"]),
    ("IX", "Отшельник", ["THE HERMIT"]),
    ("X", "Колесо Фортуны", ["WHEEL OF FORTUNE"]),
    ("XI", "Справедливость", ["JUSTICE"]),
    ("XII", "Повешенный", ["HANGED MAN"]),
    ("XIII", "Смерть", ["DEATH"]),
    ("XIV", "Умеренность", ["TEMPERANCE"]),
    ("XV", "Дьявол", ["THE DEVIL"]),
    ("XVI", "Башня", ["THE TOWER"]),
    ("XVII", "Звезда", ["THE STAR"]),
    ("XVIII", "Луна", ["THE MOON"]),
    ("XIX", "Солнце", ["THE SUN"]),
    ("XX", "Суд", ["JUDGEMENT", "JUDGMENT"]),
    ("XXI", "Мир", ["THE WORLD"]),
]

ROMAN_UP = {"0": "0", "i": "I", "ii": "II", "iii": "III", "iv": "IV", "v": "V",
            "vi": "VI", "vii": "VII", "viii": "VIII", "ix": "IX", "x": "X",
            "xi": "XI", "xii": "XII", "xiii": "XIII", "xiv": "XIV", "xv": "XV",
            "xvi": "XVI", "xvii": "XVII", "xviii": "XVIII", "xix": "XIX",
            "xx": "XX", "xxi": "XXI"}


def get(url: str, timeout: int = 30, binary: bool = False) -> requests.Response:
    headers = IMAGE_HEADERS if binary else HEADERS
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r


def soup_text(url: str) -> tuple[str, str]:
    """Повертає (title, plain_text) для legacy-сторінки sacred-texts."""
    html = get(url).text
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.select("nav, header, footer, script, style"):
        tag.decompose()
    title_tag = soup.find("h1") or soup.find("h2") or soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else url
    paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    return title, "\n\n".join(p for p in paras if len(p) > 40)


# ---------------------------------------------------------------- 1. Уейт
def fetch_waite_text(cache: Path) -> str:
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists():
        print(f"[cache] {cache.name} ({cache.stat().st_size // 1024} KB)")
        return cache.read_text(encoding="utf-8", errors="replace")
    print(f"[GET] {WAITE_TXT_URL}")
    text = get(WAITE_TXT_URL, timeout=120).text
    cache.write_text(text, encoding="utf-8")
    time.sleep(DELAY)
    return text


def split_waite_majors(full: str) -> dict[str, str]:
    """Ріже текст на 22 фрагменти за ordered-маркерами (стійко до OCR-шуму)."""
    upper = re.sub(r"\s+", " ", full.upper())
    # працюємо лише з дивінаторною секцією, якщо вона знаходиться
    start = upper.find("DIVINATORY MEANINGS")
    section = upper[start:] if start != -1 else upper
    positions: list[tuple[int, str]] = []
    for number, _ru, variants in WAITE_MARKERS:
        hits = [section.find(v) for v in variants if section.find(v) != -1]
        if hits:
            positions.append((min(hits), number))
    positions.sort()
    out: dict[str, str] = {}
    for i, (pos, number) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else min(pos + 12000, len(section))
        out[number] = section[pos:end].strip()[:8000]
    return out


def save_waite_to_db(fragments: dict[str, str], dry_run: bool = False) -> tuple[int, int]:
    db = SessionLocal()
    try:
        deck = db.query(Deck).filter(Deck.name.contains("Уэйта")).first() \
            or db.query(Deck).filter(Deck.name.contains("Waite")).first()
        if not deck:
            print("[WARN] колоду Уейта-Сміт не знайдено — спочатку python scripts/seed_db.py")
            return 0, 0
        updated = matched = 0
        for number, _ru, _v in WAITE_MARKERS:
            card = db.query(Card).filter_by(deck_id=deck.id, number=number).first()
            if not card:
                continue
            matched += 1
            frag = fragments.get(number, "")
            if frag and not dry_run:
                tr = dict(card.translations or {})
                en = dict(tr.get("en", {}))
                en["meaning_general_waite1911"] = frag
                en["source_reference"] = WAITE_REF
                card.translations = {**tr, "en": en}
                card.symbolism = ((card.symbolism or "") + f"\nИсточник EN: {WAITE_REF}").strip()
                updated += 1
        if not dry_run:
            db.commit()
        print(f"[waite] matched={matched}/22 fragments={len(fragments)} updated={updated}")
        return matched, updated
    finally:
        db.close()


# ---------------------------------------------------------------- 2. RWS-скани
def fetch_rws_images(limit: int | None = None, dry_run: bool = False) -> list[dict]:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    api = "https://commons.wikimedia.org/w/api.php"
    # Канонічний PD-набір; як порожній — скануємо категорію за regex.
    category = "Category:Rider-Waite-Smith tarot deck (TaionWC)"
    params = {"action": "query", "list": "categorymembers", "cmtitle": category,
              "cmtype": "file", "cmlimit": "500", "format": "json"}
    try:
        members = requests.get(api, params=params, headers=HEADERS, timeout=30).json() \
            .get("query", {}).get("categorymembers", [])
    except Exception as e:
        print(f"[WARN] категорія {category}: {e}; пробую Rider-Waite tarot deck")
        params["cmtitle"] = "Category:Rider-Waite tarot deck"
        members = requests.get(api, params=params, headers=HEADERS, timeout=30).json() \
            .get("query", {}).get("categorymembers", [])
    time.sleep(DELAY)
    wanted = [m["title"] for m in members
              if re.search(r"RWS Tarot \d+", m["title"], re.I)]
    if limit:
        wanted = wanted[:limit]
    print(f"[images] кандидатів: {len(wanted)}")
    downloaded = []
    for title in wanted:
        info = requests.get(api, params={"action": "query", "titles": title, "prop": "imageinfo",
                                         "iiprop": "url", "format": "json"},
                            headers=HEADERS, timeout=30).json()
        time.sleep(0.5)
        for page in info.get("query", {}).get("pages", {}).values():
            ii = page.get("imageinfo")
            if not ii:
                continue
            url = ii[0]["url"].split("?")[0]
            fname = re.sub(r"[^\w.\-]", "_", title.replace("File:", ""))
            dest = IMAGES_DIR / fname
            if dest.exists():
                downloaded.append({"title": title, "local_path": str(dest), "skipped": True})
                continue
            if dry_run:
                downloaded.append({"title": title, "local_path": str(dest), "skipped": "dry-run"})
                continue
            dest.write_bytes(get(url, timeout=60, binary=True).content)
            print(f"[OK] {fname}")
            downloaded.append({"title": title, "local_path": str(dest)})
            time.sleep(DELAY)
    # Привʼязка majors за номером в імені файлу
    if not dry_run:
        link_rws_images_to_cards()
    return downloaded


def link_rws_images_to_cards() -> int:
    db = SessionLocal()
    try:
        deck = db.query(Deck).filter(Deck.name.contains("Уэйта")).first()
        if not deck:
            return 0
        linked = 0
        for f in sorted(IMAGES_DIR.glob("*")):
            m = re.search(r"RWS[_\s]?Tarot[_\s]?(\d{1,2})", f.name, re.I)
            if not m:
                continue
            num = int(m.group(1))
            if num > 21:
                continue  # молодші аркани мапляться вручну (див. docs)
            number = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
                      "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX",
                      "XX", "XXI"][num]
            card = db.query(Card).filter_by(deck_id=deck.id, number=number).first()
            if card:
                card.image_path = f"/assets/card_images/rws/{f.name}"
                linked += 1
        db.commit()
        print(f"[images] привʼязано старших арканів: {linked}/22")
        return linked
    finally:
        db.close()


# ---------------------------------------------------------------- 3. І-Цзин
def fetch_iching(limit: int | None = None) -> list[dict]:
    out = []
    n = limit or 64
    for i in range(1, n + 1):
        url = f"https://sacred-texts.com/ich/ic{str(i).zfill(2)}.htm"
        try:
            title, text = soup_text(url)
        except Exception as e:
            print(f"[WARN] гексаграма {i}: {e}")
            continue
        out.append({"hexagram_number": i, "title": title, "text": text, "source_url": url})
        print(f"[OK] гексаграма {i}: {title[:60]}")
        time.sleep(DELAY)
    return out


def save_iching_to_db(items: list[dict], dry_run: bool = False) -> int:
    db = SessionLocal()
    try:
        system = db.query(System).filter_by(name="И-Цзин").first()
        if not system:
            if dry_run:
                print("[dry-run] створив би System І-Цзин")
                return 0
            system = System(name="И-Цзин", category="гадательные",
                            description="64 гексаграммы Книги Перемен; карточная адаптация для изучения.",
                            origin_country="Китай", approx_year=-1000,
                            translations={"uk": {"name": "І-Цзин"},
                                          "en": {"name": "I Ching"}})
            db.add(system)
            db.flush()
        deck = db.query(Deck).filter_by(name="И-Цзин (Легг, 1899)").first()
        if not deck:
            if dry_run:
                print("[dry-run] створив би Deck І-Цзин (Легг, 1899)")
                return 0
            deck = Deck(system_id=system.id, name="И-Цзин (Легг, 1899)",
                        author="James Legge (перевод, 1899, public domain)",
                        year=1899, card_count=64,
                        description="Перевод Легга, гексаграммы 1–64.",
                        translations={"uk": {"name": "І-Цзин (Легг, 1899)"},
                                      "en": {"name": "I Ching (Legge, 1899)"}})
            db.add(deck)
            db.flush()
        added = 0
        for h in items:
            exists = db.query(Card).filter_by(deck_id=deck.id, number=str(h["hexagram_number"])).first()
            if exists or dry_run:
                continue
            db.add(Card(deck_id=deck.id, number=str(h["hexagram_number"]), name=h["title"],
                        arcana_type="Гексаграмма",
                        meaning_general=h["text"][:12000],
                        symbolism=f"Источник: {LEGGE_REF} ({h['source_url']})",
                        translations={"en": {"name": h["title"], "source_reference": LEGGE_REF}}))
            added += 1
        if not dry_run:
            db.commit()
        print(f"[iching] нових: {added}")
        return added
    finally:
        db.close()


# ---------------------------------------------------------------- 4. Руни
# Джерело: Wikisource, Dickins 1915 (PD). Структура сторінки: давньоанглійські
# строфи з нумерованими заголовками (<номер рядка> + імʼя руни), далі англійський
# переклад Діккінса в тому самому порядку (29 строф). SPA sacred-texts для цього не годиться
# (контент підвантажується JS, у статиці порожньо — перевірено 2026-09-12).
RUNE_WIKI_URL = ("https://en.wikisource.org/wiki/Runic_and_Heroic_Poems_of_the_Old_Teutonic_Peoples/"
                 "The_Runic_Poems/The_Anglo-Saxon_Runic_Poem")

RUNE_OE_NAMES = ["Feoh", "Ur", "Ðorn", "Os", "Rad", "Cen", "Gyfu", "Wen", "Hægl",
                 "Nyd", "Is", "Ger", "Eoh", "Peorð", "Eolh", "Sigel", "Tir",
                 "Beorc", "Eh", "Man", "Lagu", "Ing", "Eðel", "Dæg", "Ac",
                 "Æsc", "Yr", "Iar", "Ear"]
RUNE_RU = ["Феох", "Ур", "Торн", "Ос", "Рад", "Кен", "Гифу", "Вин", "Хегль",
           "Нид", "Ис", "Гер", "Эох", "Пеорт", "Эольх", "Сигель", "Тир",
           "Беорк", "Эх", "Ман", "Лагу", "Инг", "Этель", "Дег", "Ак",
           "Эск", "Юр", "Иар", "Эар"]
RUNE_UK = ["Феох", "Ур", "Торн", "Ос", "Рад", "Кен", "Гіфу", "Вин", "Хегль",
           "Нід", "Іс", "Гер", "Еох", "Пеорт", "Еольх", "Сігель", "Тір",
           "Беорк", "Ех", "Ман", "Лагу", "Інг", "Етель", "Дег", "Ак",
           "Еск", "Юр", "Іар", "Еар"]


def _norm_oe(s: str) -> str:
    return s.replace("Ð", "Þ").replace("þorn", "þorn").strip()


def fetch_rune_poem() -> list[dict]:
    html = get(RUNE_WIKI_URL).text
    soup = BeautifulSoup(html, "html.parser")
    body = soup.select_one("div.mw-parser-output")
    lines = body.get_text("\n").splitlines()

    # --- давньоанглійські строфи: два формати заголовків ---
    #   A: "<число>" + "<Імʼя>" (+ "[n]"); B: "<число> <Імʼя> <початок вірша>" в одному рядку.
    # Імена НЕ матчимо строго (у тексті варіанти Wenne, Eolh-sec) — порядок строф
    # фіксований (Feoh→Ear), імена/переклади беремо за індексом.
    oe: list[str] = []
    NAME = r"[A-ZÆÐÞ][A-Za-zæøþðÆØÞÐ]{1,11}"
    SKIP = re.compile(r"^(\[\s*\d+\s*\]|\d{1,3}\s*|\[|\]|​)\s*$")
    HEAD_INLINE = re.compile(r"\d{1,3}\s+(" + NAME + r")\b\s*(.*)")
    HEAD_NEXT = re.compile(r"(" + NAME + r")(?:-.*)?\b\s*(.*)")

    def is_head_at(j: int) -> re.Match | None:
        """Заголовок строфи в позиції j (формати A/B/C), інакше None."""
        if j >= len(lines):
            return None
        cur = lines[j] or ""
        if re.fullmatch(r"\d{1,3}\s*", cur) and j + 1 < len(lines):
            m = HEAD_NEXT.match((lines[j + 1] or "").strip())
            if m:
                return m
            return None
        return HEAD_INLINE.match(cur)

    def glue(frags: list[str]) -> str:
        """Склейка літер, розірваних per-letter <span> (o/ð/rum → oðrum)."""
        tokens: list[tuple[str, bool]] = []  # (текст, приклеїти до попереднього через пробіл)
        buf = ""
        for v in frags:
            if len(v) == 1:
                buf += v
            else:
                if buf:
                    v = buf + v
                    buf = ""
                    glued = True
                else:
                    glued = False
                tokens.append((v, glued))
        if buf:
            tokens.append((buf, False))
        out = ""
        for text, glued in tokens:
            if not out:
                out = text
            elif glued:
                out += " " + text
            else:
                out += " / " + text
        return out

    i = 0
    while i < len(lines) and len(oe) < 29:
        m = is_head_at(i)
        if not m:
            i += 1
            continue
        cur = lines[i] or ""
        if re.fullmatch(r"\d{1,3}\s*", cur):
            i += 2
        else:
            i += 1
        if i < len(lines) and re.fullmatch(r"\[\s*\d+\s*\]", (lines[i] or "").strip()):
            i += 1  # виноска-номер "[n]"
        verse = [m.group(2).strip()] if m.group(2).strip() else []
        while i < len(lines) and len(verse) < 14:
            if is_head_at(i):
                break
            s = (lines[i] or "").strip()
            if s and not SKIP.match(s):
                verse.append(s)
            i += 1
        text = glue(verse)
        if len(text) > 20:
            oe.append(text[:4000])

    # --- переклад Діккінса: йде після 2-го "THE ANGLO-SAXON RUNIC POEM", ті самі 29 по порядку ---
    title_hits = [n for n, l in enumerate(lines) if l.strip() == "THE ANGLO-SAXON RUNIC POEM"]
    en: list[str] = []
    if len(title_hits) >= 2:
        region = lines[title_hits[1] + 1:]
        heads = re.compile(r"^(?:[A-ZÆÐÞ]\.(?=\s)|Ger|Eoh|Peor\w*|Eolh|Sigel|Ing|Eth?el|Dæg|Ac|Æsc|Yr|Ior|Iar|Ear)(?=\s|$)")
        cur: list[str] = []
        for ln in region:
            s = ln.strip()
            if not s or s.startswith("↑") or len(s) > 600:
                continue  # виноски й примітки
            if heads.match(s) and cur:
                en.append(" ".join(cur)[:4000])
                cur = [s]
            elif heads.match(s):
                cur = [s]
            elif cur:
                cur.append(s)
            if len(en) == 29:
                break
        if cur and len(en) < 29:
            en.append(" ".join(cur)[:4000])

    print(f"[runes] OE строф: {len(oe)}/29, EN строф: {len(en)}/29")
    out = []
    for k in range(min(len(oe), 29)):
        out.append({"order": k + 1, "oe_name": RUNE_OE_NAMES[k],
                    "oe": oe[k],
                    "en": en[k] if k < len(en) else "",
                    "source_url": RUNE_WIKI_URL})
    return out


def save_runes_to_db(stanzas: list[dict], dry_run: bool = False) -> int:
    db = SessionLocal()
    try:
        system = db.query(System).filter_by(name="Руны").first()
        if not system:
            if dry_run:
                print("[dry-run] створив би System Руни")
                return 0
            system = System(name="Руны", category="гадательные",
                            description="Рунические системы: англосаксонский футорк (поэма VIII–IX вв.), Старший Футарк.",
                            origin_country="Англия / Скандинавия", approx_year=800,
                            translations={"uk": {"name": "Руни"}, "en": {"name": "Runes"}})
            db.add(system)
            db.flush()
        deck = db.query(Deck).filter_by(name="Англосаксонская руническая поэма").first()
        if not deck:
            if dry_run:
                print("[dry-run] створив би Deck рунічної поеми")
                return 0
            deck = Deck(system_id=system.id, name="Англосаксонская руническая поэма",
                        author="аноним VIII–IX вв.; пер. Bruce Dickins (1915), public domain",
                        card_count=len(stanzas),
                        description="29 строф: древнеанглийский оригинал + перевод Диккинса.",
                        translations={"uk": {"name": "Англосаксонська рунічна поема"},
                                      "en": {"name": "Anglo-Saxon Rune Poem"}})
            db.add(deck)
            db.flush()
        else:
            # чистка legacy-картки з першої (невдалої) ітерації парсера
            for junk in db.query(Card).filter_by(deck_id=deck.id).filter(Card.name.like("Строфа %")).all():
                db.delete(junk)
            db.flush()
        added = 0
        for s in stanzas:
            exists = db.query(Card).filter_by(deck_id=deck.id, number=str(s["order"])).first()
            if exists or dry_run:
                continue
            idx = s["order"] - 1
            ru = RUNE_RU[idx] if idx < len(RUNE_RU) else s["oe_name"]
            uk = RUNE_UK[idx] if idx < len(RUNE_UK) else s["oe_name"]
            meaning = f"{s['oe']}" + (f"\n\n[EN, Dickins 1915] {s['en']}" if s.get("en") else "")
            db.add(Card(deck_id=deck.id, number=str(s["order"]),
                        name=f"{ru} ({s['oe_name']})",
                        arcana_type="Руна",
                        keywords_upright=f"руна {ru}: учебное значение строфы",
                        meaning_general=meaning[:12000],
                        symbolism=f"Источник: {RUNE_REF} ({s['source_url']})",
                        translations={"uk": {"name": f"{uk} ({s['oe_name']})"},
                                      "en": {"name": s["oe_name"],
                                             "meaning_general": s.get("en", "")[:6000],
                                             "source_reference": RUNE_REF}}))
            added += 1
        if not dry_run:
            db.commit()
        print(f"[runes] нових: {added}")
        return added
    finally:
        db.close()


# ---------------------------------------------------------------- 5. Сучасні джерела — лише вручну
def import_modern_source_manually(*_a, **_kw):
    """Див. docstring: масовий скрейпінг авторських сайтів заборонений їхніми ToS і копірайтом."""
    raise NotImplementedError(
        "Сучасні джерела — вручну: прочитати → переписати своїми словами → "
        "CSV (name, meaning_general, source_reference) → python scripts/import_from_csv.py"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Імпорт public-domain джерел (див. docstring).")
    ap.add_argument("--only", choices=["waite", "images", "iching", "runes", "all"], default="all")
    ap.add_argument("--limit", type=int, default=None, help="Обмежити число сторінок/файлів (для перевірки).")
    ap.add_argument("--dry-run", action="store_true", help="Не писати в БД і не качати файли.")
    args = ap.parse_args()

    Base.metadata.create_all(bind=engine)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if args.only in ("waite", "all"):
        print("=== 1. Уейт (archive.org, 1 запит) ===")
        try:
            full = fetch_waite_text(CACHE_DIR / "waite_pkt_djvu.txt")
            frags = split_waite_majors(full)
            save_waite_to_db(frags, dry_run=args.dry_run)
        except Exception as e:
            print(f"[WARN] waite: {e}")

    if args.only in ("images", "all"):
        print("\n=== 2. RWS-скани (Wikimedia Commons API) ===")
        try:
            fetch_rws_images(limit=args.limit, dry_run=args.dry_run)
        except Exception as e:
            print(f"[WARN] images: {e}")

    if args.only in ("iching", "all"):
        print("\n=== 3. І-Цзин Легга (sacred-texts /ich/) ===")
        try:
            save_iching_to_db(fetch_iching(limit=args.limit), dry_run=args.dry_run)
        except Exception as e:
            print(f"[WARN] iching: {e}")

    if args.only in ("runes", "all") and not args.limit:
        print("\n=== 4. Рунічна поема (Wikisource Dickins 1915, 1 запит) ===")
        try:
            save_runes_to_db(fetch_rune_poem(), dry_run=args.dry_run)
        except Exception as e:
            print(f"[WARN] runes: {e}")

    try:
        from sqlalchemy import text as _t
        with engine.begin() as conn:
            conn.execute(_t("INSERT OR IGNORE INTO cards_fts(cards_fts) VALUES('rebuild')"))
    except Exception:
        pass
    print("\nГотово.")


if __name__ == "__main__":
    main()
