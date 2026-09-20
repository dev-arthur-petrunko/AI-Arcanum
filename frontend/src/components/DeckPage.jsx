"use client";
import { useEffect, useState } from "react";
import { DeckClientSuspense } from "./DeckClient";
import SideMenu from "./SideMenu";

/** Клієнт обгортки сторінки колоди: мова + навігація. Дані — із серверного page.jsx. */
export default function DeckPage({ deck, initialCards, relatedDeck, relatedCards, isDivination }) {
  const [lang, setLang] = useState("uk");
  const [theme, setTheme] = useState("dark");
  if (!deck?.id) return <main className="wrap" style={{ paddingTop: 120 }}><p>404 — колоди нема.</p><a href="/">←</a></main>;

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

  return (
    <>
      <nav className="nav">
        <div className="wrap nav-inner">
          <SideMenu lang={lang} setLang={setLang} />
          <a className="brand" href="/">✦ AI-<b>Arcanum</b></a>
          <div className="nav-links" style={{ alignItems: "center", marginLeft: "auto" }}>
            <button className="theme-btn" onClick={toggleTheme} title="theme">
              {theme === "dark" ? "☀" : "☾"}
            </button>
            <div className="lang-switch">
              {["ru", "uk", "en"].map((l) => (
                <button key={l} className={l === lang ? "active" : ""} onClick={() => setLang(l)}>
                  {l.toUpperCase()}
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>
      <main className="wrap" style={{ paddingTop: 110, paddingBottom: 60 }}>
        <DeckClientSuspense deck={deck} initialCards={initialCards} relatedDeck={relatedDeck} relatedCards={relatedCards} isDivination={isDivination} lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} />
      </main>
    </>
  );
}
