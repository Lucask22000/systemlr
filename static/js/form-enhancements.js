(function () {
    const FIELD_META = {
        cpf: {
            label: 'CPF',
            hint: 'Formato: 000.000.000-00',
            placeholder: '000.000.000-00'
        },
        cnpj: {
            label: 'CNPJ',
            hint: 'Formato: 00.000.000/0000-00',
            placeholder: '00.000.000/0000-00'
        },
        cpf_cnpj: {
            label: 'Documento',
            hint: 'Informe CPF ou CNPJ valido.',
            placeholder: 'CPF ou CNPJ'
        },
        cep: {
            label: 'CEP',
            hint: 'Formato: 00000-000',
            placeholder: '00000-000'
        },
        phone: {
            label: 'Telefone',
            hint: 'Formato: (00) 00000-0000',
            placeholder: '(00) 00000-0000'
        },
        email: {
            label: 'Email',
            hint: 'Exemplo: nome@empresa.com',
            placeholder: 'nome@empresa.com'
        },
        time: {
            label: 'Horario',
            hint: 'Formato: 08:30',
            placeholder: '08:30'
        },
        uf: {
            label: 'UF',
            hint: 'Use a sigla com 2 letras. Ex.: MT',
            placeholder: 'MT'
        },
        code: {
            label: 'Codigo',
            hint: 'Use letras, numeros e hifen.',
            placeholder: ''
        },
        currency: {
            label: 'Valor',
            hint: 'Use numeros com ate 2 casas decimais.',
            placeholder: '0.00'
        },
        integer: {
            label: 'Numero',
            hint: 'Use apenas numeros inteiros.',
            placeholder: ''
        },
        decimal: {
            label: 'Numero',
            hint: 'Use numeros decimais.',
            placeholder: '0.00'
        }
    };

    function whenReady(callback) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', callback, { once: true });
            return;
        }
        callback();
    }

    function getFieldIdentity(field) {
        return [field.name, field.id, field.getAttribute('autocomplete')]
            .filter(Boolean)
            .join(' ')
            .toLowerCase();
    }

    function hasAnyTerm(value, terms) {
        return terms.some(function (term) {
            return value.indexOf(term) !== -1;
        });
    }

    function isEligibleField(field) {
        if (!(field instanceof HTMLElement)) return false;
        if (field.disabled) return false;
        if (field.tagName !== 'INPUT' && field.tagName !== 'SELECT' && field.tagName !== 'TEXTAREA') return false;

        const type = ((field.getAttribute('type') || '').toLowerCase());
        return !['hidden', 'file', 'submit', 'button', 'reset', 'image', 'checkbox', 'radio'].includes(type);
    }

    function getManagedFields(root) {
        return Array.from(root.querySelectorAll('input, select, textarea')).filter(isEligibleField);
    }

    function detectFieldKind(field) {
        const explicit = (field.dataset.fieldKind || '').trim();
        if (explicit) return explicit;

        const identity = getFieldIdentity(field);
        const type = ((field.getAttribute('type') || '').toLowerCase());

        if (type === 'email' || identity.indexOf('email') !== -1) return 'email';
        if (hasAnyTerm(identity, ['cpf_cnpj', 'cpfcnpj', 'documento'])) return 'cpf_cnpj';
        if (identity.indexOf('cnpj') !== -1) return 'cnpj';
        if (identity.indexOf('cpf') !== -1) return 'cpf';
        if (identity.indexOf('cep') !== -1) return 'cep';
        if (hasAnyTerm(identity, ['telefone', 'celular', 'whatsapp', 'fone'])) return 'phone';
        if (type === 'time' || hasAnyTerm(identity, ['horario', 'hora_inicio', 'hora_fim', 'hora_fechamento'])) return 'time';
        if (hasAnyTerm(identity, [' codigo_empresa', 'codigo_empresa', ' codigo_filial', 'codigo_filial', ' matricula', 'matricula'])) return 'code';
        if (/(^|[\s_-])uf($|[\s_-])/.test(identity) || identity.indexOf('estado_sigla') !== -1) return 'uf';

        if (type === 'number') {
            if (hasAnyTerm(identity, ['preco', 'valor', 'custo', 'saldo', 'desconto', 'total', 'troco', 'dinheiro', 'cartao', 'credito', 'debito', 'frete', 'unitario'])) {
                return 'currency';
            }
            if (hasAnyTerm(identity, ['quantidade', 'qtd', 'estoque', 'minima', 'minimo', 'numero_cadastro', 'cadastro', 'sequencial'])) {
                return 'integer';
            }
            return field.step && field.step !== '1' ? 'decimal' : 'integer';
        }

        return '';
    }

    function applyFieldAttributes(field, kind) {
        const meta = FIELD_META[kind] || {};
        const type = ((field.getAttribute('type') || '').toLowerCase());

        field.dataset.fieldKind = kind;

        if (meta.placeholder && !field.getAttribute('placeholder') && field.tagName === 'INPUT' && type !== 'password') {
            field.setAttribute('placeholder', meta.placeholder);
        }

        if (kind === 'email') {
            if (type === 'text') {
                field.setAttribute('type', 'email');
            }
            field.setAttribute('inputmode', 'email');
            field.setAttribute('autocomplete', field.getAttribute('autocomplete') || 'email');
            field.setAttribute('spellcheck', 'false');
        }

        if (kind === 'cpf') {
            field.setAttribute('inputmode', 'numeric');
            field.setAttribute('maxlength', '14');
        }

        if (kind === 'cnpj') {
            field.setAttribute('inputmode', 'numeric');
            field.setAttribute('maxlength', '18');
        }

        if (kind === 'cpf_cnpj') {
            field.setAttribute('inputmode', 'numeric');
            field.setAttribute('maxlength', '18');
        }

        if (kind === 'cep') {
            field.setAttribute('inputmode', 'numeric');
            field.setAttribute('maxlength', '9');
            field.setAttribute('autocomplete', field.getAttribute('autocomplete') || 'postal-code');
        }

        if (kind === 'phone') {
            field.setAttribute('inputmode', 'tel');
            field.setAttribute('maxlength', '15');
            field.setAttribute('autocomplete', field.getAttribute('autocomplete') || 'tel');
        }

        if (kind === 'time' && type !== 'time') {
            field.setAttribute('inputmode', 'numeric');
            field.setAttribute('maxlength', '5');
            field.setAttribute('pattern', '^\\d{2}:\\d{2}$');
            field.dataset.patternMessage = 'Use o horario no formato HH:MM.';
        }

        if (kind === 'uf') {
            field.setAttribute('maxlength', '2');
            field.setAttribute('autocapitalize', 'characters');
            field.setAttribute('spellcheck', 'false');
        }

        if (kind === 'code') {
            field.setAttribute('autocapitalize', 'characters');
            field.setAttribute('spellcheck', 'false');
            field.setAttribute('autocomplete', field.getAttribute('autocomplete') || 'off');
        }

        if (kind === 'currency' || kind === 'decimal') {
            field.setAttribute('inputmode', 'decimal');
            if (type === 'number' && !field.getAttribute('step')) {
                field.setAttribute('step', '0.01');
            }
        }

        if (kind === 'integer') {
            field.setAttribute('inputmode', 'numeric');
            if (type === 'number' && !field.getAttribute('step')) {
                field.setAttribute('step', '1');
            }
        }
    }

    function digitsOnly(value) {
        return (value || '').replace(/\D/g, '');
    }

    function formatCpf(value) {
        const digits = digitsOnly(value).slice(0, 11);
        return digits
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }

    function formatCnpj(value) {
        const digits = digitsOnly(value).slice(0, 14);
        return digits
            .replace(/^(\d{2})(\d)/, '$1.$2')
            .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
            .replace(/\.(\d{3})(\d)/, '.$1/$2')
            .replace(/(\d{4})(\d)/, '$1-$2');
    }

    function formatCep(value) {
        const digits = digitsOnly(value).slice(0, 8);
        return digits.replace(/(\d{5})(\d)/, '$1-$2');
    }

    function formatPhone(value) {
        const digits = digitsOnly(value).slice(0, 11);
        if (digits.length <= 10) {
            return digits
                .replace(/(\d{2})(\d)/, '($1) $2')
                .replace(/(\d{4})(\d)/, '$1-$2');
        }
        return digits
            .replace(/(\d{2})(\d)/, '($1) $2')
            .replace(/(\d{5})(\d)/, '$1-$2');
    }

    function formatTime(value) {
        const digits = digitsOnly(value).slice(0, 4);
        if (digits.length <= 2) return digits;
        return digits.slice(0, 2) + ':' + digits.slice(2);
    }

    function sanitizeFieldValue(field, mode) {
        const kind = field.dataset.fieldKind || detectFieldKind(field);
        const type = ((field.getAttribute('type') || '').toLowerCase());
        if (!kind) {
            if (mode === 'blur' && field.tagName !== 'SELECT' && type !== 'password') {
                field.value = field.value.trim();
            }
            return;
        }

        if (kind === 'cpf') {
            field.value = formatCpf(field.value);
            return;
        }

        if (kind === 'cnpj') {
            field.value = formatCnpj(field.value);
            return;
        }

        if (kind === 'cpf_cnpj') {
            const digits = digitsOnly(field.value);
            field.value = digits.length > 11 ? formatCnpj(digits) : formatCpf(digits);
            return;
        }

        if (kind === 'cep') {
            field.value = formatCep(field.value);
            return;
        }

        if (kind === 'phone') {
            field.value = formatPhone(field.value);
            return;
        }

        if (kind === 'time' && type !== 'time') {
            field.value = formatTime(field.value);
            return;
        }

        if (kind === 'uf') {
            field.value = field.value.replace(/[^a-z]/gi, '').toUpperCase().slice(0, 2);
            return;
        }

        if (kind === 'code') {
            field.value = field.value.toUpperCase().replace(/[^A-Z0-9-]/g, '');
            return;
        }

        if (kind === 'email' && mode === 'blur') {
            field.value = field.value.trim().toLowerCase();
            return;
        }

        if ((kind === 'currency' || kind === 'decimal') && type === 'number') {
            field.value = (field.value || '').replace(',', '.');
            return;
        }

        if (kind === 'integer' && type === 'number') {
            field.value = (field.value || '').replace(/[^\d-]/g, '');
            return;
        }

        if (mode === 'blur' && field.tagName !== 'SELECT' && type !== 'password') {
            field.value = field.value.trim();
        }
    }

    function isRepeatedDigits(value) {
        return /^(\d)\1+$/.test(value);
    }

    function isValidCpf(value) {
        const digits = digitsOnly(value);
        if (digits.length !== 11 || isRepeatedDigits(digits)) return false;

        let sum = 0;
        for (let index = 0; index < 9; index += 1) {
            sum += parseInt(digits.charAt(index), 10) * (10 - index);
        }
        let remainder = (sum * 10) % 11;
        if (remainder === 10) remainder = 0;
        if (remainder !== parseInt(digits.charAt(9), 10)) return false;

        sum = 0;
        for (let index = 0; index < 10; index += 1) {
            sum += parseInt(digits.charAt(index), 10) * (11 - index);
        }
        remainder = (sum * 10) % 11;
        if (remainder === 10) remainder = 0;
        return remainder === parseInt(digits.charAt(10), 10);
    }

    function isValidCnpj(value) {
        const digits = digitsOnly(value);
        if (digits.length !== 14 || isRepeatedDigits(digits)) return false;

        const calculateCheckDigit = function (baseDigits, factors) {
            const sum = baseDigits.split('').reduce(function (total, digit, index) {
                return total + parseInt(digit, 10) * factors[index];
            }, 0);
            const remainder = sum % 11;
            return remainder < 2 ? 0 : 11 - remainder;
        };

        const base = digits.slice(0, 12);
        const firstDigit = calculateCheckDigit(base, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
        const secondDigit = calculateCheckDigit(base + firstDigit, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);

        return digits === base + String(firstDigit) + String(secondDigit);
    }

    function isValidEmail(value) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test((value || '').trim());
    }

    function isValidTime(value) {
        if (!/^\d{2}:\d{2}$/.test(value || '')) return false;
        const parts = (value || '').split(':');
        const hours = parseInt(parts[0], 10);
        const minutes = parseInt(parts[1], 10);
        return hours >= 0 && hours <= 23 && minutes >= 0 && minutes <= 59;
    }

    function isValidNumber(value) {
        const normalized = String(value || '').replace(',', '.').trim();
        if (!normalized) return false;
        return !Number.isNaN(Number(normalized));
    }

    function isValidInteger(value) {
        return /^-?\d+$/.test(String(value || '').trim());
    }

    function getCustomError(field) {
        const kind = field.dataset.fieldKind || '';
        const value = String(field.value || '').trim();

        if (!value) return '';

        if (kind === 'email' && !isValidEmail(value)) {
            return 'Informe um email valido.';
        }

        if (kind === 'cpf' && !isValidCpf(value)) {
            return 'Informe um CPF valido.';
        }

        if (kind === 'cnpj' && !isValidCnpj(value)) {
            return 'Informe um CNPJ valido.';
        }

        if (kind === 'cpf_cnpj') {
            const digits = digitsOnly(value);
            const valid = digits.length <= 11 ? isValidCpf(digits) : isValidCnpj(digits);
            if (!valid) {
                return 'Informe um CPF ou CNPJ valido.';
            }
        }

        if (kind === 'cep' && digitsOnly(value).length !== 8) {
            return 'Informe um CEP valido com 8 numeros.';
        }

        if (kind === 'phone' && ![10, 11].includes(digitsOnly(value).length)) {
            return 'Informe um telefone com DDD.';
        }

        if (kind === 'time' && !isValidTime(value)) {
            return 'Use o horario no formato HH:MM.';
        }

        if (kind === 'uf' && !/^[A-Z]{2}$/.test(value.toUpperCase())) {
            return 'Use a UF com 2 letras.';
        }

        if (kind === 'code' && !/^[A-Z0-9-]+$/.test(value.toUpperCase())) {
            return 'Use apenas letras, numeros e hifen.';
        }

        if ((kind === 'currency' || kind === 'decimal') && !isValidNumber(value)) {
            return 'Informe um valor numerico valido.';
        }

        if (kind === 'integer' && !isValidInteger(value)) {
            return 'Use somente numeros inteiros.';
        }

        return '';
    }

    function getNativeError(field) {
        if (field.validity.valueMissing) return 'Preencha este campo.';
        if (field.validity.typeMismatch) {
            return (field.dataset.fieldKind || '') === 'email'
                ? 'Informe um email valido.'
                : 'Formato invalido.';
        }
        if (field.validity.patternMismatch) {
            return field.dataset.patternMessage || 'Formato invalido.';
        }
        if (field.validity.stepMismatch) {
            return (field.dataset.fieldKind || '') === 'integer'
                ? 'Use somente numeros inteiros.'
                : 'Ajuste o valor informado.';
        }
        if (field.validity.rangeUnderflow) return 'Informe um valor maior ou igual ao minimo.';
        if (field.validity.rangeOverflow) return 'Informe um valor menor ou igual ao maximo.';
        return '';
    }

    function getFieldFeedback(field) {
        const feedbackId = field.dataset.feedbackId;
        if (feedbackId) {
            const existing = document.getElementById(feedbackId);
            if (existing) return existing;
        }

        const wrapper = field.closest('.auth-field, .form-group, .field-group, .form-field, .filter-field');
        const feedback = document.createElement('div');
        const nextId = field.id || field.name || ('field-' + Math.random().toString(36).slice(2, 8));
        feedback.id = 'feedback-' + nextId.replace(/[^a-zA-Z0-9_-]/g, '-');
        feedback.className = 'field-feedback';
        feedback.hidden = true;
        feedback.setAttribute('aria-live', 'polite');

        if (wrapper) {
            wrapper.appendChild(feedback);
        } else {
            field.insertAdjacentElement('afterend', feedback);
        }

        field.dataset.feedbackId = feedback.id;
        const existingDescription = (field.getAttribute('aria-describedby') || '').trim();
        if (!existingDescription) {
            field.setAttribute('aria-describedby', feedback.id);
        } else if (!existingDescription.split(/\s+/).includes(feedback.id)) {
            field.setAttribute('aria-describedby', existingDescription + ' ' + feedback.id);
        }
        return feedback;
    }

    function updateFeedback(field, state, options) {
        const meta = FIELD_META[field.dataset.fieldKind || ''] || {};
        const hint = meta.hint || '';
        const hasManagedHint = Boolean(hint);
        const shouldShowHint = hasManagedHint && (!state.value || options.forceHint || field === document.activeElement);

        if (!state.error && !shouldShowHint) {
            const feedbackId = field.dataset.feedbackId;
            if (!feedbackId) return;
            const existing = document.getElementById(feedbackId);
            if (existing) {
                existing.hidden = true;
                existing.textContent = '';
                existing.dataset.state = '';
                existing.dataset.kindLabel = '';
            }
            return;
        }

        const feedback = getFieldFeedback(field);
        feedback.hidden = false;
        feedback.dataset.kindLabel = meta.label ? meta.label + ':' : '';

        if (state.error) {
            feedback.dataset.state = 'error';
            feedback.textContent = state.error;
            return;
        }

        feedback.dataset.state = 'hint';
        feedback.textContent = hint;
    }

    function updateFieldState(field, options) {
        const state = options || {};
        const value = String(field.value || '').trim();
        const touched = field.dataset.fieldTouched === '1';
        const dirty = field.dataset.fieldDirty === '1' || value !== '';
        const shouldValidate = Boolean(
            state.forceValidation ||
            touched ||
            (dirty && field !== document.activeElement && value !== '')
        );

        if (!shouldValidate && value === '') {
            field.setCustomValidity('');
            field.classList.remove('field-invalid', 'field-valid');
            field.classList.add('field-empty');
            updateFeedback(field, { error: '', value: value }, state);
            return { valid: true, error: '' };
        }

        const customError = getCustomError(field);
        field.setCustomValidity(customError);

        const nativeError = customError ? '' : getNativeError(field);
        if (nativeError) {
            field.setCustomValidity(nativeError);
        }

        const error = customError || nativeError;
        const valid = !error && field.checkValidity();

        field.classList.toggle('field-invalid', Boolean(error));
        field.classList.toggle('field-valid', valid && value !== '');
        field.classList.toggle('field-empty', value === '');

        updateFeedback(field, { error: error, value: value }, state);
        return { valid: valid, error: error };
    }

    function enhanceField(field) {
        if (!isEligibleField(field) || field.dataset.enhancedField === '1') return;
        field.dataset.enhancedField = '1';

        const kind = detectFieldKind(field);
        if (kind) {
            applyFieldAttributes(field, kind);
        }

        field.addEventListener('input', function () {
            if (String(field.value || '').trim() !== '') {
                field.dataset.fieldDirty = '1';
            }
            sanitizeFieldValue(field, 'input');
            updateFieldState(field, { forceHint: false });
        });

        field.addEventListener('blur', function () {
            field.dataset.fieldTouched = '1';
            if (String(field.value || '').trim() !== '') {
                field.dataset.fieldDirty = '1';
            }
            sanitizeFieldValue(field, 'blur');
            updateFieldState(field, { forceHint: false });
        });

        field.addEventListener('change', function () {
            field.dataset.fieldTouched = '1';
            if (String(field.value || '').trim() !== '') {
                field.dataset.fieldDirty = '1';
            }
            sanitizeFieldValue(field, 'blur');
            updateFieldState(field, { forceHint: false });
        });

        field.addEventListener('focus', function () {
            updateFieldState(field, { forceHint: true });
        });

        sanitizeFieldValue(field, 'input');
        updateFieldState(field, { forceHint: false });
    }

    function validateForm(form) {
        if (!(form instanceof HTMLFormElement)) return true;

        const fields = getManagedFields(form);
        fields.forEach(enhanceField);

        let firstInvalidField = null;
        fields.forEach(function (field) {
            field.dataset.fieldTouched = '1';
            const state = updateFieldState(field, { forceHint: false, forceValidation: true });
            if (!state.valid && !firstInvalidField) {
                firstInvalidField = field;
            }
        });

        if (firstInvalidField) {
            firstInvalidField.focus();
            if (typeof firstInvalidField.reportValidity === 'function') {
                firstInvalidField.reportValidity();
            }
            return false;
        }

        return true;
    }

    function initFormEnhancements() {
        document.querySelectorAll('form').forEach(function (form) {
            getManagedFields(form).forEach(enhanceField);

            if (form.dataset.enhancedValidation === '1') return;
            form.dataset.enhancedValidation = '1';
            form.addEventListener('submit', function (event) {
                if (!validateForm(form)) {
                    event.preventDefault();
                }
            });
        });

        document.addEventListener('focusin', function (event) {
            if (!isEligibleField(event.target)) return;
            enhanceField(event.target);
        });
    }

    window.formEnhancements = {
        init: initFormEnhancements,
        validateForm: validateForm,
        validateField: function (field) {
            enhanceField(field);
            field.dataset.fieldTouched = '1';
            return updateFieldState(field, { forceHint: false, forceValidation: true }).valid;
        }
    };

    whenReady(initFormEnhancements);
}());
