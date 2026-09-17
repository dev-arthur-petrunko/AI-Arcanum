"""cleanup_decks.py
-----------------
Безопасное удаление лишних колод из AI-Arcanum.

Удаляются:
  - 7 "придуманных" колод Таро (id 51-57): Таро Ангелів, Неоколоніальне таро
    Америк, Анімоване таро Байкаря, Таро Аліси в Країні Чудес,
    Таро Пошуку Видіння, Таро Золотого Чорного Кота, Фольклорне таро
  - 5 астрологічних оракулів-дублів (id 45-49): Ар-нуво, Астрологічний рік,
    Аркани астрології, Сяюче Сонце, Архетипічна астрологія

Остаются нетронутыми:
  - Таро: id 1 (RWS), 23 (Visconti-Sforza), 24 (Marseille)
  - Астрологія: id 50 (Астрологічний довідник, REF)
  - Все остальные 30+ систем — без изменений

ВАЖНО, с учётом инцидента с каскадным удалением из истории проекта:
  1. Скрипт СНАЧАЛА делает полную резервную копию файла БД.
  2. Затем печатает, что именно будет удалено, и требует подтверждения.
  3. Удаляет карты, потом сами колоды, в одной транзакции.
  4. В конце сверяет итоговые счётчики через прямой SELECT COUNT(*).

Запуск:
    python cleanup_decks.py            # спросит подтверждение
    python cleanup_decks.py --yes      # без вопроса (для CI/автоматизации)
    python cleanup_decks.py --dry-run  # только показать, что будет удалено
"""

import argparse
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("backend/Database/fortune_cards.db")

DECK_IDS_TO_DELETE = [
    # "Придумані" колоди Таро без реального джерела
    51, 52, 53, 54, 55, 56, 57,
    # Астрологічні оракули-дублі (структурно повторюють реальні комерційні видання)
    45, 46, 47, 48, 49,
]


def backup_db(db_path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path.with_name(f"{db_path.stem}_backup_{timestamp}{db_path.suffix}")
    shutil.copy2(db_path, backup_path)
    print(f"[OK] Резервна копія створена: {backup_path}")
    return backup_path


def fetch_summary(conn: sqlite3.Connection, deck_ids: list[int]) -> list[tuple]:
    placeholders = ",".join("?" for _ in deck_ids)
    cur = conn.execute(
        f"""
        SELECT d.id, d.name, s.name, COUNT(c.id) AS card_count
        FROM decks d
        LEFT JOIN systems s ON s.id = d.system_id
        LEFT JOIN cards c ON c.deck_id = d.id
        WHERE d.id IN ({placeholders})
        GROUP BY d.id
        ORDER BY d.id
        """,
        deck_ids,
    )
    return cur.fetchall()


def total_counts(conn: sqlite3.Connection) -> tuple[int, int]:
    decks = conn.execute("SELECT COUNT(*) FROM decks").fetchone()[0]
    cards = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
    return decks, cards


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--yes", action="store_true", help="не питати підтвердження")
    parser.add_argument("--dry-run", action="store_true", help="тільки показати, нічого не видаляти")
    args = parser.parse_args()

    if not DB_PATH.exists():
        raise SystemExit(f"Файл БД не знайдено: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    before_decks, before_cards = total_counts(conn)
    print(f"До видалення: {before_decks} колод, {before_cards} карт\n")

    rows = fetch_summary(conn, DECK_IDS_TO_DELETE)
    if not rows:
        print("Жодної з вказаних колод не знайдено в БД — нема чого видаляти.")
        return

    print("Буде видалено:")
    total_cards_to_delete = 0
    for deck_id, deck_name, system_name, card_count in rows:
        print(f"  id={deck_id:<4} {deck_name:<55} ({system_name}) — {card_count} карт")
        total_cards_to_delete += card_count
    print(f"\nРазом: {len(rows)} колод, {total_cards_to_delete} карт.\n")

    if args.dry_run:
        print("[DRY-RUN] Нічого не видалено — це був лише перегляд.")
        conn.close()
        return

    if not args.yes:
        answer = input("Підтвердити видалення? Це незворотньо (yes/no): ").strip().lower()
        if answer not in ("yes", "y", "так"):
            print("Скасовано користувачем.")
            conn.close()
            return

    backup_db(DB_PATH)

    placeholders = ",".join("?" for _ in DECK_IDS_TO_DELETE)
    try:
        with conn:
            conn.execute(f"DELETE FROM cards WHERE deck_id IN ({placeholders})", DECK_IDS_TO_DELETE)
            conn.execute(f"DELETE FROM decks WHERE id IN ({placeholders})", DECK_IDS_TO_DELETE)
        print("[OK] Видалення виконано в межах однієї транзакції.")
    except sqlite3.Error as e:
        print(f"[ПОМИЛКА] Транзакція відкочена: {e}")
        conn.close()
        raise SystemExit(1)

    after_decks, after_cards = total_counts(conn)
    expected_decks = before_decks - len(rows)
    expected_cards = before_cards - total_cards_to_delete

    print(f"\nПісля видалення: {after_decks} колод, {after_cards} карт")
    print(f"Очікувалось:      {expected_decks} колод, {expected_cards} карт")

    if (after_decks, after_cards) == (expected_decks, expected_cards):
        print("[OK] Лічильники сходяться — видалення пройшло коректно.")
    else:
        print("[УВАГА] Лічильники НЕ сходяться! Перевірте вручну або відновіть з бекапу.")

    conn.close()


if __name__ == "__main__":
    main()