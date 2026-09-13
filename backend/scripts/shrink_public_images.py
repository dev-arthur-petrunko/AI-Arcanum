"""shrink_public_images.py — разовий скрипт: стискає скани для вебу у frontend/public
(ширина 600px, quality 70), повний архів у backend/Database/images НЕ чіпає.
Запуск з папки backend/: python scripts/shrink_public_images.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image

PUB = Path(__file__).resolve().parents[2] / "frontend" / "public" / "assets" / "card_images" / "rws"


def run(width: int = 600, quality: int = 70) -> None:
    files = sorted(PUB.glob("*.jpg"))
    for f in files:
        img = Image.open(f).convert("RGB")
        if img.width > width:
            img = img.resize((width, int(img.height * width / img.width)), Image.LANCZOS)
        img.save(f, quality=quality, optimize=True)
    total = sum(f.stat().st_size for f in PUB.glob("*.jpg")) / 1024 / 1024
    print(f"Стиснуто: {len(files)} файлів, разом {total:.1f} MB")


if __name__ == "__main__":
    run()
