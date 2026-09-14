"""fetch_pd_v3.py — download PD cards: Marseille (deck 24) + Visconti (deck 23).
Marseille: File:T{n} Tarot.png (n=1..21), TT Tarot.png (0), {1..10}{B,C,P,S} Tarot.png,
          {J,H,Q,K}{B,C,P,S} Tarot.png  (B=wands, C=cups, P=pentacles, S=swords; J=паж,H=лицар,Q=королева,K=король)
Visconti: File:Bembo-Visconti-tarot-<name>.jpg (реальні імена з категорії), + Tre di spade.jpg
Slots: старші — roman (0, I..XXI); молодші — suit-NN (wands-01 ...).
"""
import json, shutil, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, r"C:\Users\Arthur\AppData\Local\Temp\opencode")
from wm_common import api

ROOT = Path(__file__).resolve().parents[2]
UA = "Arcanum-StudyBot/1.0 (tarot database; contact: owner)"

ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]
SCODE = {"B": "wands", "C": "cups", "P": "pentacles", "S": "swords"}
CR = {"J": "11", "H": "12", "Q": "13", "K": "14"}


def marseille_items():
    items = [("File:TT Tarot.png", "0")]
    for i in range(1, 22):
        items.append((f"File:T{i} Tarot.png", ROMAN[i]))
    for code in ("B", "C", "P", "S"):
        for n in range(1, 11):
            items.append((f"File:{n}{code} Tarot.png", f"{SCODE[code]}-{n:02d}"))
    for letter, rank in CR.items():
        for code in ("B", "C", "P", "S"):
            items.append((f"File:{letter}{code} Tarot.png", f"{SCODE[code]}-{rank}"))
    return items


def visconti_items():
    AR = {
        "arcanum-fool": "0",
        "arcanum-01-magician": "1", "arcanum-02-high priestess": "2", "arcanum-03-empress": "3",
        "arcanum-04-emperor": "4", "arcanum-05-hierophant": "5", "arcanum-06-lovers": "6",
        "arcanum-07-chariot": "7", "arcanum-08-justice": "8", "arcanum-09-hermit": "9",
        "arcanum-10-wheel of fortune": "10", "arcanum-11-strength": "11", "arcanum-12-hanged man": "12",
        "arcanum-13": "13", "arcanum-14-temperance": "14",
        # no 15,16 in Morgan set
        "arcanum-17-star": "17", "arcanum-18-moon": "18", "arcanum-19-sun": "19",
        "arcanum-20-judgement": "20", "arcanum-21-world": "21",
    }
    items = [(f"File:Bembo-Visconti-tarot-{k}.jpg", ROMAN[int(v)]) for k, v in AR.items()]
    MIN = {"coins": "pentacles", "cups": "cups", "staves": "wands", "swords": "swords"}
    SUF = {1: "01-ace", 2: "02-deuce", 11: "11-knave", 12: "12-knight", 13: "13-queen", 14: "14-king"}
    skip = {"coins": {12}, "cups": {14}, "swords": {3}}  # missing files in Bembo series
    for suit, scode in MIN.items():
        for n in range(1, 15):
            if n in skip.get(suit, set()):
                continue
            fname = SUF.get(n, f"{n:02d}")
            items.append((f"File:Bembo-Visconti-tarot-{suit}-{fname}.jpg", f"{scode}-{n:02d}"))
    return items


def get_urls(titles):
    urls = {}
    for i in range(0, len(titles), 30):
        chunk = titles[i:i+30]
        ok = False
        for attempt in range(6):
            r = api({"action": "query", "titles": "|".join(chunk),
                     "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 800, "format": "json"})
            if r is None:
                time.sleep(6); continue
            ok = True
            for page in (r or {}).get("query", {}).get("pages", {}).values():
                if page.get("imageinfo"):
                    urls[page["title"]] = page["imageinfo"][0].get("thumburl") or page["imageinfo"][0]["url"]
            break
        if not ok:
            print("  fail chunk", i)
        time.sleep(2)
    return urls


def dl(url, dest):
    if dest.exists() and dest.stat().st_size > 10000:
        return True
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                dest.write_bytes(resp.read())
            return True
        except urllib.error.HTTPError as e:
            if e.code in (429, 403):
                time.sleep(8 + 6 * attempt)
                continue
            print(f"  HTTP {e.code} {dest.name}"); return False
        except Exception as e:
            print(f"  ERR {dest.name}: {e}"); time.sleep(6)
    print(f"  GIVE UP {dest.name}")
    return False


def run_deck(deck_id, items):
    dest = ROOT / "backend" / "Database" / "images" / str(deck_id)
    pub = ROOT / "frontend" / "public" / "assets" / str(deck_id)
    dest.mkdir(parents=True, exist_ok=True); pub.mkdir(parents=True, exist_ok=True)
    titles = [t for t, _ in items]
    print(f"deck {deck_id}: {len(titles)} items, запитую URL...")
    urls = get_urls(titles)
    print(f"  отримано URL: {len(urls)}")
    ok = 0
    mapping = []
    for title, slot in items:
        url = urls.get(title)
        if not url:
            print(f"  MISS {title}")
            mapping.append({"file": title, "slot": slot, "ok": False})
            continue
        target = dest / f"{slot}.jpg"
        good = dl(url, target)
        if good:
            ok += 1
        mapping.append({"file": title, "slot": slot, "ok": good})
        time.sleep(3)
    for f in dest.glob("*.jpg"):
        shutil.copy2(f, pub / f.name)
    print(f"deck {deck_id}: скачано {ok}/{len(items)}")
    (ROOT / "backend" / "Database" / f"pd_map_{deck_id}.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    run_deck(24, marseille_items())
    run_deck(23, visconti_items())