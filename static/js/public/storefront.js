(function () {
    function initLoadingProgress() {
        const overlay = document.querySelector('[data-store-loading-overlay]');
        if (!overlay) {
            return;
        }

        const bar = overlay.querySelector('[data-store-loading-bar]');
        const percentNode = overlay.querySelector('[data-store-loading-percent]');
        const statusNode = overlay.querySelector('[data-store-loading-status]');
        const resources = [];
        const seen = new Set();

        document.querySelectorAll('img').forEach(function (img) {
            if (!img || !img.currentSrc && !img.src) return;
            const key = img.currentSrc || img.src;
            if (seen.has(key)) return;
            seen.add(key);
            resources.push(img);
        });

        const fontPromise = (document.fonts && typeof document.fonts.ready === 'object')
            ? document.fonts.ready
            : Promise.resolve();

        const total = Math.max(resources.length + 2, 3);
        let completed = 0;
        let currentPercent = 0;

        function updateStatus(message) {
            if (statusNode) {
                statusNode.textContent = message;
            }
        }

        function renderProgress(forcePercent) {
            const calculated = typeof forcePercent === 'number'
                ? forcePercent
                : Math.min(96, Math.round((completed / total) * 100));
            currentPercent = Math.max(currentPercent, calculated);
            if (bar) {
                bar.style.width = currentPercent + '%';
            }
            if (percentNode) {
                percentNode.textContent = currentPercent + '%';
            }
        }

        function step(message, forcePercent) {
            completed += 1;
            if (message) {
                updateStatus(message);
            }
            renderProgress(forcePercent);
        }

        function finish() {
            updateStatus('Loja pronta.');
            renderProgress(100);
            window.setTimeout(function () {
                overlay.classList.add('is-hidden');
            }, 180);
        }

        updateStatus('Mapeando recursos da vitrine...');
        renderProgress(8);

        let loadedImages = 0;
        if (!resources.length) {
            step('Sem imagens pendentes, liberando vitrine...', 42);
        } else {
            resources.forEach(function (img) {
                const onDone = function () {
                    loadedImages += 1;
                    const percentualImagens = Math.min(82, 12 + Math.round((loadedImages / resources.length) * 58));
                    updateStatus('Carregando imagens da vitrine (' + loadedImages + '/' + resources.length + ')...');
                    renderProgress(percentualImagens);
                };

                if (img.complete) {
                    onDone();
                    return;
                }

                img.addEventListener('load', onDone, { once: true });
                img.addEventListener('error', onDone, { once: true });
            });
        }

        Promise.resolve(fontPromise).then(function () {
            step('Tipografia carregada.', 88);
        }).catch(function () {
            step('Tipografia liberada.', 88);
        });

        window.addEventListener('load', function () {
            step('Conexão principal estabilizada.', 96);
            finish();
        }, { once: true });

        window.setTimeout(function () {
            if (!overlay.classList.contains('is-hidden')) {
                finish();
            }
        }, 5000);
    }

    function normalizarTexto(texto) {
        return (texto || '')
            .toString()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .toLowerCase()
            .trim();
    }

    function initCarousel() {
        const carousel = document.querySelector('[data-store-carousel]');
        if (!carousel) {
            return;
        }

        const slides = Array.from(carousel.querySelectorAll('[data-store-slide]'));
        const dots = Array.from(carousel.querySelectorAll('[data-store-dot]'));
        if (slides.length <= 1) {
            return;
        }

        let current = 0;

        function render(index) {
            current = index;
            slides.forEach(function (slide, position) {
                slide.classList.toggle('is-active', position === current);
            });
            dots.forEach(function (dot, position) {
                dot.classList.toggle('is-active', position === current);
            });
        }

        dots.forEach(function (dot, index) {
            dot.addEventListener('click', function () {
                render(index);
            });
        });

        window.setInterval(function () {
            render((current + 1) % slides.length);
        }, 5000);
    }

    function initPaymentToggle() {
        const radios = Array.from(document.querySelectorAll('input[name="metodo_pagamento"]'));
        const valorWrap = document.querySelector('[data-valor-recebido-wrap]');
        if (!radios.length || !valorWrap) {
            return;
        }

        function sync() {
            const selected = document.querySelector('input[name="metodo_pagamento"]:checked');
            valorWrap.classList.toggle('store-hide', !(selected && selected.value === 'dinheiro'));
        }

        radios.forEach(function (radio) {
            radio.addEventListener('change', sync);
        });
        sync();
    }

    function initProductSearch() {
        const searchRoot = document.querySelector('[data-store-product-search]');
        if (!searchRoot) {
            return;
        }

        const input = searchRoot.querySelector('[data-store-search-input]');
        const clearButton = searchRoot.querySelector('[data-store-search-clear]');
        const feedback = searchRoot.querySelector('[data-store-search-feedback]');
        const cards = Array.from(document.querySelectorAll('[data-product-card]'));
        if (!input || !cards.length) {
            return;
        }

        function applyFilter() {
            const term = normalizarTexto(input.value);
            let visible = 0;

            cards.forEach(function (card) {
                const haystack = normalizarTexto(card.getAttribute('data-product-search'));
                const match = !term || haystack.indexOf(term) >= 0;
                card.classList.toggle('is-hidden', !match);
                if (match) {
                    visible += 1;
                }
            });

            if (clearButton) {
                clearButton.hidden = !term;
            }
            if (feedback) {
                feedback.textContent = term
                    ? 'Exibindo ' + visible + ' produto(s) para "' + input.value.trim() + '".'
                    : 'Exibindo ' + visible + ' produto(s) em destaque.';
            }
        }

        input.addEventListener('input', applyFilter);

        if (clearButton) {
            clearButton.addEventListener('click', function () {
                input.value = '';
                applyFilter();
                input.focus();
            });
        }

        applyFilter();
    }

    document.addEventListener('DOMContentLoaded', function () {
        initLoadingProgress();
        initCarousel();
        initPaymentToggle();
        initProductSearch();
    });
})();
