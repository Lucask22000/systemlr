(function () {
    var timer = null;

    function pctText(v) {
        return (Number(v || 0)).toFixed(1) + '%';
    }

    function updateView(data) {
        var kpis = data || {};
        var total = kpis.pedidos_totais || 1;
        document.getElementById('rtStatus').textContent = 'Atualizado';
        document.getElementById('rtSeparacaoQtd').textContent = kpis.separacao.em_andamento;
        document.getElementById('rtSeparacaoPct').style.width = pctText(kpis.separacao.pct);
        document.getElementById('rtEntregasAndamento').textContent = kpis.entregas.em_andamento;
        document.getElementById('rtEntregasPct').style.width = pctText((kpis.entregas.em_andamento / total) * 100.0);
        document.getElementById('rtEntregasConcluidas').textContent = kpis.entregas.concluidas;
        document.getElementById('rtEntregasConcluidasPct').style.width = pctText(kpis.entregas.pct_concluidas);
        document.getElementById('rtRecebimentosPendentes').textContent = kpis.recebimentos_pendentes;
        document.getElementById('rtAvarias').textContent = kpis.avarias_30d;
        document.getElementById('rtDevolucoes').textContent = kpis.devolucoes_30d;
    }

    function tick() {
        fetch('/api/estoque/processos-tempo-real')
            .then(function (r) { return r.json(); })
            .then(function (res) {
                if (res && res.success && res.data) {
                    updateView(res.data);
                }
            })
            .catch(function () {
                document.getElementById('rtStatus').textContent = 'Erro ao atualizar';
            });
    }

    document.addEventListener('DOMContentLoaded', function () {
        tick();
        timer = setInterval(tick, 5000);
    });
})();
