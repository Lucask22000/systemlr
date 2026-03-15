(function () {
    const DISMISS_KEY = 'systemlr:pwa-install-dismissed-at';
    const INSTALLED_KEY = 'systemlr:pwa-installed';
    const DISMISS_TTL_MS = 7 * 24 * 60 * 60 * 1000;
    let deferredPrompt = null;
    let promptNode = null;

    function isMobileViewport() {
        return window.matchMedia('(max-width: 991px)').matches;
    }

    function isMobileDevice() {
        return /Android|iPhone|iPad|iPod|Mobile/i.test(window.navigator.userAgent || '') || isMobileViewport();
    }

    function isIosSafari() {
        const ua = window.navigator.userAgent || '';
        const isIos = /iPhone|iPad|iPod/i.test(ua);
        const isSafari = /Safari/i.test(ua) && !/CriOS|FxiOS|EdgiOS/i.test(ua);
        return isIos && isSafari;
    }

    function isStandaloneMode() {
        return window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
    }

    function hasRecentDismissal() {
        try {
            const stored = Number(window.localStorage.getItem(DISMISS_KEY) || 0);
            return stored > 0 && (Date.now() - stored) < DISMISS_TTL_MS;
        } catch (_) {
            return false;
        }
    }

    function markDismissed() {
        try {
            window.localStorage.setItem(DISMISS_KEY, String(Date.now()));
        } catch (_) {
            return;
        }
    }

    function markInstalled() {
        try {
            window.localStorage.setItem(INSTALLED_KEY, '1');
            window.localStorage.removeItem(DISMISS_KEY);
        } catch (_) {
            return;
        }
    }

    function shouldShowPrompt() {
        if (!isMobileDevice() || isStandaloneMode()) {
            return false;
        }

        try {
            if (window.localStorage.getItem(INSTALLED_KEY) === '1') {
                return false;
            }
        } catch (_) {
            return false;
        }

        return !hasRecentDismissal();
    }

    function getAppName() {
        if (document.body && document.body.dataset && document.body.dataset.appInstallName) {
            return document.body.dataset.appInstallName;
        }
        return 'SystemLR';
    }

    function ensurePromptNode() {
        if (promptNode) {
            return promptNode;
        }

        promptNode = document.createElement('aside');
        promptNode.className = 'pwa-install-shell';
        promptNode.innerHTML = [
            '<div class="pwa-install-card" role="dialog" aria-live="polite" aria-label="Adicionar app a tela inicial">',
            '  <div class="pwa-install-copy">',
            '    <strong class="pwa-install-title"></strong>',
            '    <p class="pwa-install-text" data-pwa-copy></p>',
            '  </div>',
            '  <div class="pwa-install-actions">',
            '    <button type="button" class="btn btn-primary" data-pwa-install>Adicionar agora</button>',
            '    <button type="button" class="btn btn-outline-secondary" data-pwa-dismiss>Agora nao</button>',
            '  </div>',
            '</div>',
        ].join('');

        promptNode.querySelector('[data-pwa-dismiss]').addEventListener('click', function () {
            hidePrompt(true);
        });

        promptNode.querySelector('[data-pwa-install]').addEventListener('click', async function () {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const choice = await deferredPrompt.userChoice;
                if (choice && choice.outcome === 'accepted') {
                    markInstalled();
                    hidePrompt(false);
                } else {
                    hidePrompt(true);
                }
                deferredPrompt = null;
                return;
            }

            if (isIosSafari()) {
                hidePrompt(true);
            }
        });

        document.body.appendChild(promptNode);
        return promptNode;
    }

    function refreshPromptCopy() {
        const node = ensurePromptNode();
        const titleEl = node.querySelector('.pwa-install-title');
        const copyEl = node.querySelector('[data-pwa-copy]');
        const installButton = node.querySelector('[data-pwa-install]');

        titleEl.textContent = 'Adicionar ' + getAppName() + ' a tela inicial';

        if (deferredPrompt) {
            copyEl.textContent = 'Instale como app para abrir mais rapido, usar em tela cheia e facilitar o acesso no celular.';
            installButton.hidden = false;
            installButton.textContent = 'Adicionar agora';
            return true;
        }

        if (isIosSafari()) {
            copyEl.textContent = 'No iPhone, toque em Compartilhar e depois em Adicionar a Tela de Inicio para usar o sistema como app.';
            installButton.hidden = true;
            return true;
        }

        return false;
    }

    function showPrompt() {
        if (!shouldShowPrompt()) {
            return;
        }

        if (!refreshPromptCopy()) {
            return;
        }

        ensurePromptNode().classList.add('is-visible');
    }

    function hidePrompt(rememberDismissal) {
        if (rememberDismissal) {
            markDismissed();
        }

        if (promptNode) {
            promptNode.classList.remove('is-visible');
        }
    }

    function registerServiceWorker() {
        if (!('serviceWorker' in navigator)) {
            return;
        }

        window.addEventListener('load', function () {
            navigator.serviceWorker.register('/sw.js').catch(function () {
                return;
            });
        });
    }

    window.addEventListener('beforeinstallprompt', function (event) {
        event.preventDefault();
        deferredPrompt = event;
        showPrompt();
    });

    window.addEventListener('appinstalled', function () {
        markInstalled();
        hidePrompt(false);
    });

    document.addEventListener('DOMContentLoaded', function () {
        registerServiceWorker();

        if (shouldShowPrompt() && isIosSafari()) {
            window.setTimeout(showPrompt, 900);
        }
    });
})();
