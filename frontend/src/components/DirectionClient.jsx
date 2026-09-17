"use client";
import { useEffect, useState } from "react";
import SiteNav from "./SiteNav";
import Reveal from "./Reveal";
import Scene3D from "./Scene3D";
import { getJSON } from "../lib/api";

const T = {
  ru: {
    cards: "Значения карт", practice: "Практика", guides: "Гайды",
    decks: "Колоды направления", decksSub: "Клик ведёт на 3D-витрину колоды.",
    showcase: "3D-витрина", showcaseSub: "Первые карты первой колоды направления.",
    systems: "Системы", open: "Открыть →", back: "← Все направления",
    cardsIn: "карт", studyBadge: "навчальна модель", partialBadge: "неполный набор",
    empty: "В этом направлении пока нет колод.",
  },
  uk: {
    cards: "Значення карт", practice: "Практика", guides: "Гайди",
    decks: "Колоди напрямку", decksSub: "Клік веде на 3D-вітрину колоди.",
    showcase: "3D-вітрина", showcaseSub: "Перші карти першої колоди напрямку.",
    systems: "Системи", open: "Відкрити →", back: "← Усі напрямки",
    cardsIn: "карт", studyBadge: "навчальна модель", partialBadge: "неповний набір",
    empty: "У цьому напрямку поки немає колод.",
  },
  en: {
    cards: "Card meanings", practice: "Practice", guides: "Guides",
    decks: "Direction decks", decksSub: "Click opens the deck's 3D shelf.",
    showcase: "3D showcase", showcaseSub: "First cards of the direction's first deck.",
    systems: "Systems", open: "Open →", back: "← All directions",
    cardsIn: "cards", studyBadge: "study model", partialBadge: "partial set",
    empty: "No decks in this direction yet.",
  },
};

/** Клієнт напрямку: вкладки + 3D-вітрина + сітка колод + системи. */
export default function DirectionClient({ direction, systems, decks }) {
  const [lang, setLang] = useState("uk");
  const [theme, setTheme] = useState("dark");
  const [fan, setFan] = useState([]);
  const [fanDeck, setFanDeck] = useState(null);
  const t = T[lang];

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

  useEffect(() => {
    const first = (decks || []).find((d) => d.cards > 0);
    if (!first) return;
    setFanDeck(first);
    getJSON(`/cards?deck_id=${first.id}&limit=7`).then((cs) => {
      if (Array.isArray(cs)) setFan(cs);
    }).catch(() => {});
  }, [decks]);

  const totalCards = (decks || []).reduce((a, d) => a + (d.cards || 0), 0);

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
            {(systems || []).length} · {t.systems.toLowerCase()} · {(decks || []).length} · {t.decks.toLowerCase()} · {totalCards} · {t.cardsIn}
          </p>
        </header>

        <nav className="dir-tabs" aria-label={direction.title.uk}>
          <a href={`/directions/${direction.slug}`} className="active">{t.cards}</a>
          <a href={`/directions/${direction.slug}/spreads`}>{t.practice}</a>
          <a href={`/directions/${direction.slug}/guides`}>{t.guides}</a>
        </nav>

        {fan.length > 0 && (
          <Reveal>
            <section className="section" style={{ paddingTop: 20 }}>
              <div className="section-head">
                <span className="num">✦</span>
                <div>
                  <h2>{t.showcase}</h2>
                  <p>{t.showcaseSub} — {fanDeck?.name}</p>
                </div>
              </div>
              <Scene3D cards={fan} lang={lang} onSelect={() => {}} />
            </section>
          </Reveal>
        )}

        <Reveal>
          <section className="section">
            <div className="section-head">
              <span className="num">{direction.icon}</span>
              <div><h2>{t.decks}</h2><p>{t.decksSub}</p></div>
            </div>
            {(decks || []).length === 0 ? (
              <p style={{ color: "var(--muted)" }}>{t.empty}</p>
            ) : (
              <div className="sys-grid">
                {decks.map((d) => (
                  <a key={d.id} className="sys-card glow-border" href={`/decks/${d.id}`}
                    style={{ textDecoration: "none", color: "inherit" }}>
                    <span className="badge badge-study">{t.studyBadge}</span>
                    {d.is_partial && <span className="badge badge-partial">{t.partialBadge}</span>}
                    {d.cover && (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img src={d.cover} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                        style={{ width: "100%", borderRadius: 10, marginBottom: 10 }} />
                    )}
                    <div className="cat">{d.system}</div>
                    <b>{d.name}</b>
                    <div className="n">{d.cards}</div>
                    <small>{d.cards} · {t.cardsIn} — {t.open}</small>
                  </a>
                ))}
              </div>
            )}
          </section>
        </Reveal>

        <Reveal>
          <div className="divider">✦ ✦ ✦</div>
          <section className="section">
            <div className="section-head">
              <span className="num">§</span>
              <div><h2>{t.systems}</h2></div>
            </div>
            <div className="chips" style={{ marginBottom: 0 }}>
              {(systems || []).map((s) => (
                <span key={s.id} className="chip" style={{ cursor: "default" }}>
                  {s.name} · {s.cards} {t.cardsIn}
                </span>
              ))}
            </div>
            <p style={{ marginTop: 22 }}>
              <a className="btn btn-ghost" href="/" style={{ display: "inline-block" }}>{t.back}</a>
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
