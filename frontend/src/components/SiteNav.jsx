"use client";
import { useEffect, useRef, useState } from "react";
import SideMenu from "./SideMenu";
import { DIRECTIONS } from "../lib/directions";

const T = {
  ru: { directions: "Направления", spreads: "Расклады", articles: "Гайды и статьи", glossary: "Глоссарий", quiz: "Квиз" },
  uk: { directions: "Напрямки", spreads: "Розклади", articles: "Гайди і статті", glossary: "Глосарій", quiz: "Квіз" },
  en: { directions: "Directions", spreads: "Spreads", articles: "Guides & articles", glossary: "Glossary", quiz: "Quiz" },
};

/** Спільна шапка: бургер + бренд + випадаюче меню «Напрямки» + загальні розділи. */
export default function SiteNav({ lang = "uk", setLang, theme, toggleTheme, active }) {
  const t = T[lang] || T.uk;
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const close = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    const esc = (e) => e.key === "Escape" && setOpen(false);
    document.addEventListener("click", close);
    document.addEventListener("keydown", esc);
    return () => {
      document.removeEventListener("click", close);
      document.removeEventListener("keydown", esc);
    };
  }, []);

  return (
    <nav className="nav">
      <div className="wrap nav-inner">
        <SideMenu lang={lang} setLang={setLang} />
        <a className="brand" href="/">✦ AI-<b>Arcanum</b></a>
        <div className="nav-links" style={{ alignItems: "center" }}>
          <div className={`drop${open ? " open" : ""}`} ref={ref}>
            <button type="button" className="drop-btn" aria-haspopup="true" aria-expanded={open}
              onClick={(e) => { e.stopPropagation(); setOpen((v) => !v); }}>
              {t.directions} ▾
            </button>
            <div className="drop-menu" role="menu">
              {DIRECTIONS.map((d) => (
                <a key={d.slug} href={`/directions/${d.slug}`} role="menuitem">
                  <span className="ico" aria-hidden="true">{d.icon}</span>
                  {d.title[lang] || d.title.uk}
                </a>
              ))}
            </div>
          </div>
          <a href="/spreads" className={active === "spreads" ? "active" : ""}>{t.spreads}</a>
          <a href="/articles" className={active === "articles" ? "active" : ""}>{t.articles}</a>
          <a href="/glossary" className={active === "glossary" ? "active" : ""}>{t.glossary}</a>
          <a href="/quiz" className={active === "quiz" ? "active" : ""}>{t.quiz}</a>
        </div>
        {toggleTheme && (
          <button className="theme-btn" onClick={toggleTheme} title="theme" style={{ marginLeft: "auto" }}>
            {theme === "dark" ? "☀" : "☾"}
          </button>
        )}
        <div className="lang-switch" style={{ marginLeft: toggleTheme ? 8 : "auto" }}>
          {["ru", "uk", "en"].map((l) => (
            <button key={l} className={l === lang ? "active" : ""} onClick={() => setLang(l)}>
              {l.toUpperCase()}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
}
