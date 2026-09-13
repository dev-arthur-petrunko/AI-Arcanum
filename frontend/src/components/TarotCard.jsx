"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { backTexture, frontFallbackTexture } from "../lib/textures";

/**
 * Одна карта: товстий бокс, лице (скан RWS або процедурна заглушка),
 * сорочка (процедурна), переворот по кліку, паріння й підсвітка при наведенні.
 */
export default function TarotCard({ card, position, rotationY = 0, phase = 0, label, initialFlipped = false, onSelect }) {
  const mesh = useRef();
  const glow = useRef();
  const [flipped, setFlipped] = useState(initialFlipped);
  const [hovered, setHovered] = useState(false);
  const [photo, setPhoto] = useState(null);
  const rot = useRef(rotationY + (initialFlipped ? Math.PI : 0));
  const lift = useRef(0);

  const back = useMemo(() => backTexture(), []);
  const fallback = useMemo(() => frontFallbackTexture(label), [label]);

  useEffect(() => {
    if (!card?.image_path) return;
    let alive = true;
    new THREE.TextureLoader().load(
      card.image_path,
      (t) => { if (alive) { t.colorSpace = THREE.SRGBColorSpace; setPhoto(t); } },
      undefined,
      () => {}
    );
    return () => { alive = false; };
  }, [card?.image_path]);

  useFrame((state, dt) => {
    const t = state.clock.elapsedTime;
    const targetRot = rotationY + (flipped ? Math.PI : 0);
    rot.current = THREE.MathUtils.damp(rot.current, targetRot, 5, dt);
    lift.current = THREE.MathUtils.damp(lift.current, hovered ? 0.35 : 0, 6, dt);
    if (mesh.current) {
      mesh.current.rotation.y = rot.current;
      mesh.current.position.y = position[1] + Math.sin(t * 1.1 + phase) * 0.07 + lift.current;
      const s = hovered ? 1.06 : 1;
      mesh.current.scale.setScalar(THREE.MathUtils.damp(mesh.current.scale.x, s, 8, dt));
    }
    if (glow.current) glow.current.material.opacity = THREE.MathUtils.damp(
      glow.current.material.opacity, hovered ? 0.55 : 0, 8, dt
    );
  });

  const face = photo || fallback;
  const mats = useMemo(() => {
    const edge = new THREE.MeshStandardMaterial({ color: "#2a2415", roughness: 0.6 });
    const mFront = new THREE.MeshStandardMaterial({ map: face, roughness: 0.55 });
    const mBack = new THREE.MeshStandardMaterial({ map: back, roughness: 0.55 });
    // порядок box: +x, -x, +y, -y, +z (лице), -z (сорочка)
    return [edge, edge, edge, edge, mFront, mBack];
  }, [face, back]);

  return (
    <group position={position} rotation={[0, 0, 0]}>
      {/* золоте світіння-підкладка при наведенні */}
      <mesh ref={glow} rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.32, 0]}>
        <planeGeometry args={[2.4, 2.4]} />
        <meshBasicMaterial color="#d4a94e" transparent opacity={0} depthWrite={false} />
      </mesh>
      <mesh
        ref={mesh}
        material={mats}
        rotation={[0, rotationY, 0]}
        onClick={(e) => { e.stopPropagation(); const n = !flipped; setFlipped(n); if (n) onSelect?.(card); }}
        onPointerOver={(e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = "pointer"; }}
        onPointerOut={() => { setHovered(false); document.body.style.cursor = "auto"; }}
      >
        <boxGeometry args={[1.5, 2.6, 0.05]} />
      </mesh>
    </group>
  );
}
