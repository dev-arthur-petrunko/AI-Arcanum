/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Same-origin проксі: браузер завжди ходить в /api (свій origin),
  // Next перекидає на Python-бекенд. Ніяких зашитих хостів у бандлі + нема CORS.
  async rewrites() {
    return [
      { source: "/api/:path*", destination: "http://127.0.0.1:8001/:path*" },
    ];
  },
};
module.exports = nextConfig;
