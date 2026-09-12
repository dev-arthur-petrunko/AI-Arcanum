import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stars, ContactShadows, Environment } from "@react-three/drei";
import Card3D from "./Card3D";

/** DeckShelf3D: "полка" — веер карт + орбитальная камера + звёздный фон. */
export default function DeckShelf3D({ cards = [], onSelect }) {
  const fan = cards.length ? cards : [{ name: "Шут" }, { name: "Маг" }, { name: "Жрица" }, { name: "Мир" }];
  return (
    <div style={{ height: 480, borderRadius: 16, overflow: "hidden", background: "#0b0e1a" }}>
      <Canvas camera={{ position: [0, 2.4, 6], fov: 45 }}>
        <ambientLight intensity={0.6} />
        <directionalLight position={[4, 6, 4]} intensity={1.2} />
        <Stars radius={60} depth={40} count={2500} factor={4} fade />
        {fan.slice(0, 9).map((c, i) => {
          const n = fan.slice(0, 9).length;
          const x = (i - (n - 1) / 2) * 1.1;
          return (
            <Card3D key={c.id ?? i} position={[x, 0.4, -Math.abs(x) * 0.12]}
              label={c.name} onFlip={(f) => f && onSelect?.(c)} />
          );
        })}
        {/* стол */}
        <mesh position={[0, -1.2, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[30, 30]} />
          <meshStandardMaterial color="#141a33" roughness={0.9} />
        </mesh>
        <ContactShadows position={[0, -1.19, 0]} opacity={0.6} scale={12} blur={2} />
        <OrbitControls enablePan={false} minDistance={3} maxDistance={12} maxPolarAngle={1.45} />
      </Canvas>
    </div>
  );
}
