"use client";
import { useCallback, useEffect, useState } from "react";
import Scene3D from "../components/Scene3D";
import SearchPanel from "../components/SearchPanel";
import QuizModule from "../components/QuizModule";
import Reveal from "../components/Reveal";
import { API, cardName, getJSON, pick } from "../lib/api";

const T = {
  ru: {
    nav: ["Витрина", "Карта дня", "История", "Глоссарий", "Квиз"],
    eyebrow: "Интерактивная 3D-энциклопедия · backend — 100% Python",
    titleA: "Карты судьбы —", titleB: "живая энциклопедия",
    sub: "Таро, Ленорман, И-Цзин и руны: история, символика и значения 145 карт с настоящей 3D-витриной. Данные — из Python API, public-domain источники.",
    cta1: "Открыть витрину", cta2: "Мне повезёт",
    stats: ["карт в базе", "систем", "языка"],
    shelf: "Витрина колод", shelfSub: "Клик по карте — переворот и разбор. Камера вращается, колесо — зум.",
    results: "Найдено", pickCard: "Выбери карту на витрине ↑",
    daily: "Карта дня", timeline: "История систем", timelineSub: "От игральных карт XV века до оракулов — GET /timeline из Python API.",
    gloss: "Глоссарий", glossSub: "Термины энциклопедии — GET /glossary.",
    quiz: "Проверь себя", quizSub: "Флеш-карты с подсказками, прогресс считает Python.",
    foot: "RWS 1909 и Уэйт 1911 — общественное достояние. Современные трактовки — только пересказ своими словами.",
  },
  uk: {
    nav: ["Вітрина", "Карта дня", "Історія", "Глосарій", "Квіз"],
    eyebrow: "Інтерактивна 3D-енциклопедія · backend — 100% Python",
    titleA: "Карти долі —", titleB: "жива енциклопедія",
    sub: "Таро, Ленорман, І-Цзин і руни: історія, символіка та значення 145 карт зі справжньою 3D-вітриною.",
    cta1: "Відкрити вітрину", cta2: "Мені пощастить",
    stats: ["карт у базі", "систем", "мови"],
    shelf: "Вітрина колод", shelfSub: "Клік по карті — переворот і розбір.",
    results: "Знайдено", pickCard: "Обери карту на вітрині ↑",
    daily: "Карта дня", timeline: "Історія систем", timelineSub: "Від гральних карт XV століття.",
    gloss: "Глосарій", glossSub: "Терміни енциклопедії.",
    quiz: "Перевір себе", quizSub: "Флеш-картки з підказками.",
    foot: "RWS 1909 і Уейт 1911 — суспільне надбання.",
  },
  en: {
    nav: ["Shelf", "Daily card", "History", "Glossary", "Quiz"],
    eyebrow: "Interactive 3D encyclopedia · 100% Python backend",
    titleA: "Fortune cards —", titleB: "a living encyclopedia",
    sub: "Tarot, Lenormand, I Ching and runes: history, symbolism and meanings of 145 cards with a real 3D shelf.",
    cta1: "Open the shelf", cta2: "Feeling lucky",
    stats: ["cards in DB", "systems", "languages"],
    shelf: "Deck shelf", shelfSub: "Click a card to flip it and read the breakdown.",
    results: "Found", pickCard: "Pick a card on the shelf ↑",
    daily: "Card of the day", timeline: "Systems timeline", timelineSub: "From 15th-century playing cards.",
    gloss: "Glossary", glossSub: "Encyclopedia terms.",
    quiz: "Test yourself", quizSub: "Flashcards with hints.",
    foot: "RWS 1909 & Waite 1911 — public domain.",
  },
};

function Detail({ card, lang }) {
  if (!card) return <p style={{ color: "var(--muted)" }}>{T[lang].pickCard}</p>;
  const c = pick(card, lang, "name", "description");
  return (
    <div className="drawer">
      {card.image_path && card.id > 0 ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={card.image_path} alt={c.name} onError={(e) => (e.currentTarget.style.display = "none")} />
      ) : <div style={{ fontSize: 90, textAlign: "center" }}>✦</div>}
      <div>
        <div className="meta">{card.number} · {card.arcana_type || "—"}</div>
        <h3>{c.name}</h3>
        <p>{card.keywords_upright}</p>
        <p>{card.meaning_general}</p>
        {card.symbolism && <p style={{ color: "var(--muted)" }}>🔣 {card.symbolism.split("\n")[0]}</p>}
        <dl className="kv">
          {!!card.meaning_love && (<><dt>♥</dt><dd>{card.meaning_love}</dd></>)}
          {!!card.meaning_career && (<><dt>⚒</dt><dd>{card.meaning_career}</dd></>)}
          {[card.element, card.planet, card.zodiac_sign].some(Boolean) && (
            <><dt>✳</dt><dd>{[card.element, card.planet, card.zodiac_sign].filter(Boolean).join(" · ")}</dd></>
          )}
        </dl>
        {(card.translations?.en?.source_reference || card.symbolism?.includes("Источник") || card.symbolism?.includes("Джерело")) && (
          <div className="src">📜 {card.translations?.en?.source_reference || ({ ru: "см. backend/Database/sources_log.md", uk: "див. backend/Database/sources_log.md", en: "see backend/Database/sources_log.md" })[lang]}</div>
        )}
      </div>
    </div>
  );
}

export default function Page() {
  const [lang, setLang] = useState("uk");
  const [cards, setCards] = useState([]);
  const [selected, setSelected] = useState(null);
  const [daily, setDaily] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [glossary, setGlossary] = useState([]);
  const [counts, setCounts] = useState({ cards: 145, systems: 4 });
  const t = T[lang];

  useEffect(() => {
    getJSON("/cards?limit=50").then((d) => Array.isArray(d) && setCards(d.slice(0, 14))).catch(() => {});
    getJSON("/cards/daily").then(setDaily).catch(() => {});
    getJSON("/timeline").then(setTimeline).catch(() => {});
    getJSON("/glossary").then(setGlossary).catch(() => {});
    getJSON("/stats").then((s) => s && setCounts({ cards: s.cards, systems: s.systems })).catch(() => {});
    // Lenis smooth scroll (прогресивне покращення)
    import("lenis").then(({ default: Lenis }) => {
      try { new Lenis({ autoRaf: true, lerp: 0.09 }); } catch {}
    }).catch(() => {});
  }, []);

  const lucky = useCallback(async () => {
    try {
      const d = await getJSON("/quiz/question");
      if (d?.card_id) {
        const full = await getJSON(`/cards/${d.card_id}`);
        setSelected(full);
        document.getElementById("shelf")?.scrollIntoView({ behavior: "smooth" });
      }
    } catch {}
  }, []);

  return (
    <>
      <nav className="nav">
        <div className="wrap nav-inner">
          <a className="brand" href="#top">✦ AI-<b>Arcanum</b></a>
          <div className="nav-links">
            <a href="#shelf">{t.nav[0]}</a>
            <a href="#daily">{t.nav[1]}</a>
            <a href="#history">{t.nav[2]}</a>
            <a href="#glossary">{t.nav[3]}</a>
            <a href="#quiz">{t.nav[4]}</a>
          </div>
          <div className="lang-switch" style={{ marginLeft: 12 }}>
            {["ru", "uk", "en"].map((l) => (
              <button key={l} className={l === lang ? "active" : ""} onClick={() => setLang(l)}>
                {l.toUpperCase()}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main id="top" className="wrap">
        <header className="hero">
          <span className="eyebrow">{t.eyebrow}</span>
          <h1>{t.titleA} <em>{t.titleB}</em></h1>
          <p>{t.sub}</p>
          <div className="cta-row">
            <a className="btn btn-gold" href="#shelf">{t.cta1}</a>
            <button className="btn btn-ghost" onClick={lucky}>🎲 {t.cta2}</button>
          </div>
          <div className="stats">
            <div className="stat"><b>{counts.cards}</b><span>{t.stats[0]}</span></div>
            <div className="stat"><b>{counts.systems}</b><span>{t.stats[1]}</span></div>
            <div className="stat"><b>3</b><span>{t.stats[2]}</span></div>
          </div>
        </header>

        <Reveal>
          <section id="shelf" className="section">
            <div className="section-head">
              <span className="num">01</span>
              <div><h2>{t.shelf}</h2><p>{t.shelfSub}</p></div>
            </div>
            <SearchPanel lang={lang} onResults={(d) => d.length && setCards(d.slice(0, 14))} />
            <Scene3D cards={cards} lang={lang} onSelect={setSelected} />
            <div style={{ marginTop: 18 }}><Detail card={selected} lang={lang} /></div>
            {cards.length > 0 && (
              <div style={{ marginTop: 16 }}>
                <p style={{ color: "var(--muted)", fontSize: 13 }}>{t.results}: {cards.length}</p>
                <div className="grid-cards">
                  {cards.map((c) => (
                    <div key={c.id} className="mini-card" onClick={() => setSelected(c)}>
                      <b>{cardName(c, lang)}</b>
                      <span>{c.number} · {c.arcana_type}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        </Reveal>

        {daily?.id && (
          <Reveal>
            <section id="daily" className="section">
              <div className="daily">
                <div className="meta" style={{ color: "var(--gold-soft)", letterSpacing: ".2em", fontSize: 12 }}>🃏 {t.daily.toUpperCase()}</div>
                <h2 className="big">{cardName(daily, lang)}</h2>
                <p style={{ color: "#d8dcee" }}>{daily.keywords_upright}</p>
                <button className="btn btn-ghost" onClick={() => { setSelected(daily); document.getElementById("shelf")?.scrollIntoView({ behavior: "smooth" }); }}>
                  {t.cta1} →
                </button>
              </div>
            </section>
          </Reveal>
        )}

        <Reveal>
          <section id="history" className="section">
            <div className="section-head">
              <span className="num">02</span>
              <div><h2>{t.timeline}</h2><p>{t.timelineSub}</p></div>
            </div>
            <div className="timeline">
              {timeline.map((p, i) => (
                <div key={i} className="tl-item">
                  <b>{p.year}</b>
                  <p>{p[lang] || p.ru}</p>
                </div>
              ))}
            </div>
          </section>
        </Reveal>

        <Reveal>
          <section id="glossary" className="section">
            <div className="section-head">
              <span className="num">03</span>
              <div><h2>{t.gloss}</h2><p>{t.glossSub}</p></div>
            </div>
            <div className="gloss-grid">
              {glossary.map((g, i) => (
                <div key={i} className="gloss">
                  <b>{g.term?.[lang] || g.term?.ru}</b>
                  <p>{g.definition?.[lang] || g.definition?.ru}</p>
                </div>
              ))}
            </div>
          </section>
        </Reveal>

        <Reveal>
          <section id="quiz" className="section">
            <div className="section-head">
              <span className="num">04</span>
              <div><h2>{t.quiz}</h2><p>{t.quizSub}</p></div>
            </div>
            <QuizModule lang={lang} />
          </section>
        </Reveal>
      </main>

      <footer className="footer">
        <div className="wrap">
          <span>✦ AI-Arcanum · FastAPI (Python) + SQLite + Next.js/R3F</span>
          <span>{t.foot}</span>
        </div>
      </footer>
    </>
  );
}
