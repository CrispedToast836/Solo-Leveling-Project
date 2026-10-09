// Service worker ANTIGO (da época em que o app ficava na raiz do site).
// O app mudou para www/ e tem o próprio www/sw.js. Este arquivo só existe
// para desinstalar o service worker velho de quem já tinha aberto o site.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.registration.unregister())
  );
});
