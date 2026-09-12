export const metadata = { title: "Fortune-telling Cards", description: "Энциклопедия гадательных карт: Таро, Ленорман, оракулы (RU/UK/EN)" };

export default function RootLayout({ children }) {
  return (
    <html lang="ru">
      <body style={{ margin: 0, background: "#0b0e1a", color: "#eee", fontFamily: "system-ui" }}>{children}</body>
    </html>
  );
}
