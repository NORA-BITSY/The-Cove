const CACHE = 'cove-v2';

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE).then(c =>
      c.addAll(['/'])            // precache the app shell only
    )
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
});

// Optional: add Stale-While-Revalidate caching for GET /api/*
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then(response => {
      const fetchPromise = fetch(event.request).then(networkResponse => {
        caches.open(CACHE).then(cache => cache.put(event.request, networkResponse.clone()));
        return networkResponse;
      });
      return response || fetchPromise;
    })
  );
});
