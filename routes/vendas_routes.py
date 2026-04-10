import math
from datetime import datetime
from datetime import time
from datetime import timedelta
import json
import secrets
import qrcode
from io import BytesIO
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import render_template, request, redirect, url_for, flash, session, Response, jsonify
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import selectinload, load_only

from app import extensions
from models import (
    db,
    Caixa,
    ClienteEndereco,
    EnderecoEstoque,
    EmpresaConfig,
    FrotaVeiculo,
    Funcionario,
    Garcom,
    ItemPedido,
    Mesa,
    Movimentacao,
    MovimentacaoCaixa,
    Pedido,
    PermissaoAcesso,
    Produto,
)
from realtime import publish_alert, sse_stream
from security import json_response
from app.constants import ENDPOINT_TO_PAGINA
from app.exceptions import AppError, BusinessRuleError, ValidationError
from app.services.financeiro_service import _build_payment_data
from app.services.pedido_service import (
    _aplicar_transicao_status as service_aplicar_transicao_status,
    create_order as service_create_order,
    _normalizar_item_payload,
    _recalcular_total_pedido,
    update_order as service_update_order,
)
from app.services.transaction import atomic_transaction
from app.services.venda_service import VendaService
from app.services.workflow import ExpedicaoStatus, transition_expedicao_status
from app.services.operational_rules import require_cancel_reason
from app.services.utils_service import _to_float, _to_int
from app.utils.payment_config import default_payment_id, infer_payment_method_id, load_payment_options, payment_methods_map
from app.utils.responses import fail, ok
from app.utils.validators import validar_cep

ORDER_ALLOWED_TRANSITIONS = Pedido.TRANSICOES_PERMITIDAS
ORDER_IMMUTABLE_STATUSES = Pedido.STATUS_IMUTAVEIS
DELIVERY_SEPARATION_STATUSES = {Pedido.STATUS_ABERTO, Pedido.STATUS_EM_PREPARO, Pedido.STATUS_ENTREGUE}
venda_service = VendaService()


def _obter_empresa_config():
    empresa = EmpresaConfig.query.first()
    if not empresa:
        empresa = EmpresaConfig()
        db.session.add(empresa)
        db.session.commit()
    return empresa


def _atendimento_mesas_ativo():
    empresa = _obter_empresa_config()
    return empresa.atendimento_mesas_ativo is not False


def _separacao_entrega_ativa(empresa=None):
    empresa = empresa or _obter_empresa_config()
    return empresa.separacao_entrega_ativa is not False


def _emissao_etiqueta_entrega_ativa(empresa=None):
    empresa = empresa or _obter_empresa_config()
    return _separacao_entrega_ativa(empresa) and empresa.emissao_etiqueta_entrega_ativa is not False


def _parse_horario_hhmm(valor):
    texto = (valor or '').strip()
    if not texto:
        return None
    try:
        hora_txt, minuto_txt = texto.split(':', 1)
        hora = int(hora_txt)
        minuto = int(minuto_txt)
    except (AttributeError, TypeError, ValueError):
        return None
    if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
        return None
    return time(hour=hora, minute=minuto)


def _origens_separacao_entrega(empresa=None):
    empresa = empresa or _obter_empresa_config()
    origens = ['site']
    if empresa.separacao_entrega_unir_vendas_off:
        origens.append('interno')
    return origens


def _pedido_pronto_para_roteirizacao(pedido):
    if not pedido:
        return False
    if not pedido.separacao_entrega_concluida:
        return False
    if pedido.status in {Pedido.STATUS_CANCELADO, Pedido.STATUS_FECHADO}:
        return False
    return True


def _coletar_metricas_dashboard_tempo_real():
    agora = datetime.utcnow()
    inicio_dia = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        pedidos_ultimos_15_min = Pedido.query.filter(Pedido.criado_em >= (agora - timedelta(minutes=15))).count()
        faturamento_dia = db.session.query(db.func.sum(Pedido.total)).filter(
            Pedido.status == Pedido.STATUS_FECHADO,
            Pedido.fechado_em >= inicio_dia,
            Pedido.fechado_em < inicio_dia + timedelta(days=1),
        ).scalar() or 0.0
        produtos_vendidos_turno = db.session.query(db.func.sum(ItemPedido.quantidade)).join(
            Pedido, Pedido.id == ItemPedido.pedido_id
        ).filter(
            Pedido.status == Pedido.STATUS_FECHADO,
            Pedido.fechado_em >= inicio_dia,
            Pedido.fechado_em < inicio_dia + timedelta(days=1),
        ).scalar() or 0
    except (OperationalError, ProgrammingError):
        db.session.rollback()
        pedidos_ultimos_15_min = 0
        faturamento_dia = 0.0
        produtos_vendidos_turno = 0
    return {
        'pedidos_ultimos_15_min': int(pedidos_ultimos_15_min or 0),
        'faturamento_dia': float(faturamento_dia or 0.0),
        'produtos_vendidos_turno': int(produtos_vendidos_turno or 0),
    }


def _publicar_metricas_dashboard_tempo_real():
    try:
        publish_alert({
            'event': 'dashboard_metrics',
            'data': _coletar_metricas_dashboard_tempo_real(),
        })
    except Exception:
        pass


def _referencia_pedido_roteirizacao(pedido):
    return (
        pedido.separacao_entrega_em
        or pedido.fechado_em
        or pedido.criado_em
    )


def _config_corte_roteirizacao(empresa, agora=None):
    agora = agora or datetime.utcnow()
    horario_txt = (
        empresa.entrega_horario_fechamento_roteirizacao
        if empresa and empresa.entrega_horario_fechamento_roteirizacao
        else ''
    )
    horario = _parse_horario_hhmm(horario_txt)
    if not horario:
        return {
            'ativo': False,
            'horario': None,
            'janela_aberta': True,
            'corte_do_dia': None,
            'proximo_ciclo_em': None,
        }

    corte_do_dia = agora.replace(
        hour=horario.hour,
        minute=horario.minute,
        second=0,
        microsecond=0,
    )
    janela_aberta = agora <= corte_do_dia
    proximo_ciclo_em = corte_do_dia if janela_aberta else (corte_do_dia + timedelta(days=1))
    return {
        'ativo': True,
        'horario': horario_txt,
        'janela_aberta': janela_aberta,
        'corte_do_dia': corte_do_dia,
        'proximo_ciclo_em': proximo_ciclo_em,
    }


def _separar_pedidos_por_corte_roteirizacao(pedidos, empresa, agora=None):
    corte = _config_corte_roteirizacao(empresa, agora=agora)
    pedidos_base = list(pedidos or [])
    if not corte['ativo']:
        return pedidos_base, [], corte

    liberados = []
    proximo_ciclo = []
    limite = corte['corte_do_dia']
    for pedido in pedidos_base:
        referencia = _referencia_pedido_roteirizacao(pedido)
        if referencia and referencia > limite:
            proximo_ciclo.append(pedido)
        else:
            liberados.append(pedido)
    return liberados, proximo_ciclo, corte


def _carregar_lista_config(valor_json):
    if not valor_json:
        return []
    try:
        dados = json.loads(valor_json)
    except Exception:
        return []
    if not isinstance(dados, list):
        return []
    itens = []
    for item in dados:
        if isinstance(item, dict):
            texto = (
                item.get('nome')
                or item.get('empresa')
                or item.get('descricao')
                or ''
            )
        else:
            texto = str(item or '').strip()
        if texto:
            itens.append(texto)
    return itens


def _normalizar_linhas_configuracao(texto):
    linhas = []
    vistos = set()
    for linha in (texto or '').splitlines():
        valor = linha.strip()
        if not valor:
            continue
        chave = valor.lower()
        if chave in vistos:
            continue
        vistos.add(chave)
        linhas.append(valor)
    return linhas


def _parse_veiculo_cadastrado(valor):
    texto = (valor or '').strip()
    if not texto:
        return None, None
    if '|' in texto:
        nome, placa = texto.split('|', 1)
        nome = nome.strip() or None
        placa = placa.strip().upper() or None
        return nome, placa
    return texto, None


def _carregar_veiculos_config(valor_json=None, empresa=None):
    empresa_ref = empresa
    if isinstance(valor_json, EmpresaConfig):
        empresa_ref = valor_json
        valor_json = empresa_ref.entrega_veiculos_json

    if empresa_ref is not None and _frota_relacional_disponivel():
        veiculos_relacionais = _listar_veiculos_frota(empresa_ref)
        if veiculos_relacionais:
            return [_serializar_frota_veiculo(item) for item in veiculos_relacionais]
        valor_json = valor_json or empresa_ref.entrega_veiculos_json

    return _carregar_veiculos_config_legado(valor_json)


def _carregar_veiculos_config_legado(valor_json):
    if not valor_json:
        return []
    try:
        dados = json.loads(valor_json)
    except Exception:
        return []
    if not isinstance(dados, list):
        return []

    veiculos = []
    for item in dados:
        if isinstance(item, dict):
            nome = (item.get('nome') or '').strip()
            if not nome:
                continue
            veiculos.append({
                'nome': nome,
                'placa': (item.get('placa') or '').strip().upper() or None,
                'categoria': (item.get('categoria') or '').strip().lower() or 'geral',
                'tipo_entrega': (item.get('tipo_entrega') or '').strip().lower() or 'todos',
                'capacidade_pedidos': max(int(item.get('capacidade_pedidos') or 0), 0),
                'capacidade_kg': float(item.get('capacidade_kg') or 0) if item.get('capacidade_kg') not in (None, '') else None,
                'empresa': (item.get('empresa') or '').strip() or None,
                'ativo': item.get('ativo', True) is not False,
            })
            continue

        partes = [p.strip() for p in str(item or '').split('|')]
        nome = partes[0] if partes else ''
        if not nome:
            continue
        capacidade_pedidos = 0
        try:
            capacidade_pedidos = int(partes[4]) if len(partes) > 4 and partes[4] else 0
        except Exception:
            capacidade_pedidos = 0
        capacidade_kg = None
        try:
            capacidade_kg = float(partes[5]) if len(partes) > 5 and partes[5] else None
        except Exception:
            capacidade_kg = None
        veiculos.append({
            'nome': nome,
            'placa': partes[1].upper() if len(partes) > 1 and partes[1] else None,
            'categoria': (partes[2].lower() if len(partes) > 2 and partes[2] else 'geral'),
            'tipo_entrega': (partes[3].lower() if len(partes) > 3 and partes[3] else 'todos'),
            'capacidade_pedidos': capacidade_pedidos,
            'capacidade_kg': capacidade_kg,
            'empresa': partes[6] if len(partes) > 6 and partes[6] else None,
            'ativo': True,
        })
    return veiculos


def _serializar_veiculos_config_texto(veiculos):
    linhas = []
    for item in veiculos:
        linhas.append(' | '.join([
            item.get('nome') or '',
            item.get('placa') or '',
            item.get('categoria') or 'geral',
            item.get('tipo_entrega') or 'todos',
            str(item.get('capacidade_pedidos') or ''),
            str(item.get('capacidade_kg') or ''),
            item.get('empresa') or '',
        ]).strip())
    return '\n'.join(linhas)


def _normalizar_veiculos_texto(texto):
    veiculos = []
    vistos = set()
    for linha in (texto or '').splitlines():
        partes = [p.strip() for p in linha.split('|')]
        nome = partes[0] if partes else ''
        if not nome:
            continue
        chave = nome.lower(), (partes[1].upper() if len(partes) > 1 and partes[1] else '')
        if chave in vistos:
            continue
        vistos.add(chave)
        capacidade_pedidos = 0
        try:
            capacidade_pedidos = int(partes[4]) if len(partes) > 4 and partes[4] else 0
        except Exception:
            capacidade_pedidos = 0
        capacidade_kg = None
        try:
            capacidade_kg = float(partes[5]) if len(partes) > 5 and partes[5] else None
        except Exception:
            capacidade_kg = None
        veiculos.append({
            'nome': nome,
            'placa': partes[1].upper() if len(partes) > 1 and partes[1] else None,
            'categoria': (partes[2].lower() if len(partes) > 2 and partes[2] else 'geral'),
            'tipo_entrega': (partes[3].lower() if len(partes) > 3 and partes[3] else 'todos'),
            'capacidade_pedidos': capacidade_pedidos,
            'capacidade_kg': capacidade_kg,
            'empresa': partes[6] if len(partes) > 6 and partes[6] else None,
            'ativo': True,
        })
    return veiculos


def _frota_relacional_disponivel():
    """Verifica se a tabela relacional da frota esta acessivel na conexao ativa."""
    try:
        return db.inspect(db.session.connection()).has_table('frota_veiculos')
    except Exception:
        try:
            return db.inspect(db.engine).has_table('frota_veiculos')
        except Exception:
            return False


def _listar_veiculos_frota(empresa, *, apenas_ativos=False):
    if not empresa or not getattr(empresa, 'id', None) or not _frota_relacional_disponivel():
        return []
    query = FrotaVeiculo.query.filter(FrotaVeiculo.empresa_id == empresa.id)
    if apenas_ativos:
        query = query.filter(FrotaVeiculo.ativo.is_(True))
    return query.order_by(FrotaVeiculo.nome.asc(), FrotaVeiculo.id.asc()).all()


def _serializar_frota_veiculo(veiculo):
    return {
        'id': veiculo.id,
        'nome': veiculo.nome,
        'placa': (veiculo.placa or '').strip().upper() or None,
        'categoria': veiculo.tipo or 'geral',
        'tipo': veiculo.tipo or 'geral',
        'tipo_entrega': (veiculo.tipo_entrega or 'todos').strip().lower(),
        'capacidade_pedidos': int(veiculo.capacidade_pedidos or 0),
        'capacidade_kg': float(veiculo.capacidade_kg or 0) if veiculo.capacidade_kg is not None else None,
        'capacidade_volume': float(veiculo.capacidade_volume or 0) if veiculo.capacidade_volume is not None else None,
        'motorista_padrao': veiculo.motorista_padrao,
        'empresa': veiculo.empresa_terceirizada,
        'ativo': veiculo.ativo is not False,
    }


def _opcoes_veiculos_cadastrados(empresa):
    if empresa and _frota_relacional_disponivel():
        return _listar_veiculos_frota(empresa, apenas_ativos=True)
    return [
        {
            'id': '',
            'nome': item.get('nome'),
            'placa': item.get('placa'),
        }
        for item in _carregar_veiculos_config_legado(empresa.entrega_veiculos_json if empresa else None)
        if item.get('ativo', True)
    ]


def _obter_veiculo_frota(empresa, veiculo_id):
    if not empresa or not veiculo_id or not _frota_relacional_disponivel():
        return None
    return FrotaVeiculo.query.filter_by(id=veiculo_id, empresa_id=empresa.id).first()


def _sincronizar_frota_legada(empresa):
    """Mantem o JSON legado atualizado enquanto a frota migra para tabela propria."""
    if not empresa:
        return
    if _frota_relacional_disponivel():
        veiculos = [
            _serializar_frota_veiculo(item)
            for item in _listar_veiculos_frota(empresa)
        ]
        empresa.entrega_veiculos_json = json.dumps(veiculos, ensure_ascii=False) if veiculos else None


def _carregar_regras_roteirizacao(empresa):
    regras = {
        'prefixo_rota': 'Rota',
        'tipo_entrega': 'todos',
        'modo_distribuicao': 'capacidade',
        'considerar_capacidade': True,
        'max_paradas_por_rota': 0,
        'somente_sem_rota': True,
    }
    if not empresa or not empresa.entrega_regras_roteirizacao_json:
        return regras
    try:
        dados = json.loads(empresa.entrega_regras_roteirizacao_json)
    except Exception:
        return regras
    if not isinstance(dados, dict):
        return regras
    regras.update({
        'prefixo_rota': (dados.get('prefixo_rota') or regras['prefixo_rota']).strip() or 'Rota',
        'tipo_entrega': (dados.get('tipo_entrega') or regras['tipo_entrega']).strip().lower() or 'todos',
        'modo_distribuicao': (dados.get('modo_distribuicao') or regras['modo_distribuicao']).strip().lower() or 'capacidade',
        'considerar_capacidade': bool(dados.get('considerar_capacidade', True)),
        'max_paradas_por_rota': max(int(dados.get('max_paradas_por_rota') or 0), 0),
        'somente_sem_rota': bool(dados.get('somente_sem_rota', True)),
    })
    return regras


def _regras_roteirizacao_do_form(request_obj, empresa):
    atuais = _carregar_regras_roteirizacao(empresa)
    return {
        'prefixo_rota': (request_obj.form.get('prefixo_rota') or atuais['prefixo_rota']).strip() or 'Rota',
        'tipo_entrega': (request_obj.form.get('tipo_entrega') or atuais['tipo_entrega']).strip().lower() or 'todos',
        'modo_distribuicao': (request_obj.form.get('modo_distribuicao') or atuais['modo_distribuicao']).strip().lower() or 'capacidade',
        'considerar_capacidade': request_obj.form.get('considerar_capacidade') == 'on',
        'max_paradas_por_rota': max(int(request_obj.form.get('max_paradas_por_rota') or 0), 0),
        'somente_sem_rota': request_obj.form.get('somente_sem_rota') == 'on',
    }


def _distribuir_pedidos_automaticamente(pedidos, veiculos, regras, empresa):
    if not pedidos:
        return 0

    pedidos_ordenados = sorted(pedidos, key=lambda p: (p.criado_em or datetime.utcnow(), p.id))
    tipo_entrega = regras.get('tipo_entrega') or 'todos'
    if tipo_entrega != 'todos':
        pedidos_ordenados = [p for p in pedidos_ordenados if (p.origem or '').strip().lower() == tipo_entrega]

    if regras.get('somente_sem_rota', True):
        pedidos_ordenados = [p for p in pedidos_ordenados if not (p.rota_entrega or '').strip()]

    if not pedidos_ordenados:
        return 0

    pedidos_ordenados = _ordenar_pedidos_por_proximidade(pedidos_ordenados, getattr(empresa, 'cep', None))

    veiculos_ativos = [v for v in veiculos if v.get('ativo', True)]
    if tipo_entrega != 'todos':
        veiculos_ativos = [
            v for v in veiculos_ativos
            if (v.get('tipo_entrega') or 'todos') in {'todos', tipo_entrega}
        ]

    if not veiculos_ativos:
        veiculos_ativos = [{
            'nome': empresa.entrega_veiculo_padrao or 'Expedicao',
            'placa': None,
            'categoria': 'geral',
            'tipo_entrega': tipo_entrega,
            'capacidade_pedidos': 0,
            'capacidade_kg': None,
            'empresa': None,
            'ativo': True,
        }]

    modo = regras.get('modo_distribuicao') or 'capacidade'
    if modo == 'capacidade':
        veiculos_base = sorted(veiculos_ativos, key=lambda v: (-(v.get('capacidade_pedidos') or 0), v.get('nome') or ''))
    else:
        veiculos_base = list(veiculos_ativos)

    prefixo = regras.get('prefixo_rota') or 'Rota'
    max_paradas_regra = int(regras.get('max_paradas_por_rota') or 0)
    considerar_capacidade = bool(regras.get('considerar_capacidade'))
    alocados = 0
    cursor_pedido = 0
    rodada = 1

    while cursor_pedido < len(pedidos_ordenados):
        if modo == 'round_robin':
            iteracao_veiculos = veiculos_ativos
        else:
            iteracao_veiculos = veiculos_base

        for indice_veiculo, veiculo in enumerate(iteracao_veiculos, start=1):
            if cursor_pedido >= len(pedidos_ordenados):
                break
            limite = max_paradas_regra if max_paradas_regra > 0 else 0
            if considerar_capacidade and (veiculo.get('capacidade_pedidos') or 0) > 0:
                capacidade_veiculo = int(veiculo.get('capacidade_pedidos') or 0)
                limite = min(limite, capacidade_veiculo) if limite > 0 else capacidade_veiculo
            if limite <= 0:
                limite = len(pedidos_ordenados)

            rota_nome = f"{prefixo} {rodada}.{indice_veiculo} - {veiculo.get('nome') or 'Expedicao'}"
            ordem = 1
            while cursor_pedido < len(pedidos_ordenados) and ordem <= limite:
                pedido = pedidos_ordenados[cursor_pedido]
                pedido.rota_entrega = rota_nome
                pedido.ordem_rota = ordem
                pedido.local_saida = pedido.local_saida or empresa.entrega_local_saida_padrao
                pedido.veiculo_tipo = veiculo.get('nome') or empresa.entrega_veiculo_padrao
                pedido.veiculo_placa = veiculo.get('placa') or pedido.veiculo_placa
                pedido.motorista_nome = pedido.motorista_nome or empresa.entrega_motorista_padrao
                pedido.empresa_terceirizada = veiculo.get('empresa') or pedido.empresa_terceirizada
                ordem += 1
                cursor_pedido += 1
                alocados += 1
                if modo == 'round_robin':
                    break
        rodada += 1

    return alocados


def _resolver_etapa_expedicao(pedido):
    if not pedido.separacao_entrega_concluida:
        return 'separacao'
    if not pedido.etiqueta_entrega_emitida_em:
        return 'embalagem'
    if not pedido.saiu_para_entrega_em:
        return 'expedicao'
    if not pedido.entrega_concluida_em:
        return 'em_rota'
    return 'entregue'


def _pedido_na_fila_entrega(pedido, empresa=None):
    empresa = empresa or _obter_empresa_config()
    return (
        _separacao_entrega_ativa(empresa)
        and (pedido.origem or '').strip().lower() in _origens_separacao_entrega(empresa)
    )


def _validar_pedido_para_separacao(pedido, funcionario=None):
    """Garante que os itens estao em areas autorizadas para picking/expedicao."""
    tipos_permitidos = {'picking', 'box_expedicao', 'expedicao'}
    endereco_ids = {
        item.produto.endereco_id
        for item in (pedido.itens or [])
        if item.produto and item.produto.endereco_id
    }
    enderecos = {}
    if endereco_ids:
        enderecos = {
            endereco.id: endereco
            for endereco in _endereco_query_permitida(funcionario).filter(EnderecoEstoque.id.in_(endereco_ids)).all()
        }

    produtos_sem_picking = []
    produtos_vencidos = []
    for item in pedido.itens or []:
        produto = item.produto
        if not produto:
            produtos_sem_picking.append(f'Produto #{item.produto_id}')
            continue
        if produto.vencido:
            produtos_vencidos.append(produto.nome)
            continue
        endereco = enderecos.get(produto.endereco_id) if produto.endereco_id else None
        tipo_area = (getattr(endereco, 'tipo_area', None) or '').strip().lower()
        if not endereco or tipo_area not in tipos_permitidos:
            produtos_sem_picking.append(produto.nome)

    if produtos_vencidos:
        raise BusinessRuleError(
            'Produtos vencidos nao podem ser separados: '
            + ', '.join(dict.fromkeys(produtos_vencidos))
            + '.'
        )
    if produtos_sem_picking:
        raise BusinessRuleError(
            'Os produtos a seguir precisam estar enderecados em areas de picking/expedicao antes da separacao: '
            + ', '.join(dict.fromkeys(produtos_sem_picking))
            + '.'
        )


def _visao_operacional_pedido(pedido, empresa=None):
    empresa = empresa or _obter_empresa_config()
    fila_entrega = _pedido_na_fila_entrega(pedido, empresa)
    possui_rota = bool((pedido.rota_entrega or '').strip())

    if pedido.status == Pedido.STATUS_CANCELADO:
        return {
            'chave': 'cancelado',
            'titulo': 'Cancelado',
            'descricao': 'Pedido fora da fila operacional ativa.',
            'proxima_acao': 'Sem acao operacional. Revise somente estorno, estoque ou registro interno se necessario.',
            'apos_concluir': 'Pedido permanece fora da fila de trabalho.',
        }

    if pedido.status == Pedido.STATUS_FECHADO:
        return {
            'chave': 'concluido',
            'titulo': 'Concluido',
            'descricao': 'Venda encerrada e fora da fila operacional.',
            'proxima_acao': 'Nenhuma acao pendente no pedido.',
            'apos_concluir': 'Fluxo finalizado.',
        }

    if fila_entrega and pedido.saiu_para_entrega_em and not pedido.entrega_concluida_em:
        return {
            'chave': 'em_rota',
            'titulo': 'Em rota',
            'descricao': 'Pedido ja saiu para entrega e aguarda confirmacao final.',
            'proxima_acao': 'Acompanhe o motorista, confirme a entrega e registre ocorrencias se houver.',
            'apos_concluir': 'Marque como entregue e encaminhe para fechamento da venda.',
        }

    if fila_entrega and pedido.entrega_concluida_em:
        return {
            'chave': 'fechamento',
            'titulo': 'Fechamento',
            'descricao': 'Entrega concluida, aguardando encerramento comercial e financeiro.',
            'proxima_acao': 'Conferir comprovantes, baixa financeira e fechar o pedido.',
            'apos_concluir': 'Pedido sai da fila operacional.',
        }

    if fila_entrega and pedido.separacao_entrega_concluida:
        if not possui_rota:
            proxima_acao = 'Defina rota, ordem de parada, local de saida e responsavel pelo transporte.'
        elif not pedido.etiqueta_entrega_emitida_em:
            proxima_acao = 'Emita a etiqueta, confira volumes e deixe o pedido pronto para despacho.'
        else:
            proxima_acao = 'Registre a saida para entrega e encaminhe o pedido ao motorista ou terceirizada.'

        return {
            'chave': 'roteirizacao',
            'titulo': 'Roteirizacao e despacho',
            'descricao': 'Pedido separado e aguardando roteirizacao final ou despacho.',
            'proxima_acao': proxima_acao,
            'apos_concluir': 'Pedido entra em acompanhamento de rota ate a confirmacao da entrega.',
        }

    if fila_entrega and pedido.status == Pedido.STATUS_ENTREGUE:
        return {
            'chave': 'separacao',
            'titulo': 'Separacao',
            'descricao': 'Pedido pronto comercialmente e aguardando separacao fisica.',
            'proxima_acao': 'Separar os itens, revisar quantidades, embalar e marcar o pedido como separado.',
            'apos_concluir': 'Envie para roteirizacao, etiqueta e despacho.',
        }

    if pedido.status == Pedido.STATUS_EM_PREPARO:
        return {
            'chave': 'preparo',
            'titulo': 'Preparo',
            'descricao': 'Pedido em producao, montagem ou conferencia operacional.',
            'proxima_acao': 'Produza, monte ou confira os itens conforme observacoes e disponibilidade.',
            'apos_concluir': (
                'Atualize para entregue e siga para separacao.'
                if fila_entrega
                else 'Entregue ao cliente e siga para fechamento da venda.'
            ),
        }

    if pedido.status == Pedido.STATUS_ABERTO:
        return {
            'chave': 'registro',
            'titulo': 'Registro e conferencia',
            'descricao': 'Pedido recem-lancado e aguardando validacao inicial.',
            'proxima_acao': 'Conferir itens, origem, pagamento e encaminhar para a equipe responsavel.',
            'apos_concluir': 'Mova o pedido para preparo.',
        }

    return {
        'chave': 'fechamento',
        'titulo': 'Fechamento',
        'descricao': 'Pedido aguarda revisao final para sair da fila.',
        'proxima_acao': 'Conferir documentacao, pagamento e concluir o encerramento.',
        'apos_concluir': 'Pedido sai da fila operacional.',
    }


def _acoes_rapidas_pedido(pedido, empresa=None, funcionario=None, paginas_permitidas=None):
    empresa = empresa or _obter_empresa_config()
    fila_entrega = _pedido_na_fila_entrega(pedido, empresa)
    pode_alterar_status = _usuario_tem_acesso_endpoint('alterar_status_pedido', funcionario=funcionario, paginas_permitidas=paginas_permitidas)
    pode_separar = _usuario_tem_acesso_endpoint('atualizar_separacao_entrega_pedido', funcionario=funcionario, paginas_permitidas=paginas_permitidas)
    pode_despachar = _usuario_tem_acesso_endpoint('atualizar_despacho_entrega', funcionario=funcionario, paginas_permitidas=paginas_permitidas)
    pode_ver_separacao = _usuario_tem_acesso_endpoint('listar_separacao_entrega', funcionario=funcionario, paginas_permitidas=paginas_permitidas)
    pode_ver_roteirizacao = _usuario_tem_acesso_endpoint('listar_roteirizacao_entrega', funcionario=funcionario, paginas_permitidas=paginas_permitidas)

    acoes = []

    def adicionar_formulario(tipo, label, valor, classe):
        acoes.append({
            'tipo': tipo,
            'label': label,
            'valor': valor,
            'classe': classe,
        })

    def adicionar_link(label, url, classe='btn-outline-primary'):
        acoes.append({
            'tipo': 'link',
            'label': label,
            'url': url,
            'classe': classe,
        })

    if pedido.status == Pedido.STATUS_ABERTO and pode_alterar_status:
        adicionar_formulario('status', 'Enviar p/ preparo', Pedido.STATUS_EM_PREPARO, 'btn-primary')
    elif pedido.status == Pedido.STATUS_EM_PREPARO and pode_alterar_status:
        adicionar_formulario('status', 'Marcar pronto', Pedido.STATUS_ENTREGUE, 'btn-warning')

    if fila_entrega and pedido.status == Pedido.STATUS_ENTREGUE and not pedido.separacao_entrega_concluida:
        if pode_separar:
            adicionar_formulario('separacao', 'Separado', 'concluir', 'btn-success')
        if pode_ver_separacao:
            adicionar_link('Fila de separacao', url_for('listar_separacao_entrega', busca=str(pedido.id)), 'btn-outline-secondary')
    elif fila_entrega and _pedido_pronto_para_roteirizacao(pedido):
        if not (pedido.rota_entrega or '').strip() or not pedido.etiqueta_entrega_emitida_em:
            if pode_ver_roteirizacao:
                rota_kwargs = {'rota': pedido.rota_entrega} if (pedido.rota_entrega or '').strip() else {}
                adicionar_link('Roteirizar', url_for('listar_roteirizacao_entrega', **rota_kwargs), 'btn-outline-secondary')
        elif not pedido.saiu_para_entrega_em and pode_despachar:
            adicionar_formulario('despacho', 'Saiu p/ entrega', 'sair', 'btn-info')
        elif pedido.saiu_para_entrega_em and not pedido.entrega_concluida_em and pode_despachar:
            adicionar_formulario('despacho', 'Confirmar entrega', 'entregar', 'btn-success')
        elif pedido.entrega_concluida_em and pedido.status == Pedido.STATUS_ENTREGUE and pode_alterar_status:
            adicionar_formulario('status', 'Fechar venda', Pedido.STATUS_FECHADO, 'btn-primary')
    elif pedido.status == Pedido.STATUS_ENTREGUE and pode_alterar_status:
        adicionar_formulario('status', 'Fechar venda', Pedido.STATUS_FECHADO, 'btn-primary')

    adicionar_link('Ver completo', url_for('detalhes_pedido', pedido_id=pedido.id))
    return acoes


def _resumir_filas_operacionais_pedidos(pedidos, empresa=None):
    empresa = empresa or _obter_empresa_config()
    contagens = {
        'registro': 0,
        'preparo': 0,
        'separacao': 0,
        'roteirizacao': 0,
        'em_rota': 0,
        'fechamento': 0,
    }

    for pedido in pedidos:
        fluxo = _visao_operacional_pedido(pedido, empresa)
        if fluxo['chave'] in contagens:
            contagens[fluxo['chave']] += 1

    cards = [
        {
            'chave': 'registro',
            'titulo': 'Registro e conferencia',
            'quantidade': contagens['registro'],
            'descricao': 'Pedidos novos aguardando validacao inicial.',
            'proxima_acao': 'Conferir itens, pagamento, canal e observacoes do pedido.',
            'apos_concluir': 'Enviar para preparo.',
            'url': url_for('listar_pedidos', status='aberto'),
        },
        {
            'chave': 'preparo',
            'titulo': 'Preparo',
            'quantidade': contagens['preparo'],
            'descricao': 'Pedidos em producao, montagem ou conferencia.',
            'proxima_acao': 'Separar internamente a producao e revisar faltas antes de liberar.',
            'apos_concluir': (
                'Atualizar para entregue e seguir para separacao.'
                if _separacao_entrega_ativa(empresa)
                else 'Entregar ao cliente e seguir para fechamento.'
            ),
            'url': url_for('listar_pedidos', status='em_preparo'),
        },
    ]

    if _separacao_entrega_ativa(empresa):
        cards.extend([
            {
                'chave': 'separacao',
                'titulo': 'Separacao',
                'quantidade': contagens['separacao'],
                'descricao': 'Pedidos prontos comercialmente, aguardando separacao fisica.',
                'proxima_acao': 'Separar itens, embalar e validar volumes.',
                'apos_concluir': 'Encaminhar para roteirizacao e despacho.',
                'url': url_for('listar_separacao_entrega', pendente='1'),
            },
            {
                'chave': 'roteirizacao',
                'titulo': 'Roteirizacao e despacho',
                'quantidade': contagens['roteirizacao'],
                'descricao': 'Pedidos separados aguardando rota, etiqueta ou saida.',
                'proxima_acao': 'Definir rota, motorista, etiqueta e expedicao.',
                'apos_concluir': 'Registrar saida para entrega.',
                'url': url_for('listar_roteirizacao_entrega', status_entrega='aguardando'),
            },
            {
                'chave': 'em_rota',
                'titulo': 'Em rota',
                'quantidade': contagens['em_rota'],
                'descricao': 'Pedidos ja despachados e em acompanhamento de entrega.',
                'proxima_acao': 'Monitorar entrega e tratar ocorrencias.',
                'apos_concluir': 'Confirmar entrega e seguir para fechamento.',
                'url': url_for('listar_roteirizacao_entrega', status_entrega='em_rota'),
            },
        ])

    cards.append({
        'chave': 'fechamento',
        'titulo': 'Fechamento',
        'quantidade': contagens['fechamento'],
        'descricao': 'Pedidos aguardando encerramento final da venda.',
        'proxima_acao': 'Conferir comprovantes, pagamento e documentacao.',
        'apos_concluir': 'Retirar o pedido da fila operacional.',
        'url': url_for('listar_pedidos', status='entregue'),
    })

    return cards


def _publicar_evento_expedicao(pedido, acao):
    try:
        publish_alert({
            'tipo': 'expedicao',
            'acao': acao,
            'pedido_id': pedido.id,
            'rota': pedido.rota_entrega,
            'etapa': _resolver_etapa_expedicao(pedido),
            'atualizado_em': datetime.utcnow().isoformat(),
        })
    except Exception:
        pass


def _coletar_progresso_expedicao_diario(empresa):
    agora = datetime.utcnow()
    inicio_dia = datetime(agora.year, agora.month, agora.day)
    fim_dia = inicio_dia + timedelta(days=1)

    pedidos = Pedido.query.filter(
        Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
        Pedido.origem.in_(_origens_separacao_entrega(empresa)),
        Pedido.criado_em >= inicio_dia,
        Pedido.criado_em < fim_dia,
    ).all()

    totais = {
        'separacao': 0,
        'embalagem': 0,
        'expedicao': 0,
        'em_rota': 0,
        'entregue': 0,
    }
    for pedido in pedidos:
        etapa = _resolver_etapa_expedicao(pedido)
        totais[etapa] = totais.get(etapa, 0) + 1

    total_dia = len(pedidos)
    etapas = [
        ('separacao', 'Separacao'),
        ('embalagem', 'Embalagem'),
        ('expedicao', 'Expedicao'),
        ('em_rota', 'Em rota'),
        ('entregue', 'Entregue'),
    ]
    progresso = []
    for chave, label in etapas:
        quantidade = int(totais.get(chave, 0))
        percentual = round((quantidade * 100.0 / total_dia), 1) if total_dia else 0.0
        progresso.append({
            'chave': chave,
            'label': label,
            'quantidade': quantidade,
            'percentual': percentual,
        })

    return {
        'total_dia': total_dia,
        'inicio_dia': inicio_dia.isoformat(),
        'fim_dia': fim_dia.isoformat(),
        'progresso': progresso,
    }


def _coletar_dashboard_expedicao(empresa):
    agora = datetime.utcnow()
    inicio_dia = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_dia = inicio_dia + timedelta(days=1)
    pedidos = Pedido.query.options(
        selectinload(Pedido.caixa),
        selectinload(Pedido.itens).selectinload(ItemPedido.produto),
    ).filter(
        Pedido.origem.in_(_origens_separacao_entrega(empresa)),
        Pedido.criado_em >= inicio_dia,
        Pedido.criado_em < fim_dia,
    ).order_by(Pedido.criado_em.asc()).all()

    pedidos_fluxo = [pedido for pedido in pedidos if pedido.status in DELIVERY_SEPARATION_STATUSES]
    por_hora = {f'{hora:02d}:00': {'separacao': 0, 'embalagem': 0, 'expedicao': 0, 'entregue': 0} for hora in range(24)}
    fila_por_hora = {f'{hora:02d}:00': 0 for hora in range(24)}
    status_rotas = {'em_rota': 0, 'entregues': 0, 'atrasadas': 0}
    tempos_separacao = []
    aderencia_ok = 0
    aderencia_total = 0
    pedidos_separacao = []
    pedidos_rota = []

    for pedido in pedidos_fluxo:
        etapa = _resolver_etapa_expedicao(pedido)
        hora_ref = (pedido.criado_em or inicio_dia).strftime('%H:00')
        if etapa == 'separacao':
            por_hora[hora_ref]['separacao'] += 1
            fila_por_hora[hora_ref] += 1
            espera_min = max((agora - pedido.criado_em).total_seconds() / 60.0, 0.0) if pedido.criado_em else 0.0
            pedidos_separacao.append({
                'id': pedido.id,
                'cliente': pedido.cliente_nome or '-',
                'rota': pedido.rota_entrega or '-',
                'motorista': pedido.motorista_nome or '-',
                'tempo_espera_min': round(espera_min, 1),
            })
        elif etapa == 'embalagem':
            por_hora[hora_ref]['embalagem'] += 1
        elif etapa == 'expedicao':
            por_hora[hora_ref]['expedicao'] += 1
        elif etapa == 'entregue':
            por_hora[hora_ref]['entregue'] += 1

        if pedido.separacao_entrega_em and pedido.criado_em:
            tempos_separacao.append(max((pedido.separacao_entrega_em - pedido.criado_em).total_seconds() / 60.0, 0.0))

        if pedido.saiu_para_entrega_em and not pedido.entrega_concluida_em:
            status_rotas['em_rota'] += 1
            previsao = pedido.saiu_para_entrega_em + timedelta(minutes=90)
            pedidos_rota.append({
                'id': pedido.id,
                'cliente': pedido.cliente_nome or '-',
                'rota': pedido.rota_entrega or '-',
                'motorista': pedido.motorista_nome or '-',
                'previsao_entrega': previsao.strftime('%H:%M'),
            })
        elif pedido.entrega_concluida_em:
            status_rotas['entregues'] += 1
            aderencia_total += 1
            if pedido.saiu_para_entrega_em and (pedido.entrega_concluida_em - pedido.saiu_para_entrega_em) <= timedelta(minutes=90):
                aderencia_ok += 1
        elif pedido.rota_entrega and pedido.separacao_entrega_concluida:
            status_rotas['atrasadas'] += 1

    veiculos_config = _carregar_veiculos_config(empresa)
    veiculos = []
    for item in veiculos_config:
        veiculos.append({
            'nome': item.get('nome') or 'Veiculo',
            'placa': item.get('placa') or '-',
            'tipo': item.get('tipo') or '-',
            'capacidade': item.get('capacidade_pedidos') or '-',
        })

    alertas = []
    pedidos_separacao.sort(key=lambda item: item['tempo_espera_min'], reverse=True)
    pedidos_rota.sort(key=lambda item: item['previsao_entrega'])
    if pedidos_separacao and pedidos_separacao[0]['tempo_espera_min'] > 30:
        alertas.append({
            'nivel': 'warning',
            'titulo': 'Pedidos parados na separacao',
            'descricao': f'O pedido #{pedidos_separacao[0]["id"]} aguarda ha {pedidos_separacao[0]["tempo_espera_min"]:.1f} minutos.',
        })
    corte = _config_corte_roteirizacao(empresa, agora=agora)
    if corte['ativo'] and not corte['janela_aberta']:
        alertas.append({
            'nivel': 'danger',
            'titulo': 'Horario de fechamento da rota atingido',
            'descricao': f'Roteirizacao fechada desde {corte["horario"]}.',
        })
    if any(str(item.get('nome') or '').strip() for item in veiculos_config) and not veiculos:
        alertas.append({
            'nivel': 'info',
            'titulo': 'Frota sem cadastro estruturado',
            'descricao': 'Revise os veiculos configurados para preencher tipo, placa e capacidade.',
        })

    return {
        'kpis': {
            'pedidos_dia_total': len(pedidos_fluxo),
            'separados': sum(1 for pedido in pedidos_fluxo if pedido.separacao_entrega_concluida),
            'embalados': sum(1 for pedido in pedidos_fluxo if pedido.etiqueta_entrega_emitida_em),
            'expedidos': sum(1 for pedido in pedidos_fluxo if pedido.saiu_para_entrega_em),
            'entregues': sum(1 for pedido in pedidos_fluxo if pedido.entrega_concluida_em),
            'tempo_medio_separacao_min': round(sum(tempos_separacao) / len(tempos_separacao), 1) if tempos_separacao else 0.0,
            'aderencia_rota_pct': round((aderencia_ok / aderencia_total) * 100.0, 1) if aderencia_total else 0.0,
        },
        'progresso_por_hora': [
            {
                'hora': hora,
                'separacao': valores['separacao'],
                'embalagem': valores['embalagem'],
                'expedicao': valores['expedicao'],
                'entregue': valores['entregue'],
            }
            for hora, valores in por_hora.items()
        ],
        'fila_separacao_por_hora': [
            {'hora': hora, 'pendentes': qtd}
            for hora, qtd in fila_por_hora.items()
        ],
        'status_rotas': status_rotas,
        'pedidos_separacao': pedidos_separacao[:5],
        'pedidos_rota': pedidos_rota[:5],
        'veiculos': veiculos[:5],
        'alertas': alertas,
    }


def _bloquear_se_atendimento_mesas_desativado():
    if _atendimento_mesas_ativo():
        return None
    flash('Modulo de mesas e garcons esta desativado para esta empresa.', 'warning')
    return redirect(url_for('pdv'))


def _usuario_tem_acesso_endpoint(endpoint, funcionario=None, paginas_permitidas=None):
    if funcionario is None:
        funcionario_id = session.get('funcionario_id')
        if not funcionario_id:
            return False
        funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario or not funcionario.ativo:
        return False
    if funcionario.role == 'admin':
        return True
    if not funcionario.controle_acesso_ativo:
        return True
    pagina = ENDPOINT_TO_PAGINA.get(endpoint)
    if not pagina:
        return True
    if paginas_permitidas is not None:
        return pagina in paginas_permitidas
    return pagina in _paginas_efetivas_funcionario(funcionario)


def _paginas_perfil_acesso_funcionario(funcionario):
    perfil = getattr(funcionario, 'perfil_acesso', None)
    if not perfil or not perfil.permissoes_padrao:
        return set()
    try:
        dados = json.loads(perfil.permissoes_padrao)
    except Exception:
        return set()
    if not isinstance(dados, list):
        return set()
    return {
        pagina
        for pagina in dados
        if isinstance(pagina, str)
    }


def _paginas_efetivas_funcionario(funcionario):
    if not funcionario or not funcionario.ativo:
        return set()
    if funcionario.role == 'admin' or not funcionario.controle_acesso_ativo:
        return set(ENDPOINT_TO_PAGINA.values())

    permitidas = set(_paginas_perfil_acesso_funcionario(funcionario))
    for permissao in PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id).all():
        if permissao.permitido:
            permitidas.add(permissao.pagina)
        else:
            permitidas.discard(permissao.pagina)
    return permitidas


def _estoques_permitidos_ids_base(funcionario=None):
    funcionario = funcionario or _funcionario_logado_vendas()
    if not funcionario or funcionario.role == 'admin' or not getattr(funcionario, 'restricao_estoques_ativa', False):
        return None
    ids = set()
    if getattr(funcionario, 'estoque_principal_id', None):
        ids.add(funcionario.estoque_principal_id)
    for estoque in getattr(funcionario, 'estoques_permitidos', []) or []:
        if getattr(estoque, 'id', None):
            ids.add(estoque.id)
    return ids


def _estoque_contexto_selecionado_id(funcionario=None):
    funcionario = funcionario or _funcionario_logado_vendas()
    valor = session.get('estoque_contexto_id')
    if valor in (None, '', 'all'):
        return None
    try:
        estoque_id = int(valor)
    except (TypeError, ValueError):
        session.pop('estoque_contexto_id', None)
        return None
    ids_base = _estoques_permitidos_ids_base(funcionario)
    if ids_base is not None and estoque_id not in ids_base:
        session.pop('estoque_contexto_id', None)
        return None
    return estoque_id


def _estoques_permitidos_ids(funcionario=None):
    funcionario = funcionario or _funcionario_logado_vendas()
    ids_base = _estoques_permitidos_ids_base(funcionario)
    estoque_contexto_id = _estoque_contexto_selecionado_id(funcionario)
    if estoque_contexto_id:
        return {estoque_contexto_id}
    return ids_base


def _endereco_query_permitida(funcionario=None):
    query = EnderecoEstoque.query
    ids = _estoques_permitidos_ids(funcionario)
    if ids is None:
        return query
    if not ids:
        return query.filter(EnderecoEstoque.id == -1)
    return query.filter(EnderecoEstoque.estoque_id.in_(ids))


def _normalizar_cep_entrega(valor):
    cep = validar_cep((valor or '').strip())
    if not cep or cep == '__invalid__':
        return None
    return cep


def _extrair_cep_pedido(pedido):
    observacoes = {}
    try:
        observacoes = json.loads(pedido.observacoes) if pedido and pedido.observacoes else {}
    except Exception:
        observacoes = {}

    if isinstance(observacoes, dict):
        cliente_cadastro = observacoes.get('cliente_cadastro') or {}
        cep = _normalizar_cep_entrega(cliente_cadastro.get('cep'))
        if cep:
            return cep
        endereco_id = observacoes.get('cliente_endereco_id')
        if endereco_id:
            endereco = ClienteEndereco.query.filter_by(id=endereco_id).first()
            if endereco:
                cep = _normalizar_cep_entrega(endereco.cep)
                if cep:
                    return cep

    cliente_publico = getattr(pedido, 'cliente_publico', None)
    if cliente_publico:
        endereco_principal = getattr(cliente_publico, 'endereco_principal', None)
        if endereco_principal:
            cep = _normalizar_cep_entrega(endereco_principal.cep)
            if cep:
                return cep
        cep = _normalizar_cep_entrega(getattr(cliente_publico, 'cep', None))
        if cep:
            return cep
    return None


def _obter_coordenadas_cep(cep):
    """Resolve coordenadas aproximadas via geocodificacao com cache local."""
    cep_normalizado = _normalizar_cep_entrega(cep)
    if not cep_normalizado:
        return None

    cache = extensions.cache
    cache_key = f'geocode:cep:{cep_normalizado}'
    if cache is not None:
        cached = cache.get(cache_key)
        if cached:
            return tuple(cached)

    query_string = urlencode({
        'postalcode': cep_normalizado,
        'country': 'Brazil',
        'format': 'jsonv2',
        'limit': 1,
    })
    request_obj = Request(
        f'https://nominatim.openstreetmap.org/search?{query_string}',
        headers={'User-Agent': 'SystemLR/1.0'},
    )
    try:
        with urlopen(request_obj, timeout=2.5) as response:
            payload = json.loads(response.read().decode('utf-8'))
        if not payload:
            return None
        coordenadas = (float(payload[0]['lat']), float(payload[0]['lon']))
    except Exception:
        return None

    if cache is not None:
        cache.set(cache_key, coordenadas, timeout=86400)
    return coordenadas


def _distancia_haversine(origem, destino):
    if not origem or not destino:
        return float('inf')
    lat1, lon1 = origem
    lat2, lon2 = destino
    raio_terra_km = 6371.0
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(delta_lon / 2) ** 2
    )
    return raio_terra_km * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def _ordenar_pedidos_por_proximidade(pedidos, cep_origem):
    """Ordena pedidos pelo CEP mais proximo da loja usando Haversine."""
    pedidos_base = list(pedidos or [])
    coordenada_origem = _obter_coordenadas_cep(cep_origem)
    if not coordenada_origem:
        return sorted(pedidos_base, key=lambda item: (item.criado_em or datetime.utcnow(), item.id or 0))

    def _sort_key(pedido):
        coordenada_destino = _obter_coordenadas_cep(_extrair_cep_pedido(pedido))
        sem_coordenada = coordenada_destino is None
        distancia = _distancia_haversine(coordenada_origem, coordenada_destino)
        return (
            1 if sem_coordenada else 0,
            distancia,
            pedido.criado_em or datetime.utcnow(),
            pedido.id or 0,
        )

    return sorted(pedidos_base, key=_sort_key)


def _garcom_logado_id():
    funcionario_id = session.get('funcionario_id')
    if not funcionario_id:
        return None
    garcom = Garcom.query.filter_by(funcionario_id=funcionario_id, ativo=True).first()
    return garcom.id if garcom else None


def _funcionario_logado_vendas():
    funcionario_id = session.get('funcionario_id')
    if not funcionario_id:
        return None
    return Funcionario.query.get(funcionario_id)


def _parse_status(value, default='aberto'):
    status = (value or default).strip().lower()
    return status if status in ORDER_ALLOWED_TRANSITIONS else default


def _http_status_for_order_error(message):
    text = (message or '').lower()
    conflict_terms = (
        'imutavel',
        'transicao',
        'insuficiente',
        'caixa do pedido esta fechada',
        'somente pedidos',
        'ja esta',
        'nao pode ser fechado',
    )
    for term in conflict_terms:
        if term in text:
            return 409, 'business_rule'
    return 400, 'validation_error'


def _aplicar_transicao_status(pedido, novo_status, *, actor=None, detalhes=None, require_delivery_separation=False):
    return service_aplicar_transicao_status(
        pedido,
        novo_status,
        actor=actor,
        detalhes=detalhes,
        require_delivery_separation=require_delivery_separation,
    )


def register_vendas_routes(app, login_required, require_role):
    vendas_operacao_roles = ('admin', 'gerente', 'caixa', 'operador', 'garcom')
    vendas_gestao_roles = ('admin', 'gerente')
    caixa_operacao_roles = ('admin', 'gerente', 'caixa')
    separacao_entrega_roles = ('admin', 'gerente', 'caixa', 'operador')

    @app.route('/expedicao')
    @require_role(*separacao_entrega_roles)
    def central_expedicao():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        progresso = _coletar_progresso_expedicao_diario(empresa)
        dashboard = _coletar_dashboard_expedicao(empresa)
        return render_template(
            'expedicao/central.html',
            empresa=empresa,
            progresso=progresso,
            dashboard=dashboard,
            veiculos_cadastrados=_opcoes_veiculos_cadastrados(empresa),
            terceirizadas_cadastradas=_carregar_lista_config(empresa.entrega_terceirizadas_json),
            etiquetas_ativas=_emissao_etiqueta_entrega_ativa(empresa),
            emissao_nota_ativa=empresa.emissao_nota_entrega_ativa is not False,
        )

    @app.route('/expedicao/frota', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def frota_expedicao():
        empresa = _obter_empresa_config()
        veiculo_edicao = _obter_veiculo_frota(empresa, request.args.get('veiculo_id', type=int))
        if request.method == 'POST':
            acao = (request.form.get('acao') or 'salvar_configuracao').strip().lower()
            try:
                with atomic_transaction(db.session):
                    if acao == 'salvar_configuracao':
                        empresa.entrega_local_saida_padrao = (request.form.get('entrega_local_saida_padrao') or '').strip() or None
                        empresa.entrega_motorista_padrao = (request.form.get('entrega_motorista_padrao') or '').strip() or None
                        empresa.entrega_veiculo_padrao = (request.form.get('entrega_veiculo_padrao') or '').strip() or None
                        horario_fechamento_roteirizacao = _parse_horario_hhmm(request.form.get('entrega_horario_fechamento_roteirizacao'))
                        horario_fechamento_roteirizacao_txt = (request.form.get('entrega_horario_fechamento_roteirizacao') or '').strip()
                        if horario_fechamento_roteirizacao_txt and not horario_fechamento_roteirizacao:
                            raise ValidationError('Horario de fechamento da roteirizacao invalido. Use HH:MM.')
                        empresa.entrega_horario_fechamento_roteirizacao = (
                            horario_fechamento_roteirizacao.strftime('%H:%M')
                            if horario_fechamento_roteirizacao
                            else None
                        )
                        terceirizadas_linhas = _normalizar_linhas_configuracao(request.form.get('entrega_terceirizadas_cadastro', ''))
                        empresa.entrega_terceirizadas_json = json.dumps(terceirizadas_linhas, ensure_ascii=False) if terceirizadas_linhas else None
                        _sincronizar_frota_legada(empresa)
                        mensagem = 'Configuracao operacional da frota atualizada com sucesso.'
                    elif acao == 'salvar_veiculo':
                        if not _frota_relacional_disponivel():
                            raise BusinessRuleError('A tabela de frota ainda nao esta disponivel. Execute a migration antes de cadastrar veiculos.')
                        veiculo_id = request.form.get('veiculo_id', type=int)
                        veiculo = _obter_veiculo_frota(empresa, veiculo_id) if veiculo_id else None
                        if veiculo is None:
                            veiculo = FrotaVeiculo(empresa_id=empresa.id)
                            db.session.add(veiculo)
                        nome = (request.form.get('nome') or '').strip()
                        if not nome:
                            raise ValidationError('Informe o nome do veiculo.')
                        tipo = (request.form.get('tipo') or FrotaVeiculo.TIPO_CARRO).strip().lower()
                        if tipo not in FrotaVeiculo.TIPOS_VALIDOS:
                            raise ValidationError('Tipo de veiculo invalido. Use moto, carro, caminhao ou utilitario.')

                        veiculo.nome = nome
                        veiculo.placa = (request.form.get('placa') or '').strip().upper() or None
                        veiculo.tipo = tipo
                        veiculo.capacidade_kg = _to_float(request.form.get('capacidade_kg'), None)
                        veiculo.capacidade_volume = _to_float(request.form.get('capacidade_volume'), None)
                        veiculo.motorista_padrao = (request.form.get('motorista_padrao') or '').strip() or None
                        veiculo.tipo_entrega = (request.form.get('tipo_entrega') or 'todos').strip().lower() or 'todos'
                        veiculo.capacidade_pedidos = max(int(_to_int(request.form.get('capacidade_pedidos'), 0) or 0), 0)
                        veiculo.empresa_terceirizada = (request.form.get('empresa_terceirizada') or '').strip() or None
                        veiculo.ativo = request.form.get('ativo') == 'on'
                        if not empresa.entrega_veiculo_padrao and veiculo.ativo:
                            empresa.entrega_veiculo_padrao = veiculo.nome
                        _sincronizar_frota_legada(empresa)
                        mensagem = f'Veiculo "{veiculo.nome}" salvo com sucesso.'
                    elif acao == 'excluir_veiculo':
                        if not _frota_relacional_disponivel():
                            raise BusinessRuleError('A tabela de frota ainda nao esta disponivel. Execute a migration antes de excluir veiculos.')
                        veiculo = _obter_veiculo_frota(empresa, request.form.get('veiculo_id', type=int))
                        if not veiculo:
                            raise ValidationError('Veiculo nao encontrado para exclusao.')
                        nome_veiculo = veiculo.nome
                        db.session.delete(veiculo)
                        _sincronizar_frota_legada(empresa)
                        mensagem = f'Veiculo "{nome_veiculo}" removido com sucesso.'
                    else:
                        raise ValidationError('Acao de frota invalida.')
                db.session.commit()
                flash(mensagem, 'success')
            except AppError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar cadastro de frota: {str(e)}', 'error')
            return redirect(url_for('frota_expedicao'))

        terceirizadas_texto = '\n'.join(_carregar_lista_config(empresa.entrega_terceirizadas_json))
        return render_template(
            'expedicao/frota.html',
            empresa=empresa,
            veiculos_frota=_carregar_veiculos_config(empresa),
            veiculo_em_edicao=veiculo_edicao,
            terceirizadas_texto=terceirizadas_texto,
        )

    @app.route('/garcons')
    @require_role(*vendas_gestao_roles)
    def listar_garcons():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        garcons = Garcom.query.order_by(Garcom.nome.asc()).all()
        pedidos_em_andamento = Pedido.query.filter(Pedido.status.in_(['aberto', 'em_preparo', 'entregue'])).order_by(Pedido.criado_em.desc()).all()
        empresa = _obter_empresa_config()
        return render_template(
            'vendas/garcons/garcons.html',
            garcons=garcons,
            pedidos_em_andamento=pedidos_em_andamento,
            empresa=empresa
        )

    @app.route('/garcons/novo', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def novo_garcom():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                celular = (request.form.get('celular') or '').strip()
                ativo = (request.form.get('ativo') == 'on')
                if not nome:
                    flash('Nome do garcom e obrigatorio.', 'error')
                    return redirect(url_for('novo_garcom'))

                garcom = Garcom(nome=nome, celular=celular or None, ativo=ativo)
                db.session.add(garcom)
                db.session.commit()
                flash('Garcom cadastrado com sucesso.', 'success')
                return redirect(url_for('listar_garcons'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar garcom: {str(e)}', 'error')
        return render_template('vendas/garcons/novo_garcom.html')

    @app.route('/garcons/<int:garcom_id>/editar', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def editar_garcom(garcom_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        garcom = Garcom.query.get_or_404(garcom_id)
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                if not nome:
                    flash('Nome do garcom e obrigatorio.', 'error')
                    return redirect(url_for('editar_garcom', garcom_id=garcom_id))
                garcom.nome = nome
                garcom.celular = (request.form.get('celular') or '').strip() or None
                garcom.ativo = (request.form.get('ativo') == 'on')
                db.session.commit()
                flash('Garcom atualizado com sucesso.', 'success')
                return redirect(url_for('listar_garcons'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar garcom: {str(e)}', 'error')
        return render_template('vendas/garcons/editar_garcom.html', garcom=garcom)

    @app.route('/garcons/<int:garcom_id>/deletar', methods=['POST'])
    @require_role(*vendas_gestao_roles)
    def deletar_garcom(garcom_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        garcom = Garcom.query.get_or_404(garcom_id)
        try:
            Pedido.query.filter_by(garcom_id=garcom.id).update({'garcom_id': None})
            db.session.delete(garcom)
            db.session.commit()
            flash('Garcom removido com sucesso.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover garcom: {str(e)}', 'error')
        return redirect(url_for('listar_garcons'))

    @app.route('/garcons/config', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def configurar_distribuicao_garcons():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        empresa = _obter_empresa_config()
        if request.method == 'POST':
            try:
                empresa.distribuicao_ativa = (request.form.get('distribuicao_ativa') == 'on')
                modo = (request.form.get('modo_distribuicao_pedidos') or 'round_robin').strip().lower()
                if modo not in {'round_robin', 'menos_pedidos', 'manual'}:
                    modo = 'round_robin'
                empresa.modo_distribuicao_pedidos = modo
                db.session.commit()
                flash('Configuracao de distribuicao salva com sucesso.', 'success')
                return redirect(url_for('configurar_distribuicao_garcons'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao salvar configuracao: {str(e)}', 'error')
        return render_template('vendas/garcons/config_distribuicao.html', empresa=empresa)

    @app.route('/caixas')
    @require_role(*caixa_operacao_roles)
    def listar_caixas():
        caixas = Caixa.query.all()
        return render_template('vendas/caixas/caixas.html', caixas=caixas)

    @app.route('/caixas/nova', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def nova_caixa():
        if request.method == 'POST':
            try:
                nome = request.form.get('nome')
                saldo = float(request.form.get('saldo_inicial') or 0)
                caixa = Caixa(nome=nome, saldo_inicial=saldo, saldo_atual=saldo)
                db.session.add(caixa)
                db.session.commit()
                flash(f'Caixa "{caixa.nome}" criado com sucesso!', 'success')
                return redirect(url_for('listar_caixas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar caixa: {str(e)}', 'error')
        return render_template('vendas/caixas/nova_caixa.html')

    @app.route('/caixas/<int:caixa_id>/editar', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def editar_caixa(caixa_id):
        caixa = Caixa.query.get_or_404(caixa_id)
        if request.method == 'POST':
            try:
                caixa.nome = request.form.get('nome', caixa.nome)
                caixa.saldo_atual = float(request.form.get('saldo_atual', caixa.saldo_atual))
                aberto = request.form.get('aberto')
                caixa.aberto = bool(aberto == 'on')
                if not caixa.aberto and not caixa.fechado_em:
                    caixa.fechado_em = datetime.utcnow()
                db.session.commit()
                flash(f'Caixa "{caixa.nome}" atualizado com sucesso!', 'success')
                return redirect(url_for('listar_caixas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar caixa: {str(e)}', 'error')
        return render_template('vendas/caixas/editar_caixa.html', caixa=caixa)

    @app.route('/caixas/<int:caixa_id>/deletar', methods=['POST'])
    @require_role(*vendas_gestao_roles)
    def deletar_caixa(caixa_id):
        caixa = Caixa.query.get_or_404(caixa_id)
        try:
            db.session.delete(caixa)
            db.session.commit()
            flash(f'Caixa "{caixa.nome}" deletado.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar caixa: {str(e)}', 'error')
        return redirect(url_for('listar_caixas'))

    @app.route('/caixas/<int:caixa_id>/abrir', methods=['GET', 'POST'])
    @require_role(*caixa_operacao_roles)
    def abrir_caixa(caixa_id):
        """Abre uma caixa e a atribui a um funcionário"""
        caixa = Caixa.query.get_or_404(caixa_id)
        
        # Valida se caixa já está aberta
        if caixa.aberto:
            flash(f'Caixa "{caixa.nome}" já está aberta!', 'warning')
            return redirect(url_for('listar_caixas'))
        
        if request.method == 'POST':
            try:
                funcionario_id = request.form.get('funcionario_id', type=int)
                saldo_inicial = float(request.form.get('saldo_inicial', 0))
                observacoes = request.form.get('observacoes', '')
                
                funcionario = Funcionario.query.get(funcionario_id)
                if not funcionario:
                    flash('Funcionário selecionado não existe!', 'danger')
                    return redirect(url_for('abrir_caixa', caixa_id=caixa_id))
                
                # Abre a caixa
                caixa.funcionario_id = funcionario_id
                caixa.saldo_inicial = saldo_inicial
                caixa.saldo_atual = saldo_inicial
                caixa.aberto = True
                caixa.aberto_em = datetime.utcnow()
                caixa.observacoes = observacoes
                
                # Registra a movimentação de abertura
                mov = MovimentacaoCaixa(
                    caixa_id=caixa.id,
                    tipo=MovimentacaoCaixa.TIPO_ENTRADA,
                    valor=saldo_inicial,
                    descricao=f'Abertura de caixa por {funcionario.nome}'
                )
                db.session.add(mov)
                db.session.commit()
                
                flash(f'Caixa "{caixa.nome}" aberta com sucesso! Atribuída a {funcionario.nome}', 'success')
                return redirect(url_for('listar_caixas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao abrir caixa: {str(e)}', 'error')
        
        funcionarios = Funcionario.query.filter_by(ativo=True).all()
        return render_template('vendas/caixas/abrir_caixa.html', caixa=caixa, funcionarios=funcionarios)

    @app.route('/caixas/<int:caixa_id>/fechar', methods=['GET', 'POST'])
    @require_role(*caixa_operacao_roles)
    def fechar_caixa(caixa_id):
        """Fecha uma caixa com saldo de fechamento"""
        caixa = Caixa.query.get_or_404(caixa_id)
        
        # Valida se caixa está fechada
        if not caixa.aberto:
            flash(f'Caixa "{caixa.nome}" já está fechada!', 'warning')
            return redirect(url_for('listar_caixas'))
        
        if request.method == 'POST':
            try:
                saldo_fechamento = float(request.form.get('saldo_fechamento', 0))
                observacoes = request.form.get('observacoes', '')
                
                # Calcula diferença
                diferenca = saldo_fechamento - caixa.saldo_atual
                
                # Fecha a caixa
                caixa.saldo_fechamento = saldo_fechamento
                caixa.aberto = False
                caixa.fechado_em = datetime.utcnow()
                caixa.observacoes = observacoes
                
                # Registra a movimentação de fechamento
                mov = MovimentacaoCaixa(
                    caixa_id=caixa.id,
                    tipo=MovimentacaoCaixa.TIPO_SAIDA if diferenca < 0 else MovimentacaoCaixa.TIPO_ENTRADA,
                    valor=abs(diferenca),
                    descricao=f'Fechamento de caixa - Diferença: R$ {diferenca:.2f}'
                )
                db.session.add(mov)
                db.session.commit()
                
                msg = f'Caixa "{caixa.nome}" fechada com sucesso!'
                if diferenca != 0:
                    msg += f' Diferença: R$ {diferenca:.2f}'
                flash(msg, 'success')
                return redirect(url_for('listar_caixas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao fechar caixa: {str(e)}', 'error')
        
        return render_template('vendas/caixas/fechar_caixa.html', caixa=caixa)

    @app.route('/caixas/<int:caixa_id>/historico')
    @require_role(*caixa_operacao_roles)
    def historico_caixa(caixa_id):
        """Exibe histórico de movimentações da caixa"""
        caixa = Caixa.query.get_or_404(caixa_id)
        movimentacoes = MovimentacaoCaixa.query.filter_by(caixa_id=caixa_id).order_by(
            MovimentacaoCaixa.criado_em.desc()
        ).all()
        
        return render_template('vendas/caixas/historico_caixa.html', caixa=caixa, movimentacoes=movimentacoes)

    @app.route('/mesas')
    @require_role(*caixa_operacao_roles)
    def listar_mesas():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        mesas = Mesa.query.all()
        # Garante que todas as mesas tenham token para QR Code
        for mesa in mesas:
            if not mesa.qr_token:
                mesa.qr_token = secrets.token_urlsafe(12)
        db.session.commit()
        return render_template('vendas/mesas/mesas.html', mesas=mesas)

    @app.route('/mesas/nova', methods=['GET', 'POST'])
    @require_role(*caixa_operacao_roles)
    def nova_mesa():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        if request.method == 'POST':
            try:
                numero = request.form.get('numero')
                capacidade = int(request.form.get('capacidade') or 1)
                mesa = Mesa(numero=numero, capacidade=capacidade, status='livre', qr_token=secrets.token_urlsafe(12))
                db.session.add(mesa)
                db.session.commit()
                flash(f'Mesa "{mesa.numero}" criada com sucesso!', 'success')
                return redirect(url_for('listar_mesas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar mesa: {str(e)}', 'error')
        return render_template('vendas/mesas/nova_mesa.html')

    @app.route('/mesas/<int:mesa_id>/editar', methods=['GET', 'POST'])
    @require_role(*caixa_operacao_roles)
    def editar_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        mesa = Mesa.query.get_or_404(mesa_id)
        if not mesa.qr_token:
            mesa.qr_token = secrets.token_urlsafe(12)
        if request.method == 'POST':
            try:
                mesa.numero = request.form.get('numero', mesa.numero)
                mesa.capacidade = int(request.form.get('capacidade', mesa.capacidade))
                mesa.status = request.form.get('status', mesa.status)
                db.session.commit()
                flash(f'Mesa "{mesa.numero}" atualizada!', 'success')
                return redirect(url_for('listar_mesas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar mesa: {str(e)}', 'error')
        return render_template('vendas/mesas/editar_mesa.html', mesa=mesa)

    @app.route('/mesas/<int:mesa_id>/deletar', methods=['POST'])
    @require_role(*caixa_operacao_roles)
    def deletar_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        mesa = Mesa.query.get_or_404(mesa_id)
        try:
            db.session.delete(mesa)
            db.session.commit()
            flash(f'Mesa "{mesa.numero}" deletada.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar mesa: {str(e)}', 'error')
        return redirect(url_for('listar_mesas'))

    @app.route('/mesas/<int:mesa_id>/qrcode')
    @require_role(*caixa_operacao_roles)
    def visualizar_qrcode_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        """Exibe o QR code da mesa com opções de impressão e download"""
        mesa = Mesa.query.get_or_404(mesa_id)
        
        # Garante que a mesa tenha token
        if not mesa.qr_token:
            mesa.qr_token = secrets.token_urlsafe(12)
            db.session.commit()
        
        # URL publica da comanda (rota QR)
        qr_url = url_for('public.cardapio_mesa', token=mesa.qr_token, _external=True)
        
        return render_template('vendas/mesas/qrcode_mesa.html', mesa=mesa, qr_url=qr_url)

    @app.route('/mesas/<int:mesa_id>/qrcode/download')
    @require_role(*caixa_operacao_roles)
    def download_qrcode_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        """Faz download da imagem do QR code"""
        mesa = Mesa.query.get_or_404(mesa_id)
        
        if not mesa.qr_token:
            flash('QR code não disponível para esta mesa', 'error')
            return redirect(url_for('listar_mesas'))
        
        try:
            # Gera o QR code com rota publica da comanda
            qr_url = url_for('public.cardapio_mesa', token=mesa.qr_token, _external=True)
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=2,
            )
            qr.add_data(qr_url)
            qr.make(fit=True)
            
            # Cria a imagem em memória
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Salva em bytes
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            
            # Retorna como resposta
            return Response(
                img_io.getvalue(),
                mimetype='image/png',
                headers={"Content-Disposition": f"attachment;filename=qrcode_mesa_{mesa.numero}.png"}
            )
        except Exception as e:
            flash(f'Erro ao gerar QR code: {str(e)}', 'error')
            return redirect(url_for('visualizar_qrcode_mesa', mesa_id=mesa_id))

    @app.route('/mesas/<int:mesa_id>/qrcode/print')
    @require_role(*caixa_operacao_roles)
    def print_qrcode_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        """Exibe o QR code em formato para impressão"""
        mesa = Mesa.query.get_or_404(mesa_id)
        
        if not mesa.qr_token:
            flash('QR code não disponível para esta mesa', 'error')
            return redirect(url_for('listar_mesas'))
        
        qr_url = url_for('public.cardapio_mesa', token=mesa.qr_token, _external=True)
        
        return render_template('vendas/mesas/print_qrcode_mesa.html', mesa=mesa, qr_url=qr_url)

    @app.route('/pedidos')
    @require_role(*vendas_operacao_roles)
    def listar_pedidos():
        empresa = _obter_empresa_config()
        funcionario = Funcionario.query.get(session.get('funcionario_id')) if session.get('funcionario_id') else None
        paginas_permitidas = _paginas_efetivas_funcionario(funcionario)
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        status_filtro = (request.args.get('status') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()

        query = Pedido.query
        if status_filtro in {'aberto', 'em_preparo', 'entregue', 'fechado', 'cancelado'}:
            query = query.filter(Pedido.status == status_filtro)

        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    db.cast(Pedido.id, db.String).ilike(termo),
                    Pedido.cliente_nome.ilike(termo),
                    Pedido.cliente_celular.ilike(termo),
                    Pedido.mesa.has(Mesa.numero.ilike(termo)),
                    Pedido.caixa.has(Caixa.nome.ilike(termo))
                )
            )

        filas_operacionais = _resumir_filas_operacionais_pedidos(
            query.with_entities(
                Pedido.id,
                Pedido.status,
                Pedido.origem,
                Pedido.separacao_entrega_concluida,
                Pedido.etiqueta_entrega_emitida_em,
                Pedido.rota_entrega,
                Pedido.saiu_para_entrega_em,
                Pedido.entrega_concluida_em,
            ).all(),
            empresa=empresa,
        )
        pedidos = (
            query.options(
                load_only(
                    Pedido.id,
                    Pedido.mesa_id,
                    Pedido.caixa_id,
                    Pedido.garcom_id,
                    Pedido.cliente_nome,
                    Pedido.cliente_celular,
                    Pedido.total,
                    Pedido.status,
                    Pedido.origem,
                    Pedido.criado_em,
                    Pedido.separacao_entrega_concluida,
                    Pedido.etiqueta_entrega_emitida_em,
                    Pedido.rota_entrega,
                    Pedido.saiu_para_entrega_em,
                    Pedido.entrega_concluida_em,
                ),
                selectinload(Pedido.mesa).load_only(Mesa.id, Mesa.numero, Mesa.status),
                selectinload(Pedido.caixa).load_only(Caixa.id, Caixa.nome),
                selectinload(Pedido.garcom).load_only(Garcom.id, Garcom.nome, Garcom.ativo),
                selectinload(Pedido.itens).load_only(
                    ItemPedido.id,
                    ItemPedido.pedido_id,
                    ItemPedido.produto_id,
                    ItemPedido.quantidade,
                    ItemPedido.preco_unitario,
                ).selectinload(ItemPedido.produto).load_only(
                    Produto.id,
                    Produto.nome,
                    Produto.codigo,
                ),
            )
            .order_by(Pedido.criado_em.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        for pedido in pedidos.items:
            pedido.fluxo_operacional = _visao_operacional_pedido(pedido, empresa=empresa)
            pedido.acoes_operacionais = _acoes_rapidas_pedido(
                pedido,
                empresa=empresa,
                funcionario=funcionario,
                paginas_permitidas=paginas_permitidas,
            )
        return render_template(
            'vendas/pedidos/pedidos.html',
            pedidos=pedidos.items,
            pagination=pedidos,
            per_page=per_page,
            status_filtro=status_filtro,
            busca=busca,
            query_params=request.args.to_dict(),
            status_transitions=ORDER_ALLOWED_TRANSITIONS,
            empresa=empresa,
            filas_operacionais=filas_operacionais,
        )

    @app.route('/pedidos/separacao-entrega')
    @require_role(*separacao_entrega_roles)
    def listar_separacao_entrega():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        busca = (request.args.get('busca') or '').strip()
        pendente = (request.args.get('pendente') or '1').strip().lower()

        query = Pedido.query.options(
            load_only(
                Pedido.id,
                Pedido.caixa_id,
                Pedido.mesa_id,
                Pedido.cliente_nome,
                Pedido.cliente_celular,
                Pedido.status,
                Pedido.origem,
                Pedido.total,
                Pedido.criado_em,
                Pedido.separacao_entrega_concluida,
                Pedido.separacao_entrega_em,
                Pedido.etiqueta_entrega_emitida_em,
                Pedido.rota_entrega,
                Pedido.motorista_nome,
                Pedido.saiu_para_entrega_em,
                Pedido.entrega_concluida_em,
            ),
            selectinload(Pedido.caixa).load_only(Caixa.id, Caixa.nome),
            selectinload(Pedido.mesa).load_only(Mesa.id, Mesa.numero),
            selectinload(Pedido.itens).load_only(
                ItemPedido.id,
                ItemPedido.pedido_id,
                ItemPedido.produto_id,
                ItemPedido.quantidade,
                ItemPedido.preco_unitario,
            ).selectinload(ItemPedido.produto).load_only(Produto.id, Produto.nome, Produto.codigo),
        ).filter(
            Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
            Pedido.origem.in_(_origens_separacao_entrega(empresa)),
        )

        if pendente == '1':
            query = query.filter(
                db.or_(
                    Pedido.separacao_entrega_concluida.is_(False),
                    Pedido.separacao_entrega_concluida.is_(None),
                )
            )
        elif pendente == '0':
            query = query.filter(Pedido.separacao_entrega_concluida.is_(True))

        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    db.cast(Pedido.id, db.String).ilike(termo),
                    Pedido.cliente_nome.ilike(termo),
                    Pedido.cliente_celular.ilike(termo),
                )
            )

        pagination = query.order_by(Pedido.criado_em.desc()).paginate(page=page, per_page=per_page, error_out=False)
        veiculos_cadastrados = _opcoes_veiculos_cadastrados(empresa)
        terceirizadas_cadastradas = _carregar_lista_config(empresa.entrega_terceirizadas_json)
        return render_template(
            'vendas/pedidos/separacao_entrega.html',
            pedidos=pagination.items,
            pagination=pagination,
            per_page=per_page,
            busca=busca,
            pendente=pendente,
            query_params=request.args.to_dict(),
            empresa=empresa,
            etiquetas_ativas=_emissao_etiqueta_entrega_ativa(empresa),
            roteirizacao_ativa=empresa.roteirizacao_entrega_ativa is not False,
            emissao_nota_ativa=empresa.emissao_nota_entrega_ativa is not False,
            veiculos_cadastrados=veiculos_cadastrados,
            terceirizadas_cadastradas=terceirizadas_cadastradas,
        )

    @app.route('/estoque/coletor')
    @require_role(*separacao_entrega_roles)
    def coletor_estoque():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        busca = (request.args.get('busca') or '').strip()
        etapa = (request.args.get('etapa') or 'todos').strip().lower()

        query = Pedido.query.options(
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
            selectinload(Pedido.caixa),
            selectinload(Pedido.mesa),
        ).filter(
            Pedido.origem.in_(_origens_separacao_entrega(empresa)),
            Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
        )

        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    db.cast(Pedido.id, db.String).ilike(termo),
                    Pedido.cliente_nome.ilike(termo),
                    Pedido.cliente_celular.ilike(termo),
                    Pedido.rota_entrega.ilike(termo),
                )
            )

        pedidos = query.order_by(
            db.case((Pedido.separacao_entrega_concluida.is_(False), 0), else_=1),
            Pedido.criado_em.asc(),
        ).all()

        cards = []
        for pedido in pedidos:
            if not pedido.separacao_entrega_concluida:
                etapa_atual = 'separacao'
            elif not pedido.etiqueta_entrega_emitida_em:
                etapa_atual = 'embalagem'
            elif not pedido.saiu_para_entrega_em:
                etapa_atual = 'expedicao'
            elif not pedido.entrega_concluida_em:
                etapa_atual = 'em_rota'
            else:
                etapa_atual = 'concluido'

            if etapa != 'todos' and etapa != etapa_atual:
                continue

            cards.append({
                'pedido': pedido,
                'etapa_atual': etapa_atual,
            })

        return render_template(
            'estoque/coletor.html',
            cards=cards,
            empresa=empresa,
            busca=busca,
            etapa=etapa,
            etiquetas_ativas=_emissao_etiqueta_entrega_ativa(empresa),
        )

    @app.route('/pedidos/expedicao/iniciar', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def iniciar_processo_expedicao():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))
        session['expedicao_iniciada_em'] = datetime.utcnow().isoformat()
        flash('Processo de expedicao iniciado para monitoramento diario.', 'success')
        return redirect(url_for('painel_expedicao'))

    @app.route('/pedidos/expedicao/painel')
    @require_role(*vendas_operacao_roles)
    def painel_expedicao():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        progresso = _coletar_progresso_expedicao_diario(empresa)
        iniciado_em = session.get('expedicao_iniciada_em')
        return render_template(
            'vendas/pedidos/painel_expedicao.html',
            empresa=empresa,
            progresso=progresso,
            iniciado_em=iniciado_em,
        )

    @app.route('/api/pedidos/expedicao/progresso')
    @require_role(*vendas_operacao_roles)
    def api_progresso_expedicao():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            return jsonify({'success': False, 'message': 'Separacao de entrega desativada.'}), 409

        data = _coletar_progresso_expedicao_diario(empresa)
        data['iniciado_em'] = session.get('expedicao_iniciada_em')
        return jsonify({'success': True, 'data': data})

    @app.route('/api/expedicao/analytics')
    @require_role(*vendas_operacao_roles)
    def analytics_expedicao_api():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            return jsonify({'success': False, 'message': 'Separacao de entrega desativada.'}), 409
        cache = extensions.cache
        cache_key = f'analytics:expedicao:{datetime.utcnow().strftime("%Y%m%d")}'
        if cache is not None:
            cached_payload = cache.get(cache_key)
            if cached_payload is not None:
                return jsonify(cached_payload)
        payload = {
            'success': True,
            'message': 'Analytics de expedicao carregado com sucesso.',
            'data': _coletar_dashboard_expedicao(empresa),
        }
        if cache is not None:
            cache.set(cache_key, payload, timeout=60)
        return jsonify(payload)

    @app.route('/pedidos/roteirizacao-entrega')
    @require_role(*separacao_entrega_roles)
    def listar_roteirizacao_entrega():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        rota_filtro = (request.args.get('rota') or '').strip()
        status_filtro = (request.args.get('status_entrega') or 'todos').strip().lower()

        query = Pedido.query.options(
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
            selectinload(Pedido.caixa),
        ).filter(
            Pedido.origem.in_(_origens_separacao_entrega(empresa)),
            Pedido.separacao_entrega_concluida.is_(True),
        )

        if rota_filtro:
            query = query.filter(Pedido.rota_entrega == rota_filtro)

        if status_filtro == 'aguardando':
            query = query.filter(Pedido.saiu_para_entrega_em.is_(None))
        elif status_filtro == 'em_rota':
            query = query.filter(
                Pedido.saiu_para_entrega_em.is_not(None),
                Pedido.entrega_concluida_em.is_(None)
            )
        elif status_filtro == 'entregue':
            query = query.filter(Pedido.entrega_concluida_em.is_not(None))

        pedidos_base = query.order_by(
            db.case((Pedido.rota_entrega.is_(None), 1), else_=0),
            Pedido.rota_entrega.asc(),
            db.case((Pedido.ordem_rota.is_(None), 1), else_=0),
            Pedido.ordem_rota.asc(),
            Pedido.criado_em.asc(),
        ).all()
        pedidos, pedidos_proximo_ciclo, corte_roteirizacao = _separar_pedidos_por_corte_roteirizacao(
            pedidos_base,
            empresa,
        )

        rotas_disponiveis = (
            db.session.query(Pedido.rota_entrega)
            .filter(Pedido.rota_entrega.is_not(None), Pedido.rota_entrega != '')
            .distinct()
            .order_by(Pedido.rota_entrega.asc())
            .all()
        )
        rotas_disponiveis = [r[0] for r in rotas_disponiveis if r and r[0]]
        regras_roteirizacao = _carregar_regras_roteirizacao(empresa)
        veiculos_configurados = _carregar_veiculos_config(empresa)
        resumo_roteirizacao = {
            'total_pedidos': len(pedidos),
            'aguardando': 0,
            'em_rota': 0,
            'entregue': 0,
            'sem_rota': 0,
            'proximo_ciclo': len(pedidos_proximo_ciclo),
            'rotas_ativas': len({(pedido.rota_entrega or '').strip() for pedido in pedidos if (pedido.rota_entrega or '').strip()}),
            'veiculos_configurados': len(veiculos_configurados),
        }
        for pedido in pedidos:
            if pedido.entrega_concluida_em:
                resumo_roteirizacao['entregue'] += 1
            elif pedido.saiu_para_entrega_em:
                resumo_roteirizacao['em_rota'] += 1
            else:
                resumo_roteirizacao['aguardando'] += 1

            if not (pedido.rota_entrega or '').strip():
                resumo_roteirizacao['sem_rota'] += 1

        return render_template(
            'vendas/pedidos/roteirizacao_entrega.html',
            pedidos=pedidos,
            empresa=empresa,
            rota_filtro=rota_filtro,
            status_filtro=status_filtro,
            rotas_disponiveis=rotas_disponiveis,
            regras_roteirizacao=regras_roteirizacao,
            veiculos_configurados=veiculos_configurados,
            resumo_roteirizacao=resumo_roteirizacao,
            pedidos_proximo_ciclo=pedidos_proximo_ciclo,
            corte_roteirizacao=corte_roteirizacao,
        )

    @app.route('/pedidos/roteirizacao-entrega/otimizar', methods=['POST'])
    @require_role(*separacao_entrega_roles)
    def otimizar_rota_entrega():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        acao_otimizacao = (request.form.get('acao_otimizacao') or 'ordem').strip().lower()
        regras_roteirizacao = _regras_roteirizacao_do_form(request, empresa)
        empresa.entrega_regras_roteirizacao_json = json.dumps(regras_roteirizacao, ensure_ascii=False)

        try:
            if acao_otimizacao == 'distribuir_automatico':
                pedidos_base = Pedido.query.filter(
                    Pedido.origem.in_(_origens_separacao_entrega(empresa)),
                    Pedido.separacao_entrega_concluida.is_(True),
                    Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
                ).order_by(Pedido.criado_em.asc()).all()
                pedidos_disponiveis, pedidos_proximo_ciclo, corte_roteirizacao = _separar_pedidos_por_corte_roteirizacao(
                    pedidos_base,
                    empresa,
                )
                if not pedidos_disponiveis:
                    if corte_roteirizacao['ativo'] and pedidos_proximo_ciclo:
                        flash(
                            f'Nenhum pedido liberado para o ciclo atual. {len(pedidos_proximo_ciclo)} pedido(s) ficaram para o proximo ciclo apos o corte das {corte_roteirizacao["horario"]}.',
                            'warning',
                        )
                    else:
                        flash('Nenhum pedido disponivel para roteirizacao automatica.', 'warning')
                    return redirect(url_for('listar_roteirizacao_entrega'))
                veiculos = _carregar_veiculos_config(empresa)
                total_alocados = _distribuir_pedidos_automaticamente(
                    pedidos_disponiveis,
                    veiculos,
                    regras_roteirizacao,
                    empresa,
                )
                db.session.commit()
                flash(f'Distribuicao automatica concluida com {total_alocados} pedido(s) roteirizado(s).', 'success')
                if corte_roteirizacao['ativo'] and pedidos_proximo_ciclo:
                    flash(
                        f'{len(pedidos_proximo_ciclo)} pedido(s) ficaram fora do ciclo atual por ultrapassarem o horario de fechamento das {corte_roteirizacao["horario"]}.',
                        'info',
                    )
                return redirect(url_for('listar_roteirizacao_entrega'))

            rota = (request.form.get('rota') or '').strip()
            if not rota:
                db.session.rollback()
                flash('Informe a rota para otimizar a sequencia.', 'warning')
                return redirect(url_for('listar_roteirizacao_entrega'))

            pedidos_rota = Pedido.query.filter(
                Pedido.rota_entrega == rota,
                Pedido.separacao_entrega_concluida.is_(True),
                Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
            ).order_by(Pedido.ordem_rota.asc().nullslast(), Pedido.criado_em.asc()).all()

            ordem = 1
            for pedido in pedidos_rota:
                pedido.ordem_rota = ordem
                ordem += 1

            db.session.commit()
            flash(f'Rota "{rota}" otimizada com {len(pedidos_rota)} paradas.', 'success')
            return redirect(url_for('listar_roteirizacao_entrega', rota=rota))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao otimizar rota: {str(e)}', 'error')

        return redirect(url_for('listar_roteirizacao_entrega'))

    @app.route('/pedidos/<int:pedido_id>/despacho-entrega', methods=['POST'])
    @require_role(*separacao_entrega_roles)
    def atualizar_despacho_entrega(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        empresa = _obter_empresa_config()
        if not _pedido_pronto_para_roteirizacao(pedido):
            flash('Pedido nao esta pronto para despacho de entrega.', 'warning')
            return redirect(url_for('listar_roteirizacao_entrega'))

        acao = (request.form.get('acao') or '').strip().lower()
        try:
            if acao == 'sair':
                if not pedido.motorista_nome:
                    pedido.motorista_nome = empresa.entrega_motorista_padrao
                transition_expedicao_status(
                    pedido,
                    ExpedicaoStatus.EM_ROTA,
                    actor=_funcionario_logado_vendas(),
                    enabled=_separacao_entrega_ativa(empresa),
                    allowed_origins=_origens_separacao_entrega(empresa),
                    detalhes='Despacho de saida para entrega.',
                )
                flash(f'Pedido #{pedido.id} marcado como saiu para entrega.', 'success')
            elif acao == 'entregar':
                transition_expedicao_status(
                    pedido,
                    ExpedicaoStatus.ENTREGUE,
                    actor=_funcionario_logado_vendas(),
                    enabled=_separacao_entrega_ativa(empresa),
                    allowed_origins=_origens_separacao_entrega(empresa),
                    detalhes='Entrega confirmada na expedicao.',
                )
                flash(f'Pedido #{pedido.id} marcado como entregue.', 'success')
            elif acao == 'reabrir':
                transition_expedicao_status(
                    pedido,
                    ExpedicaoStatus.SEPARADO,
                    actor=_funcionario_logado_vendas(),
                    enabled=_separacao_entrega_ativa(empresa),
                    allowed_origins=_origens_separacao_entrega(empresa),
                    detalhes='Reabertura do despacho para nova expedicao.',
                )
                flash(f'Pedido #{pedido.id} retornou para aguardando despacho.', 'success')
            else:
                flash('Acao de despacho invalida.', 'warning')
                return redirect(url_for('listar_roteirizacao_entrega'))

            db.session.commit()
            _publicar_evento_expedicao(pedido, f'despacho_{acao}')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar despacho: {str(e)}', 'error')

        return redirect(url_for('listar_roteirizacao_entrega', rota=(pedido.rota_entrega or '')))

    @app.route('/pedidos/<int:pedido_id>/separacao-entrega', methods=['POST'])
    @require_role(*separacao_entrega_roles)
    def atualizar_separacao_entrega_pedido(pedido_id):
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(request.referrer or url_for('listar_pedidos'))

        pedido = Pedido.query.options(
            selectinload(Pedido.itens).selectinload(ItemPedido.produto).selectinload(Produto.endereco),
        ).get_or_404(pedido_id)
        if pedido.origem not in _origens_separacao_entrega(empresa):
            flash('Pedido fora da fila configurada para separacao de entrega.', 'warning')
            return redirect(request.referrer or url_for('listar_separacao_entrega'))

        acao = (request.form.get('acao') or 'concluir').strip().lower()
        actor = _funcionario_logado_vendas()
        try:
            with atomic_transaction(db.session):
                if acao == 'reabrir':
                    transition_expedicao_status(
                        pedido,
                        ExpedicaoStatus.PENDENTE_SEPARACAO,
                        actor=actor,
                        enabled=_separacao_entrega_ativa(empresa),
                        allowed_origins=_origens_separacao_entrega(empresa),
                        detalhes='Reabertura da separacao de entrega.',
                    )
                    mensagem = f'Pedido #{pedido.id} retornou para fila de separacao.'
                else:
                    _validar_pedido_para_separacao(pedido, actor)
                    rota_entrega = (request.form.get('rota_entrega') or '').strip() or None
                    ordem_rota = _to_int(request.form.get('ordem_rota'), None)
                    local_saida = (request.form.get('local_saida') or '').strip() or None
                    veiculo_tipo = (request.form.get('veiculo_tipo') or '').strip() or None
                    veiculo_placa = (request.form.get('veiculo_placa') or '').strip().upper() or None
                    motorista_nome = (request.form.get('motorista_nome') or '').strip() or None
                    empresa_terceirizada = (request.form.get('empresa_terceirizada') or '').strip() or None
                    nota_fiscal_numero = (request.form.get('nota_fiscal_numero') or '').strip() or None
                    nota_fiscal_chave = (request.form.get('nota_fiscal_chave') or '').strip() or None
                    emitir_nota = (request.form.get('emitir_nota') == 'on')

                    veiculo_cadastrado = _obter_veiculo_frota(empresa, request.form.get('veiculo_cadastrado_id', type=int))
                    if veiculo_cadastrado:
                        veiculo_tipo = veiculo_cadastrado.nome or veiculo_tipo
                        veiculo_placa = veiculo_placa or veiculo_cadastrado.placa
                        motorista_nome = motorista_nome or veiculo_cadastrado.motorista_padrao
                        empresa_terceirizada = empresa_terceirizada or veiculo_cadastrado.empresa_terceirizada
                    else:
                        veiculo_cadastrado_legacy = (request.form.get('veiculo_cadastrado') or '').strip()
                        if veiculo_cadastrado_legacy:
                            nome_veiculo_cfg, placa_veiculo_cfg = _parse_veiculo_cadastrado(veiculo_cadastrado_legacy)
                            if nome_veiculo_cfg:
                                veiculo_tipo = nome_veiculo_cfg
                            if placa_veiculo_cfg and not veiculo_placa:
                                veiculo_placa = placa_veiculo_cfg

                    transition_expedicao_status(
                        pedido,
                        ExpedicaoStatus.SEPARADO,
                        actor=actor,
                        enabled=_separacao_entrega_ativa(empresa),
                        allowed_origins=_origens_separacao_entrega(empresa),
                        detalhes='Separacao de entrega concluida.',
                        metadata={
                            'rota_entrega': rota_entrega,
                            'ordem_rota': ordem_rota,
                            'local_saida': local_saida or empresa.entrega_local_saida_padrao,
                            'veiculo_tipo': veiculo_tipo or empresa.entrega_veiculo_padrao,
                            'veiculo_placa': veiculo_placa,
                            'motorista_nome': motorista_nome or empresa.entrega_motorista_padrao,
                            'empresa_terceirizada': empresa_terceirizada,
                            'nota_fiscal_numero': nota_fiscal_numero,
                            'nota_fiscal_chave': nota_fiscal_chave,
                            'nota_fiscal_emitida': bool(emitir_nota and empresa.emissao_nota_entrega_ativa is not False),
                        },
                    )
                    mensagem = f'Pedido #{pedido.id} marcado como separado.'
                    corte_roteirizacao = _config_corte_roteirizacao(empresa)
                    referencia_roteirizacao = _referencia_pedido_roteirizacao(pedido)
                    if (
                        corte_roteirizacao['ativo']
                        and referencia_roteirizacao
                        and referencia_roteirizacao > corte_roteirizacao['corte_do_dia']
                    ):
                        mensagem += f' Ficara disponivel para o proximo ciclo de roteirizacao apos o corte das {corte_roteirizacao["horario"]}.'
            db.session.commit()
            _publicar_evento_expedicao(pedido, f'separacao_{acao}')
            flash(mensagem, 'success')
        except AppError as e:
            db.session.rollback()
            flash(str(e), 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar separacao de entrega: {str(e)}', 'error')
        return redirect(request.referrer or url_for('listar_separacao_entrega'))

    @app.route('/pedidos/<int:pedido_id>/etiqueta-entrega')
    @require_role(*separacao_entrega_roles)
    def imprimir_etiqueta_entrega_pedido(pedido_id):
        empresa = _obter_empresa_config()
        if not _emissao_etiqueta_entrega_ativa(empresa):
            flash('Emissao de etiquetas de entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(request.referrer or url_for('listar_pedidos'))

        pedido = Pedido.query.options(
            selectinload(Pedido.caixa),
            selectinload(Pedido.mesa),
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
        ).get_or_404(pedido_id)
        if pedido.origem not in _origens_separacao_entrega(empresa):
            flash('Pedido fora da fila configurada para etiquetas de entrega.', 'warning')
            return redirect(request.referrer or url_for('listar_pedidos'))

        try:
            pedido.marcar_etiqueta_entrega_emitida()
            db.session.commit()
            _publicar_evento_expedicao(pedido, 'etiqueta_emitida')
        except Exception:
            db.session.rollback()

        return render_template(
            'vendas/pedidos/etiqueta_entrega.html',
            pedido=pedido,
            empresa=empresa,
        )

    @app.route('/pedidos/etiquetas-entrega/lote')
    @require_role(*separacao_entrega_roles)
    def imprimir_etiquetas_entrega_lote():
        empresa = _obter_empresa_config()
        if not _emissao_etiqueta_entrega_ativa(empresa):
            flash('Emissao de etiquetas de entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(request.referrer or url_for('listar_pedidos'))

        ids_brutos = (request.args.get('ids') or '').strip()
        ids = []
        for valor in ids_brutos.split(','):
            valor = valor.strip()
            if not valor or not valor.isdigit():
                continue
            pedido_id = int(valor)
            if pedido_id not in ids:
                ids.append(pedido_id)

        if not ids:
            flash('Nenhum pedido valido foi informado para impressao das etiquetas.', 'warning')
            return redirect(request.referrer or url_for('listar_separacao_entrega'))

        pedidos_base = Pedido.query.options(
            selectinload(Pedido.caixa),
            selectinload(Pedido.mesa),
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
        ).filter(
            Pedido.id.in_(ids),
            Pedido.origem.in_(_origens_separacao_entrega(empresa)),
            Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
        ).all()

        pedidos_por_id = {pedido.id: pedido for pedido in pedidos_base}
        pedidos = [pedidos_por_id[pedido_id] for pedido_id in ids if pedido_id in pedidos_por_id]

        if not pedidos:
            flash('Nenhum pedido da fila de separacao foi encontrado para impressao.', 'warning')
            return redirect(request.referrer or url_for('listar_separacao_entrega'))

        try:
            for pedido in pedidos:
                pedido.marcar_etiqueta_entrega_emitida()
            db.session.commit()
            for pedido in pedidos:
                _publicar_evento_expedicao(pedido, 'etiqueta_emitida_lote')
        except Exception:
            db.session.rollback()

        return render_template(
            'vendas/pedidos/etiquetas_entrega_lote.html',
            pedidos=pedidos,
            empresa=empresa,
        )

    @app.route('/pedidos/pendentes')
    @require_role(*vendas_operacao_roles)
    def listar_pedidos_pendentes():
        pendentes = Pedido.query.filter(Pedido.status.in_(['aberto', 'em_preparo'])).order_by(Pedido.criado_em.desc()).all()
        data = [
            {
                'id': p.id,
                'mesa': p.mesa.numero if p.mesa else None,
                'status': p.status,
                'total': p.total,
                'criado_em': p.criado_em.isoformat()
            } for p in pendentes
        ]
        return jsonify(data)

    @app.route('/pedidos/<int:pedido_id>/status', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def alterar_status_pedido(pedido_id):
        novo_status = _parse_status(request.form.get('status'), default='')
        if not novo_status:
            flash('Status invalido.', 'danger')
            return redirect(url_for('listar_pedidos'))

        pedido = Pedido.query.get_or_404(pedido_id)
        try:
            detalhes = None
            if novo_status == Pedido.STATUS_CANCELADO:
                detalhes = require_cancel_reason(request.form.get('motivo_cancelamento'), entity_label='pedido')
            _aplicar_transicao_status(
                pedido,
                novo_status,
                actor=_funcionario_logado_vendas(),
                detalhes=detalhes,
                require_delivery_separation=_pedido_na_fila_entrega(pedido, _obter_empresa_config()),
            )
            db.session.commit()
            status_label = 'venda concluida' if novo_status == 'fechado' else novo_status
            flash(f'Pedido {pedido.id} atualizado para {status_label}.', 'success')
        except AppError as exc:
            db.session.rollback()
            flash(str(exc), 'danger')

        return redirect(request.referrer or url_for('listar_pedidos'))

    @app.route('/pedidos/novo', methods=['GET', 'POST'])
    @require_role(*vendas_operacao_roles)
    def novo_pedido():
        produtos = Produto.query.filter(Produto.ativo.is_(True), Produto.filtro_nao_vencidos()).all()
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        mesas = Mesa.query.all() if atendimento_mesas_ativo else []
        caixas = Caixa.query.filter_by(aberto=True).all()
        if request.method == 'POST':
            try:
                mesa_id = request.form.get('mesa_id', type=int) or None
                if not atendimento_mesas_ativo:
                    mesa_id = None
                caixa_id = request.form.get('caixa_id', type=int) or None
                observacoes = request.form.get('observacoes')

                caixa = Caixa.query.get(caixa_id) if caixa_id else None
                mesa = Mesa.query.get(mesa_id) if atendimento_mesas_ativo and mesa_id else None
                itens_payload = [
                    {
                        'produto_id': request.form.get(f'produto_{i}'),
                        'quantidade': request.form.get(f'quantidade_{i}', 1),
                    }
                    for i in range(int(request.form.get('item_count', 0)))
                ]

                pedido = service_create_order(
                    caixa=caixa,
                    itens_payload=itens_payload,
                    mesa=mesa,
                    garcom_id=_garcom_logado_id(),
                    atendimento_mesas_ativo=atendimento_mesas_ativo,
                    normalizar_item_payload=_normalizar_item_payload,
                    actor=_funcionario_logado_vendas(),
                )
                pedido.observacoes = observacoes
                db.session.commit()
                flash('Pedido criado com sucesso!', 'success')
                return redirect(url_for('listar_pedidos'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar pedido: {str(e)}', 'error')
        return render_template(
            'vendas/pedidos/novo_pedido.html',
            produtos=produtos,
            mesas=mesas,
            caixas=caixas,
            atendimento_mesas_ativo=atendimento_mesas_ativo
        )

    @app.route('/pedidos/<int:pedido_id>/editar', methods=['GET', 'POST'])
    @require_role(*vendas_operacao_roles)
    def editar_pedido(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        if _parse_status(pedido.status) in ORDER_IMMUTABLE_STATUSES and request.method == 'POST':
            flash('Pedido finalizado/cancelado nao pode ser editado.', 'danger')
            return redirect(url_for('listar_pedidos'))
        produtos = Produto.query.filter(Produto.ativo.is_(True), Produto.filtro_nao_vencidos()).all()
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        mesas = Mesa.query.all() if atendimento_mesas_ativo else []
        caixas = Caixa.query.all()
        empresa = _obter_empresa_config()
        metodos_pagamento_pdv = load_payment_options(empresa.pagamentos_pdv_json, 'pdv')
        metodos_pagamento_pdv_map = payment_methods_map(empresa.pagamentos_pdv_json, 'pdv')
        if request.method == 'POST':
            try:
                actor = _funcionario_logado_vendas()
                status_atual = _parse_status(pedido.status)
                novo_status = _parse_status(request.form.get('status', pedido.status), default=status_atual)
                caixa_id = request.form.get('caixa_id', type=int) or None
                caixa = Caixa.query.get(caixa_id) if caixa_id else None
                if caixa_id and not caixa:
                    raise ValueError('Caixa informada nao existe.')
                mesa_id = request.form.get('mesa_id', type=int) or None
                mesa = Mesa.query.get(mesa_id) if atendimento_mesas_ativo and mesa_id else None

                itens_payload = [
                    {
                        'produto_id': request.form.get(f'produto_{i}'),
                        'quantidade': request.form.get(f'quantidade_{i}', 1),
                    }
                    for i in range(int(request.form.get('item_count', 0)))
                ]

                metodo = request.form.get('metodo_pagamento')
                if metodo:
                    metodo_texto, valor_pago = _build_payment_data(
                        metodo_raw=metodo,
                        valor_raw=request.form.get('valor_pago'),
                        total_pedido=pedido.total,
                        payment_methods=metodos_pagamento_pdv_map,
                        split_raw={
                            'dinheiro': request.form.get('valor_dinheiro'),
                            'cartao': request.form.get('valor_cartao')
                        },
                        cliente_crediario=request.form.get('cliente_crediario', '')
                    )
                    pedido.metodo_pagamento = metodo_texto
                    pedido.valor_pago = valor_pago
                else:
                    pedido.metodo_pagamento = None
                    pedido.valor_pago = None

                detalhes = None
                if novo_status == Pedido.STATUS_CANCELADO:
                    detalhes = require_cancel_reason(request.form.get('motivo_cancelamento'), entity_label='pedido')
                if novo_status == Pedido.STATUS_FECHADO:
                    service_update_order(
                        pedido,
                        novo_status=status_atual,
                        caixa=caixa,
                        mesa=mesa,
                        atendimento_mesas_ativo=atendimento_mesas_ativo,
                        observacoes=request.form.get('observacoes', pedido.observacoes),
                        itens_payload=itens_payload,
                        metodo_pagamento=pedido.metodo_pagamento,
                        valor_pago=pedido.valor_pago,
                        actor=actor,
                        detalhes=detalhes,
                        require_delivery_separation=_pedido_na_fila_entrega(pedido, empresa),
                        normalizar_item_payload=_normalizar_item_payload,
                        status_transition=_aplicar_transicao_status,
                    )
                    venda_service.processar_venda_rapida(
                        pedido,
                        metodo_pagamento=pedido.metodo_pagamento,
                        valor_pago=pedido.valor_pago,
                        desconto_total=request.form.get('desconto_total') or 0.0,
                        incluir_contabilidade=(request.form.get('incluir_contabilidade') == 'on'),
                        actor=actor,
                        commit=False,
                    )
                else:
                    service_update_order(
                        pedido,
                        novo_status=novo_status,
                        caixa=caixa,
                        mesa=mesa,
                        atendimento_mesas_ativo=atendimento_mesas_ativo,
                        observacoes=request.form.get('observacoes', pedido.observacoes),
                        itens_payload=itens_payload,
                        metodo_pagamento=pedido.metodo_pagamento,
                        valor_pago=pedido.valor_pago,
                        actor=actor,
                        detalhes=detalhes,
                        require_delivery_separation=_pedido_na_fila_entrega(pedido, empresa),
                        normalizar_item_payload=_normalizar_item_payload,
                        status_transition=_aplicar_transicao_status,
                    )
                db.session.commit()
                flash('Pedido atualizado com sucesso!', 'success')
                return redirect(url_for('listar_pedidos'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar pedido: {str(e)}', 'error')
        return render_template(
            'vendas/pedidos/editar_pedido.html',
            pedido=pedido,
            produtos=produtos,
            mesas=mesas,
            caixas=caixas,
            atendimento_mesas_ativo=atendimento_mesas_ativo,
            metodos_pagamento_pdv=metodos_pagamento_pdv,
            metodo_pagamento_atual_id=infer_payment_method_id(pedido.metodo_pagamento, metodos_pagamento_pdv),
        )

    @app.route('/pedidos/<int:pedido_id>/deletar', methods=['POST'])
    @require_role(*vendas_gestao_roles)
    def deletar_pedido(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        try:
            db.session.delete(pedido)
            db.session.commit()
            flash('Pedido excluido.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao excluir pedido: {str(e)}', 'error')
        return redirect(url_for('listar_pedidos'))

    @app.route('/pedidos/<int:pedido_id>/comprovante')
    @require_role(*vendas_operacao_roles)
    def visualizar_comprovante_pedido(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        empresa = EmpresaConfig.query.first()
        troco_repassado = None
        if pedido.valor_pago is not None:
            metodo = (pedido.metodo_pagamento or '').strip().lower()
            if 'dinheiro' in metodo or 'dividido' in metodo:
                troco_repassado = max(float(pedido.valor_pago or 0.0) - float(pedido.total or 0.0), 0.0)
            else:
                troco_repassado = 0.0
        return render_template(
            'vendas/pedidos/comprovante.html',
            pedido=pedido,
            empresa=empresa,
            troco_repassado=troco_repassado,
        )

    @app.route('/pedidos/<int:pedido_id>/detalhes')
    @require_role(*vendas_operacao_roles)
    def detalhes_pedido(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        empresa = _obter_empresa_config()
        separacao_ativa = _separacao_entrega_ativa(empresa)
        unir_off = bool(empresa and empresa.separacao_entrega_unir_vendas_off)
        origem_elegivel_separacao = (pedido.origem == 'site') or (unir_off and pedido.origem == 'interno')

        funcionario = Funcionario.query.get(session.get('funcionario_id')) if session.get('funcionario_id') else None
        paginas_permitidas = None
        if funcionario and funcionario.ativo and funcionario.role != 'admin' and funcionario.controle_acesso_ativo:
            paginas_permitidas = _paginas_efetivas_funcionario(funcionario)
        return render_template(
            'vendas/pedidos/detalhes_pedido.html',
            pedido=pedido,
            empresa=empresa,
            status_transitions=ORDER_ALLOWED_TRANSITIONS,
            separacao_ativa=separacao_ativa,
            origem_elegivel_separacao=origem_elegivel_separacao,
            etiquetas_ativas=_emissao_etiqueta_entrega_ativa(empresa),
            pode_editar=_usuario_tem_acesso_endpoint('editar_pedido', funcionario, paginas_permitidas),
            pode_alterar_status=_usuario_tem_acesso_endpoint('alterar_status_pedido', funcionario, paginas_permitidas),
            pode_excluir=_usuario_tem_acesso_endpoint('deletar_pedido', funcionario, paginas_permitidas),
            pode_atualizar_separacao=_usuario_tem_acesso_endpoint('atualizar_separacao_entrega_pedido', funcionario, paginas_permitidas),
            pode_imprimir_etiqueta=_usuario_tem_acesso_endpoint('imprimir_etiqueta_entrega_pedido', funcionario, paginas_permitidas),
            pode_ver_comprovante=_usuario_tem_acesso_endpoint('visualizar_comprovante_pedido', funcionario, paginas_permitidas),
        )

    @app.route('/pdv')
    @require_role(*vendas_operacao_roles)
    def pdv():
        """Interface de PDV (Ponto de Venda) para o operador de caixa"""
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        empresa = _obter_empresa_config()
        produtos = Produto.query.filter(Produto.ativo.is_(True), Produto.filtro_nao_vencidos()).order_by(Produto.nome).all()
        caixas_abertas = Caixa.query.filter_by(aberto=True).all()
        mesas = Mesa.query.all() if atendimento_mesas_ativo else []
        garcons = Garcom.query.filter_by(ativo=True).order_by(Garcom.nome.asc()).all() if atendimento_mesas_ativo else []
        metodos_pagamento_pdv = load_payment_options(empresa.pagamentos_pdv_json, 'pdv')
        return render_template(
            'vendas/pdv.html',
            produtos=produtos,
            caixas_abertas=caixas_abertas,
            mesas=mesas,
            garcons=garcons,
            atendimento_mesas_ativo=atendimento_mesas_ativo,
            metodos_pagamento_pdv=metodos_pagamento_pdv,
            metodo_pagamento_pdv_padrao=default_payment_id(empresa.pagamentos_pdv_json, 'pdv') or 'dinheiro',
        )

    @app.route('/api/pedidos/criar', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def criar_pedido_api():
        """API para criar pedido via AJAX."""
        try:
            atendimento_mesas_ativo = _atendimento_mesas_ativo()
            data = request.get_json(silent=True) or {}
            caixa_id = data.get('caixa_id')
            mesa_id = data.get('mesa_id') or None
            if not atendimento_mesas_ativo:
                mesa_id = None
            itens = data.get('itens', [])

            if not caixa_id or not itens:
                return json_response(False, 'Caixa e produtos sao obrigatorios.', status=400, code='validation_error')

            caixa = Caixa.query.get(caixa_id)
            mesa = Mesa.query.get(mesa_id) if atendimento_mesas_ativo and mesa_id else None
            pedido = service_create_order(
                caixa=caixa,
                itens_payload=itens,
                mesa=mesa,
                garcom_id=_garcom_logado_id(),
                atendimento_mesas_ativo=atendimento_mesas_ativo,
                normalizar_item_payload=_normalizar_item_payload,
                empty_items_message='Nenhum item valido para criar o pedido.',
                actor=_funcionario_logado_vendas(),
            )

            db.session.commit()
            try:
                publish_alert({
                    'pedido_id': pedido.id,
                    'mesa': mesa.numero if mesa else None,
                    'criado_em': pedido.criado_em.isoformat() if pedido.criado_em else datetime.utcnow().isoformat(),
                    'itens': [
                        {'quantidade': ip.quantidade, 'produto': ip.produto.nome if ip.produto else ''}
                        for ip in pedido.itens
                    ]
                })
            except Exception:
                pass
            _publicar_metricas_dashboard_tempo_real()

            return json_response(
                True,
                f'Pedido #{pedido.id} criado com sucesso.',
                data={'pedido_id': pedido.id, 'total': float(pedido.total or 0.0)}
            )
        except AppError as e:
            db.session.rollback()
            return json_response(
                False,
                str(e),
                status=getattr(e, 'status_code', 400),
                code=getattr(e, 'code', 'app_error'),
            )
        except Exception as e:
            db.session.rollback()
            return json_response(False, str(e), status=500, code='internal_error')

    @app.route('/api/pedidos/<int:pedido_id>/finalizar', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def finalizar_pedido_api(pedido_id):
        """API para finalizar pedido via AJAX."""
        try:
            pedido = venda_service.carregar_pedido_pdv(pedido_id)
            if _parse_status(pedido.status) in ORDER_IMMUTABLE_STATUSES:
                return json_response(False, f'Pedido ja esta {pedido.status}.', status=409, code='business_rule')

            dados = request.get_json(silent=True) or {}
            metodo = dados.get('metodo_pagamento')
            empresa = _obter_empresa_config()
            metodos_pagamento_pdv_map = payment_methods_map(empresa.pagamentos_pdv_json, 'pdv')
            if metodo:
                metodo_texto, valor_pago = _build_payment_data(
                    metodo_raw=metodo,
                    valor_raw=dados.get('valor_pago'),
                    total_pedido=pedido.total,
                    payment_methods=metodos_pagamento_pdv_map,
                    split_raw=dados.get('split_pagamento'),
                    cliente_crediario=dados.get('cliente_crediario', '')
                )
            else:
                metodo_texto = pedido.metodo_pagamento
                valor_pago = pedido.valor_pago

            payload = venda_service.processar_venda_rapida(
                pedido_id,
                metodo_pagamento=metodo_texto,
                valor_pago=valor_pago,
                desconto_total=dados.get('desconto_total') or 0.0,
                incluir_contabilidade=bool(dados.get('incluir_contabilidade')),
                actor=_funcionario_logado_vendas(),
            )
            _publicar_metricas_dashboard_tempo_real()

            return json_response(
                True,
                'Pedido finalizado com sucesso.',
                data=payload
            )
        except AppError as e:
            db.session.rollback()
            status_code, code = _http_status_for_order_error(str(e))
            return json_response(False, str(e), status=getattr(e, 'status_code', status_code), code=getattr(e, 'code', code))
        except Exception as e:
            db.session.rollback()
            return json_response(False, str(e), status=500, code='internal_error')

    @app.route('/api/pdv/produtos/buscar')
    @require_role(*vendas_operacao_roles)
    def buscar_produtos_pdv_api():
        termo = (request.args.get('q') or '').strip()
        if not termo:
            return fail('Informe um termo de busca.', code='validation_error', status=400, fields={'q': 'obrigatorio'})

        try:
            produtos = venda_service.buscar_produtos_pdv(termo, limit=request.args.get('limit', type=int) or 12)
            return ok(
                {
                    'query': termo,
                    'items': produtos,
                    'latency_target_ms': 100,
                    'search_strategy': 'barcode_first_then_ranked_text',
                },
                message='Busca de produtos processada com sucesso.',
                code='pdv_search_ok',
            )
        except AppError as e:
            return fail(str(e), code=getattr(e, 'code', 'app_error'), status=getattr(e, 'status_code', 400))

    @app.route('/api/pedidos/aberto/<int:caixa_id>')
    @require_role(*vendas_operacao_roles)
    def get_pedido_aberto(caixa_id):
        """Retorna pedido aberto para determinada caixa, se existir"""
        pedido = Pedido.query.filter_by(caixa_id=caixa_id, status='aberto').first()
        if not pedido:
            return jsonify({'exists': False})
        itens = []
        for ip in pedido.itens:
            itens.append({
                'produto_id': ip.produto_id,
                'nome': ip.produto.nome,
                'quantidade': ip.quantidade,
                'preco': ip.preco_unitario
            })
        return jsonify({
            'exists': True,
            'pedido_id': pedido.id,
            'itens': itens,
            'total': pedido.total
        })

    @app.route('/api/pedidos/em-aberto')
    @require_role(*vendas_operacao_roles)
    def listar_pedidos_em_aberto_pdv():
        """Lista pedidos nao finalizados para selecao no PDV (todas as caixas ou filtrado)."""
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        status_filtro = (request.args.get('status') or '').strip().lower()
        mesa_id = request.args.get('mesa_id', type=int)
        garcom_id = request.args.get('garcom_id', type=int)
        caixa_id = request.args.get('caixa_id', type=int)

        query = Pedido.query.filter(
            Pedido.status.in_(['aberto', 'em_preparo', 'entregue'])
        )

        if status_filtro in {'aberto', 'em_preparo', 'entregue'}:
            query = query.filter(Pedido.status == status_filtro)
        if caixa_id:
            query = query.filter(Pedido.caixa_id == caixa_id)
        if atendimento_mesas_ativo and mesa_id:
            query = query.filter(Pedido.mesa_id == mesa_id)
        if atendimento_mesas_ativo and garcom_id:
            query = query.filter(Pedido.garcom_id == garcom_id)

        pedidos = query.order_by(Pedido.criado_em.desc()).all()

        return jsonify({
            'success': True,
            'pedidos': [
                {
                    'id': p.id,
                    'status': p.status,
                    'caixa_id': p.caixa_id,
                    'caixa_nome': p.caixa.nome if p.caixa else None,
                    'mesa_id': p.mesa_id,
                    'mesa_numero': p.mesa.numero if p.mesa else None,
                    'garcom_id': p.garcom_id,
                    'garcom_nome': p.garcom.nome if p.garcom else None,
                    'cliente_nome': p.cliente_nome,
                    'origem': p.origem,
                    'total': p.total or 0.0,
                    'criado_em': p.criado_em.isoformat() if p.criado_em else None
                }
                for p in pedidos
            ]
        })

    @app.route('/api/pedidos/caixa/<int:caixa_id>/em-aberto')
    @require_role(*vendas_operacao_roles)
    def listar_pedidos_caixa_em_aberto(caixa_id):
        """Compat: mantem endpoint legado por caixa."""
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        status_filtro = (request.args.get('status') or '').strip().lower()
        mesa_id = request.args.get('mesa_id', type=int)
        garcom_id = request.args.get('garcom_id', type=int)

        query = Pedido.query.filter(
            Pedido.caixa_id == caixa_id,
            Pedido.status.in_(['aberto', 'em_preparo', 'entregue'])
        )

        if status_filtro in {'aberto', 'em_preparo', 'entregue'}:
            query = query.filter(Pedido.status == status_filtro)
        if atendimento_mesas_ativo and mesa_id:
            query = query.filter(Pedido.mesa_id == mesa_id)
        if atendimento_mesas_ativo and garcom_id:
            query = query.filter(Pedido.garcom_id == garcom_id)

        pedidos = query.order_by(Pedido.criado_em.desc()).all()
        return jsonify({
            'success': True,
            'pedidos': [
                {
                    'id': p.id,
                    'status': p.status,
                    'caixa_id': p.caixa_id,
                    'caixa_nome': p.caixa.nome if p.caixa else None,
                    'mesa_id': p.mesa_id,
                    'mesa_numero': p.mesa.numero if p.mesa else None,
                    'garcom_id': p.garcom_id,
                    'garcom_nome': p.garcom.nome if p.garcom else None,
                    'cliente_nome': p.cliente_nome,
                    'origem': p.origem,
                    'total': p.total or 0.0,
                    'criado_em': p.criado_em.isoformat() if p.criado_em else None
                }
                for p in pedidos
            ]
        })

    @app.route('/api/pedidos/<int:pedido_id>/detalhes-json')
    @require_role(*vendas_operacao_roles)
    def detalhes_pedido_api(pedido_id):
        """Retorna detalhes do pedido para carregar no PDV."""
        pedido = Pedido.query.get_or_404(pedido_id)

        itens = []
        for ip in pedido.itens:
            nome_produto = ip.produto.nome if ip.produto else f'Produto {ip.produto_id}'
            itens.append({
                'produto_id': ip.produto_id,
                'nome': nome_produto,
                'quantidade': ip.quantidade,
                'preco': ip.preco_unitario
            })

        return jsonify({
            'success': True,
            'pedido': {
                'id': pedido.id,
                'status': pedido.status,
                'mesa_id': pedido.mesa_id,
                'mesa_numero': pedido.mesa.numero if pedido.mesa else None,
                'garcom_id': pedido.garcom_id,
                'garcom_nome': pedido.garcom.nome if pedido.garcom else None,
                'cliente_nome': pedido.cliente_nome,
                'total': pedido.total or 0.0,
                'itens': itens
            }
        })

    @app.route('/api/pedidos/<int:pedido_id>/adicionar', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def adicionar_itens_pedido_api(pedido_id):
        """Adiciona itens a um pedido ja aberto."""
        pedido = Pedido.query.get_or_404(pedido_id)
        if _parse_status(pedido.status) != 'aberto':
            return json_response(False, 'Somente pedidos com status aberto podem receber itens.', status=409, code='business_rule')

        dados = request.get_json(silent=True) or {}
        itens = dados.get('itens', [])
        if not itens:
            return json_response(False, 'Nenhum item enviado.', status=400, code='validation_error')

        itens_validos = 0
        try:
            for it in itens:
                normalizado, erro = _normalizar_item_payload(it)
                if erro:
                    continue
                prod = normalizado['produto']
                qty = normalizado['quantidade']
                ip = ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=prod.id,
                    quantidade=qty,
                    preco_unitario=prod.preco_venda
                )
                db.session.add(ip)
                itens_validos += 1

            if itens_validos == 0:
                return json_response(False, 'Nenhum item valido para adicionar.', status=400, code='validation_error')

            _recalcular_total_pedido(pedido)
            db.session.commit()
            _publicar_metricas_dashboard_tempo_real()
            return json_response(
                True,
                'Itens adicionados com sucesso.',
                data={'pedido_id': pedido.id, 'total': float(pedido.total or 0.0)}
            )
        except Exception as e:
            db.session.rollback()
            return json_response(False, str(e), status=500, code='internal_error')

    @app.route('/eventos/pedidos')
    @require_role(*vendas_operacao_roles)
    def sse_pedidos():
        return Response(sse_stream(), mimetype='text/event-stream')




