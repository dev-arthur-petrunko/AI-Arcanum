import zones00 from "./zones00";
import zonesMajorA from "./zonesMajorA";
import zonesMajorB from "./zonesMajorB";
import zonesWands from "./zonesWands";
import zonesCups from "./zonesCups";
import zonesSwords from "./zonesSwords";
import zonesPents from "./zonesPents";

/** Усі зони символіки колоди RWS, згруповані за card.number. */
export const RWS_ZONES = { ...zones00, ...zonesMajorA, ...zonesMajorB, ...zonesWands, ...zonesCups, ...zonesSwords, ...zonesPents };

/** Чи є інтерактивні зони для даної карти колоди (key = card.number). */
export function hasZones(key) {
  return Array.isArray(RWS_ZONES[key]) && RWS_ZONES[key].length > 0;
}

/** Повертає зони карти. Завжди масив (порожній, якщо дані відсутні). */
export function zonesFor(key) {
  return hasZones(key) ? RWS_ZONES[key] : [];
}