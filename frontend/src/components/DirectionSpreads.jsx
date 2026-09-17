"use client";
import { useEffect, useState } from "react";
import SiteNav from "./SiteNav";
import Reveal from "./Reveal";
import { cardName, getJSON, pick } from "../lib/api";

const T = {
  ru: {
    title: "Практика", sub: "Как работать с колодами направления: схемы и онлайн-вытягивание.",
    back: "← К направлению", deckLabel: "Колода", draw: "🎲 Вытянуть карту",
    clear: "Очистить", empty: "Загрузка…", schemes: "Схемы направления",
    general: "Все схемы — в общем каталоге", goCatalog: "Открыть каталог раскладов →",
    note: "Для этого направления нет жёстких схем: одна карта и вопрос — уже практика.",
    upright: "Прямо", reversed: "Наклон", source: "→ Открыть в колоде",
  },
  uk: {
    title: "Практика", sub: "Як працювати з колодами напрямку: схеми й онлайн-витягування.",
    back: "← До напрямку", deckLabel: "Колода", draw: "🎲 Витягнути карту",
    clear: "Очистити", empty: "Завантаження…", schemes: "Схеми напрямку",
    general: "Усі схеми — у загальному каталозі", goCatalog: "Відкрити каталог розкладів →",
    note: "Для цього напрямку немає жорстких схем: одна карта і запитання — уже практика.",
    upright: "Прямо", reversed: "Наклон", source: "→ Відкрити в колоді",
  },
  en: {
    title: "Practice", sub: "How to work with this direction's decks: layouts and online draws.",
    back: "← Back to direction", deckLabel: "Deck", draw: "🎲 Draw a card",
    clear: "Clear", empty: "Loading…", schemes: "Direction layouts",
    general: "All layouts live in the general catalog", goCatalog: "Open the spreads catalog →",
    note: "This direction has no fixed layouts: one card and a question is already practice.",
    upright: "Upright", reversed: "Reversed", source: "→ Open in deck",
  },
};

/** /directions/{slug}/spreads — практика напрямку: схеми БД + онлайн-витягування. */
export default function DirectionSpreads({ direction, decks, initialSpreads }) {
  const [lang, setLang] = useState("uk");
  const [theme, setTheme] = useState("dark");
  const [deckId, setDeckId] = useState(null);
  const [card, setCard] = useState(null);
  const [loading, setLoading] = useState(false);
  const t = T[lang];

  useEffect(() => {
    try {
      const saved = localStorage.getItem("arcanum-theme");
      if (saved === "light" || saved === "dark") {
        setTheme(saved);
        document.documentElement.dataset.theme = saved;
      }
    } catch {}
    const usable = (decks || []).find((d) => d.cards > 0);
    if (usable) setDeckId(usable.id);
  }, [decks]);

  function toggleTheme() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    try {
      localStorage.setItem("arcanum-theme", next);
      document.documentElement.dataset.theme = next;
    } catch {}
  }

  const draw = async () => {
    setLoading(true);
    try {
      const c = await getJSON(`/cards/random${deckId ? `?deck_id=${deckId}` : ""}`);
      setCard(c?.id ? c : null);
    } catch {} finally {
      setLoading(false);
    }
  };

  const cc = card ? pick(card, lang, "name", "meaning_general", "keywords_upright", "keywords_reversed") : null;
  const rev = card && (card.id ?? 0) % 4 === 0;

  return (
    <>
      <SiteNav lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} active="spreads" />
      <main className="wrap" style={{ paddingTop: 110, paddingBottom: 60 }}>
        <div className="crumbs">
          <a href={`/directions/${direction.slug}`}>{direction.title[lang] || direction.title.uk}</a>
          <span>›</span>
          <span>{t.title}</span>
        </div>
        <div className="section-head">
          <span className="num">{direction.icon}</span>
          <div><h2 style={{ margin: 0 }}>{t.title}</h2><p>{t.sub}</p></div>
        </div>

        <Reveal>
          <section className="section" style={{ paddingTop: 10 }}>
            <h3 className="serif" style={{ fontSize: 24 }}>{t.schemes}</h3>
            {(initialSpreads || []).length === 0 ? (
              <p style={{ color: "var(--muted)", lineHeight: 1.7 }}>◈ {t.note}</p>
            ) : (
              <div className="spread-grid">
                {(initialSpreads || []).map((s) => (
                  <div key={s.id} className="spread-card">
                    <b>{s.translations?.[lang]?.name || s.name}</b>
                    <p>{s.translations?.[lang]?.description || s.description}</p>
                    <small style={{ color: "var(--muted)" }}>×{s.positions_count}</small>
                  </div>
                ))}
              </div>
            )}
            <p style={{ color: "var(--muted)" }}>{t.general}: <a href="/spreads">{t.goCatalog}</a></p>
          </section>
        </Reveal>

        <Reveal>
          <div className="daily" style={{ marginTop: 26 }}>
            <h2>{t.draw}</h2>
            <div className="form-row" style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "end", marginBottom: 10 }}>
              <label style={{ color: "var(--muted)", fontSize: 13 }}>
                {t.deckLabel}
                <select value={deckId ?? ""} onChange={(e) => { setDeckId(e.target.value ? Number(e.target.value) : null); setCard(null); }}
                  style={{ display: "block", marginTop: 6, padding: "10px 12px", borderRadius: 10, background: "var(--panel)", color: "var(--ivory)", border: "1px solid var(--line)", fontSize: 14, minWidth: 240 }}>
                  {(decks || []).filter((d) => (d.cards ?? 0) > 0).map((d) => (
                    <option key={d.id} value={d.id}>{d.name} · {d.cards}</option>
                  ))}
                </select>
              </label>
              <button type="button" className="btn btn-gold" onClick={draw} disabled={loading}>
                {loading ? "…" : t.draw}
              </button>
              {card && (
                <button type="button" className="btn btn-ghost" onClick={() => setCard(null)}>{t.clear}</button>
              )}
            </div>
            {card && (
              <div className="drawer drawer-card" style={{ gridTemplateColumns: "140px 1fr" }}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={card.image_path} alt={cc.name} onError={(e) => (e.currentTarget.style.display = "none")} />
                <div>
                  <div className="meta">{card.number} · {rev ? t.reversed : t.upright}</div>
                  <h3>{cardName(card, lang)}</h3>
                  <p><b>{rev && cc.keywords_reversed ? cc.keywords_reversed : cc.keywords_upright}</b></p>
                  {cc.meaning_general && <p style={{ whiteSpace: "pre-wrap" }}>{cc.meaning_general}</p>}
                  {card.deck_id && <a href={`/decks/${card.deck_id}?card=${card.id}`} style={{ color: "var(--gold-soft)", fontSize: 13 }}>{t.source}</a>}
                </div>
              </div>
            )}
          </div>
        </Reveal>

        <p style={{ marginTop: 22 }}>
          <a className="btn btn-ghost" href={`/directions/${direction.slug}`} style={{ display: "inline-block" }}>{t.back}</a>
        </p>
      </main>
      <footer className="footer">
        <div className="wrap"><span>✦ AI-Arcanum · {direction.title[lang] || direction.title.uk}</span></div>
      </footer>
    </>
  );
}
