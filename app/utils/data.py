from datetime import datetime, timedelta


def parse_date_range(data_inicial_str, data_final_str, default_days=7):
    """Normaliza intervalo de datas em formato YYYY-MM-DD para uso em filtros."""
    agora = datetime.utcnow()
    inicio_hoje = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_hoje = inicio_hoje + timedelta(days=1)

    data_inicial_str = (data_inicial_str or '').strip()
    data_final_str = (data_final_str or '').strip()

    try:
        if data_inicial_str:
            inicio_periodo = datetime.strptime(data_inicial_str, '%Y-%m-%d')
        else:
            inicio_periodo = inicio_hoje - timedelta(days=max(default_days - 1, 0))
            data_inicial_str = inicio_periodo.strftime('%Y-%m-%d')
    except ValueError:
        inicio_periodo = inicio_hoje - timedelta(days=max(default_days - 1, 0))
        data_inicial_str = inicio_periodo.strftime('%Y-%m-%d')

    try:
        if data_final_str:
            fim_periodo = datetime.strptime(data_final_str, '%Y-%m-%d') + timedelta(days=1)
        else:
            fim_periodo = fim_hoje
            data_final_str = inicio_hoje.strftime('%Y-%m-%d')
    except ValueError:
        fim_periodo = fim_hoje
        data_final_str = inicio_hoje.strftime('%Y-%m-%d')

    if fim_periodo <= inicio_periodo:
        fim_periodo = inicio_periodo + timedelta(days=1)
        data_final_str = (fim_periodo - timedelta(days=1)).strftime('%Y-%m-%d')

    return inicio_periodo, fim_periodo, data_inicial_str, data_final_str
