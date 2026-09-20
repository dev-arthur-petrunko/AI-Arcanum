"use client";
import { useEffect, useState } from "react";
import SiteNav from "./SiteNav";
import Reveal from "./Reveal";
import { pick } from "../lib/api";

const T = {
  ru: {
    back: "← Вернуться к колоде", home: "На главную", prev: "← Назад", next: "Вперёд →",
    of: "из", cards: "в колоде", src: "см. backend/Database/sources_log.md",
    more: "Читать далее ↓", less: "Свернуть ↑",
  },
  uk: {
    back: "← Повернутися до колоди", home: "На головну", prev: "← Назад", next: "Вперед →",
    of: "з", cards: "у колоді", src: "див. backend/Database/sources_log.md",
    more: "Читати далі ↓", less: "Згорнути ↑",
  },
  en: {
    back: "← Back to deck", home: "Home", prev: "← Prev", next: "Next →",
    of: "of", cards: "in deck", src: "see backend/Database/sources_log.md",
    more: "Read more ↓", less: "Collapse ↑",
  },
};

const CUT = 600;

/** Окрема сторінка карти: повний опис + навігація по колоді. */
export default function CardPage({ card, deck, deckCards, direction }) {
  const [lang, setLang] = useState("uk");
  const [theme, setTheme] = useState("dark");
  const [open, setOpen] = useState(false);
  const t = T[lang];

  useEffect(() => {
    try {
      if (localStorage.getItem("arcanum-lang")) setLang(localStorage.getItem("arcanum-lang"));
      const saved = localStorage.getItem("arcanum-theme");
      if (saved === "light" || saved === "dark") {
        setTheme(saved);
        document.documentElement.dataset.theme = saved;
      }
    } catch {}
  }, []);
  useEffect(() => { document.documentElement.dataset.theme = theme; }, [theme]);

  function toggleTheme() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    try { localStorage.setItem("arcanum-theme", next); } catch {}
  }

  if (!card?.id) return null;

  const c = pick(
    card, lang, "name", "description", "theme",
    "keywords_upright", "keywords_reversed", "meaning_general",
    "meaning_love", "meaning_career", "meaning_health",
    "meaning_spirituality", "meaning_reversed", "symbolism"
  );
  const long = (c.meaning_general || "").length > CUT;
  const shown = !long || open ? c.meaning_general : `${c.meaning_general.slice(0, CUT)}…`;

  const list = (deckCards || []).filter((x) => x && x.id);
  const idx = list.findIndex((x) => x.id === card.id);
  const prev = idx > 0 ? list[idx - 1] : null;
  const next = idx >= 0 && idx < list.length - 1 ? list[idx + 1] : null;
  const position = idx >= 0 ? idx + 1 : card.number;
  const base = `/directions/${direction?.slug || "divination"}/card`;
  const deckUrl = deck ? `/decks/${deck.id}` : "/";

  return (
    <>
      <SiteNav lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} />
      <main className="wrap" style={{ paddingTop: 110, paddingBottom: 60 }}>
        <div className="crumbs">
          <a href={deckUrl}>{t.back}</a>
          {direction && (
            <>
              <span style={{ color: "var(--muted)" }}> · </span>
              <a href={`/directions/${direction.slug}`} style={{ color: "var(--muted)" }}>{t.home}</a>
            </>
          )}
        </div>

        <Reveal>
          <header className="page-hero sparkle-field" style={{ padding: "30px 30px", marginBottom: 6 }}>
            <span style={{ fontSize: 34 }}>{direction?.icon || "✦"}</span>
            <h1 style={{ margin: "10px 0 6px", fontSize: "clamp(30px, 4vw, 48px)" }}>{c.name}</h1>
            <p style={{ color: "var(--muted)", maxWidth: 680, lineHeight: 1.6 }}>
              {deck?.name} — {String(position)} · {String(list.length)} · {t.of} {list.length} {t.cards}
            </p>
          </header>
        </Reveal>

        <div style={{ display: "flex", gap: 26, flexWrap: "wrap", marginTop: 22, alignItems: "flex-start" }}>
          <div style={{ flex: "0 1 360px", minWidth: 260 }}>
            {card.image_path && card.id > 0 ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={card.image_path} alt={c.name} style={{ width: "100%", borderRadius: 18, border: "1px solid var(--line)", boxShadow: "0 18px 50px rgba(0,0,0,.45)" }} />
            ) : (
              <div style={{ fontSize: 120, textAlign: "center", border: "1px solid var(--line)", borderRadius: 18, padding: "60px 0" }}>✦</div>
            )}
          </div>

          <div style={{ flex: "1 1 440px", minWidth: 300 }}>
            <div className="meta">{card.number} · {card.arcana_type || card.category || "—"}</div>
            <h2 style={{ fontSize: 26, margin: "10px 0 4px" }}>{c.name}</h2>
            {c.theme && <p style={{ color: "var(--gold-soft)" }}>◈ {c.theme}</p>}
            {c.keywords_upright && <p><b>{c.keywords_upright}</b></p>}
            {c.keywords_reversed && <p style={{ color: "var(--muted)" }}>⇄ {c.keywords_reversed}</p>}
            <p style={{ whiteSpace: "pre-wrap", lineHeight: 1.7 }}>{shown}</p>
            {long && (
              <button className="btn btn-ghost" style={{ padding: "8px 18px", fontSize: 13 }}
                onClick={() => setOpen(!open)}>
                {open ? t.less : t.more}
              </button>
            )}
            {c.meaning_reversed && (
              <p style={{ color: "var(--muted)" }}>⇄ {c.meaning_reversed}</p>
            )}
            <dl className="kv">
              {!!c.meaning_love && (<><dt>♥</dt><dd>{c.meaning_love}</dd></>)}
              {!!c.meaning_career && (<><dt>⚒</dt><dd>{c.meaning_career}</dd></>)}
              {!!c.meaning_health && (<><dt>✚</dt><dd>{c.meaning_health}</dd></>)}
              {!!c.meaning_spirituality && (<><dt>☯</dt><dd>{c.meaning_spirituality}</dd></>)}
              {[card.element, card.planet, card.zodiac_sign].some(Boolean) && (
                <><dt>✳</dt><dd>{[card.element, card.planet, card.zodiac_sign].filter(Boolean).join(" · ")}</dd></>
              )}
            </dl>
            {(card.translations?.en?.source_reference || card.symbolism?.includes("Источник") || card.symbolism?.includes("Джерело")) && (
              <div className="src">📜 {card.translations?.en?.source_reference || t.src}</div>
            )}

            <div style={{ display: "flex", gap: 12, marginTop: 26, flexWrap: "wrap" }}>
              {prev && <a className="btn btn-ghost" href={`${base}/${prev.id}`} style={{ display: "inline-block" }}>← {pick(prev, lang, "name").name}</a>}
              {next && <a className="btn btn-ghost" href={`${base}/${next.id}`} style={{ display: "inline-block" }}>{pick(next, lang, "name").name} →</a>}
            </div>
          </div>
        </div>

        <div style={{ marginTop: 34 }}>
          <a className="btn btn-ghost" href={deckUrl} style={{ display: "inline-block" }}>{t.back}</a>
        </div>
      </main>
      <footer className="footer">
        <div className="wrap"><span>✦ AI-Arcanum · {deck?.name || "Карта"}</span></div>
      </footer>
    </>
  );
}