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
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont

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
SERIF = "C:/Windows/Fonts/georgia.ttf"     # І-Цзин: елегантна тиографіка
SERIF_B = "C:/Windows/Fonts/georgiab.ttf"

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

EMOJI = "C:/Windows/Fonts/seguiemj.ttf"   # емоji (у PIL — монохромні силуети)
CJK = "C:/Windows/Fonts/msyh.ttc"         # китайські ієрогліфи (Багуа)

# Справжні Unicode-гліфи огама (U+1680–169F, Segoe UI Historic) — на заміну
# процедурним рискам; фолбек лишається в draw_ogham.
OGHAM_UNICODE = {
    "B": "\u1681", "L": "\u1682", "F": "\u1683", "S": "\u1684", "N": "\u1685",
    "H": "\u1686", "D": "\u1687", "T": "\u1688", "C": "\u1689", "Q": "\u168a",
    "M": "\u168b", "G": "\u168c", "NG": "\u168d", "Z": "\u168e", "R": "\u168f",
    "A": "\u1690", "O": "\u1691", "U": "\u1692", "E": "\u1693", "I": "\u1694",
}

# Емоji-силуети для колод (PIL малює їх монохромними, колір задається fill).
MOON_EMOJI = {1: "🌑", 2: "🌒", 3: "🌓", 4: "🌔", 5: "🌕", 6: "🌖", 7: "🌗", 8: "🌘"}
ZODIAC_EMOJI = ["🐀", "🐂", "🐅", "🐇", "🐉", "🐍", "🐎", "🐐", "🐒", "🐓", "🐕", "🐖"]
PLUTCHIK_EMOJI = {"Радість": "😊", "Сум": "😢", "Довіра": "🤝", "Відраза": "🤢",
                  "Страх": "😨", "Гнів": "😠", "Здивування": "😲", "Очікування": "⏳"}

# Циганські карти (навчальні), 36 символів: гліф у EMOJI + фолбек у SYM.
GYPSY_GLYPH = {
    "1": ("❤", "♥"),  # Кохання
    "2": ("💍", "◈"),  # Вірність
    "3": ("😠", "▲"),  # Ревнощі
    "4": ("🛤", "✶"),  # Дорога
    "5": ("🌅", "☀"),  # Далечінь
    "6": ("💌", "✉"),  # Лист
    "7": ("💰", "¤"),  # Гроші
    "8": ("🎁", "❖"),  # Подарунок
    "9": ("🏠", "⌂"),  # Дім
    "10": ("💒", "♡"),  # Весілля
    "11": ("👶", "◍"),  # Дитина
    "12": ("🏥", "✚"),  # Хвороба
    "13": ("☠", "✠"),  # Ворог
    "14": ("🤝", "☞"),  # Друг
    "15": ("🍀", "★"),  # Удача
    "16": ("💔", "✕"),  # Невдача
    "17": ("⚖", "☽"),  # Суд
    "18": ("👑", "♛"),  # Влада
    "19": ("⛪", "☩"),  # Церква
    "20": ("🎉", "☼"),  # Свято
    "21": ("💧", "☁"),  # Сльози
    "22": ("😊", "☺"),  # Радість
    "23": ("🔥", "▲"),  # Вогонь
    "24": ("🌊", "≈"),  # Вода
    "25": ("🍞", "☗"),  # Хліб
    "26": ("🍷", "☉"),  # Вино
    "27": ("🐎", "♞"),  # Кінь
    "28": ("🐦", "☊"),  # Пташка
    "29": ("🌸", "✿"),  # Квітка
    "30": ("🪞", "◇"),  # Дзеркало
    "31": ("🗝", "☞"),  # Ключ
    "32": ("🔒", "☒"),  # Замок
    "33": ("☀", "☀"),  # Сонце
    "34": ("🌙", "☾"),  # Місяць
    "35": ("⭐", "✦"),  # Зірка
    "36": ("✝", "✚"),  # Хрест
}

# Тасеографія · Чайні листки (навчальна): 20 знаків чаші за suit (англ.).
TASEO_GLYPH = {
    "Anchor": ("⚓", "⚓"),
    "Bird": ("🐦", "☊"),
    "Book": ("📖", "☖"),
    "Bridge": ("🌉", "≋"),
    "Butterfly": ("🦋", "❄"),
    "Cross": ("✝", "✚"),
    "Dog": ("🐕", "☉"),
    "Fish": ("🐟", "Ω"),
    "Flower": ("🌸", "✿"),
    "Heart": ("❤", "♥"),
    "Key": ("🔑", "☞"),
    "Ladder": ("🪜", "◫"),
    "Moon": ("🌙", "☾"),
    "Mountain": ("⛰", "▲"),
    "Ring": ("💍", "◈"),
    "Ship": ("⛵", "⚓"),
    "Snake": ("🐍", "≈"),
    "Star": ("⭐", "✦"),
    "Tree": ("🌳", "⌘"),
    "Umbrella": ("☂", "☂"),
}

# Гральні 36: блок еmoji Playing Cards (U+1F0A1...) з SYM.
_SUIT_BASE = {"S": 0x1F0A0, "H": 0x1F0B0, "D": 0x1F0C0, "C": 0x1F0D0}
_RANK_OFF = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
             "9": 9, "10": 10, "J": 11, "Q": 13, "K": 14}


def playing_card_unicode(suit_letter, rank):
    return chr(_SUIT_BASE.get(str(suit_letter).upper(), 0x1F0A0) + _RANK_OFF.get(str(rank), 1))

# Триграми І-Цзин: (нижня, середня, верхня лінія: 0=інь, 1=ян) → (символ, назва укр)
TRIGRAMS = {
    (1, 1, 1): ("☰", "Небо"),
    (0, 0, 0): ("☷", "Земля"),
    (1, 0, 1): ("☲", "Вогонь"),
    (0, 1, 0): ("☵", "Вода"),
    (1, 1, 0): ("☱", "Озеро"),
    (0, 0, 1): ("☶", "Гора"),
    (1, 0, 0): ("☳", "Грім"),
    (0, 1, 1): ("☴", "Вітер"),
}

THEMES = {
    "Таро Уэйта-Смит": ("#f5edd8", "#2a2350", "#8a6b25"),
    "default": ("#10173a", "#e8c87a", "#d4a94e"),
    "light": ("#f5edd8", "#2a2350", "#8a6b25"),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def base_card(bg, fg, frame, top=None):
    if top is not None:  # вертикальний градієнт top→bg (через resize — швидко)
        strip = Image.new("RGB", (1, H))
        spx = strip.load()
        c0 = ImageColor.getrgb(top)
        c1 = ImageColor.getrgb(bg)
        for y in range(H):
            k = y / H
            spx[0, y] = tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3))
        img = strip.resize((W, H))
    else:
        img = Image.new("RGB", (W, H), bg)
    g = ImageDraw.Draw(img)
    g.rectangle([14, 14, W - 14, H - 14], outline=frame, width=6)
    g.rectangle([30, 30, W - 30, H - 30], outline=frame, width=2)
    # кутові ромби-орнаменти
    for (x, y) in ((14, 14), (W - 14, 14), (14, H - 14), (W - 14, H - 14)):
        g.polygon([(x, y - 12), (x + 12, y), (x, y + 12), (x - 12, y)], fill=frame)
    cx0 = W / 2
    g.polygon([(cx0, 40), (cx0 + 10, 52), (cx0, 64), (cx0 - 10, 52)], fill=frame)
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
    """frac: 0=молодик..1=повня. Світло праворуч від термінатора; фон не чіпаємо."""
    import math
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    if frac <= 0:
        return
    pad = 6
    box = (int(cx - r - pad), int(cy - r - pad), int(cx + r + pad), int(cy + r + pad))
    rgb = ImageColor.getrgb(color)
    layer = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([pad, pad, layer.width - pad, layer.height - pad], fill=rgb + (255,))
    tx = pad + r + r * math.cos(math.pi * min(max(frac, 0.0), 1.0))
    d.rectangle([0, 0, int(tx), layer.height], fill=(0, 0, 0, 0))
    img.paste(layer, box, layer)


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


def star_points(cx, cy, r1, r2, n=5, rot=-90):
    import math
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_house_wheel(g, cx, cy, active, color, dim):
    """12-секторне колесо домів; активний дім світиться золотом."""
    import math
    R, Ri = 150, 96
    for i in range(12):
        a0 = math.radians(-90 + i * 30)
        a1 = math.radians(-90 + (i + 1) * 30)
        def pt(r, a):
            return (cx + r * math.cos(a), cy + r * math.sin(a))
        poly = [pt(R, a0), pt(Ri, a0), pt(Ri, a1), pt(R, a1)]
        if i == active % 12:
            g.polygon(poly, outline=color, fill=shade("#c9a24a", 0.25),
                      width=4)
            g.text(pt((R + Ri) / 2, (a0 + a1) / 2), str(i + 1),
                   font=font(ARIAL, 26), fill="#10173a", anchor="mm")
        else:
            g.polygon(poly, outline=dim, width=2)
            g.text(pt((R + Ri) / 2, (a0 + a1) / 2), str(((i) % 12) + 1),
                   font=font(ARIAL, 22), fill=dim, anchor="mm")
    g.ellipse([cx - Ri, cy - Ri, cx + Ri, cy + Ri], outline=dim, width=2)
    g.text((cx, cy), str(active + 1), font=font(ARIAL, 40), fill=color, anchor="mm")


def draw_asteroid(g, cx, cy, color, dim):
    """Астероїд: зоряна іскра + еліптична орбіта в трьох планах."""
    g.ellipse([cx - 128, cy - 66, cx + 128, cy + 66], outline=dim, width=3)
    g.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], outline=color, width=6)
    g.text((cx, cy), "✦", font=font(SYM, 72), fill=color, anchor="mm")


def draw_eclipse(g, cx, cy, color, dim):
    """Затемнення: сонце-диск, що перекривається місяцем (гліф-силует)."""
    g.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], outline=color, width=6)
    # місячний диск із тінню, зсунутий направо — сонце за ним
    g.ellipse([cx + 42, cy - 96, cx + 118, cy - 18], outline=dim, width=5)
    g.ellipse([cx + 26, cy - 66, cx + 96, cy + 14], fill=(0, 0, 0, 0),
              outline="#f0d080", width=3)
    g.text((cx, cy), "☀", font=font(SYM, 96), fill=color, anchor="mm")


def draw_maslow_pyramid(g, cx, cy, active, color, dim):
    """Піраміда Маслоу: 5 сходинок, активний рівень світиться кольором."""
    import math
    levels = 5
    top_w, bot_w = 148, 396
    step_h = 44
    total_h = levels * step_h
    top_y = cy - total_h / 2
    for i in range(levels):
        frac = i / (levels - 1)
        w_i = top_w + (bot_w - top_w) * frac
        y0 = top_y + i * step_h
        y1 = top_y + (i + 1) * step_h
        w_top = w_i + (bot_w - top_w) / (levels - 1) * 0.5
        w_bot = w_i
        level_no = levels - i  # нижній = 1 (фізіологія)
        if level_no == active:
            g.polygon([(cx - w_bot, y1), (cx + w_bot, y1), (cx + w_top, y0),
                       (cx - w_top, y0)], fill=color, outline=dim, width=4)
        else:
            g.polygon([(cx - w_bot, y1), (cx + w_bot, y1), (cx + w_top, y0),
                       (cx - w_top, y0)], fill=shade(color, -0.55), outline=dim, width=2)


def lenormand_icon(g, num, cx, cy, col):
    """Контурні іконки 36 карт Ленорман (золото на синьому)."""
    s = 90
    n = str(num)
    if n == "1":  # Вершник — стріла
        g.line([cx - s, cy + 40, cx + s - 20, cy + 40], fill=col, width=10)
        g.polygon([(cx + s - 20, cy + 10), (cx + s + 20, cy + 40), (cx + s - 20, cy + 70)], fill=col)
        g.line([cx - s, cy + 40, cx - s + 40, cy - 20], fill=col, width=10)
    elif n == "2":  # Конюшина
        for dx, dy in ((0, -38), (-36, 22), (36, 22)):
            g.ellipse([cx + dx - 30, cy + dy - 30, cx + dx + 30, cy + dy + 30], outline=col, width=9)
        g.line([cx, cy + 40, cx, cy + 95], fill=col, width=9)
    elif n == "3":  # Корабель
        g.polygon([(cx - 95, cy + 30), (cx + 95, cy + 30), (cx + 60, cy + 85), (cx - 60, cy + 85)], outline=col, width=9)
        g.line([cx, cy + 30, cx, cy - 95], fill=col, width=9)
        g.polygon([(cx, cy - 95), (cx, cy - 10), (cx + 70, cy - 10)], outline=col, width=8)
        g.polygon([(cx, cy - 80), (cx, cy - 10), (cx - 60, cy - 10)], outline=col, width=8)
        for wx in (-70, -20, 30, 80):
            g.line([cx + wx - 22, cy + 110, cx + wx + 22, cy + 110], fill=col, width=6)
    elif n == "4":  # Дім
        g.rectangle([cx - 70, cy - 20, cx + 70, cy + 90], outline=col, width=9)
        g.polygon([(cx - 90, cy - 20), (cx, cy - 95), (cx + 90, cy - 20)], outline=col, width=9)
        g.rectangle([cx - 20, cy + 25, cx + 20, cy + 90], outline=col, width=7)
    elif n == "5":  # Дерево
        g.polygon([(cx, cy - 100), (cx - 65, cy + 10), (cx + 65, cy + 10)], outline=col, width=9)
        g.polygon([(cx, cy - 45), (cx - 80, cy + 60), (cx + 80, cy + 60)], outline=col, width=9)
        g.line([cx, cy + 60, cx, cy + 100], fill=col, width=12)
    elif n == "6":  # Хмари
        for ex, ey, er in ((cx - 55, cy + 10, 48), (cx + 5, cy - 20, 58), (cx + 65, cy + 15, 42)):
            g.ellipse([ex - er, ey - er, ex + er, ey + er], outline=col, width=9)
        g.line([cx - 100, cy + 62, cx + 100, cy + 62], fill=col, width=9)
    elif n == "7":  # Змія
        pts = [(cx - 95 + i * 12, cy + 55 * (-1) ** 0 + 0) for i in range(17)]
        import math as _m
        pts = [(cx - 95 + i * 12, cy + 45 * _m.sin(i * 0.85)) for i in range(17)]
        g.line(pts, fill=col, width=11, joint="curve")
        g.polygon([(cx + 95, cy - 45), (cx + 125, cy - 10), (cx + 95, cy + 5)], fill=col)
    elif n == "8":  # Труна
        g.polygon([(cx - 45, cy - 90), (cx + 45, cy - 90), (cx + 75, cy - 20),
                   (cx + 75, cy + 90), (cx - 75, cy + 90), (cx - 75, cy - 20)], outline=col, width=10)
    elif n == "9":  # Букет
        for dx, dy in ((0, -45), (-42, -5), (42, -5), (-22, 40), (22, 40)):
            g.ellipse([cx + dx - 22, cy + dy - 22, cx + dx + 22, cy + dy + 22], outline=col, width=8)
        g.line([cx, cy + 55, cx, cy + 100], fill=col, width=9)
    elif n == "10":  # Коса
        g.line([cx + 60, cy - 95, cx - 60, cy + 95], fill=col, width=10)
        g.arc([cx - 110, cy - 90, cx + 60, cy + 80], start=200, end=350, fill=col, width=10)
    elif n == "11":  # Мітла/різки
        g.line([cx - 45, cy - 95, cx + 45, cy + 60], fill=col, width=9)
        g.line([cx + 45, cy - 95, cx - 45, cy + 60], fill=col, width=9)
        for dx in (-30, 0, 30):
            g.line([cx + dx - 14, cy + 60, cx + dx - 14, cy + 100], fill=col, width=7)
    elif n == "12":  # Птахи
        for dx in (-55, 55):
            g.arc([cx + dx - 45, cy - 25, cx + dx + 45, cy + 65], start=200, end=340, fill=col, width=10)
    elif n == "13":  # Дитина — кулька
        g.ellipse([cx - 45, cy - 85, cx + 45, cy + 5], outline=col, width=9)
        g.line([cx, cy + 5, cx + 25, cy + 95], fill=col, width=7)
    elif n == "14":  # Лис — морда
        g.polygon([(cx, cy + 80), (cx - 70, cy - 10), (cx + 70, cy - 10)], outline=col, width=9)
        g.polygon([(cx - 70, cy - 10), (cx - 50, cy - 80), (cx - 15, cy - 25)], fill=col)
        g.polygon([(cx + 70, cy - 10), (cx + 50, cy - 80), (cx + 15, cy - 25)], fill=col)
    elif n == "15":  # Ведмідь — голова
        g.ellipse([cx - 60, cy - 50, cx + 60, cy + 80], outline=col, width=10)
        g.ellipse([cx - 85, cy - 85, cx - 35, cy - 35], outline=col, width=8)
        g.ellipse([cx + 35, cy - 85, cx + 85, cy - 35], outline=col, width=8)
        g.ellipse([cx - 25, cy + 15, cx + 25, cy + 55], outline=col, width=7)
    elif n == "16":  # Зорі
        g.polygon(star_points(cx, cy - 30, 70, 28), outline=col, width=8)
        g.polygon(star_points(cx - 70, cy + 55, 30, 12), outline=col, width=6)
        g.polygon(star_points(cx + 70, cy + 55, 30, 12), outline=col, width=6)
    elif n == "17":  # Лелека
        g.ellipse([cx - 60, cy - 30, cx + 60, cy + 30], outline=col, width=9)
        g.polygon([(cx + 60, cy - 10), (cx + 110, cy - 25), (cx + 60, cy + 5)], fill=col)
        g.line([cx - 20, cy + 30, cx - 20, cy + 100], fill=col, width=8)
        g.line([cx + 20, cy + 30, cx + 20, cy + 100], fill=col, width=8)
    elif n == "18":  # Собака — кістка
        for ex in (cx - 70, cx + 70):
            g.ellipse([ex - 28, cy - 45, ex + 28, cy - 5], fill=col)
            g.ellipse([ex - 28, cy + 5, ex + 28, cy + 45], fill=col)
        g.rectangle([cx - 70, cy - 18, cx + 70, cy + 18], fill=col)
    elif n == "19":  # Вежа
        g.rectangle([cx - 45, cy - 60, cx + 45, cy + 95], outline=col, width=10)
        for dx in (-30, 0, 30):
            g.rectangle([cx + dx - 12, cy - 95, cx + dx + 12, cy - 60], outline=col, width=7)
        g.rectangle([cx - 16, cy + 35, cx + 16, cy + 95], outline=col, width=7)
    elif n == "20":  # Сад — паркан
        for dx in (-80, -40, 0, 40, 80):
            g.line([cx + dx, cy - 60, cx + dx, cy + 80], fill=col, width=9)
        g.line([cx - 100, cy - 25, cx + 100, cy - 25], fill=col, width=8)
        g.line([cx - 100, cy + 35, cx + 100, cy + 35], fill=col, width=8)
    elif n == "21":  # Гора
        g.polygon([(cx - 100, cy + 90), (cx - 35, cy - 60), (cx + 30, cy + 90)], outline=col, width=10)
        g.polygon([(cx - 30, cy + 90), (cx + 40, cy - 20), (cx + 105, cy + 90)], outline=col, width=10)
    elif n == "22":  # Роздоріжжя
        g.line([cx, cy + 95, cx, cy], fill=col, width=11)
        g.line([cx, cy, cx - 75, cy - 70], fill=col, width=11)
        g.line([cx, cy, cx + 75, cy - 70], fill=col, width=11)
    elif n == "23":  # Щури — крапля/силует
        g.ellipse([cx - 45, cy - 10, cx + 45, cy + 70], outline=col, width=9)
        g.arc([cx + 20, cy - 80, cx + 110, cy + 10], start=270, end=90, fill=col, width=8)
        g.ellipse([cx - 12, cy + 10, cx + 12, cy + 34], fill=col)
    elif n == "24":  # Серце
        g.polygon(star_points(cx, cy + 10, 75, 75, n=2, rot=-90), fill=col)
        g.ellipse([cx - 62, cy - 55, cx - 2, cy + 5], fill=col)
        g.ellipse([cx + 2, cy - 55, cx + 62, cy + 5], fill=col)
        g.polygon([(cx - 58, cy - 10), (cx + 58, cy - 10), (cx, cy + 85)], fill=col)
    elif n == "25":  # Каблучка
        g.ellipse([cx - 65, cy - 65, cx + 65, cy + 65], outline=col, width=16)
        g.polygon(star_points(cx, cy - 95, 26, 11), fill=col)
    elif n == "26":  # Книга
        g.polygon([(cx - 80, cy - 60), (cx, cy - 40), (cx, cy + 60), (cx - 80, cy + 40)], outline=col, width=9)
        g.polygon([(cx + 80, cy - 60), (cx, cy - 40), (cx, cy + 60), (cx + 80, cy + 40)], outline=col, width=9)
    elif n == "27":  # Лист
        g.rectangle([cx - 80, cy - 55, cx + 80, cy + 65], outline=col, width=9)
        g.line([cx - 80, cy - 55, cx, cy + 15], fill=col, width=8)
        g.line([cx + 80, cy - 55, cx, cy + 15], fill=col, width=8)
    elif n == "28":  # Чоловік ♂
        g.ellipse([cx - 45, cy - 30, cx + 45, cy + 60], outline=col, width=11)
        g.line([cx + 32, cy - 17, cx + 85, cy - 70], fill=col, width=11)
        g.line([cx + 85, cy - 70, cx + 45, cy - 70], fill=col, width=9)
        g.line([cx + 85, cy - 70, cx + 85, cy - 30], fill=col, width=9)
    elif n == "29":  # Жінка ♀
        g.ellipse([cx - 45, cy - 80, cx + 45, cy + 10], outline=col, width=11)
        g.line([cx, cy + 10, cx, cy + 95], fill=col, width=11)
        g.line([cx - 35, cy + 60, cx + 35, cy + 60], fill=col, width=9)
    elif n == "30":  # Лілії
        for dx, ang in ((0, 0), (-45, -25), (45, 25)):
            g.ellipse([cx + dx - 20, cy - 80, cx + dx + 20, cy + 20], outline=col, width=8)
        g.line([cx, cy + 20, cx, cy + 95], fill=col, width=9)
    elif n == "31":  # Сонце
        g.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], outline=col, width=11)
        import math as _m
        for i in range(8):
            a = _m.radians(i * 45)
            g.line([cx + 60 * _m.cos(a), cy + 60 * _m.sin(a),
                    cx + 90 * _m.cos(a), cy + 90 * _m.sin(a)], fill=col, width=8)
    elif n == "32":  # Місяць — півмісяць
        g.arc([cx - 60, cy - 80, cx + 60, cy + 80], start=70, end=290, fill=col, width=13)
        g.polygon(star_points(cx + 45, cy - 45, 20, 8), fill=col)
    elif n == "33":  # Ключ
        g.ellipse([cx - 40, cy - 90, cx + 40, cy - 10], outline=col, width=11)
        g.line([cx, cy - 10, cx, cy + 90], fill=col, width=11)
        g.line([cx, cy + 55, cx + 35, cy + 55], fill=col, width=9)
        g.line([cx, cy + 90, cx + 35, cy + 90], fill=col, width=9)
    elif n == "34":  # Риби
        g.ellipse([cx - 70, cy - 30, cx + 10, cy + 30], outline=col, width=9)
        g.polygon([(cx + 10, cy - 30), (cx + 70, cy), (cx + 10, cy + 30)], outline=col, width=9)
        g.ellipse([cx - 50, cy - 12, cx - 38, cy + 0], fill=col)
    elif n == "35":  # Якір
        g.ellipse([cx - 18, cy - 95, cx + 18, cy - 59], outline=col, width=9)
        g.line([cx, cy - 59, cx, cy + 60], fill=col, width=11)
        g.line([cx - 55, cy - 30, cx + 55, cy - 30], fill=col, width=9)
        g.arc([cx - 70, cy - 10, cx + 70, cy + 110], start=20, end=160, fill=col, width=11)
    elif n == "36":  # Хрест
        g.rectangle([cx - 20, cy - 95, cx + 20, cy + 95], fill=col)
        g.rectangle([cx - 65, cy - 40, cx + 65, cy + 0], fill=col)
    else:
        g.text((cx, cy), "✦", font=font(SYM, 120), fill=col, anchor="mm")


def shaman_icon(g, num, cx, cy, col):
    """12 різних тотемів: кожному своя контурна іконка."""
    n = str(num)
    if n == "1":  # Вовк — голова
        g.polygon([(cx, cy + 70), (cx - 60, cy - 20), (cx + 60, cy - 20)], outline=col, width=10)
        g.polygon([(cx - 60, cy - 20), (cx - 48, cy - 85), (cx - 12, cy - 30)], fill=col)
        g.polygon([(cx + 60, cy - 20), (cx + 48, cy - 85), (cx + 12, cy - 30)], fill=col)
        g.line([cx, cy + 70, cx, cy + 30], fill=col, width=8)
    elif n == "2":  # Ведмідь — голова з вухами
        g.ellipse([cx - 60, cy - 50, cx + 60, cy + 80], outline=col, width=10)
        g.ellipse([cx - 85, cy - 85, cx - 35, cy - 35], outline=col, width=8)
        g.ellipse([cx + 35, cy - 85, cx + 85, cy - 35], outline=col, width=8)
        g.ellipse([cx - 25, cy + 15, cx + 25, cy + 55], outline=col, width=7)
    elif n == "3":  # Орел — крила
        g.line([cx, cy + 80, cx, cy - 40], fill=col, width=11)
        g.arc([cx - 150, cy - 60, cx - 10, cy + 80], start=270, end=90, fill=col, width=11)
        g.arc([cx + 10, cy - 60, cx + 150, cy + 80], start=90, end=270, fill=col, width=11)
    elif n == "4":  # Крук — дзьоб
        g.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], outline=col, width=10)
        g.polygon([(cx + 40, cy - 15), (cx + 105, cy + 10), (cx + 40, cy + 30)], fill=col)
        g.ellipse([cx - 8, cy - 20, cx + 8, cy - 4], fill=col)
    elif n == "5":  # Сова — очі
        g.ellipse([cx - 80, cy - 60, cx - 5, cy + 15], outline=col, width=10)
        g.ellipse([cx + 5, cy - 60, cx + 80, cy + 15], outline=col, width=10)
        g.ellipse([cx - 48, cy - 28, cx - 28, cy - 8], fill=col)
        g.ellipse([cx + 28, cy - 28, cx + 48, cy - 8], fill=col)
        g.polygon([(cx - 12, cy + 25), (cx + 12, cy + 25), (cx, cy + 50)], fill=col)
    elif n == "6":  # Змія — хвиля
        import math as _m
        pts = [(cx - 90 + i * 12, cy + 50 * _m.sin(i * 0.7)) for i in range(16)]
        g.line(pts, fill=col, width=12, joint="curve")
        g.polygon([(cx + 90, cy - 40), (cx + 118, cy - 8), (cx + 90, cy + 8)], fill=col)
    elif n == "7":  # Олень — роги
        g.line([cx, cy + 90, cx, cy], fill=col, width=11)
        for sgn in (-1, 1):
            g.line([cx, cy + 20, cx + sgn * 55, cy - 40], fill=col, width=9)
            g.line([cx + sgn * 30, cy - 12, cx + sgn * 30, cy - 75], fill=col, width=8)
            g.line([cx + sgn * 55, cy - 40, cx + sgn * 85, cy - 60], fill=col, width=8)
    elif n == "8":  # Лисиця — гостра морда
        g.polygon([(cx, cy + 85), (cx - 45, cy - 30), (cx + 45, cy - 30)], outline=col, width=10)
        g.polygon([(cx - 45, cy - 30), (cx - 60, cy - 90), (cx - 5, cy - 45)], fill=col)
        g.polygon([(cx + 45, cy - 30), (cx + 60, cy - 90), (cx + 5, cy - 45)], fill=col)
    elif n == "9":  # Кінь — голова
        g.polygon([(cx - 25, cy - 90), (cx + 35, cy - 70), (cx + 55, cy + 20),
                   (cx + 20, cy + 90), (cx - 35, cy + 60)], outline=col, width=10)
        for i, dx in enumerate((-45, -60, -72)):
            g.line([cx - 25 + dx * 0, cy - 60 + i * 30, cx - 25 + dx, cy - 40 + i * 30], fill=col, width=7)
    elif n == "10":  # Черепаха — купол
        g.arc([cx - 90, cy - 40, cx + 90, cy + 120], start=180, end=360, fill=col, width=11)
        g.line([cx - 90, cy + 40, cx + 90, cy + 40], fill=col, width=9)
        for dx in (-110, -70, 70, 110):
            g.line([cx + dx, cy + 30, cx + dx + (12 if dx > 0 else -12), cy + 75], fill=col, width=8)
        g.ellipse([cx + 95, cy + 10, cx + 125, cy + 40], outline=col, width=7)
    elif n == "11":  # Лосось — риба вгору
        g.ellipse([cx - 40, cy - 90, cx + 40, cy - 10], outline=col, width=10)
        g.polygon([(cx - 40, cy - 80), (cx - 40, cy - 20), (cx - 85, cy - 50)], outline=col, width=9)
        g.line([cx, cy - 10, cx, cy + 90], fill=col, width=8)
        for i in range(3):
            g.line([cx - 30, cy + 10 + i * 25, cx + 30, cy + 25 + i * 25], fill=col, width=6)
    elif n == "12":  # Павук
        g.ellipse([cx - 35, cy - 20, cx + 35, cy + 50], fill=col)
        g.ellipse([cx - 20, cy - 65, cx + 20, cy - 25], fill=col)
        for sgn in (-1, 1):
            for i, (dy, ln) in enumerate((( -20, 70), (5, 85), (30, 80), (50, 65))):
                g.line([cx + sgn * 30, cy + dy, cx + sgn * (30 + ln), cy + dy - 25 + i * 12], fill=col, width=7)
    else:
        g.text((cx, cy), "✦", font=font(SYM, 120), fill=col, anchor="mm")


def ancestor_icon(g, num, cx, cy, col):
    """12 родинних символів."""
    n = str(num)
    if n == "1":  # Мати — серце
        g.ellipse([cx - 55, cy - 50, cx - 5, cy + 0], fill=col)
        g.ellipse([cx + 5, cy - 50, cx + 55, cy + 0], fill=col)
        g.polygon([(cx - 52, cy - 5), (cx + 52, cy - 5), (cx, cy + 75)], fill=col)
    elif n == "2":  # Батько — колона
        g.rectangle([cx - 30, cy - 80, cx + 30, cy + 80], outline=col, width=11)
        g.line([cx - 50, cy - 80, cx + 50, cy - 80], fill=col, width=11)
        g.line([cx - 50, cy + 80, cx + 50, cy + 80], fill=col, width=11)
    elif n == "3":  # Бабуся — хустка
        g.polygon([(cx, cy - 85), (cx - 75, cy + 40), (cx + 75, cy + 40)], outline=col, width=10)
        g.ellipse([cx - 22, cy - 30, cx + 22, cy + 14], outline=col, width=8)
    elif n == "4":  # Дідусь — капелюх і борода
        g.line([cx - 80, cy - 20, cx + 80, cy - 20], fill=col, width=10)
        g.arc([cx - 45, cy - 75, cx + 45, cy + 15], start=180, end=360, fill=col, width=10)
        g.polygon([(cx - 40, cy + 10), (cx + 40, cy + 10), (cx, cy + 90)], outline=col, width=8)
    elif n == "5":  # Дитина — кулька
        g.ellipse([cx - 45, cy - 85, cx + 45, cy + 5], outline=col, width=10)
        g.line([cx, cy + 5, cx + 25, cy + 95], fill=col, width=7)
    elif n == "6":  # Рід — дерево
        g.line([cx, cy + 20, cx, cy + 95], fill=col, width=12)
        g.ellipse([cx - 65, cy - 85, cx + 65, cy + 35], outline=col, width=10)
    elif n == "7":  # Дім
        g.rectangle([cx - 65, cy - 10, cx + 65, cy + 90], outline=col, width=10)
        g.polygon([(cx - 85, cy - 10), (cx, cy - 85), (cx + 85, cy - 10)], outline=col, width=10)
    elif n == "8":  # Спадок — скриня
        g.rectangle([cx - 80, cy - 10, cx + 80, cy + 80], outline=col, width=10)
        g.arc([cx - 80, cy - 70, cx + 80, cy + 40], start=180, end=360, fill=col, width=10)
        g.ellipse([cx - 12, cy + 15, cx + 12, cy + 39], outline=col, width=7)
    elif n == "9":  # Коріння
        g.line([cx, cy - 90, cx, cy + 10], fill=col, width=11)
        for dx, ln in ((-55, 70), (-25, 90), (25, 90), (55, 70)):
            g.line([cx, cy + 10, cx + dx, cy + 10 + ln], fill=col, width=8)
    elif n == "10":  # Крила
        g.arc([cx - 130, cy - 40, cx - 10, cy + 80], start=270, end=90, fill=col, width=11)
        g.arc([cx + 10, cy - 40, cx + 130, cy + 80], start=90, end=270, fill=col, width=11)
    elif n == "11":  # Прощення — дві дуги назустріч
        g.arc([cx - 110, cy - 60, cx - 10, cy + 80], start=270, end=90, fill=col, width=10)
        g.arc([cx + 10, cy - 60, cx + 110, cy + 80], start=90, end=270, fill=col, width=10)
    elif n == "12":  # Коло — вінок
        g.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], outline=col, width=14)
        g.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], outline=col, width=5)
    else:
        g.text((cx, cy), "✦", font=font(SYM, 120), fill=col, anchor="mm")


# ── Нові навчальні колоди (з відкритих джерел, своя графіка) ─────────
# Огам: літера → (сім'я рисок, кількість). R=праворуч, L=ліворуч, C=навхрест, V=голосні-засічки.
OGHAM_GLYPH = {
    "B": ("R", 1), "L": ("R", 2), "F": ("R", 3), "S": ("R", 4), "N": ("R", 5),
    "H": ("L", 1), "D": ("L", 2), "T": ("L", 3), "C": ("L", 4), "Q": ("L", 5),
    "M": ("C", 1), "G": ("C", 2), "NG": ("C", 3), "Z": ("C", 4), "R": ("C", 5),
    "A": ("V", 1), "O": ("V", 2), "U": ("V", 3), "E": ("V", 4), "I": ("V", 5),
}
SIGN_CODE_INDEX = {"ari": 0, "tau": 1, "gem": 2, "can": 3, "leo": 4, "vir": 5,
                   "lib": 6, "sco": 7, "sag": 8, "cap": 9, "aqu": 10, "pis": 11}
CHAKRA_COLORS = {"red": "#c92a1e", "orange": "#e87a20", "yellow": "#e0b32a",
                 "green": "#2f9e63", "blue": "#2f7fc9", "indigo": "#3b3fa0",
                 "violet": "#7a4fa8", "white": "#e8e6f0"}
CRYSTAL_COLORS = {"amethyst": "#8a4ba8", "rose": "#e8849c", "citrine": "#e0b32a",
                  "clear": "#e8e6f0", "tourmaline": "#2f3542", "selenite": "#e8e0ce",
                  "carnelian": "#d6453d", "jade": "#2f9e63", "lapis": "#2f5d8a",
                  "labradorite": "#4a6f9e", "fluorite": "#5fbfa9", "tiger": "#c9962e",
                  "moonstone": "#b8c4d8", "malachite": "#1f8a62", "obsidian": "#23232d",
                  "aventurine": "#3f9e5f"}

# Об'єднана терапевтична колода: кольори блоків VIA / BASIC Ph / Маслоу
THERAPEUTIC_COLORS = {
    # VIA — 6 доброчесностей
    "wisdom": "#c9962e", "courage": "#b04e3d", "humanity": "#c96a8b",
    "justice": "#4f8a5f", "temperance": "#4f7fb0", "transcendence": "#8a6fd0",
    # BASIC Ph — 6 каналів
    "belief": "#c9962e", "affect": "#d64a4a", "social": "#4f8a5f",
    "imagination": "#9a6fd0", "cognition": "#3fa8c9", "physiology": "#b0782f",
    # Маслоу — 5 рівнів
    "physiological": "#b04e3d", "safety": "#c9882e", "belonging": "#4f8a5f",
    "esteem": "#4f7fb0", "selfactualization": "#8a6fd0",
}


def shade(hexc, f):
    """f >= 0 — світліше (до білого), f < 0 — темніше."""
    r, g, b = ImageColor.getrgb(hexc)
    if f >= 0:
        return tuple(int(c + (255 - c) * f) for c in (r, g, b))
    return tuple(int(c * (1 + f)) for c in (r, g, b))


def wrap_lines(g, text, fnt, max_w, limit=6):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if g.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:limit]


def draw_ogham(g, letter, cx, top, bot, col, w=10):
    g.line([cx, top, cx, bot], fill=col, width=w + 2)
    fam, cnt = OGHAM_GLYPH.get(letter, ("R", 1))
    if not fam:
        return
    step = (bot - top) / (cnt + 1)
    for i in range(1, cnt + 1):
        y = top + i * step
        if fam == "R":
            g.line([cx, y, cx + 108, y], fill=col, width=w)
        elif fam == "L":
            g.line([cx - 108, y, cx, y], fill=col, width=w)
        elif fam == "C":
            g.line([cx - 108, y, cx + 108, y], fill=col, width=w)
        else:
            g.line([cx - 58, y + 22, cx + 58, y - 22], fill=col, width=w)


def emotion_face(g, cx, cy, r, key, col, dark):
    """Схематичне обличчя-смайл за емоцією Плутчика (своя графіка)."""
    g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=shade(col, 0.82),
              outline=dark, width=8)
    k = str(key).lower()
    exd, eye_r, ey = r * 0.34, max(4, int(r * 0.06)), cy - r * 0.15

    def brow(s, tilt):
        x1, x2 = cx + s * exd - r * 0.18, cx + s * exd + r * 0.18
        y1 = ey - r * 0.44 - tilt * s * r * 0.16
        y2 = ey - r * 0.34 + tilt * s * r * 0.16
        g.line([x1, y1, x2, y2], fill=dark, width=8)

    bw = {"гнів": -1, "страх": 1, "здивування": 1, "очікування": 0.7,
          "відраза": 0.7}.get(k, 0)
    for s in (-1, 1):
        if bw:
            brow(s, bw)
    if "страх" in k or "здив" in k:
        for s in (-1, 1):
            ex = cx + s * exd
            er = r * 0.10
            g.ellipse([ex - er, ey - er, ex + er, ey + er], fill=dark)
    else:
        g.ellipse([cx - exd - eye_r, ey - eye_r, cx - exd + eye_r, ey + eye_r], fill=dark)
        g.ellipse([cx + exd - eye_r, ey - eye_r, cx + exd + eye_r, ey + eye_r], fill=dark)
    my, mw = cy + r * 0.24, r * 0.42
    if "радість" in k or "довіра" in k:
        g.arc([cx - mw, my - mw * 0.5, cx + mw, my + mw * 0.9], 0, 180, fill=dark, width=8)
    elif "сум" in k:
        g.arc([cx - mw, my - mw * 0.9, cx + mw, my + mw * 0.5], 180, 360, fill=dark, width=8)
    elif "відраза" in k:
        g.line([cx - mw * 0.6, my + mw * 0.2, cx + mw * 0.6, my + mw * 0.2], fill=dark, width=8)
    elif "здив" in k:
        g.ellipse([cx - mw * 0.36, my, cx + mw * 0.36, my + mw * 0.6], fill=dark)
    elif "гнів" in k:
        g.line([cx - mw, my, cx + mw, my], fill=dark, width=8)
        g.line([cx - mw, my, cx - mw, my + mw * 0.4], fill=dark, width=8)
        g.line([cx + mw, my, cx + mw, my + mw * 0.4], fill=dark, width=8)
        g.line([cx - mw, my + mw * 0.4, cx + mw, my + mw * 0.4], fill=dark, width=8)
    elif "очікув" in k:
        g.arc([cx - mw, my - mw * 0.3, cx + mw, my + mw * 0.5], 15, 165, fill=dark, width=7)
    else:  # страх — хвилястий рот
        pts = [(cx - mw + i * 2 * mw / 5, my + (7 if i % 2 else -7)) for i in range(6)]
        g.line(pts, fill=dark, width=7, joint="curve")


def chakra_lotus(g, cx, cy, dark, main, n=8):
    import math as _m
    g.ellipse([cx - 208, cy - 208, cx + 208, cy + 208], outline=main, width=3)
    g.ellipse([cx - 176, cy - 176, cx + 176, cy + 176], outline=dark, width=2)
    for i in range(n):
        a = _m.radians(i * 360 / n + 22.5)
        px, py = cx + 188 * _m.cos(a), cy + 188 * _m.sin(a)
        g.ellipse([px - 40, py - 40, px + 40, py + 40], outline=main, width=5)
    g.ellipse([cx - 106, cy - 106, cx + 106, cy + 106], outline=main, width=4)
    for i in range(n * 2):
        a = _m.radians(i * 360 / (n * 2))
        px, py = cx + 106 * _m.cos(a), cy + 106 * _m.sin(a)
        g.line([px, py, cx + 76 * _m.cos(a), cy + 76 * _m.sin(a)], fill=main, width=3)
    g.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], fill=shade(main, 0.15),
              outline=main, width=4)
    g.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=main)


def zodiak_coin(g, cx, cy, idx, col, dark):
    import math as _m
    g.ellipse([cx - 175, cy - 175, cx + 175, cy + 175], outline=col, width=4)
    g.ellipse([cx - 156, cy - 156, cx + 156, cy + 156], outline=dark, width=2)
    for i in range(12):
        a = _m.radians(i * 30 - 90)
        r1, r2 = (205, 222) if i == idx else (185, 222)
        g.line([cx + r1 * _m.cos(a), cy + r1 * _m.sin(a),
                cx + r2 * _m.cos(a), cy + r2 * _m.sin(a)],
               fill=col if i == idx else dark, width=8 if i == idx else 5)
    g.rectangle([cx - 78, cy - 78, cx + 78, cy + 78], outline=col, width=5)
    g.rectangle([cx - 62, cy - 62, cx + 62, cy + 62], outline=dark, width=2)


# ── Помічники нових систем ─────────────────────────────────────────────

BAGUA_LINES = {  # 乾☰ 兑☱ 離☲ 震☳ 巽☴ 坎☵ 艮☶ 坤☷ (нижня, середня, верхня)
    "☰": (1, 1, 1), "☱": (1, 1, 0), "☲": (1, 0, 1), "☳": (1, 0, 0),
    "☴": (0, 1, 1), "☵": (0, 1, 0), "☶": (0, 0, 1), "☷": (0, 0, 0)}


def draw_trigram(g, cx, cy, gly, color):
    """Три риси триграми (суцільна=ян)."""
    lines = BAGUA_LINES.get(gly, (1, 1, 1))
    for i, yang in enumerate(lines):
        y = cy - 80 + i * 62
        if yang:
            g.rectangle([cx - 112, y - 13, cx + 112, y + 13], fill=color)
        else:
            g.rectangle([cx - 112, y - 13, cx - 18, y + 13], fill=color)
            g.rectangle([cx + 18, y - 13, cx + 112, y + 13], fill=color)


def draw_gem(g, cx, cy, s, color, light):
    """Гранований самоцвіт (один камінь, кілька граней)."""
    g.polygon([(cx, cy - s), (cx + s, cy - s * 0.28), (cx + s * 0.62, cy + s),
               (cx - s * 0.62, cy + s), (cx - s, cy - s * 0.28)],
              fill=shade(color, 0.72), outline=light, width=4)
    g.polygon([(cx, cy - s), (cx + s * 0.5, cy - s * 0.42), (cx, cy - s * 0.18),
               (cx - s * 0.5, cy - s * 0.42)], fill=shade(color, 0.9),
              outline=light, width=3)


def draw_teacup(g, cx, cy, color, dark):
    """Чашка для тасеографії: блюдце, листя на дні, пара, ручка."""
    # блюдце
    g.ellipse([cx - 142, cy + 74, cx + 142, cy + 118], fill=shade(dark, 0.8))
    g.ellipse([cx - 142, cy + 74, cx + 142, cy + 118], outline=dark, width=4)
    g.ellipse([cx - 96, cy + 82, cx + 96, cy + 108], outline=shade(dark, 0.55), width=3)
    # тіло чашки (трапеція)
    g.polygon([(cx - 92, cy - 78), (cx + 84, cy - 78), (cx + 66, cy + 58),
               (cx - 74, cy + 58)], fill="#f3ecda", outline=color, width=5)
    g.polygon([(cx - 74, cy + 30), (cx + 60, cy + 30), (cx + 62, cy + 44),
               (cx - 72, cy + 44)], fill=shade(color, 0.45))
    # ручка (права)
    g.arc([cx - 66, cy - 96, cx + 96, cy + 58], 30, 150, fill=color, width=6)
    # поверхня чаю: овал-«дно»
    g.ellipse([cx - 74, cy - 30, cx + 72, cy + 26], outline=dark, width=2)
    # листя чаю на дні: крапки-штрихи
    seed_ = int(cx * 7 + cy * 13)
    random.seed(seed_)
    for _ in range(26):
        xx = cx + random.randint(-58, 56)
        yy = cy + random.randint(-22, 18)
        rr = random.uniform(2.5, 6.5)
        g.ellipse([xx - rr, yy - rr * 0.6, xx + rr, yy + rr * 0.6],
                  fill=shade(color, 0.55) if random.random() > 0.45 else color)
    # пара
    for i, dx in enumerate((0, -22, 22)):
        g.arc([cx - 66 + dx, cy - 158, cx + 46 + dx, cy - 96], 200, 340,
              fill=shade(color, 0.75), width=5)


def pip_grid(n, cx, cy, dx=70, dy=80):
    """Симетрична сітка піпок таро (до 2 стовпців, останній непарний — в центрі)."""
    rows = (n + 1) // 2
    pts, i = [], 0
    for r in range(rows):
        y = cy + (r - (rows - 1) / 2) * dy
        if n - i == 1:
            pts.append((cx, y))
            break
        pts.append((cx - dx, y))
        pts.append((cx + dx, y))
        i += 2
    return pts


def draw_tarot_orb(g, cx, cy, r, base):
    """Куля-піпка таро з обідком і сяйвом."""
    g.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=shade(base, 0.55),
              outline=shade(base, 0.35), width=2)
    g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=shade(base, 0.25),
              outline=shade(base, 0.75), width=3)
    g.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
              outline=shade(base, 0.9), width=2)


def draw_radiant(g, cx, cy, r, color, dark):
    """Сяюча зірка-ореол (архангели)."""
    import math as _m
    for i in range(16):
        a = _m.radians(i * 22.5)
        g.line([cx + (r - 30) * _m.cos(a), cy + (r - 30) * _m.sin(a),
                cx + (r + 18) * _m.cos(a), cy + (r + 18) * _m.sin(a)],
               fill=color, width=6 if i % 2 == 0 else 3)
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=6)
    g.ellipse([cx - r - 22, cy - r - 22, cx + r + 22, cy + r + 22], outline=dark, width=2)


SEPHIROT_POS = {1: (0.00, 0.06), 2: (0.66, 0.13), 3: (-0.66, 0.13),
                4: (0.60, 0.42), 5: (-0.60, 0.42), 6: (0.00, 0.50),
                7: (0.60, 0.79), 8: (-0.60, 0.79), 9: (0.00, 0.85), 10: (0.00, 1.00)}
SEPHIROT_EDGES = [(1, 2), (1, 3), (2, 3), (2, 6), (3, 6), (2, 4), (3, 5), (4, 5),
                  (4, 6), (5, 6), (6, 7), (6, 8), (7, 8), (7, 9), (8, 9), (9, 10)]

# ── 7 навчальних таро (деки 51–57): тематичні палітри ──
TAROT_THEMES = {
    "angel": {"top": "#1a1030", "bg": "#2a1b45", "fg": "#f4e9d0", "frame": "#d4b05a",
              "glow": "#e8c87a", "label": "АНГЕЛИ"},
    "neocolonial": {"top": "#3a2413", "bg": "#5a3a20", "fg": "#f2e6c8", "frame": "#c9932e",
                    "glow": "#e0a94e", "label": "НЕОКОЛОНІАЛЬНЕ"},
    "fablemaker": {"top": "#2b1540", "bg": "#3e1f5a", "fg": "#f4e8f0", "frame": "#e09ad0",
                   "glow": "#e8b0ff", "label": "БАЙКАР"},
    "alice": {"top": "#12333a", "bg": "#1c4a55", "fg": "#f2ecdf", "frame": "#d4b04f",
              "glow": "#e8cf8a", "label": "АЛІСА"},
    "visionquest": {"top": "#142018", "bg": "#1f3226", "fg": "#ede6d2", "frame": "#c9962e",
                    "glow": "#e0b44e", "label": "ВИДІННЯ"},
    "goldencat": {"top": "#14121a", "bg": "#1f1c26", "fg": "#f2e6c8", "frame": "#d4af37",
                  "glow": "#f0cd60", "label": "ЗОЛОТИЙ КІТ"},
    "folklore": {"top": "#14303a", "bg": "#1d4352", "fg": "#f5ecd8", "frame": "#c9a24a",
                 "glow": "#e0c07a", "label": "ФОЛЬКЛОР"},
}

TAROT_SUITGLYPH = {
    "wands": ("⚝", "wand"),
    "cups": ("⚶", "cup"),
    "swords": ("⚔", "sword"),
    "pentacles": ("⚲", "coin"),
}
TAROT_RANKWORD = {11: "ПАЖ", 12: "ЛИЦАР", 13: "КОРОЛЕВА", 14: "КОРОЛЬ"}


def tarot_theme(dnl):
    if "неоколоніальне" in dnl or "неоколоніальн" in dnl:
        return TAROT_THEMES["neocolonial"]
    if "байкар" in dnl or "fablemaker" in dnl:
        return TAROT_THEMES["fablemaker"]
    if "аліс" in dnl or "alice" in dnl:
        return TAROT_THEMES["alice"]
    if "видіння" in dnl or "vision" in dnl:
        return TAROT_THEMES["visionquest"]
    if "золотого чорного кота" in dnl or "golden black cat" in dnl or "золотого черного кота" in dnl:
        return TAROT_THEMES["goldencat"]
    if "фольклорн" in dnl or "folklore" in dnl:
        return TAROT_THEMES["folklore"]
    return TAROT_THEMES["angel"]


def tree_of_life(g, cx, top, bot, highlight, color, dim, path_hi=None):
    """Древо Життя: highlight — активна сфіра, path_hi=(a,b) — сяючий шлях."""
    def pos(n):
        kx, ky = SEPHIROT_POS[n]
        return cx + kx * 150, top + ky * (bot - top)
    for a, b in SEPHIROT_EDGES:
        hi = path_hi == (a, b) or path_hi == (b, a)
        g.line([pos(a), pos(b)], fill=color if hi else dim,
               width=10 if hi else 3)
    glow = None
    for n, (kx, ky) in SEPHIROT_POS.items():
        x, y = pos(n)
        if n == highlight:
            g.ellipse([x - 24, y - 24, x + 24, y + 24], fill=color, outline="#ffffff", width=3)
            g.text((x, y), str(n), font=font(ARIAL, 20), fill="#10173a", anchor="mm")
        else:
            g.ellipse([x - 20, y - 20, x + 20, y + 20], outline=dim, width=3)
            g.text((x, y), str(n), font=font(ARIAL, 16), fill=dim, anchor="mm")


def ifa_grid(g, cx, cy, binario, color, dark):
    """Дошка Іфа у стилі opele (ланцюжок opó oja).

    Перші 4 біти — права колонка, останні 4 — ліва (стандарт опритування Yorùbá:
    цикл «Eji Ogbe … Oyeku»). Біт '1' — одна активна паличка (I), '0' — дві
    порожні (II), як у класичному записі «II - II - II - II · I - II - II - I».
    """
    code = str(binario or "").strip()
    if len(code) != 8 or set(code) - {"0", "1"}:
        code = "00000000"
    # центральний стовбур ланцюжка
    g.line([cx, cy - 170, cx, cy + 150], fill=dark, width=10)
    g.line([cx, cy - 170, cx, cy + 150], fill="#8a9e4f", width=4)
    for i in range(8):
        if i < 4:
            x = cx + 105      # права колонка: біти 0..3 (зверху вниз)
            y = cy - 150 + i * 88
        else:
            x = cx - 105      # ліва колонка: біти 4..7 (зверху вниз)
            y = cy - 150 + (i - 4) * 88
        active = code[i] == "1"
        if active:
            # одна товста «паличка» I
            g.rounded_rectangle([x - 16, y - 42, x + 16, y + 42], radius=8,
                                fill=color, outline="#0f1c10", width=2)
            g.line([x - 6, y - 34, x - 6, y + 34], fill="#2b1510", width=3)
        else:
            # дві тонкі «палички» II
            g.rounded_rectangle([x - 34, y - 40, x + 34, y + 40], radius=16,
                                outline=dark, width=2)
            for dx in (-13, 13):
                g.rounded_rectangle([x + dx - 7, y - 30, x + dx + 7, y + 30],
                                    radius=5, outline="#8a9e4f", width=3)
    # обрамлення знаку опритування
    g.ellipse([cx - 235, cy - 235, cx + 235, cy + 235], outline=dark, width=3)


def draw_rune_stone(img, g, cx, cy, r, ring, glyph, glyph_color, rune_font):
    """Рунічний камінь: м'яке сяйво + диск + кільце етиру + руна.

    Конвертує img у RGBA, накладає сяйво і повертає (новий img, новий g).
    """
    img = img.convert("RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for rr in range(r + 130, 0, -4):
        a = int(34 * (1 - (rr / (r + 130)) ** 2.2))
        if a > 0:
            gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(200, 170, 80, a))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img, glow).convert("RGB")
    g = ImageDraw.Draw(img)
    # диск каменя
    g.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#1b2431",
              outline=shade(ring, 0.45), width=10)
    g.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26],
              outline=shade(ring, 0.6), width=3)
    # кільце кольору етиру
    g.ellipse([cx - r + 44, cy - r + 44, cx + r - 44, cy + r - 44],
              outline=ring, width=6)
    g.text((cx, cy + 6), glyph, font=rune_font, fill=glyph_color, anchor="mm")
    return img, g


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
        fg_rgb = (232, 200, 122)
        frame_rgb = (201, 162, 74)
        CX, CY = W // 2, 370
        HEX_TOP = 220
        HEX_SP = 60

        # ── 1. Deep indigo-black background ──
        img = Image.new("RGBA", (W, H), (10, 5, 28, 255))

        # ── 2. Multi-layer radial warm glow ──
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for r in range(230, 0, -3):
            a = int(38 * (1 - (r / 230) ** 2.5))
            if a > 0:
                gd.ellipse([CX - r, CY - r, CX + r, CY + r],
                           fill=(160, 120, 30, a))
        for r in range(110, 0, -2):
            a = int(50 * (1 - (r / 110) ** 2))
            if a > 0:
                gd.ellipse([CX - r, CY - r, CX + r, CY + r],
                           fill=(210, 170, 50, a))
        glow = glow.filter(ImageFilter.GaussianBlur(22))
        img = Image.alpha_composite(img, glow)

        # ── 3. Concentric mandala ellipses (very subtle) ──
        mand = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        md = ImageDraw.Draw(mand)
        for rx, ry in [(188, 218), (168, 196), (150, 178)]:
            md.ellipse([CX - rx, CY - ry, CX + rx, CY + ry],
                       outline=(200, 160, 50, 40), width=1)
        for dy in (-218, 218):
            md.polygon([(CX, CY + dy - 8), (CX + 8, CY + dy),
                        (CX, CY + dy + 8), (CX - 8, CY + dy)],
                       fill=(200, 160, 50, 55))
        img = Image.alpha_composite(img, mand)

        # ── 4. Hexagram line glow (shape-following, blurred) ──
        if lines:
            hgl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            hg = ImageDraw.Draw(hgl)
            for i, yang in enumerate(lines):
                y = HEX_TOP + (5 - i) * HEX_SP
                if yang:
                    hg.rectangle([CX - 138, y - 20, CX + 138, y + 20],
                                 fill=(232, 200, 122, 80))
                else:
                    hg.rectangle([CX - 138, y - 20, CX - 10, y + 20],
                                 fill=(232, 200, 122, 80))
                    hg.rectangle([CX + 10, y - 20, CX + 138, y + 20],
                                 fill=(232, 200, 122, 80))
            hgl = hgl.filter(ImageFilter.GaussianBlur(14))
            img = Image.alpha_composite(img, hgl)

        # ── 5. Convert to RGB, draw sharp hexagram ──
        img = img.convert("RGB")
        g = ImageDraw.Draw(img)
        if lines:
            for i, yang in enumerate(lines):
                y = HEX_TOP + (5 - i) * HEX_SP
                if yang:
                    g.rectangle([CX - 130, y - 13, CX + 130, y + 13],
                                fill="#e8c87a")
                else:
                    g.rectangle([CX - 130, y - 13, CX - 16, y + 13],
                                fill="#e8c87a")
                    g.rectangle([CX + 16, y - 13, CX + 130, y + 13],
                                fill="#e8c87a")
        if lines:
            bin_code = "".join("1" if x else "0" for x in lines)
            bcf = font(ARIAL, 18)
            g.text((CX, HEX_TOP + 6 * HEX_SP + 30), bin_code, font=bcf,
                   fill="#8a7440", anchor="mm")

        # ── 6. Trigrams in side margins ──
        low = tuple(int(x) for x in (lines[0], lines[1], lines[2])) if lines else None
        up = tuple(int(x) for x in (lines[3], lines[4], lines[5])) if lines else None
        for (tr, glyph), (tx, ty) in (((TRIGRAMS.get(up), "☰"), (74, CY)),
                                       ((TRIGRAMS.get(low), "☷"), (W - 74, CY))):
            tr_sym = tr[0] if tr else glyph
            tr_name = tr[1].upper() if tr else ""
            g.text((tx, ty - 6), tr_sym, font=font(SYM, 58), fill="#e8c87a",
                   anchor="mm")
            nf = font(ARIAL, 16)
            g.text((tx, ty + 38), tr_name, font=nf, fill="#c9a24a", anchor="mm")

        # ── 7. Ornate frame ──
        g.rectangle([10, 10, W - 10, H - 10], outline="#c9a24a", width=5)
        g.rectangle([22, 22, W - 22, H - 22], outline="#c9a24a", width=1)
        for fx, fy in [(10, 10), (W - 10, 10), (10, H - 10), (W - 10, H - 10)]:
            g.polygon([(fx, fy - 14), (fx + 14, fy), (fx, fy + 14), (fx - 14, fy)],
                      fill="#c9a24a")
        for y0 in (50, H - 66):
            x = 48
            while x < W - 48:
                g.rectangle([x, y0, x + 10, y0 + 10], outline="#c9a24a", width=2)
                x += 16

        # ── 8. Text ──
        g.line([50, 155, W - 50, 155], fill=frame_rgb, width=1)
        g.line([50, H - 88, W - 50, H - 88], fill="#c9a24a", width=1)
        centered_text(g, 105, "ГЕКСАГРАМА " + str(num), font(SERIF, 30),
                      "#e8c87a")
        centered_text(g, 620, "Гексаграма " + str(num), font(SERIF, 24), "#c9a24a")
        name_face = ((card.translations or {}).get("uk", {}) or {}).get("name") or name
        name_f = font(SERIF_B, 40)
        while name_f.size > 24 and g.textlength(name_face, font=name_f) > W - 140:
            name_f = font(SERIF_B, name_f.size - 3)
        centered_text(g, 700, name_face, name_f, "#e8c87a")
        kw_face = str(card.keywords_upright or "")
        if kw_face:
            kf = font(ARIAL, 21)
            while kf.size > 14 and g.textlength(kw_face, font=kf) > W - 200:
                kf = font(ARIAL, kf.size - 2)
            centered_text(g, 748, kw_face, kf, "#c9a24a", max_w=W - 200)
    elif "футарк" in dnl or "futhark" in dnl:
        try:
            idx = int(num) - 1
            glyph = FUTHARK[idx] if 0 <= idx < 24 else "ᚠ"
        except ValueError:
            idx, glyph = 0, "ᚠ"
        # рунічний камінь кольору етиру (слава: fehu/feoh, hagal/isa, tiw)
        ring = ["#a33327", "#3f7a4e", "#2f5d8a"][int(idx // 8) if idx else 0]
        img, g = base_card("#11161f", "#e8c87a", "#8a7440", top="#060a12")
        fg, frame = "#e8c87a", "#8a7440"
        img, g = draw_rune_stone(img, g, W / 2, 345, 165, ring, glyph, "#cfb45c", f_rune)
        centered_text(g, 585, "РУНА " + str(num), font(ARIAL, 30), frame)
        centered_text(g, 645, name, f_med, fg)
        aett = ["Феху · перша етир", "Хагал · друга етир", "Тіваз · третя етир"][int(idx // 8) if idx else 0]
        centered_text(g, 705, aett, font(ARIAL, 22), "#c9a24a")
        centered_text(g, 752, str(card.keywords_upright or "")[:44], font(ARIAL, 20),
                      "#b8a877", max_w=W - 170)
    elif "поем" in dn or "поэм" in dn:
        try:
            idx = int(num) - 1
            glyph = POEM_RUNES[idx] if 0 <= idx < 29 else "ᚠ"
        except ValueError:
            idx, glyph = 0, "ᚠ"
        # та сама рунічна каменюка, але бронзова (поема = давніший футорк)
        ring = "#a9833f"
        img, g = base_card("#13100a", "#e8d9a8", "#9a7a3a", top="#070503")
        fg, frame = "#e8d9a8", "#9a7a3a"
        img, g = draw_rune_stone(img, g, W / 2, 345, 165, ring, glyph, "#cfb45c", f_rune)
        centered_text(g, 585, "РУНА " + str(num), font(ARIAL, 30), frame)
        centered_text(g, 645, name, f_med, fg)
        centered_text(g, 705, "Англосаксонський футорк · поема", font(ARIAL, 22), "#c9a24a")
        centered_text(g, 752, str(card.keywords_upright or "")[:46], font(ARIAL, 20),
                      "#b8a877", max_w=W - 170)
    elif "місячн" in dnl or "лунн" in dnl or "moon" in dnl:
        # нічне небо: градієнт + зорі + місячна емоji-силует на світлому диску
        import random as _rnd
        img, g = base_card("#0a1030", "#e8ecf5", "#c0c8e0", top="#02040c")
        fg = "#e8ecf5"
        try:
            ph = int(str(num).split("-")[0])
        except ValueError:
            ph = 1
        _r = _rnd.Random(ph)
        for _ in range(46):
            sx, sy = _r.randint(50, W - 50), _r.randint(70, 560)
            r0 = _r.choice([2, 2, 3])
            g.ellipse([sx - r0, sy - r0, sx + r0, sy + r0], fill="#cdd6f4")
        em = MOON_EMOJI.get(ph, "🌕")
        mf = font(EMOJI, 210)
        if has_glyph(mf, em):
            g.ellipse([W / 2 - 92, 238, W / 2 + 92, 422], fill="#e6dfc8", outline="#c9c2a8", width=5)
            g.text((W / 2, 330), em, font=mf, fill="#2a3a60", anchor="mm")
        else:
            frac = {1: 0.0, 2: 0.15, 3: 0.5, 4: 0.75, 5: 1.0, 6: 0.75, 7: 0.5, 8: 0.15}.get(ph, 0.5)
            draw_moon(img, g, W / 2, 330, 115, frac, "#e8ecf5")
        centered_text(g, 560, str(num), font(ARIAL, 40), "#c0c8e0")
        centered_text(g, 612, name, f_med, fg)
        centered_text(g, 668, str(card.category or "Місячна фаза"), font(ARIAL, 24), "#cdd6f4")
    elif "астролог" in dnl or "astrolog" in dnl:
        # яскравий градієнт за стихією
        el = (card.element or "").lower()
        grad = {"вогонь": ("#3a0f16", "#8a2e1a"), "огонь": ("#3a0f16", "#8a2e1a"),
                "вода": ("#081426", "#1f6f8a"), "повітря": ("#0c1e33", "#4f9ad5"),
                "воздух": ("#0c1e33", "#4f9ad5"), "земля": ("#16210e", "#7a8a2f")}
        top, bot = grad.get(el, ("#10173a", "#232c5e"))
        img, g = base_card(bot, "#f5f0e0", "#e8c87a", top=top)
        fg = "#f5f0e0"
        arc = (card.arcana_type or "")
        glyph = None
        try:
            n = int(num) - 1
        except (TypeError, ValueError):
            n = 0
        if "Дім" in arc or "Дом" in arc:
            # астрологічні доми: 12-секторне колесо, активний дім світиться
            sc = str(card.suit_code or "")
            hi = int(sc.replace("house", "")) - 1 if sc.startswith("house") else n % 12
            draw_house_wheel(g, W / 2, 330, hi, fg, "#8a6b25")
            title_block(600)
        elif "Фаза" in arc or "фаза" in arc:
            # фази Місяця: справжня форма місяця за номером фази 1–8
            import math
            sc = str(card.suit_code or "")
            ph = int(sc.replace("phase", "")) if sc.startswith("phase") else (n % 8) + 1
            frac = {1: 0.0, 2: 0.18, 3: 0.5, 4: 0.82, 5: 1.0, 6: 0.82,
                    7: 0.5, 8: 0.18}.get(ph, 0.5)
            draw_moon(img, g, W / 2, 330, 120, frac, fg)
            centered_text(g, 500, str(card.category or "Місячний цикл"),
                          font(ARIAL, 24), "#a9c2e8")
            title_block(600)
        elif "Пора року" in arc or "річн" in arc.lower():
            # поворотні точки року: символ знака-точки в центрі
            sc = str(card.suit_code or "")
            si = int(sc.replace("season", "")) - 1 if sc.startswith("season") else n % 4
            sig = {0: 0, 1: 3, 2: 6, 3: 9}[si % 4]
            g.text((W / 2, 330), ZODIAC[sig], font=font(SYM, 200), fill=fg, anchor="mm")
            centered_text(g, 500, str(card.theme or "Точка року"), font(ARIAL, 26), "#a9c2e8")
            title_block(600)
        elif "Астеро" in arc:
            # астероїд: коло + орбіта + іскра
            draw_asteroid(g, W / 2, 330, fg, "#8a6b25")
            centered_text(g, 500, str(card.planet or "Астероїд"), font(ARIAL, 26), "#a9c2e8")
            title_block(600)
        elif "Затемнен" in arc:
            # затемнення: сонце й місяць, що перекриваються
            draw_eclipse(g, W / 2, 330, fg, "#8a6b25")
            title_block(600)
        elif "Пара" in arc or "пара" in arc:
            # планетарна пара: два гліфи поруч
            p1 = PLANET_GLYPH.get(str(card.planet or ""), "☉")
            p2 = PLANET_GLYPH.get(str(card.suit or ""), "☿")
            f_pair = font(SYM, 128)
            g.text((W / 2 - 90, 330), p1, font=f_pair, fill=fg, anchor="mm")
            g.text((W / 2 + 90, 330), p2, font=f_pair, fill=fg, anchor="mm")
            title_block(600)
        elif "у знаку" in arc or "в знаку" in arc:
            # Radiant Sun: планета-масть велика + знак-колір збоку
            pg = PLANET_GLYPH.get(str(card.suit or ""), "☉")
            sg = SIGN_CODE_INDEX.get(str(card.zodiac_sign_code or "").lower(), 0)
            g.text((W / 2, 320), pg, font=font(SYM, 150), fill=fg, anchor="mm")
            g.text((W / 2, 320), ZODIAC[sg], font=font(SYM, 72), fill="#f0d080",
                   anchor="mm")
            centered_text(g, 460, str(card.suit or "") + " · " + str(card.zodiac_sign or ""),
                          font(ARIAL, 26), "#a9c2e8")
            title_block(600)
        elif "Знак" in arc:
            # знаки 12: точний символ за знаком, а не лише за num
            sig = SIGN_CODE_INDEX.get(str(card.zodiac_sign_code or "").lower(),
                                      n % 12 if 0 <= n < 12 else 0)
            glyph = ZODIAC[sig]
        elif "Планет" in arc:
            glyph = PLANET_GLYPH.get(str(name), PLANET_GLYPH.get(str(card.planet or "")))
        elif "Стих" in arc:
            glyph = {"Вогонь": "🜂", "Земля": "🜃", "Повітря": "🜁", "Вода": "🜄",
                     "Огонь": "🜂", "Воздух": "🜁"}.get(name)
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
    elif "архетип" in dnl or "archetyp" in dnl:
        # МАК: світло/тінь — верх пергамент, низ індіго (дух парності Шпеццано, своя графіка)
        img, g = base_card("#1a1440", "#e8c87a", "#d4a94e")
        fg = "#e8c87a"
        g.rectangle([30, 30, W - 30, H // 2 + 40], fill="#f5edd8")
        g.text((W / 2, 250), "☉", font=font(SYM, 90), fill="#8a6b25", anchor="mm")
        g.text((W / 2, 430), "☽", font=font(SYM, 90), fill="#e8c87a", anchor="mm")
        centered_text(g, 600, str(num), font(ARIAL, 40), "#d4a94e")
        centered_text(g, 652, name, f_med, fg)
    elif "шаман" in dnl or "shaman" in dnl:
        # тотем: смуга стихії + своя іконка кожному звіру
        el = (card.element or "").lower()
        band = {"вогонь": "#a33327", "огонь": "#a33327", "вода": "#2f5d8a",
                "повітря": "#4f9ad5", "воздух": "#4f9ad5", "земля": "#7a8a2f"}.get(el, "#d4a94e")
        g.rectangle([30, 30, W - 30, 130], fill=band)
        shaman_icon(g, str(card.number or ""), W / 2, 350, fg)
        title_block(600)
    elif "роду" in dnl or "предк" in dnl:
        # родинні символи: кожній ролі свій знак
        ancestor_icon(g, str(card.number or ""), W / 2, 340, fg)
        title_block(600)
    elif "cope" in dnl:
        # велика літера каналу в колі
        letter = str(card.category or "?")[:1].upper() or str(num or "?")[:1]
        g.ellipse([W / 2 - 120, 180, W / 2 + 120, 420], outline=fg, width=8)
        g.text((W / 2, 300), letter, font=font(ARIAL, 170), fill=fg, anchor="mm")
        centered_text(g, 520, str(card.category or ""), font(ARIAL, 40), frame)
        title_block(620)
    elif "терапевт" in dnl or "therapeutic" in dnl:
        # Терапевтична колода 85: VIA / BASIC Ph / Маслоу — єдина стилістика,
        # колір блоку за suit_code, великий символ-показник у центрі.
        sc = str(card.suit_code or "").lower()
        n = str(num or "")
        if n.startswith("M"):
            kind, block = "maslow", n
        elif len(n) == 2 and n[0].upper() in "BASICPM":
            kind, block = "basic", n[0].upper()
        else:
            kind, block = "via", n
        col = THERAPEUTIC_COLORS.get(sc, "#4f9ad5")
        r, g_, b_ = shade(col, -0.6)
        img, g = base_card("#101a2e", "#eef2e8", col, top="#%02x%02x%02x" % (r, g_, b_))
        fg, frame = "#eef2e8", col
        if kind == "via":
            # VIA: шестикутна зірка сили + назва доброчесності
            centered_text(g, 150, "VIA · СИЛА ХАРАКТЕРУ", font(ARIAL, 26), frame)
            pts = star_points(W / 2, 300, 118, 54, n=6)
            g.polygon(pts, outline=frame, width=6)
            nx = str(card.number or "")
            g.text((W / 2, 300), nx, font=font(SERIF_B, 56), fill=fg, anchor="mm")
            centered_text(g, 470, str(card.category or ""), font(ARIAL, 30), frame)
            centered_text(g, 618, str(num), font(ARIAL, 40), frame)
            centered_text(g, 672, name, f_med, fg)
            centered_text(g, 726, str(card.keywords_upright or "")[:44], font(ARIAL, 20),
                           "#cdd9ce", max_w=W - 160)
        elif kind == "basic":
            letter = block
            g.ellipse([W / 2 - 120, 180, W / 2 + 120, 420], outline=frame, width=8)
            g.text((W / 2, 300), letter, font=font(SERIF_B, 170), fill=fg, anchor="mm")
            centered_text(g, 470, str(card.category or ""), font(ARIAL, 30), frame)
            centered_text(g, 618, str(num), font(ARIAL, 40), frame)
            centered_text(g, 672, name, f_med, fg)
            centered_text(g, 726, str(card.keywords_upright or "")[:44], font(ARIAL, 20),
                           "#cdd9ce", max_w=W - 160)
        else:
            # Маслоу: піраміда з 5 рівнів, активний світиться
            try:
                lv = int(n[1:])
            except ValueError:
                lv = 1
            active_level = (lv - 1) // 5 + 1
            draw_maslow_pyramid(g, W / 2, 300, active_level, frame, "#8a9b8e")
            centered_text(g, 470, str(card.category or ""), font(ARIAL, 30), frame)
            centered_text(g, 618, str(num), font(ARIAL, 40), frame)
            centered_text(g, 672, name, f_med, fg)
            centered_text(g, 726, str(card.keywords_upright or "")[:44], font(ARIAL, 20),
                           "#cdd9ce", max_w=W - 160)
    elif "нумеролог" in dnl or "numerolog" in dnl:
        g.text((W / 2, 330), str(num), font=font(ARIAL, 220), fill=fg, anchor="mm")
        title_block(600)
    elif "гральн" in dnl or "игральн" in dnl or "playing" in dnl:
        # гральні 36: справжні символи Playing Cards (U+1F0A1...) або ранг+масть
        # на світлому картуші — щоб піки/трефи (чорні) були чітко видимі
        img, g = base_card("#f2e9d8", "#1c1a16", "#8a6b25")
        fg, frame = "#1c1a16", "#8a6b25"
        suit = card.suit or ""
        col = {"Чирва": "#a02222", "Бубна": "#a02222", "Трефа": "#1c1a16",
               "Піка": "#1c1a16"}.get(suit, "#1c1a16")
        rank = str(num or "").split("-")[-1]
        sl = str(num or "").split("-")[0] if "-" in str(num or "") else ""
        gpc = font(SYM, 250)
        uni = playing_card_unicode(sl, rank) if sl else ""
        if uni and has_glyph(gpc, uni):
            g.text((W / 2, 340), uni, font=gpc, fill=col, anchor="mm")
            g.text((70, 60), rank, font=font(ARIAL, 64), fill=col, anchor="ma")
            g.text((70, 130), SUIT_GLYPH.get(suit, "✦"), font=font(SYM, 56), fill=col, anchor="ma")
        else:
            glyph = SUIT_GLYPH.get(suit, "✦")
            g.text((70, 60), rank, font=font(ARIAL, 64), fill=col, anchor="ma")
            g.text((70, 130), glyph, font=font(SYM, 56), fill=col, anchor="ma")
            g.text((W / 2, 380), glyph, font=font(SYM, 220), fill=col, anchor="mm")
        title_block(620)
    elif "ленорман" in dnl or "lenormand" in dnl:
        # пергамент + контурна іконка + гральна відповідність
        img, g = base_card("#efe3cb", "#3a2c14", "#8a6b25")
        fg, frame = "#3a2c14", "#8a6b25"
        inset = LENORMAND_INSET.get(str(num), "")
        lenormand_icon(g, str(num), W / 2, 330, "#7a5a1e")
        if inset:
            g.text((W / 2, 500), inset, font=font(ARIAL, 60), fill="#7a5a1e", anchor="mm")
        centered_text(g, 600, str(num), font(ARIAL, 40), frame)
        centered_text(g, 652, name, f_med, fg)
    elif "цолькин" in dnl or "tzolkin" in dnl:
        if str(num or "").startswith("S"):
            idx = int(str(num[1:])) - 1
            col = SEAL_COLORS[idx % 4]
            # справжній гліф дня в білому картуші + кільце кольору печатки
            gl = DB_IMG / "13" / f"seal_{idx + 1:02d}.png"
            g.ellipse([W / 2 - 135, 175, W / 2 + 135, 445], outline=col, width=8)
            if gl.exists():
                glyph = Image.open(gl).convert("RGB").resize((220, 220))
                img.paste(glyph, (W // 2 - 110, 225))
                g.rectangle([W / 2 - 110, 225, W / 2 + 110, 445], outline=frame, width=4)
            else:
                g.ellipse([W / 2 - 110, 220, W / 2 + 110, 440], fill=col, outline=frame, width=5)
                g.text((W / 2, 330), str(num), font=font(ARIAL, 64), fill="#10173a" if idx % 4 == 1 else fg, anchor="mm")
        else:
            maya_number(g, W / 2, 330, int(str(num or "T0")[1:]), fg)
        title_block(600)
    elif "зодіак" in dnl or "зодиак" in dnl:
        # китайська монета + емоji-силует знака зодіаку в центрі
        img, g = base_card("#5c1522", "#f6d66a", "#c8922a", top="#22050a")
        fg, frame = "#f6d66a", "#c8922a"
        try:
            idx = (int(num) - 1) % 12
        except ValueError:
            idx = 0
        zodiak_coin(g, W / 2, 350, idx, fg, shade("#c8922a", -0.45))
        em = ZODIAC_EMOJI[idx]
        ef = font(EMOJI, 160)
        if has_glyph(ef, em):
            g.text((W / 2, 350), em, font=ef, fill="#5c1522", anchor="mm")
        else:
            nf = font(SERIF_B, 46)
            while nf.size > 24 and g.textlength(name, font=nf) > W - 220:
                nf = font(SERIF_B, nf.size - 3)
            centered_text(g, 350, name, nf, fg)
        lucky = (card.symbolism or "").split(". ")[0]
        centered_text(g, 596, str(num), font(ARIAL, 40), frame)
        centered_text(g, 650, "Китайський зодіак", font(ARIAL, 26), frame)
        centered_text(g, 700, lucky[:52], font(ARIAL, 20), shade("#f6d66a", -0.35))
    elif "огам" in dnl or "ogham" in dnl:
        # друїдична роща: нічна лісова галявина + стебло-вісь з рисками огама
        img = Image.new("RGBA", (W, H), (8, 10, 8, 255))
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for rr in range(200, 0, -4):
            a = int(40 * (1 - (rr / 200) ** 2.2))
            if a > 0:
                gd.ellipse([W / 2 - rr, 330 - rr, W / 2 + rr, 330 + rr],
                           fill=(70, 100, 60, a))
        glow = glow.filter(ImageFilter.GaussianBlur(20))
        img = Image.alpha_composite(img, glow).convert("RGB")
        g = ImageDraw.Draw(img)
        letter = str(num).upper()
        uni = OGHAM_UNICODE.get(letter, "")
        fg, frame = "#e8e2c4", "#5f8a4e"
        # кельтський орнамент по боках (трилисник-спіральки)
        for sx in (46, W - 46):
            for sy in (120, 330, 560):
                for rr in (26, 14):
                    g.arc([sx - rr, sy - rr, sx + rr, sy + rr], 0, 300,
                          fill="#4a6e3d", width=3)
        og_f = font(HIST, 270)
        # стебло-вісь по центру
        g.line([W / 2, 118, W / 2, 500], fill="#c8b27a", width=8)
        g.line([W / 2, 118, W / 2, 500], fill="#8a9e6b", width=3)
        if uni and has_glyph(og_f, uni):
            g.text((W / 2, 318), uni, font=og_f, fill="#e6d8a0", anchor="mm")
        else:
            draw_ogham(g, letter, W / 2, 168, 500, "#e6d8a0", w=11)
        # назва літери та дерево (suit)
        centered_text(g, 565, letter, font(SERIF_B, 30), "#b8c68a")
        tree = str(card.suit or "")
        centered_text(g, 615, tree, font(SERIF, 38), "#e8e2c4")
        centered_text(g, 672, name, f_med, fg)
        centered_text(g, 738, str(card.keywords_upright or "")[:48], font(ARIAL, 20),
                      "#9fb67e", max_w=W - 170)
        centered_text(g, 782, "Огам · " + str(card.category or ""), font(ARIAL, 22), "#5f8a4e")
    elif "сабіан" in dnl or "sabian" in dnl:
        # Сабіан-360: ГОЛОВНИЙ елемент — текст образу (symbolism), а не знак.
        # Знак зодіаку — дрібний маркер у куті; внизу мелко градус + знак.
        img, g = base_card("#0b0f2e", "#e8c87a", "#8a6b25", top="#04060f")
        fg, frame = "#e8c87a", "#8a6b25"
        sig = SIGN_CODE_INDEX.get(str(card.zodiac_sign_code or "").lower(), 0)
        try:
            deg = int(str(card.category or 0))
        except ValueError:
            deg = 0
        # дрібний знак у лівому куті + градус ліворуч
        g.text((76, 100), ZODIAC[sig], font=font(SYM, 64), fill="#a9833f", anchor="mm")
        g.text((76, 168), f"{deg}°", font=font(ARIAL, 30), fill="#8a6b25", anchor="mm")
        g.text((W - 76, 100), str(num), font=font(ARIAL, 36), fill="#8a6b25", anchor="mm")
        # образ-символ — контент усього полотна
        phrase = str(card.symbolism or "")
        pf = font(SERIF_B, 34)
        while pf.size > 22 and g.textlength(phrase, font=pf) > W - 150:
            pf = font(SERIF_B, pf.size - 2)
        lines = wrap_lines(g, phrase, pf, W - 150, 7)
        y = 300 - (len(lines) - 1) * 18
        for ln in lines:
            centered_text(g, y, ln, pf, fg)
            y += 44
        # нижній рядок: градус + знак, афірмація приналежності до системи
        g.line([W / 2 - 130, 640, W / 2 + 130, 640], fill="#8a6b25", width=1)
        centered_text(g, 688, f"{deg}° {str(card.zodiac_sign or '')}", font(ARIAL, 30),
                      "#c9a24a")
        centered_text(g, 732, "Сабіанський символ · " + str(num), font(ARIAL, 22), frame)
    elif "накшатр" in dnl or "nakshat" in dnl:
        # нічне небо: місячний серп + символ місячної стоянки
        img, g = base_card("#0a1030", "#e8ecf5", "#c0c8e0", top="#02040c")
        fg, frame = "#e8ecf5", "#c0c8e0"
        import random as _rnd
        _r = _rnd.Random(int(str(num or "1").split("-")[0]) if str(num or "1").split("-")[0].isdigit() else 7)
        for _ in range(42):
            sx, sy = _r.randint(50, W - 50), _r.randint(70, 560)
            g.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill="#cdd6f4")
        draw_moon(img, g, W / 2, 300, 120, 0.85, "#e8ecf5")
        sig = SIGN_CODE_INDEX.get(str(card.zodiac_sign_code or "").lower(), 0)
        g.text((W / 2, 300), ZODIAC[sig], font=font(SYM, 72), fill="#e8c87a", anchor="mm")
        centered_text(g, 470, name, font(SERIF_B, 36), fg)
        centered_text(g, 520, str(card.zodiac_sign or ""), font(ARIAL, 24), "#cdd6f4")
        pl = str(card.planet or "")
        pg = PLANET_GLYPH.get(pl, "")
        centered_text(g, 560, (pg + " " + pl).strip(), font(ARIAL, 24), "#e8c87a")
        centered_text(g, 608, str(card.theme or ""), font(ARIAL, 20), "#cdd6f4")
        centered_text(g, 644, str(card.symbolism or ""), font(ARIAL, 18), "#a9b4d6")
        centered_text(g, 684, str(num), font(ARIAL, 34), frame)
        centered_text(g, 728, str(card.category or ""), font(ARIAL, 22), "#cdd6f4")
    elif "плутчик" in dnl or "plutchik" in dnl:
        # пергамент + емоji-силует емоції Плутчика
        img, g = base_card("#faf4e8", "#2a2350", "#c9a24a")
        fg, frame = "#2a2350", "#c9a24a"
        col = str(card.element or "#e8c87a")
        dark = shade(col, -0.3)
        em = PLUTCHIK_EMOJI.get(name, "")
        ef = font(EMOJI, 220)
        if em and has_glyph(ef, em):
            g.text((W / 2, 300), em, font=ef, fill=col, anchor="mm")
        else:
            emotion_face(g, W / 2, 330, 142, name, col, dark)
        centered_text(g, 522, name, font(SERIF_B, 46), fg)
        opp = str(card.suit or "")
        centered_text(g, 572, "Опонент: " + opp, font(ARIAL, 26), "#6b5330")
        kw = (card.keywords_upright or "").split(",")[0].strip()
        centered_text(g, 614, kw, font(ARIAL, 22), shade("#2a2350", -0.25),
                      max_w=W - 140)
        centered_text(g, 680, str(num), font(ARIAL, 40), frame)
        centered_text(g, 732, "Карта емоцій · Плутчик", font(ARIAL, 22), "#8a6b25")
    elif "чакр" in dnl or "chakr" in dnl:
        # лотос чакри в її кольорі (мандала) + биджа-мантра в центрі
        base = CHAKRA_COLORS.get(str(card.element_code or "").lower(), "#e8c87a")
        r, g_, b_ = shade(base, -0.55)
        img, g = base_card("#12102a", "#f0ead8", "#c9a24a",
                           top="#%02x%02x%02x" % (r, g_, b_))
        fg, frame = "#f0ead8", "#c9a24a"
        chakra_lotus(g, W / 2, 330, shade(base, -0.45), base)
        bija = {1: "लं", 2: "वं", 3: "रं", 4: "यं", 5: "हं",
                6: "ॐ", 7: "ॐ"}.get(int(str(num or "1")[:1]), "ॐ")
        g.text((W / 2, 330), bija, font=font(ARIAL, 52), fill=fg, anchor="mm")
        g.text((W / 2, 272), "बीज", font=font(ARIAL, 22), fill=frame, anchor="ma")
        centered_text(g, 592, name, font(SERIF_B, 40), fg)
        centered_text(g, 648, str(card.element or ""), font(ARIAL, 26), frame)
        centered_text(g, 700, "Лотос " + str(num) + " · Чакра", font(ARIAL, 22), "#c9a24a")
    elif "цінн" in dnl or "ценност" in dnl:
        # цінності (Шварц): скарбниця на вечірньому тлі
        img, g = base_card("#231a3a", "#efe6cf", "#cfa75a", top="#120d22")
        fg, frame = "#efe6cf", "#cfa75a"
        g.text((W / 2, 250), "✦", font=font(SYM, 120), fill=frame, anchor="mm")
        centered_text(g, 150, "ЦІННІСТЬ · ОРІЄНТИР", font(ARIAL, 26), frame)
        kw = str(card.keywords_upright or "").split(",")[0].strip()
        kf = font(SERIF_B, 52)
        while kf.size > 24 and g.textlength(kw, font=kf) > W - 150:
            kf = font(SERIF_B, kf.size - 3)
        centered_text(g, 330, kw, kf, fg)
        centered_text(g, 420, str(card.keywords_upright or ""), font(ARIAL, 21), frame,
                       max_w=W - 160)
        centered_text(g, 610, str(num), font(ARIAL, 40), frame)
        centered_text(g, 662, name, f_med, fg)
        centered_text(g, 716, "Карта цінностей", font(ARIAL, 22), frame)
    elif "ресурс" in dnl or "resourc" in dnl:
        # ресурси стійкості: смарагдова енергія
        img, g = base_card("#0e2a24", "#edf2e9", "#6fae9a", top="#061512")
        fg, frame = "#edf2e9", "#6fae9a"
        g.text((W / 2, 250), "☘", font=font(SYM, 120), fill=frame, anchor="mm")
        centered_text(g, 150, "РЕСУРС · ОПОРА", font(ARIAL, 26), frame)
        kw = str(card.keywords_upright or "").split(",")[0].strip()
        kf = font(SERIF_B, 52)
        while kf.size > 24 and g.textlength(kw, font=kf) > W - 150:
            kf = font(SERIF_B, kf.size - 3)
        centered_text(g, 330, kw, kf, fg)
        centered_text(g, 420, str(card.keywords_upright or ""), font(ARIAL, 21), frame,
                       max_w=W - 160)
        centered_text(g, 610, str(num), font(ARIAL, 40), frame)
        centered_text(g, 662, name, f_med, fg)
        centered_text(g, 716, "Карта ресурсів", font(ARIAL, 22), frame)
    elif "стихі" in dnl or "стихии" in dnl or "стих" in dnl:
        # стихії: алхімічний трикутник/символ у власних кольорах
        colmap = {"fire": "#e0563a", "water": "#3f86c9", "air": "#7cbfe8",
                  "earth": "#8a9e4f", "aether": "#9a6fd0"}
        basec = colmap.get(str(card.element_code or "").lower(), "#cfa75a")
        r, g_, b_ = shade(basec, -0.6)
        img, g = base_card("#10142a", "#f0ead8", basec, top="#080a18")
        fg, frame = "#f0ead8", basec
        gly = str(card.symbolism or "🜁")
        gf = font(SYM, 260)
        if has_glyph(gf, gly):
            g.text((W / 2, 320), gly, font=gf, fill=frame, anchor="mm")
        else:  # трикутник стихії
            up = "ого" in name.lower() or "ітря" in name.lower() or "оздух" in name.lower()
            s = 120
            if up:
                g.polygon([(W / 2 - s, 420), (W / 2 + s, 420), (W / 2, 220)], outline=fg, width=8)
            else:
                g.polygon([(W / 2 - s, 220), (W / 2 + s, 220), (W / 2, 420)], outline=fg, width=8)
        centered_text(g, 502, name, font(SERIF_B, 46), fg)
        centered_text(g, 560, str(card.suit or ""), font(ARIAL, 26), frame)
        centered_text(g, 614, str(card.keywords_upright or ""), font(ARIAL, 22), "#cdd3e8",
                       max_w=W - 160)
        centered_text(g, 680, "Стихія " + str(num), font(ARIAL, 32), frame)
        centered_text(g, 732, "Елемент · класична філософія", font(ARIAL, 22), frame)
    elif "архангел" in dnl or "archangel" in dnl:
        # архангели: сяюча зірка-ореол на нічному синьому
        img, g = base_card("#0b1d33", "#f3e9ce", "#d9a05b", top="#040b16")
        fg, frame = "#f3e9ce", "#d9a05b"
        draw_radiant(g, W / 2, 330, 150, frame, "#7a5a1e")
        g.text((W / 2, 330), "✶", font=font(SYM, 90), fill=shade("#d9a05b", 0.4),
               anchor="mm")
        centered_text(g, 512, name, font(SERIF_B, 44), fg)
        centered_text(g, 566, str(card.suit or ""), font(ARIAL, 26), frame)
        centered_text(g, 612, str(card.keywords_upright or "")[:48], font(ARIAL, 22), "#c8d2e8",
                       max_w=W - 150)
        centered_text(g, 676, str(num), font(ARIAL, 36), frame)
        centered_text(g, 726, "Ангельський оракул", font(ARIAL, 22), frame)
    elif "афірм" in dnl or "affirm" in dnl:
        # афірмації: сонячна пергаментна картка-нагадування
        img, g = base_card("#f7f0e2", "#3a2c14", "#8a6b25")
        fg, frame = "#3a2c14", "#8a6b25"
        g.text((W / 2, 240), "❀", font=font(SYM, 120), fill="#8a6b25", anchor="mm")
        centered_text(g, 140, "АФІРМАЦІЯ · ДЕНЬ", font(ARIAL, 26), "#8a6b25")
        kw = str(card.keywords_upright or "").split(",")[0].strip()
        a = str(card.meaning_general or "").split(".")
        kf = font(SERIF, 38)
        while kf.size > 22 and g.textlength(kw, font=kf) > W - 150:
            kf = font(SERIF, kf.size - 3)
        centered_text(g, 330, kw, kf, fg)
        lf = font(SERIF, 20)
        lines = wrap_lines(g, str(card.meaning_general or ""), lf, W - 170, 4)
        y = 410
        for ln in lines:
            centered_text(g, y, ln, lf, "#6b5330")
            y += 28
        centered_text(g, 580, str(num), font(ARIAL, 36), "#8a6b25")
        centered_text(g, 632, name, font(SERIF_B, 34), fg)
        centered_text(g, 686, "Карта дня", font(ARIAL, 22), "#8a6b25")
    elif "бажан" in dnl or "wish" in dnl:
        # бажання: зірка-амбіція на теплому тлі
        img, g = base_card("#2b1a12", "#f5e9da", "#d9a05b", top="#140b06")
        fg, frame = "#f5e9da", "#d9a05b"
        pts = star_points(W / 2, 250, 95, 38, n=6)
        g.polygon(pts, outline=frame, width=6)
        centered_text(g, 150, "БАЖАННЯ", font(ARIAL, 26), frame)
        kw = str(card.keywords_upright or "").split(",")[0].strip()
        kf = font(SERIF_B, 50)
        while kf.size > 24 and g.textlength(kw, font=kf) > W - 150:
            kf = font(SERIF_B, kf.size - 3)
        centered_text(g, 400, kw, kf, fg)
        centered_text(g, 470, str(card.keywords_upright or ""), font(ARIAL, 21), frame,
                       max_w=W - 160)
        centered_text(g, 610, str(num), font(ARIAL, 40), frame)
        centered_text(g, 662, name, f_med, fg)
        centered_text(g, 716, "Карта бажань", font(ARIAL, 22), frame)
    elif "сфір" in dnl or "sephir" in dnl:
        # Каббала: Древо Життя, активна сфіра сяє золотом
        img, g = base_card("#1a1440", "#e8c87a", "#8a6b25", top="#0a0724")
        fg, frame = "#e8c87a", "#8a6b25"
        try:
            hi = int(str(num))
        except ValueError:
            hi = 1
        tree_of_life(g, W / 2, 205, 555, hi % 10, fg, frame)
        centered_text(g, 150, "СФІРА " + str(num), font(ARIAL, 30), frame)
        centered_text(g, 606, name, font(SERIF_B, 36), fg)
        centered_text(g, 656, str(card.theme or ""), font(ARIAL, 24), frame, max_w=W - 150)
        centered_text(g, 700, str(card.suit or ""), font(ARIAL, 22), "#a9833f")
        centered_text(g, 748, "Каббала · Древо Життя", font(ARIAL, 20), frame)
    elif "шлях" in dnl or "path" in dnl:
        # Каббала: шлях 11–32 — сяюча грань між сфіротами + літера івриту
        img, g = base_card("#241244", "#efe6cf", "#cfa75a", top="#0e071f")
        fg, frame = "#efe6cf", "#cfa75a"
        pa, pb = 1, 2
        try:
            pa, pb = (int(x) for x in str(card.theme or "1→2").replace("→", " ").split())
        except ValueError:
            pass
        centered_text(g, 148, "ШЛЯХ " + str(num), font(ARIAL, 28), frame)
        heb = str(card.suit or "")
        hb = font(ARIAL, 76)
        if heb and has_glyph(hb, heb):
            g.text((W / 2, 92), heb, font=hb, fill=fg, anchor="mm")
        else:
            centered_text(g, 92, str(card.suit_code or ""), font(SERIF_B, 30), fg)
        tree_of_life(g, W / 2, 230, 560, pa, fg, frame, path_hi=(pa, pb))
        taro = str(card.symbolism or "")
        centered_text(g, 602, taro[:40], font(ARIAL, 26), frame)
        centered_text(g, 656, name, font(SERIF_B, 30), fg)
        centered_text(g, 704, str(card.element or ""), font(ARIAL, 22), frame)
        centered_text(g, 744, str(card.suit_code or ""), font(ARIAL, 20), "#a9833f")
    elif "багуа" in dnl or "bagua" in dnl:
        # Багуа: ієрогліф + три риси триграми
        img, g = base_card("#141024", "#f0ead8", "#c9a24a", top="#080611")
        fg, frame = "#f0ead8", "#c9a24a"
        cjk = str(card.suit or "")
        cf = font(CJK, 150)
        if has_glyph(cf, cjk):
            g.text((W / 2, 240), cjk, font=cf, fill=fg, anchor="mm")
        else:
            centered_text(g, 220, str(card.suit_code or ""), font(SYM, 120), fg)
        try:
            idx = int(num) - 1
            trig = "☰☱☲☳☴☵☶☷"[idx % 8]
        except (ValueError, IndexError):
            trig = "☰"
        draw_trigram(g, W / 2, 430, trig, fg)
        centered_text(g, 596, name, font(SERIF_B, 36), fg)
        centered_text(g, 648, str(card.zodiac_sign or ""), font(ARIAL, 24), frame)
        centered_text(g, 692, str(card.element or ""), font(ARIAL, 24), frame)
        centered_text(g, 732, "Багуа · " + str(num), font(ARIAL, 22), "#a9833f")
    elif "іфа" in dnl or "ifa" in dnl:
        # Іфа: ланцюжок opó oja (палички I/II) у стилі ifa-wisdom.com
        img, g = base_card("#12200f", "#f0ecd8", "#c9a24a", top="#060f07")
        fg, frame = "#f0ecd8", "#c9a24a"
        binario = str(card.suit_code or "00000000")
        if len(binario) != 8 or set(binario) - {"0", "1"}:
            binario = "00000000"
        is_meji = "межі" in str(card.arcana_type or "").lower()
        # шапка: бінарний код у рамці
        g.rounded_rectangle([W / 2 - 140, 96, W / 2 + 140, 162], radius=12,
                            fill="#0b180a", outline="#2c4026", width=2)
        bf = font(ARIAL, 28)
        while bf.size > 16 and g.textlength(binario, font=bf) > W - 330:
            bf = font(ARIAL, bf.size - 2)
        g.text((W / 2, 122), binario, font=bf, fill="#e6c86a", anchor="mm")
        centered_text(g, 168, "ОПÓ ОЖА · ОДУ", font(ARIAL, 22), "#7ea25f")
        ifa_grid(g, W / 2, 370, binario, frame, "#2c4026")
        epitet = str(card.meaning_spirituality or "")
        if not epitet and card.translations:
            epitet = str((card.translations.get("uk") or {}).get("meaning_spirituality") or "")
        centered_text(g, 622, epitet[:96], font(ARIAL, 22), "#c8c89a", max_w=W - 160)
        centered_text(g, 664, name, font(SERIF_B, 36), fg)
        centered_text(g, 712, ("Межі · Оду " if is_meji else "Омо · Оду ") + str(num),
                      font(ARIAL, 24), frame)
        centered_text(g, 752, "Іфа · " + str(card.suit or ""), font(ARIAL, 20), "#8ba96f")
    elif "числ-ангел" in dnl or "angel-number" in dnl:
        # числа-ангели: велике число в сяйві
        img, g = base_card("#141423", "#f0ead8", "#c9a24a", top="#07070f")
        fg, frame = "#f0ead8", "#c9a24a"
        for i in range(12):
            import math as _m
            a = _m.radians(i * 30)
            g.line([W / 2 + 160 * _m.cos(a), 330 + 160 * _m.sin(a),
                    W / 2 + 205 * _m.cos(a), 330 + 205 * _m.sin(a)],
                   fill="#4a4372", width=3)
        nf = font(SERIF_B, 130)
        while nf.size > 60 and g.textlength(str(num or ""), font=nf) > W - 170:
            nf = font(SERIF_B, nf.size - 6)
        centered_text(g, 330, str(num or ""), nf, fg)
        centered_text(g, 500, name, font(SERIF_B, 34), fg)
        centered_text(g, 552, str(card.keywords_upright or "")[:52], font(ARIAL, 22),
                       frame, max_w=W - 160)
        centered_text(g, 660, "Число-ангел · " + str(num), font(ARIAL, 26), frame)
    elif "тасеограф" in dnl or "tealeaf" in dnl or "чай" in dnl:
        # тасеографія: чашка + листя на дні + символ знака (гліф у чашці)
        img, g = base_card("#efe3cb", "#3a2c14", "#8a6b25")
        fg, frame = "#3a2c14", "#8a6b25"
        draw_teacup(g, W / 2, 430, "#7a5a1e", "#8a6b25")
        em, fb = TASEO_GLYPH.get(str(card.suit or ""), ("✦", "✦"))
        sf = font(EMOJI, 110)
        if has_glyph(sf, em):
            g.text((W / 2, 452), em, font=sf, fill="#2b1510", anchor="mm")
        else:
            g.text((W / 2, 452), fb, font=font(SYM, 105), fill="#2b1510", anchor="mm")
        centered_text(g, 132, "СИМВОЛ У ЧАШЦІ", font(ARIAL, 24), "#8a6b25")
        centered_text(g, 610, name, font(SERIF_B, 40), fg)
        centered_text(g, 670, str(card.suit or ""), font(ARIAL, 26), "#7a5a1e")
        centered_text(g, 722, str(card.keywords_upright or "")[:48], font(ARIAL, 22), "#6b5330",
                       max_w=W - 160)
        centered_text(g, 782, "Знак " + str(num) + " · Тасеографія", font(ARIAL, 22), "#8a6b25")
    elif "кристал" in dnl or "crystal" in dnl:
        # кристали: кольоровий самоцвіт + властивості
        basec = CRYSTAL_COLORS.get(str(card.element_code or "").lower(), "#9a6fd0")
        r, g_, b_ = shade(basec, -0.6)
        img, g = base_card("#141423", "#f0ead8", basec, top="#07070f")
        fg, frame = "#f0ead8", basec
        draw_gem(g, W / 2, 330, 130, basec, frame)
        centered_text(g, 520, name, font(SERIF_B, 40), fg)
        centered_text(g, 574, str(card.suit or ""), font(ARIAL, 26), frame)
        centered_text(g, 622, str(card.keywords_upright or "")[:48], font(ARIAL, 22),
                       "#cdd3e8", max_w=W - 160)
        centered_text(g, 682, str(num), font(ARIAL, 34), frame)
        centered_text(g, 726, "Оракул самоцвітів", font(ARIAL, 20), frame)
    elif "навчальн" in dnl and ("таро" in dnl or "tarot" in dnl):
        # 7 навчальних таро (51–57): старші — сяйво + номер, молодші — піпки/двір
        th = tarot_theme(dnl)
        img, g = base_card(th["top"], th["bg"], th["fg"], top=th["top"])
        fg, frame = th["fg"], th["frame"]
        is_major = "старш" in arc
        if is_major:
            draw_radiant(g, W / 2, 330, 165, th["glow"], shade(th["glow"], -0.55))
            nf = font(SERIF_B, 120)
            while nf.size > 30 and g.textlength(str(num or ""), font=nf) > W - 190:
                nf = font(SERIF_B, nf.size - 6)
            centered_text(g, 332, str(num or ""), nf, fg)
            draw_tarot_orb(g, W / 2, 150, 34, th["glow"])
            centered_text(g, 118, th["label"], font(ARIAL, 26), th["glow"])
            centered_text(g, 540, name, font(SERIF_B, 46), fg)
            centered_text(g, 600, str(card.keywords_upright or "")[:52], font(ARIAL, 22),
                          frame, max_w=W - 160)
            centered_text(g, 672, str(card.arcana_type or "") + " · " + str(num),
                          font(ARIAL, 28), frame)
            centered_text(g, 720, "Таро · процедурна вправа", font(ARIAL, 20), frame)
        else:
            suit = (card.suit_code or "").lower()
            try:
                rank = int(str(num).rsplit("-", 1)[1])
            except (ValueError, IndexError):
                rank = 1
            kind = "major" if False else ""
            if rank <= 10:
                for (px, py) in pip_grid(rank, W / 2, 320):
                    draw_tarot_orb(g, px, py, 30, th["glow"] if rank % 2 == 0 else frame)
            else:
                draw_tarot_orb(g, W / 2, 330, 96, th["glow"])
                centered_text(g, 470, str(card.suit or ""), font(ARIAL, 34), frame)
                centered_text(g, 150, (TAROT_RANKWORD.get(rank, "") or ""),
                              font(ARIAL, 36), th["glow"])
            sl = TAROT_SUITGLYPH.get(suit)
            if sl:
                centered_text(g, 532, sl[1].upper() if False else str(card.suit or ""),
                              font(ARIAL, 30), frame)
            centered_text(g, 580, name, font(SERIF_B, 42), fg)
            centered_text(g, 640, str(card.keywords_upright or "")[:48], font(ARIAL, 22),
                          frame, max_w=W - 160)
            centered_text(g, 708, str(card.suit or "") + " · " + str(rank),
                          font(ARIAL, 28), frame)
            centered_text(g, 748, "Таро · процедурна вправа", font(ARIAL, 18), frame)
    elif "циган" in dnl or "gypsy" in dnl or "цыган" in dnl:
        # Циганські (навчальні): пергамент + символ-гліф (значення карти)
        img, g = base_card("#efe3cb", "#3a2c14", "#8a6b25")
        fg, frame = "#3a2c14", "#8a6b25"
        em, fb = GYPSY_GLYPH.get(str(num), ("✦", "✦"))
        gf = font(EMOJI, 230)
        if has_glyph(gf, em):
            g.text((W / 2, 300), em, font=gf, fill="#7a5a1e", anchor="mm")
        else:
            g.text((W / 2, 300), fb, font=font(SYM, 200), fill="#7a5a1e", anchor="mm")
        centered_text(g, 490, str(num), font(ARIAL, 40), frame)
        centered_text(g, 545, name, f_med, fg)
        centered_text(g, 610, str(card.keywords_upright or "")[:46], font(ARIAL, 22),
                      "#6b5330", max_w=W - 160)
        centered_text(g, 676, "Циганська карта · " + str(num), font(ARIAL, 22), frame)
        centered_text(g, 726, str(card.symbolism or "")[:60], font(ARIAL, 20), "#8a6b25",
                      max_w=W - 120)
    elif "сонник" in dnl or "сонник" in dnl or "dream dict" in dnl:
        # Сонник (навчальний): нічне небо + емоji-символ сновидіння
        img, g = base_card("#0a0d22", "#e8ecf5", "#c0c8e0", top="#02030a")
        fg, frame = "#e8ecf5", "#c0c8e0"
        em = str(card.theme or "🌙").split()[0]
        ef = font(EMOJI, 220)
        if has_glyph(ef, em):
            g.text((W / 2, 250), em, font=ef, fill="#d8c65e", anchor="mm")
        else:
            fb = str(card.symbolism or "✦")
            g.text((W / 2, 250), fb, font=font(SYM, 150), fill="#d8c65e", anchor="mm")
        centered_text(g, 120, "СОННИК", font(ARIAL, 26), frame)
        centered_text(g, 400, str(card.arcana_type or "Символ сну"), font(ARIAL, 24), "#cdd6f4")
        centered_text(g, 470, str(num), font(ARIAL, 40), frame)
        centered_text(g, 530, name, f_med, fg)
        centered_text(g, 586, str(card.keywords_upright or ""), font(ARIAL, 22), "#a9b4d6",
                       max_w=W - 160)
        centered_text(g, 700, "Сонник · символ сновидіння", font(ARIAL, 22), frame)
    else:
        g.text((W / 2, 300), "✦", font=font(SYM, 170), fill=fg, anchor="mm")
        title_block(560)
    return img


def slug_deck(deck_id, deck_name):
    return f"{deck_id:02d}"


def run(only=None, force=False):
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
                if force or not dest.exists():
                    render(c, deck).save(dest, quality=82)
                    made += 1
                pub = PUB / rel
                if force or not pub.exists():
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
    argv = _s.argv[1:]
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    force = "--force" in argv
    run(only, force=force)
