(function () {
    function moeda(v) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0);
    }

    function pct(v) {
        return (Number(v || 0)).toFixed(1) + '%';
    }

    function todayIso(offsetDays) {
        var d = new Date();
        d.setDate(d.getDate() + (offsetDays || 0));
        return d.toISOString().slice(0, 10);
    }

    function applyPreset() {
        var preset = document.getElementById('periodoPreset');
        var ini = document.getElementById('data_inicial');
        var fim = document.getElementById('data_final');
        if (!preset || !ini || !fim) return;
        if (preset.value === 'hoje') {
            ini.value = todayIso(0);
            fim.value = todayIso(0);
        } else if (preset.value === 'ontem') {
            ini.value = todayIso(-1);
            fim.value = todayIso(-1);
        } else if (preset.value === 'semana') {
            ini.value = todayIso(-6);
            fim.value = todayIso(0);
        } else if (preset.value === 'mes') {
            ini.value = todayIso(-29);
            fim.value = todayIso(0);
        }
    }

    function buildUrl() {
        var ini = document.getElementById('data_inicial');
        var fim = document.getElementById('data_final');
        var params = new URLSearchParams();
        if (ini && ini.value) params.set('data_inicial', ini.value);
        if (fim && fim.value) params.set('data_final', fim.value);
        return '/api/dashboard/analytics?' + params.toString();
    }

    function tbodyRows(id, rows, emptyText) {
        var el = document.getElementById(id);
        if (!el) return;
        if (!rows.length) {
            el.innerHTML = '<tr><td colspan="5" class="text-center">' + emptyText + '</td></tr>';
            return;
        }
        el.innerHTML = rows.join('');
    }

    var charts = {};
    function destroyCharts() {
        Object.keys(charts).forEach(function (key) {
            if (charts[key]) charts[key].destroy();
        });
        charts = {};
    }

    function renderAlerts(alertas) {
        var wrap = document.getElementById('financeiroAlertas');
        if (!wrap) return;
        if (!(alertas || []).length) {
            wrap.innerHTML = '<p class="text-muted mb-0">Nenhum alerta critico para o periodo.</p>';
            return;
        }
        wrap.innerHTML = alertas.map(function (item) {
            var cls = item.nivel === 'danger' ? 'danger' : (item.nivel === 'warning' ? 'warning' : 'info');
            return '<div class="alert alert-' + cls + ' mb-0"><strong>' + item.titulo + ':</strong> ' + item.descricao + '</div>';
        }).join('');
    }

    function renderKpis(data) {
        var comp = data.comparativos || {};
        document.getElementById('kpiFaturamento').textContent = moeda(data.faturamento_periodo);
        document.getElementById('metaFaturamento').textContent = pct((comp.faturamento || {}).variacao_pct);
        document.getElementById('kpiTicket').textContent = moeda(data.ticket_medio_periodo);
        document.getElementById('metaTicket').textContent = pct((comp.ticket_medio || {}).variacao_pct);
        document.getElementById('kpiMargemBruta').textContent = pct(data.margem_bruta_pct);
        document.getElementById('metaMargemBruta').textContent = 'Lucro bruto ' + moeda(data.lucro_bruto_periodo);
        document.getElementById('kpiMargemOperacional').textContent = pct(data.margem_operacional_pct);
        document.getElementById('metaMargemOperacional').textContent = 'Resultado ' + moeda(data.resultado_operacional_periodo);
        document.getElementById('kpiDespesas').textContent = moeda(data.despesas_operacionais_periodo);
        document.getElementById('metaDespesas').textContent = pct(data.despesas_operacionais_pct_faturamento) + ' do faturamento';
        document.getElementById('kpiCancelamento').textContent = pct(data.taxa_cancelamento_pct);
        document.getElementById('metaCancelamento').textContent = String(data.pedidos_cancelados_periodo || 0) + ' pedidos cancelados';
    }

    function renderTables(data) {
        tbodyRows('tableTopProdutos', (data.top_produtos_vendidos || []).map(function (item) {
            return '<tr><td>' + (item.sku || '-') + '</td><td>' + item.nome + '</td><td>' + item.quantidade + '</td><td>' + moeda(item.receita) + '</td><td>' + pct((item.margem_contribuicao || 0) * 100) + '</td></tr>';
        }), 'Sem dados de produtos.');
        tbodyRows('tableTopClientes', (data.top_clientes || []).map(function (item) {
            return '<tr><td>' + item.cliente_nome + '</td><td>' + item.pedidos + '</td><td>' + moeda(item.faturamento) + '</td></tr>';
        }), 'Sem dados de clientes.');
        tbodyRows('tableDesempenho', (data.desempenho_operacional || []).map(function (item) {
            return '<tr><td>' + item.tipo + '</td><td>' + item.nome + '</td><td>' + item.pedidos + '</td><td>' + moeda(item.faturamento) + '</td><td>' + moeda(item.ticket_medio) + '</td></tr>';
        }), 'Sem dados operacionais.');
    }

    function renderCharts(data) {
        destroyCharts();
        charts.receitaDespesas = new Chart(document.getElementById('chartReceitaDespesas'), {
            type: 'line',
            data: {
                labels: (data.receita_vs_despesas || []).map(function (x) { return x.data_curta; }),
                datasets: [
                    { label: 'Receita', data: (data.receita_vs_despesas || []).map(function (x) { return x.faturamento; }), borderColor: '#0f766e', backgroundColor: 'rgba(15,118,110,.12)', fill: true, tension: .25 },
                    { label: 'Despesas', data: (data.receita_vs_despesas || []).map(function (x) { return x.despesas; }), borderColor: '#dc2626', backgroundColor: 'rgba(220,38,38,.08)', fill: true, tension: .25 }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
        charts.margens = new Chart(document.getElementById('chartMargens'), {
            type: 'line',
            data: {
                labels: (data.margens_periodo || []).map(function (x) { return x.data_curta; }),
                datasets: [
                    { label: 'Margem bruta %', data: (data.margens_periodo || []).map(function (x) { return x.margem_bruta_pct; }), borderColor: '#2563eb', backgroundColor: 'rgba(37,99,235,.14)', fill: true, tension: .25 },
                    { label: 'Margem operacional %', data: (data.margens_periodo || []).map(function (x) { return x.margem_operacional_pct; }), borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,.12)', fill: true, tension: .25 }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
        charts.categorias = new Chart(document.getElementById('chartCmvCategorias'), {
            type: 'bar',
            data: {
                labels: (data.cmv_vs_categorias || []).map(function (x) { return x.categoria; }),
                datasets: [{ label: 'Valor (R$)', data: (data.cmv_vs_categorias || []).map(function (x) { return x.valor; }), backgroundColor: '#155e75' }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
        charts.pagamento = new Chart(document.getElementById('chartPagamento'), {
            type: 'doughnut',
            data: {
                labels: (data.metodos_pagamento || []).map(function (x) { return x.metodo; }),
                datasets: [{ data: (data.metodos_pagamento || []).map(function (x) { return x.quantidade; }), backgroundColor: ['#0f766e', '#2563eb', '#f59e0b', '#16a34a', '#9333ea'] }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    function load() {
        fetch(buildUrl()).then(function (r) { return r.json(); }).then(function (res) {
            if (!res || !res.success || !res.data) return;
            renderKpis(res.data);
            renderAlerts(res.data.alertas || []);
            renderTables(res.data);
            renderCharts(res.data);
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var preset = document.getElementById('periodoPreset');
        if (preset) preset.addEventListener('change', function () {
            if (preset.value !== 'personalizado') applyPreset();
        });
        var ini = document.getElementById('data_inicial');
        var fim = document.getElementById('data_final');
        if ((!ini || !ini.value) && (!fim || !fim.value)) applyPreset();
        load();
        var form = document.querySelector('.dashboard-filter-form');
        if (form) form.addEventListener('submit', function (e) {
            e.preventDefault();
            history.replaceState({}, '', window.location.pathname + '?' + buildUrl().split('?')[1]);
            load();
        });
    });
})();
