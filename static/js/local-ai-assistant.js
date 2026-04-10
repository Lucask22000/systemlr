document.addEventListener('DOMContentLoaded', function () {
    const shell = document.getElementById('localAssistant');
    if (!shell) {
        return;
    }

    const toggle = document.getElementById('assistantToggle');
    const panel = document.getElementById('assistantPanel');
    const closeButton = document.getElementById('assistantClose');
    const resetButton = document.getElementById('assistantReset');
    const form = document.getElementById('assistantForm');
    const input = document.getElementById('assistantQuestion');
    const messages = document.getElementById('assistantMessages');
    const statusText = document.getElementById('assistantStatusText');
    const suggestions = document.getElementById('assistantSuggestions');
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    const currentEndpoint = document.body.dataset.currentEndpoint || '';
    const currentScreen = document.body.dataset.currentScreen || '';
    const historyKey = 'systemlr.marcia.history';
    const openKey = 'systemlr.marcia.open';

    const initialMessage = {
        role: 'assistant',
        text: 'Sou a Marcia, sua assistente virtual. Posso ajudar com navegacao, proximos passos e duvidas operacionais sem sair da tela atual.',
        status: statusText.textContent || 'Marcia esta offline e pronta para ajudar.',
        actions: [],
        sources: [],
        timestamp: new Date().toISOString(),
    };

    function escapeHtml(value) {
        return String(value || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function escapeRegex(value) {
        return String(value || '').replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function normalizeLookup(value) {
        return String(value || '')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .toLowerCase()
            .replace(/\s+/g, ' ')
            .trim();
    }

    function cleanLinkLabel(value) {
        return String(value || '')
            .replace(/\s+/g, ' ')
            .trim();
    }

    function cleanActionLabel(label, reason) {
        const cleaned = cleanLinkLabel(label);
        if (!cleaned) {
            return '';
        }
        const normalized = normalizeLookup(cleaned);
        if (normalized === 'abrir' || normalized === 'abrir guia' || normalized === 'abrir guia detalhado') {
            return '';
        }
        if (!/^abrir\s+/i.test(cleaned)) {
            return cleaned;
        }
        const stripped = cleanLinkLabel(cleaned.replace(/^abrir\s+/i, ''));
        if (!stripped) {
            return '';
        }
        if (reason && normalizeLookup(stripped) === normalizeLookup(reason)) {
            return cleanLinkLabel(reason);
        }
        return stripped;
    }

    function formatTime(isoValue) {
        const date = isoValue ? new Date(isoValue) : new Date();
        if (Number.isNaN(date.getTime())) {
            return '';
        }
        return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    }

    function updateFab(status) {
        const subtitle = toggle.querySelector('.assistant-fab-subtitle');
        if (!subtitle || !status) {
            return;
        }
        if (status.mode === 'semantic') {
            subtitle.textContent = 'Conversa offline pronta';
        } else if (status.state === 'preparing') {
            subtitle.textContent = 'Aprendendo o sistema';
        } else {
            subtitle.textContent = 'Sua assistente de IA';
        }
    }

    function syncSuggestionsVisibility() {
        const shouldHide = conversationHistory.length > 1;
        suggestions.classList.toggle('is-hidden', shouldHide);
    }

    function focusInputToEnd() {
        if (panel.hidden) {
            return;
        }
        const valueLength = input.value.length;
        input.focus({ preventScroll: true });
        try {
            input.setSelectionRange(valueLength, valueLength);
        } catch (error) {
        }
    }

    function scrollMessagesToBottom() {
        window.requestAnimationFrame(function () {
            messages.scrollTop = messages.scrollHeight;
            window.requestAnimationFrame(function () {
                messages.scrollTop = messages.scrollHeight;
            });
        });
    }

    function loadHistory() {
        try {
            const parsed = JSON.parse(window.sessionStorage.getItem(historyKey) || '[]');
            if (Array.isArray(parsed) && parsed.length) {
                return parsed;
            }
        } catch (error) {
        }
        return [initialMessage];
    }

    function saveHistory(history) {
        window.sessionStorage.setItem(historyKey, JSON.stringify(history.slice(-20)));
    }

    function buildInlineLinkCandidates(message) {
        const candidates = new Map();
        let order = 0;

        function addCandidate(label, url, priority) {
            const cleanedLabel = cleanLinkLabel(label);
            if (!cleanedLabel || !url) {
                return;
            }
            const key = normalizeLookup(cleanedLabel);
            if (!key || key.length < 3) {
                return;
            }
            const current = candidates.get(key);
            if (current) {
                if (priority > current.priority || (priority === current.priority && cleanedLabel.length > current.label.length)) {
                    current.label = cleanedLabel;
                    current.url = url;
                    current.priority = priority;
                }
                return;
            }
            candidates.set(key, {
                key: key,
                label: cleanedLabel,
                url: url,
                priority: priority,
                order: order++,
            });
        }

        (message.actions || []).forEach(function (item) {
            addCandidate(item.reason, item.url, 3);
            addCandidate(cleanActionLabel(item.label, item.reason), item.url, 2);
        });

        (message.sources || []).forEach(function (item) {
            addCandidate(item.title, item.url, 4);
        });

        return Array.from(candidates.values()).sort(function (left, right) {
            return left.order - right.order;
        });
    }

    function linkifyAssistantText(text, candidates) {
        const content = String(text || '');
        if (!candidates.length) {
            return {
                html: escapeHtml(content),
                usedKeys: new Set(),
            };
        }

        const candidatesByKey = new Map(candidates.map(function (item) {
            return [item.key, item];
        }));
        const sortedCandidates = candidates.slice().sort(function (left, right) {
            return right.label.length - left.label.length;
        });
        const pattern = new RegExp(
            `(^|[^A-Za-z0-9])(${sortedCandidates.map(function (item) {
                return escapeRegex(item.label);
            }).join('|')})(?=$|[^A-Za-z0-9])`,
            'gi'
        );

        let html = '';
        let cursor = 0;
        const usedKeys = new Set();
        let match = pattern.exec(content);

        while (match) {
            const prefix = match[1] || '';
            const label = match[2] || '';
            const start = match.index + prefix.length;
            const end = start + label.length;
            const candidate = candidatesByKey.get(normalizeLookup(label));

            html += escapeHtml(content.slice(cursor, start));

            if (candidate) {
                usedKeys.add(candidate.key);
                html += `<a href="${escapeHtml(candidate.url)}" class="assistant-inline-link">${escapeHtml(content.slice(start, end))}</a>`;
            } else {
                html += escapeHtml(content.slice(start, end));
            }

            cursor = end;
            match = pattern.exec(content);
        }

        html += escapeHtml(content.slice(cursor));
        return {
            html: html,
            usedKeys: usedKeys,
        };
    }

    function buildRelatedLinksMarkup(candidates, usedKeys) {
        const remaining = candidates
            .filter(function (item) {
                return !usedKeys.has(item.key);
            })
            .slice(0, 4);

        if (!remaining.length) {
            return '';
        }

        return `
            <div class="assistant-inline-links">
                <span>Links:</span>
                ${remaining.map(function (item) {
                    return `<a href="${escapeHtml(item.url)}" class="assistant-inline-link">${escapeHtml(item.label)}</a>`;
                }).join('')}
            </div>
        `;
    }

    function buildAssistantMessageMarkup(message) {
        const candidates = buildInlineLinkCandidates(message);
        const linkedText = linkifyAssistantText(message.text || '', candidates);
        return `
            <div class="assistant-message-content">
                <div class="assistant-message-text">${linkedText.html}</div>
                ${buildRelatedLinksMarkup(candidates, linkedText.usedKeys)}
            </div>
        `;
    }

    function buildFeedbackMarkup(message) {
        if (message.role !== 'assistant' || !message.responseId || message.typing) {
            return '';
        }

        const likeActive = message.feedbackVote === 'like' ? ' is-selected' : '';
        const dislikeActive = message.feedbackVote === 'dislike' ? ' is-selected' : '';
        const savingText = message.feedbackPending ? '<span class="assistant-feedback-status">Salvando feedback...</span>' : '';
        const savedText = !message.feedbackPending && message.feedbackVote
            ? `<span class="assistant-feedback-status">Feedback: ${escapeHtml(message.feedbackVote === 'like' ? 'curti' : 'nao ajudou')}</span>`
            : '';

        return `
            <div class="assistant-feedback" data-feedback-shell="${escapeHtml(message.responseId)}">
                <span class="assistant-feedback-label">Essa resposta ajudou?</span>
                <div class="assistant-feedback-actions">
                    <button
                        type="button"
                        class="assistant-feedback-btn${likeActive}"
                        data-feedback-vote="like"
                        data-response-id="${escapeHtml(message.responseId)}"
                        aria-pressed="${message.feedbackVote === 'like' ? 'true' : 'false'}"
                        ${message.feedbackPending ? 'disabled' : ''}
                    >
                        Like
                    </button>
                    <button
                        type="button"
                        class="assistant-feedback-btn${dislikeActive}"
                        data-feedback-vote="dislike"
                        data-response-id="${escapeHtml(message.responseId)}"
                        aria-pressed="${message.feedbackVote === 'dislike' ? 'true' : 'false'}"
                        ${message.feedbackPending ? 'disabled' : ''}
                    >
                        Dislike
                    </button>
                </div>
                ${savingText || savedText}
            </div>
        `;
    }

    function renderMessage(message) {
        const wrapper = document.createElement('article');
        const isAssistant = message.role === 'assistant';
        wrapper.className = `assistant-message assistant-message-${isAssistant ? 'assistant' : 'user'}`;
        if (message.responseId) {
            wrapper.dataset.responseId = message.responseId;
        }

        const avatar = `
            <span class="assistant-avatar ${isAssistant ? 'assistant-avatar-marcia' : 'assistant-avatar-user'}">
                ${isAssistant ? 'M' : 'VOCE'}
            </span>
        `;

        const typingMarkup = message.typing ? `
            <div class="assistant-typing" aria-label="Marcia esta digitando">
                <span></span><span></span><span></span>
            </div>
        ` : (isAssistant
            ? buildAssistantMessageMarkup(message)
            : `<p class="assistant-message-text">${escapeHtml(message.text || '')}</p>`);

        const metaStatus = isAssistant && message.status ? `<span>${escapeHtml(message.status)}</span>` : '';
        const feedbackMarkup = isAssistant ? buildFeedbackMarkup(message) : '';

        wrapper.innerHTML = `
            ${isAssistant ? avatar : ''}
            <div class="assistant-bubble">
                <div class="assistant-message-meta">
                    <span>${isAssistant ? 'Marcia' : 'Voce'}</span>
                    <span>${formatTime(message.timestamp)}</span>
                </div>
                ${typingMarkup}
                ${metaStatus}
                ${feedbackMarkup}
            </div>
            ${!isAssistant ? avatar : ''}
        `;
        messages.appendChild(wrapper);
        scrollMessagesToBottom();
        return wrapper;
    }

    function renderHistory(history) {
        messages.replaceChildren();
        history.forEach(renderMessage);
        syncSuggestionsVisibility();
        scrollMessagesToBottom();
    }

    function snapshotHistoryForRequest() {
        return conversationHistory
            .filter(function (item) {
                return !item.typing && item.text && (item.role === 'user' || item.role === 'assistant');
            })
            .slice(-6)
            .map(function (item) {
                return {
                    role: item.role,
                    text: item.text,
                };
            });
    }

    function findMessageIndexByResponseId(responseId) {
        return conversationHistory.findIndex(function (item) {
            return item.responseId === responseId;
        });
    }

    function updateMessageFeedbackState(responseId, updates) {
        const index = findMessageIndexByResponseId(responseId);
        if (index < 0) {
            return;
        }
        conversationHistory[index] = Object.assign({}, conversationHistory[index], updates);
        saveHistory(conversationHistory);
        renderHistory(conversationHistory);
    }

    let conversationHistory = loadHistory();
    renderHistory(conversationHistory);
    syncSuggestionsVisibility();

    function setPanelOpen(open) {
        panel.hidden = !open;
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        window.sessionStorage.setItem(openKey, open ? '1' : '0');
        if (open) {
            scrollMessagesToBottom();
            focusInputToEnd();
        }
    }

    function syncInitialState() {
        const stored = window.sessionStorage.getItem(openKey);
        setPanelOpen(stored === '1');
    }

    function appendUserMessage(text) {
        const message = {
            role: 'user',
            text: text,
            timestamp: new Date().toISOString(),
        };
        conversationHistory.push(message);
        saveHistory(conversationHistory);
        renderMessage(message);
        syncSuggestionsVisibility();
        focusInputToEnd();
    }

    function appendTypingMessage() {
        const typingMessage = {
            role: 'assistant',
            typing: true,
            text: '',
            timestamp: new Date().toISOString(),
        };
        const element = renderMessage(typingMessage);
        return { element };
    }

    function appendFeedbackToBubble(bubble, message) {
        if (!message.responseId) {
            return;
        }
        bubble.insertAdjacentHTML('beforeend', buildFeedbackMarkup(message));
    }

    async function animateAssistantMessage(element, message, statusPayload) {
        const bubble = element.querySelector('.assistant-bubble');
        const body = bubble.querySelector('.assistant-typing');
        const content = document.createElement('div');
        content.className = 'assistant-message-content';
        const meta = document.createElement('div');
        meta.className = 'assistant-message-text';
        content.appendChild(meta);
        body.replaceWith(content);

        const finalText = message.text || 'Nao consegui montar uma orientacao para esta pergunta.';
        for (let index = 1; index <= finalText.length; index += 3) {
            meta.textContent = finalText.slice(0, index);
            scrollMessagesToBottom();
            await new Promise(function (resolve) { window.setTimeout(resolve, 12); });
        }

        const finalMarkup = buildAssistantMessageMarkup(message);
        content.outerHTML = finalMarkup;

        if (statusPayload && statusPayload.message) {
            const status = document.createElement('span');
            status.textContent = statusPayload.message;
            bubble.appendChild(status);
            statusText.textContent = statusPayload.message;
            updateFab(statusPayload);
        }

        appendFeedbackToBubble(bubble, message);
        scrollMessagesToBottom();
        focusInputToEnd();
    }

    async function loadStatus() {
        try {
            const response = await fetch('/api/assistente-local/status', {
                headers: { Accept: 'application/json' },
                credentials: 'same-origin',
            });
            const payload = await response.json();
            if (payload.success && payload.data) {
                statusText.textContent = payload.data.message || 'Marcia esta offline e pronta para ajudar.';
                shell.dataset.assistantState = payload.data.state || 'idle';
                shell.dataset.assistantMode = payload.data.mode || 'lexical';
                updateFab(payload.data);
                focusInputToEnd();
            }
        } catch (error) {
            statusText.textContent = 'Nao foi possivel consultar o status da Marcia.';
        }
    }

    async function submitFeedback(responseId, vote) {
        const index = findMessageIndexByResponseId(responseId);
        if (index < 0) {
            return;
        }

        const message = conversationHistory[index];
        if (message.feedbackPending || !message.responseId) {
            return;
        }

        updateMessageFeedbackState(responseId, { feedbackPending: true });

        try {
            const response = await fetch('/api/assistente-local/feedback', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken,
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    response_id: message.responseId,
                    vote: vote,
                    question_text: message.questionText || '',
                    answer_text: message.text || '',
                    endpoint_atual: currentEndpoint,
                    tela_atual: currentScreen,
                    matched_doc_ids: message.matchedDocIds || [],
                }),
            });
            const payload = await response.json();
            if (!payload.success) {
                throw new Error(payload.message || 'Nao foi possivel salvar o feedback.');
            }

            updateMessageFeedbackState(responseId, {
                feedbackPending: false,
                feedbackVote: vote,
            });
        } catch (error) {
            updateMessageFeedbackState(responseId, {
                feedbackPending: false,
            });
        }
    }

    async function ask(question) {
        const pergunta = (question || '').trim();
        if (!pergunta) {
            focusInputToEnd();
            return;
        }

        const historySnapshot = snapshotHistoryForRequest();
        appendUserMessage(pergunta);
        input.value = '';
        const pending = appendTypingMessage();
        focusInputToEnd();

        try {
            const response = await fetch('/api/assistente-local/perguntar', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken,
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    pergunta: pergunta,
                    endpoint_atual: currentEndpoint,
                    tela_atual: currentScreen,
                    historico: historySnapshot,
                }),
            });
            const payload = await response.json();
            if (!payload.success) {
                throw new Error(payload.message || 'Falha ao consultar a Marcia.');
            }

            const answerPayload = payload.data || {};
            const assistantMessage = {
                role: 'assistant',
                text: answerPayload.answer || '',
                status: answerPayload.status ? answerPayload.status.message : '',
                actions: answerPayload.actions || [],
                sources: answerPayload.sources || [],
                timestamp: new Date().toISOString(),
                responseId: answerPayload.response_id || '',
                matchedDocIds: answerPayload.matched_doc_ids || [],
                questionText: pergunta,
                feedbackVote: '',
                feedbackPending: false,
            };

            await animateAssistantMessage(pending.element, assistantMessage, answerPayload.status);
            conversationHistory.push(assistantMessage);
            saveHistory(conversationHistory);
            syncSuggestionsVisibility();
            focusInputToEnd();
        } catch (error) {
            pending.element.remove();
            const fallback = {
                role: 'assistant',
                text: error.message || 'Nao foi possivel responder agora.',
                status: 'Tente novamente em instantes.',
                actions: [],
                sources: [],
                timestamp: new Date().toISOString(),
            };
            conversationHistory.push(fallback);
            saveHistory(conversationHistory);
            renderMessage(fallback);
            syncSuggestionsVisibility();
            focusInputToEnd();
        }
    }

    function resetConversation() {
        conversationHistory = [initialMessage];
        saveHistory(conversationHistory);
        renderHistory(conversationHistory);
        focusInputToEnd();
    }

    toggle.addEventListener('click', function () {
        setPanelOpen(panel.hidden);
    });

    closeButton.addEventListener('click', function () {
        setPanelOpen(false);
    });

    resetButton.addEventListener('click', function () {
        resetConversation();
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        ask(input.value);
    });

    input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            ask(input.value);
        }
    });

    messages.addEventListener('click', function (event) {
        const button = event.target.closest('[data-feedback-vote]');
        if (!button) {
            return;
        }
        submitFeedback(
            button.getAttribute('data-response-id') || '',
            button.getAttribute('data-feedback-vote') || ''
        );
    });

    suggestions.querySelectorAll('[data-assistant-question]').forEach(function (button) {
        button.addEventListener('click', function () {
            const pergunta = button.getAttribute('data-assistant-question') || '';
            input.value = pergunta;
            ask(pergunta);
        });
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !panel.hidden) {
            setPanelOpen(false);
        }
    });

    syncInitialState();
    loadStatus();
    window.setInterval(loadStatus, 20000);
    focusInputToEnd();
});
