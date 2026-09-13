"use client";
import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import Scene3D from "./Scene3D";
import CardDetail from "./CardDetail";
import { cardName, getJSON, pick } from "../lib/api";

const T = {
  ru: { back: "← Все колоды", searchPh: "Поиск по колоде…", found: "Найдено", pick: "Кликни карту в 3D или в списке ↓", lucky: "🎲 Случайная карта колоды" },
  uk: { back: "← Усі колоди", searchPh: "Пошук по колоді…", found: "Знайдено", pick: "Клікни карту в 3D або в списку ↓", lucky: "🎲 Випадкова карта колоди" },
  en: { back: "← All decks", searchPh: "Search this deck…", found: "Found", pick: "Click a card in 3D or in the list ↓", lucky: "🎲 Random card of this deck" },
};

/** Клієнт сторінки колоди: 3D-віяло, пошук усередині колоди, розбір, ?card=підсвітка. */
export default function DeckClient({ deck, initialCards, lang, setLang }) {
  const t = T[lang];
  const params = useSearchParams();
  const [cards, setCards] = useState(initialCards);
  const [selected, setSelected] = useState(null);
  const [q, setQ] = useState("");

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

  const deckName = pick(deck, lang, "name", "description").name || deck.name;
  const deckDesc = pick(deck, lang, "description").description || deck.description;

  return (
    <>
      <a className="btn btn-ghost" href="/#decks" style={{ display: "inline-block", marginBottom: 18 }}>{t.back}</a>
      <div className="section-head">
        <span className="num">✦</span>
        <div>
          <h2 style={{ fontSize: "clamp(34px,5vw,56px)", margin: 0 }}>{deckName}</h2>
          <p>{[deck.author, deck.year].filter(Boolean).join(" · ")}</p>
          {deckDesc && <p style={{ maxWidth: 720 }}>{deckDesc}</p>}
        </div>
      </div>
      <div style={{ display: "flex", gap: 10, marginBottom: 14, flexWrap: "wrap" }}>
        <form onSubmit={search} className="search-row" style={{ flex: 1, minWidth: 240, margin: 0 }}>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder={t.searchPh} />
          <button type="submit">🔎</button>
        </form>
        <button className="btn btn-gold" onClick={luckyDeck}>{t.lucky}</button>
      </div>
      <Scene3D cards={cards} lang={lang} onSelect={setSelected} />
      <div style={{ marginTop: 18 }}>
        <CardDetail card={selected} lang={lang} emptyText={t.pick} />
      </div>
      <p style={{ color: "var(--muted)", fontSize: 13, marginTop: 16 }}>{t.found}: {cards.length}</p>
      <div className="grid-cards">
        {cards.map((c) => (
          <div key={c.id} className="mini-card" onClick={() => {
            setSelected(c);
            setTimeout(() => document.getElementById("card-detail")?.scrollIntoView({ behavior: "smooth", block: "center" }), 100);
          }}>
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
