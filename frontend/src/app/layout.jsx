import "./globals.css";

export const metadata = {
  title: "AI-Arcanum — енциклопедія ворожбильних карт",
  description: "Таро, Ленорман, І-Цзин, руни: інтерактивна 3D-енциклопедія (UK/RU/EN). Backend — 100% Python.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="uk">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Manrope:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
