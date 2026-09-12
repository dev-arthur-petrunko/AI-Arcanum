// Процедурні Canvas-текстури карт: сорочка + лице-заглушка (якщо нема скана RWS).
// Працює лише в браузері; текстури кешуються.
import * as THREE from "three";

const cache = new Map();

function canvasTex(w, h, draw) {
  const cv = document.createElement("canvas");
  cv.width = w; cv.height = h;
  draw(cv.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(cv);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

export function backTexture() {
  if (cache.has("back")) return cache.get("back");
  const t = canvasTex(512, 840, (g, w, h) => {
    const grad = g.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, "#1b2450"); grad.addColorStop(1, "#0c1130");
    g.fillStyle = grad; g.fillRect(0, 0, w, h);
    // золота рамка
    g.strokeStyle = "#d4a94e"; g.lineWidth = 10; g.strokeRect(24, 24, w - 48, h - 48);
    g.strokeStyle = "rgba(212,169,78,.45)"; g.lineWidth = 3; g.strokeRect(48, 48, w - 96, h - 96);
    // місяць і зорі
    g.fillStyle = "#e8c87a";
    g.beginPath(); g.arc(w / 2, h * 0.36, 70, 0, Math.PI * 2); g.fill();
    g.fillStyle = "#1b2450";
    g.beginPath(); g.arc(w / 2 + 28, h * 0.36 - 18, 62, 0, Math.PI * 2); g.fill();
    g.fillStyle = "#f2ead8";
    const stars = [[90, 120], [420, 200], [150, 560], [370, 640], [256, 700], [110, 420], [410, 470]];
    for (const [x, y] of stars) {
      g.save(); g.translate(x, y); g.rotate(Math.PI / 4);
      g.fillRect(-2, -14, 4, 28); g.fillRect(-14, -2, 28, 4);
      g.restore();
    }
    g.fillStyle = "#e8c87a"; g.font = "600 44px Georgia"; g.textAlign = "center";
    g.fillText("✦ ARCANUM ✦", w / 2, h - 110);
  });
  cache.set("back", t);
  return t;
}

export function frontFallbackTexture(title) {
  const key = "front:" + title;
  if (cache.has(key)) return cache.get(key);
  const t = canvasTex(512, 840, (g, w, h) => {
    const grad = g.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, "#f5edd8"); grad.addColorStop(1, "#e2d3ac");
    g.fillStyle = grad; g.fillRect(0, 0, w, h);
    g.strokeStyle = "#8a6b25"; g.lineWidth = 8; g.strokeRect(20, 20, w - 40, h - 40);
    // арка-портал
    g.strokeStyle = "#3a3f6e"; g.lineWidth = 6;
    g.beginPath(); g.arc(w / 2, h * 0.44, 130, Math.PI, 0); g.stroke();
    g.fillStyle = "#3a3f6e";
    g.beginPath(); g.arc(w / 2, h * 0.44, 46, 0, Math.PI * 2); g.fill();
    g.fillStyle = "#e8c87a";
    g.beginPath(); g.arc(w / 2, h * 0.44, 20, 0, Math.PI * 2); g.fill();
    // назва
    g.fillStyle = "#2a2350"; g.textAlign = "center";
    const words = String(title || "").split(" ");
    g.font = "600 52px Georgia";
    if (words.join(" ").length > 14) g.font = "600 40px Georgia";
    const lines = [];
    let line = "";
    for (const wd of words) {
      if ((line + " " + wd).trim().length > 16) { lines.push(line.trim()); line = wd; }
      else line += " " + wd;
    }
    lines.push(line.trim());
    lines.slice(0, 3).forEach((ln, i) => g.fillText(ln, w / 2, h - 220 + i * 52));
    g.fillStyle = "#8a6b25"; g.font = "44px Georgia";
    g.fillText("✦", w / 2, 110);
  });
  cache.set(key, t);
  return t;
}
