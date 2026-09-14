"""cut_game_of_hope.py — разовий скрипт: ріже аркуш Das Spiel der Hofnung (1799, PD)
6×6 на 36 карт Ленорман (порядок рядками 1–36, як у колоді).
Джерело: Wikimedia Commons (Public domain, 1799).
Запуск з папки backend/: python scripts/cut_game_of_hope.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image, ImageStat

SRC = Path(__file__).resolve().parents[1] / "Database" / "raw" / "lenormand" / "game_of_hope_1799.png"
DB_IMG = Path(__file__).resolve().parents[1] / "Database" / "images" / "02"
PUB = Path(__file__).resolve().parents[2] / "frontend" / "public" / "assets" / "02"

import sys as _s
_sys = _s
_sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def find_gutters(lengths, n_inner, axis_len):
    """Шукає n_inner світлих смуг-розділювачів за профілем яскравості."""
    runs, in_run, start = [], False, 0
    for i, v in enumerate(lengths):
        if v > 238 and not in_run:
            in_run, start = True, i
        elif v <= 238 and in_run:
            in_run = False
            runs.append((start, i))
    if in_run:
        runs.append((start, len(lengths)))
    runs = [(a, b) for a, b in runs if b - a >= 4]
    # відкидаємо крайові поля: беремо n_inner внутрішніх
    inner = sorted(runs, key=lambda r: r[1] - r[0], reverse=True)
    inner = [r for r in inner if 0 < r[0] and r[1] < axis_len - 1]
    inner = sorted(inner[:n_inner])
    assert len(inner) == n_inner, f"знайдено розділювачів: {len(inner)}, треба {n_inner}"
    return [(a + b) // 2 for a, b in inner]


def run():
    img = Image.open(SRC).convert("RGB")
    W, H = img.size
    print(f"аркуш: {W}x{H}")
    small = img.resize((650, 817)).convert("L")
    px = small.load()
    col_mean = [sum(px[x, y] for y in range(817)) / 817 for x in range(650)]
    row_mean = [sum(px[x, y] for x in range(650)) / 650 for y in range(817)]
    vxs = find_gutters(col_mean, 5, 650)
    hys = find_gutters(row_mean, 5, 817)
    sx, sy = W / 650, H / 817
    xs = [0] + [int(x * sx) for x in vxs] + [W]
    ys = [0] + [int(y * sy) for y in hys] + [H]
    DB_IMG.mkdir(parents=True, exist_ok=True)
    PUB.mkdir(parents=True, exist_ok=True)
    k = 0
    for r in range(6):
        for c_ in range(6):
            k += 1
            cell = img.crop((xs[c_] + 6, ys[r] + 6, xs[c_ + 1] - 6, ys[r + 1] - 6))
            dest = DB_IMG / f"{k}.jpg"
            cell.save(dest, quality=88)
            cell.resize((512, int(512 * cell.height / cell.width))).save(PUB / f"{k}.jpg", quality=74)
    print(f"нарізано: {k} карт")


if __name__ == "__main__":
    run()
