"use client";
import { pick } from "../lib/api";

const SRC = {
  ru: "см. backend/Database/sources_log.md",
  uk: "див. backend/Database/sources_log.md",
  en: "see backend/Database/sources_log.md",
};

/** Розбір однієї карти: назва, ключові слова, значення, звʼязки. */
export default function CardDetail({ card, lang, emptyText }) {
  if (!card) return <p style={{ color: "var(--muted)" }}>{emptyText}</p>;
  const c = pick(card, lang, "name", "description", "theme");
  return (
    <div className="drawer" id="card-detail">
      {card.image_path && card.id > 0 ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={card.image_path} alt={c.name} onError={(e) => (e.currentTarget.style.display = "none")} />
      ) : <div style={{ fontSize: 90, textAlign: "center" }}>✦</div>}
      <div>
        <div className="meta">{card.number} · {card.arcana_type || card.category || "—"}</div>
        <h3>{c.name}</h3>
        {c.theme && <p style={{ color: "var(--gold-soft)" }}>◈ {c.theme}</p>}
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
          <div className="src">📜 {card.translations?.en?.source_reference || SRC[lang]}</div>
        )}
      </div>
    </div>
  );
}
