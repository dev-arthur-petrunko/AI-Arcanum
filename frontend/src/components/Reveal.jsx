"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";

/** Плавна поява секції при скролі (GSAP, без зайвих залежностей). */
export default function Reveal({ children, y = 28, delay = 0 }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    gsap.set(el, { opacity: 0, y });
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            gsap.to(el, { opacity: 1, y: 0, duration: 0.9, delay, ease: "power3.out" });
            io.disconnect();
          }
        });
      },
      { threshold: 0.12 }
    );
    io.observe(el);
    return () => io.disconnect();
  }, [y, delay]);
  return <div ref={ref}>{children}</div>;
}
