"""seed_articles.py — імпорт Database/articles/*.md (front-matter → таблиця articles).
Ідемпотентний (за slug). Запуск з папки backend/: python scripts/seed_articles.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Article

ART_DIR = Path(__file__).resolve().parents[1] / "Database" / "articles"


def parse_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path.name}: немає front-matter")
    meta_raw, body = m.group(1), m.group(2).strip()
    meta: dict = {}
    trans: dict = {}
    for line in meta_raw.splitlines():
        if re.match(r"\s+\w", line) and ":" in line and "translations" in meta_raw:
            mm = re.match(r"\s*(\w+):\s*\{\s*title:\s*\"?([^\",}]+)\"?", line)
            if mm:
                trans.setdefault(mm.group(1), {})["title"] = mm.group(2).strip()
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    if trans:
        meta["translations"] = trans
    meta["body"] = body
    return meta


def run() -> int:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    n = 0
    try:
        for path in sorted(ART_DIR.glob("*.md")):
            if path.name == "README.md":
                continue
            meta = parse_md(path)
            art = db.query(Article).filter_by(slug=meta["slug"]).first()
            if art:
                art.title = meta.get("title", art.title)
                art.body = meta.get("body", art.body)
                art.system = meta.get("system", art.system)
                art.source_reference = meta.get("source_reference", art.source_reference)
                art.translations = meta.get("translations", art.translations)
            else:
                db.add(Article(slug=meta["slug"], title=meta.get("title", meta["slug"]),
                               system=meta.get("system"), lang=meta.get("lang", "ru"),
                               body=meta.get("body", ""),
                               source_reference=meta.get("source_reference"),
                               translations=meta.get("translations")))
                n += 1
        db.commit()
        print(f"[articles] нових: {n}, всього: {db.query(Article).count()}")
        return n
    finally:
        db.close()


if __name__ == "__main__":
    run()
