"use client";
import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import Scene3D from "./Scene3D";
import CardDetail from "./CardDetail";
import { cardName, getJSON, pick } from "../lib/api";

const T = {
  ru: {
    back: "← Все колоды", searchPh: "Поиск по колоде…", found: "Найдено", pick: "Кликни карту в 3D или в списке ↓",
    lucky: "🎲 Случайная карта колоды", studyBadge: "навчальна модель", partialBadge: "неполный набор",
    tab3d: "3D-витрина", tabValues: "Значения карт",
    suits: { wands: "Жезлы", cups: "Кубки", swords: "Мечи", pentacles: "Пентакли" },
  },
  uk: {
    back: "← Усі колоди", searchPh: "Пошук по колоді…", found: "Знайдено", pick: "Клікни карту в 3D або в списку ↓",
    lucky: "🎲 Випадкова карта колоди", studyBadge: "навчальна модель", partialBadge: "неповний набір",
    tab3d: "3D-вітрина", tabValues: "Значення карт",
    suits: { wands: "Жезли", cups: "Кубки", swords: "Мечі", pentacles: "Пентаклі" },
  },
  en: {
    back: "← All decks", searchPh: "Search this deck…", found: "Found", pick: "Click a card in 3D or in the list ↓",
    lucky: "🎲 Random card of this deck", studyBadge: "study model", partialBadge: "partial set",
    tab3d: "3D showcase", tabValues: "Card meanings",
    suits: { wands: "Wands", cups: "Cups", swords: "Swords", pentacles: "Pentacles" },
  },
};

/** Короткий ключ карти: перша фраза keywords_upright (або theme). */
function shortKey(c, lang) {
  const tr = (c.translations || {})[lang] || {};
  const kw = tr.keywords_upright || c.keywords_upright || "";
  if (kw) return kw.split(",")[0].trim();
  return tr.theme || c.theme || "";
}

/** Згруповані карти: старші + молодші по мастях. */
function groupByArcana(cards) {
  const majors = cards.filter((c) => /Старш/i.test(c.arcana_type || ""));
  const minors = cards.filter((c) => !/Старш/i.test(c.arcana_type || "") && c.suit_code);
  const suitOrder = { wands: 0, cups: 1, swords: 2, pentacles: 3 };
  const bySuit = new Map();
  for (const c of minors) {
    if (!bySuit.has(c.suit_code)) bySuit.set(c.suit_code, []);
    bySuit.get(c.suit_code).push(c);
  }
  const suits = [...bySuit.entries()]
    .sort((a, b) => (suitOrder[a[0]] ?? 9) - (suitOrder[b[0]] ?? 9))
    .map(([code, list]) => ({ code, list }));
  return { majors, suits };
}

/** Клієнт сторінки колоди: 3D-віяло або сітка значень арканів, пошук, розбір, ?card=підсвітка. */
export default function DeckClient({ deck, initialCards, lang, setLang }) {
  const t = T[lang];
  const params = useSearchParams();
  const [cards, setCards] = useState(initialCards);
  const [selected, setSelected] = useState(null);
  const [q, setQ] = useState("");
  const [tab, setTab] = useState("values");

  const hasMajors = useMemo(() => cards.some((c) => /Старш/i.test(c.arcana_type || "")), [cards]);
  const groups = useMemo(() => groupByArcana(cards), [cards]);

  // ?card=<id> — прямий вхід на карту (кнопка «Мені пощастить»)
  useEffect(() => {
    const id = params.get("card");
    if (!id) return;
    getJSON(`/cards/${id}`).then((c) => {
      if (c?.id) {
        setSelected(c);
        setTimeout(() => document.getElementById("card-detail")?.scrollIntoView({ behavior: "smooth", block: "center" }), 400);
      }
    }).catch(() => {});
  }, [params]);

  async function search(e) {
    e?.preventDefault();
    const query = `/cards?deck_id=${deck.id}&limit=200${q.trim().length >= 2 ? `&q=${encodeURIComponent(q.trim())}` : ""}`;
    try {
      const d = await getJSON(query);
      if (Array.isArray(d)) setCards(d);
    } catch {}
  }

  async function luckyDeck() {
    try {
      const c = await getJSON(`/cards/random?deck_id=${deck.id}`);
      if (c?.id) {
        const full = await getJSON(`/cards/${c.id}?lang=${lang}`);
        setSelected(full);
        setTimeout(() => document.getElementById("card-detail")?.scrollIntoView({ behavior: "smooth", block: "center" }), 200);
      }
    } catch {}
  }

  /** Клік по карті у сітці значень. */
  function pickCard(c) {
    setSelected(c);
    setTimeout(() => document.getElementById("card-detail")?.scrollIntoView({ behavior: "smooth", block: "center" }), 100);
  }

  const deckName = pick(deck, lang, "name", "description").name || deck.name;
  const deckDesc = pick(deck, lang, "description").description || deck.description;
  const deckNote = pick(deck, lang, "note").note || null;

  return (
    <>
      <a className="btn btn-ghost" href="/#decks" style={{ display: "inline-block", marginBottom: 18 }}>{t.back}</a>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        <span className="badge badge-study">{t.studyBadge}</span>
        {deck.is_partial && <span className="badge badge-partial">{t.partialBadge}</span>}
      </div>
      {deckNote && (
        <p className="deck-note" style={{ maxWidth: 720, marginTop: 12 }}>⚠️ {deckNote}</p>
      )}
      <div className="section-head">
        <span className="num">✦</span>
        <div>
          <h2 style={{ fontSize: "clamp(34px,5vw,56px)", margin: 0 }}>{deckName}</h2>
          <p>{[deck.author, deck.year].filter(Boolean).join(" · ")}</p>
          {deckDesc && <p style={{ maxWidth: 720 }}>{deckDesc}</p>}
        </div>
      </div>
      {hasMajors && (
        <div className="tabs" style={{ marginBottom: 18 }}>
          <button className={`tab${tab === "values" ? " active" : ""}`} onClick={() => setTab("values")}>{t.tabValues}</button>
          <button className={`tab${tab === "3d" ? " active" : ""}`} onClick={() => setTab("3d")}>{t.tab3d}</button>
        </div>
      )}
      <div style={{ display: "flex", gap: 10, marginBottom: 14, flexWrap: "wrap" }}>
        <form onSubmit={search} className="search-row" style={{ flex: 1, minWidth: 240, margin: 0 }}>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder={t.searchPh} />
          <button type="submit">🔎</button>
        </form>
        <button className="btn btn-gold" onClick={luckyDeck}>{t.lucky}</button>
      </div>

      {tab === "values" && hasMajors ? (
        <>
          {groups.majors.length > 0 && (
            <>
              <p className="arc-title"><b>{t.tabValues}</b> <span className="arc-count">{groups.majors.length}</span></p>
              <div className="grid-cards">
                {groups.majors.map((c) => (
                  <div key={c.id} className="mini-card" onClick={() => pickCard(c)}>
                    {c.image_path && (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img src={c.image_path} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                        style={{ width: "100%", borderRadius: 8, marginBottom: 8 }} />
                    )}
                    <b className="arc-no">{c.number}</b>
                    <b>{cardName(c, lang)}</b>
                    {shortKey(c, lang) && <span className="arc-key">{shortKey(c, lang)}</span>}
                  </div>
                ))}
              </div>
            </>
          )}
          {groups.suits.map((s) => (
            <div key={s.code} style={{ marginTop: 22 }}>
              <p className="arc-title"><b>{t.suits[s.code] || s.code}</b> <span className="arc-count">{s.list.length}</span></p>
              <div className="grid-cards">
                {s.list.map((c) => (
                  <div key={c.id} className="mini-card" onClick={() => pickCard(c)}>
                    {c.image_path && (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img src={c.image_path} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                        style={{ width: "100%", borderRadius: 8, marginBottom: 8 }} />
                    )}
                    <b>{cardName(c, lang)}</b>
                    {shortKey(c, lang) && <span className="arc-key">{shortKey(c, lang)}</span>}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </>
      ) : (
        <>
          <Scene3D cards={cards} lang={lang} onSelect={setSelected} />
          <p style={{ color: "var(--muted)", fontSize: 13, marginBottom: 14 }}>{t.pick}</p>
        </>
      )}

      <div style={{ marginTop: 18 }}>
        <CardDetail card={selected} lang={lang} emptyText={t.pick} />
      </div>
      <p style={{ color: "var(--muted)", fontSize: 13, marginTop: 16 }}>{t.found}: {cards.length}</p>
      <div className="grid-cards" style={{ marginBottom: 10 }}>
        {cards.map((c) => (
          <div key={c.id} className="mini-card" onClick={() => pickCard(c)}>
            {c.image_path && (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={c.image_path} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                style={{ width: "100%", borderRadius: 8, marginBottom: 8 }} />
            )}
            <b>{cardName(c, lang)}</b>
            <span>{c.number} · {c.arcana_type}</span>
          </div>
        ))}
      </div>
    </>
  );
}

export function DeckClientSuspense(props) {
  return (
    <Suspense>
      <DeckClient {...props} />
    </Suspense>
  );
}