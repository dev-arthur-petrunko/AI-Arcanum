"use client";
import { useEffect, useState } from "react";
import SiteNav from "../../components/SiteNav";
import Reveal from "../../components/Reveal";
import { getJSON } from "../../lib/api";

const T = {
  ru: { title: "История систем", sub: "От игральных карт XV века до оракулов.", back: "← На главную" },
  uk: { title: "Історія систем", sub: "Від гральних карт XV століття до оракулів.", back: "← На головну" },
  en: { title: "Systems history", sub: "From 15th-century playing cards to oracles.", back: "← Home" },
};

/** /history — повна стрічка історії (на головній лишився тільки тизер). */
export default function HistoryPage() {
  const [lang, setLang] = useState("uk");
  const [theme, setTheme] = useState("dark");
  const [timeline, setTimeline] = useState([]);
  const t = T[lang];

  useEffect(() => {
    try {
      const saved = localStorage.getItem("arcanum-theme");
      if (saved === "light" || saved === "dark") {
        setTheme(saved);
        document.documentElement.dataset.theme = saved;
      }
    } catch {}
    getJSON("/timeline").then(setTimeline).catch(() => {});
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
      <SiteNav lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} />
      <main className="wrap" style={{ paddingTop: 110, paddingBottom: 60 }}>
        <div className="section-head">
          <span className="num">⏳</span>
          <div><h2 style={{ margin: 0 }}>{t.title}</h2><p>{t.sub}</p></div>
        </div>
        <Reveal>
          <div className="timeline" style={{ flexWrap: "wrap", overflow: "visible" }}>
            {timeline.map((p, i) => (
              <div key={i} className="tl-item glow-border" style={{ minWidth: 250, flex: "1 1 250px" }}>
                <b>{p.year}</b>
                <p>{p[lang] || p.ru}</p>
              </div>
            ))}
          </div>
        </Reveal>
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
