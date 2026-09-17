"""Видалення 5 осиротілих systems (34-38) після cleanup_decks.py.
Колоди 45-49 вже видалено; лишились systems без жодної колоди:
  34 Астрологія · Ар-нуво, 35 Астрологічний рік, 36 Аркани астрології,
  37 Сяюче Сонце, 38 Архетипічна астрологія.
Безпека: бекап → перевірка 0 decks/0 cards/0 spreads → DELETE → звірка лічильників.
"""
import argparse
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("Database/fortune_cards.db")
ORPHAN_IDS = [34, 35, 36, 37, 38]

parser = argparse.ArgumentParser()
parser.add_argument("--yes", action="store_true")
args = parser.parse_args()

assert DB_PATH.exists(), f"нема БД: {DB_PATH}"
con = sqlite3.connect(DB_PATH)
con.execute("PRAGMA foreign_keys = ON")

print("Перевірка сиріт:")
for i in ORPHAN_IDS:
    s = con.execute("SELECT id, name, category FROM systems WHERE id=?", (i,)).fetchone()
    nd = con.execute("SELECT COUNT(*) FROM decks WHERE system_id=?", (i,)).fetchone()[0]
    nc = con.execute(
        "SELECT COUNT(*) FROM cards WHERE deck_id IN (SELECT id FROM decks WHERE system_id=?)", (i,)
    ).fetchone()[0]
    ns = con.execute("SELECT COUNT(*) FROM spreads WHERE system_id=?", (i,)).fetchone()[0]
    print(f"  id={i} {s} decks={nd} cards={nc} spreads={ns}")
    assert s is not None, f"system {i} вже відсутня"
    assert (nd, nc, ns) == (0, 0, 0), f"system {i} НЕ сирота — стоп!"

before = con.execute("SELECT COUNT(*) FROM systems").fetchone()[0]
print(f"systems до: {before}")
if not args.yes:
    ans = input("Видалити 5 сиріт? (yes/no): ").strip().lower()
    if ans not in ("yes", "y", "так"):
        print("Скасовано.")
        raise SystemExit(0)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
bak = DB_PATH.with_name(f"{DB_PATH.stem}_backup_{ts}{DB_PATH.suffix}")
shutil.copy2(DB_PATH, bak)
print(f"[OK] бекап: {bak}")

with con:
    con.execute(f"DELETE FROM systems WHERE id IN ({','.join('?' for _ in ORPHAN_IDS)})", ORPHAN_IDS)

after = con.execute("SELECT COUNT(*) FROM systems").fetchone()[0]
left = con.execute(f"SELECT id FROM systems WHERE id IN ({','.join('?' for _ in ORPHAN_IDS)})", ORPHAN_IDS).fetchall()
print(f"systems після: {after} (очікувалось {before - 5}), залишки ids: {left}")
assert after == before - 5 and not left, "Лічильники не зійшлись!"
print("[OK] 5 сиріт видалено.")
con.close()
