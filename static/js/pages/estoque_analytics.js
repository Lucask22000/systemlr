(function () {
    function pct(v) { return (Number(v || 0)).toFixed(1) + '%'; }
    var charts = {};

    function destroyCharts() {
        Object.keys(charts).forEach(function (key) {
            if (charts[key]) charts[key].destroy();
        });
        charts = {};
    }

    function rows(id, data, empty, cols) {
        var el = document.getElementById(id);
        if (!el) return;
        if (!data.length) {
            el.innerHTML = '<tr><td colspan="' + cols + '" class="text-center">' + empty + '</td></tr>';
            return;
        }
        el.innerHTML = data.join('');
    }

    function renderAlerts(alertas) {
        var wrap = document.getElementById('estoqueAlertas');
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

    function render(data) {
        destroyCharts();
        var kpis = data.kpis || {};
        document.getElementById('kpiGiro').textContent = (Number(kpis.giro_estoque || 0)).toFixed(2) + 'x';
        document.getElementById('kpiCobertura').textContent = (Number(kpis.dias_cobertura || 0)).toFixed(1);
        document.getElementById('kpiRuptura').textContent = String(kpis.produtos_ruptura || 0);
        document.getElementById('kpiOcupacao').textContent = pct((data.ocupacao_enderecos || {}).taxa_ocupacao_pct);
        document.getElementById('metaOcupacao').textContent = (data.ocupacao_enderecos || {}).ocupados + ' / ' + (data.ocupacao_enderecos || {}).total + ' ocupados';
        document.getElementById('kpiRecebimentosPendentes').textContent = String(data.recebimentos_pendentes_armazenagem || 0);
        renderAlerts(data.alertas || []);

        charts.mov = new Chart(document.getElementById('chartMovimentacoesEstoque'), {
            type: 'line',
            data: {
                labels: (data.movimentacao_diaria || []).map(function (x) { return x.dia.slice(5); }),
                datasets: [
                    { label: 'Entradas', data: (data.movimentacao_diaria || []).map(function (x) { return x.entradas; }), borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,.12)', fill: true, tension: .25 },
                    { label: 'Saidas', data: (data.movimentacao_diaria || []).map(function (x) { return x.saidas; }), borderColor: '#dc2626', backgroundColor: 'rgba(220,38,38,.08)', fill: true, tension: .25 }
                ]
            }, options: { responsive: true, maintainAspectRatio: false }
        });
        charts.pareto = new Chart(document.getElementById('chartParetoEstoque'), {
            data: {
                labels: (data.pareto_produtos || []).map(function (x) { return (x.sku || '-') + ' - ' + x.produto; }),
                datasets: [
                    { type: 'bar', label: 'Qtde', data: (data.pareto_produtos || []).map(function (x) { return x.quantidade; }), backgroundColor: '#2563eb' },
                    { type: 'line', label: 'Acumulado %', data: (data.pareto_produtos || []).map(function (x) { return x.percentual_acumulado; }), yAxisID: 'y1', borderColor: '#f59e0b', tension: .25 }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y1: { position: 'right', min: 0, max: 100, grid: { drawOnChartArea: false } } } }
        });
        charts.oc = new Chart(document.getElementById('chartOcupacaoEnderecos'), {
            type: 'doughnut',
            data: {
                labels: ['Ocupados', 'Livres'],
                datasets: [{ data: [(data.ocupacao_enderecos || {}).ocupados || 0, (data.ocupacao_enderecos || {}).livres || 0], backgroundColor: ['#2563eb', '#cbd5e1'] }]
            }, options: { responsive: true, maintainAspectRatio: false }
        });

        rows('tableRuptura', (data.produtos_risco_ruptura || []).map(function (item) {
            return '<tr><td>' + (item.sku || '-') + '</td><td>' + item.nome + '</td><td>' + item.estoque_atual + '</td><td>' + item.estoque_minimo + '</td><td>' + item.fornecedor + '</td></tr>';
        }), 'Sem produtos em risco.', 5);
        rows('tableSemGiro', (data.produtos_sem_giro || []).map(function (item) {
            return '<tr><td>' + (item.sku || '-') + '</td><td>' + item.nome + '</td><td>' + item.ultima_movimentacao + '</td></tr>';
        }), 'Sem produtos sem giro.', 3);
    }

    function carregar(periodo) {
        fetch('/api/estoque/analytics?periodo=' + encodeURIComponent(periodo))
            .then(function (r) { return r.json(); })
            .then(function (res) { if (res && res.success && res.data) render(res.data); });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var select = document.getElementById('estoquePeriodo');
        carregar(select ? select.value : '30');
        if (select) select.addEventListener('change', function () { carregar(select.value || '30'); });
    });
})();
