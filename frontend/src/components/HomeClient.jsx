"use client";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Reveal from "./Reveal";
import SiteNav from "./SiteNav";
import { cardName, getJSON } from "../lib/api";
import { DIRECTIONS, normCat } from "../lib/directions";

const MARQ = ["ТАРО", "ЛЕНОРМАН", "І-ЦЗИН", "РУНИ", "ОРАКУЛИ", "МАК", "АСТРОЛОГІЯ", "ШАМАНСЬКІ", "ЦИГАНСЬКІ", "ЦОЛЬКІН", "ОГАМ", "БАГУА", "ІФА", "КАБАЛА", "ЧИСЛА-АНГЕЛИ", "КРИСТАЛИ"];

const T = {
  ru: {
    eyebrow: "Интерактивная 3D-энциклопедия · backend — 100% Python",
    titleA: "Карты судьбы —", titleB: "живая энциклопедия",
    sub: "Актуальная база: {cards} карт и {systems} систем. Выбери направление — дальше витрина колод, практика и гайды.",
    cta1: "Открыть витрину", cta2: "Мне повезёт",
    stats: ["карт в базе", "систем", "направлений"],
    dirs: "Направления", dirsSub: "Восемь дверей — каждая ведёт на свою страницу: значения карт, практика, гайды.",
    daily: "Карта дня",
    history: "История систем", historySub: "От игральных карт XV века до оракулов.", historyGo: "Вся история →",
    hub: "Разделы", hubSub: "Общее для всех направлений.",
    hubSpreads: "Расклады", hubSpreadsD: "Каталог схем и онлайн-вытягивание",
    hubGuides: "Гайды и статьи", hubGuidesD: "Руководства, история, практика чтения",
    hubGloss: "Глоссарий", hubGlossD: "Термины энциклопедии",
    hubQuiz: "Квиз", hubQuizD: "Проверь себя: выбор колоды и счёт",
    foot: "RWS 1909 и Уэйт 1911 — общественное достояние. Современные трактовки — только пересказ своими словами.",
    decksIn: "колод", open: "Открыть →",
  },
  uk: {
    eyebrow: "Інтерактивна 3D-енциклопедія · backend — 100% Python",
    titleA: "Карти долі —", titleB: "жива енциклопедія",
    sub: "Актуальна база: {cards} карт і {systems} систем. Обери напрямок — далі вітрина колод, практика й гайди.",
    cta1: "Відкрити вітрину", cta2: "Мені пощастить",
    stats: ["карт у базі", "систем", "напрямків"],
    dirs: "Напрямки", dirsSub: "Вісім дверей — кожна веде на свою сторінку: значення карт, практика, гайди.",
    daily: "Карта дня",
    history: "Історія систем", historySub: "Від гральних карт XV століття до оракулів.", historyGo: "Уся історія →",
    hub: "Розділи", hubSub: "Спільне для всіх напрямків.",
    hubSpreads: "Розклади", hubSpreadsD: "Каталог схем і онлайн-витягування",
    hubGuides: "Гайди і статті", hubGuidesD: "Керівництва, історія, практика читання",
    hubGloss: "Глосарій", hubGlossD: "Терміни енциклопедії",
    hubQuiz: "Квіз", hubQuizD: "Перевір себе: вибір колоди й рахунок",
    foot: "RWS 1909 і Уейт 1911 — суспільне надбання.",
    decksIn: "колод", open: "Відкрити →",
  },
  en: {
    eyebrow: "Interactive 3D encyclopedia · 100% Python backend",
    titleA: "Fortune cards —", titleB: "a living encyclopedia",
    sub: "Live DB: {cards} cards, {systems} systems. Pick a direction — then decks, practice and guides.",
    cta1: "Open the shelf", cta2: "Feeling lucky",
    stats: ["cards in DB", "systems", "directions"],
    dirs: "Directions", dirsSub: "Eight doors — each opens its own page: meanings, practice, guides.",
    daily: "Card of the day",
    history: "Systems history", historySub: "From 15th-century playing cards to oracles.", historyGo: "Full history →",
    hub: "Sections", hubSub: "Shared across all directions.",
    hubSpreads: "Spreads", hubSpreadsD: "Layout catalog and online draws",
    hubGuides: "Guides & articles", hubGuidesD: "Manuals, history, reading practice",
    hubGloss: "Glossary", hubGlossD: "Encyclopedia terms",
    hubQuiz: "Quiz", hubQuizD: "Test yourself: deck picker and score",
    foot: "RWS 1909 & Waite 1911 — public domain.",
    decksIn: "decks", open: "Open →",
  },
};

/** Головна (slim): hero → карта дня → 8 напрямків → тизер історії → загальні розділи.
 *  Детальні розбори (COPE) і повний список систем живуть на профільних сторінках. */
export default function HomeClient({ initialCounts, initialDecks, initialSystems }) {
  const router = useRouter();
  const [lang, setLang] = useState("uk");
  const [decks, setDecks] = useState(initialDecks || []);
  const [daily, setDaily] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [systems, setSystems] = useState(initialSystems || []);
  const [counts, setCounts] = useState(initialCounts || { cards: 912, systems: 33 });
  const [theme, setTheme] = useState("dark");
  const [progress, setProgress] = useState(0);
  const t = T[lang];

  const sysCat = useMemo(() => {
    const m = {};
    (systems || []).forEach((s) => { m[s.id] = s.category; });
    return m;
  }, [systems]);

  const countsByCat = useMemo(() => {
    const m = {};
    (decks || []).forEach((d) => {
      const k = normCat(sysCat[d.system_id]);
      m[k] = (m[k] || 0) + 1;
    });
    return m;
  }, [decks, sysCat]);

  useEffect(() => {
    try {
      const saved = localStorage.getItem("arcanum-theme");
      if (saved === "light" || saved === "dark") {
        setTheme(saved);
        document.documentElement.dataset.theme = saved;
      }
    } catch {}
    const onScroll = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      setProgress(max > 0 ? h.scrollTop / max : 0);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  function toggleTheme() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    try {
      localStorage.setItem("arcanum-theme", next);
      document.documentElement.dataset.theme = next;
    } catch {}
  }

  useEffect(() => {
    getJSON("/cards/daily").then(setDaily).catch(() => {});
    getJSON("/timeline").then(setTimeline).catch(() => {});
    getJSON("/stats").then((s) => {
      if (!s) return;
      setCounts({ cards: s.cards, systems: s.systems });
      if (Array.isArray(s.by_system)) setSystems(s.by_system);
      if (Array.isArray(s.by_deck)) setDecks(s.by_deck);
    }).catch(() => {});
    import("lenis").then(({ default: Lenis }) => {
      try { new Lenis({ autoRaf: true, lerp: 0.09 }); } catch {}
    }).catch(() => {});
  }, []);

  // «Мені пощастить»: випадкова карта → одразу на її сторінку в колоді
  const lucky = useCallback(async () => {
    try {
      const c = await getJSON("/cards/random");
      if (c?.id) router.push(`/decks/${c.deck_id}?card=${c.id}`);
    } catch {}
  }, [router]);

  return (
    <>
      <div className="progress-bar" style={{ width: `${Math.round(progress * 100)}%` }} />
      <SiteNav lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} />

      <main id="top" className="wrap">
        <header className="hero sparkle-field" style={{ position: "relative", overflow: "visible" }}>
          <span className="hero-orb" style={{ width: 280, height: 280, left: "-60px", top: "40px", background: "rgba(122,92,255,.35)" }} />
          <span className="hero-orb" style={{ width: 220, height: 220, right: "-40px", top: "120px", background: "rgba(212,169,78,.4)", animationDelay: "-5s" }} />
          <span className="eyebrow">{t.eyebrow}</span>
          <h1>{t.titleA} <em>{t.titleB}</em></h1>
          <p>{t.sub.replace("{cards}", counts.cards).replace("{systems}", counts.systems)}</p>
          <div className="cta-row">
            <a className="btn btn-gold" href="#directions">{t.cta1}</a>
            <button className="btn btn-ghost" onClick={lucky}>🎲 {t.cta2}</button>
          </div>
          <div className="stats">
            <div className="stat"><b>{counts.cards}</b><span>{t.stats[0]}</span></div>
            <div className="stat"><b>{counts.systems}</b><span>{t.stats[1]}</span></div>
            <div className="stat"><b>8</b><span>{t.stats[2]}</span></div>
          </div>
        </header>
        <div className="marquee" aria-hidden="true">
          <span>✦ {MARQ.join(" ✦ ")} ✦ {MARQ.join(" ✦ ")}&nbsp;</span>
        </div>

        {daily?.id && (
          <Reveal>
            <section id="daily" className="section">
              <div className="daily glow-border">
                <div className="meta" style={{ color: "var(--gold-soft)", letterSpacing: ".2em", fontSize: 12 }}>🃏 {t.daily.toUpperCase()}</div>
                <h2 className="big">{cardName(daily, lang)}</h2>
                <p style={{ color: "var(--text2)" }}>{daily.keywords_upright}</p>
                <button className="btn btn-ghost" onClick={() => router.push(`/decks/${daily.deck_id}?card=${daily.id}`)}>
                  {t.open}
                </button>
              </div>
            </section>
          </Reveal>
        )}

        <Reveal>
          <section id="directions" className="section">
            <div className="section-head">
              <span className="num">08</span>
              <div><h2>{t.dirs}</h2><p>{t.dirsSub}</p></div>
            </div>
            <div className="dir-grid">
              {DIRECTIONS.map((d) => (
                <a key={d.slug} className="sys-card dir-card glow-border" href={`/directions/${d.slug}`}>
                  <span className="ico" aria-hidden="true">{d.icon}</span>
                  <div className="cat">{countsByCat[d.slug] || 0} · {t.decksIn}</div>
                  <b>{d.title[lang] || d.title.uk}</b>
                  <p style={{ fontSize: 13, color: "var(--muted)", lineHeight: 1.6 }}>
                    {d.desc[lang] || d.desc.uk}
                  </p>
                  <span className="go">{t.open}</span>
                </a>
              ))}
            </div>
          </section>
        </Reveal>

        <Reveal>
          <div className="divider">✦ ✦ ✦</div>
          <section id="history-teaser" className="section">
            <div className="section-head">
              <span className="num">⏳</span>
              <div><h2>{t.history}</h2><p>{t.historySub}</p></div>
            </div>
            <div className="timeline">
              {timeline.map((p, i) => (
                <div key={i} className="tl-item">
                  <b>{p.year}</b>
                  <p>{p[lang] || p.ru}</p>
                </div>
              ))}
            </div>
            <p style={{ marginTop: 16 }}>
              <a className="btn btn-ghost" href="/history" style={{ display: "inline-block" }}>{t.historyGo}</a>
            </p>
          </section>
        </Reveal>

        <Reveal>
          <div className="divider">✦ ✦ ✦</div>
          <section id="hub" className="section">
            <div className="section-head">
              <span className="num">✦</span>
              <div><h2>{t.hub}</h2><p>{t.hubSub}</p></div>
            </div>
            <div className="hub-grid">
              <a className="sys-card hub-card glow-border" href="/spreads">
                <span className="ico" aria-hidden="true">🔀</span>
                <b>{t.hubSpreads}</b>
                <p style={{ fontSize: 13, color: "var(--muted)" }}>{t.hubSpreadsD}</p>
              </a>
              <a className="sys-card hub-card glow-border" href="/articles">
                <span className="ico" aria-hidden="true">📜</span>
                <b>{t.hubGuides}</b>
                <p style={{ fontSize: 13, color: "var(--muted)" }}>{t.hubGuidesD}</p>
              </a>
              <a className="sys-card hub-card glow-border" href="/glossary">
                <span className="ico" aria-hidden="true">📖</span>
                <b>{t.hubGloss}</b>
                <p style={{ fontSize: 13, color: "var(--muted)" }}>{t.hubGlossD}</p>
              </a>
              <a className="sys-card hub-card glow-border" href="/quiz">
                <span className="ico" aria-hidden="true">🧠</span>
                <b>{t.hubQuiz}</b>
                <p style={{ fontSize: 13, color: "var(--muted)" }}>{t.hubQuizD}</p>
              </a>
            </div>
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
