import { notFound } from "next/navigation";
import { API } from "../../../../lib/api";
import { directionBySlug, normCat } from "../../../../lib/directions";
import DirectionSpreads from "../../../../components/DirectionSpreads";

/** /directions/{slug}/spreads — практика: схеми БД цього напрямку + онлайн-витягування. */
export default async function DirectionSpreadsPage({ params }) {
  const d = directionBySlug(params.slug);
  if (!d) notFound();

  let systems = [];
  let decks = [];
  let spreads = [];
  try {
    const r = await fetch(`${API}/stats`, { cache: "no-store" });
    if (r.ok) {
      const s = await r.json();
      const allSystems = Array.isArray(s?.by_system) ? s.by_system : [];
      const sysIds = new Set(
        allSystems.filter((x) => normCat(x.category) === d.slug).map((x) => x.id),
      );
      systems = allSystems.filter((x) => sysIds.has(x.id));
      decks = (Array.isArray(s?.by_deck) ? s.by_deck : []).filter((x) => sysIds.has(x.system_id));
    }
  } catch {}
  try {
    const r = await fetch(`${API}/spreads`, { cache: "no-store" });
    if (r.ok) {
      const all = await r.json();
      const sysIds = new Set(systems.map((x) => x.id));
      spreads = (Array.isArray(all) ? all : []).filter((x) => sysIds.has(x.system_id));
    }
  } catch {}

  return <DirectionSpreads direction={d} decks={decks} systems={systems} initialSpreads={spreads} />;
}
