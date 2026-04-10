(function () {
    function moeda(v) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0);
    }
    var charts = {};

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
        var wrap = document.getElementById('rhAlertas');
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
        var k = data.kpis || {};
        document.getElementById('kpiFuncionarios').textContent = String(k.total_funcionarios || 0);
        document.getElementById('metaFuncionarios').textContent = String(k.funcionarios_ativos || 0) + ' ativos / ' + String(k.funcionarios_inativos || 0) + ' inativos';
        document.getElementById('kpiAcessos').textContent = String(k.acessos_controlados || 0);
        document.getElementById('kpiProdutividade').textContent = Number(k.produtividade_media || 0).toFixed(2);
        document.getElementById('kpiEquipe').textContent = String(k.equipe_operacional_ativa || 0);
        document.getElementById('kpiDeficit').textContent = String(k.deficit_equipe || 0);
        renderAlerts(data.alertas || []);

        charts.cargos = new Chart(document.getElementById('chartRhCargos'), {
            type: 'bar',
            data: {
                labels: (data.distribuicao_cargos || []).map(function (x) { return x.cargo; }),
                datasets: [{ label: 'Ativos', data: (data.distribuicao_cargos || []).map(function (x) { return x.ativos || x.quantidade; }), backgroundColor: '#2563eb' }]
            }, options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y', plugins: { legend: { display: false } } }
        });
        charts.admissoes = new Chart(document.getElementById('chartRhAdmissoes'), {
            type: 'line',
            data: {
                labels: (data.admissoes_diarias || []).map(function (x) { return x.dia; }),
                datasets: [{ label: 'Admissoes', data: (data.admissoes_diarias || []).map(function (x) { return x.quantidade; }), borderColor: '#0f766e', backgroundColor: 'rgba(15,118,110,.12)', fill: true, tension: .25 }]
            }, options: { responsive: true, maintainAspectRatio: false }
        });
        charts.scatter = new Chart(document.getElementById('chartRhProdutividadeScatter'), {
            type: 'scatter',
            data: { datasets: [{ label: 'Pedidos x faturamento', data: (data.produtividade_vs_faturamento || []).map(function (x) { return { x: x.faturamento, y: x.pedidos, nome: x.nome }; }), backgroundColor: '#f59e0b' }] },
            options: { responsive: true, maintainAspectRatio: false }
        });
        charts.perfis = new Chart(document.getElementById('chartRhPerfis'), {
            type: 'doughnut',
            data: {
                labels: (data.distribuicao_perfis_acesso || []).map(function (x) { return x.perfil; }),
                datasets: [{ data: (data.distribuicao_perfis_acesso || []).map(function (x) { return x.quantidade; }), backgroundColor: ['#0f766e', '#2563eb', '#f59e0b', '#16a34a', '#9333ea', '#dc2626'] }]
            }, options: { responsive: true, maintainAspectRatio: false }
        });

        rows('tableTopProdutividade', (data.top_produtividade || []).map(function (item) {
            return '<tr><td>' + item.nome + '</td><td>' + item.cargo + '</td><td>' + item.pedidos + '</td><td>' + moeda(item.faturamento) + '</td><td>' + moeda(item.ticket_medio) + '</td></tr>';
        }), 'Sem dados de produtividade.', 5);
        rows('tableFuncionariosRecentes', (data.funcionarios_recentes || []).map(function (item) {
            return '<tr><td>' + item.nome + '</td><td>' + item.cargo + '</td><td>' + item.data_admissao + '</td></tr>';
        }), 'Sem funcionarios recentes.', 3);
        rows('tableCargosSemCobertura', (data.cargos_sem_cobertura || []).map(function (item) {
            return '<tr><td>' + item.cargo + '</td><td>' + item.ativos + '</td></tr>';
        }), 'Todos os cargos ativos possuem cobertura.', 2);
    }

    function carregar(periodo) {
        fetch('/api/rh/analytics?periodo=' + encodeURIComponent(periodo))
            .then(function (r) { return r.json(); })
            .then(function (res) { if (res && res.success && res.data) render(res.data); });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var select = document.getElementById('rhPeriodo');
        carregar(select ? select.value : '30');
        if (select) select.addEventListener('change', function () { carregar(select.value || '30'); });
    });
})();
