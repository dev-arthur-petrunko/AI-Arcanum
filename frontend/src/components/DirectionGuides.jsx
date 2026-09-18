"use client";
import { useEffect, useState } from "react";
import SiteNav from "./SiteNav";
import { getJSON } from "../lib/api";
import { articleBelongs } from "../lib/directions";

/** Методика COPE · BASIC Ph — переїхала з головної сюди (рівень напрямку, не hero).
 *  Рамка колоди COPE (О. Аялон, OH Cards Institute); чесна позначка: готових
 *  «значень» 88 карт нема — є 6 каналів, до яких терапевт відносить образ. */
const COPE = {
  slug: "cope-basic-ph",
  title: { ru: "Методика COPE · BASIC Ph", uk: "Методика COPE · BASIC Ph", en: "COPE method · BASIC Ph" },
  sub: {
    ru: "Шесть ресурсных каналов — рамка колоды COPE (О. Аялон, OH Cards Institute).",
    uk: "Шість ресурсних каналів — рамка колоди COPE (О. Аялон, OH Cards Institute).",
    en: "Six resource channels — the frame of the COPE deck (O. Ayalon, OH Cards Institute).",
  },
  caveat: {
    ru: "Честно: у методики COPE нет готовых «значений» образов, как в Таро. Есть 6 каналов, к которым терапевт относит образ в работе, — они вошли в объединённую терапевтическую колоду.",
    uk: "Чесно: у методики COPE нема готових «значень» образів, як у Таро. Є 6 каналів, до яких терапевт відносить образ у роботі, — вони увійшли в об'єднану терапевтичну колоду.",
    en: "Honest note: the COPE method has no ready-made “meanings” for images like Tarot does. There are 6 channels a therapist maps an image to — they are part of the combined therapeutic deck.",
  },
  srcDocs: { ru: "Официальные источники методики", uk: "Офіційні джерела методики", en: "Official method sources" },
  pdfLabel: {
    ru: "Методичка О. Аялон (PDF, OH Institute)",
    uk: "Методичка О. Аялон (PDF, OH Institute)",
    en: "O. Ayalon manual (PDF, OH Institute)",
  },
  openDeck: { ru: "Открыть объединённую колоду →", uk: "Відкрити об'єднану колоду →", en: "Open the combined deck →" },
  links: [
    { href: "https://www.oh-cards-institute.org/wp-content/uploads/2012/06/Ofra-Ayalon-Healing-Trauma-with-Metaphoric-Cards.pdf", label: null },
    { href: "https://oh-cards.com/cope/", label: "oh-cards.com/cope" },
    { href: "https://www.theohcards.com/ohcards/cope-cards", label: "theohcards.com" },
    { href: "http://projective-cards.ru/cope/", label: "projective-cards.ru" },
  ],
};

const T = {
  ru: { title: "Гайды и статьи", sub: "Материалы направления: руководства, история, практика чтения карт.", back: "← К направлению", empty: "Для этого направления статей пока нет — загляни в общий раздел.", all: "Все гайды и статьи →", src: "📜" },
  uk: { title: "Гайди і статті", sub: "Матеріали напрямку: керівництва, історія, практика читання карт.", back: "← До напрямку", empty: "Для цього напрямку статей поки немає — зазирни до загального розділу.", all: "Усі гайди і статті →", src: "📜" },
  en: { title: "Guides and articles", sub: "Direction materials: manuals, history, card reading practice.", back: "← Back to direction", empty: "No articles for this direction yet — see the general section.", all: "All guides & articles →", src: "📜" },
};

/** /directions/{slug}/guides — гайди напрямку (фільтр GET /articles) + COPE-стаття для therapeutic. */
export default function DirectionGuides({ direction, decks, initialArticles }) {
  const [lang, setLang] = useState("uk");
  const [theme, setTheme] = useState("dark");
  const [articles, setArticles] = useState(initialArticles || []);
  const t = T[lang];

  useEffect(() => {
    try {
      const saved = localStorage.getItem("arcanum-theme");
      if (saved === "light" || saved === "dark") {
        setTheme(saved);
        document.documentElement.dataset.theme = saved;
      }
    } catch {}
    getJSON("/articles")
      .then((d) => Array.isArray(d) && setArticles(d))
      .catch(() => {});
  }, []);

  function toggleTheme() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    try {
      localStorage.setItem("arcanum-theme", next);
      document.documentElement.dataset.theme = next;
    } catch {}
  }

  const mine = (articles || []).filter((a) => articleBelongs(a, direction));
  const copeDeck = (decks || []).find((d) => (d.name || "").includes("Терапевтична колода"));
  const showCope = direction.slug === "therapeutic";

  return (
    <>
      <SiteNav lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} active="articles" />
      <main className="wrap" style={{ paddingTop: 110, paddingBottom: 60 }}>
        <div className="crumbs">
          <a href={`/directions/${direction.slug}`}>{direction.title[lang] || direction.title.uk}</a>
          <span>›</span>
          <span>{t.title}</span>
        </div>
        <div className="section-head">
          <span className="num">{direction.icon}</span>
          <div><h2 style={{ margin: 0 }}>{t.title}</h2><p>{t.sub}</p></div>
        </div>

        {showCope && (
          <details className="article-card glow-border" open>
            <summary>
              <span>{COPE.title[lang]}</span>
              <span className="sys">COPE</span>
            </summary>
            <div className="article-body">
              {COPE.sub[lang]}
              {"\n\n"}⚖ {COPE.caveat[lang]}
              <div className="src">📚 {COPE.srcDocs[lang]}:</div>
              <div className="ref-links">
                {COPE.links.map((l) => (
                  <a key={l.href} className="chip" href={l.href} target="_blank" rel="noreferrer">
                    📄 {l.label || COPE.pdfLabel[lang]}
                  </a>
                ))}
              </div>
              {copeDeck && (
                <p><a className="btn btn-gold" href={`/decks/${copeDeck.id}`} style={{ display: "inline-block", marginTop: 8 }}>{COPE.openDeck[lang]}</a></p>
              )}
            </div>
          </details>
        )}

        {mine.length === 0 && !showCope ? (
          <p style={{ color: "var(--muted)" }}>{t.empty}</p>
        ) : (
          <div style={{ marginTop: 8 }}>
            {mine.map((a) => (
              <details key={a.id} className="article-card">
                <summary>
                  <span>{a.translations?.[lang]?.title || a.title}</span>
                  <span className="sys">{a.system}</span>
                </summary>
                <div className="article-body">
                  {a.translations?.[lang]?.body || a.body}
                  {a.source_reference && <div className="src">{t.src} {a.source_reference}</div>}
                </div>
              </details>
            ))}
          </div>
        )}

        <p style={{ marginTop: 22, display: "flex", gap: 10, flexWrap: "wrap" }}>
          <a className="btn btn-ghost" href="/articles" style={{ display: "inline-block" }}>{t.all}</a>
          <a className="btn btn-ghost" href={`/directions/${direction.slug}`} style={{ display: "inline-block" }}>{t.back}</a>
        </p>
      </main>
      <footer className="footer">
        <div className="wrap"><span>✦ AI-Arcanum · {direction.title[lang] || direction.title.uk}</span></div>
      </footer>
    </>
  );
}
