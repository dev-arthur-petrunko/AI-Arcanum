import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function SearchPanel({ lang = "ru", onResults }) {
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);

  async function run(e) {
    e?.preventDefault();
    if (q.trim().length < 2) return;
    setLoading(true);
    try {
      const r = await fetch(`${API}/search?q=${encodeURIComponent(q)}`);
      const data = await r.json();
      onResults?.(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={run} style={{ display: "flex", gap: 8 }}>
      <input value={q} onChange={(e) => setQ(e.target.value)}
        placeholder={lang === "uk" ? "Пошук: символ, стихія, планета…" : lang === "en" ? "Search: symbol, element, planet…" : "Поиск: символ, стихия, планета…"}
        style={{ flex: 1, padding: "10px 12px", borderRadius: 10, border: "1px solid #333", background: "#11142a", color: "#fff" }} />
      <button type="submit" disabled={loading} style={{ padding: "10px 16px", borderRadius: 10 }}>
        {loading ? "…" : "🔎"}
      </button>
    </form>
  );
}
