"use client";
import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import Scene3D from "./Scene3D";
import CardDetail from "./CardDetail";
import CatalogClient from "./CatalogClient";
import InteractiveCardModal from "./InteractiveCardModal";
import { cardName, getJSON, pick } from "../lib/api";
import { subgroupInfo } from "../lib/subgroups";
import { hasZones } from "../lib/rws";

const T = {
  ru: {
    back: "← Все колоды", searchPh: "Поиск по колоде…", found: "Найдено", pick: "Кликни карту в 3D или в списке ↓",
    lucky: "🎲 Случайная карта колоды", studyBadge: "навчальна модель", partialBadge: "неполный набор",
    valuesBlock: "Значение карт", showcaseBlock: "3D-витрина", cardsIn: "карт", historyBlock: "История",
    relatedBlock: "Из чего состоят гексаграммы",
    suits: { wands: "Жезлы", cups: "Кубки", swords: "Мечи", pentacles: "Пентакли" },
  },
  uk: {
    back: "← Усі колоди", searchPh: "Пошук по колоді…", found: "Знайдено", pick: "Клікни карту в 3D або в списку ↓",
    lucky: "🎲 Випадкова карта колоди", studyBadge: "навчальна модель", partialBadge: "неповний набір",
    valuesBlock: "Значення карт", showcaseBlock: "3D-вітрина", cardsIn: "карт", historyBlock: "Історія",
    relatedBlock: "Із чого складаються гексаграми",
    suits: { wands: "Жезли", cups: "Кубки", swords: "Мечі", pentacles: "Пентаклі" },
  },
  en: {
    back: "← All decks", searchPh: "Search this deck…", found: "Found", pick: "Click a card in 3D or in the list ↓",
    lucky: "🎲 Random card of this deck", studyBadge: "study model", partialBadge: "partial set",
    valuesBlock: "Card meanings", showcaseBlock: "3D showcase", cardsIn: "cards", historyBlock: "History",
    relatedBlock: "What hexagrams are made of",
    suits: { wands: "Wands", cups: "Cups", swords: "Swords", pentacles: "Pentacles" },
  },
};

/** Короткий ключ карти: перша фраза keywords_upright (або theme). */
function shortKey(c, lang) {
  const tr = (c.translations || {})[lang] || {};
  const kw = tr.keywords_upright || c.keywords_upright || "";
  if (kw) return kw.split(",")[0].trim();
  return tr.theme || c.theme || "";
}

/** Згруповані карти: старші + молодші по мастях. */
function groupByArcana(cards) {
  const majors = cards.filter((c) => /Старш/i.test(c.arcana_type || ""));
  const minors = cards.filter((c) => !/Старш/i.test(c.arcana_type || "") && c.suit_code);
  const suitOrder = { wands: 0, cups: 1, swords: 2, pentacles: 3 };
  const bySuit = new Map();
  for (const c of minors) {
    if (!bySuit.has(c.suit_code)) bySuit.set(c.suit_code, []);
    bySuit.get(c.suit_code).push(c);
  }
  const suits = [...bySuit.entries()]
    .sort((a, b) => (suitOrder[a[0]] ?? 9) - (suitOrder[b[0]] ?? 9))
    .map(([code, list]) => ({ code, list }));
  return { majors, suits };
}

/** Клієнт сторінки колоди: 3D-віяло або сітка значень арканів, пошук, розбір, ?card=підсвітка.
 *  relatedDeck/relatedCards — «будівельна» колода (напр. Багуа → триграми на сторінці І-Цзин). */
export default function DeckClient({ deck, initialCards, relatedDeck, relatedCards, lang, setLang, theme = "dark", isDivination, catalogMode }) {
  const t = T[lang];
  const params = useSearchParams();
  const [cards, setCards] = useState(initialCards);
  const [selected, setSelected] = useState(null);
  const [interactive, setInteractive] = useState(null);
  const [q, setQ] = useState("");

  const hasMajors = useMemo(() => cards.some((c) => /Старш/i.test(c.arcana_type || "")), [cards]);
  const groups = useMemo(() => groupByArcana(cards), [cards]);
  const flat = !hasMajors; // колоди без Старших/мастей — показуємо усі карти сіткою одразу

  // ?card=<id> — прямий вхід на карту (кнопка «Мені пощастить»)
  useEffect(() => {
    const id = params.get("card");
    if (!id) return;
    if (isDivination) {
      window.location.href = `/directions/divination/card/${id}`;
      return;
    }
    getJSON(`/cards/${id}`).then((c) => {
      if (c?.id) {
        if (hasZones(String(c.number ?? ""))) setInteractive(c);
        else setSelected(c);
      }
    }).catch(() => {});
  }, [params]);

  async function search(e) {
    e?.preventDefault();
    const query = `/cards?deck_id=${deck.id}&limit=200${q.trim().length >= 2 ? `&q=${encodeURIComponent(q.trim())}` : ""}`;
    try {
      const d = await getJSON(query);
      if (Array.isArray(d)) setCards(d);
    } catch {}
  }

  async function luckyDeck() {
    try {
      const c = await getJSON(`/cards/random?deck_id=${deck.id}`);
      if (c?.id) {
        if (hasZones(String(c.number ?? ""))) {
          setInteractive(c);
          return;
        }
        if (isDivination) {
          window.location.href = `/directions/divination/card/${c.id}`;
          return;
        }
        const full = await getJSON(`/cards/${c.id}?lang=${lang}`);
        setSelected(full);
      }
    } catch {}
  }

  /** Клік по карті: RWS з зонами — інтерактив; «Гадальні» — окрема сторінка; решта — модальне вікно. */
  function pickCard(c) {
    if (hasZones(String(c?.number ?? ""))) {
      setInteractive(c);
      return;
    }
    if (isDivination) {
      window.location.href = `/directions/divination/card/${c.id}`;
      return;
    }
    setSelected(c);
  }

  const deckName = pick(deck, lang, "name", "description").name || deck.name;
  const deckDesc = pick(deck, lang, "description").description || deck.description;
  const deckNote = pick(deck, lang, "note").note || null;
  const gi = deck?.directory_group
    ? subgroupInfo(deck.directory_group, lang)
    : deck?.system?.category || "";

  return (
    <>
      <a className="btn btn-ghost" href="/#decks" style={{ display: "inline-block", marginBottom: 18 }}>{t.back}</a>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        <span className="badge badge-study">{t.studyBadge}</span>
        {deck.is_partial && <span className="badge badge-partial">{t.partialBadge}</span>}
      </div>
      {deckNote && (
        <p className="deck-note" style={{ maxWidth: 720, marginTop: 12 }}>⚠️ {deckNote}</p>
      )}
      <div className="section-head">
        <span className="num">✦</span>
        <div>
          <h2 style={{ fontSize: "clamp(34px,5vw,56px)", margin: 0 }}>{deckName}</h2>
          <p>{[deck.author, deck.year].filter(Boolean).join(" · ")}</p>
          {deckDesc && <p style={{ maxWidth: 720 }}>{deckDesc}</p>}
        </div>
      </div>
      {gi && gi.history && (
        <section className="section" style={{ padding: 0, marginBottom: 22 }}>
          <div className="section-head" style={{ marginBottom: 8 }}>
            <span className="num">☯</span>
            <div>
              <h3 style={{ margin: 0, fontSize: 20 }}>{t.historyBlock}</h3>
            </div>
          </div>
          <p style={{ maxWidth: 760, color: "var(--muted)", lineHeight: 1.65 }}>{gi.history}</p>
        </section>
      )}
      <div style={{ display: "flex", gap: 10, marginBottom: 14, flexWrap: "wrap" }}>
        <form onSubmit={search} className="search-row" style={{ flex: 1, minWidth: 240, margin: 0 }}>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder={t.searchPh} />
          <button type="submit">🔎</button>
        </form>
        <button className="btn btn-gold" onClick={luckyDeck}>{t.lucky}</button>
      </div>

      <section className="section">
        <div className="section-head">
          <span className="num">✦</span>
          <div>
            <h3 style={{ margin: 0, fontSize: 24 }}>{t.showcaseBlock}</h3>
          </div>
        </div>
        <Scene3D cards={cards} lang={lang} theme={theme} onSelect={pickCard} />
        <p style={{ color: "var(--muted)", fontSize: 13, marginBottom: 14 }}>{t.pick}</p>
      </section>

      <div className="divider">✦ ✦ ✦</div>

      <section className="section" style={{ paddingTop: 0 }}>
        {catalogMode ? (
          <CatalogClient cards={cards} lang={lang} onOpen={pickCard} />
        ) : flat ? (
          <>
            <p className="arc-title"><b>{t.valuesBlock}</b> <span className="arc-count">{cards.length}</span></p>
            <div className="grid-cards">
              {cards.map((c) => (
                <div key={c.id} className="mini-card" onClick={() => pickCard(c)}>
                  {c.image_path && (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img src={c.image_path} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                      style={{ width: "100%", borderRadius: 8, marginBottom: 8 }} />
                  )}
                  <b>{cardName(c, lang)}</b>
                  {shortKey(c, lang) && <span className="arc-key">{shortKey(c, lang)}</span>}
                </div>
              ))}
            </div>
          </>
        ) : (
          <>
            {groups.majors.length > 0 && (
              <>
                <p className="arc-title"><b>{t.valuesBlock} · 0</b> <span className="arc-count">{groups.majors.length}</span></p>
                <div className="grid-cards">
                  {groups.majors.map((c) => (
                    <div key={c.id} className="mini-card" onClick={() => pickCard(c)}>
                      {c.image_path && (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img src={c.image_path} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                          style={{ width: "100%", borderRadius: 8, marginBottom: 8 }} />
                      )}
                      <b className="arc-no">{c.number}</b>
                      <b>{cardName(c, lang)}</b>
                      {shortKey(c, lang) && <span className="arc-key">{shortKey(c, lang)}</span>}
                    </div>
                  ))}
                </div>
              </>
            )}
            {groups.suits.map((s) => (
              <div key={s.code} style={{ marginTop: 22 }}>
                <p className="arc-title"><b>{t.suits[s.code] || s.code}</b> <span className="arc-count">{s.list.length}</span></p>
                <div className="grid-cards">
                  {s.list.map((c) => (
                    <div key={c.id} className="mini-card" onClick={() => pickCard(c)}>
                      {c.image_path && (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img src={c.image_path} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                          style={{ width: "100%", borderRadius: 8, marginBottom: 8 }} />
                      )}
                      <b>{cardName(c, lang)}</b>
                      {shortKey(c, lang) && <span className="arc-key">{shortKey(c, lang)}</span>}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </>
        )}
      </section>

      <div style={{ marginTop: 18 }}>
        <CardDetail card={selected} lang={lang} onClose={() => setSelected(null)} />
        <InteractiveCardModal card={interactive} lang={lang} onClose={() => setInteractive(null)} />
      </div>
      {relatedDeck?.id && relatedCards?.length > 0 && (
        <section className="section" style={{ marginTop: 30, paddingTop: 0 }}>
          <div className="divider">✦ ✦ ✦</div>
          <div className="section-head">
            <span className="num">☰</span>
            <div>
              <h2>{t.relatedBlock}</h2>
              <p>{relatedDeck.name} · {relatedCards.length} {t.cardsIn || ""}</p>
            </div>
          </div>
          <div className="grid-cards">
            {relatedCards.map((c) => (
              <div key={c.id} className="mini-card" onClick={() => pickCard(c)}>
                {c.image_path && (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={c.image_path} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                    style={{ width: "100%", borderRadius: 8, marginBottom: 8 }} />
                )}
                <b>{cardName(c, lang)}</b>
                <span>{c.number} · {c.arcana_type || c.category || ""}</span>
              </div>
            ))}
          </div>
        </section>
      )}
      {!flat && (
        <>
          <p style={{ color: "var(--muted)", fontSize: 13, marginTop: 16 }}>{t.found}: {cards.length}</p>
          <div className="grid-cards" style={{ marginBottom: 10 }}>
            {cards.map((c) => (
              <div key={c.id} className="mini-card" onClick={() => pickCard(c)}>
                {c.image_path && (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={c.image_path} alt="" onError={(e) => (e.currentTarget.style.display = "none")}
                    style={{ width: "100%", borderRadius: 8, marginBottom: 8 }} />
                )}
                <b>{cardName(c, lang)}</b>
                <span>{c.number} · {c.arcana_type}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </>
  );
}

export function DeckClientSuspense(props) {
  return (
    <Suspense>
      <DeckClient {...props} />
    </Suspense>
  );
}