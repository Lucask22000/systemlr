(function () {
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
        initCarousel();
        initPaymentToggle();
        initProductSearch();
    });
})();
