document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menuToggle');
    const navbarMenu = document.getElementById('navbarMenu');
    const dropdownToggles = document.querySelectorAll('.nav-dropdown-toggle');
    const mobileBreakpoint = window.matchMedia('(max-width: 768px)');

    if (menuToggle && navbarMenu) {
        const closeDropdowns = function () {
            document.querySelectorAll('.nav-dropdown.open').forEach(function (drop) {
                drop.classList.remove('open');
            });
        };

        const setMenuState = function (isOpen) {
            navbarMenu.classList.toggle('active', isOpen);
            menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            menuToggle.setAttribute('aria-label', isOpen ? 'Fechar menu' : 'Abrir menu');
        };

        menuToggle.addEventListener('click', function () {
            const isOpen = !navbarMenu.classList.contains('active');
            setMenuState(isOpen);
        });

        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                setMenuState(false);
                closeDropdowns();
            });
        });

        document.addEventListener('keydown', function (event) {
            if (event.key !== 'Escape') return;
            setMenuState(false);
            closeDropdowns();
        });

        document.addEventListener('click', function (event) {
            if (!mobileBreakpoint.matches) return;
            const clickedInsideMenu = navbarMenu.contains(event.target);
            const clickedToggle = menuToggle.contains(event.target);
            if (!clickedInsideMenu && !clickedToggle) {
                setMenuState(false);
                closeDropdowns();
            }
        });

        const handleBreakpoint = function (event) {
            if (event.matches) return;
            setMenuState(false);
            closeDropdowns();
        };

        if (typeof mobileBreakpoint.addEventListener === 'function') {
            mobileBreakpoint.addEventListener('change', handleBreakpoint);
        } else {
            mobileBreakpoint.addListener(handleBreakpoint);
        }
    }

    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function () {
            const parentDropdown = this.closest('.nav-dropdown');
            document.querySelectorAll('.nav-dropdown.open').forEach(function (drop) {
                if (drop !== parentDropdown) {
                    drop.classList.remove('open');
                }
            });
            parentDropdown.classList.toggle('open');
        });
    });

    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            this.parentElement.style.display = 'none';
        });
    });

    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.display = 'none';
        }, 5000);
    });

    initConfirmActionModal();
    initBarcodeScannerButtons();
    initFormFieldTooltips();
    initCollapsiblePanels();
});

function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

function formatarData(data) {
    return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(data));
}

function validarFormulario(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let valido = true;

    inputs.forEach(function (input) {
        if (!input.value.trim()) {
            input.style.borderColor = '#D9534F';
            valido = false;
        } else {
            input.style.borderColor = '';
        }
    });

    return valido;
}

function initConfirmActionModal() {
    const modalEl = document.getElementById('confirmActionModal');
    const messageEl = document.getElementById('confirmActionModalMessage');
    const okBtn = document.getElementById('confirmActionModalOk');
    if (!modalEl || !messageEl || !okBtn || typeof bootstrap === 'undefined') return;

    const modal = new bootstrap.Modal(modalEl, { backdrop: 'static', keyboard: true });
    let pendingForm = null;

    document.addEventListener('submit', function (event) {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        const confirmMessage = form.getAttribute('data-confirm-message');
        if (!confirmMessage) return;
        if (form.dataset.confirmedSubmit === '1') {
            delete form.dataset.confirmedSubmit;
            return;
        }
        event.preventDefault();
        pendingForm = form;
        messageEl.textContent = confirmMessage;
        modal.show();
    });

    okBtn.addEventListener('click', function () {
        if (!pendingForm) {
            modal.hide();
            return;
        }
        pendingForm.dataset.confirmedSubmit = '1';
        const form = pendingForm;
        pendingForm = null;
        modal.hide();
        if (typeof form.requestSubmit === 'function') {
            form.requestSubmit();
        } else {
            form.submit();
        }
    });

    modalEl.addEventListener('hidden.bs.modal', function () {
        pendingForm = null;
    });
}

function initBarcodeScannerButtons() {
    const buttons = document.querySelectorAll('.js-open-barcode-scanner');
    if (!buttons.length) return;

    let modalState = null;

    buttons.forEach(function (button) {
        button.addEventListener('click', async function () {
            const targetId = this.getAttribute('data-barcode-target');
            const targetInput = document.getElementById(targetId);
            const mode = (this.getAttribute('data-barcode-mode') || 'single').toLowerCase();
            const continuous = mode === 'continuous' || mode === 'sequence';

            if (!targetInput) {
                alert('Campo de codigo nao encontrado.');
                return;
            }

            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                alert('Seu navegador nao suporta acesso a camera.');
                return;
            }

            if (typeof window.BarcodeDetector === 'undefined') {
                alert('Leitura por camera indisponivel neste navegador. Use Chrome/Edge atualizados.');
                return;
            }

            try {
                if (modalState && typeof modalState.close === 'function') {
                    modalState.close();
                }

                const detector = new window.BarcodeDetector({
                    formats: ['ean_13', 'ean_8', 'code_128', 'upc_a', 'upc_e', 'code_39', 'codabar']
                });
                modalState = await openBarcodeScannerModal(targetInput, detector, {
                    continuous: continuous
                });
            } catch (error) {
                console.error('Erro ao iniciar leitura de codigo:', error);
                alert('Nao foi possivel iniciar a leitura. Verifique permissoes da camera.');
            }
        });
    });

    window.addEventListener('beforeunload', function () {
        if (modalState && typeof modalState.close === 'function') {
            modalState.close();
        }
    });
}

function initFormFieldTooltips() {
    if (typeof bootstrap === 'undefined' || typeof bootstrap.Tooltip === 'undefined') return;

    const controls = document.querySelectorAll('form input, form select, form textarea');
    controls.forEach(function (field) {
        if (!field || field.dataset.tooltipReady === '1') return;
        if (field.type === 'hidden') return;
        if (field.disabled) return;

        const explicit = (field.getAttribute('data-tooltip') || '').trim();
        const label = getFieldLabelText(field);
        const placeholder = (field.getAttribute('placeholder') || '').trim();
        const requiredText = field.required ? 'Campo obrigatorio.' : '';

        let tooltipText = explicit;
        if (!tooltipText) {
            const parts = [];
            if (label) parts.push(label + '.');
            if (placeholder) parts.push('Exemplo: ' + placeholder + '.');
            if (requiredText) parts.push(requiredText);
            tooltipText = parts.join(' ').trim();
        }

        if (!tooltipText) return;

        field.setAttribute('data-bs-toggle', 'tooltip');
        field.setAttribute('data-bs-placement', 'top');
        field.setAttribute('data-bs-trigger', 'hover focus');
        field.setAttribute('title', tooltipText);
        field.dataset.tooltipReady = '1';
        bootstrap.Tooltip.getOrCreateInstance(field);
    });
}

function getFieldLabelText(field) {
    if (!field || !field.id) return '';
    const label = document.querySelector('label[for="' + field.id + '"]');
    if (!label) return '';
    return (label.textContent || '').replace(/\s+/g, ' ').replace(/\*/g, '').trim();
}

async function openBarcodeScannerModal(targetInput, detector, options) {
    options = options || {};
    const continuous = Boolean(options.continuous);
    const scanIntervalMs = continuous ? 120 : 250;
    const duplicateCooldownMs = continuous ? 350 : 0;
    const lastReadByCode = {};

    const modal = document.createElement('div');
    modal.className = 'barcode-scanner-modal active';
    modal.innerHTML = [
        '<div class="barcode-scanner-content">',
        '  <div class="barcode-scanner-header">',
        '    <span class="barcode-scanner-title">Leitura de Codigo de Barras</span>',
        '    <button type="button" class="barcode-scanner-close" aria-label="Fechar">&times;</button>',
        '  </div>',
        '  <div class="barcode-scanner-body">',
        '    <video class="barcode-scanner-video" autoplay playsinline muted></video>',
        continuous
            ? '    <p class="barcode-scanner-help">Modo continuo ativo: aproxime e afaste os produtos para leitura em sequencia.</p>'
            : '    <p class="barcode-scanner-help">Aponte a camera para o codigo de barras.</p>',
        '  </div>',
        '</div>'
    ].join('');

    document.body.appendChild(modal);

    const video = modal.querySelector('.barcode-scanner-video');
    const closeBtn = modal.querySelector('.barcode-scanner-close');
    let running = true;
    let stream = null;

    const close = function () {
        running = false;
        if (stream) {
            stream.getTracks().forEach(function (track) {
                track.stop();
            });
        }
        modal.remove();
    };

    closeBtn.addEventListener('click', close);
    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            close();
        }
    });

    stream = await navigator.mediaDevices.getUserMedia({
        video: {
            facingMode: { ideal: 'environment' },
            width: { ideal: 1280 },
            height: { ideal: 720 }
        },
        audio: false
    });

    video.srcObject = stream;

    const scanLoop = async function () {
        if (!running) return;

        try {
            const barcodes = await detector.detect(video);
            if (barcodes && barcodes.length > 0) {
                let rawValue = '';
                for (let i = 0; i < barcodes.length; i++) {
                    const candidate = (barcodes[i].rawValue || '').trim();
                    if (candidate) {
                        rawValue = candidate;
                        break;
                    }
                }

                if (rawValue) {
                    const now = Date.now();
                    const lastReadAt = lastReadByCode[rawValue] || 0;
                    if (duplicateCooldownMs > 0 && (now - lastReadAt) < duplicateCooldownMs) {
                        setTimeout(scanLoop, scanIntervalMs);
                        return;
                    }
                    lastReadByCode[rawValue] = now;

                    targetInput.value = rawValue;
                    targetInput.dispatchEvent(new Event('input', { bubbles: true }));
                    targetInput.dispatchEvent(new Event('change', { bubbles: true }));
                    targetInput.dispatchEvent(new CustomEvent('barcode:detected', {
                        bubbles: true,
                        detail: { value: rawValue, continuous: continuous }
                    }));

                    if (continuous && navigator.vibrate) {
                        navigator.vibrate(30);
                    }

                    if (!continuous) {
                        close();
                        return;
                    }
                }
            }
        } catch (error) {
            // Ignora falhas pontuais de detecção por frame.
        }

        setTimeout(scanLoop, scanIntervalMs);
    };

    scanLoop();

    return { close: close };
}

function initCollapsiblePanels() {
    const panels = [];

    document.querySelectorAll('.pdv-panel').forEach(function (panel) {
        const header = panel.querySelector(':scope > .pdv-panel-head') || panel.querySelector('.pdv-panel-head');
        const body = panel.querySelector(':scope > .pdv-panel-body') || panel.querySelector('.pdv-panel-body');
        if (!header || !body) return;
        panels.push({ panel: panel, header: header, contentNodes: [body], idHint: 'pdv-' + header.textContent.trim() });
    });

    document.querySelectorAll('.card').forEach(function (panel) {
        const header = panel.querySelector(':scope > .card-header') || panel.querySelector('.card-header');
        if (!header) return;
        const body = panel.querySelector(':scope > .card-body') || panel.querySelector('.card-body');
        const contentNodes = body ? [body] : Array.from(panel.children).filter(function (child) { return child !== header; });
        if (!contentNodes.length) return;
        panels.push({ panel: panel, header: header, contentNodes: contentNodes, idHint: 'card-' + header.textContent.trim() });
    });

    document.querySelectorAll('.section').forEach(function (panel) {
        if (panel.closest('.card')) return;
        const title = panel.querySelector(':scope > h1, :scope > h2, :scope > h3, :scope > h4');
        if (!title) return;
        const contentNodes = Array.from(panel.children).filter(function (child) { return child !== title; });
        if (!contentNodes.length) return;

        let headerWrap = panel.querySelector(':scope > .panel-toggle-head');
        if (!headerWrap) {
            headerWrap = document.createElement('div');
            headerWrap.className = 'panel-toggle-head';
            panel.insertBefore(headerWrap, title);
            headerWrap.appendChild(title);
        }

        panels.push({ panel: panel, header: headerWrap, contentNodes: contentNodes, idHint: 'section-' + title.textContent.trim() });
    });

    const seen = new WeakSet();
    panels.forEach(function (item, index) {
        if (!item.panel || !item.header || seen.has(item.panel)) return;
        seen.add(item.panel);

        item.panel.classList.add('panel-collapsible');
        item.contentNodes.forEach(function (node) {
            if (node && node.classList) node.classList.add('panel-collapsible-content');
        });

        let btn = item.header.querySelector('.panel-toggle-btn');
        if (!btn) {
            btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-sm btn-outline-secondary panel-toggle-btn';
            item.header.appendChild(btn);
        }

        const storageKey = 'panel-collapse:' + window.location.pathname + ':' + slugifyPanelId(item.idHint || String(index));
        const stored = window.localStorage ? localStorage.getItem(storageKey) : null;
        let collapsed = stored === '1';

        const applyState = function () {
            item.panel.classList.toggle('panel-collapsed', collapsed);
            btn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
            btn.textContent = collapsed ? 'Expandir' : 'Minimizar';
        };

        btn.addEventListener('click', function () {
            collapsed = !collapsed;
            if (window.localStorage) {
                localStorage.setItem(storageKey, collapsed ? '1' : '0');
            }
            applyState();
        });

        applyState();
    });
}

function slugifyPanelId(value) {
    return (value || 'panel')
        .toString()
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '')
        .slice(0, 80) || 'panel';
}
