"use client";
import { useEffect, useState } from "react";
import { getJSON } from "../lib/api";

const T = {
  ru: { title: "Статьи", sub: "Гайды энциклопедии: история, системы и практика чтения карт.", back: "← На главную", empty: "Статьи загружаются…", src: "📜" },
  uk: { title: "Статті", sub: "Гайди енциклопедії: історія, системи та практика читання карт.", back: "← На головну", empty: "Статті завантажуються…", src: "📜" },
  en: { title: "Articles", sub: "Encyclopedia guides: history, systems and card reading practice.", back: "← Home", empty: "Loading articles…", src: "📜" },
};

/** Окрема сторінка статей: акордеон усіх матеріалів з GET /articles. */
export default function ArticlesPage() {
  const [lang, setLang] = useState("uk");
  const [articles, setArticles] = useState([]);
  const t = T[lang];

  useEffect(() => {
    getJSON("/articles").then((d) => Array.isArray(d) && setArticles(d)).catch(() => {});
  }, []);

  return (
    <>
      <nav className="nav">
        <div className="wrap nav-inner">
          <a className="brand" href="/">✦ AI-<b>Arcanum</b></a>
          <div className="nav-links">
            <a href="/spreads">Розклади / Расклады / Spreads</a>
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
        <a className="btn btn-ghost" href="/" style={{ display: "inline-block", marginBottom: 18 }}>{t.back}</a>
        <div className="section-head">
          <span className="num">✦</span>
          <div><h2 style={{ margin: 0 }}>{t.title}</h2><p>{t.sub}</p></div>
        </div>
        {articles.length === 0 ? <p style={{ color: "var(--muted)" }}>{t.empty}</p> : (
          <div style={{ marginTop: 8 }}>
            {articles.map((a) => (
              <details key={a.id} className="article-card">
                <summary>
                  <span>{a.translations?.[lang]?.title || a.title}</span>
                  <span className="sys">{a.system}</span>
                </summary>
                <div className="article-body">
                  {a.body}
                  {a.source_reference && <div className="src">{t.src} {a.source_reference}</div>}
                </div>
              </details>
            ))}
          </div>
        )}
      </main>
      <footer className="footer">
        <div className="wrap"><span>✦ AI-Arcanum · Статті</span></div>
      </footer>
    </>
  );
}