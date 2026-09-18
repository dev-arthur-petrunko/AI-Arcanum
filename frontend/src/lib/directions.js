/** Напрямки-сторінки /directions/{slug} — 8 категорій із systems.category.
 *  Фільтрація — клієнтська, через GET /stats (бекенд не чіпаємо).
 *  normCat() — канонізація категорій БД (ru/uk) до ключа напрямку.
 */

/** Канонічні ключі категорій (порядок карток на головній). */
export const CAT_ORDER = [
  "divination",
  "oracles",
  "therapeutic",
  "astrological",
  "shamanic",
  "calendar",
  "esoteric",
  "numerological",
];

/** Нормалізує systems.category (ru/uk) до канонічного ключа. */
export function normCat(c) {
  const s = (c || "").toString().trim().toLowerCase();
  if (s.includes("гадател") || s.includes("гадалн")) return "divination";
  if (s.includes("оракул")) return "oracles";
  if (s.includes("терапевт")) return "therapeutic";
  if (s.includes("астролог")) return "astrological";
  if (s.includes("шаман")) return "shamanic";
  if (s.includes("календар")) return "calendar";
  if (s.includes("езотер") || s.includes("эзотер")) return "esoteric";
  if (s.includes("нумеролог")) return "numerological";
  return "other";
}

export const DIRECTIONS = [
  {
    slug: "divination",
    icon: "🔮",
    title: { ru: "Гадальные", uk: "Гадальні", en: "Divination" },
    desc: {
      ru: "Таро, Ленорман, руны, И-Цзин и другие системы предсказания.",
      uk: "Таро, Ленорман, руни, І-Цзин та інші системи передбачення.",
      en: "Tarot, Lenormand, runes, I-Ching and other fortune-telling systems.",
    },
    systemsHint: ["Таро", "Ленорман", "І-Цзин", "Руни", "Циганські карти", "Гральні карти", "Огам", "Карти снів", "Багуа", "Іфа", "Тасеографія"],
    articleMatch: ["таро", "ленорман", "рун", "цзин", "цыган", "циган", "игральн", "гральн", "огам", "снов", "багуа", "ифа", "іфа", "тасеограф"],
    hasSpreads: true,
  },
  {
    slug: "oracles",
    icon: "🌙",
    title: { ru: "Оракулы", uk: "Оракули", en: "Oracles" },
    desc: {
      ru: "Свободные оракульные колоды: фазы Луны и работа с циклами.",
      uk: "Вільні оракульні колоди: фази Місяця й робота з циклами.",
      en: "Free-form oracle decks: Moon phases and cycle work.",
    },
    systemsHint: ["Місячні фази"],
    articleMatch: ["оракул", "лун", "місяц"],
    hasSpreads: false,
  },
  {
    slug: "therapeutic",
    icon: "🌿",
    title: { ru: "Терапевтические", uk: "Терапевтичні", en: "Therapeutic" },
    desc: {
      ru: "Объединённая колода 85: сильные стороны VIA, каналы COPE и потребности Маслоу.",
      uk: "Об'єднана колода 85: сильні сторони VIA, канали COPE і потреби Маслоу.",
      en: "Combined deck of 85: VIA strengths, COPE channels and Maslow needs.",
    },
    systemsHint: ["Терапевтичні карти"],
    articleMatch: ["мак", "cope", "коп", "эмоц", "емоц", "ценност", "цінност", "ресурс", "афірмац", "аффирм", "желан", "бажан", "предк", "роду", "терапевт"],
    hasSpreads: false,
  },
  {
    slug: "astrological",
    icon: "⭐",
    title: { ru: "Астрологические", uk: "Астрологічні", en: "Astrological" },
    desc: {
      ru: "Звёзды как язык символов: оракул, сабианские символы, накшатры.",
      uk: "Зорі як мова символів: оракул, сабіанські символи, накшатри.",
      en: "Stars as a symbolic language: oracle, Sabian symbols, nakshatras.",
    },
    systemsHint: ["Астрологічний оракул", "Сабіанські символи", "Накшатри", "Астрологічний довідник"],
    articleMatch: ["астро", "сабиан", "сабіан", "накшатр", "знак", "планет", "дом", "аспект", "овен", "телец", "солнце", "луна", "зодиак"],
    hasSpreads: false,
  },
  {
    slug: "shamanic",
    icon: "🦉",
    title: { ru: "Шаманские", uk: "Шаманські", en: "Shamanic" },
    desc: {
      ru: "Оракул тотемов: животные-проводники и сила природы.",
      uk: "Оракул тотемів: тварини-провідники й сила природи.",
      en: "Totem oracle: spirit animals and the power of nature.",
    },
    systemsHint: ["Оракул тотемів"],
    articleMatch: ["шаман", "тотем"],
    hasSpreads: false,
  },
  {
    slug: "calendar",
    icon: "📅",
    title: { ru: "Календарные", uk: "Календарні", en: "Calendar" },
    desc: {
      ru: "Время как система: Цолькин майя и китайский зодиак.",
      uk: "Час як система: Цолькин майя та китайський зодіак.",
      en: "Time as a system: the Maya Tzolk'in and the Chinese zodiac.",
    },
    systemsHint: ["Цолькин", "Китайський зодіак"],
    articleMatch: ["цолькин", "тцолькин", "майя", "китай", "зодиак", "зодіак"],
    hasSpreads: false,
  },
  {
    slug: "esoteric",
    icon: "🜂",
    title: { ru: "Эзотерические", uk: "Езотеричні", en: "Esoteric" },
    desc: {
      ru: "Нумерология, чакры, стихии, каббала, кристаллы, ангелы.",
      uk: "Нумерологія, чакри, стихії, каббала, кристали, ангели.",
      en: "Numerology, chakras, elements, kabbalah, crystals, angels.",
    },
    systemsHint: ["Нумерологія", "Чакри", "Карти стихій", "Ангельський оракул", "Каббала", "Кристали"],
    articleMatch: ["нумеро", "чакр", "стих", "ангел", "каббала", "сфирот", "сфірот", "кристал", "архангел"],
    hasSpreads: false,
  },
  {
    slug: "numerological",
    icon: "🔢",
    title: { ru: "Нумерологические", uk: "Нумерологічні", en: "Numerological" },
    desc: {
      ru: "Язык чисел: числа-ангелы и числовые коды дня.",
      uk: "Мова чисел: числа-ангели й числові коди дня.",
      en: "The language of numbers: angel numbers and daily codes.",
    },
    systemsHint: ["Числа-ангели"],
    articleMatch: ["числ", "ангел", "нумеро"],
    hasSpreads: false,
  },
];

export const directionBySlug = (slug) => DIRECTIONS.find((d) => d.slug === slug);

/** Чи належить стаття напрямку (за полем system, нечіткий збіг). */
export function articleBelongs(article, direction) {
  const sys = (article?.system || "").toString().toLowerCase();
  if (!sys) return false;
  return direction.articleMatch.some((m) => sys.includes(m));
}
