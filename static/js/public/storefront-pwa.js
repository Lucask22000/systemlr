(function () {
    const DISMISS_KEY = 'systemlr:store-pwa-dismissed-at';
    const INSTALLED_KEY = 'systemlr:store-pwa-installed';
    const DISMISS_TTL_MS = 7 * 24 * 60 * 60 * 1000;

    let deferredPrompt = null;

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

    function getNodes() {
        return {
            banner: document.querySelector('[data-store-install-banner]'),
            panels: Array.from(document.querySelectorAll('[data-store-install-panel]')),
            titles: Array.from(document.querySelectorAll('[data-store-install-title]')),
            copies: Array.from(document.querySelectorAll('[data-store-install-copy]')),
            actionButtons: Array.from(document.querySelectorAll('[data-store-install-action], [data-store-install-shortcut]')),
            dismissButton: document.querySelector('[data-store-install-dismiss]'),
        };
    }

    function refreshCopy(nodes) {
        const titleText = 'Baixar app da loja';
        const actionText = deferredPrompt ? 'Baixar app' : (isIosSafari() ? 'Como instalar' : 'Baixar app');
        const copyText = deferredPrompt
            ? ('Adicione ' + getAppName() + ' na tela inicial do celular e use a loja como web-app, direto pelo navegador.')
            : 'No iPhone, toque em Compartilhar e depois em Adicionar a Tela de Inicio para criar o atalho da loja.';

        nodes.titles.forEach(function (node) {
            node.textContent = titleText;
        });
        nodes.copies.forEach(function (node) {
            node.textContent = copyText;
        });
        nodes.actionButtons.forEach(function (button) {
            button.textContent = actionText;
            button.hidden = false;
        });
    }

    function hidePrompt(rememberDismissal) {
        const nodes = getNodes();
        if (rememberDismissal) {
            markDismissed();
        }
        if (nodes.banner) {
            nodes.banner.classList.remove('is-visible');
            nodes.banner.hidden = true;
        }
        nodes.panels.forEach(function (panel) {
            panel.hidden = true;
        });
    }

    function showPrompt() {
        const nodes = getNodes();
        if (!nodes.banner || !shouldShowPrompt()) {
            return;
        }
        if (!deferredPrompt && !isIosSafari()) {
            return;
        }
        refreshCopy(nodes);
        nodes.banner.hidden = false;
        nodes.banner.classList.add('is-visible');
        nodes.panels.forEach(function (panel) {
            panel.hidden = false;
        });
    }

    async function triggerInstall() {
        if (!shouldShowPrompt()) {
            return;
        }

        if (deferredPrompt) {
            deferredPrompt.prompt();
            const choice = await deferredPrompt.userChoice;
            if (choice && choice.outcome === 'accepted') {
                markInstalled();
                hidePrompt(false);
            } else {
                showPrompt();
            }
            deferredPrompt = null;
            return;
        }

        if (isIosSafari()) {
            showPrompt();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    function bindEvents() {
        const nodes = getNodes();

        nodes.actionButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                triggerInstall();
            });
        });

        if (nodes.dismissButton) {
            nodes.dismissButton.addEventListener('click', function () {
                hidePrompt(true);
            });
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
        bindEvents();

        if (shouldShowPrompt()) {
            const nodes = getNodes();
            refreshCopy(nodes);
            if (isIosSafari()) {
                window.setTimeout(showPrompt, 900);
            }
        } else {
            hidePrompt(false);
        }
    });
})();
