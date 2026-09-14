"""fetch_pd_v2.py — batch download PD cards from Wikimedia Commons.
Strategy: get thumburl for all titles in one API call, then download with delays."""
import json, shutil, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, r"C:\Users\Arthur\AppData\Local\Temp\opencode")
from wm_common import api
ROOT = Path(__file__).resolve().parents[2]
UA = "Arcanum-StudyBot/1.0 (tarot database; contact: owner)"


def get_thumb_urls(titles: list[str], batch=40) -> dict[str, str]:
    """Return {title: thumburl} for all titles via batched API calls."""
    urls = {}
    for i in range(0, len(titles), batch):
        chunk = titles[i:i+batch]
        r = api({"action": "query", "titles": "|".join(chunk),
                 "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 1200,
                 "format": "json"})
        for page in (r or {}).get("query", {}).get("pages", {}).values():
            if page.get("imageinfo"):
                urls[page["title"]] = page["imageinfo"][0].get("thumburl") or page["imageinfo"][0]["url"]
        time.sleep(1.5)
    return urls


def dl(url: str, dest: Path) -> bool:
    if dest.exists():
        return True
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            dest.write_bytes(resp.read())
        return True
    except Exception as e:
        print(f"  ERR {dest.name}: {e}")
        return False


def run():
    # ---------- MARSEILLE (deck 24) ----------
    罗马 = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
           "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]
    MM2 = []
    MM2.append(("File:TT Tarot.png", "0"))
    for i in range(1, 22):
        MM2.append((f"File:T{i} Tarot.png", 罗马[i]))
    SCODE = {"B": "wands", "C": "cups", "P": "pentacles", "S": "swords"}
    for code in ("B", "C", "P", "S"):
        for num in range(1, 11):
            MM2.append((f"File:{num}{code} Tarot.png", f"{SCODE[code]}-{num:02d}"))
    CRANK = {"J": "11", "H": "12", "Q": "13", "K": "14"}
    for letter, rank in CRANK.items():
        for code in ("B", "C", "P", "S"):
            MM2.append((f"File:{letter}{code} Tarot.png", f"{SCODE[code]}-{rank}"))

    titles = [t for t, _ in MM2]
    print(f"Marseille: запитую URL для {len(titles)} файлів...")
    url_map = get_thumb_urls(titles)
    print(f"  отримано URL: {len(url_map)}")
    dest24 = ROOT / "backend" / "Database" / "images" / "24"
    dest24.mkdir(parents=True, exist_ok=True)
    ok24 = 0
    mapping24 = []
    for title, slot in MM2:
        url = url_map.get(title)
        if not url:
            print(f"  MISS {title}")
            mapping24.append({"file": title, "slot": slot, "ok": False})
            continue
        target = dest24 / f"{slot}.jpg"
        if dl(url, target):
            ok24 += 1
            mapping24.append({"file": title, "slot": slot, "ok": True})
        time.sleep(3)
    # copy to frontend
    pub24 = ROOT / "frontend" / "public" / "assets" / "24"
    pub24.mkdir(parents=True, exist_ok=True)
    for f in dest24.glob("*.jpg"):
        shutil.copy2(f, pub24 / f.name)
    print(f"Marseille: скачано {ok24}/{len(MM2)}")

    # ---------- VISCONTI (deck 23) ----------
    V23 = []
    V23.append(("File:Bembo-Visconti-tarot-arcanum-fool.jpg", "0"))
    for i in range(1, 15):
        V23.append((f"File:Bembo-Visconti-tarot-arcanum-{i:02d}.jpg", str(i)))
    for i in range(17, 22):
        V23.append((f"File:Bembo-Visconti-tarot-arcanum-{i:02d}.jpg", str(i)))
    MIN23 = {"coins": "pentacles", "cups": "cups", "staves": "wands", "swords": "swords"}
    for suit, scode in MIN23.items():
        for num in range(1, 15):
            rn = f"{num:02d}"
            if suit == "swords" and num == 3:
                continue
            if suit == "coins" and num == 12:
                continue
            if num <= 10:
                fname = rn
            else:
                fname = {11: "11-knave", 12: "12-knight", 13: "13-queen", 14: "14-king"}[num]
            V23.append((f"File:Bembo-Visconti-tarot-{suit}-{fname}.jpg", f"{scode}-{rn}"))
    titles23 = [t for t, _ in V23]
    print(f"\nVisconti: запитую URL для {len(titles23)} файлів...")
    url_map23 = get_thumb_urls(titles23)
    print(f"  отримано URL: {len(url_map23)}")
    dest23 = ROOT / "backend" / "Database" / "images" / "23"
    dest23.mkdir(parents=True, exist_ok=True)
    ok23 = 0
    for title, slot in V23:
        url = url_map23.get(title)
        if not url:
            print(f"  MISS {title}")
            continue
        if dl(url, dest23 / f"{slot}.jpg"):
            ok23 += 1
        time.sleep(3)
    pub23 = ROOT / "frontend" / "public" / "assets" / "23"
    pub23.mkdir(parents=True, exist_ok=True)
    for f in dest23.glob("*.jpg"):
        shutil.copy2(f, pub23 / f.name)
    print(f"Visconti: скачано {ok23}/{len(V23)}")

    # save mappings
    ROOT / "backend" / "Database" / "pd_map_24.json"
    Path(ROOT / "backend" / "Database" / "pd_map_24.json").write_text(
        json.dumps(mapping24, ensure_ascii=False, indent=1), encoding="utf-8")
    Path(ROOT / "backend" / "Database" / "pd_map_23.json").write_text(
        json.dumps(V23, ensure_ascii=False, indent=1), encoding="utf-8")
    print("mapping збережено.")


if __name__ == "__main__":
    run()