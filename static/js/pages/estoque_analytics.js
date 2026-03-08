(function () {
    var chartMov = null;
    var chartCategoria = null;
    var analyticsData = null;
    var lastMobileState = isMobileViewport();

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
                        maxRotation: mobile ? 0 : 35,
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

    function carregar(periodo) {
        fetch('/api/estoque/analytics?periodo=' + encodeURIComponent(periodo))
            .then(function (r) { return r.json(); })
            .then(function (res) {
                if (!res || !res.success || !res.data) return;
                renderizar(res.data);
            })
            .catch(function (err) {
                console.error('Erro ao carregar analytics de estoque', err);
            });
    }

    function renderizar(data) {
        analyticsData = data;
        if (chartMov) chartMov.destroy();
        if (chartCategoria) chartCategoria.destroy();
        var mobile = isMobileViewport();

        var c1 = document.getElementById('chartMovimentacoesEstoque');
        if (c1) {
            var movOptions = buildChartOptions('line', mobile);
            chartMov = new Chart(c1, {
                type: 'line',
                data: {
                    labels: (data.movimentacao_diaria || []).map(function (x) { return x.dia.slice(5); }),
                    datasets: [
                        { label: 'Entradas', data: (data.movimentacao_diaria || []).map(function (x) { return x.entradas; }), borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,0.15)', fill: true, tension: 0.2, pointRadius: mobile ? 0 : 2, pointHoverRadius: mobile ? 3 : 4 },
                        { label: 'Saidas', data: (data.movimentacao_diaria || []).map(function (x) { return x.saidas; }), borderColor: '#dc2626', backgroundColor: 'rgba(220,38,38,0.12)', fill: true, tension: 0.2, pointRadius: mobile ? 0 : 2, pointHoverRadius: mobile ? 3 : 4 }
                    ]
                },
                options: movOptions
            });
        }

        var c2 = document.getElementById('chartValorCategoriaEstoque');
        if (c2) {
            var categoriaOptions = buildChartOptions('bar', mobile);
            categoriaOptions.plugins.legend.display = false;
            if (mobile) {
                categoriaOptions.indexAxis = 'y';
                categoriaOptions.scales.y.ticks.autoSkip = false;
            }
            chartCategoria = new Chart(c2, {
                type: 'bar',
                data: {
                    labels: (data.valor_por_categoria || []).map(function (x) { return x.categoria; }),
                    datasets: [{
                        label: 'Valor (R$)',
                        data: (data.valor_por_categoria || []).map(function (x) { return x.valor_total; }),
                        backgroundColor: '#0f766e'
                    }]
                },
                options: categoriaOptions
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var select = document.getElementById('estoquePeriodo');
        var periodo = select ? select.value : '30';
        carregar(periodo);
        if (select) {
            select.addEventListener('change', function () {
                carregar(select.value || '30');
            });
        }

        window.addEventListener('resize', function () {
            var mobileNow = isMobileViewport();
            if (mobileNow === lastMobileState) return;
            lastMobileState = mobileNow;
            if (analyticsData) renderizar(analyticsData);
        });
    });
})();
