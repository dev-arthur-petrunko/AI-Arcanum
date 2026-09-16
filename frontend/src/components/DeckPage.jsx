"use client";
import { useState } from "react";
import { DeckClientSuspense } from "./DeckClient";

/** Клієнт обгортки сторінки колоди: мова + навігація. Дані — із серверного page.jsx. */
export default function DeckPage({ deck, initialCards }) {
  const [lang, setLang] = useState("uk");
  if (!deck?.id) return <main className="wrap" style={{ paddingTop: 120 }}><p>404 — колоди нема.</p><a href="/">←</a></main>;
  return (
    <>
      <nav className="nav">
        <div className="wrap nav-inner">
          <a className="brand" href="/">✦ AI-<b>Arcanum</b></a>
          <div className="nav-links">
            <a className="active" href="/#decks">Значення карт</a>
            <a href="/spreads">Види розкладів</a>
            <a href="/articles">Гайди і статті</a>
            <a href="/quiz">Квіз</a>
          </div>
          <div className="lang-switch" style={{ marginLeft: "auto" }}>
            {["ru", "uk", "en"].map((l) => (
              <button key={l} className={l === lang ? "active" : ""} onClick={() => setLang(l)}>
                {l.toUpperCase()}
              </button>
            ))}
          </div>
        </div>
      </nav>
      <main className="wrap" style={{ paddingTop: 110, paddingBottom: 60 }}>
        <DeckClientSuspense deck={deck} initialCards={initialCards} lang={lang} setLang={setLang} />
      </main>
    </>
  );
}
