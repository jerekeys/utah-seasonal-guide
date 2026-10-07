const VERSION = 'utah-guide-2026-10-07-coverage-8';
const CORE = VERSION + '-core', PAGES = VERSION + '-pages', IMAGES = VERSION + '-images';
const SHELL = ['/', '/saved/', '/app/', '/offline/', '/assets/data.js', '/assets/site.js', '/assets/vibes.js', '/assets/date-tools.js', '/assets/event-enhancements.js', '/assets/app.js', '/assets/styles.css', '/assets/date-tools.css', '/assets/seasonal.css', '/assets/favicon.svg', '/assets/art/seasonal/winter-community.svg', '/manifest.webmanifest', '/assets/app/icon-192.png', '/assets/app/icon-512.png', '/assets/app/icon-180.png', '/assets/app/icon-maskable-512.png'];
self.addEventListener('install', event => event.waitUntil(caches.open(CORE).then(cache => cache.addAll(SHELL))));
self.addEventListener('activate', event => event.waitUntil((async () => {
  for (const key of await caches.keys()) if (key.startsWith('utah-guide-') && ![CORE, PAGES, IMAGES].includes(key)) await caches.delete(key);
  await self.clients.claim();
})()));
self.addEventListener('message', event => { if (event.data?.type === 'ACTIVATE_UPDATE') self.skipWaiting(); });
async function remember(cacheName, request, response, limit) {
  if (!response.ok || response.type === 'opaque') return;
  const cache = await caches.open(cacheName); await cache.put(request, response.clone());
  const keys = await cache.keys(); if (keys.length > limit) await cache.delete(keys[0]);
}
self.addEventListener('fetch', event => {
  const request = event.request, url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;
  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const response = await fetch(request);
        if (response.ok && response.headers.get('content-type')?.includes('text/html') && new URL(response.url).origin === url.origin) await remember(PAGES, request, response, 60);
        return response;
      } catch { return await caches.match(request) || (url.pathname === '/' ? await caches.match('/') : null) || await caches.match('/offline/'); }
    })());
  } else if (request.destination === 'image') {
    event.respondWith((async () => {
      const cached = await caches.match(request); if (cached) return cached;
      try { const response = await fetch(request); await remember(IMAGES, request, response, 100); return response; }
      catch { return new Response('', { status: 503 }); }
    })());
  } else if (url.pathname.startsWith('/assets/') || url.pathname === '/manifest.webmanifest') {
    event.respondWith((async () => {
      try {
        const response = await fetch(request);
        if (SHELL.includes(url.pathname) && response.ok) await (await caches.open(CORE)).put(request, response.clone());
        return response;
      } catch { return await caches.match(request) || new Response('', { status: 503 }); }
    })());
  }
});
