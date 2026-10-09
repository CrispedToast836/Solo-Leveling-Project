// Service worker do SISTEMA (opcional, mas recomendado).
// Fica na MESMA pasta do index.html (www/), servido em HTTPS pelo GitHub Pages.
// No APK (Capacitor) ele não é usado. Ele guarda o app em cache para abrir offline.
// Estratégia: tenta a rede primeiro; sem internet, usa o cache.

const CACHE = 'sistema-v4';   // mude o número quando atualizar o app

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(['./', './index.html']))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  // Tiles do mapa: vão direto para a rede (não enchem o cache do celular)
  const host = new URL(e.request.url).hostname;
  if (host === 'tile.openstreetmap.org' || host.endsWith('basemaps.cartocdn.com')) return;
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});
