"use client";
import { useMemo } from "react";
import { pick } from "../lib/api";

const ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
  "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"];

const L = {
  ru: { majors: "Старшие арканы", upright: "Прямое", reversed: "Перевёрнутое", love: "Любовь и отношения", career: "Карьера и работа", health: "Здоровье", spirituality: "Духовность", of: "в", arcanaType: "аркан" },
  uk: { majors: "Старші аркани", upright: "Пряме", reversed: "Перевернуте", love: "Любов і стосунки", career: "Кар'єра і робота", health: "Здоров'я", spirituality: "Духовність", of: "із", arcanaType: "аркан" },
  en: { majors: "Major Arcana", upright: "Upright", reversed: "Reversed", love: "Love and relationships", career: "Career and work", health: "Health", spirituality: "Spirituality", of: "of", arcanaType: "arcana" },
};

const SUIT_NAME = {
  ru: { wands: "Жезлы", cups: "Кубки", swords: "Мечи", pentacles: "Пентакли" },
  uk: { wands: "Жезли", cups: "Кубки", swords: "Мечі", pentacles: "Пентаклі" },
  en: { wands: "Wands", cups: "Cups", swords: "Swords", pentacles: "Pentacles" },
};

/** Обʼєднує базові поля + translations[lang] — зручний доступ до локалізованої картки. */
function loc(c, lang) {
  return pick(c, lang, "name", "theme", "keywords_upright", "keywords_reversed",
    "meaning_general", "meaning_love", "meaning_career", "meaning_health",
    "meaning_spirituality", "meaning_reversed", "symbolism");
}

function CardRow({ c, lang, isMajor, onOpen }) {
  const x = loc(c, lang);
  const no = isMajor ? ROMAN[parseInt(c.number, 10)] ?? c.number : c.number;
  const en = c.translations?.en?.name || "";
  const kw = String(x.keywords_upright || "").split(",").map((s) => s.trim()).filter(Boolean).slice(0, 6);
  const areas = [
    [x.meaning_love, L[lang].love],
    [x.meaning_career, L[lang].career],
    [x.meaning_health, L[lang].health],
    [x.meaning_spirituality, L[lang].spirituality],
  ].filter(([v]) => v);
  return (
    <article className="cat-card">
      <div className="cat-img-wrap">
        {c.image_path ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img className="cat-img" src={c.image_path} alt={x.name}
            onClick={() => onOpen?.(c)} role="button" tabIndex={0} aria-label={x.name}
            onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && onOpen?.(c)}
            onError={(e) => (e.currentTarget.style.display = "none")} />
        ) : <div className="cat-img" style={{ display: "flex", alignItems: "center", justifyContent: "center", fontSize: 46 }}>✦</div>}
        <span className="cat-open">☝</span>
      </div>
      <div>
        <div className="cat-head">
          <span className="cat-no">{isMajor ? no : no}</span>
          <h4>{x.name}</h4>
          {en && <span className="cat-en">{en}</span>}
        </div>
        {kw.length > 0 && (
          <div className="cat-kw">{kw.map((k) => <span key={k}>{k}</span>)}</div>
        )}
        {x.meaning_general && <p className="cat-meaning">{x.meaning_general}</p>}
        {x.meaning_reversed && <p className="cat-rev">⇄ {L[lang].reversed}: {x.meaning_reversed}</p>}
        {areas.length > 0 && (
          <div className="cat-areas">
            {areas.map(([v, label]) => (
              <div className="cat-area" key={label}><b>{label}</b><p>{v}</p></div>
            ))}
          </div>
        )}
        {(c.translations?.en?.source_reference) && <div className="cat-src">📜 {c.translations.en.source_reference}</div>}
      </div>
    </article>
  );
}

function Group({ title, count, total, cards, lang, isMajor, onOpen }) {
  if (cards.length === 0) return null;
  return (
    <section style={{ marginTop: 26 }}>
      <p className="arc-title"><b>{title}</b> <span className="arc-count">{count} {L[lang].of} {total}</span></p>
      {cards.map((c) => <CardRow key={c.id} c={c} lang={lang} isMajor={isMajor} onOpen={onOpen} />)}
    </section>
  );
}

/** Повний каталог колоди з розкритими значеннями: Старші аркани + 4 масті. */
export default function CatalogClient({ cards, lang, onOpen }) {
  const { majors, suits } = useMemo(() => {
    const m = cards.filter((c) => /Старш/i.test(c.arcana_type || ""));
    const order = { wands: 0, cups: 1, swords: 2, pentacles: 3 };
    const map = new Map();
    for (const c of cards) {
      if (/Старш/i.test(c.arcana_type || "")) continue;
      const code = c.suit_code || "";
      if (!map.has(code)) map.set(code, []);
      map.get(code).push(c);
    }
    const sl = [...map.entries()]
      .filter(([k]) => k in order)
      .sort((a, b) => (order[a[0]] ?? 9) - (order[b[0]] ?? 9));
    return { majors: m, suits: sl.map(([code, list]) => ({ code, list })) };
  }, [cards]);
  return (
    <>
      <Group title={L[lang].majors} count={majors.length} total={22}
        cards={majors} lang={lang} isMajor onOpen={onOpen} />
      {suits.map((s) => (
        <Group key={s.code} title={SUIT_NAME[lang][s.code] || s.code} count={s.list.length} total={14}
          cards={s.list} lang={lang} onOpen={onOpen} />
      ))}
      {suits.length === 0 && majors.length > 0 && (
        <Group title="—" count={cards.length - majors.length} total={cards.length - majors.length}
          cards={cards.filter((c) => !/Старш/i.test(c.arcana_type || ""))} lang={lang} onOpen={onOpen} />
      )}
    </>
  );
}