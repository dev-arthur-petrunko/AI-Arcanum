import { useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import { Html } from "@react-three/drei";
import * as THREE from "three";

/**
 * Card3D — настоящие R3F-меши (не CSS-иллюзия).
 * Паттерн взят как референс из devantic/react-flipcard3d (Front/Back + flipped),
 * но переписан на mesh-rotate: boxGeometry толщиной + две текстуры (рубашка/лицо).
 * Клик -> gsap-анимация переворота; hover -> лёгкий lift.
 */
export default function Card3D({ position = [0, 0, 0], frontColor = "#f5edd8", backColor = "#1b2340", label = "Шут", onFlip }) {
  const ref = useRef();
  const [flipped, setFlipped] = useState(false);
  const [hovered, setHovered] = useState(false);
  const target = useRef(0);

  useFrame((_, dt) => {
    const goal = flipped ? Math.PI : 0;
    target.current = THREE.MathUtils.damp(target.current, goal, 6, dt);
    if (ref.current) {
      ref.current.rotation.y = target.current;
      ref.current.position.y = position[1] + (hovered ? 0.12 : 0);
    }
  });

  return (
    <mesh
      ref={ref}
      position={position}
      onClick={() => {
        const next = !flipped;
        setFlipped(next);
        onFlip?.(next);
      }}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <boxGeometry args={[1.7, 2.8, 0.04]} />
      {/* 6 материалов box: [px, nx, py, ny, pz(front), nz(back)] */}
      <meshStandardMaterial color={backColor} />
      <meshStandardMaterial color={backColor} />
      <meshStandardMaterial color="#888" />
      <meshStandardMaterial color="#888" />
      <meshStandardMaterial color={flipped ? backColor : frontColor} />
      <meshStandardMaterial color={flipped ? frontColor : backColor} />
      <Html center distanceFactor={8} occlude={false} style={{ pointerEvents: "none" }}>
        <div style={{
          width: 140, textAlign: "center", fontSize: 13, color: flipped ? "#fff" : "#222",
          background: "transparent", userSelect: "none"
        }}>{label}</div>
      </Html>
    </mesh>
  );
}
