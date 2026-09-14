"""fetch_reference_images.py — фото для довідкових профілів видань.
PD/сумісне лише: Вісконті (Cary-Yale, PD, Yale/Beinecke) + Марсель Конвер
(CC-BY-SA 4.0, Tarot World Project — атрибуція в описі колоди + sources_log).
Сучасні комерційні колоди (Thoth, Hay House, Rockpool, OH, Спеццано) — НЕ качаємо
(копірайт): їм генеруємо фірмову емблему-обкладинку.
Запуск з папки backend/: python scripts/fetch_reference_images.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import requests
from PIL import Image, ImageDraw, ImageFont

from app.core.database import Base, SessionLocal, engine
from app.models import Deck
from import_public_domain_sources import HEADERS, IMAGE_HEADERS

W, H = 512, 840
ROOT = Path(__file__).resolve().parents[2]
DB_IMG = Path(__file__).resolve().parents[1] / "Database" / "images"
PUB = ROOT / "frontend" / "public" / "assets"

import sys as _s
_s.stdout.reconfigure(encoding="utf-8", errors="replace")

PHOTOS = {
    "Visconti-Sforza Tarot": [
        "File:Cary-Yale Tarot deck - The Empress.jpg",
        "File:Cary-Yale Tarot deck - Hope.jpg",
        "File:Cary-Yale Tarot deck - Charity.jpg",
    ],
    "Tarot de Marseille": [
        "File:LE MAT Nicolas Conver Tarot 1760.jpg",
        "File:I LE BATELEUR Nicolas Conver Tarot 1760.jpg",
        "File:XXI LE MONDE Nicolas Conver Tarot 1760.jpg",
    ],
}

EMBLEMS = [  # (deck_name, short_title) — процедурні обкладинки замість чужих фото
    ("Thoth Tarot", "THOTH"),
    ("Mystical Shaman Oracle", "MYSTICAL\nSHAMAN"),
    ("Спиритический оракул тотемов", "ТОТЕМИ"),
    ("Shamanic Oracle (Rockpool)", "SHAMANIC\nORACLE"),
    ("Cope (оригінальне видання, 88)", None),
    ("OH cards / Persona (оригінальні видання)", "OH ·\nPERSONA"),
    ("Архетипы и Тени (Спеццано, 90)", "АРХЕТИПИ\nІ ТІНІ"),
    ("Astrological Oracle (22, огляд Aeclectic)", "ASTRO\nORACLE"),
]

COPE_EXACT = "Cope (оригінальне видання, 88)"


def resolve_url(title):
    d = requests.get("https://commons.wikimedia.org/w/api.php",
                     params={"action": "query", "titles": title, "prop": "imageinfo",
                             "iiprop": "url", "format": "json"},
                     headers=HEADERS, timeout=30).json()
    page = list(d["query"]["pages"].values())[0]
    ii = page.get("imageinfo")
    if not ii:
        raise ValueError(f"нема imageinfo: {title}")
    return ii[0]["url"].split("?")[0]


def emblem(title, year=""):
    img = Image.new("RGB", (W, H), "#171233")
    g = ImageDraw.Draw(img)
    g.rectangle([14, 14, W - 14, H - 14], outline="#8f7bff", width=6)
    g.rectangle([30, 30, W - 30, H - 30], outline="#8f7bff", width=2)
    g.ellipse([W / 2 - 120, 130, W / 2 + 120, 370], outline="#d4a94e", width=6)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 56)
    y = 240
    for line in title.split("\n"):
        g.text((W / 2, y), line, font=f, fill="#e8c87a", anchor="mm")
        y += 70
    g.text((W / 2, 470), "", font=f, fill="#8f7bff", anchor="mm")
    cx0 = W / 2
    g.polygon([(cx0, 430), (cx0 + 26, 470), (cx0, 510), (cx0 - 26, 470)], fill="#8f7bff")
    if year:
        g.text((W / 2, 620), str(year), font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 44),
               fill="#b9a7ff", anchor="mm")
    return img


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for deck_name, files in PHOTOS.items():
            deck = db.query(Deck).filter_by(name=deck_name).first()
            if not deck:
                print(f"[WARN] нема колоди: {deck_name}")
                continue
            key = f"ref_{deck.id:02d}"
            web_paths = []
            for idx, title in enumerate(files):
                fname = ["cover.jpg", "prev1.jpg", "prev2.jpg"][idx]
                try:
                    url = resolve_url(title)
                except Exception as e:
                    print(f"[WARN] {title}: {e}")
                    continue
                time.sleep(1)
                dest = DB_IMG / key / fname
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    r = requests.get(url.split("?")[0], headers=IMAGE_HEADERS, timeout=60)
                    r.raise_for_status()
                    dest.write_bytes(r.content)
                    print(f"[OK] {key}/{fname}")
                    time.sleep(3)
                pub = PUB / key / fname
                pub.parent.mkdir(parents=True, exist_ok=True)
                if not pub.exists():
                    Image.open(dest).save(pub, quality=72, optimize=True)
                web_paths.append(f"/assets/{key}/{fname}")
            deck.cover_image = web_paths[0]
            deck.gallery = web_paths[1:]
            if deck_name == "Tarot de Marseille" and "Tarot World Project" not in (deck.description or ""):
                deck.description = (deck.description or "") + (
                    "\nФото карт: Tarot World Project, CC BY-SA 4.0 (Wikimedia Commons).")
        for deck_name, short in EMBLEMS:
            deck = db.query(Deck).filter_by(name=deck_name).first()
            if not deck:
                print(f"[WARN] нема колоди: {deck_name}")
                continue
            key = f"ref_{deck.id:02d}"
            dest = DB_IMG / key / "cover.jpg"
            dest.parent.mkdir(parents=True, exist_ok=True)
            title = short or deck.name[:24]
            if not dest.exists():
                emblem(title, deck.year or "").save(dest, quality=82)
                print(f"[OK] emblem {key}")
            pub = PUB / key / "cover.jpg"
            pub.parent.mkdir(parents=True, exist_ok=True)
            if not pub.exists():
                Image.open(dest).save(pub, quality=72, optimize=True)
            deck.cover_image = f"/assets/{key}/cover.jpg"
            deck.gallery = deck.gallery or []
        db.commit()
        print("[ref-images] готово")
    finally:
        db.close()


if __name__ == "__main__":
    run()
