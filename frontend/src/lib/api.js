export const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getJSON(path) {
  const r = await fetch(`${API}${path}`);
  if (!r.ok) throw new Error(`${path}: ${r.status}`);
  return r.json();
}

/** Базове поле + оверлей translations[lang] для вказаних ключів. */
export function pick(obj, lang, ...fields) {
  if (!obj) return {};
  const out = { ...obj };
  const tr = obj.translations?.[lang];
  if (tr) for (const f of fields) if (tr[f]) out[f] = tr[f];
  return out;
}

export const cardName = (c, lang) => pick(c, lang, "name").name || c?.name;
