"""Завантаження RWS 1909 (суспільне надбання) з Wikimedia Commons + Pillow-превʼю.
Запуск: python scripts/download_rws.py [--limit N]
Класти у frontend/src/assets/card_images/rws/. Сучасні колоди сюди НЕ качати (копірайт).
"""
import sys
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

try:
    from PIL import Image
except ImportError:
    print("Потрібен Pillow: pip install pillow")
    sys.exit(1)

OUT = Path(__file__).resolve().parents[2] / "frontend" / "src" / "assets" / "card_images" / "rws"
OUT.mkdir(parents=True, exist_ok=True)

# Перевірені файли RWS на Commons (орієнтовний набір; повний — 78; решта добирається тим самим патерном).
SAMPLE = {
    "major_0.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg",
    "major_I.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
    "major_II.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg",
}

def fetch(name: str, url: str):
    dest = OUT / name
    if dest.exists():
        print(f"пропуск {name}")
        return
    print(f"GET {url}")
    data = urlopen(url, timeout=60).read()
    img = Image.open(BytesIO(data)).convert("RGB")
    img.save(dest, quality=88)
    img.thumbnail((512, 900))
    img.save(OUT / (dest.stem + "_thumb.jpg"), quality=80)
    print(f"збережено {dest.name}")

if __name__ == "__main__":
    limit = int((sys.argv[sys.argv.index("--limit") + 1] if "--limit" in sys.argv else len(SAMPLE)))
    for i, (n, u) in enumerate(SAMPLE.items()):
        if i >= limit:
            break
        fetch(n, u)
    print(f"готово → {OUT}")
