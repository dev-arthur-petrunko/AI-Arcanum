"""seed_articles.py — імпорт Database/articles/*.md (front-matter → таблиця articles).
Ідемпотентний (за slug). Конвенція переводів тіла: файли {slug}.{lang}.md
з front-matter `link: <slug>` — вони додають translations[lang] = {title, body}
до базової статті (slug без суфікса). Запуск з папки backend/: python scripts/seed_articles.py
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.models import Article

ART_DIR = Path(__file__).resolve().parents[1] / "Database" / "articles"

LANG_SUFFIX = re.compile(r"^(.*)\.(uk|en|ru)\.md$")
LINK_RE = re.compile(r"^link\s*:\s*(.+)$")


def parse_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path.name}: немає front-matter")
    meta_raw, body = m.group(1), m.group(2).strip()
    meta: dict = {}
    for line in meta_raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    meta["body"] = body
    return meta


def run() -> int:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    n = 0
    try:
        files = sorted(ART_DIR.glob("*.md"))
        base_files = [p for p in files if not LANG_SUFFIX.match(p.name) and p.name != "README.md"]
        trans_files = [(LANG_SUFFIX.match(p.name), p) for p in files if LANG_SUFFIX.match(p.name)]

        # спочатку базові статті
        for path in base_files:
            meta = parse_md(path)
            art = db.query(Article).filter_by(slug=meta["slug"]).first()
            if art:
                art.title = meta.get("title", art.title)
                art.body = meta.get("body", art.body)
                art.system = meta.get("system", art.system)
                art.source_reference = meta.get("source_reference", art.source_reference)
            else:
                db.add(Article(slug=meta["slug"], title=meta.get("title", meta["slug"]),
                               system=meta.get("system"),
                               lang=meta.get("lang", "ru"), body=meta.get("body", ""),
                               source_reference=meta.get("source_reference")))
                n += 1
        db.flush()  # базові статті мають бути видні до обробки файлів-перекладів

        # потім файли-переклади: зливаємо title+body у translations
        for match, path in trans_files:
            slug, lang = match.group(1), match.group(2)
            meta = parse_md(path)
            link = (meta.get("link") or "").strip() or slug
            art = db.query(Article).filter_by(slug=link).first()
            if not art:
                print(f"[articles] !! немає базової статті для {path.name} (link={link})")
                continue
            tr = dict(art.translations or {})
            tr[lang] = {"title": meta.get("title", art.title), "body": meta.get("body", "")}
            art.translations = tr

        db.commit()
        print(f"[articles] нових: {n}, всього: {db.query(Article).count()}")
        return n
    finally:
        db.close()


if __name__ == "__main__":
    run()