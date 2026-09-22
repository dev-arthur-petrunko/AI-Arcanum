"use client";
import { useEffect } from "react";
import InteractiveCard from "./InteractiveCard";

const T = {
  ru: { hint: "Символика карти", close: "Закрыть" },
  uk: { hint: "Символіка карти", close: "Закрити" },
  en: { hint: "Card symbolism", close: "Close" },
};

/** Модальне вікно з інтерактивною картою (зони + значення нижче). */
export default function InteractiveCardModal({ card, lang, onClose }) {
  const t = T[lang] || T.uk;

  useEffect(() => {
    if (!card?.id) return;
    document.body.classList.add("modal-open");
    const esc = (e) => e.key === "Escape" && onClose?.();
    document.addEventListener("keydown", esc);
    return () => {
      document.body.classList.remove("modal-open");
      document.removeEventListener("keydown", esc);
    };
  }, [card?.id, onClose]);

  if (!card?.id) return null;

  return (
    <div className="modal-ov rws-modal" onClick={() => onClose?.()}>
      <div className="drawer modal-card rws-modal-inner" onClick={(e) => e.stopPropagation()}>
        <button type="button" className="modal-x" onClick={() => onClose?.()} aria-label={t.close}>✕</button>
        <h3 style={{ marginTop: 0 }}>{t.hint}</h3>
        <InteractiveCard card={card} lang={lang} />
      </div>
    </div>
  );
}