"""fetch_maya_glyphs.py — 20 гліфів днів (DaySign *.svg) з Wikimedia Commons.
Гліфи тисячолітньої давнини — PD; конкретні SVG-прорисовки можуть бути CC-BY-SA:
автора і ліцензію пишемо в опис колоди + sources_log (умови дотримано).
PNG отримуємо серверним рендером Commons (Special:FilePath?width=).
Запуск з папки backend/: python scripts/fetch_maya_glyphs.py
"""
import sys
import time
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import requests

from app.core.database import SessionLocal
from app.models import Card, Deck
from import_public_domain_sources import HEADERS, IMAGE_HEADERS

SEALS = ["Imix", "Ik", "Akbal", "Kan", "Chiccan", "Cimi", "Manik", "Lamat",
         "Muluc", "Oc", "Chuen", "Eb", "Ben", "Ix", "Men", "Cib", "Caban",
         "Etznab", "Cauac", "Ahau"]
API = "https://commons.wikimedia.org/w/api.php"
DB_IMG = Path(__file__).resolve().parents[1] / "Database" / "images" / "13"
PUB = Path(__file__).resolve().parents[2] / "frontend" / "public" / "assets" / "13"

import sys as _s
_s.stdout.reconfigure(encoding="utf-8", errors="replace")


def info(title):
    d = requests.get(API, params={"action": "query", "titles": title, "prop": "imageinfo",
                                  "iiprop": "url|extmetadata", "format": "json"},
                     headers=HEADERS, timeout=30).json()
    page = list(d["query"]["pages"].values())[0]
    if "missing" in page:
        return None
    return page["imageinfo"][0]


def run():
    DB_IMG.mkdir(parents=True, exist_ok=True)
    PUB.mkdir(parents=True, exist_ok=True)
    credits = []
    db = SessionLocal()
    try:
        deck = db.query(Deck).filter(Deck.name.like("%Цолькин%")).first()
        for i, seal in enumerate(SEALS, 1):
            title = f"File:DaySign {seal}.svg"
            try:
                ii = info(title)
            except Exception as e:
                print(f"[WARN] {seal}: {e}")
                continue
            if not ii:
                print(f"[WARN] нема файлу: {title}")
                continue
            meta = ii.get("extmetadata", {})
            artist = (meta.get("Artist", {}) or {}).get("value", "")
            lic = ((meta.get("LicenseShortName", {}) or {}).get("value", "") or "см. Commons").strip()
            import re
            artist = re.sub(r"<[^>]+>", "", artist).strip()[:120]
            credits.append(f"{seal}: {artist} ({lic})")
            url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(title.replace('File:', ''))}?width=600"
            dest = DB_IMG / f"seal_{i:02d}.png"
            if not dest.exists():
                r = requests.get(url, headers=IMAGE_HEADERS, timeout=60)
                r.raise_for_status()
                dest.write_bytes(r.content)
                print(f"[OK] {seal} ({lic})")
                time.sleep(3)
            pub = PUB / f"seal_{i:02d}.png"
            if not pub.exists():
                pub.write_bytes(dest.read_bytes())
            card = db.query(Card).filter_by(deck_id=deck.id, number=f"S{i:02d}").first()
            if card:
                card.image_path = f"/assets/13/seal_{i:02d}.png"
        db.commit()
        cred = "Гліфи днів: " + "; ".join(credits)
        deck.description = (deck.description or "") + f"\n{cred}"
        db.commit()
        Path(__file__).resolve().parents[1] / "Database" / "_pd_cache" / "maya_credits.txt"
        print(f"[glyphs] готово, атрибуцій: {len(credits)}")
        with open(Path(__file__).resolve().parents[1] / "Database" / "_pd_cache" / "maya_credits.txt",
                   "w", encoding="utf-8") as f:
            f.write(cred)
    finally:
        db.close()


if __name__ == "__main__":
    run()
