"use client";
import { useEffect, useState } from "react";

const HOME = { href: "/", ru: "На главную", uk: "На головну", en: "Home" };
const LINKS = [
  { href: "/#decks", icon: "🃏", ru: "Значение карт", uk: "Значення карт", en: "Card meanings" },
  { href: "/spreads", icon: "🔀", ru: "Виды раскладов", uk: "Види розкладів", en: "Spread layouts" },
  { href: "/articles", icon: "📜", ru: "Гайды и статьи", uk: "Гайди і статті", en: "Guides & articles" },
  { href: "/quiz", icon: "🧠", ru: "Квиз", uk: "Квіз", en: "Quiz" },
];
const T = {
  close: { ru: "Закрыть", uk: "Закрити", en: "Close" },
  menu: { ru: "Меню", uk: "Меню", en: "Menu" },
  lang: { ru: "Язык", uk: "Мова", en: "Language" },
};

export default function SideMenu({ lang = "ru", setLang }) {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => (document.body.style.overflow = "");
  }, [open]);
  const close = () => setOpen(false);

  return (
    <>
      <button type="button" className="burger" aria-label={T.menu[lang]} aria-expanded={open}
        onClick={() => setOpen(true)}>
        <span /><span /><span />
      </button>
      {open && (
        <>
          <div className="drawer-overlay" onClick={close} aria-hidden="true" />
          <aside className="drawer" role="dialog" aria-modal="true" aria-label={T.menu[lang]}>
            <div className="drawer-top">
              <b className="brand" style={{ fontSize: 16 }}>✦ AI-<b>Arcanum</b></b>
              <button type="button" className="drawer-close" aria-label={T.close[lang]} onClick={close}>✕</button>
            </div>
            <a className="drawer-home" href={HOME.href} onClick={close}>{HOME[lang]}</a>
            <nav className="drawer-nav">
              {LINKS.map((m) => (
                <a key={m.href} href={m.href} onClick={close}>
                  <span className="drawer-ico" aria-hidden="true">{m.icon}</span>
                  {m[lang]}
                </a>
              ))}
            </nav>
            <div className="drawer-lang">
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
      )}
    </>
  );
}