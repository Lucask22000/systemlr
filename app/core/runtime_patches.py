"""Runtime schema patches isolados do bootstrap principal.

Permite manter app/__init__.py mais enxuto sem alterar o comportamento legado.
"""

import os

from sqlalchemy import inspect, text


def runtime_schema_patches_enabled(*, app):
    configurado = os.environ.get('SYSTEMLR_ENABLE_RUNTIME_SCHEMA_PATCHES')
    if configurado is None:
        return app.config.get('ENV_NAME') == 'testing'
    return configurado.strip().lower() in {'1', 'true', 'yes', 'on'}


def _safe_execute(db, statement):
    try:
        db.session.execute(statement)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


def _add_column_if_missing(db, inspector, table_name, columns, column_name, definition):
    if column_name in columns:
        return
    _safe_execute(db, text(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}'))


def _add_missing_columns_bulk(db, inspector, table_name, columns_map):
    if not inspector.has_table(table_name):
        return
    columns = {col['name'] for col in inspector.get_columns(table_name)}
    for column_name, definition in columns_map.items():
        _add_column_if_missing(db, inspector, table_name, columns, column_name, definition)


def apply_runtime_schema_patches(
    *,
    app,
    db,
    perfil_acesso_model,
    processo_evento_model,
    cliente_publico_model,
    lancamento_financeiro_model,
    fundo_solicitacao_model,
    equipamento_movimentacao_model,
    manutencao_equipamento_model,
    ordem_servico_model,
    chamado_interno_model,
    almoxarifado_atribuicao_model,
    assistente_local_feedback_model,
    funcionario_estoques_table,
):
    with app.app_context():
        inspector = inspect(db.engine)
        if not runtime_schema_patches_enabled(app=app):
            return

        app.logger.warning(
            'Runtime schema patches habilitados. Use apenas como contingencia temporaria e aplique '
            '`flask db upgrade` para manter o schema via migrations formais.'
        )

        if inspector.has_table('funcoes_rh'):
            colunas_funcoes = {col['name'] for col in inspector.get_columns('funcoes_rh')}
            if 'permissoes_padrao' not in colunas_funcoes:
                _safe_execute(db, text('ALTER TABLE funcoes_rh ADD COLUMN permissoes_padrao TEXT'))

        if not inspector.has_table('perfis_acesso'):
            perfil_acesso_model.__table__.create(bind=db.engine, checkfirst=True)
        if not inspector.has_table('processo_eventos'):
            processo_evento_model.__table__.create(bind=db.engine, checkfirst=True)

        if inspector.has_table('funcionarios'):
            colunas_funcionarios = {col['name'] for col in inspector.get_columns('funcionarios')}
            if 'superior_id' not in colunas_funcionarios:
                _safe_execute(db, text('ALTER TABLE funcionarios ADD COLUMN superior_id INTEGER'))

            colunas_novas_funcionarios = {
                'numero_cadastro': 'INTEGER',
                'matricula': 'VARCHAR(30)',
                'cpf': 'VARCHAR(14)',
                'rg': 'VARCHAR(20)',
                'data_nascimento': 'DATE',
                'celular': 'VARCHAR(30)',
                'cep': 'VARCHAR(12)',
                'endereco': 'VARCHAR(180)',
                'bairro': 'VARCHAR(100)',
                'cidade': 'VARCHAR(100)',
                'estado': 'VARCHAR(2)',
                'imagem_perfil_path': 'VARCHAR(255)',
                'permitir_editar_imagem_perfil': 'INTEGER DEFAULT 0',
                'senha_provisoria': 'INTEGER DEFAULT 0',
                'departamento': 'VARCHAR(80)',
                'time_nome': 'VARCHAR(80)',
                'nivel_organograma': 'VARCHAR(40)',
                'pagina_inicial': "VARCHAR(30) DEFAULT 'dashboard'",
                'receber_alertas': 'INTEGER DEFAULT 1',
                'restricao_estoques_ativa': 'INTEGER DEFAULT 0',
                'estoque_principal_id': 'INTEGER',
                'perfil_acesso_id': 'INTEGER',
            }
            for coluna_nome, definicao in colunas_novas_funcionarios.items():
                _add_column_if_missing(db, inspector, 'funcionarios', colunas_funcionarios, coluna_nome, definicao)

        if inspector.has_table('permissoes_acesso'):
            colunas_permissoes_acesso = {col['name'] for col in inspector.get_columns('permissoes_acesso')}
            if 'permitido' not in colunas_permissoes_acesso:
                _safe_execute(db, text('ALTER TABLE permissoes_acesso ADD COLUMN permitido INTEGER DEFAULT 1'))

        _add_missing_columns_bulk(db, inspector, 'estoques', {
            'codigo_filial': 'VARCHAR(20)',
        })

        _add_missing_columns_bulk(db, inspector, 'movimentacoes', {
            'pedido_id': 'INTEGER',
            'recebimento_id': 'INTEGER',
        })

        _add_missing_columns_bulk(db, inspector, 'lancamentos_financeiros', {
            'pedido_id': 'INTEGER',
            'recebimento_id': 'INTEGER',
        })

        _add_missing_columns_bulk(db, inspector, 'empresa_config', {
            'codigo_empresa': 'VARCHAR(20)',
            'favicon_path': 'VARCHAR(255)',
            'app_icon_path': 'VARCHAR(255)',
            'separacao_entrega_ativa': 'INTEGER DEFAULT 1',
            'emissao_etiqueta_entrega_ativa': 'INTEGER DEFAULT 1',
            'separacao_entrega_unir_vendas_off': 'INTEGER DEFAULT 0',
            'roteirizacao_entrega_ativa': 'INTEGER DEFAULT 1',
            'emissao_nota_entrega_ativa': 'INTEGER DEFAULT 1',
            'entrega_local_saida_padrao': 'VARCHAR(160)',
            'entrega_veiculo_padrao': 'VARCHAR(80)',
            'entrega_motorista_padrao': 'VARCHAR(120)',
            'entrega_horario_fechamento_roteirizacao': 'VARCHAR(5)',
            'entrega_veiculos_json': 'TEXT',
            'entrega_terceirizadas_json': 'TEXT',
            'entrega_regras_roteirizacao_json': 'TEXT',
            'servicos_tecnicos_ativos': 'INTEGER DEFAULT 0',
            'servico_montagem_instalacao_ativo': 'INTEGER DEFAULT 0',
            'tipo_negocio': "VARCHAR(30) DEFAULT 'conveniencia'",
            'canal_operacao': "VARCHAR(30) DEFAULT 'hibrido'",
            'ecommerce_ativo': 'INTEGER DEFAULT 1',
            'ecom_cor_primaria': "VARCHAR(20) DEFAULT '#ff7848'",
            'ecom_cor_secundaria': "VARCHAR(20) DEFAULT '#ff5a2a'",
            'ecom_card_bg': "VARCHAR(20) DEFAULT '#ffffff'",
            'ecom_titulo_banner': 'VARCHAR(140)',
            'ecom_subtitulo_banner': 'VARCHAR(255)',
            'ecom_texto_promocao': 'VARCHAR(255)',
            'ecom_banner_path': 'VARCHAR(255)',
            'ecom_favicon_path': 'VARCHAR(255)',
            'ecom_produto_placeholder_path': 'VARCHAR(255)',
            'ecom_banners_json': 'TEXT',
            'ecom_campanhas_json': 'TEXT',
            'ecom_cupons_json': 'TEXT',
            'ecom_footer_bg': "VARCHAR(20) DEFAULT '#1f2b38'",
            'ecom_footer_texto': 'VARCHAR(255)',
            'ecom_footer_contato': 'VARCHAR(255)',
            'ecom_footer_creditos': 'VARCHAR(255)',
            'pagamentos_pdv_json': 'TEXT',
            'pagamentos_ecommerce_json': 'TEXT',
            'integracoes_pdv_json': 'TEXT',
            'integracoes_ecommerce_json': 'TEXT',
            'reposicao_loja_fisica_ativa': 'INTEGER DEFAULT 1',
            'emissao_etiqueta_loja_ativa': 'INTEGER DEFAULT 1',
            'emissao_etiqueta_endereco_ativa': 'INTEGER DEFAULT 1',
        })

        if not inspector.has_table('funcionario_estoques'):
            funcionario_estoques_table.create(bind=db.engine, checkfirst=True)

        _add_missing_columns_bulk(db, inspector, 'pedidos', {
            'cliente_publico_id': 'INTEGER',
            'codigo_rastreio': 'VARCHAR(100)',
            'transportadora': 'VARCHAR(100)',
            'data_estimada_entrega': 'DATE',
            'separacao_entrega_concluida': 'INTEGER DEFAULT 0',
            'separacao_entrega_em': 'DATETIME',
            'etiqueta_entrega_emitida_em': 'DATETIME',
            'rota_entrega': 'VARCHAR(120)',
            'ordem_rota': 'INTEGER',
            'local_saida': 'VARCHAR(160)',
            'veiculo_tipo': 'VARCHAR(80)',
            'veiculo_placa': 'VARCHAR(20)',
            'motorista_nome': 'VARCHAR(120)',
            'empresa_terceirizada': 'VARCHAR(150)',
            'nota_fiscal_numero': 'VARCHAR(60)',
            'nota_fiscal_chave': 'VARCHAR(120)',
            'nota_fiscal_emitida_em': 'DATETIME',
            'saiu_para_entrega_em': 'DATETIME',
            'entrega_concluida_em': 'DATETIME',
        })

        _add_missing_columns_bulk(db, inspector, 'produtos', {
            'tipo_movimentacao': "VARCHAR(20) DEFAULT 'manual'",
            'fora_picking': 'INTEGER DEFAULT 0',
            'prioridade_reabastecimento': 'INTEGER',
            'ultima_baixa_picking_em': 'DATETIME',
            'servico_montagem_disponivel': 'INTEGER DEFAULT 0',
            'servico_instalacao_disponivel': 'INTEGER DEFAULT 0',
        })

        if inspector.has_table('recebimentos_fornecedor'):
            colunas_recebimentos = {col['name'] for col in inspector.get_columns('recebimentos_fornecedor')}
            if 'tipo_recebimento' not in colunas_recebimentos:
                _safe_execute(
                    db,
                    text(
                        "ALTER TABLE recebimentos_fornecedor "
                        "ADD COLUMN tipo_recebimento VARCHAR(40) DEFAULT 'compra_revenda'"
                    ),
                )
            if 'local_recebimento_id' not in colunas_recebimentos:
                _safe_execute(
                    db,
                    text(
                        "ALTER TABLE recebimentos_fornecedor "
                        "ADD COLUMN local_recebimento_id INTEGER"
                    ),
                )
            if 'recebedor_funcionario_id' not in colunas_recebimentos:
                _safe_execute(
                    db,
                    text(
                        "ALTER TABLE recebimentos_fornecedor "
                        "ADD COLUMN recebedor_funcionario_id INTEGER"
                    ),
                )

        if not inspector.has_table('clientes_publicos'):
            cliente_publico_model.__table__.create(bind=db.engine, checkfirst=True)
        if not inspector.has_table('lancamentos_financeiros'):
            lancamento_financeiro_model.__table__.create(bind=db.engine, checkfirst=True)
        if not inspector.has_table('fundos_solicitacoes'):
            fundo_solicitacao_model.__table__.create(bind=db.engine, checkfirst=True)
        if not inspector.has_table('equipamentos_movimentacao'):
            equipamento_movimentacao_model.__table__.create(bind=db.engine, checkfirst=True)
        if not inspector.has_table('manutencoes_equipamento'):
            manutencao_equipamento_model.__table__.create(bind=db.engine, checkfirst=True)
        if not inspector.has_table('ordens_servico'):
            ordem_servico_model.__table__.create(bind=db.engine, checkfirst=True)
        else:
            _add_missing_columns_bulk(db, inspector, 'ordens_servico', {
                'pedido_id': 'INTEGER',
                'iniciado_em': 'DATETIME',
                'retorno_tecnico': 'TEXT',
            })
        if not inspector.has_table('chamados_internos'):
            chamado_interno_model.__table__.create(bind=db.engine, checkfirst=True)
        if not inspector.has_table('almoxarifado_atribuicoes'):
            almoxarifado_atribuicao_model.__table__.create(bind=db.engine, checkfirst=True)
        if not inspector.has_table('assistente_local_feedback'):
            assistente_local_feedback_model.__table__.create(bind=db.engine, checkfirst=True)
