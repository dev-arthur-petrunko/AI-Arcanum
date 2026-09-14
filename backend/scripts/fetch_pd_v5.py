"""fetch_pd_v5.py — download PD cards with 500px thumbs + long pauses.
Usage: python fetch_pd_v5.py 24 [max_new] | 23 [max_new]
"""
import json, shutil, sys, time, urllib.error, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = "Arcanum-StudyBot/1.0 (tarot database; contact: owner)"
ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]
SCODE = {"B": "wands", "C": "cups", "P": "pentacles", "S": "swords"}
CR = {"J": "11", "H": "12", "Q": "13", "K": "14"}


def api(params, retries=10, base=3):
    params = dict(params, format="json")
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for a in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 403):
                time.sleep(base * (a + 1))
                continue
            raise
        except Exception:
            time.sleep(4)
            continue
    return None


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
        "arcanum-fool": "0", "arcanum-01-magician": "1", "arcanum-02-high priestess": "2",
        "arcanum-03-empress": "3", "arcanum-04-emperor": "4", "arcanum-05-hierophant": "5",
        "arcanum-06-lovers": "6", "arcanum-07-chariot": "7", "arcanum-08-justice": "8",
        "arcanum-09-hermit": "9", "arcanum-10-wheel of fortune": "10", "arcanum-11-strength": "11",
        "arcanum-12-hanged man": "12", "arcanum-13": "13", "arcanum-14-temperance": "14",
        "arcanum-17-star": "17", "arcanum-18-moon": "18", "arcanum-19-sun": "19",
        "arcanum-20-judgement": "20", "arcanum-21-world": "21",
    }
    items = [(f"File:Bembo-Visconti-tarot-{k}.jpg", ROMAN[int(v)]) for k, v in AR.items()]
    MIN = {"coins": "pentacles", "cups": "cups", "staves": "wands", "swords": "swords"}
    SUF = {1: "01-ace", 2: "02-deuce", 11: "11-knave", 12: "12-knight", 13: "13-queen", 14: "14-king"}
    skip = {"coins": {12}, "cups": {14}, "swords": {3}}
    for suit, scode in MIN.items():
        for n in range(1, 15):
            if n in skip.get(suit, set()):
                continue
            fname = SUF.get(n, f"{n:02d}")
            items.append((f"File:Bembo-Visconti-tarot-{suit}-{fname}.jpg", f"{scode}-{n:02d}"))
    return items


def get_all_urls(items):
    """Fetch thumburl for each file via batched API (30 titles/call)."""
    urls = {}
    titles = [t for t, _ in items]
    for i in range(0, len(titles), 30):
        chunk = titles[i:i+30]
        r = api({"action": "query", "titles": "|".join(chunk), "prop": "imageinfo",
                 "iiprop": "url", "iiurlwidth": 500, "format": "json"})
        if not r:
            print("  батч fail", i)
            continue
        for page in r.get("query", {}).get("pages", {}).values():
            if page.get("imageinfo"):
                urls[page["title"]] = page["imageinfo"][0].get("thumburl") or page["imageinfo"][0]["url"]
        time.sleep(3)
    return urls


def dl(url, dest):
    if dest.exists() and dest.stat().st_size > 10000:
        return True
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                dest.write_bytes(resp.read())
            return True
        except urllib.error.HTTPError as e:
            if e.code in (429, 403):
                time.sleep(10 + 8 * attempt)
                continue
            print(f"  HTTP {e.code} {dest.name}"); return False
        except Exception as e:
            print(f"  ERR {dest.name}: {e}"); time.sleep(6)
    print(f"  GIVE UP {dest.name}")
    return False


def run(deck_id, max_new):
    fetch = marseille_items if deck_id == 24 else visconti_items
    items = fetch()
    dest = ROOT / "backend" / "Database" / "images" / str(deck_id)
    pub = ROOT / "frontend" / "public" / "assets" / str(deck_id)
    dest.mkdir(parents=True, exist_ok=True); pub.mkdir(parents=True, exist_ok=True)
    cache = ROOT / "backend" / "Database" / f"pd_urls_{deck_id}.json"
    if cache.exists():
        urls = json.loads(cache.read_text(encoding="utf-8"))
        print(f"URL-кеш завантажено: {len(urls)}")
    else:
        print("Отримую URL...")
        urls = get_all_urls(items)
        cache.write_text(json.dumps(urls, ensure_ascii=False), encoding="utf-8")
        print(f"URL отримано: {len(urls)}")

    new = 0
    done = 0
    results = []
    for title, slot in items:
        target = dest / f"{slot}.jpg"
        if target.exists() and target.stat().st_size > 10000:
            done += 1
            results.append({"file": title, "slot": slot, "ok": True})
            continue
        url = urls.get(title)
        if not url:
            print(f"  NO URL {title}")
            results.append({"file": title, "slot": slot, "ok": False})
            continue
        if dl(url, target):
            new += 1
            done += 1
            results.append({"file": title, "slot": slot, "ok": True})
            print(f"  + {slot} ({done}/{len(items)})", flush=True)
        else:
            results.append({"file": title, "slot": slot, "ok": False})
        if new >= max_new:
            break
    for f in dest.glob("*.jpg"):
        shutil.copy2(f, pub / f.name)
    (ROOT / "backend" / "Database" / f"pd_map_{deck_id}.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"deck {deck_id}: готово {done}/{len(items)} (новий: {new})", flush=True)


if __name__ == "__main__":
    deck_id = int(sys.argv[1])
    max_new = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    run(deck_id, max_new)