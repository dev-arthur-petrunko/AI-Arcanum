import { notFound } from "next/navigation";
import { API } from "../../../lib/api";
import { directionBySlug, normCat } from "../../../lib/directions";
import DirectionClient from "../../../components/DirectionClient";
import DreamDictionary from "../../../components/DreamDictionary";

/** Сонник: колода 52 у БД містить картку-символ з перекладами uk/ru/en.
 *  Мапимо поля БД у форму {id, icon, name, keywords, text} для словника. */
function dbCardToSymbol(c) {
  const trRu = c.translations?.ru || {};
  const trEn = c.translations?.en || {};
  const icon = (c.theme || "").trim().split(/\s+/)[0] || "💤";
  return {
    id: c.number,
    icon,
    name: { uk: c.name, ru: trRu.name || c.name, en: trEn.name || c.name },
    keywords: {
      uk: c.keywords_upright || "",
      ru: trRu.keywords_upright || c.keywords_upright || "",
      en: trEn.keywords_upright || c.keywords_upright || "",
    },
    text: {
      uk: c.meaning_general || "",
      ru: trRu.meaning_general || c.meaning_general || "",
      en: trEn.meaning_general || c.meaning_general || "",
    },
  };
}

async function fetchDreamSymbols() {
  try {
    const r = await fetch(`${API}/cards?deck_id=52&limit=200`, { cache: "no-store" });
    if (r.ok) {
      const cards = await r.json();
      if (Array.isArray(cards) && cards.length > 0) return cards.map(dbCardToSymbol);
    }
  } catch {}
  return null;
}

export async function generateMetadata({ params }) {
  const d = directionBySlug(params.slug);
  if (!d) return { title: "Напрямок — AI-Arcanum" };
  return { title: `${d.title.uk} — AI-Arcanum`, description: d.desc.uk };
}

/** /directions/{slug} — Значення карт: вітрина колод напрямку + 3D-переглядач.
 *  Дані — ті самі GET /stats, відфільтровані за systems.category (бекенд без змін). */
export default async function DirectionPage({ params }) {
  const d = directionBySlug(params.slug);
  if (!d) notFound();

  // Сонник — окрема навчальна сторінка: алфавітний словник символів.
  if (d.slug === "dreams") {
    const symbols = await fetchDreamSymbols();
    return <DreamDictionary direction={d} symbols={symbols} />;
  }

  let systems = [];
  let decks = [];
  try {
    const r = await fetch(`${API}/stats`, { cache: "no-store" });
    if (r.ok) {
      const s = await r.json();
      const allSystems = Array.isArray(s?.by_system) ? s.by_system : [];
      const sysIds = new Set(
        allSystems.filter((x) => normCat(x.category) === d.slug).map((x) => x.id),
      );
      systems = allSystems.filter((x) => sysIds.has(x.id) && x.decks > 0);
      decks = (Array.isArray(s?.by_deck) ? s.by_deck : []).filter((x) => sysIds.has(x.system_id) && x.is_shown_in_directory !== false);
    }
  } catch {}

  return <DirectionClient direction={d} systems={systems} decks={decks} />;
}
