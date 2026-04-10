(function () {
    var charts = {};

    function pct(v) { return (Number(v || 0)).toFixed(1) + '%'; }

    function destroyCharts() {
        Object.keys(charts).forEach(function (key) {
            if (charts[key]) charts[key].destroy();
        });
        charts = {};
    }

    function rows(id, items, empty, cols) {
        var el = document.getElementById(id);
        if (!el) return;
        if (!items.length) {
            el.innerHTML = '<tr><td colspan="' + cols + '" class="text-center">' + empty + '</td></tr>';
            return;
        }
        el.innerHTML = items.join('');
    }

    function renderAlerts(alertas) {
        var wrap = document.getElementById('expedicaoAlertas');
        if (!wrap) return;
        if (!(alertas || []).length) {
            wrap.innerHTML = '<p class="text-muted mb-0">Nenhum alerta critico para hoje.</p>';
            return;
        }
        wrap.innerHTML = alertas.map(function (item) {
            var cls = item.nivel === 'danger' ? 'danger' : (item.nivel === 'warning' ? 'warning' : 'info');
            return '<div class="alert alert-' + cls + ' mb-0"><strong>' + item.titulo + ':</strong> ' + item.descricao + '</div>';
        }).join('');
    }

    function render(data) {
        destroyCharts();
        var k = data.kpis || {};
        document.getElementById('kpiExpTotal').textContent = String(k.pedidos_dia_total || 0);
        document.getElementById('kpiExpSeparados').textContent = String(k.separados || 0) + ' / ' + String(k.embalados || 0);
        document.getElementById('kpiExpExpedidos').textContent = String(k.expedidos || 0) + ' / ' + String(k.entregues || 0);
        document.getElementById('kpiExpTempo').textContent = Number(k.tempo_medio_separacao_min || 0).toFixed(1) + ' min';
        document.getElementById('kpiExpAderencia').textContent = pct(k.aderencia_rota_pct);
        renderAlerts(data.alertas || []);

        charts.progresso = new Chart(document.getElementById('chartExpedicaoProgresso'), {
            type: 'bar',
            data: {
                labels: (data.progresso_por_hora || []).map(function (x) { return x.hora; }),
                datasets: [
                    { label: 'Separacao', data: (data.progresso_por_hora || []).map(function (x) { return x.separacao; }), backgroundColor: '#2563eb' },
                    { label: 'Embalagem', data: (data.progresso_por_hora || []).map(function (x) { return x.embalagem; }), backgroundColor: '#f59e0b' },
                    { label: 'Expedicao', data: (data.progresso_por_hora || []).map(function (x) { return x.expedicao; }), backgroundColor: '#0f766e' },
                    { label: 'Entregue', data: (data.progresso_por_hora || []).map(function (x) { return x.entregue; }), backgroundColor: '#16a34a' }
                ]
            }, options: { responsive: true, maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true } } }
        });
        charts.fila = new Chart(document.getElementById('chartExpedicaoFila'), {
            type: 'bar',
            data: {
                labels: (data.fila_separacao_por_hora || []).map(function (x) { return x.hora; }),
                datasets: [{ label: 'Pendentes', data: (data.fila_separacao_por_hora || []).map(function (x) { return x.pendentes; }), backgroundColor: '#dc2626' }]
            }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
        charts.rotas = new Chart(document.getElementById('chartExpedicaoRotas'), {
            type: 'doughnut',
            data: {
                labels: ['Em rota', 'Entregues', 'Atrasadas'],
                datasets: [{ data: [(data.status_rotas || {}).em_rota || 0, (data.status_rotas || {}).entregues || 0, (data.status_rotas || {}).atrasadas || 0], backgroundColor: ['#2563eb', '#16a34a', '#dc2626'] }]
            }, options: { responsive: true, maintainAspectRatio: false }
        });

        rows('tableExpSeparacao', (data.pedidos_separacao || []).map(function (item) {
            return '<tr><td>#' + item.id + '</td><td>' + item.cliente + '</td><td>' + item.rota + '</td><td>' + item.motorista + '</td><td>' + item.tempo_espera_min.toFixed(1) + ' min</td></tr>';
        }), 'Nenhum pedido em separacao.', 5);
        rows('tableExpRota', (data.pedidos_rota || []).map(function (item) {
            return '<tr><td>#' + item.id + '</td><td>' + item.cliente + '</td><td>' + item.rota + '</td><td>' + item.motorista + '</td><td>' + item.previsao_entrega + '</td></tr>';
        }), 'Nenhum pedido em rota.', 5);
        rows('tableExpVeiculos', (data.veiculos || []).map(function (item) {
            return '<tr><td>' + item.nome + '</td><td>' + item.placa + '</td><td>' + item.tipo + '</td><td>' + item.capacidade + '</td></tr>';
        }), 'Nenhum veiculo configurado.', 4);
    }

    function carregar() {
        fetch('/api/expedicao/analytics')
            .then(function (r) { return r.json(); })
            .then(function (res) { if (res && res.success && res.data) render(res.data); });
    }

    document.addEventListener('DOMContentLoaded', function () {
        carregar();
    });
})();
