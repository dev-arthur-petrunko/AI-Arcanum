"use client";
import { useState } from "react";
import { pick } from "../lib/api";

const SRC = {
  ru: "см. backend/Database/sources_log.md",
  uk: "див. backend/Database/sources_log.md",
  en: "see backend/Database/sources_log.md",
};
const MORE = { ru: "Читать далее ↓", uk: "Читати далі ↓", en: "Read more ↓" };
const LESS = { ru: "Свернуть ↑", uk: "Згорнути ↑", en: "Collapse ↑" };
const CUT = 600;

/** Розбір однієї карти: ВСІ текстові поля через pick() (поважає lang),
    довгі тексти — зі згортанням. */
export default function CardDetail({ card, lang, emptyText }) {
  const [open, setOpen] = useState(false);
  if (!card) return <p style={{ color: "var(--muted)" }}>{emptyText}</p>;
  const c = pick(
    card, lang, "name", "description", "theme",
    "keywords_upright", "keywords_reversed", "meaning_general",
    "meaning_love", "meaning_career", "meaning_health", "symbolism"
  );
  const long = (c.meaning_general || "").length > CUT;
  const shown = !long || open ? c.meaning_general : `${c.meaning_general.slice(0, CUT)}…`;
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
        <p><b>{c.keywords_upright}</b></p>
        {c.keywords_reversed && <p style={{ color: "var(--muted)" }}>⇄ {c.keywords_reversed}</p>}
        <p style={{ whiteSpace: "pre-wrap" }}>{shown}</p>
        {long && (
          <button className="btn btn-ghost" style={{ padding: "8px 18px", fontSize: 13 }}
            onClick={() => { setOpen(!open); }}>
            {open ? LESS[lang] : MORE[lang]}
          </button>
        )}
        <dl className="kv">
          {!!c.meaning_love && (<><dt>♥</dt><dd>{c.meaning_love}</dd></>)}
          {!!c.meaning_career && (<><dt>⚒</dt><dd>{c.meaning_career}</dd></>)}
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
