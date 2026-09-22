"use client";
import { pick } from "../lib/api";

const L = {
  ru: {
    upright: "Прямое", reversed: "Перевёрнутое", love: "Любовь и отношения", career: "Карьера и работа",
    health: "Здоровье", spirituality: "Духовность", arcana: "аркан", theme: "Тема",
  },
  uk: {
    upright: "Пряме", reversed: "Перевернуте", love: "Любов і стосунки", career: "Кар'єра і робота",
    health: "Здоров'я", spirituality: "Духовність", arcana: "аркан", theme: "Тема",
  },
  en: {
    upright: "Upright", reversed: "Reversed", love: "Love and relationships", career: "Career and work",
    health: "Health", spirituality: "Spirituality", arcana: "arcana", theme: "Theme",
  },
};

/** Повна характеристика карти: ключі, прямо/перевернуто, сфери життя, символика.
 *  Використовується в розкладах та інтерактиві — замість скороченого блоку. */
export default function CardBreakdown({ card, lang, reversed, compact }) {
  const t = L[lang] || L.uk;
  const c = pick(card, lang, "name", "theme", "keywords_upright", "keywords_reversed",
    "meaning_general", "meaning_love", "meaning_career", "meaning_health",
    "meaning_spirituality", "meaning_reversed", "symbolism");
  const kw = String(reversed && c.keywords_reversed ? c.keywords_reversed : c.keywords_upright || "")
    .split(",").map((s) => s.trim()).filter(Boolean);
  const areas = [
    [c.meaning_love, t.love],
    [c.meaning_career, t.career],
    [c.meaning_health, t.health],
    [c.meaning_spirituality, t.spirituality],
  ].filter(([v]) => v);
  return (
    <div className="cat-data">
      <div className="cat-head" style={{ marginBottom: 6 }}>
        <span className="cat-no">{card.number}</span>
        <h4>{c.name}</h4>
        {card.translations?.en?.name && <span className="cat-en">{card.translations.en.name}</span>}
      </div>
      {c.theme && <p className="cat-kw" style={{ marginTop: 0 }}><span style={{ margin: 0 }}>◈ {c.theme}</span></p>}
      {kw.length > 0 && <div className="cat-kw">{kw.slice(0, 6).map((k) => <span key={k}>{k}</span>)}</div>}
      {c.meaning_general && <p className="cat-meaning">{c.meaning_general}</p>}
      {c.meaning_reversed && <p className="cat-rev">⇄ {t.reversed}: {c.meaning_reversed}</p>}
      {areas.length > 0 && (
        <div className={`cat-areas${compact ? " cat-areas-sm" : ""}`}>
          {areas.map(([v, label]) => (
            <div className="cat-area" key={label}><b>{label}</b><p>{v}</p></div>
          ))}
        </div>
      )}
      {c.symbolism && c.symbolism.includes("Источник") || c.symbolism?.includes("Джерело") || c.symbolism?.length > 200 ? (
        <div className="cat-src">📜 {c.symbolism}</div>
      ) : null}
    </div>
  );
}