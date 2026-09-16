"use client";
import { useEffect, useState } from "react";
import { cardName, getJSON, pick } from "../lib/api";

const T = {
  ru: {
    title: "Виды раскладов", sub: "Каталог схем: сколько карт, уровень, время и когда подходит. Расклад ниже можно перетянуть",
    back: "← На главную", deckLabel: "Колода", deckAll: "Любая колода",
    draw: "🎲 Вытянуть карты", clear: "Очистить", empty: "Загрузка колод…",
    noCards: "В этой колоде нет карт (профиль издания). Выбери другую.",
    pos: "Позиция", meaning: "Значение", upright: "Прямо", reversed: "Наклон",
    general: "Толкование", source: "→ Открыть в колоде",
    cards: "карт", min: "мин", level: "уровень", when: "Пригодится, когда",
    goToTool: "Расклад онлайн", applied: "Расклад выбран", chooseToDraw: "— выбери схему выше или расклад ниже",
  },
  uk: {
    title: "Види розкладів", sub: "Каталог схем: скільки карт, рівень, час і коли доречно.",
    back: "← На головну", deckLabel: "Колода", deckAll: "Будь-яка колода",
    draw: "🎲 Витягнути карти", clear: "Очистити", empty: "Завантаження колод…",
    noCards: "У цій колоді немає карт (профіль видання). Обери іншу.",
    pos: "Позиція", meaning: "Значення", upright: "Прямо", reversed: "Наклон",
    general: "Тлумачення", source: "→ Відкрити в колоді",
    cards: "карт", min: "хв", level: "рівень", when: "Стане в пригоді, коли",
    goToTool: "Розклад онлайн", applied: "Розклад обрано", chooseToDraw: "— обери схему або розклад нижче",
  },
  en: {
    title: "Spread layouts", sub: "Catalog of layouts: how many cards, level, time and when to use.",
    back: "← Home", deckLabel: "Deck", deckAll: "Any deck",
    draw: "🎲 Draw cards", clear: "Clear", empty: "Loading decks…",
    noCards: "This deck has no cards (edition profile). Pick another.",
    pos: "Position", meaning: "Meaning", upright: "Upright", reversed: "Reversed",
    general: "Interpretation", source: "→ Open in deck",
    cards: "cards", min: "min", level: "level", when: "Use when",
    goToTool: "Online spread", applied: "Spread selected", chooseToDraw: "— pick a scheme below",
  },
};

const LEVEL = {
  ru: { start: "старт", mid: "средний", hard: "сложный" },
  uk: { start: "старт", mid: "середній", hard: "складний" },
  en: { start: "start", mid: "intermediate", hard: "advanced" },
};

const POS_NAME = {
  ru: {
    0: "Ситуация", 1: "Прошлое", 2: "Настоящее", 3: "Будущее", 4: "Корень", 5: "Перекрёсток", 6: "Основа", 7: "Опасение", 8: "Совет", 9: "Итог",
    10: "Путь А", 11: "Итог А", 12: "Путь Б", 13: "Итог Б",
    14: "Ты", 15: "Партнёр", 16: "Связь", 17: "Препятствие", 18: "Совет",
    19: "Сейчас", 20: "Ближние дни", 21: "Середина месяца", 22: "Итог месяца",
    23: "Дом", 24: "Надежда", 25: "Перемены", 26: "Силы", 27: "Совет",
  },
  uk: {
    0: "Ситуація", 1: "Минуле", 2: "Теперішнє", 3: "Майбутнє", 4: "Корінь", 5: "Перехрестя", 6: "Основа", 7: "Побоювання", 8: "Порада", 9: "Підсумок",
    10: "Шлях А", 11: "Підсумок А", 12: "Шлях Б", 13: "Підсумок Б",
    14: "Ти", 15: "Партнер", 16: "Зв'язок", 17: "Перешкода", 18: "Порада",
    19: "Зараз", 20: "Найближчі дні", 21: "Середина місяця", 22: "Підсумок місяця",
    23: "Дім", 24: "Надія", 25: "Зміни", 26: "Сили", 27: "Порада",
  },
  en: {
    0: "Situation", 1: "Past", 2: "Present", 3: "Future", 4: "Root", 5: "Crossing", 6: "Foundation", 7: "Fear", 8: "Advice", 9: "Outcome",
    10: "Path A", 11: "Outcome A", 12: "Path B", 13: "Outcome B",
    14: "You", 15: "Partner", 16: "Connection", 17: "Obstacle", 18: "Advice",
    19: "Now", 20: "Coming days", 21: "Mid-month", 22: "Monthly outcome",
    23: "Home", 24: "Hope", 25: "Changes", 26: "Strengths", 27: "Advice",
  },
};

/**
 * Каталог раскладов по образцу craft-cards/taro/rozklady.
 * n — карт, lvl — уровень, minutes — время, posNames — индексы названий позиций (начиная с 0).
 */
const SPREADS = [
  { id: "day", n: 1, lvl: "start", minutes: 2, posNames: [0] },
  { id: "yesno", n: 1, lvl: "start", minutes: 2, posNames: [0] },
  { id: "three", n: 3, lvl: "start", minutes: 5, posNames: [1, 2, 3] },
  { id: "sdi", n: 3, lvl: "start", minutes: 5, posNames: [0, 2, 3] },
  { id: "ab", n: 5, lvl: "mid", minutes: 10, posNames: [10, 11, 12, 13, 0] },
  { id: "relation", n: 6, lvl: "mid", minutes: 12, posNames: [14, 15, 16, 17, 1, 18] },
  { id: "love", n: 7, lvl: "mid", minutes: 15, posNames: [14, 15, 16, 17, 0, 2, 18] },
  { id: "month", n: 5, lvl: "start", minutes: 8, posNames: [19, 20, 21, 22, 18] },
  { id: "horseshoe", n: 7, lvl: "mid", minutes: 12, posNames: [1, 0, 2, 3, 23, 24, 27] },
  { id: "cross", n: 10, lvl: "hard", minutes: 20, posNames: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] },
  { id: "year", n: 12, lvl: "hard", minutes: 25, posNames: [19, 20, 21, 22, 23, 24, 25, 26, 27, 0, 2, 3] },
];

const SPREAD_META = {
  ru: {
    day: "Карта дня", yesno: "Да / Нет", three: "Три карты", sdi: "Ситуация – Действие – Итог",
    ab: "Выбор А или Б", relation: "Про отношения", love: "Про любовь", month: "Расклад на месяц",
    horseshoe: "Подкова", cross: "Кельтский крест", year: "Год впереди",
  },
  uk: {
    day: "Картка дня", yesno: "Так / Ні", three: "Три карти", sdi: "Ситуація – Дія – Підсумок",
    ab: "Вибір А чи Б", relation: "Про стосунки", love: "Про кохання", month: "Розклад на місяць",
    horseshoe: "Підкова", cross: "Кельтський хрест", year: "Рік попереду",
  },
  en: {
    day: "Daily card", yesno: "Yes / No", three: "Three cards", sdi: "Situation – Action – Outcome",
    ab: "Choice A or B", relation: "About a relationship", love: "About love", month: "Month ahead",
    horseshoe: "Horseshoe", cross: "Celtic cross", year: "Year ahead",
  },
};

const SPREAD_WHEN = {
  ru: {
    day: "для вопроса «что меня ждёт сегодня»", yesno: "для чёткого ответа да/нет",
    three: "для краткого взгляда на прошлое–настоящее–будущее",
    sdi: "когда есть ситуация и нужно понять, что делать дальше",
    ab: "когда стоишь перед выбором из двух путей",
    relation: "чтобы разобраться в отношениях с близким человеком",
    love: "для глубокого разбора любовной связки",
    month: "чтобы наметить план месяца", horseshoe: "для обзора ключевой недели",
    cross: "для полной картины вопроса — классика вопроса",
    year: "для годового прогноза",
  },
  uk: {
    day: "для запитання «що на мене чекає сьогодні»", yesno: "для чіткої відповіді так/ні",
    three: "для короткого погляду на минуле–теперішнє–майбутнє",
    sdi: "коли є ситуація і треба зрозуміти, що робити далі",
    ab: "коли стоїш перед вибором з двох шляхів",
    relation: "щоб розібратися у стосунках з близькою людиною",
    love: "для глибокого розбору любовного зв'язку",
    month: "щоб намітити план місяця", horseshoe: "для огляду ключового тижня",
    cross: "для повної картини питання — класика запитання",
    year: "для річного прогнозу",
  },
  en: {
    day: "for the question «what awaits me today»", yesno: "for a clear yes/no answer",
    three: "for a quick look at past–present–future",
    sdi: "when you have a situation and need to know what to do next",
    ab: "when you face a choice between two paths",
    relation: "to understand a relationship with a close person",
    love: "for a deep look at a love bond",
    month: "to plan the month ahead", horseshoe: "for an overview of a key week",
    cross: "for a full picture of a question — the classic layout",
    year: "for a yearly forecast",
  },
};

/** Сторінка розкладів: каталог схем (вкладка) + випадкові карти онлайн. */
export default function SpreadsPage() {
  const [lang, setLang] = useState("uk");
  const [decks, setDecks] = useState([]);
  const [deckId, setDeckId] = useState(null);
  const [spreadId, setSpreadId] = useState("three");
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const t = T[lang];

  useEffect(() => {
    getJSON("/decks").then((ds) => {
      if (!Array.isArray(ds)) return;
      setDecks(ds);
    }).catch(() => {});
  }, []);

  const draw = async () => {
    setLoading(true);
    try {
      const s = SPREADS.find((x) => x.id === spreadId) || SPREADS[0];
      const out = [];
      const seen = new Set();
      const fill = async () => {
        const params = deckId ? `?deck_id=${deckId}` : "";
        const c = await getJSON(`/cards/random${params}`);
        if (c?.id && !seen.has(c.id)) { seen.add(c.id); out.push(c); }
        else { out.push(c); }
      };
      for (let i = 0; i < s.n; i++) await fill();
      setCards(out);
    } catch {} finally {
      setLoading(false);
    }
  };

  const hasCards = decks.length === 0 || !deckId || (decks.find((d) => d.id === deckId)?.card_count ?? 0) > 0;
  const spread = SPREADS.find((s) => s.id === spreadId) || SPREADS[0];

  const chooseSpread = (id) => {
    setSpreadId(id);
    setCards([]);
    setTimeout(() => document.getElementById("spread-tool")?.scrollIntoView({ behavior: "smooth", block: "start" }), 80);
  };

  return (
    <>
      <nav className="nav">
        <div className="wrap nav-inner">
          <a className="brand" href="/">✦ AI-<b>Arcanum</b></a>
          <div className="nav-links">
            <a href="/#decks">Значення карт</a>
            <a className="active" href="/spreads">Види розкладів</a>
            <a href="/articles">Гайди і статті</a>
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
          <span className="num">🃏</span>
          <div><h2 style={{ margin: 0 }}>{t.title}</h2><p>{t.sub}</p></div>
        </div>

        <div className="grid-arc" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 14, marginBottom: 10 }}>
          {SPREADS.map((s) => (
            <div key={s.id} className={`sys-card spread-card${s.id === spreadId ? " spread-on" : ""}`} onClick={() => chooseSpread(s.id)}>
              <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 10 }}>
                <span className="n" style={{ minWidth: 46, textAlign: "center" }}>×{s.n}</span>
                <div style={{ minWidth: 0 }}>
                  <b style={{ display: "block", fontSize: 18 }}>{SPREAD_META[lang][s.id]}</b>
                  <div className="cat" style={{ marginTop: 4 }}>
                    {LEVEL[lang][s.lvl]} · ~{s.minutes} {t.min}
                  </div>
                </div>
              </div>
              <small>{t.when}: {SPREAD_WHEN[lang][s.id]}</small>
              {s.id === spreadId && (
                <div style={{ color: "var(--gold)", fontSize: 12, marginTop: 10 }}>✓ {t.applied}</div>
              )}
            </div>
          ))}
        </div>

        <div id="spread-tool" className="daily" style={{ marginTop: 26 }}>
          <h2>{t.goToTool}</h2>
          <p style={{ margin: "0 0 18px", color: "var(--text2)" }}>{SPREAD_META[lang][spread.id]} {t.chooseToDraw}</p>
          <div className="form-row" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 14, marginBottom: 10, maxWidth: 860 }}>
            <label style={{ color: "var(--muted)", fontSize: 13 }}>
              {t.deckLabel}
              <select value={deckId ?? ""} onChange={(e) => { setDeckId(e.target.value ? Number(e.target.value) : null); setCards([]); }}
                style={{ width: "100%", marginTop: 6, padding: "10px 12px", borderRadius: 10, background: "var(--panel)", color: "var(--text)", border: "1px solid var(--line)", fontSize: 14 }}>
                <option value="">{t.deckAll}</option>
                {decks.filter((d) => (d.card_count ?? 0) > 0).map((d) => (
                  <option key={d.id} value={d.id}>{pick(d, lang, "name").name || d.name} · {d.card_count}</option>
                ))}
              </select>
            </label>
            <label style={{ color: "var(--muted)", fontSize: 13 }}>
              {t.goToTool}
              <select value={spreadId} onChange={(e) => setSpreadId(e.target.value)}
                style={{ width: "100%", marginTop: 6, padding: "10px 12px", borderRadius: 10, background: "var(--panel)", color: "var(--text)", border: "1px solid var(--line)", fontSize: 14 }}>
                {SPREADS.map((s) => (
                  <option key={s.id} value={s.id}>{SPREAD_META[lang][s.id]} · ×{s.n}</option>
                ))}
              </select>
            </label>
            <div style={{ alignSelf: "end", display: "flex", gap: 8 }}>
              <button type="button" className="btn btn-gold" onClick={draw} disabled={loading || !hasCards}>
                {loading ? "…" : t.draw}
              </button>
              {cards.length > 0 && (
                <button type="button" className="btn btn-ghost" onClick={() => setCards([])}>{t.clear}</button>
              )}
            </div>
          </div>

          {!hasCards && <p style={{ color: "var(--muted)" }}>{t.noCards}</p>}

          <div className="drawer-grid" style={{ display: "grid", gap: 16, marginTop: 14 }}>
            {cards.map((c, i) => {
              const cc = pick(c, lang, "name", "meaning_general", "keywords_upright", "keywords_reversed");
              const rev = (c.id ?? 0) % 4 === 0;
              const posName = POS_NAME[lang][spread.posNames[i]] || "—";
              return (
                <div key={`${c.id}-${i}`} className="drawer" style={{ gridTemplateColumns: "120px 1fr" }}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={c.image_path} alt={cc.name} onError={(e) => (e.currentTarget.style.display = "none")} />
                  <div>
                    <div className="meta">{t.pos} {i + 1} · {posName} · {c.number} {rev ? `· ${t.reversed}` : `· ${t.upright}`}</div>
                    <h3>{cc.name}</h3>
                    <p><b>{rev && cc.keywords_reversed ? cc.keywords_reversed : cc.keywords_upright}</b></p>
                    {cc.meaning_general && <p style={{ whiteSpace: "pre-wrap" }}>{cc.meaning_general}</p>}
                    {c.deck_id && <a href={`/decks/${c.deck_id}?card=${c.id}`} style={{ color: "var(--gold-soft)", fontSize: 13 }}>{t.source}</a>}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </main>
      <footer className="footer">
        <div className="wrap"><span>✦ AI-Arcanum · Види розкладів</span></div>
      </footer>
    </>
  );
}