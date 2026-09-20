import DeckPage from "../../../components/DeckPage";
import { API } from "../../../lib/api";
import { normCat } from "../../../lib/directions";

async function getJSON(path) {
  try {
    const r = await fetch(`${API}${path}`, { cache: "no-store" });
    if (!r.ok) return null;
    return await r.json();
  } catch {
    return null;
  }
}

/** Серверна сторінка колоди: дані тягнуться до рендеру, 3D — на клієнті.
 *  related_deck_id — «будівельна» колода (напр. Багуа для І-Цзин), показується окремим блоком. */
export default async function DeckRoute({ params }) {
  const deck = await getJSON(`/decks/${params.id}`);
  const cards = (await getJSON(`/cards?deck_id=${params.id}&limit=200`)) || [];
  let relatedDeck = null;
  let relatedCards = [];
  if (deck?.related_deck_id) {
    relatedDeck = await getJSON(`/decks/${deck.related_deck_id}`);
    relatedCards = (await getJSON(`/cards?deck_id=${deck.related_deck_id}&limit=200`)) || [];
  }
  // «Гадальні»: карта відкривається на окремій сторінці /directions/divination/card/<id>
  let isDivination = false;
  if (deck?.system_id) {
    try {
      const r = await fetch(`${API}/stats`, { cache: "no-store" });
      if (r.ok) {
        const s = await r.json();
        const sys = (Array.isArray(s?.by_system) ? s.by_system : []).find((x) => x.id === deck.system_id);
        isDivination = normCat(sys?.category) === "divination";
      }
    } catch {}
  }
  return (
    <DeckPage
      deck={deck}
      initialCards={Array.isArray(cards) ? cards : []}
      relatedDeck={relatedDeck}
      relatedCards={Array.isArray(relatedCards) ? relatedCards : []}
      isDivination={isDivination}
    />
  );
}
