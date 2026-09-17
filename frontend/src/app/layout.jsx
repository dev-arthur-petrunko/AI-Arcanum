import "./globals.css";

export const metadata = {
  title: "AI-Arcanum — енциклопедія ворожбильних карт",
  description: "Таро, Ленорман, І-Цзин, руни, оракули, психологічні й символічні системи: інтерактивна 3D-енциклопедія (UK/RU/EN). Backend — 100% Python.",
  icons: { icon: "/icon.svg", shortcut: "/icon.svg", apple: "/icon.svg" },
};

export default function RootLayout({ children }) {
  return (
    <html lang="uk" data-theme="dark">
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: "try{document.documentElement.dataset.theme=localStorage.getItem('arcanum-theme')||'dark'}catch(e){}",
          }}
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){function open(){try{document.body.classList.add('side-open');document.body.style.overflow='hidden'}catch(e){}}function close(){try{document.body.classList.remove('side-open');document.body.style.overflow=''}catch(e){}}function dropToggle(t){var d=t.closest('.drop');if(d){d.classList.toggle('open')}}function dropClose(t){if(!t||!t.closest||t.closest('.drop'))return;var ds=document.querySelectorAll('.drop.open');for(var i=0;i<ds.length;i++)ds[i].classList.remove('open')}document.addEventListener('click',function(e){var t=e.target;if(!t||!t.classList)return;if(t.closest('.drop-btn')){dropToggle(t);return}if(t.closest('.burger')){open();return}if(t.closest('.side-overlay')||t.closest('.side-close')||t.closest('.side-drawer a')){if(document.body.classList.contains('side-open'))close();return}dropClose(t)});document.addEventListener('keydown',function(e){if(e.key==='Escape')close();var ds=document.querySelectorAll('.drop.open');for(var i=0;i<ds.length;i++)ds[i].classList.remove('open')});})();`,
          }}
        />
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
