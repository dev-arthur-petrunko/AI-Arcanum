import HomeClient from "../components/HomeClient";
import { API } from "../lib/api";

/** Серверний компонент: підтягує живі лічильники (/stats), щоб SSR одразу показував правду. */
export default async function Page() {
  let initialCounts = null;
  let initialDecks = null;
  let initialSystems = null;
  try {
    const r = await fetch(`${API}/stats`, { cache: "no-store" });
    if (r.ok) {
      const s = await r.json();
      if (s?.cards) {
        initialCounts = { cards: s.cards, systems: s.systems };
        initialDecks = s.by_deck || null;
        initialSystems = s.by_system || null;
      }
    }
  } catch {}
  return <HomeClient initialCounts={initialCounts} initialDecks={initialDecks} initialSystems={initialSystems} />;
}
