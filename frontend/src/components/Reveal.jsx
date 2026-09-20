"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";

/** Плавна поява секції при скролі (GSAP, без зайвих залежностей).
 *  Строго детерміновано: секція, що вже у в'юпорті на момент завантаження,
 *  з'являється одразу; решта — при першому пікселі на екрані (threshold 0,
 *  щоб високі секції на кшталт сонника ніколи не лишалися невидимими). */
export default function Reveal({ children, y = 28, delay = 0 }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    gsap.set(el, { opacity: 0, y });
    const reveal = () => gsap.to(el, { opacity: 1, y: 0, duration: 0.9, delay, ease: "power3.out" });
    const rect = el.getBoundingClientRect();
    const vh = window.innerHeight || document.documentElement.clientHeight;
    if (rect.top <= vh && rect.bottom >= 0) {
      reveal();
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            reveal();
            io.disconnect();
          }
        });
      },
      { threshold: 0 }
    );
    io.observe(el);
    return () => io.disconnect();
  }, [y, delay]);
  return <div ref={ref}>{children}</div>;
}
