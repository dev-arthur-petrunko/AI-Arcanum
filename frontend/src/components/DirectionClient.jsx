"use client";
import { useEffect, useState } from "react";
import SiteNav from "./SiteNav";
import Reveal from "./Reveal";
import Scene3D from "./Scene3D";
import CardDetail from "./CardDetail";
import { cardName, getJSON } from "../lib/api";
import { subgroupInfo } from "../lib/subgroups";

const T = {
  ru: {
    cards: "Значения карт", practice: "Практика", guides: "Гайды",
    decks: "Колоды направления", decksSub: "Все карты колод направления — клик открывает значения.",
    showcase: "3D-витрина", showcaseSub: "Первые карты первой колоды направления.",
    systems: "Системы", open: "Открыть →", back: "← Все направления",
    cardsIn: "карт", studyBadge: "навчальна модель", partialBadge: "неполный набор",
    empty: "В этом направлении пока нет колод.",
  },
  uk: {
    cards: "Значення карт", practice: "Практика", guides: "Гайди",
    decks: "Колоди напрямку", decksSub: "Усі карти колод напрямку — клік відкриває значення.",
    showcase: "3D-вітрина", showcaseSub: "Перші карти першої колоди напрямку.",
    systems: "Системи", open: "Відкрити →", back: "← Усі напрямки",
    cardsIn: "карт", studyBadge: "навчальна модель", partialBadge: "неповний набір",
    empty: "У цьому напрямку поки немає колод.",
  },
  en: {
    cards: "Card meanings", practice: "Practice", guides: "Guides",
    decks: "Direction decks", decksSub: "All deck cards at once — click opens the meaning.",
    showcase: "3D showcase", showcaseSub: "First cards of the direction's first deck.",
    systems: "Systems", open: "Open →", back: "← All directions",
    cardsIn: "cards", studyBadge: "study model", partialBadge: "partial set",
    empty: "No decks in this direction yet.",
  },
};

/** Клієнт напрямку: вкладки + 3D-вітрина + сітка колод + системи. */
export default function DirectionClient({ direction, systems, decks }) {
  const [lang, setLang] = useState("uk");
  const [theme, setTheme] = useState("dark");
  const [fan, setFan] = useState([]);
  const [fanDeck, setFanDeck] = useState(null);
  const [allCards, setAllCards] = useState([]);
  const [selected, setSelected] = useState(null);
  const t = T[lang];

  useEffect(() => {
    try {
      const saved = localStorage.getItem("arcanum-theme");
      if (saved === "light" || saved === "dark") {
        setTheme(saved);
        document.documentElement.dataset.theme = saved;
      }
    } catch {}
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
    const first = (decks || []).find((d) => d.cards > 0);
    if (!first) return;
    setFanDeck(first);
    getJSON(`/cards?deck_id=${first.id}&limit=7`).then((cs) => {
      if (Array.isArray(cs)) setFan(cs);
    }).catch(() => {});
  }, [decks]);

  // усі карти напрямку одразу (колоди напрямку — картинки без кліку)
  useEffect(() => {
    if (!decks?.length) { setAllCards([]); return; }
    let alive = true;
    Promise.all((decks || []).map((d) =>
      getJSON(`/cards?deck_id=${d.id}&limit=200`).catch(() => []),
    )).then((groups) => {
      if (!alive) return;
      setAllCards(groups.flat());
    });
    return () => { alive = false; };
  }, [decks]);

  const totalCards = (decks || []).reduce((a, d) => a + (d.cards || 0), 0);

  function openCard(c) {
    // «Гадальні» ведуть на окрему сторінку карти, решта — модалка
    if (direction.slug === "divination") {
      window.location.href = `/directions/divination/card/${c.id}`;
      return;
    }
    setSelected(c);
  }

  return (
    <>
      <SiteNav lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} />
      <main className="wrap" style={{ paddingTop: 110, paddingBottom: 60 }}>
        <div className="crumbs">
          <a href="/">{lang === "en" ? "Home" : lang === "ru" ? "Главная" : "Головна"}</a>
          <span>›</span>
          <span>{direction.title[lang] || direction.title.uk}</span>
        </div>
        <header className="page-hero sparkle-field" style={{ padding: "34px 30px", marginBottom: 6 }}>
          <span style={{ fontSize: 40 }}>{direction.icon}</span>
          <h1 style={{ margin: "10px 0 6px", fontSize: "clamp(34px, 5vw, 56px)" }}>
            {direction.title[lang] || direction.title.uk}
          </h1>
          <p style={{ color: "var(--muted)", maxWidth: 680, lineHeight: 1.65 }}>
            {direction.desc[lang] || direction.desc.uk}
          </p>
          <p style={{ color: "var(--gold-soft)", fontSize: 14 }}>
            {(systems || []).length} · {t.systems.toLowerCase()} · {(decks || []).length} · {t.decks.toLowerCase()} · {totalCards} · {t.cardsIn}
          </p>
        </header>

        <nav className="dir-tabs" aria-label={direction.title.uk}>
          <a href={`/directions/${direction.slug}`} className="active">{t.cards}</a>
          <a href={`/directions/${direction.slug}/spreads`}>{t.practice}</a>
          <a href={`/directions/${direction.slug}/guides`}>{t.guides}</a>
        </nav>

        {direction.slug !== "divination" && fan.length > 0 && (
          <Reveal>
            <section className="section" style={{ paddingTop: 20 }}>
              <div className="section-head">
                <span className="num">✦</span>
                <div>
                  <h2>{t.showcase}</h2>
                  <p>{t.showcaseSub} — {fanDeck?.name}</p>
                </div>
              </div>
              <Scene3D cards={fan} lang={lang} theme={theme} onSelect={openCard} />
            </section>
          </Reveal>
        )}

        <Reveal>
          <section className="section">
            <div className="section-head">
              <span className="num">{direction.icon}</span>
              <div><h2>{t.decks}</h2><p>{t.decksSub}</p></div>
            </div>
            {(decks || []).length === 0 ? (
              <p style={{ color: "var(--muted)" }}>{t.empty}</p>
            ) : (
              (() => {
                // групуємо колоди одного directory_group під спільним підзаголовком
                const groups = [];
                const byGroup = new Map();
                (decks || []).forEach((d) => {
                  const g = d.directory_group || null;
                  if (g) {
                    if (!byGroup.has(g)) {
                      const entry = { group: g, decks: [] };
                      byGroup.set(g, entry);
                      groups.push(entry);
                    }
                    byGroup.get(g).decks.push(d);
                  } else {
                    groups.push({ group: null, decks: [d] });
                  }
                });
                return groups.map((gr, gi) => {
                  const gi2 = subgroupInfo(gr.group, lang);
                  const inner = (
                    <>
                      {gr.group && (
                        <div style={{ margin: "26px 0 14px" }}>
                          <h3 className="dir-group" style={{ letterSpacing: ".08em" }}>{gi2?.title || gr.group}</h3>
                          {gi2?.history && (
                            <p style={{ margin: "6px 0 0", color: "var(--muted)", fontSize: 14, lineHeight: 1.55, maxWidth: 760 }}>
                              {gi2.history}
                            </p>
                          )}
                        </div>
                      )}
                      {direction.slug === "divination" ? (
                        // «Гадальні»: кожна колода — на власній сторінці /decks/<id>
                        <div className="grid-decks" key={gr.group || gi}>
                          {gr.decks.map((d) => (
                            <div key={d.id} className="deck-card">
                              {d.cover ? (
                                // eslint-disable-next-line @next/next/no-img-element
                                <a href={`/decks/${d.id}`} style={{ display: "block" }}>
                                  <img src={d.cover} alt={d.name} className="dd-cover" />
                                </a>
                              ) : (
                                <a href={`/decks/${d.id}`} style={{ display: "block" }}>
                                  <div className="dd-fallback">✦</div>
                                </a>
                              )}
                              <a href={`/decks/${d.id}`} style={{ color: "inherit", textDecoration: "none" }}>
                                <b>{d.name}</b>
                              </a>
                              <span style={{ display: "block", margin: "4px 0 10px" }}>{d.cards} · {t.cardsIn}</span>
                              <div style={{ display: "flex", gap: 8 }}>
                                <a className="btn btn-ghost" href={`/decks/${d.id}`} style={{ flex: 1, padding: "7px 10px", fontSize: 13, textAlign: "center" }}>{t.cards}</a>
                                <a className="btn btn-ghost" href={`/decks/${d.id}?tab=3d`} style={{ flex: 1, padding: "7px 10px", fontSize: 13, textAlign: "center" }}>{t.showcase}</a>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        gr.decks.map((d) => {
                          const dCards = (allCards || []).filter((c) => c.deck_id === d.id);
                          return (
                            <div key={d.id} className="deck-block" style={{ marginBottom: 26 }}>
                              <div className="section-head" style={{ marginBottom: 12 }}>
                                <span className="num">
                                  {d.cover ? (
                                    // eslint-disable-next-line @next/next/no-img-element
                                    <img src={d.cover} alt="" style={{ width: 46, height: 46, objectFit: "cover", borderRadius: 8, verticalAlign: "middle" }} />
                                  ) : "✦"}
                                </span>
                                <div>
                                  <h3 style={{ margin: 0 }}>
                                    <a href={`/decks/${d.id}`} style={{ color: "inherit", textDecoration: "none" }}>
                                      {d.name} ↗
                                    </a>
                                  </h3>
                                  <p style={{ margin: 0, color: "var(--muted)" }}>{dCards.length} · {t.cardsIn}</p>
                                </div>
                              </div>
                              {dCards.length === 0 ? (
                                <p style={{ color: "var(--muted)" }}>{t.empty}</p>
                              ) : (
                                <div className="grid-cards">
                                  {dCards.map((c) => (
                                    <div key={c.id} className="mini-card" onClick={() => openCard(c)}>
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
                              )}
                            </div>
                          );
                        })
                      )}
                    </>
                  );
                  return <div key={gi}>{inner}</div>;
                });
              })()
            )}
            <div style={{ marginTop: 14 }}>
              <CardDetail card={selected} lang={lang} onClose={() => setSelected(null)} />
            </div>
          </section>
        </Reveal>

        <Reveal>
          <div className="divider">✦ ✦ ✦</div>
          <section className="section">
            <div className="section-head">
              <span className="num">§</span>
              <div><h2>{t.systems}</h2></div>
            </div>
            <div className="chips" style={{ marginBottom: 0 }}>
              {(systems || []).map((s) => (
                <span key={s.id} className="chip" style={{ cursor: "default" }}>
                  {s.name} · {s.cards} {t.cardsIn}
                </span>
              ))}
            </div>
            <p style={{ marginTop: 22 }}>
              <a className="btn btn-ghost" href="/" style={{ display: "inline-block" }}>{t.back}</a>
            </p>
          </section>
        </Reveal>
      </main>
      <footer className="footer">
        <div className="wrap"><span>✦ AI-Arcanum · {direction.title[lang] || direction.title.uk}</span></div>
      </footer>
    </>
  );
}
