self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open('edudhvani').then(function(cache) {
      return cache.addAll([
        '/',
        '/static/site.css'
      ]);
    })
  );
});
self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});