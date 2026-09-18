"use client";
import { Suspense, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { ContactShadows, Environment, OrbitControls, Sparkles, Stars } from "@react-three/drei";
import { EffectComposer, Bloom, Vignette } from "@react-three/postprocessing";
import * as THREE from "three";
import TarotCard from "./TarotCard";

function Moon() {
  const ref = useMemo(() => ({ c: null }), []);
  useFrame(({ clock }) => {
    if (ref.c) ref.c.position.y = 5.4 + Math.sin(clock.elapsedTime * 0.3) * 0.15;
  });
  return (
    <group>
      <mesh position={[-6.5, 5.4, -9]} ref={(m) => (ref.c = m)}>
        <sphereGeometry args={[0.9, 32, 32]} />
        <meshStandardMaterial color="#fdf6e0" emissive="#e8c87a" emissiveIntensity={1.6} roughness={0.4} />
      </mesh>
      <pointLight position={[-6.5, 5.4, -8]} intensity={12} distance={30} color="#e8c87a" />
    </group>
  );
}

function Table() {
  return (
    <group>
      {/* круглий езотеричний стіл */}
      <mesh position={[0, -1.45, 0]}>
        <cylinderGeometry args={[5.2, 5.5, 0.25, 64]} />
        <meshStandardMaterial color="#131a3d" roughness={0.35} metalness={0.25} />
      </mesh>
      {/* золоте кільце-інкрустація */}
      <mesh position={[0, -1.31, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[3.9, 4.02, 96]} />
        <meshStandardMaterial color="#d4a94e" emissive="#d4a94e" emissiveIntensity={0.9} roughness={0.3} />
      </mesh>
      <mesh position={[0, -1.31, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.7, 1.76, 96]} />
        <meshStandardMaterial color="#7a5cff" emissive="#7a5cff" emissiveIntensity={0.7} roughness={0.3} />
      </mesh>
      {/* підлога під столом */}
      <mesh position={[0, -2.6, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[60, 60]} />
        <meshStandardMaterial color="#05070f" roughness={1} />
      </mesh>
      <ContactShadows position={[0, -1.3, 0]} opacity={0.75} scale={13} blur={2.4} far={4} />
    </group>
  );
}

const FALLBACK = [
  { id: -1, name: "Дурень" }, { id: -2, name: "Маг" }, { id: -3, name: "Жриця" },
  { id: -4, name: "Світ" }, { id: -5, name: "Зірка" }, { id: -6, name: "Сонце" },
  { id: -7, name: "Місяць" },
];

/** Просунута сцена: місяць, стіл з кільцями, віяло карт, зорі, пил, bloom. */
export default function Scene3D({ cards, lang, onSelect, theme = "dark" }) {
  const bg = theme === "light" ? "#f4ecdc" : "#070912";
  const fan = (cards?.length ? cards : FALLBACK).slice(0, 7);
  const layout = useMemo(() => {
    const n = fan.length;
    return fan.map((_, i) => {
      const k = i - (n - 1) / 2;
      return {
        x: k * 1.35,
        z: -Math.abs(k) * 0.45 + 0.6,
        ry: -k * 0.22,
      };
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fan.length]);

  return (
    <div className="scene-frame">
      <div style={{ height: 560 }}>
        <Canvas camera={{ position: [0, 2.1, 8.2], fov: 40 }} dpr={[1, 2]} gl={{ antialias: true }}>
          <color attach="background" args={[bg]} />
          <fog attach="fog" args={[bg, 12, 30]} />
          <ambientLight intensity={0.55} />
          <directionalLight position={[4, 7, 5]} intensity={1.15} color="#fff3d6" />
          <pointLight position={[0, 3.4, 2.5]} intensity={14} distance={16} color="#b9a7ff" />
          <Suspense fallback={null}>
            <Environment preset="night" />
          </Suspense>
          <Suspense fallback={null}>
            <Stars radius={70} depth={40} count={4200} factor={4} saturation={0.4} fade speed={0.6} />
            <Sparkles count={130} scale={[11, 5, 6]} position={[0, 1.4, -1]} size={3.2} speed={0.35} color="#e8c87a" opacity={0.7} />
            <Moon />
            <Table />
            {fan.map((c, i) => (
              <TarotCard
                key={c.id ?? i}
                card={c.id > 0 ? c : null}
                label={c.translations?.[lang]?.name || c.name}
                position={[layout[i].x, 0.35, layout[i].z]}
                rotationY={layout[i].ry}
                phase={i * 0.9}
                initialFlipped={true}
                onSelect={onSelect}
              />
            ))}
          </Suspense>
          <OrbitControls
            enablePan={false} enableZoom={true} minDistance={4.5} maxDistance={13}
            maxPolarAngle={1.42} minPolarAngle={0.6} autoRotate autoRotateSpeed={0.45}
            target={[0, 0.4, 0]}
          />
          <EffectComposer>
            <Bloom intensity={0.75} luminanceThreshold={0.22} luminanceSmoothing={0.3} mipmapBlur />
            <Vignette eskil={false} offset={0.22} darkness={0.78} />
          </EffectComposer>
        </Canvas>
      </div>
      <div className="scene-hint">✦ {lang === "uk" ? "клік — перевернути карту" : lang === "en" ? "click a card to flip it" : "клик — перевернуть карту"} · drag — orbit · scroll — zoom ✦</div>
    </div>
  );
}
