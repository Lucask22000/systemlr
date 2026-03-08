(function () {
    var chartPerfis = null;
    var chartAdmissoes = null;
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
        fetch('/api/rh/analytics?periodo=' + encodeURIComponent(periodo))
            .then(function (r) { return r.json(); })
            .then(function (res) {
                if (!res || !res.success || !res.data) return;
                renderizar(res.data);
            })
            .catch(function (err) {
                console.error('Erro ao carregar analytics RH', err);
            });
    }

    function renderizar(data) {
        analyticsData = data;
        if (chartPerfis) chartPerfis.destroy();
        if (chartAdmissoes) chartAdmissoes.destroy();
        var mobile = isMobileViewport();

        var c1 = document.getElementById('chartRhPerfis');
        if (c1) {
            var perfisOptions = buildChartOptions('doughnut', mobile);
            chartPerfis = new Chart(c1, {
                type: 'doughnut',
                data: {
                    labels: (data.distribuicao_roles || []).map(function (x) { return (x.role || '').toUpperCase(); }),
                    datasets: [{
                        data: (data.distribuicao_roles || []).map(function (x) { return x.quantidade; }),
                        backgroundColor: ['#0f766e', '#2563eb', '#f59e0b', '#16a34a', '#dc2626']
                    }]
                },
                options: perfisOptions
            });
        }

        var c2 = document.getElementById('chartRhAdmissoes');
        if (c2) {
            var admissoesOptions = buildChartOptions('bar', mobile);
            admissoesOptions.plugins.legend.display = false;
            chartAdmissoes = new Chart(c2, {
                type: 'bar',
                data: {
                    labels: (data.admissoes_diarias || []).map(function (x) { return x.dia.slice(5); }),
                    datasets: [{
                        label: 'Admissoes',
                        data: (data.admissoes_diarias || []).map(function (x) { return x.quantidade; }),
                        backgroundColor: '#0ea5a4'
                    }]
                },
                options: admissoesOptions
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var select = document.getElementById('rhPeriodo');
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
