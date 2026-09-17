"use client";
import { useEffect, useState } from "react";
import QuizModule from "./QuizModule";
import SideMenu from "./SideMenu";
import { getJSON, pick } from "../lib/api";

const T = {
  ru: { title: "Проверь себя", sub: "Выбери колоду — вопросы будут только по ней. Счёт идёт до смены колоды.", all: "Все колоды", back: "← На главную" },
  uk: { title: "Перевір себе", sub: "Обери колоду — питання будуть лише з неї. Рахунок іде до зміни колоди.", all: "Усі колоди", back: "← На головну" },
  en: { title: "Test yourself", sub: "Pick a deck — questions come only from it. Score runs until you switch decks.", all: "All decks", back: "← Home" },
};

/** Окрема сторінка квізу: вибір колоди + рахунок. */
export default function QuizPage() {
  const [lang, setLang] = useState("uk");
  const [decks, setDecks] = useState([]);
  const [deckId, setDeckId] = useState(null);
  const t = T[lang];

  useEffect(() => {
    // лише колоди з картами (довідкові профілі без набору — не для квізу)
    getJSON("/stats").then((s) => {
      const rows = Array.isArray(s?.by_deck) ? s.by_deck.filter((d) => d.cards > 0) : [];
      setDecks(rows);
    }).catch(() => {});
  }, []);

  return (
    <>
      <nav className="nav">
        <div className="wrap nav-inner">
          <SideMenu lang={lang} setLang={setLang} />
          <a className="brand" href="/">✦ AI-<b>Arcanum</b></a>
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
          <span className="num">🧠</span>
          <div><h2 style={{ margin: 0 }}>{t.title}</h2><p>{t.sub}</p></div>
        </div>
        <div className="chips" style={{ marginBottom: 16 }}>
          <button type="button" className={`chip${deckId === null ? " active" : ""}`} onClick={() => setDeckId(null)}>
            {t.all}
          </button>
          {decks.map((d) => (
            <button key={d.id} type="button" className={`chip${deckId === d.id ? " active" : ""}`} onClick={() => setDeckId(d.id)}>
              {pick(d, lang, "name").name || d.name}
            </button>
          ))}
        </div>
        <QuizModule key={deckId ?? "all"} deckId={deckId} lang={lang} />
      </main>
    </>
  );
}
