import DeckPage from "../../../components/DeckPage";
import { API } from "../../../lib/api";

async function getJSON(path) {
  try {
    const r = await fetch(`${API}${path}`, { cache: "no-store" });
    if (!r.ok) return null;
    return await r.json();
  } catch {
    return null;
  }
}

/** Серверна сторінка колоди: дані тягнуться до рендеру, 3D — на клієнті. */
export default async function DeckRoute({ params }) {
  const deck = await getJSON(`/decks/${params.id}`);
  const cards = (await getJSON(`/cards?deck_id=${params.id}&limit=200`)) || [];
  return <DeckPage deck={deck} initialCards={Array.isArray(cards) ? cards : []} />;
}
