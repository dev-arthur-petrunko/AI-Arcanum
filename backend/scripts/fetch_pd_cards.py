"""fetch_pd_cards.py — скачує реальні PD-карти двох колод з Wikimedia Commons:
  deck 24 Tarot de Marseille (Lequart, PD), 78 карт — категорія «Tarot de Marseille (Single Cards)»;
  deck 23 Visconti-Sforza (Pierpont Morgan-Bergamo, PD), доступні карти — серія Bembo-Visconti-tarot-*.
Кладемо у backend/Database/images/<deck_id>/ та копіюємо у frontend/public/assets/<deck_id>/.
Слот-ідентифікатор файла = «slot»: для старших римська цифра (0, I..XXI), для молодших «масть-номер».
"""
import json
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, r"C:\Users\Arthur\AppData\Local\Temp\opencode")
from wm_common import api

UA = "Arcanum-StudyBot/1.0 (educational tarot database; contact: owner)"
ROOT = Path(__file__).resolve().parents[2]

SUIT_CODE = {"B": "wands", "C": "cups", "P": "pentacles", "S": "swords"}
FRO = {"J": 11, "H": 12, "Q": 13, "K": 14}


def marseille_cards():
    items = [
        ("File:TT Tarot.png", "0"),
    ]
    for i in range(1, 22):
        items.append((f"File:T{i} Tarot.png", i))  # I..XXI
    for code in ("B", "C", "P", "S"):
        for num in range(1, 11):
            items.append((f"File:{num}{code} Tarot.png", f"{code}-{num:02d}"))
    for letter, rank in FRO.items():
        for code in ("B", "C", "P", "S"):
            items.append((f"File:{letter}{code} Tarot.png", f"{code}-{rank}"))
    return items


def visconti_cards():
    def arcan(n):
        return f"File:Bembo-Visconti-tarot-arcanum-{n}.jpg"

    items = [(arcan("fool"), "0")]
    for i in range(1, 15):
        items.append((arcan(f"{i:02d}"), i))
    # триумфи 15,16 у Morgan-наборі відсутні (Диявол, Башта) — у колоді Visconti-Sforza їх немає
    for i in range(17, 22):
        items.append((arcan(f"{i:02d}"), i))

    for suit, code in (("coins", "pentacles"), ("cups", "cups"), ("staves", "wands"), ("swords", "swords")):
        FRO1 = {"01": "01-ace", "02": "02-deuce"}
        for num in range(1, 15):
            rn = f"{num:02d}"
            if suit == "swords" and num == 3:
                continue  # у наборі немає 3 мечів
            if suit == "coins" and num == 12:
                continue  # немає лицаря монет
            if num <= 10:
                fname = rn
            else:
                fname = {"11": "11-knave", "12": "12-knight", "13": "13-queen", "14": "14-king"}[rn]
            items.append((f"File:Bembo-Visconti-tarot-{suit}-{fname}.jpg", f"{code}-{rn}"))
    return items


def download(title: str, fname: Path):
    if fname.exists():
        return True
    r = api({"action": "query", "titles": title, "prop": "imageinfo",
             "iiprop": "url|size", "iiurlwidth": 1200, "format": "json"})
    pages = (r or {}).get("query", {}).get("pages", {})
    info = None
    for page in pages.values():
        if page.get("imageinfo"):
            info = page["imageinfo"][0]
            break
    if not info:
        print("  MISS", title)
        return False
    src = info.get("thumburl") or info.get("url")
    req = urllib.request.Request(src, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 403):
                time.sleep(4 * (attempt + 1))
                continue
            raise
    else:
        return False
    fname.write_bytes(data)
    time.sleep(1.2)
    return True


def slot_name(number):
    if isinstance(number, int) and number == 0:
        return "0"
    if isinstance(number, int):
        return ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
                "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"][number]
    return number  # "wands-01" тощо


def run():
    for deck_id, builder in ((24, marseille_cards), (23, visconti_cards)):
        items = builder()
        dest = ROOT / "backend" / "Database" / "images" / str(deck_id)
        dest.mkdir(parents=True, exist_ok=True)
        pub = ROOT / "frontend" / "public" / "assets" / str(deck_id)
        pub.mkdir(parents=True, exist_ok=True)
        ok = 0
        mapping = []
        for title, number in items:
            slot = slot_name(number)
            fname = f"{slot}.jpg"
            target = dest / fname
            if download(title, target):
                ok += 1
                shutil.copy2(target, pub / fname)
            mapping.append({"file": title, "slot": slot})
            time.sleep(0.5)
        print(f"deck {deck_id}: звантажено {ok}/{len(items)}")
        (ROOT / "backend" / "Database" / f"pd_map_{deck_id}.json").write_text(
            json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    run()