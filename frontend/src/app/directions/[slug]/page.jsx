import { notFound } from "next/navigation";
import { API } from "../../../lib/api";
import { directionBySlug, normCat } from "../../../lib/directions";
import DirectionClient from "../../../components/DirectionClient";

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
