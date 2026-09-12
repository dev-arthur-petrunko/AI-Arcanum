"use client";
import { useEffect, useState } from "react";
import DeckShelf3D from "../components/DeckShelf3D";
import SearchPanel from "../components/SearchPanel";
import QuizModule from "../components/QuizModule";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const UI = {
  ru: { title: "Карты судьбы — энциклопедия", shelf: "Полка колод (3D)", cardDay: "Карта дня", quiz: "Обучение" },
  uk: { title: "Карти долі — енциклопедія", shelf: "Полиця колод (3D)", cardDay: "Карта дня", quiz: "Навчання" },
  en: { title: "Fortune-telling Cards — encyclopedia", shelf: "Deck shelf (3D)", cardDay: "Card of the day", quiz: "Study" },
};

export default function Page() {
  const [lang, setLang] = useState("ru");
  const [cards, setCards] = useState([]);
  const [selected, setSelected] = useState(null);
  const [daily, setDaily] = useState(null);
  const t = UI[lang];

  useEffect(() => {
    fetch(`${API}/cards?limit=9`).then((r) => r.json()).then(setCards).catch(() => {});
    fetch(`${API}/cards/daily`).then((r) => r.json()).then(setDaily).catch(() => {});
  }, []);

  const name = (c) => c?.translations?.[lang]?.name || c?.name;

  return (
    <main style={{ maxWidth: 1100, margin: "0 auto", padding: 24, display: "grid", gap: 20 }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>{t.title}</h1>
        <div style={{ display: "flex", gap: 8 }}>
          {["ru", "uk", "en"].map((l) => (
            <button key={l} onClick={() => setLang(l)} disabled={l === lang}>{l.toUpperCase()}</button>
          ))}
        </div>
      </header>

      <SearchPanel lang={lang} onResults={setCards} />

      <section>
        <h2>{t.shelf}</h2>
        <DeckShelf3D cards={cards} onSelect={setSelected} />
        {selected && (
          <article style={{ marginTop: 12, padding: 16, background: "#12162e", borderRadius: 12 }}>
            <h3>{name(selected)} <small style={{ opacity: 0.6 }}>{selected.number} · {selected.arcana_type}</small></h3>
            <p>{selected.keywords_upright}</p>
            <p style={{ opacity: 0.85 }}>{selected.meaning_general}</p>
            {selected.symbolism && <p style={{ opacity: 0.7 }}>🔣 {selected.symbolism}</p>}
          </article>
        )}
      </section>

      {daily && daily.id && (
        <section style={{ padding: 16, background: "#171c3a", borderRadius: 12 }}>
          <h2>🃏 {t.cardDay}: {name(daily)}</h2>
          <p>{daily.keywords_upright}</p>
        </section>
      )}

      <QuizModule />
      <footer style={{ opacity: 0.6, fontSize: 13 }}>
        RWS 1909 — public domain. Современные трактовки — только пересказ своими словами. См. content/sources_log.md
      </footer>
    </main>
  );
}
