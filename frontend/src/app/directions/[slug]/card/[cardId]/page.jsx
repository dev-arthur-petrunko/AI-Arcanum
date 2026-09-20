import { notFound } from "next/navigation";
import { API } from "../../../../../lib/api";
import { directionBySlug } from "../../../../../lib/directions";
import CardPage from "../../../../../components/CardPage";

async function getJSON(path) {
  try {
    const r = await fetch(`${API}${path}`, { cache: "no-store" });
    if (!r.ok) return null;
    return await r.json();
  } catch {
    return null;
  }
}

export async function generateMetadata({ params }) {
  const card = await getJSON(`/cards/${params.cardId}`);
  const d = directionBySlug(params.slug);
  if (!card) return { title: "Карта — AI-Arcanum" };
  return { title: `${card.name} — AI-Arcanum`, description: (card.meaning_general || "").slice(0, 160) };
}

/** /directions/{slug}/card/{id} — окрема сторінка однієї карти з навігацією по колоді. */
export default async function CardPageRoute({ params }) {
  const d = directionBySlug(params.slug);
  const card = await getJSON(`/cards/${params.cardId}`);
  if (!card) notFound();

  let deck = null;
  let deckCards = [];
  if (card.deck_id) {
    deck = await getJSON(`/decks/${card.deck_id}`);
    deckCards = (await getJSON(`/cards?deck_id=${card.deck_id}&limit=200`)) || [];
  }
  return (
    <CardPage
      card={card}
      deck={deck}
      deckCards={Array.isArray(deckCards) ? deckCards : []}
      direction={d}
    />
  );
}