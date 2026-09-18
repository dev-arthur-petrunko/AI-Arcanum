import { notFound } from "next/navigation";
import { API } from "../../../../lib/api";
import { directionBySlug, normCat } from "../../../../lib/directions";
import DirectionGuides from "../../../../components/DirectionGuides";

/** /directions/{slug}/guides — гайди напрямку (фільтр GET /articles, бекенд без змін). */
export default async function DirectionGuidesPage({ params }) {
  const d = directionBySlug(params.slug);
  if (!d) notFound();

  let systems = [];
  let decks = [];
  let articles = [];
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
  try {
    const r = await fetch(`${API}/articles`, { cache: "no-store" });
    if (r.ok) {
      const a = await r.json();
      if (Array.isArray(a)) articles = a;
    }
  } catch {}

  return <DirectionGuides direction={d} decks={decks} initialArticles={articles} />;
}
