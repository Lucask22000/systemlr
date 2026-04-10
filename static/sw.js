const CACHE_VERSION = 'v5';
const STATIC_CACHE = `systemlr-static-${CACHE_VERSION}`;
const PAGE_CACHE = `systemlr-pages-${CACHE_VERSION}`;
const IMAGE_CACHE = `systemlr-images-${CACHE_VERSION}`;
const FONT_CACHE = `systemlr-fonts-${CACHE_VERSION}`;
const APP_SHELL = [
    '/',
    '/manifest.webmanifest',
    '/static/icons/pwa/store-192.png',
    '/static/icons/pwa/store-512.png',
];

async function fromNetworkThenCache(request, cacheName) {
    const cache = await caches.open(cacheName);
    const response = await fetch(request);
    if (response && response.ok) {
        cache.put(request, response.clone());
    }
    return response;
}

async function staleWhileRevalidate(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    const networkPromise = fetch(request)
        .then((response) => {
            if (response && response.ok) {
                cache.put(request, response.clone());
            }
            return response;
        })
        .catch(() => null);

    return cached || networkPromise;
}

async function networkFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    try {
        const response = await fetch(request);
        if (response && response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (_) {
        const cached = await cache.match(request);
        if (cached) {
            return cached;
        }
        throw _;
    }
}

self.addEventListener('install', (event) => {
    event.waitUntil((async () => {
        const cache = await caches.open(STATIC_CACHE);
        await cache.addAll(APP_SHELL);
        await self.skipWaiting();
    })());
});

self.addEventListener('activate', (event) => {
    event.waitUntil((async () => {
        const cacheNames = await caches.keys();
        await Promise.all(
            cacheNames
                .filter((cacheName) => ![STATIC_CACHE, PAGE_CACHE, IMAGE_CACHE, FONT_CACHE].includes(cacheName))
                .map((cacheName) => caches.delete(cacheName))
        );
        await self.clients.claim();
    })());
});

self.addEventListener('fetch', (event) => {
    const { request } = event;
    if (request.method !== 'GET') {
        return;
    }

    const url = new URL(request.url);
    if (url.origin !== self.location.origin) {
        if (request.destination === 'font') {
            event.respondWith(staleWhileRevalidate(request, FONT_CACHE));
        }
        return;
    }

    if (request.mode === 'navigate') {
        event.respondWith(networkFirst(request, PAGE_CACHE));
        return;
    }

    if (request.destination === 'style' || request.destination === 'script' || request.destination === 'manifest') {
        event.respondWith(networkFirst(request, STATIC_CACHE));
        return;
    }

    if (request.destination === 'image') {
        event.respondWith(staleWhileRevalidate(request, IMAGE_CACHE));
        return;
    }

    if (request.destination === 'font') {
        event.respondWith(staleWhileRevalidate(request, FONT_CACHE));
        return;
    }
});
