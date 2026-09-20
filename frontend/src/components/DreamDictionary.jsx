"use client";
import { useEffect, useMemo, useState } from "react";
import SiteNav from "./SiteNav";
import Reveal from "./Reveal";
import { DREAMS, ALPHABETS } from "../lib/dreams";

const T = {
  ru: {
    search: "Найти символ или слово…",
    all: "Все",
    symbols: "символов",
    noResults: "По этому запросу в соннике ничего не найдено.",
    alphabet: "Алфавит",
    hint: "Выбери букву, чтобы сузить список, или воспользуйся поиском. Клик по карточке раскрывает толкование.",
    cards: "Значения карт", practice: "Практика", guides: "Гайды",
    back: "← Все направления",
    deckLink: "Карты-символы сонника →",
    deckSub: "50 навчальних карт-символів: інший погляд на ті самі образи.",
    keywords: "ключи",
    copy: "Дивись на сни як на тихий голос власних почуттів: вони рідко передрікають — вони відображають.",
  },
  uk: {
    search: "Знайти символ або слово…",
    all: "Усі",
    symbols: "символів",
    noResults: "За цим запитом у соннику нічого не знайдено.",
    alphabet: "Абетка",
    hint: "Обери букву, щоб звузити список, або скористайся пошуком. Клік по картці розкриває тлумачення.",
    cards: "Значення карт", practice: "Практика", guides: "Гайди",
    back: "← Усі напрямки",
    deckLink: "Карти-символи сонника →",
    deckSub: "50 навчальних карт-символів: інший погляд на ті самі образи.",
    keywords: "ключі",
    copy: "Дивись на сни як на тихий голос власних почуттів: вони рідко передрікають — вони відображають.",
  },
  en: {
    search: "Find a symbol or word…",
    all: "All",
    symbols: "symbols",
    noResults: "Nothing found in the dream dictionary for this query.",
    alphabet: "Alphabet",
    hint: "Pick a letter to narrow the list, or use search. Click a card to reveal the meaning.",
    cards: "Card meanings", practice: "Practice", guides: "Guides",
    back: "← All directions",
    deckLink: "Dream symbol cards →",
    deckSub: "50 learning symbol cards: another take on the same images.",
    keywords: "keys",
    copy: "See dreams as the quiet voice of your own feelings: they rarely predict — they reflect.",
  },
};

/** Сонник · алфавітний словник символів (навчальна модель).
 *  Дані — з БД (дек 52) через SSR, фолбек на статичний масив `lib/dreams`. */
export default function DreamDictionary({ direction, symbols = null }) {
  const [lang, setLang] = useState("ru");
  const [theme, setTheme] = useState("dark");
  const [query, setQuery] = useState("");
  const [letter, setLetter] = useState(null);
  const t = T[lang] || T.ui;

  useEffect(() => {
    try {
      const saved = localStorage.getItem("arcanum-theme");
      if (saved === "light" || saved === "dark") {
        setTheme(saved);
        document.documentElement.dataset.theme = saved;
      }
    } catch {}
  }, []);

  function toggleTheme() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    try {
      localStorage.setItem("arcanum-theme", next);
      document.documentElement.dataset.theme = next;
    } catch {}
  }

  const source = useMemo(() => (symbols && symbols.length > 0 ? symbols : DREAMS), [symbols]);

  // алфавіт мови + які літери реально присутні в даних
  const { letters, groups } = useMemo(() => {
    const abc = (ALPHABETS[lang] || ALPHABETS.uk).split("");
    const used = new Set(source.map((s) => (s.name[lang] || s.name.uk).charAt(0).toUpperCase()));
    const letters = abc.filter((ch) => used.has(ch));
    const groups = letters.map((ch) => ({
      ch,
      items: source.filter((s) => (s.name[lang] || s.name.uk).charAt(0).toUpperCase() === ch),
    }));
    return { letters, groups };
  }, [lang, source]);

  // пошук по імені, ключах і тексту поточною мовою
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return null;
    return groups
      .map((g) => ({
        ch: g.ch,
        items: g.items.filter((s) => {
          const v = s.name[lang] || s.name.uk;
          const k = s.keywords[lang] || s.keywords.uk;
          const x = s.text[lang] || s.text.uk;
          return v.toLowerCase().includes(q)
            || k.toLowerCase().includes(q)
            || x.toLowerCase().includes(q);
        }),
      }))
      .filter((g) => g.items.length > 0);
  }, [query, lang, groups]);

  function pickLetter(ch) {
    setLetter((prev) => (prev === ch ? null : ch));
  }

  const list = query.trim() ? filtered : (letter ? groups.filter((g) => g.ch === letter) : groups);
  const count = source.length;

  return (
    <>
      <SiteNav lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} />
      <main className="wrap" style={{ paddingTop: 110, paddingBottom: 60 }}>
        <div className="crumbs">
          <a href="/">{lang === "en" ? "Home" : lang === "ru" ? "Главная" : "Головна"}</a>
          <span>›</span>
          <span>{direction.title[lang] || direction.title.uk}</span>
        </div>

        <header className="page-hero sparkle-field" style={{ padding: "34px 30px", marginBottom: 6 }}>
          <span style={{ fontSize: 40 }}>{direction.icon}</span>
          <h1 style={{ margin: "10px 0 6px", fontSize: "clamp(34px, 5vw, 56px)" }}>
            {direction.title[lang] || direction.title.uk}
          </h1>
          <p style={{ color: "var(--muted)", maxWidth: 680, lineHeight: 1.65 }}>
            {direction.desc[lang] || direction.desc.uk}
          </p>
          <p style={{ color: "var(--gold-soft)", fontSize: 14 }}>
            {count} · {t.symbols} · {letters.length} · {t.alphabet.toLowerCase()}
          </p>
        </header>

        <nav className="dir-tabs" aria-label={direction.title.uk}>
          <a href={`/directions/${direction.slug}`} className="active">{t.cards}</a>
          <a href={`/directions/${direction.slug}/spreads`}>{t.practice}</a>
          <a href={`/directions/${direction.slug}/guides`}>{t.guides}</a>
        </nav>

        <Reveal>
          <section className="section" style={{ paddingTop: 20 }}>
            <div className="section-head">
              <span className="num">✦</span>
              <div><h2>{t.alphabet}</h2><p>{t.hint}</p></div>
            </div>

            <div style={{ marginBottom: 16 }}>
              <input
                type="search"
                placeholder={t.search}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                style={{ width: "100%", maxWidth: 420, padding: "12px 16px", borderRadius: 12,
                  border: "1px solid var(--line)", background: "var(--panel)", color: "var(--text)" }}
              />
            </div>

            <div className="chips" style={{ marginBottom: 4 }}>
              <button type="button" className={`chip${letter === null && !query ? " active" : ""}`}
                onClick={() => { setLetter(null); setQuery(""); }} style={{ cursor: "pointer" }}>
                {t.all}
              </button>
              {letters.map((ch) => (
                <button key={ch} type="button"
                  className={`chip${letter === ch && !query ? " active" : ""}`}
                  onClick={() => pickLetter(ch)} style={{ cursor: "pointer" }}>
                  {ch}
                </button>
              ))}
            </div>

            {(list || []).map((g) => (
              <div key={g.ch} style={{ marginTop: 22 }}>
                <h3 style={{ color: "var(--gold-soft)", fontSize: 20, margin: "0 0 12px" }}>
                  {g.ch} <span style={{ color: "var(--muted)", fontSize: 13 }}>· {g.items.length}</span>
                </h3>
                {g.items.map((s) => (
                  <details key={s.id} className="article-card" style={{ padding: 0 }}>
                    <summary>
                      <span style={{ display: "flex", gap: 14, alignItems: "center" }}>
                        <span style={{ fontSize: 24 }}>{s.icon}</span>
                        <span>
                          <b>{s.name[lang] || s.name.uk}</b>
                          <span className="sys" style={{ display: "block", marginTop: 4 }}>
                            {t.keywords} · {s.keywords[lang] || s.keywords.uk}
                          </span>
                        </span>
                      </span>
                    </summary>
                    <div className="article-body">
                      <span style={{ fontSize: 15, fontStyle: "italic", color: "var(--gold-soft)" }}>
                        {s.name.en}
                      </span>
                      <br /><br />
                      {s.text[lang] || s.text.uk}
                    </div>
                  </details>
                ))}
              </div>
            ))}

            {(!list || list.length === 0) && (
              <p style={{ color: "var(--muted)", marginTop: 24 }}>{t.noResults}</p>
            )}

            <p style={{ marginTop: 22, color: "var(--muted)", fontSize: 14, fontStyle: "italic" }}>
              {t.copy}
            </p>
          </section>
        </Reveal>

        <Reveal>
          <div className="divider">✦ ✦ ✦</div>
          <section className="section">
            <div className="section-head">
              <span className="num">🃏</span>
              <div><h2>{t.deckLink}</h2><p>{t.deckSub}</p></div>
            </div>
            <p style={{ marginTop: 6 }}>
              <a className="btn btn-ghost" href="/decks/52" style={{ display: "inline-block" }}>{t.deckLink}</a>
              <a className="btn btn-ghost" href="/" style={{ display: "inline-block", marginLeft: 10 }}>{t.back}</a>
            </p>
          </section>
        </Reveal>
      </main>
      <footer className="footer">
        <div className="wrap"><span>✦ AI-Arcanum · {direction.title[lang] || direction.title.uk}</span></div>
      </footer>
    </>
  );
}