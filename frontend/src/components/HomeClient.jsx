"use client";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Reveal from "./Reveal";
import { cardName, getJSON, pick } from "../lib/api";

/** Канонічні ключі категорій систем (порядок вкладок). */
const CAT_ORDER = ["all", "divination", "oracles", "therapeutic", "astrological", "shamanic", "calendar", "esoteric", "numerological"];

/** Нормалізує systems.category (ru/uk) до канонічного ключа. */
function normCat(c) {
  const s = (c || "").toString().trim().toLowerCase();
  if (s.includes("гадател") || s.includes("гадалн")) return "divination";
  if (s.includes("оракул")) return "oracles";
  if (s.includes("терапевт")) return "therapeutic";
  if (s.includes("астролог")) return "astrological";
  if (s.includes("шаман")) return "shamanic";
  if (s.includes("календар")) return "calendar";
  if (s.includes("езотер") || s.includes("эзотер")) return "esoteric";
  if (s.includes("нумеролог")) return "numerological";
  return "other";
}

const MARQ = ["ТАРО", "ЛЕНОРМАН", "І-ЦЗИН", "РУНИ", "ОРАКУЛИ", "МАК", "АСТРОЛОГІЯ", "ШАМАНСЬКІ", "ЦИГАНСЬКІ", "ЦОЛЬКІН", "ОГАМ", "БАГУА", "ІФА", "КАБАЛА", "ЧИСЛА-АНГЕЛИ", "КРИСТАЛИ"];

const T = {
  ru: {
    eyebrow: "Интерактивная 3D-энциклопедия · backend — 100% Python",
    titleA: "Карты судьбы —", titleB: "живая энциклопедия",
    sub: "Актуальная база: {cards} карт и {systems} систем. Сначала выбери колоду — потом листай её в 3D, читай разборы и проверяй себя в квизе.",
    cta1: "Выбрать колоду", cta2: "Мне повезёт",
    stats: ["карт в базе", "систем", "языка"],
    decks: "Колоды", decksSub: "Сначала колода — потом всё остальное. Клик ведёт на 3D-витрину колоды.",
    cats: {
      all: "Все", divination: "Гадальные", oracles: "Оракулы", therapeutic: "Терапевтические",
      astrological: "Астрологические", shamanic: "Шаманские", calendar: "Календарные",
      esoteric: "Эзотерические", numerological: "Нумерологические",
    },
    systems: "Системы карт", systemsSub: "Живой склад базы — GET /stats.",
    daily: "Карта дня",
    spreads: "Расклады", spreadsSub: "Отдельные страницы: выбор колоды и случайные карты.",
    timeline: "История систем", timelineSub: "От игральных карт XV века до оракулов.",
    articles: "Статьи", articlesSub: "Отдельные страницы: гайды энциклопедии — GET /articles.",
    gloss: "Глоссарий", glossSub: "Термины энциклопедии.",
    quiz: "Проверь себя", quizSub: "Отдельная страница: выбор колоды и счёт.", quizGo: "Открыть квиз →",
    method: "Методика COPE · BASIC Ph", methodSub: "Шесть ресурсных каналов — рамка колоды COPE (О. Аялон, OH Cards Institute).",
    caveat: "Честно: в COPE нет готовых «значений» 88 карт, как в Таро. Есть 6 категорий, к которым терапевт относит образ в работе.",
    srcDocs: "Официальные источники методики", openDeck: "Открыть колоду COPE →",
    pdfLabel: "Методичка О. Аялон (PDF, OH Institute)",
    foot: "RWS 1909 и Уэйт 1911 — общественное достояние. Современные трактовки — только пересказ своими словами.",
    cardsIn: "карт", decksIn: "колод", open: "Открыть →",
    studyBadge: "навчальна модель",
    partialBadge: "неповний набір",
  },
  uk: {
    eyebrow: "Інтерактивна 3D-енциклопедія · backend — 100% Python",
    titleA: "Карти долі —", titleB: "жива енциклопедія",
    sub: "Актуальна база: {cards} карт і {systems} систем. Спочатку обери колоду — потім гортай її в 3D, читай розбори й перевіряй себе у квізі.",
    cta1: "Обрати колоду", cta2: "Мені пощастить",
    stats: ["карт у базі", "систем", "мови"],
    decks: "Колоди", decksSub: "Спочатку колода — потім усе інше. Клік веде на 3D-вітрину колоди.",
    cats: {
      all: "Усі", divination: "Гадальні", oracles: "Оракули", therapeutic: "Терапевтичні",
      astrological: "Астрологічні", shamanic: "Шаманські", calendar: "Календарні",
      esoteric: "Езотеричні", numerological: "Нумерологічні",
    },
    systems: "Системи карт", systemsSub: "Живий склад бази — GET /stats.",
    daily: "Карта дня",
    spreads: "Розклади", spreadsSub: "Окремі сторінки: вибір колоди й випадкові карти.",
    timeline: "Історія систем", timelineSub: "Від гральних карт XV століття.",
    articles: "Статті", articlesSub: "Окремі сторінки: гайди енциклопедії — GET /articles.",
    gloss: "Глосарій", glossSub: "Терміни енциклопедії.",
    quiz: "Перевір себе", quizSub: "Окрема сторінка: вибір колоди й рахунок.", quizGo: "Відкрити квіз →",
    method: "Методика COPE · BASIC Ph", methodSub: "Шість ресурсних каналів — рамка колоди COPE (О. Аялон, OH Cards Institute).",
    caveat: "Чесно: у COPE нема готових «значень» 88 карт, як у Таро. Є 6 категорій, до яких терапевт відносить образ у роботі.",
    srcDocs: "Офіційні джерела методики", openDeck: "Відкрити колоду COPE →",
    pdfLabel: "Методичка О. Аялон (PDF, OH Institute)",
    foot: "RWS 1909 і Уейт 1911 — суспільне надбання.",
    cardsIn: "карт", decksIn: "колод", open: "Відкрити →",
    studyBadge: "навчальна модель",
    partialBadge: "неповний набір",
  },
  en: {
    eyebrow: "Interactive 3D encyclopedia · 100% Python backend",
    titleA: "Fortune cards —", titleB: "a living encyclopedia",
    sub: "Live DB: {cards} cards, {systems} systems. Pick a deck first — then browse it in 3D, read breakdowns and test yourself.",
    cta1: "Pick a deck", cta2: "Feeling lucky",
    stats: ["cards in DB", "systems", "languages"],
    decks: "Decks", decksSub: "Deck first — everything else after. Click opens the deck's 3D shelf.",
    cats: {
      all: "All", divination: "Divination", oracles: "Oracles", therapeutic: "Therapeutic",
      astrological: "Astrological", shamanic: "Shamanic", calendar: "Calendar",
      esoteric: "Esoteric", numerological: "Numerological",
    },
    systems: "Card systems", systemsSub: "Live DB contents — GET /stats.",
    daily: "Card of the day",
    spreads: "Spreads", spreadsSub: "Separate pages: deck picker and random cards.",
    timeline: "Systems timeline", timelineSub: "From 15th-century playing cards.",
    articles: "Articles", articlesSub: "Separate pages: encyclopedia guides — GET /articles.",
    gloss: "Glossary", glossSub: "Encyclopedia terms.",
    quiz: "Test yourself", quizSub: "Separate page: deck picker and score.", quizGo: "Open quiz →",
    method: "COPE method · BASIC Ph", methodSub: "Six resource channels — the frame of the COPE deck (O. Ayalon, OH Cards Institute).",
    caveat: "Honest note: COPE has no ready-made “meanings” for its 88 cards like Tarot does. There are 6 categories a therapist maps an image to.",
    srcDocs: "Official method sources", openDeck: "Open the COPE deck →",
    pdfLabel: "O. Ayalon manual (PDF, OH Institute)",
    foot: "RWS 1909 & Waite 1911 — public domain.",
    cardsIn: "cards", decksIn: "decks", open: "Open →",
    studyBadge: "study model",
    partialBadge: "partial set",
  },
};

/** Головна: герой → сітка колод → дейлі → системи/розклади/історія/статті/глосарій → тизер квізу. */
export default function HomeClient({ initialCounts, initialDecks, initialSystems }) {
  const router = useRouter();
  const [lang, setLang] = useState("uk");
  const [decks, setDecks] = useState(initialDecks || []);
  const [daily, setDaily] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [glossary, setGlossary] = useState([]);
  const [systems, setSystems] = useState(initialSystems || []);
  const [cope, setCope] = useState([]);
  const [copeDeckId, setCopeDeckId] = useState(null);
  const [counts, setCounts] = useState(initialCounts || { cards: 424, systems: 13 });
  const [theme, setTheme] = useState("dark");
  const [progress, setProgress] = useState(0);
  const [cat, setCat] = useState("all");
  const t = T[lang];

  const sysCat = useMemo(() => {
    const m = {};
    (systems || []).forEach((s) => { m[s.id] = s.category; });
    return m;
  }, [systems]);

  const enriched = useMemo(
    () => (decks || []).map((d) => ({ ...d, catKey: normCat(sysCat[d.system_id]) })),
    [decks, sysCat],
  );

  const countsByCat = useMemo(() => {
    const m = { all: enriched.length };
    enriched.forEach((d) => { m[d.catKey] = (m[d.catKey] || 0) + 1; });
    return m;
  }, [enriched]);

  const catTabs = useMemo(() => CAT_ORDER.filter((k) => k === "all" || countsByCat[k] > 0), [countsByCat]);

  const shown = useMemo(
    () => (cat === "all" ? enriched : enriched.filter((d) => d.catKey === cat)),
    [enriched, cat],
  );

  useEffect(() => {
    const read = () => {
      const m = window.location.hash.match(/^#decks-([a-z]+)$/);
      if (m && CAT_ORDER.includes(m[1])) setCat(m[1]);
    };
    read();
    window.addEventListener("hashchange", read);
    return () => window.removeEventListener("hashchange", read);
  }, []);

  function pickCat(k) {
    setCat(k);
    try { history.replaceState(null, "", `#decks-${k}`); } catch {}
  }

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
    getJSON("/glossary").then(setGlossary).catch(() => {});
    getJSON("/decks").then((ds) => {
      if (!Array.isArray(ds)) return;
      const found = ds.find((d) => (d.name || "").includes("COPE"));
      if (found) {
        setCopeDeckId(found.id);
        getJSON(`/cards?deck_id=${found.id}&limit=50`).then((cs) => Array.isArray(cs) && setCope(cs)).catch(() => {});
      }
    }).catch(() => {});
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
      <nav className="nav">
        <div className="wrap nav-inner">
          <a className="brand" href="#top">✦ AI-<b>Arcanum</b></a>
          <button className="theme-btn" onClick={toggleTheme} title="theme" style={{ marginLeft: "auto" }}>
            {theme === "dark" ? "☀" : "☾"}
          </button>
          <div className="lang-switch" style={{ marginLeft: 8 }}>
            {["ru", "uk", "en"].map((l) => (
              <button key={l} className={l === lang ? "active" : ""} onClick={() => setLang(l)}>
                {l.toUpperCase()}
              </button>
            ))}
          </div>
        </div>
        {catTabs.length > 1 && (
          <div className="wrap nav-cats" role="tablist" aria-label={t.decks}>
            {catTabs.map((k) => (
              <a key={k} href={`#decks-${k}`} role="tab" aria-selected={cat === k} className={cat === k ? "active" : ""}>
                {t.cats[k]}
              </a>
            ))}
          </div>
        )}
      </nav>

      <main id="top" className="wrap">
        <header className="hero" style={{ position: "relative", overflow: "visible" }}>
          <span className="hero-orb" style={{ width: 280, height: 280, left: "-60px", top: "40px", background: "rgba(122,92,255,.35)" }} />
          <span className="hero-orb" style={{ width: 220, height: 220, right: "-40px", top: "120px", background: "rgba(212,169,78,.4)", animationDelay: "-5s" }} />
          <span className="eyebrow">{t.eyebrow}</span>
          <h1>{t.titleA} <em>{t.titleB}</em></h1>
          <p>{t.sub.replace("{cards}", counts.cards).replace("{systems}", counts.systems)}</p>
          <div className="cta-row">
            <a className="btn btn-gold" href="#decks">{t.cta1}</a>
            <button className="btn btn-ghost" onClick={lucky}>🎲 {t.cta2}</button>
          </div>
          <div className="stats">
            <div className="stat"><b>{counts.cards}</b><span>{t.stats[0]}</span></div>
            <div className="stat"><b>{counts.systems}</b><span>{t.stats[1]}</span></div>
            <div className="stat"><b>3</b><span>{t.stats[2]}</span></div>
          </div>
        </header>
        <div className="marquee" aria-hidden="true">
          <span>✦ {MARQ.join(" ✦ ")} ✦ {MARQ.join(" ✦ ")}&nbsp;</span>
        </div>

        <Reveal>
          <section id="decks" className="section">
            <div className="section-head">
              <span className="num">01</span>
              <div><h2>{t.decks}</h2><p>{t.decksSub}</p></div>
            </div>
            <div className="tabs" role="tablist" aria-label={t.decks}>
              {catTabs.map((k) => (
                <button key={k} id={`decks-${k}`} role="tab" aria-selected={cat === k}
                  className={"tab" + (cat === k ? " active" : "")} onClick={() => pickCat(k)}>
                  {t.cats[k]}<span className="tab-n">{countsByCat[k]}</span>
                </button>
              ))}
            </div>
            <div className="sys-grid">
              {shown.map((d) => (
                <a key={d.id} className="sys-card" href={`/decks/${d.id}`} style={{ textDecoration: "none", color: "inherit" }}>
                  <span className="badge badge-study">{t.studyBadge}</span>
                  {d.is_partial && <span className="badge badge-partial">{t.partialBadge}</span>}
                  {d.cover && (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img src={d.cover} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                      style={{ width: "100%", borderRadius: 10, marginBottom: 10 }} />
                  )}
                  <div className="cat">{d.system}</div>
                  <b>{d.name}</b>
                  <div className="n">{d.cards}</div>
                  <small>{d.cards} · {t.cardsIn} — {t.open}</small>
                </a>
              ))}
            </div>
          </section>
        </Reveal>

        {daily?.id && (
          <Reveal>
            <section id="daily" className="section">
              <div className="daily">
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
          <div className="divider">✦ ✦ ✦</div>
          <section id="systems" className="section">
            <div className="section-head">
              <span className="num">02</span>
              <div><h2>{t.systems}</h2><p>{t.systemsSub}</p></div>
            </div>
            <div className="sys-grid">
              {systems.map((s) => (
                <div key={s.id} className="sys-card">
                  <div className="cat">{s.category || "—"}</div>
                  <b>{s.name}</b>
                  <div className="n">{s.cards}</div>
                  <small>{s.decks} · {t.decksIn} · {s.cards} · {t.cardsIn}</small>
                </div>
              ))}
            </div>
          </section>
        </Reveal>

        <Reveal>
          <div className="divider">✦ ✦ ✦</div>
          <section id="spreads" className="section">
            <div className="section-head">
              <span className="num">03</span>
              <div><h2>{t.spreads}</h2><p>{t.spreadsSub}</p></div>
            </div>
            <div className="chips">
              <a className="chip" href="/spreads">🃏 — {t.spreads} →</a>
            </div>
          </section>
        </Reveal>

        <Reveal>
          <div className="divider">✦ ✦ ✦</div>
          <section id="history" className="section">
            <div className="section-head">
              <span className="num">04</span>
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
          <div className="divider">✦ ✦ ✦</div>
          <section id="articles" className="section">
            <div className="section-head">
              <span className="num">05</span>
              <div><h2>{t.articles}</h2><p>{t.articlesSub}</p></div>
            </div>
            <a className="btn btn-ghost" href="/articles" style={{ display: "inline-block" }}>✦ — {t.articles} →</a>
          </section>
        </Reveal>

        <Reveal>
          <div className="divider">✦ ✦ ✦</div>
          <section id="method" className="section">
            <div className="section-head">
              <span className="num">06</span>
              <div><h2>{t.method}</h2><p>{t.methodSub}</p></div>
            </div>
            <p style={{ color: "var(--muted)", maxWidth: 760, lineHeight: 1.7 }}>⚖ {t.caveat}</p>
            <div className="sys-grid">
              {cope.map((c) => (
                <div key={c.id} className="sys-card">
                  <div className="cat">{c.category}</div>
                  <b>{cardName(c, lang)}</b>
                  <p style={{ fontSize: 13, color: "var(--gold-soft)" }}>◈ {pick(c, lang, "theme").theme || c.theme}</p>
                  <p style={{ fontSize: 13, color: "var(--muted)", lineHeight: 1.6 }}>{c.meaning_general}</p>
                </div>
              ))}
            </div>
            <p style={{ marginTop: 16, color: "var(--muted)", fontSize: 13 }}>📚 {t.srcDocs}:</p>
            <div className="chips">
              <a className="chip" href="https://www.oh-cards-institute.org/wp-content/uploads/2012/06/Ofra-Ayalon-Healing-Trauma-with-Metaphoric-Cards.pdf" target="_blank" rel="noreferrer">📄 {t.pdfLabel}</a>
              <a className="chip" href="https://oh-cards.com/cope/" target="_blank" rel="noreferrer">oh-cards.com/cope</a>
              <a className="chip" href="https://www.theohcards.com/ohcards/cope-cards" target="_blank" rel="noreferrer">theohcards.com</a>
              <a className="chip" href="http://projective-cards.ru/cope/" target="_blank" rel="noreferrer">projective-cards.ru</a>
            </div>
            {copeDeckId && <a className="btn btn-gold" href={`/decks/${copeDeckId}`} style={{ display: "inline-block", marginTop: 8 }}>{t.openDeck}</a>}
          </section>
        </Reveal>

        <Reveal>
          <div className="divider">✦ ✦ ✦</div>
          <section id="glossary" className="section">
            <div className="section-head">
              <span className="num">07</span>
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
          <div className="divider">✦ ✦ ✦</div>
          <section id="quiz-teaser" className="section">
            <div className="section-head">
              <span className="num">08</span>
              <div><h2>{t.quiz}</h2><p>{t.quizSub}</p></div>
            </div>
            <a className="btn btn-gold" href="/quiz" style={{ display: "inline-block" }}>{t.quizGo}</a>
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
