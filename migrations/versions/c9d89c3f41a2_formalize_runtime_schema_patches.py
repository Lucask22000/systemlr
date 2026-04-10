"""formalize runtime schema patches

Revision ID: c9d89c3f41a2
Revises: 7f4d9a1c2b10
Create Date: 2026-03-19 21:20:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = 'c9d89c3f41a2'
down_revision = '7f4d9a1c2b10'
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


def _add_columns_if_missing(table_name, columns):
    existing = _columns(table_name)
    if not existing:
        return
    for column in columns:
        if column.name in existing:
            continue
        with op.batch_alter_table(table_name, schema=None) as batch_op:
            batch_op.add_column(column)
        existing.add(column.name)


def _create_funcionario_estoques_if_missing():
    if _has_table('funcionario_estoques'):
        return
    op.create_table(
        'funcionario_estoques',
        sa.Column('funcionario_id', sa.Integer(), nullable=False),
        sa.Column('estoque_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['estoque_id'], ['estoques.id']),
        sa.ForeignKeyConstraint(['funcionario_id'], ['funcionarios.id']),
        sa.PrimaryKeyConstraint('funcionario_id', 'estoque_id'),
    )


def _create_perfis_acesso_if_missing():
    if _has_table('perfis_acesso'):
        return
    op.create_table(
        'perfis_acesso',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('descricao', sa.String(length=255), nullable=True),
        sa.Column('permissoes_padrao', sa.Text(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.Column('atualizado_em', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome'),
    )


def _create_clientes_publicos_if_missing():
    if _has_table('clientes_publicos'):
        return
    op.create_table(
        'clientes_publicos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('celular', sa.String(length=30), nullable=False),
        sa.Column('cpf_cnpj', sa.String(length=20), nullable=True),
        sa.Column('cep', sa.String(length=12), nullable=True),
        sa.Column('endereco', sa.String(length=180), nullable=True),
        sa.Column('numero', sa.String(length=20), nullable=True),
        sa.Column('complemento', sa.String(length=120), nullable=True),
        sa.Column('bairro', sa.String(length=100), nullable=True),
        sa.Column('cidade', sa.String(length=100), nullable=True),
        sa.Column('estado', sa.String(length=2), nullable=True),
        sa.Column('referencia', sa.String(length=180), nullable=True),
        sa.Column('recebe_ofertas', sa.Boolean(), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.Column('atualizado_em', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    _create_index_if_missing('clientes_publicos', 'ix_clientes_publicos_email', ['email'])
    _create_index_if_missing('clientes_publicos', 'ix_clientes_publicos_celular', ['celular'])
    _create_index_if_missing('clientes_publicos', 'ix_clientes_publicos_cpf_cnpj', ['cpf_cnpj'])
    _create_index_if_missing('clientes_publicos', 'ix_clientes_publicos_criado_em', ['criado_em'])


def _create_lancamentos_financeiros_if_missing():
    if _has_table('lancamentos_financeiros'):
        return
    op.create_table(
        'lancamentos_financeiros',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=30), nullable=False),
        sa.Column('categoria', sa.String(length=80), nullable=True),
        sa.Column('descricao', sa.String(length=255), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('data_competencia', sa.Date(), nullable=False),
        sa.Column('incluir_contabilidade', sa.Boolean(), nullable=False),
        sa.Column('enviado_contador', sa.Boolean(), nullable=False),
        sa.Column('enviado_em', sa.DateTime(), nullable=True),
        sa.Column('referencia_documento', sa.String(length=120), nullable=True),
        sa.Column('centro_custo', sa.String(length=120), nullable=True),
        sa.Column('pedido_id', sa.Integer(), nullable=True),
        sa.Column('recebimento_id', sa.Integer(), nullable=True),
        sa.Column('produto_id', sa.Integer(), nullable=True),
        sa.Column('quantidade', sa.Float(), nullable=True),
        sa.Column('criado_por_id', sa.Integer(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['criado_por_id'], ['funcionarios.id']),
        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id']),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id']),
        sa.ForeignKeyConstraint(['recebimento_id'], ['recebimentos_fornecedor.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    _create_index_if_missing('lancamentos_financeiros', 'ix_lancamentos_financeiros_tipo', ['tipo'])
    _create_index_if_missing('lancamentos_financeiros', 'ix_lancamentos_financeiros_data_competencia', ['data_competencia'])
    _create_index_if_missing('lancamentos_financeiros', 'ix_lancamentos_financeiros_pedido_id', ['pedido_id'])
    _create_index_if_missing('lancamentos_financeiros', 'ix_lancamentos_financeiros_recebimento_id', ['recebimento_id'])
    _create_index_if_missing('lancamentos_financeiros', 'ix_lancamentos_tipo_data_competencia', ['tipo', 'data_competencia'])


def _create_fundos_solicitacoes_if_missing():
    if _has_table('fundos_solicitacoes'):
        return
    op.create_table(
        'fundos_solicitacoes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=20), nullable=False),
        sa.Column('categoria', sa.String(length=80), nullable=True),
        sa.Column('descricao', sa.String(length=255), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('centro_custo', sa.String(length=120), nullable=True),
        sa.Column('referencia_documento', sa.String(length=120), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('motivo_rejeicao', sa.String(length=255), nullable=True),
        sa.Column('solicitado_por_id', sa.Integer(), nullable=True),
        sa.Column('aprovado_por_id', sa.Integer(), nullable=True),
        sa.Column('liberado_por_id', sa.Integer(), nullable=True),
        sa.Column('lancamento_financeiro_id', sa.Integer(), nullable=True),
        sa.Column('solicitado_em', sa.DateTime(), nullable=False),
        sa.Column('aprovado_em', sa.DateTime(), nullable=True),
        sa.Column('liberado_em', sa.DateTime(), nullable=True),
        sa.Column('atualizado_em', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['aprovado_por_id'], ['funcionarios.id']),
        sa.ForeignKeyConstraint(['lancamento_financeiro_id'], ['lancamentos_financeiros.id']),
        sa.ForeignKeyConstraint(['liberado_por_id'], ['funcionarios.id']),
        sa.ForeignKeyConstraint(['solicitado_por_id'], ['funcionarios.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    _create_index_if_missing('fundos_solicitacoes', 'ix_fundos_solicitacoes_status', ['status'])
    _create_index_if_missing('fundos_solicitacoes', 'ix_fundos_solicitacoes_solicitado_por_id', ['solicitado_por_id'])


def _create_processo_eventos_if_missing():
    if _has_table('processo_eventos'):
        return
    op.create_table(
        'processo_eventos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('processo_tipo', sa.String(length=40), nullable=False),
        sa.Column('etapa', sa.String(length=80), nullable=False),
        sa.Column('acao', sa.String(length=120), nullable=False),
        sa.Column('entidade', sa.String(length=80), nullable=False),
        sa.Column('entidade_id', sa.Integer(), nullable=False),
        sa.Column('pedido_id', sa.Integer(), nullable=True),
        sa.Column('recebimento_id', sa.Integer(), nullable=True),
        sa.Column('movimentacao_id', sa.Integer(), nullable=True),
        sa.Column('lancamento_financeiro_id', sa.Integer(), nullable=True),
        sa.Column('fundo_solicitacao_id', sa.Integer(), nullable=True),
        sa.Column('funcionario_id', sa.Integer(), nullable=True),
        sa.Column('funcionario_nome', sa.String(length=120), nullable=True),
        sa.Column('detalhes', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['funcionario_id'], ['funcionarios.id']),
        sa.ForeignKeyConstraint(['fundo_solicitacao_id'], ['fundos_solicitacoes.id']),
        sa.ForeignKeyConstraint(['lancamento_financeiro_id'], ['lancamentos_financeiros.id']),
        sa.ForeignKeyConstraint(['movimentacao_id'], ['movimentacoes.id']),
        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id']),
        sa.ForeignKeyConstraint(['recebimento_id'], ['recebimentos_fornecedor.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    _create_index_if_missing('processo_eventos', 'ix_processo_eventos_processo_tipo', ['processo_tipo'])
    _create_index_if_missing('processo_eventos', 'ix_processo_eventos_entidade', ['entidade'])
    _create_index_if_missing('processo_eventos', 'ix_processo_eventos_entidade_id', ['entidade_id'])
    _create_index_if_missing('processo_eventos', 'ix_processo_eventos_criado_em', ['criado_em'])
    _create_index_if_missing('processo_eventos', 'ix_processo_eventos_pedido_criado_em', ['pedido_id', 'criado_em'])
    _create_index_if_missing('processo_eventos', 'ix_processo_eventos_recebimento_criado_em', ['recebimento_id', 'criado_em'])
    _create_index_if_missing('processo_eventos', 'ix_processo_eventos_entidade_entidade_id', ['entidade', 'entidade_id'])


def _create_equipamentos_if_missing():
    if not _has_table('equipamentos_movimentacao'):
        op.create_table(
            'equipamentos_movimentacao',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('codigo', sa.String(length=40), nullable=False),
            sa.Column('nome', sa.String(length=120), nullable=False),
            sa.Column('tipo', sa.String(length=20), nullable=False),
            sa.Column('placa', sa.String(length=20), nullable=True),
            sa.Column('capacidade_kg', sa.Float(), nullable=True),
            sa.Column('bateria_codigo', sa.String(length=40), nullable=True),
            sa.Column('bateria_nivel', sa.Integer(), nullable=True),
            sa.Column('status', sa.String(length=20), nullable=False),
            sa.Column('proxima_manutencao_em', sa.Date(), nullable=True),
            sa.Column('observacoes', sa.Text(), nullable=True),
            sa.Column('ativo', sa.Boolean(), nullable=True),
            sa.Column('criado_em', sa.DateTime(), nullable=False),
            sa.Column('atualizado_em', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('codigo'),
        )
        _create_index_if_missing('equipamentos_movimentacao', 'ix_equipamentos_movimentacao_codigo', ['codigo'], unique=True)

    if not _has_table('manutencoes_equipamento'):
        op.create_table(
            'manutencoes_equipamento',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('equipamento_id', sa.Integer(), nullable=False),
            sa.Column('tipo', sa.String(length=20), nullable=False),
            sa.Column('descricao', sa.String(length=255), nullable=False),
            sa.Column('custo', sa.Float(), nullable=True),
            sa.Column('realizado_em', sa.Date(), nullable=True),
            sa.Column('proxima_em', sa.Date(), nullable=True),
            sa.Column('responsavel', sa.String(length=120), nullable=True),
            sa.Column('criado_em', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['equipamento_id'], ['equipamentos_movimentacao.id']),
            sa.PrimaryKeyConstraint('id'),
        )
        _create_index_if_missing('manutencoes_equipamento', 'ix_manutencoes_equipamento_equipamento_id', ['equipamento_id'])


def _create_ordens_chamados_if_missing():
    if not _has_table('ordens_servico'):
        op.create_table(
            'ordens_servico',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('titulo', sa.String(length=160), nullable=False),
            sa.Column('tipo', sa.String(length=30), nullable=False),
            sa.Column('servico_tipo', sa.String(length=20), nullable=False),
            sa.Column('prioridade', sa.String(length=20), nullable=True),
            sa.Column('status', sa.String(length=30), nullable=False),
            sa.Column('descricao', sa.Text(), nullable=True),
            sa.Column('observacoes', sa.Text(), nullable=True),
            sa.Column('avaria_detalhes', sa.Text(), nullable=True),
            sa.Column('inspecao_detalhes', sa.Text(), nullable=True),
            sa.Column('resultado_inspecao', sa.String(length=120), nullable=True),
            sa.Column('produto_id', sa.Integer(), nullable=True),
            sa.Column('pedido_id', sa.Integer(), nullable=True),
            sa.Column('funcionario_destino_id', sa.Integer(), nullable=True),
            sa.Column('criado_por_id', sa.Integer(), nullable=True),
            sa.Column('data_agendada', sa.Date(), nullable=True),
            sa.Column('enviada_em', sa.DateTime(), nullable=True),
            sa.Column('iniciado_em', sa.DateTime(), nullable=True),
            sa.Column('concluida_em', sa.DateTime(), nullable=True),
            sa.Column('retorno_tecnico', sa.Text(), nullable=True),
            sa.Column('criado_em', sa.DateTime(), nullable=False),
            sa.Column('atualizado_em', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['criado_por_id'], ['funcionarios.id']),
            sa.ForeignKeyConstraint(['funcionario_destino_id'], ['funcionarios.id']),
            sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id']),
            sa.ForeignKeyConstraint(['produto_id'], ['produtos.id']),
            sa.PrimaryKeyConstraint('id'),
        )
        _create_index_if_missing('ordens_servico', 'ix_ordens_servico_tipo', ['tipo'])
        _create_index_if_missing('ordens_servico', 'ix_ordens_servico_status', ['status'])
        _create_index_if_missing('ordens_servico', 'ix_ordens_servico_pedido_id', ['pedido_id'])
        _create_index_if_missing('ordens_servico', 'ix_ordens_servico_funcionario_destino_id', ['funcionario_destino_id'])
        _create_index_if_missing('ordens_servico', 'ix_ordens_servico_criado_em', ['criado_em'])

    if not _has_table('chamados_internos'):
        op.create_table(
            'chamados_internos',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('titulo', sa.String(length=160), nullable=False),
            sa.Column('categoria', sa.String(length=40), nullable=False),
            sa.Column('prioridade', sa.String(length=20), nullable=False),
            sa.Column('status', sa.String(length=30), nullable=False),
            sa.Column('setor_origem', sa.String(length=80), nullable=True),
            sa.Column('descricao', sa.Text(), nullable=False),
            sa.Column('resolucao', sa.Text(), nullable=True),
            sa.Column('solicitante_id', sa.Integer(), nullable=False),
            sa.Column('responsavel_id', sa.Integer(), nullable=True),
            sa.Column('aberto_em', sa.DateTime(), nullable=False),
            sa.Column('concluido_em', sa.DateTime(), nullable=True),
            sa.Column('atualizado_em', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['responsavel_id'], ['funcionarios.id']),
            sa.ForeignKeyConstraint(['solicitante_id'], ['funcionarios.id']),
            sa.PrimaryKeyConstraint('id'),
        )
        _create_index_if_missing('chamados_internos', 'ix_chamados_internos_titulo', ['titulo'])
        _create_index_if_missing('chamados_internos', 'ix_chamados_internos_categoria', ['categoria'])
        _create_index_if_missing('chamados_internos', 'ix_chamados_internos_prioridade', ['prioridade'])
        _create_index_if_missing('chamados_internos', 'ix_chamados_internos_status', ['status'])
        _create_index_if_missing('chamados_internos', 'ix_chamados_internos_solicitante_id', ['solicitante_id'])
        _create_index_if_missing('chamados_internos', 'ix_chamados_internos_responsavel_id', ['responsavel_id'])
        _create_index_if_missing('chamados_internos', 'ix_chamados_internos_aberto_em', ['aberto_em'])


def _create_almoxarifado_if_missing():
    if _has_table('almoxarifado_atribuicoes'):
        return
    op.create_table(
        'almoxarifado_atribuicoes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('funcionario_id', sa.Integer(), nullable=True),
        sa.Column('registrado_por_id', sa.Integer(), nullable=True),
        sa.Column('destino_tipo', sa.String(length=20), nullable=False),
        sa.Column('nome_destino', sa.String(length=120), nullable=False),
        sa.Column('setor_destino', sa.String(length=80), nullable=True),
        sa.Column('matricula_referencia', sa.String(length=30), nullable=True),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['funcionario_id'], ['funcionarios.id']),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id']),
        sa.ForeignKeyConstraint(['registrado_por_id'], ['funcionarios.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    _create_index_if_missing('almoxarifado_atribuicoes', 'ix_almoxarifado_atribuicoes_produto_id', ['produto_id'])
    _create_index_if_missing('almoxarifado_atribuicoes', 'ix_almoxarifado_atribuicoes_funcionario_id', ['funcionario_id'])
    _create_index_if_missing('almoxarifado_atribuicoes', 'ix_almoxarifado_atribuicoes_criado_em', ['criado_em'])


def _create_feedback_if_missing():
    if _has_table('assistente_local_feedback'):
        return
    op.create_table(
        'assistente_local_feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('funcionario_id', sa.Integer(), nullable=False),
        sa.Column('response_id', sa.String(length=64), nullable=False),
        sa.Column('vote', sa.String(length=10), nullable=False),
        sa.Column('question', sa.Text(), nullable=True),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('reason', sa.String(length=255), nullable=True),
        sa.Column('endpoint_atual', sa.String(length=120), nullable=True),
        sa.Column('pagina_atual', sa.String(length=80), nullable=True),
        sa.Column('tela_atual', sa.String(length=120), nullable=True),
        sa.Column('matched_doc_ids_json', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['funcionario_id'], ['funcionarios.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('funcionario_id', 'response_id', name='uq_assistente_feedback_funcionario_response'),
    )
    _create_index_if_missing('assistente_local_feedback', 'ix_assistente_local_feedback_funcionario_id', ['funcionario_id'])
    _create_index_if_missing('assistente_local_feedback', 'ix_assistente_local_feedback_response_id', ['response_id'])
    _create_index_if_missing('assistente_local_feedback', 'ix_assistente_local_feedback_vote', ['vote'])
    _create_index_if_missing('assistente_local_feedback', 'ix_assistente_local_feedback_pagina_atual', ['pagina_atual'])
    _create_index_if_missing('assistente_local_feedback', 'ix_assistente_local_feedback_criado_em', ['criado_em'])


def upgrade():
    _create_perfis_acesso_if_missing()
    _create_funcionario_estoques_if_missing()
    _create_clientes_publicos_if_missing()
    _create_lancamentos_financeiros_if_missing()
    _create_fundos_solicitacoes_if_missing()
    _create_processo_eventos_if_missing()
    _create_equipamentos_if_missing()
    _create_ordens_chamados_if_missing()
    _create_almoxarifado_if_missing()
    _create_feedback_if_missing()

    _add_columns_if_missing('funcoes_rh', [
        sa.Column('permissoes_padrao', sa.Text(), nullable=True),
    ])

    _add_columns_if_missing('funcionarios', [
        sa.Column('superior_id', sa.Integer(), nullable=True),
        sa.Column('numero_cadastro', sa.Integer(), nullable=True),
        sa.Column('matricula', sa.String(length=30), nullable=True),
        sa.Column('cpf', sa.String(length=14), nullable=True),
        sa.Column('rg', sa.String(length=20), nullable=True),
        sa.Column('data_nascimento', sa.Date(), nullable=True),
        sa.Column('celular', sa.String(length=30), nullable=True),
        sa.Column('cep', sa.String(length=12), nullable=True),
        sa.Column('endereco', sa.String(length=180), nullable=True),
        sa.Column('bairro', sa.String(length=100), nullable=True),
        sa.Column('cidade', sa.String(length=100), nullable=True),
        sa.Column('estado', sa.String(length=2), nullable=True),
        sa.Column('imagem_perfil_path', sa.String(length=255), nullable=True),
        sa.Column('permitir_editar_imagem_perfil', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('senha_provisoria', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('departamento', sa.String(length=80), nullable=True),
        sa.Column('time_nome', sa.String(length=80), nullable=True),
        sa.Column('nivel_organograma', sa.String(length=40), nullable=True),
        sa.Column('pagina_inicial', sa.String(length=30), nullable=True, server_default='dashboard'),
        sa.Column('receber_alertas', sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column('restricao_estoques_ativa', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('estoque_principal_id', sa.Integer(), nullable=True),
        sa.Column('perfil_acesso_id', sa.Integer(), nullable=True),
    ])
    _create_index_if_missing('funcionarios', 'ix_funcionarios_numero_cadastro', ['numero_cadastro'], unique=True)
    _create_index_if_missing('funcionarios', 'ix_funcionarios_matricula', ['matricula'], unique=True)
    _create_index_if_missing('funcionarios', 'ix_funcionarios_cpf', ['cpf'])
    _create_index_if_missing('funcionarios', 'ix_funcionarios_matricula_ativo', ['matricula', 'ativo'])
    _create_index_if_missing('funcionarios', 'ix_funcionarios_email_ativo', ['email', 'ativo'])
    _create_index_if_missing('funcionarios', 'ix_funcionarios_cpf_ativo', ['cpf', 'ativo'])

    _add_columns_if_missing('permissoes_acesso', [
        sa.Column('permitido', sa.Boolean(), nullable=False, server_default=sa.true()),
    ])

    _add_columns_if_missing('estoques', [
        sa.Column('codigo_filial', sa.String(length=20), nullable=True),
    ])
    _create_index_if_missing('estoques', 'ix_estoques_codigo_filial', ['codigo_filial'])

    _add_columns_if_missing('movimentacoes', [
        sa.Column('pedido_id', sa.Integer(), nullable=True),
        sa.Column('recebimento_id', sa.Integer(), nullable=True),
    ])
    _create_index_if_missing('movimentacoes', 'ix_movimentacoes_pedido_id', ['pedido_id'])
    _create_index_if_missing('movimentacoes', 'ix_movimentacoes_recebimento_id', ['recebimento_id'])

    _add_columns_if_missing('empresa_config', [
        sa.Column('codigo_empresa', sa.String(length=20), nullable=True),
        sa.Column('favicon_path', sa.String(length=255), nullable=True),
        sa.Column('app_icon_path', sa.String(length=255), nullable=True),
        sa.Column('separacao_entrega_ativa', sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column('emissao_etiqueta_entrega_ativa', sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column('separacao_entrega_unir_vendas_off', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('roteirizacao_entrega_ativa', sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column('emissao_nota_entrega_ativa', sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column('entrega_local_saida_padrao', sa.String(length=160), nullable=True),
        sa.Column('entrega_veiculo_padrao', sa.String(length=80), nullable=True),
        sa.Column('entrega_motorista_padrao', sa.String(length=120), nullable=True),
        sa.Column('entrega_horario_fechamento_roteirizacao', sa.String(length=5), nullable=True),
        sa.Column('entrega_veiculos_json', sa.Text(), nullable=True),
        sa.Column('entrega_terceirizadas_json', sa.Text(), nullable=True),
        sa.Column('entrega_regras_roteirizacao_json', sa.Text(), nullable=True),
        sa.Column('servicos_tecnicos_ativos', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('servico_montagem_instalacao_ativo', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('tipo_negocio', sa.String(length=30), nullable=True, server_default='conveniencia'),
        sa.Column('canal_operacao', sa.String(length=30), nullable=True, server_default='hibrido'),
        sa.Column('ecommerce_ativo', sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column('ecom_cor_primaria', sa.String(length=20), nullable=True, server_default='#ff7848'),
        sa.Column('ecom_cor_secundaria', sa.String(length=20), nullable=True, server_default='#ff5a2a'),
        sa.Column('ecom_titulo_banner', sa.String(length=140), nullable=True),
        sa.Column('ecom_subtitulo_banner', sa.String(length=255), nullable=True),
        sa.Column('ecom_texto_promocao', sa.String(length=255), nullable=True),
        sa.Column('ecom_banner_path', sa.String(length=255), nullable=True),
        sa.Column('ecom_favicon_path', sa.String(length=255), nullable=True),
        sa.Column('ecom_produto_placeholder_path', sa.String(length=255), nullable=True),
        sa.Column('ecom_banners_json', sa.Text(), nullable=True),
        sa.Column('ecom_campanhas_json', sa.Text(), nullable=True),
        sa.Column('ecom_footer_bg', sa.String(length=20), nullable=True, server_default='#1f2b38'),
        sa.Column('ecom_footer_texto', sa.String(length=255), nullable=True),
        sa.Column('ecom_footer_contato', sa.String(length=255), nullable=True),
        sa.Column('ecom_footer_creditos', sa.String(length=255), nullable=True),
        sa.Column('pagamentos_pdv_json', sa.Text(), nullable=True),
        sa.Column('pagamentos_ecommerce_json', sa.Text(), nullable=True),
        sa.Column('integracoes_pdv_json', sa.Text(), nullable=True),
        sa.Column('integracoes_ecommerce_json', sa.Text(), nullable=True),
        sa.Column('reposicao_loja_fisica_ativa', sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column('emissao_etiqueta_loja_ativa', sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column('emissao_etiqueta_endereco_ativa', sa.Boolean(), nullable=True, server_default=sa.true()),
    ])

    _add_columns_if_missing('pedidos', [
        sa.Column('separacao_entrega_concluida', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('separacao_entrega_em', sa.DateTime(), nullable=True),
        sa.Column('etiqueta_entrega_emitida_em', sa.DateTime(), nullable=True),
        sa.Column('rota_entrega', sa.String(length=120), nullable=True),
        sa.Column('ordem_rota', sa.Integer(), nullable=True),
        sa.Column('local_saida', sa.String(length=160), nullable=True),
        sa.Column('veiculo_tipo', sa.String(length=80), nullable=True),
        sa.Column('veiculo_placa', sa.String(length=20), nullable=True),
        sa.Column('motorista_nome', sa.String(length=120), nullable=True),
        sa.Column('empresa_terceirizada', sa.String(length=150), nullable=True),
        sa.Column('nota_fiscal_numero', sa.String(length=60), nullable=True),
        sa.Column('nota_fiscal_chave', sa.String(length=120), nullable=True),
        sa.Column('nota_fiscal_emitida_em', sa.DateTime(), nullable=True),
        sa.Column('saiu_para_entrega_em', sa.DateTime(), nullable=True),
        sa.Column('entrega_concluida_em', sa.DateTime(), nullable=True),
    ])
    _create_index_if_missing('pedidos', 'ix_pedidos_status_criado_em', ['status', 'criado_em'])
    _create_index_if_missing('pedidos', 'ix_pedidos_status_fechado_em', ['status', 'fechado_em'])

    _add_columns_if_missing('produtos', [
        sa.Column('tipo_movimentacao', sa.String(length=20), nullable=True, server_default='manual'),
        sa.Column('fora_picking', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('prioridade_reabastecimento', sa.Integer(), nullable=True),
        sa.Column('ultima_baixa_picking_em', sa.DateTime(), nullable=True),
        sa.Column('servico_montagem_disponivel', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('servico_instalacao_disponivel', sa.Boolean(), nullable=True, server_default=sa.false()),
    ])
    _create_index_if_missing('produtos', 'ix_produtos_categoria_fornecedor', ['categoria_id', 'fornecedor_id'])
    _create_index_if_missing('produtos', 'ix_produtos_endereco_ativo', ['endereco_id', 'ativo'])

    _add_columns_if_missing('recebimentos_fornecedor', [
        sa.Column('tipo_recebimento', sa.String(length=40), nullable=True, server_default='compra_revenda'),
        sa.Column('local_recebimento_id', sa.Integer(), nullable=True),
        sa.Column('recebedor_funcionario_id', sa.Integer(), nullable=True),
    ])
    _create_index_if_missing('recebimentos_fornecedor', 'ix_recebimentos_status_criado_em', ['status', 'criado_em'])
    _create_index_if_missing('recebimentos_fornecedor', 'ix_recebimentos_fornecedor_criado_em', ['fornecedor_id', 'criado_em'])

    _add_columns_if_missing('ordens_servico', [
        sa.Column('pedido_id', sa.Integer(), nullable=True),
        sa.Column('iniciado_em', sa.DateTime(), nullable=True),
        sa.Column('retorno_tecnico', sa.Text(), nullable=True),
    ])


def downgrade():
    pass
