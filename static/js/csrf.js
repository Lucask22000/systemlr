(function () {
    function readMetaToken() {
        var meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? (meta.getAttribute('content') || '') : '';
    }

    function getCsrfToken() {
        if (window.__CSRF_TOKEN__) {
            return window.__CSRF_TOKEN__;
        }
        var token = readMetaToken();
        if (token) {
            window.__CSRF_TOKEN__ = token;
        }
        return token;
    }

    function isUnsafeMethod(method) {
        var m = (method || 'GET').toUpperCase();
        return ['POST', 'PUT', 'PATCH', 'DELETE'].indexOf(m) >= 0;
    }

    function injectCsrfIntoForms() {
        var token = getCsrfToken();
        if (!token) return;

        var forms = document.querySelectorAll('form');
        forms.forEach(function (form) {
            var method = (form.getAttribute('method') || 'GET').toUpperCase();
            if (!isUnsafeMethod(method)) return;
            if (form.querySelector('input[name="csrf_token"]')) return;

            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'csrf_token';
            input.value = token;
            form.appendChild(input);
        });
    }

    function patchFetchWithCsrf() {
        if (!window.fetch) return;
        if (window.__fetch_csrf_patched__) return;
        window.__fetch_csrf_patched__ = true;

        var nativeFetch = window.fetch.bind(window);
        window.fetch = function (input, init) {
            init = init || {};
            var method = (init.method || 'GET').toUpperCase();
            if (!isUnsafeMethod(method)) {
                return nativeFetch(input, init);
            }

            var token = getCsrfToken();
            if (!token) {
                return nativeFetch(input, init);
            }

            var headers = new Headers(init.headers || {});
            if (!headers.has('X-CSRF-Token')) {
                headers.set('X-CSRF-Token', token);
            }
            init.headers = headers;
            return nativeFetch(input, init);
        };
    }

    document.addEventListener('DOMContentLoaded', function () {
        window.getCsrfToken = getCsrfToken;
        injectCsrfIntoForms();
        patchFetchWithCsrf();
    });
})();
