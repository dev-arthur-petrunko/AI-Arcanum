"use client";
import { useEffect, useState } from "react";
import { cardName, getJSON, pick } from "../lib/api";

const T = {
  ru: {
    title: "Расклады", sub: "Выбери колоду и расклад — карты лягут случайно, как в реальном чтении.",
    back: "← На главную", deckLabel: "Колода", deckAll: "Любая колода",
    spreadLabel: "Расклад", spreadDefault: "Без расклада — просто карта",
    draw: "🎲 Вытянуть карты", clear: "Очистить", empty: "Загрузка колод…",
    noCards: "В этой колоде нет карт (профиль издания). Выбери другую.",
    pos: "Позиция", meaning: "Значение", upright: "Прямо", reversed: "Наклон",
    general: "Толкование", source: "→ Открыть в колоде",
  },
  uk: {
    title: "Розклади", sub: "Обери колоду й розклад — карти ляжуть випадково, як у реальному читанні.",
    back: "← На головну", deckLabel: "Колода", deckAll: "Будь-яка колода",
    spreadLabel: "Розклад", spreadDefault: "Без розкладу — просто карта",
    draw: "🎲 Витягнути карти", clear: "Очистити", empty: "Завантаження колод…",
    noCards: "У цій колоді немає карт (профіль видання). Обери іншу.",
    pos: "Позиція", meaning: "Значення", upright: "Прямо", reversed: "Наклон",
    general: "Тлумачення", source: "→ Відкрити в колоді",
  },
  en: {
    title: "Spreads", sub: "Pick a deck and a spread — cards will fall randomly, like a real reading.",
    back: "← Home", deckLabel: "Deck", deckAll: "Any deck",
    spreadLabel: "Spread", spreadDefault: "No spread — just a card",
    draw: "🎲 Draw cards", clear: "Clear", empty: "Loading decks…",
    noCards: "This deck has no cards (edition profile). Pick another.",
    pos: "Position", meaning: "Meaning", upright: "Upright", reversed: "Reversed",
    general: "Interpretation", source: "→ Open in deck",
  },
};

const SPREADS = [
  { id: "one", positions: 1 },
  { id: "three", positions: 3 },
  { id: "five", positions: 5 },
  { id: "cross", positions: 10 },
];

const POS_NAME = {
  ru: { 0: "Ситуация", 1: "Прошлое", 2: "Настоящее", 3: "Будущее", 4: "Корень", 5: "Перекрёсток", 6: "Основа", 7: "Опасение", 8: "Совет", 9: "Итог" },
  uk: { 0: "Ситуація", 1: "Минуле", 2: "Теперішнє", 3: "Майбутнє", 4: "Корінь", 5: "Перехрестя", 6: "Основа", 7: "Побоювання", 8: "Порада", 9: "Підсумок" },
  en: { 0: "Situation", 1: "Past", 2: "Present", 3: "Future", 4: "Root", 5: "Crossing", 6: "Foundation", 7: "Fear", 8: "Advice", 9: "Outcome" },
};

/** Окрема сторінка розкладів: вибір колоди + випадкові карти. */
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
      // лише колоди з картами; спершу колоди з карт
      setDecks(ds);
    }).catch(() => {});
  }, []);

  const draw = async () => {
    setLoading(true);
    try {
      const n = (SPREADS.find((s) => s.id === spreadId) || SPREADS[0]).positions;
      const out = [];
      const seen = new Set();
      for (let i = 0; i < n; i++) {
        // унікальні карти без повторів у межах одного розкладу
        const params = deckId ? `?deck_id=${deckId}` : "";
        const c = await getJSON(`/cards/random${params}`);
        if (c?.id && !seen.has(c.id)) { seen.add(c.id); out.push(c); }
        else { out.push(c); }
      }
      setCards(out);
    } catch {} finally {
      setLoading(false);
    }
  };

  const hasCards = decks.length === 0 || !deckId || (decks.find((d) => d.id === deckId)?.card_count ?? 0) > 0;

  return (
    <>
      <nav className="nav">
        <div className="wrap nav-inner">
          <a className="brand" href="/">✦ AI-<b>Arcanum</b></a>
          <div className="nav-links">
            <a href="/articles">Статті / Статьи / Articles</a>
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
            {t.spreadLabel}
            <select value={spreadId} onChange={(e) => setSpreadId(e.target.value)}
              style={{ width: "100%", marginTop: 6, padding: "10px 12px", borderRadius: 10, background: "var(--panel)", color: "var(--text)", border: "1px solid var(--line)", fontSize: 14 }}>
              {SPREADS.map((s) => (
                <option key={s.id} value={s.id}>×{s.positions} cards</option>
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
            return (
              <div key={`${c.id}-${i}`} className="drawer" style={{ gridTemplateColumns: "120px 1fr" }}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={c.image_path} alt={cc.name} onError={(e) => (e.currentTarget.style.display = "none")} />
                <div>
                  <div className="meta">{t.pos} {i + 1} · {POS_NAME[lang][i] || "—"} · {c.number} {rev ? `· ${t.reversed}` : `· ${t.upright}`}</div>
                  <h3>{cc.name}</h3>
                  <p><b>{rev && cc.keywords_reversed ? cc.keywords_reversed : cc.keywords_upright}</b></p>
                  {cc.meaning_general && <p style={{ whiteSpace: "pre-wrap" }}>{cc.meaning_general}</p>}
                  {c.deck_id && <a href={`/decks/${c.deck_id}?card=${c.id}`} style={{ color: "var(--gold-soft)", fontSize: 13 }}>{t.source}</a>}
                </div>
              </div>
            );
          })}
        </div>
      </main>
      <footer className="footer">
        <div className="wrap"><span>✦ AI-Arcanum · Розклади</span></div>
      </footer>
    </>
  );
}