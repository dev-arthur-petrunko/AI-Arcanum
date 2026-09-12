# Статьи энциклопедии

Формат файла: markdown с front-matter:
```md
---
slug: tarot-history
title: Краткая история Таро
system: Таро
lang: ru
source_reference: собственные материалы + Waite (1911), public domain
translations:
  uk: { title: "Коротка історія Таро" }
  en: { title: "A brief history of Tarot" }
---

Текст статьи…
```

Импорт в БД (таблица `articles`, endpoint `GET /articles`):
```powershell
python scripts/seed_articles.py
```
