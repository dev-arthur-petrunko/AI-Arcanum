"use client";
import { useEffect, useState } from "react";
import SiteNav from "../../components/SiteNav";
import { getJSON } from "../../lib/api";

const T = {
  ru: { title: "Глоссарий", sub: "Термины энциклопедии.", back: "← На главную" },
  uk: { title: "Глосарій", sub: "Терміни енциклопедії.", back: "← На головну" },
  en: { title: "Glossary", sub: "Encyclopedia terms.", back: "← Home" },
};

/** /glossary — окремий розділ (раніше був лише блоком на головній). */
export default function GlossaryPage() {
  const [lang, setLang] = useState("uk");
  const [theme, setTheme] = useState("dark");
  const [glossary, setGlossary] = useState([]);
  const t = T[lang];

  useEffect(() => {
    try {
      const saved = localStorage.getItem("arcanum-theme");
      if (saved === "light" || saved === "dark") {
        setTheme(saved);
        document.documentElement.dataset.theme = saved;
      }
    } catch {}
    getJSON("/glossary").then(setGlossary).catch(() => {});
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
      <SiteNav lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} active="glossary" />
      <main className="wrap" style={{ paddingTop: 110, paddingBottom: 60 }}>
        <div className="section-head">
          <span className="num">📖</span>
          <div><h2 style={{ margin: 0 }}>{t.title}</h2><p>{t.sub}</p></div>
        </div>
        <div className="gloss-grid">
          {glossary.map((g, i) => (
            <div key={i} className="gloss">
              <b>{g.term?.[lang] || g.term?.ru}</b>
              <p>{g.definition?.[lang] || g.definition?.ru}</p>
            </div>
          ))}
        </div>
        <p style={{ marginTop: 24 }}>
          <a className="btn btn-ghost" href="/" style={{ display: "inline-block" }}>{t.back}</a>
        </p>
      </main>
      <footer className="footer">
        <div className="wrap"><span>✦ AI-Arcanum · {t.title}</span></div>
      </footer>
    </>
  );
}
