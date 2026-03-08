(function () {
    function moeda(v) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0);
    }

    function getFiltro() {
        var ini = document.getElementById('data_inicial');
        var fim = document.getElementById('data_final');
        return {
            data_inicial: ini ? ini.value : '',
            data_final: fim ? fim.value : ''
        };
    }

    function buildUrl() {
        var filtro = getFiltro();
        var params = new URLSearchParams();
        if (filtro.data_inicial) params.set('data_inicial', filtro.data_inicial);
        if (filtro.data_final) params.set('data_final', filtro.data_final);
        return '/api/dashboard/analytics?' + params.toString();
    }

    function isMobileViewport() {
        return window.matchMedia('(max-width: 768px)').matches;
    }

    function buildChartOptions(type, mobile) {
        var options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: mobile ? 'bottom' : 'top',
                    labels: {
                        boxWidth: mobile ? 10 : 14,
                        usePointStyle: mobile,
                        font: {
                            size: mobile ? 10 : 12
                        }
                    }
                }
            }
        };

        if (type !== 'doughnut') {
            options.scales = {
                x: {
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: mobile ? 6 : 12,
                        maxRotation: mobile ? 0 : 40,
                        minRotation: 0,
                        font: {
                            size: mobile ? 10 : 11
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: mobile ? 10 : 11
                        }
                    }
                }
            };
        }

        return options;
    }

    var charts = {
        faturamento: null,
        status: null,
        pagamento: null,
        topProdutos: null,
        desempenhoGarcons: null,
        desempenhoCaixas: null
    };
    var analyticsData = null;
    var lastMobileState = isMobileViewport();

    function destroyCharts() {
        Object.keys(charts).forEach(function (k) {
            if (charts[k]) {
                charts[k].destroy();
                charts[k] = null;
            }
        });
    }

    function atualizarKpis(data) {
        var map = {
            kpiFaturamentoPeriodo: moeda(data.faturamento_periodo),
            kpiTicketMedio: moeda(data.ticket_medio_periodo),
            kpiFaturamentoHoje: moeda(data.faturamento_hoje),
            kpiPedidosAbertos: String(data.pedidos_abertos || 0),
            kpiPedidosCancelados: String(data.pedidos_cancelados_periodo || 0)
        };

        Object.keys(map).forEach(function (id) {
            var el = document.getElementById(id);
            if (el) el.textContent = map[id];
        });

        var metaPedidos = document.getElementById('kpiPedidosPeriodo');
        if (metaPedidos) {
            metaPedidos.textContent = String(data.pedidos_periodo_total || 0) + ' pedidos fechados';
        }
    }

    function renderCharts(data) {
        analyticsData = data;
        destroyCharts();
        var mobile = isMobileViewport();

        var ctxFat = document.getElementById('chartFaturamento');
        if (ctxFat) {
            var fatOptions = buildChartOptions('line', mobile);
            fatOptions.plugins.legend.display = false;
            charts.faturamento = new Chart(ctxFat, {
                type: 'line',
                data: {
                    labels: (data.vendas_periodo || []).map(function (d) { return d.data_curta; }),
                    datasets: [{
                        label: 'Faturamento',
                        data: (data.vendas_periodo || []).map(function (d) { return d.faturamento; }),
                        borderColor: '#0f766e',
                        backgroundColor: 'rgba(15, 118, 110, 0.16)',
                        tension: 0.25,
                        pointRadius: mobile ? 0 : 2,
                        pointHoverRadius: mobile ? 3 : 4,
                        fill: true
                    }]
                },
                options: fatOptions
            });
        }

        var ctxStatus = document.getElementById('chartStatus');
        if (ctxStatus) {
            var statusOptions = buildChartOptions('doughnut', mobile);
            charts.status = new Chart(ctxStatus, {
                type: 'doughnut',
                data: {
                    labels: (data.pedidos_por_status || []).map(function (s) { return s.label; }),
                    datasets: [{
                        data: (data.pedidos_por_status || []).map(function (s) { return s.quantidade; }),
                        backgroundColor: ['#0f766e', '#f59e0b', '#2563eb', '#16a34a', '#dc2626']
                    }]
                },
                options: statusOptions
            });
        }

        var ctxPag = document.getElementById('chartPagamento');
        if (ctxPag) {
            var pagOptions = buildChartOptions('bar', mobile);
            pagOptions.plugins.legend.display = false;
            charts.pagamento = new Chart(ctxPag, {
                type: 'bar',
                data: {
                    labels: (data.metodos_pagamento || []).map(function (m) { return m.metodo; }),
                    datasets: [{
                        label: 'Pedidos',
                        data: (data.metodos_pagamento || []).map(function (m) { return m.quantidade; }),
                        backgroundColor: '#155e75'
                    }]
                },
                options: pagOptions
            });
        }

        var ctxTop = document.getElementById('chartTopProdutos');
        if (ctxTop) {
            var topOptions = buildChartOptions('bar', mobile);
            topOptions.plugins.legend.display = false;
            if (mobile) {
                topOptions.indexAxis = 'y';
                topOptions.scales.y.ticks.autoSkip = false;
            }
            charts.topProdutos = new Chart(ctxTop, {
                type: 'bar',
                data: {
                    labels: (data.top_produtos_vendidos || []).map(function (p) { return p.nome; }),
                    datasets: [{
                        label: 'Receita (R$)',
                        data: (data.top_produtos_vendidos || []).map(function (p) { return p.receita; }),
                        backgroundColor: '#0ea5a4'
                    }]
                },
                options: topOptions
            });
        }

        var ctxGarcons = document.getElementById('chartDesempenhoGarcons');
        if (ctxGarcons) {
            var chartWrapperGarcons = ctxGarcons.closest('.performance-chart-container');
            var garconsData = data.desempenho_garcons || [];
            if (chartWrapperGarcons) {
                chartWrapperGarcons.style.height = mobile
                    ? Math.max(220, garconsData.length * 56) + 'px'
                    : '300px';
            }

            var garconsOptions = buildChartOptions('bar', mobile);
            garconsOptions.indexAxis = 'y';
            garconsOptions.plugins.legend.display = false;
            garconsOptions.scales.x.ticks.callback = function (value) {
                return moeda(value);
            };
            garconsOptions.scales.y.ticks.autoSkip = false;

            charts.desempenhoGarcons = new Chart(ctxGarcons, {
                type: 'bar',
                data: {
                    labels: garconsData.map(function (item) { return item.nome; }),
                    datasets: [{
                        label: 'Faturamento (R$)',
                        data: garconsData.map(function (item) { return item.faturamento; }),
                        backgroundColor: '#0f766e',
                        borderRadius: 6,
                        barThickness: mobile ? 14 : 18
                    }]
                },
                options: garconsOptions
            });
        }

        var ctxCaixas = document.getElementById('chartDesempenhoCaixas');
        if (ctxCaixas) {
            var chartWrapperCaixas = ctxCaixas.closest('.performance-chart-container');
            var caixasData = data.desempenho_caixas || [];
            if (chartWrapperCaixas) {
                chartWrapperCaixas.style.height = mobile
                    ? Math.max(220, caixasData.length * 56) + 'px'
                    : '300px';
            }

            var caixasOptions = buildChartOptions('bar', mobile);
            caixasOptions.indexAxis = 'y';
            caixasOptions.plugins.legend.display = false;
            caixasOptions.scales.x.ticks.callback = function (value) {
                return moeda(value);
            };
            caixasOptions.scales.y.ticks.autoSkip = false;

            charts.desempenhoCaixas = new Chart(ctxCaixas, {
                type: 'bar',
                data: {
                    labels: caixasData.map(function (item) { return item.nome; }),
                    datasets: [{
                        label: 'Faturamento (R$)',
                        data: caixasData.map(function (item) { return item.faturamento; }),
                        backgroundColor: '#155e75',
                        borderRadius: 6,
                        barThickness: mobile ? 14 : 18
                    }]
                },
                options: caixasOptions
            });
        }
    }

    function carregarAnalytics() {
        fetch(buildUrl())
            .then(function (r) { return r.json(); })
            .then(function (res) {
                if (!res || !res.success || !res.data) return;
                atualizarKpis(res.data);
                renderCharts(res.data);
            })
            .catch(function (err) {
                console.error('Falha ao carregar analytics do dashboard', err);
            });
    }

    document.addEventListener('DOMContentLoaded', function () {
        carregarAnalytics();
        var form = document.querySelector('.dashboard-filter-form');
        if (form) {
            form.addEventListener('submit', function (event) {
                event.preventDefault();
                var filtro = getFiltro();
                var params = new URLSearchParams();
                if (filtro.data_inicial) params.set('data_inicial', filtro.data_inicial);
                if (filtro.data_final) params.set('data_final', filtro.data_final);
                var newUrl = window.location.pathname + '?' + params.toString();
                history.replaceState({}, '', newUrl);
                carregarAnalytics();
            });
        }

        window.addEventListener('resize', function () {
            var mobileNow = isMobileViewport();
            if (mobileNow === lastMobileState) return;
            lastMobileState = mobileNow;
            if (analyticsData) renderCharts(analyticsData);
        });
    });
})();
