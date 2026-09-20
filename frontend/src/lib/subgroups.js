/** Підкатегорії (directory_group) у межах напрямку «Гадальні».
 *  Ключ — стабільне значення decks.directory_group; title локалізує заголовок
 *  групи, history — коротка історія унікальності підкатегорії.
 *  Якщо ключа немає — заголовок показує саму назву групи без опису.
 */
export const SUBGROUPS = {
  "Таро · Вейта-Сміт": {
    title: { uk: "Таро Вейта-Сміт", ru: "Таро Уэйта-Смит", en: "Rider-Waite-Smith Tarot" },
    history: {
      uk: "Колода 1909 року Артура Едварда Вейта та художниці Памели Колман Сміт: повні сюжетні малюнки на всіх 78 картах зробили її «еталоном» образного Таро XX століття.",
      ru: "Колода 1909 года Артура Эдварда Уэйта и художницы Памелы Колман Смит: полные сюжетные рисунки на всех 78 картах сделали её «эталоном» образного Таро XX века.",
      en: "A 1909 deck by A. E. Waite and artist Pamela Colman Smith: full scenic pictures on all 78 cards made it the image-defining 'standard' of 20th-century Tarot.",
    },
  },
  "Таро · Вісконті-Сфорца": {
    title: { uk: "Таро Вісконті-Сфорца", ru: "Таро Висконти-Сфорца", en: "Visconti-Sforza Tarot" },
    history: {
      uk: "Найстаріша збережена колода Таро (бл. 1450, Мілан): рукописні карти з золотом і сріблом для родини Сфорца — свідок самого народження Старших арканів.",
      ru: "Старейшая сохранившаяся колода Таро (ок. 1450, Милан): рукописные карты с золотом и серебром для семьи Сфорца — свидетель самого рождения Старших арканов.",
      en: "The oldest surviving Tarot (c. 1450, Milan): hand-painted gold-and-silver cards for the Sforza family — a witness to the very birth of the Major Arcana.",
    },
  },
  "Таро · Марсель": {
    title: { uk: "Таро Марсель", ru: "Таро Марсель", en: "Tarot de Marseille" },
    history: {
      uk: "Класична французька ксилографічна колода XVIII ст.: спрощені, симетричні малюнки, за якими стоїть усталений канон Традиції Марселя — основа всієї французької школи.",
      ru: "Классическая французская ксилографическая колода XVIII века: упрощённые симметричные рисунки, за которыми стоит устойчивый канон Марсельской традиции — основа всей французской школы.",
      en: "The classic 18th-century French woodblock deck: simplified, symmetric images standing on the fixed canon of the Marseille Tradition — the root of the French Tarot school.",
    },
  },
  "Ленорман": {
    title: { uk: "Ленорман", ru: "Ленорман", en: "Lenormand" },
    history: {
      uk: "Мала колода «Petit Lenormand» (бл. 1799): 36 звичайних побутових образів без символічного шару Таро — читається парами й тріадами, що змінюють значення карти.",
      ru: "Малая колода «Petit Lenormand» (ок. 1799): 36 простых бытовых образов без символического слоя Таро — читается парами и триадами, меняющими значение карты.",
      en: "Grande and Petit Lenormand (c. 1799): 36 plain everyday images with no Tarot symbolism — read in pairs and triads that flip each card's meaning.",
    },
  },
  "І-Цзин": {
    title: { uk: "І-Цзин", ru: "И-Цзин", en: "I Ching" },
    history: {
      uk: "«Книга змін» — одна з найдавніших мантичних систем: 64 гексаграми, складені з восьми триграм, описують ситуацію через три лінії «так / ні» інтимо-як-процес.",
      ru: "«Книга перемен» — одна из древнейших мантических систем: 64 гексаграммы из восьми триграмм описывают ситуацию через три черты «да / нет» как процесс.",
      en: "The Book of Changes, one of the oldest divination systems: 64 hexagrams built from eight trigrams describe a situation line-by-line as a process of becoming.",
    },
  },
  "Руни та Огам": {
    title: { uk: "Руни та Огам", ru: "Руны и Огам", en: "Runes & Ogham" },
    history: {
      uk: "Дві «азбуки-оракули»: скандинавські руни (Старший Футарк, II–VIII ст.) і кельтський Огам (IV–VI ст.) — кожний знак має своє ім'я, стихію й є цілою літерою-символом.",
      ru: "Две «азбуки-оракула»: скандинавские руны (Старший Футарк, II–VIII вв.) и кельтский Огам (IV–VI вв.) — каждый знак имеет имя, стихию и является целой буквой-символом.",
      en: "Two alphabet-oracles: Norse runes (Elder Futhark, 2nd–8th c.) and Celtic Ogham (4th–6th c.) — each sign has a name, an element and is a symbol-letter of its own.",
    },
  },
  "Циганські та гральні карти": {
    title: { uk: "Циганські та гральні карти", ru: "Цыганские и игральные карты", en: "Gypsy & Playing Cards" },
    history: {
      uk: "Народне ворожіння без сакрального шару: 36 побутових сцен, де кожна карта має «пряме» значення, і традиція читається за звичайною колодою.",
      ru: "Народное гадание без сакрального слоя: 36 бытовых сцен, где каждая карта имеет «прямое» значение, читается обычной колодой.",
      en: "Folk divination with no sacred layer: 36 everyday scenes where each card has a 'direct' meaning, read with an ordinary deck.",
    },
  },
  "Карти снів": {
    title: { uk: "Карти снів", ru: "Карты снов", en: "Dream Cards" },
    history: {
      uk: "Навчальний словник образів сновидінь: вода, змія, політ, зуби — значення подані простими словами як власний переказ класичної символіки снів.",
      ru: "Учебный словарь образов сновидений: вода, змея, полёт, зубы — значения даны простыми словами как собственный пересказ классической символики снов.",
      en: "A study dictionary of dream images: water, snake, flying, teeth — meanings given in plain words as an own retelling of classic dream symbolism.",
    },
  },
  "Іфа": {
    title: { uk: "Іфа", ru: "Ифа", en: "Ifa" },
    history: {
      uk: "Ворожіння народу йоруба: 16 основних знаків (Oju Odù) і 240 комбінованих (Omo Odù) — 256 карт, що відтворюють повну систему опритування.",
      ru: "Гадание народа йоруба: 16 основных знаков (Oju Odù) и 240 комбинированных (Omo Odù) — 256 карт, воспроизводящие полную систему прорицания.",
      en: "Yoruba divination: 16 principal marks (Oju Odù) and 240 combined ones (Omo Odù) — 256 cards reproducing the full Ifa oracle system.",
    },
  },
  "Тасеографія": {
    title: { uk: "Тасеографія", ru: "Тасеография", en: "Tasseography" },
    history: {
      uk: "Ворожіння по чайних листках у чашці: кожен символ (якір, птах, ключ…) має усталене тлумачення; значення подано як власний переказ довідника.",
      ru: "Гадание по чайным листьям в чашке: каждый символ (якорь, птица, ключ…) имеет устоявшееся толкование; значения даны как собственный пересказ справочника.",
      en: "Tea-leaf reading in a cup: every symbol (anchor, bird, key…) has a fixed meaning; interpretations are given as an own retelling of a reference dictionary.",
    },
  },
  "Багуа": {
    title: { uk: "Багуа", ru: "Багуа", en: "Bagua" },
    history: {
      uk: "Вісім триграм китайської філософії (небо, озеро, вогонь, грім…): кожна — з родинною роллю, стихією і стороною світу; триграми складають гексаграми І-Цзин.",
      ru: "Восемь триграмм китайской философии (небо, озеро, огонь, гром…): каждая — с семейной ролью, стихией и стороной света; триграммы складывают гексаграммы И-Цзин.",
      en: "Eight trigrams of Chinese philosophy (Heaven, Lake, Fire, Thunder…): each with a family role, element and compass direction; trigrams stack into I-Ching hexagrams.",
    },
  },
};

/** Повертає {title, history} для directory_group у потрібній мові (або null). */
export function subgroupInfo(group, lang) {
  const s = SUBGROUPS[group];
  if (!s) return null;
  return {
    title: s.title[lang] || s.title.uk,
    history: s.history[lang] || s.history.uk,
  };
}