import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/** QuizModule: флеш-карты — вопрос с /quiz/question, ответ POST /quiz/answer. */
export default function QuizModule({ deckId }) {
  const [q, setQ] = useState(null);
  const [result, setResult] = useState(null);

  async function next() {
    setResult(null);
    const url = `${API}/quiz/question${deckId ? `?deck_id=${deckId}` : ""}`;
    setQ(await (await fetch(url)).json());
  }

  async function answer(choice) {
    const ok = choice.id === q.answer_id;
    setResult(ok ? "✅ Верно!" : "❌ Мимо — смотри подсказку и карточку карты");
    await fetch(`${API}/quiz/answer`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: 0, card_id: q.card_id, correct: ok }),
    });
  }

  return (
    <div style={{ border: "1px solid #2a2f55", borderRadius: 12, padding: 16, background: "#12162e" }}>
      <h3>🧠 Квиз — запомни значения</h3>
      <button onClick={next}>Следующий вопрос</button>
      {q && q.choices && (
        <>
          <p style={{ opacity: 0.8 }}>Подсказка: {q.hint}</p>
          <div style={{ display: "grid", gap: 8 }}>
            {q.choices.map((c) => (
              <button key={c.id} onClick={() => answer(c)}>{c.name}</button>
            ))}
          </div>
        </>
      )}
      {result && <p>{result}</p>}
    </div>
  );
}
