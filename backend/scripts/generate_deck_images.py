"""generate_deck_images.py — процедурні ілюстрації для колод без PD-сканів.
Автентичний контент, намальований кодом (не фото):
  І-Цзин — 6 рис гексаграми, розібрані з тексту Легга в БД (NINE=ян, SIX=інь);
  Футарк/поема — справжні рунічні знаки (Segoe UI Symbol);
  Місяць — фази за номером (частка освітлення);
  Астро — знаки ♈…♓, планети ☉…♇, стихії-трикутники;
  Цолькин — кольори печаток + нумерали крапками/рисками мая;
  Нумерологія/гральні — цифри/ранги+масті; решта — фірмова емблема.
Запуск з папки backend/: python scripts/generate_deck_images.py [--only DECK_ID]
Пише у Database/images/<deck>/ + frontend/public/assets/<deck>/ і оновлює image_path.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image, ImageDraw, ImageFont

try:  # Windows-консоль (cp1251) не вміє ʼ— поза ASCII
    import sys as _sys
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from app.core.database import Base, SessionLocal, engine
from app.models import Card, Deck

ROOT = Path(__file__).resolve().parents[2]
DB_IMG = Path(__file__).resolve().parents[1] / "Database" / "images"
PUB = ROOT / "frontend" / "public" / "assets"

W, H = 512, 840
ARIAL = "C:/Windows/Fonts/arial.ttf"
SYM = "C:/Windows/Fonts/seguisym.ttf"
HIST = "C:/Windows/Fonts/seguihis.ttf"  # руни (у seguisym лише tofu)

FUTHARK = ["ᚠ", "ᚢ", "ᚦ", "ᚨ", "ᚱ", "ᚲ", "ᚷ", "ᚹ", "ᚺ", "ᚾ", "ᛁ", "ᛄ",
           "ᛇ", "ᛈ", "ᛉ", "ᛋ", "ᛏ", "ᛒ", "ᛖ", "ᛗ", "ᛚ", "ᛜ", "ᛟ", "ᛞ"]
POEM_RUNES = ["ᚠ", "ᚢ", "ᚦ", "ᚩ", "ᚱ", "ᚳ", "ᚷ", "ᚹ", "ᚻ", "ᚾ", "ᛁ", "ᛄ",
              "ᛇ", "ᛈ", "ᛉ", "ᛋ", "ᛏ", "ᛒ", "ᛖ", "ᛗ", "ᛚ", "ᛜ", "ᛞ", "ᛟ",
              "ᚪ", "ᚫ", "ᚣ", "ᛡ", "ᛠ"]
ZODIAC = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
PLANET_GLYPH = {"Сонце": "☉", "Місяць": "☽", "Меркурій": "☿", "Венера": "♀",
                "Марс": "♂", "Юпітер": "♃", "Сатурн": "♄", "Уран": "♅",
                "Нептун": "♆", "Плутон": "♇"}
SUIT_GLYPH = {"Чирва": "♥", "Бубна": "♦", "Трефа": "♣", "Піка": "♠"}
SUIT_COLOR = {"Чирва": "#b03030", "Бубна": "#b03030", "Трефа": "#2a2a2a", "Піка": "#2a2a2a"}
SEAL_COLORS = ["#a33327", "#e8e2d2", "#2f5d8a", "#c9962e"]  # червоний/білий/синій/жовтий
LENORMAND_INSET = {  # традиційні відповідності гральним картам (факти)
    "1": "9♥", "2": "6♦", "3": "10♠", "4": "K♥", "5": "7♥", "6": "K♣",
    "7": "Q♣", "8": "9♦", "9": "Q♠", "10": "J♦", "11": "J♣", "12": "7♦",
    "13": "J♠", "14": "9♣", "15": "10♣", "16": "6♥", "17": "Q♥", "18": "10♥",
    "19": "6♠", "20": "8♠", "21": "8♣", "22": "Q♦", "23": "7♣", "24": "J♥",
    "25": "A♣", "26": "10♦", "27": "7♠", "28": "A♥", "29": "A♠", "30": "K♠",
    "31": "A♦", "32": "8♥", "33": "8♦", "34": "K♦", "35": "9♠", "36": "6♣"}

THEMES = {
    "Таро Уэйта-Смит": ("#f5edd8", "#2a2350", "#8a6b25"),
    "default": ("#10173a", "#e8c87a", "#d4a94e"),
    "light": ("#f5edd8", "#2a2350", "#8a6b25"),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def base_card(bg, fg, frame):
    img = Image.new("RGB", (W, H), bg)
    g = ImageDraw.Draw(img)
    g.rectangle([14, 14, W - 14, H - 14], outline=frame, width=6)
    g.rectangle([30, 30, W - 30, H - 30], outline=frame, width=2)
    return img, g


def centered_text(g, y, text, fnt, fill, max_w=W - 120):
    while fnt.size > 20 and g.textlength(text, font=fnt) > max_w:
        fnt = font(fnt.path, fnt.size - 4)
    g.text((W / 2, y), text, font=fnt, fill=fill, anchor="ma")
    return fnt.size


def theme_for(deck_name):
    if "Уэйта" in deck_name or "Waite" in deck_name:
        return THEMES["Таро Уэйта-Смит"]
    return THEMES["default"]


def draw_hexagram(g, cx, top, lines, color):
    """lines: 6 bool знизу вгору (True=ян суцільна)."""
    for i, yang in enumerate(lines):
        y = top + (5 - i) * 56
        if yang:
            g.rectangle([cx - 130, y - 13, cx + 130, y + 13], fill=color)
        else:
            g.rectangle([cx - 130, y - 13, cx - 18, y + 13], fill=color)
            g.rectangle([cx + 18, y - 13, cx + 130, y + 13], fill=color)


ORDINAL = {"first": 0, "second": 1, "third": 2, "fourth": 3, "fifth": 4,
           "sixth": 5, "topmost": 5, "lowest": 0}


def parse_hexagram_lines(text):
    """Витягує 6 рис із тексту Легга: NINE=ян, SIX=інь, за порядком first..sixth/topmost.
    Виноски відрізаємо (там номенклатура first six / first nine псує картину)."""
    body = re.split(r"Footnotes?", text, maxsplit=1)[0]
    lines = [None] * 6
    for m in re.finditer(r"(first|second|third|fourth|fifth|sixth|topmost|lowest)[^.]{0,60}?\b(NINE|SIX)\b",
                         body, re.I | re.S):
        if lines[ORDINAL[m.group(1).lower()]] is None:
            lines[ORDINAL[m.group(1).lower()]] = (m.group(2).upper() == "NINE")
    if any(v is None for v in lines):
        return None
    return lines


def has_glyph(fnt, char):
    try:
        return fnt.getmask(char).getbbox() is not None
    except Exception:
        return False


def draw_moon(img, g, cx, cy, r, frac, color):
    """frac: 0=молодик..1=повня. Освітлено праворуч від термінатора."""
    import math
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    if frac <= 0:
        return
    tx = cx + r * math.cos(math.pi * min(max(frac, 0.0), 1.0))
    moon = Image.new("RGB", img.size, "#0c1130")
    mg = ImageDraw.Draw(moon)
    mg.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for px in range(int(max(0, cx - r)), int(min(W, cx + r + 1))):
        if px <= tx:
            mg.line([px, cy - r, px, cy + r], fill="#0c1130")
    img.paste(moon, (0, 0))


def maya_number(g, cx, cy, n, color):
    """Нумерали мая: крапки (1-4) над рисками (5)."""
    bars, dots = divmod(max(0, n), 5)
    y = cy - (dots * 34 + bars * 30) / 2
    for _ in range(dots):
        g.ellipse([cx - 11, y, cx + 11, y + 22], fill=color)
        y += 34
    for _ in range(bars):
        g.rectangle([cx - 60, y, cx + 60, y + 18], fill=color)
        y += 30


def short_name(card):
    tr = card.translations or {}
    return card.name


def render(card, deck):
    bg, fg, frame = theme_for(deck.name)
    img, g = base_card(bg, fg, frame)
    f_big = font(SYM, 200)
    f_rune = font(HIST, 200)
    f_med = font(ARIAL, 44)
    f_small = font(ARIAL, 30)
    name = short_name(card)
    num = card.number or ""
    arc = (card.arcana_type or "").lower()

    def title_block(top=620):
        centered_text(g, top, str(num), font(ARIAL, 40), frame)
        centered_text(g, top + 52, name, f_med, fg)

    dn = deck.name
    dnl = dn.lower()
    if "и-цзин" in dnl or "і-цзин" in dnl:
        lines = parse_hexagram_lines(card.meaning_general or "")
        if lines:
            draw_hexagram(g, W / 2, 150, lines, fg)
        centered_text(g, 560, f"Гексаграма {num}", f_small, frame)
        title_block(660)
    elif "футарк" in dnl or "futhark" in dnl:
        try:
            idx = int(num) - 1
            glyph = FUTHARK[idx] if 0 <= idx < 24 else "ᚠ"
        except ValueError:
            glyph = "ᚠ"
        g.text((W / 2, 330), glyph, font=f_rune, fill=fg, anchor="mm")
        title_block(600)
    elif "поем" in dn or "поэм" in dn:
        try:
            idx = int(num) - 1
            glyph = POEM_RUNES[idx] if 0 <= idx < 29 else "ᚠ"
        except ValueError:
            glyph = "ᚠ"
        g.text((W / 2, 330), glyph, font=f_rune, fill=fg, anchor="mm")
        title_block(600)
    elif "місячн" in dnl or "лунн" in dnl or "moon" in dnl:
        frac = {1: 0.0, 2: 0.15, 3: 0.5, 4: 0.75, 5: 1.0, 6: 0.75, 7: 0.5, 8: 0.15}.get(int(num or 1), 0.5)
        draw_moon(img, g, W / 2, 350, 120, frac, fg)
        title_block(600)
    elif "астролог" in dnl or "astrolog" in dnl:
        glyph = None
        if "Знак" in (card.arcana_type or ""):
            try:
                glyph = ZODIAC[int(num) - 1]
            except (ValueError, IndexError):
                pass
        elif "Планет" in (card.arcana_type or ""):
            glyph = PLANET_GLYPH.get(name)
        elif "Стих" in (card.arcana_type or ""):
            glyph = {"Вогонь": "🜂", "Земля": "🜃", "Повітря": "🜁", "Вода": "🜄",
                 "Огонь": "🜂"}.get(name)
        drawn = False
        if glyph and has_glyph(font(SYM, 200), glyph):
            g.text((W / 2, 330), glyph, font=font(SYM, 200), fill=fg, anchor="mm")
            drawn = True
        if not drawn:
            # стихії fallback: трикутники (вогонь/повітря вгору, земля/вода вниз)
            cx, cy, s = W / 2, 330, 110
            up = ("огонь" in name.lower() or "вогонь" in name.lower()
                  or "ітря" in name.lower() or "оздух" in name.lower())
            if up:
                g.polygon([(cx - s, cy + s), (cx + s, cy + s), (cx, cy - s)], outline=fg, width=8)
            else:
                g.polygon([(cx - s, cy - s), (cx + s, cy - s), (cx, cy + s)], outline=fg, width=8)
        title_block(600)
    elif "нумеролог" in dnl or "numerolog" in dnl:
        g.text((W / 2, 330), str(num), font=font(ARIAL, 220), fill=fg, anchor="mm")
        title_block(600)
    elif "гральн" in dnl or "игральн" in dnl or "playing" in dnl:
        suit = card.suit or ""
        glyph = SUIT_GLYPH.get(suit, "✦")
        col = SUIT_COLOR.get(suit, fg)
        rank = str(num or "").split("-")[-1]
        g.text((70, 60), rank, font=font(ARIAL, 64), fill=col, anchor="ma")
        g.text((70, 130), glyph, font=font(SYM, 56), fill=col, anchor="ma")
        g.text((W / 2, 380), glyph, font=font(SYM, 220), fill=col, anchor="mm")
        title_block(620)
    elif "ленорман" in dnl or "lenormand" in dnl:
        inset = LENORMAND_INSET.get(str(num), "")
        g.text((W / 2, 300), str(num), font=font(ARIAL, 150), fill=fg, anchor="mm")
        if inset:
            g.text((W / 2, 470), inset, font=font(ARIAL, 72), fill=frame, anchor="mm")
        title_block(600)
    elif "цолькин" in dnl or "tzolkin" in dnl:
        if str(num or "").startswith("S"):
            idx = int(str(num[1:])) - 1
            col = SEAL_COLORS[idx % 4]
            g.ellipse([W / 2 - 110, 220, W / 2 + 110, 440], fill=col, outline=frame, width=5)
            g.text((W / 2, 330), str(num), font=font(ARIAL, 64), fill="#10173a" if idx % 4 == 1 else fg, anchor="mm")
        else:
            maya_number(g, W / 2, 330, int(str(num or "T0")[1:]), fg)
        title_block(600)
    else:
        g.text((W / 2, 300), "✦", font=font(SYM, 170), fill=fg, anchor="mm")
        title_block(560)
    return img


def slug_deck(deck_id, deck_name):
    return f"{deck_id:02d}"


def run(only=None):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    made = linked = skipped_hex = 0
    try:
        decks = db.query(Deck).all()
        if only:
            decks = [d for d in decks if str(d.id) == str(only)]
        for deck in decks:
            if "Уэйта" in deck.name or "Waite" in deck.name:
                continue  # у RWS є фото
            cards = db.query(Card).filter_by(deck_id=deck.id).all()
            if not cards:
                continue
            ddir = f"{deck.id:02d}"
            for base in (DB_IMG / ddir, PUB / ddir):
                base.mkdir(parents=True, exist_ok=True)
            for c in cards:
                fname = f"{re.sub(r'[^\w\-]+', '_', str(c.number or c.id))}.jpg"
                rel = f"{ddir}/{fname}"
                dest = DB_IMG / rel
                if not dest.exists():
                    render(c, deck).save(dest, quality=82)
                    made += 1
                pub = PUB / rel
                if not pub.exists():
                    Image.open(dest).save(pub, quality=72, optimize=True)
                web = f"/assets/{ddir}/{fname}"
                if c.image_path != web:
                    c.image_path = web
                    linked += 1
            print(f"[{deck.id}] {deck.name[:40]}: карт {len(cards)}")
        db.commit()
        print(f"[gen] згенеровано: {made}, привʼязано: {linked}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys as _s
    only = _s.argv[_s.argv.index("--only") + 1] if "--only" in _s.argv else None
    run(only)
