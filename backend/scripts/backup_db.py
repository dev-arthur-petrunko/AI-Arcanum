"""backup_db.py — копія БД перед будь-яким скриптом міграції/злиття.
Урок інциденту 2026-09-12 (каскад видалив колоду): бекап — перший крок.
Запуск з папки backend/: python scripts/backup_db.py [--note текст]
"""
import datetime
import shutil
import sys
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "Database" / "fortune_cards.db"
BACKUPS = DB.parent / "backups"


def main(note: str = "") -> Path | None:
    if not DB.exists():
        print(f"[backup] БД нема: {DB} — нема чого копіювати")
        return None
    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"_{note}" if note else ""
    dest = BACKUPS / f"fortune_cards_{stamp}{suffix}.db"
    shutil.copy2(DB, dest)
    # тримаємо останні 10 копій
    olds = sorted(BACKUPS.glob("fortune_cards_*.db"))
    for old in olds[:-10]:
        old.unlink()
    print(f"[backup] {dest} ({dest.stat().st_size // 1024} KB)")
    return dest


if __name__ == "__main__":
    main(sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--note" else "")
