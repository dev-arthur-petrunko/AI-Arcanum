# -*- coding: utf-8 -*-
"""gen_astro_articles.py — генерує Database/articles/05-*.md (астрологічні статті)
з data-модуля scripts/astro_data.py у форматі seed_articles.py:
  • базовий файл — front-matter slug/title/system/lang + тіло (ru);
  • файли-переклади {slug}.uk.md / {slug}.en.md — front-matter link: <slug> + тіло.
Ідемпотентний (переписує). Запуск: python scripts/gen_astro_articles.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from astro_data import ASTRO  # scripts/ на шляху

ART_DIR = ROOT / "Database" / "articles"


def gen() -> int:
    n = 0
    for i, (slug, d) in enumerate(ASTRO.items(), start=5):
        base = ART_DIR / f"{i:02d}-{slug}.md"
        glyph, ru = d["glyph"], d["ru"]
        s = f"""---
slug: {slug}
title: {ru["title"]}
system: Астрология
lang: ru
source_reference: собственная учебная энциклопедия по мотивам Astro.com и Cafe Astrology
---

{glyph} {ru["body"]}
"""
        base.write_text(s, encoding="utf-8")
        for lg in ("uk", "en"):
            tr = d[lg]
            p = ART_DIR / f"{i:02d}-{slug}.{lg}.md"
            p.write_text(
                f"""---
slug: {slug}
title: {tr["title"]}
lang: {lg}
link: {slug}
---

{glyph} {tr["body"]}
""",
                encoding="utf-8",
            )
        n += 1
    print(f"[astro] згенеровано статей: {n}")
    return n


if __name__ == "__main__":
    gen()