import { D_AG } from "./a-g";
import { D_DK } from "./d-k";
import { D_LO } from "./l-o";
import { D_PZ } from "./p-z";

/** Всі символи сонника одним масивом. Кожна запись: { id, icon,
 *  name: {uk,ru,en}, keywords: {uk,ru,en}, text: {uk,ru,en} }. */
export const DREAMS = [...D_AG, ...D_DK, ...D_LO, ...D_PZ];

/** Алфавіти для чип-навігації по першій літері. */
export const ALPHABETS = {
  uk: "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯ",
  ru: "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
  en: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
};