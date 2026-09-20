"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";

/** Плавна поява секції при скролі (GSAP, без зайвих залежностей).
 *  Строго детерміновано: секція, що вже у в'юпорті на момент завантаження,
 *  з'являється одразу; решта — при першому пікселі на екрані (threshold 0).
 *  Fallback: якщо GSAP не спрацював за 1.2с, секція стає видимою примусово. */
export default function Reveal({ children, y = 28, delay = 0 }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.classList.add("reveal-fb");
    gsap.set(el, { opacity: 0, y });
    el.classList.remove("reveal-fb");
    const reveal = () => gsap.to(el, { opacity: 1, y: 0, duration: 0.9, delay, ease: "power3.out" });
    const rect = el.getBoundingClientRect();
    const vh = window.innerHeight || document.documentElement.clientHeight;
    const cleanups = [];
    const failSafe = setTimeout(() => {
      el.classList.add("reveal-fb");
      cleanups.forEach((fn) => fn());
    }, 1200);
    cleanups.push(() => clearTimeout(failSafe));
    if (rect.top <= vh && rect.bottom >= 0) {
      reveal();
      return () => { clearTimeout(failSafe); el.classList.add("reveal-fb"); };
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            clearTimeout(failSafe);
            reveal();
            io.disconnect();
          }
        });
      },
      { threshold: 0 }
    );
    io.observe(el);
    return () => {
      io.disconnect();
      clearTimeout(failSafe);
      el.classList.add("reveal-fb");
    };
  }, [y, delay]);
  return <div ref={ref}>{children}</div>;
}
