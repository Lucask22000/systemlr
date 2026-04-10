(function () {
    function safeStorage() {
        try {
            return window.sessionStorage || null;
        } catch (error) {
            return null;
        }
    }

    function cloneJson(value) {
        return JSON.parse(JSON.stringify(value || {}));
    }

    function saveDraft(key, payload) {
        const storage = safeStorage();
        if (!storage || !key) return;
        storage.setItem(key, JSON.stringify(payload || {}));
    }

    function loadDraft(key) {
        const storage = safeStorage();
        if (!storage || !key) return null;
        const raw = storage.getItem(key);
        if (!raw) return null;
        try {
            return JSON.parse(raw);
        } catch (error) {
            storage.removeItem(key);
            return null;
        }
    }

    function clearDraft(key) {
        const storage = safeStorage();
        if (!storage || !key) return;
        storage.removeItem(key);
    }

    window.operationalFlow = {
        clearDraft: clearDraft,
        cloneJson: cloneJson,
        loadDraft: loadDraft,
        saveDraft: saveDraft
    };
}());
