"use client";
import { useEffect, useState } from "react";
import { DIRECTIONS } from "../lib/directions";

const HOME = { href: "/", ru: "На главную", uk: "На головну", en: "Home" };
const GENERAL = [
  { href: "/spreads", icon: "🔀", ru: "Виды раскладов", uk: "Види розкладів", en: "Spread layouts" },
  { href: "/articles", icon: "📜", ru: "Гайды и статьи", uk: "Гайди і статті", en: "Guides & articles" },
  { href: "/glossary", icon: "📖", ru: "Глоссарий", uk: "Глосарій", en: "Glossary" },
  { href: "/history", icon: "⏳", ru: "История", uk: "Історія", en: "History" },
  { href: "/quiz", icon: "🧠", ru: "Квиз", uk: "Квіз", en: "Quiz" },
];
const T = {
  close: { ru: "Закрыть", uk: "Закрити", en: "Close" },
  menu: { ru: "Меню", uk: "Меню", en: "Menu" },
  lang: { ru: "Язык", uk: "Мова", en: "Language" },
  dirs: { ru: "Направления", uk: "Напрямки", en: "Directions" },
  general: { ru: "Разделы", uk: "Розділи", en: "Sections" },
};

function applyMenu(v) {
  try {
    document.body.classList.toggle("side-open", v);
    document.body.style.overflow = v ? "hidden" : "";
  } catch {}
}

export default function SideMenu({ lang = "ru", setLang }) {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    try {
      if (document.body.classList.contains("side-open")) setOpen(true);
    } catch {}
  }, []);
  useEffect(() => {
    applyMenu(open);
    const onKey = (e) => { if (e.key === "Escape") setOpen(false); };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [open]);
  const openMenu = () => setOpen(true);
  const close = () => setOpen(false);

  return (
    <>
      <button type="button" className="burger" aria-label={T.menu[lang]} aria-expanded={open}
        onClick={openMenu}>
        <span /><span /><span />
      </button>
      <div className="side-overlay" onClick={close} aria-hidden="true" />
      <aside className="side-drawer" role="dialog" aria-modal="true" aria-label={T.menu[lang]}>
            <div className="side-top">
              <b className="brand" style={{ fontSize: 16 }}>✦ AI-<b>Arcanum</b></b>
              <button type="button" className="side-close" aria-label={T.close[lang]} onClick={close}>✕</button>
            </div>
            <a className="side-home" href={HOME.href} onClick={close}>{HOME[lang]}</a>
            <nav className="side-nav">
              <div className="side-sec">{T.dirs[lang]}</div>
              {DIRECTIONS.map((d) => (
                <a key={d.slug} href={`/directions/${d.slug}`} onClick={close}>
                  <span className="side-ico" aria-hidden="true">{d.icon}</span>
                  {d.title[lang] || d.title.uk}
                </a>
              ))}
              <div className="side-sec">{T.general[lang]}</div>
              {GENERAL.map((m) => (
                <a key={m.href} href={m.href} onClick={close}>
                  <span className="side-ico" aria-hidden="true">{m.icon}</span>
                  {m[lang]}
                </a>
              ))}
            </nav>
            <div className="side-lang">
              <small>{T.lang[lang]}</small>
              <div>
                {["ru", "uk", "en"].map((l) => (
                  <button key={l} className={l === lang ? "active" : ""}
                    onClick={() => { setLang && setLang(l); close(); }}>
                    {l.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>
          </aside>
    </>
  );
}
