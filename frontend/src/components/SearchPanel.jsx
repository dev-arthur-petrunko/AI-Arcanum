import { useState } from "react";
import { API } from "../lib/api";

// Лейбли — українською; value — мовно-незалежні коди (element_code в БД).
const ELEMENTS = [
  { label: "✦", value: "" },
  { label: "Вогонь", value: "fire" },
  { label: "Вода", value: "water" },
  { label: "Повітря", value: "air" },
  { label: "Земля", value: "earth" },
];

export default function SearchPanel({ lang = "uk", onResults }) {
  const [q, setQ] = useState("");
  const [element, setElement] = useState("");
  const [loading, setLoading] = useState(false);

  async function run(e) {
    e?.preventDefault();
    if (q.trim().length < 2 && !element) return;
    setLoading(true);
    try {
      const params = new URLSearchParams({ q: q.trim() || "а", ...(element ? { element } : {}) });
      const data = await (await fetch(`${API}/search?${params}`)).json();
      onResults?.(Array.isArray(data) ? data : []);
    } catch {
      onResults?.([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <form onSubmit={run} className="search-row">
        <input
          value={q} onChange={(e) => setQ(e.target.value)}
          placeholder={lang === "uk" ? "Пошук: символ, стихія, планета…" : lang === "en" ? "Search: symbol, element, planet…" : "Поиск: символ, стихия, планета…"}
        />
        <button type="submit" disabled={loading}>{loading ? "…" : "🔎"}</button>
      </form>
      <div className="chips">
        {ELEMENTS.map((el) => (
          <button key={el.value || "all"} type="button" className={`chip${element === el.value ? " active" : ""}`}
            onClick={() => setElement(el.value)}>{el.label}</button>
        ))}
      </div>
    </div>
  );
}
