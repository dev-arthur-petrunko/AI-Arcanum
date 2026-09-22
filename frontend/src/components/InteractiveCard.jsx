"use client";
import { useRef, useState } from "react";
import { zonesFor } from "../lib/rws";
import { pick } from "../lib/api";

const L = {
  ru: {
    hint: "Нажми на отметку на карте — значение откроется ниже. Наведи на точку, чтобы показать смысл символа.",
    hit: "Точка", part: "Символ", meaning: "Значение",
    empty: "Для этой карты ещё нет интерактивной символики.",
  },
  uk: {
    hint: "Натисни на позначку на карті — значення відкриється нижче. Наведи на точку, щоб показати сенс символу.",
    hit: "Точка", part: "Символ", meaning: "Значення",
    empty: "Для цієї карти ще немає інтерактивної символіки.",
  },
  en: {
    hint: "Click a marker on the card — the meaning opens below. Hover a dot to reveal the symbol's sense.",
    hit: "Marker", part: "Symbol", meaning: "Meaning",
    empty: "No interactive symbolism for this card yet.",
  },
};

/**
 * Інтерактивна карта RWS за зразком craft-cards.com.ua/taro/blazen:
 * карта видна цілком, на ній — золоті позначки зон; наведення показує значення,
 * клік по позначці скролить до частини в списку внизу (повністю всі частини).
 */
export default function InteractiveCard({ card, lang }) {
  const t = L[lang] || L.uk;
  const zones = zonesFor(String(card?.number ?? ""));
  const [active, setActive] = useState(null);
  const listRef = useRef(null);
  const imgRef = useRef(null);
  const c = pick(card, lang, "name");

  const scrollToZone = (i) => {
    setActive(i);
    const el = listRef.current?.querySelector(`[data-zone="${i}"]`);
    el?.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  const pickZone = (i) => {
    setActive(i);
    imgRef.current?.querySelector(`[data-hit="${i}"]`)?.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  if (!card?.image_path) return null;

  return (
    <div className="rws-wrap" data-zone-card={card.number}>
      <p className="rws-hint">☝ {t.hint}</p>
      <div className="rws-image">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img ref={imgRef} src={card.image_path} alt={c.name}
          onError={(e) => (e.currentTarget.style.display = "none")} />
        {zones.map((z, i) => (
          <button
            key={i} type="button" data-hit={i} className={`rws-hit${active === i ? " on" : ""}`}
            style={{ left: `${z.x}%`, top: `${z.y}%` }}
            onClick={() => scrollToZone(i)} aria-label={`${t.hit} ${i + 1}`}
          >
            <span className="rws-n">{i + 1}</span>
            <span className="rws-tip">
              <b>{z.t?.[lang] || z.t?.uk}</b>
              <span>{z.d?.[lang] || z.d?.uk}</span>
            </span>
          </button>
        ))}
        {zones.length === 0 && <div className="rws-empty">{t.empty}</div>}
      </div>

      <div className="rws-list" ref={listRef}>
        <h4>{c.name}</h4>
        {zones.map((z, i) => (
          <div key={i} data-zone={i} className={`rws-zone${active === i ? " on" : ""}`}
            onClick={() => pickZone(i)}>
            <span className="rws-zone-n">{i + 1}</span>
            <div>
              <b className="rws-zone-t">{z.t?.[lang] || z.t?.uk}</b>
              <p className="rws-zone-d">{z.d?.[lang] || z.d?.uk}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}