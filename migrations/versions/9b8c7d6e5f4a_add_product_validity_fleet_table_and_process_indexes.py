"""add product validity fleet table and process indexes

Revision ID: 9b8c7d6e5f4a
Revises: f1a2b3c4d5e6
Create Date: 2026-04-06 10:30:00.000000
"""

from __future__ import annotations

import json

from alembic import op
import sqlalchemy as sa


revision = '9b8c7d6e5f4a'
down_revision = 'f1a2b3c4d5e6'
branch_labels = None
depends_on = None


def _inspector():
    return sa.inspect(op.get_bind())


def _has_table(name):
    return _inspector().has_table(name)


def _columns(name):
    if not _has_table(name):
        return set()
    return {col['name'] for col in _inspector().get_columns(name)}


def _indexes(name):
    if not _has_table(name):
        return set()
    return {idx['name'] for idx in _inspector().get_indexes(name)}


def _create_index_if_missing(table_name, index_name, columns, *, unique=False):
    if index_name not in _indexes(table_name):
        op.create_index(index_name, table_name, columns, unique=unique)


def _drop_index_if_exists(table_name, index_name):
    if index_name in _indexes(table_name):
        op.drop_index(index_name, table_name=table_name)


def _normalizar_tipo_veiculo(valor):
    texto = (valor or '').strip().lower()
    if 'moto' in texto:
        return 'moto'
    if 'caminh' in texto:
        return 'caminhao'
    if 'util' in texto or 'van' in texto:
        return 'utilitario'
    return 'carro'


def _parse_float(valor):
    if valor in (None, ''):
        return None
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def _parse_int(valor):
    if valor in (None, ''):
        return 0
    try:
        return max(int(valor), 0)
    except (TypeError, ValueError):
        return 0


def _carregar_veiculos_legados(raw_value):
    if not raw_value:
        return []
    try:
        dados = json.loads(raw_value)
    except Exception:
        return []
    if not isinstance(dados, list):
        return []

    resultado = []
    for item in dados:
        if isinstance(item, dict):
            nome = (item.get('nome') or '').strip()
            if not nome:
                continue
            resultado.append({
                'nome': nome,
                'placa': (item.get('placa') or '').strip().upper() or None,
                'tipo': _normalizar_tipo_veiculo(item.get('categoria') or item.get('tipo')),
                'capacidade_kg': _parse_float(item.get('capacidade_kg')),
                'capacidade_volume': _parse_float(item.get('capacidade_volume')),
                'motorista_padrao': (item.get('motorista_padrao') or '').strip() or None,
                'tipo_entrega': (item.get('tipo_entrega') or 'todos').strip().lower() or 'todos',
                'capacidade_pedidos': _parse_int(item.get('capacidade_pedidos')),
                'empresa_terceirizada': (item.get('empresa') or item.get('empresa_terceirizada') or '').strip() or None,
                'ativo': item.get('ativo', True) is not False,
            })
            continue

        partes = [parte.strip() for parte in str(item or '').split('|')]
        nome = partes[0] if partes else ''
        if not nome:
            continue
        resultado.append({
            'nome': nome,
            'placa': partes[1].upper() if len(partes) > 1 and partes[1] else None,
            'tipo': _normalizar_tipo_veiculo(partes[2] if len(partes) > 2 else None),
            'capacidade_kg': _parse_float(partes[5] if len(partes) > 5 else None),
            'capacidade_volume': None,
            'motorista_padrao': None,
            'tipo_entrega': (partes[3].lower() if len(partes) > 3 and partes[3] else 'todos'),
            'capacidade_pedidos': _parse_int(partes[4] if len(partes) > 4 else None),
            'empresa_terceirizada': partes[6] if len(partes) > 6 and partes[6] else None,
            'ativo': True,
        })
    return resultado


def upgrade():
    bind = op.get_bind()

    if _has_table('produtos') and 'validade' not in _columns('produtos'):
        with op.batch_alter_table('produtos', schema=None) as batch_op:
            batch_op.add_column(sa.Column('validade', sa.Date(), nullable=True))
    if _has_table('produtos'):
        _create_index_if_missing('produtos', 'ix_produtos_validade_ativo', ['validade', 'ativo'])

    if not _has_table('frota_veiculos'):
        op.create_table(
            'frota_veiculos',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('empresa_id', sa.Integer(), nullable=False),
            sa.Column('nome', sa.String(length=120), nullable=False),
            sa.Column('placa', sa.String(length=20), nullable=True),
            sa.Column('tipo', sa.String(length=20), nullable=False, server_default='carro'),
            sa.Column('capacidade_kg', sa.Float(), nullable=True),
            sa.Column('capacidade_volume', sa.Float(), nullable=True),
            sa.Column('motorista_padrao', sa.String(length=120), nullable=True),
            sa.Column('tipo_entrega', sa.String(length=20), nullable=False, server_default='todos'),
            sa.Column('capacidade_pedidos', sa.Integer(), nullable=True, server_default='0'),
            sa.Column('empresa_terceirizada', sa.String(length=150), nullable=True),
            sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column('atualizado_em', sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.ForeignKeyConstraint(['empresa_id'], ['empresa_config.id']),
            sa.PrimaryKeyConstraint('id'),
        )
    else:
        colunas_frota = _columns('frota_veiculos')
        with op.batch_alter_table('frota_veiculos', schema=None) as batch_op:
            if 'tipo_entrega' not in colunas_frota:
                batch_op.add_column(sa.Column('tipo_entrega', sa.String(length=20), nullable=False, server_default='todos'))
            if 'capacidade_pedidos' not in colunas_frota:
                batch_op.add_column(sa.Column('capacidade_pedidos', sa.Integer(), nullable=True, server_default='0'))
            if 'empresa_terceirizada' not in colunas_frota:
                batch_op.add_column(sa.Column('empresa_terceirizada', sa.String(length=150), nullable=True))
            if 'capacidade_volume' not in colunas_frota:
                batch_op.add_column(sa.Column('capacidade_volume', sa.Float(), nullable=True))

    _create_index_if_missing('frota_veiculos', 'ix_frota_veiculos_empresa_ativo', ['empresa_id', 'ativo'])
    _create_index_if_missing('frota_veiculos', 'ix_frota_veiculos_placa', ['placa'])

    if _has_table('empresa_config') and _has_table('frota_veiculos'):
        empresa_config = sa.table(
            'empresa_config',
            sa.column('id', sa.Integer),
            sa.column('entrega_veiculos_json', sa.Text),
        )
        frota_veiculos = sa.table(
            'frota_veiculos',
            sa.column('empresa_id', sa.Integer),
            sa.column('nome', sa.String),
            sa.column('placa', sa.String),
            sa.column('tipo', sa.String),
            sa.column('capacidade_kg', sa.Float),
            sa.column('capacidade_volume', sa.Float),
            sa.column('motorista_padrao', sa.String),
            sa.column('tipo_entrega', sa.String),
            sa.column('capacidade_pedidos', sa.Integer),
            sa.column('empresa_terceirizada', sa.String),
            sa.column('ativo', sa.Boolean),
        )
        for empresa_id, raw_json in bind.execute(
            sa.select(empresa_config.c.id, empresa_config.c.entrega_veiculos_json)
        ):
            existentes = bind.execute(
                sa.select(sa.func.count()).select_from(frota_veiculos).where(frota_veiculos.c.empresa_id == empresa_id)
            ).scalar() or 0
            if existentes:
                continue
            registros = _carregar_veiculos_legados(raw_json)
            for registro in registros:
                bind.execute(
                    sa.insert(frota_veiculos).values(
                        empresa_id=empresa_id,
                        nome=registro['nome'],
                        placa=registro['placa'],
                        tipo=registro['tipo'],
                        capacidade_kg=registro['capacidade_kg'],
                        capacidade_volume=registro['capacidade_volume'],
                        motorista_padrao=registro['motorista_padrao'],
                        tipo_entrega=registro['tipo_entrega'],
                        capacidade_pedidos=registro['capacidade_pedidos'],
                        empresa_terceirizada=registro['empresa_terceirizada'],
                        ativo=registro['ativo'],
                    )
                )

    if _has_table('processo_eventos'):
        _drop_index_if_exists('processo_eventos', 'ix_processo_eventos_pedido_criado_em')
        _drop_index_if_exists('processo_eventos', 'ix_processo_eventos_recebimento_criado_em')
        _create_index_if_missing('processo_eventos', 'ix_processo_eventos_pedido_criado', ['pedido_id', 'criado_em'])
        _create_index_if_missing('processo_eventos', 'ix_processo_eventos_recebimento_criado', ['recebimento_id', 'criado_em'])


def downgrade():
    if _has_table('processo_eventos'):
        _drop_index_if_exists('processo_eventos', 'ix_processo_eventos_pedido_criado')
        _drop_index_if_exists('processo_eventos', 'ix_processo_eventos_recebimento_criado')
        _create_index_if_missing('processo_eventos', 'ix_processo_eventos_pedido_criado_em', ['pedido_id', 'criado_em'])
        _create_index_if_missing('processo_eventos', 'ix_processo_eventos_recebimento_criado_em', ['recebimento_id', 'criado_em'])

    if _has_table('frota_veiculos'):
        op.drop_table('frota_veiculos')

    if _has_table('produtos'):
        _drop_index_if_exists('produtos', 'ix_produtos_validade_ativo')
        if 'validade' in _columns('produtos'):
            with op.batch_alter_table('produtos', schema=None) as batch_op:
                batch_op.drop_column('validade')
