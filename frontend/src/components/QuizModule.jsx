import { useEffect, useState } from "react";
import { API } from "../lib/api";

/** Квиз-флешкартки: питання GET /quiz/question, відповідь POST /quiz/answer (Python-бекенд). */
export default function QuizModule({ deckId, lang = "uk" }) {
  const [q, setQ] = useState(null);
  const [result, setResult] = useState(null);
  const [score, setScore] = useState({ ok: 0, total: 0 });
  useEffect(() => { setScore({ ok: 0, total: 0 }); setQ(null); setResult(null); }, [deckId]);
  const L = {
    ru: { next: "Следующий вопрос", hint: "Подсказка", ok: "✅ Верно!", no: "❌ Мимо — открой карточку карты и повтори" },
    uk: { next: "Наступне питання", hint: "Підказка", ok: "✅ Правильно!", no: "❌ Мимо — відкрий картку карти й повтори" },
    en: { next: "Next question", hint: "Hint", ok: "✅ Correct!", no: "❌ Miss — open the card and retry" },
  }[lang];

  async function next() {
    setResult(null);
    const url = `${API}/quiz/question${deckId ? `?deck_id=${deckId}` : ""}`;
    setQ(await (await fetch(url)).json());
  }

  async function answer(choice) {
    const ok = choice.id === q.answer_id;
    setResult(ok ? L.ok : L.no);
    setScore((s) => ({ ok: s.ok + (ok ? 1 : 0), total: s.total + 1 }));
    fetch(`${API}/quiz/answer`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: 0, card_id: q.card_id, correct: ok }),
    }).catch(() => {});
  }

  const scoreLine = { ru: "Счёт", uk: "Рахунок", en: "Score" }[lang];

  return (
    <div className="quiz-box">
      <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
        <button className="quiz-next" onClick={next}>🧠 {L.next}</button>
        {score.total > 0 && <span style={{ color: "var(--gold-soft)" }}>{scoreLine}: {score.ok}/{score.total}</span>}
      </div>
      {q?.choices && (
        <>
          <p style={{ opacity: 0.8 }}>{L.hint}: {q.hint}</p>
          <div style={{ display: "grid", gap: 8 }}>
            {q.choices.map((c) => (
              <button key={c.id} onClick={() => answer(c)}>{c.name}</button>
            ))}
          </div>
        </>
      )}
      {result && <p style={{ fontSize: 17 }}>{result}</p>}
    </div>
  );
}
