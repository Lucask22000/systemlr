import os
import unittest

os.environ['FLASK_CONFIG'] = 'testing'

from app import app, db, sincronizar_garcom_funcionario  # noqa: E402
from models import AssistenteLocalFeedback, AuditoriaEvento, Caixa, Categoria, EmpresaConfig, EnderecoEstoque, Estoque, Fornecedor, Funcionario, Garcom, Mesa, Movimentacao, Pedido, PermissaoAcesso, Produto, RecebimentoFornecedor  # noqa: E402


class SystemFlowsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()

        self.funcionario = Funcionario(nome='Admin', email='admin@test.local', role='admin', ativo=True)
        self.funcionario.set_password('123456')
        db.session.add(self.funcionario)

        self.categoria = Categoria(nome='Bebidas', descricao='Categoria de teste')
        db.session.add(self.categoria)
        db.session.flush()

        self.produto = Produto(
            codigo='P001',
            nome='Refrigerante',
            categoria_id=self.categoria.id,
            preco_custo=4.0,
            preco_venda=10.0,
            quantidade_estoque=10,
            quantidade_minima=2,
            ativo=True,
        )
        db.session.add(self.produto)

        self.caixa = Caixa(
            nome='Caixa 1',
            saldo_inicial=100.0,
            saldo_atual=100.0,
            aberto=True,
            funcionario_id=None,
        )
        db.session.add(self.caixa)
        db.session.commit()

        self.csrf_token = 'test-csrf-token'
        with self.client.session_transaction() as sess:
            sess['funcionario_id'] = self.funcionario.id
            sess['funcionario_nome'] = self.funcionario.nome
            sess['funcionario_role'] = self.funcionario.role
            sess['_csrf_token'] = self.csrf_token

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_api_requires_authentication(self):
        with self.client.session_transaction() as sess:
            sess.clear()

        response = self.client.get('/api/dashboard/analytics')
        self.assertEqual(response.status_code, 401)
        payload = response.get_json()
        self.assertFalse(payload['success'])

    def test_csrf_required_for_api_write(self):
        response = self.client.post('/api/pedidos/criar', json={
            'caixa_id': self.caixa.id,
            'itens': [{'produto_id': self.produto.id, 'quantidade': 1}],
        })
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.assertFalse(payload['success'])
        self.assertEqual(payload.get('code'), 'csrf_invalid')

    def test_order_close_is_immutable_and_updates_stock_and_cash_once(self):
        headers = {'X-CSRF-Token': self.csrf_token}

        create_response = self.client.post('/api/pedidos/criar', json={
            'caixa_id': self.caixa.id,
            'itens': [{'produto_id': self.produto.id, 'quantidade': 2}],
        }, headers=headers)
        self.assertEqual(create_response.status_code, 200)
        create_payload = create_response.get_json()
        self.assertTrue(create_payload['success'])
        pedido_id = create_payload['data']['pedido_id']

        pedido = Pedido.query.get(pedido_id)
        self.assertEqual(float(pedido.total), 20.0)
        self.assertFalse(pedido.estoque_processado)
        self.assertFalse(pedido.financeiro_processado)

        finalize_response = self.client.post(f'/api/pedidos/{pedido_id}/finalizar', json={
            'metodo_pagamento': 'dinheiro',
            'valor_pago': 20.0,
        }, headers=headers)
        self.assertEqual(finalize_response.status_code, 200)
        finalize_payload = finalize_response.get_json()
        self.assertTrue(finalize_payload['success'])

        db.session.refresh(self.produto)
        db.session.refresh(self.caixa)
        db.session.refresh(pedido)

        self.assertEqual(self.produto.quantidade_estoque, 8)
        self.assertEqual(float(self.caixa.saldo_atual), 120.0)
        self.assertEqual(pedido.status, 'fechado')
        self.assertTrue(pedido.estoque_processado)
        self.assertTrue(pedido.financeiro_processado)

        finalize_again_response = self.client.post(f'/api/pedidos/{pedido_id}/finalizar', json={
            'metodo_pagamento': 'dinheiro',
            'valor_pago': 20.0,
        }, headers=headers)
        self.assertEqual(finalize_again_response.status_code, 409)

        reopen_response = self.client.post(f'/pedidos/{pedido_id}/status', data={
            'status': 'aberto',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(reopen_response.status_code, 302)
        db.session.refresh(pedido)
        self.assertEqual(pedido.status, 'fechado')

    def test_access_control_blocks_order_api_when_page_not_permitted(self):
        gerente = Funcionario(
            nome='Gerente Restrito',
            email='gerente@test.local',
            role='gerente',
            ativo=True,
            controle_acesso_ativo=True,
        )
        gerente.set_password('123456')
        db.session.add(gerente)
        db.session.flush()
        db.session.add(PermissaoAcesso(funcionario_id=gerente.id, pagina='inicio'))
        db.session.commit()

        with self.client.session_transaction() as sess:
            sess['funcionario_id'] = gerente.id
            sess['funcionario_nome'] = gerente.nome
            sess['funcionario_role'] = gerente.role
            sess['_csrf_token'] = self.csrf_token

        response = self.client.post('/api/pedidos/criar', json={
            'caixa_id': self.caixa.id,
            'itens': [{'produto_id': self.produto.id, 'quantidade': 1}],
        }, headers={'X-CSRF-Token': self.csrf_token})

        self.assertEqual(response.status_code, 403)
        payload = response.get_json()
        self.assertFalse(payload['success'])
        self.assertEqual(payload.get('code'), 'forbidden')

    def test_waiter_profile_is_disabled_when_role_changes(self):
        funcionario = Funcionario(
            nome='Garcom Teste',
            email='garcom@test.local',
            role='garcom',
            cargo='Garcom',
            ativo=True,
        )
        funcionario.set_password('123456')
        db.session.add(funcionario)
        db.session.flush()

        sincronizar_garcom_funcionario(funcionario)
        db.session.commit()

        garcom = Garcom.query.filter_by(funcionario_id=funcionario.id).first()
        self.assertIsNotNone(garcom)
        self.assertTrue(garcom.ativo)

        funcionario.role = 'caixa'
        funcionario.cargo = 'Caixa'
        sincronizar_garcom_funcionario(funcionario)
        db.session.commit()

        db.session.refresh(garcom)
        self.assertFalse(garcom.ativo)

    def test_order_api_ignores_table_when_waiter_table_module_is_disabled(self):
        empresa = EmpresaConfig(atendimento_mesas_ativo=False)
        mesa = Mesa(numero='99', capacidade=4, status='livre', qr_token='mesa-99')
        db.session.add(empresa)
        db.session.add(mesa)
        db.session.commit()

        headers = {'X-CSRF-Token': self.csrf_token}
        response = self.client.post('/api/pedidos/criar', json={
            'caixa_id': self.caixa.id,
            'mesa_id': mesa.id,
            'itens': [{'produto_id': self.produto.id, 'quantidade': 1}],
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])

        pedido_id = payload['data']['pedido_id']
        pedido = Pedido.query.get(pedido_id)
        self.assertIsNone(pedido.mesa_id)
        self.assertIsNone(pedido.garcom_id)

    def test_public_qr_routes_return_404_when_waiter_table_module_is_disabled(self):
        empresa = EmpresaConfig(atendimento_mesas_ativo=False)
        mesa = Mesa(numero='10', capacidade=4, status='livre', qr_token='mesa-publica-10')
        db.session.add(empresa)
        db.session.add(mesa)
        db.session.commit()

        response = self.client.get(f'/m/{mesa.qr_token}')
        self.assertEqual(response.status_code, 404)

    def test_stock_address_creation_requires_and_accepts_csrf(self):
        estoque = Estoque(nome='CD Principal', ativo=True)
        db.session.add(estoque)
        db.session.commit()

        without_csrf = self.client.post('/enderecos-estoque/novo', data={
            'estoque_id': estoque.id,
            'nome': 'Deposito Central',
            'loja_cd': 'LJ01',
            'setor_zona': 'deposito',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Deposito Central',
            'controle_validade': 'nenhum',
            'cidade': 'Cuiaba',
            'estado': 'MT',
            'ativo': 'on',
        })
        self.assertEqual(without_csrf.status_code, 400)

        with_csrf = self.client.post('/enderecos-estoque/novo', data={
            'estoque_id': estoque.id,
            'nome': 'Deposito Central',
            'loja_cd': 'LJ01',
            'setor_zona': 'deposito',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Deposito Central',
            'controle_validade': 'nenhum',
            'cidade': 'Cuiaba',
            'estado': 'MT',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(with_csrf.status_code, 302)

        endereco = EnderecoEstoque.query.filter_by(nome='Deposito Central').first()
        self.assertIsNotNone(endereco)
        self.assertEqual(endereco.estoque_id, estoque.id)
        self.assertEqual(endereco.estado, 'MT')
        self.assertTrue(endereco.ativo)

    def test_local_ai_status_endpoint_returns_available_mode(self):
        response = self.client.get('/api/assistente-local/status')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])
        self.assertIn(payload['data']['mode'], {'lexical', 'semantic'})
        self.assertGreater(payload['data']['document_count'], 0)

    def test_local_ai_question_returns_answer_and_actions(self):
        response = self.client.post('/api/assistente-local/perguntar', json={
            'pergunta': 'Como registrar um recebimento?',
            'endpoint_atual': 'listar_recebimentos_fornecedor',
            'tela_atual': 'Central de Recebimentos',
        }, headers={'X-CSRF-Token': self.csrf_token})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])
        self.assertTrue(payload['data']['answer'])
        self.assertTrue(payload['data']['actions'])
        self.assertTrue(payload['data']['response_id'])
        self.assertTrue(payload['data']['matched_doc_ids'])

    def test_local_ai_follow_up_uses_recent_history_context(self):
        response = self.client.post('/api/assistente-local/perguntar', json={
            'pergunta': 'E depois?',
            'endpoint_atual': 'listar_recebimentos_fornecedor',
            'tela_atual': 'Central de Recebimentos',
            'historico': [
                {'role': 'user', 'text': 'Como registrar um recebimento?'},
                {'role': 'assistant', 'text': 'Abra a Central de Recebimentos e siga o fluxo.'},
            ],
        }, headers={'X-CSRF-Token': self.csrf_token})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])
        self.assertIn('recebimento', payload['data']['answer'].lower())

    def test_local_ai_greeting_returns_conversational_reply_without_actions(self):
        response = self.client.post('/api/assistente-local/perguntar', json={
            'pergunta': 'bom dia',
            'endpoint_atual': 'dashboard',
            'tela_atual': 'Dashboard',
        }, headers={'X-CSRF-Token': self.csrf_token})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])
        self.assertEqual(payload['data']['answer'], 'Bom dia! Em que posso ajudar?')
        self.assertEqual(payload['data']['actions'], [])
        self.assertEqual(payload['data']['matched_doc_ids'], [])

    def test_local_ai_feedback_endpoint_persists_and_updates_vote(self):
        pergunta = self.client.post('/api/assistente-local/perguntar', json={
            'pergunta': 'Nao consigo liberar um pedido para roteirizacao',
            'endpoint_atual': 'listar_roteirizacao_entrega',
            'tela_atual': 'Roteirizacao',
        }, headers={'X-CSRF-Token': self.csrf_token})
        self.assertEqual(pergunta.status_code, 200)
        payload = pergunta.get_json()
        response_id = payload['data']['response_id']

        primeiro_feedback = self.client.post('/api/assistente-local/feedback', json={
            'response_id': response_id,
            'vote': 'dislike',
            'question_text': 'Nao consigo liberar um pedido para roteirizacao',
            'answer_text': payload['data']['answer'],
            'endpoint_atual': 'listar_roteirizacao_entrega',
            'tela_atual': 'Roteirizacao',
            'matched_doc_ids': payload['data']['matched_doc_ids'],
        }, headers={'X-CSRF-Token': self.csrf_token})
        self.assertEqual(primeiro_feedback.status_code, 200)

        registro = AssistenteLocalFeedback.query.filter_by(
            funcionario_id=self.funcionario.id,
            response_id=response_id,
        ).first()
        self.assertIsNotNone(registro)
        self.assertEqual(registro.vote, 'dislike')

        segundo_feedback = self.client.post('/api/assistente-local/feedback', json={
            'response_id': response_id,
            'vote': 'like',
            'question_text': 'Nao consigo liberar um pedido para roteirizacao',
            'answer_text': payload['data']['answer'],
            'endpoint_atual': 'listar_roteirizacao_entrega',
            'tela_atual': 'Roteirizacao',
            'matched_doc_ids': payload['data']['matched_doc_ids'],
        }, headers={'X-CSRF-Token': self.csrf_token})
        self.assertEqual(segundo_feedback.status_code, 200)

        registros = AssistenteLocalFeedback.query.filter_by(
            funcionario_id=self.funcionario.id,
            response_id=response_id,
        ).all()
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0].vote, 'like')

    def test_stock_analytics_api_returns_success(self):
        response = self.client.get('/api/estoque/analytics?periodo=30')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])
        self.assertEqual(payload['data']['periodo_dias'], 30)

    def test_multiple_stocks_can_be_created_and_linked_to_addresses(self):
        create_a = self.client.post('/estoques/novo', data={
            'nome': 'CD Norte',
            'descricao': 'Centro de distribuicao norte',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        create_b = self.client.post('/estoques/novo', data={
            'nome': 'CD Sul',
            'descricao': 'Centro de distribuicao sul',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(create_a.status_code, 302)
        self.assertEqual(create_b.status_code, 302)

        estoque_a = Estoque.query.filter_by(nome='CD Norte').first()
        estoque_b = Estoque.query.filter_by(nome='CD Sul').first()
        self.assertIsNotNone(estoque_a)
        self.assertIsNotNone(estoque_b)

        addr_a = self.client.post('/enderecos-estoque/novo', data={
            'estoque_id': estoque_a.id,
            'nome': 'Rua A',
            'loja_cd': 'LJ01',
            'setor_zona': 'deposito',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Rua A',
            'controle_validade': 'nenhum',
            'cidade': 'Cuiaba',
            'estado': 'MT',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        addr_b = self.client.post('/enderecos-estoque/novo', data={
            'estoque_id': estoque_b.id,
            'nome': 'Rua B',
            'loja_cd': 'LJ01',
            'setor_zona': 'deposito',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Rua B',
            'controle_validade': 'nenhum',
            'cidade': 'Cuiaba',
            'estado': 'MT',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(addr_a.status_code, 302)
        self.assertEqual(addr_b.status_code, 302)

        end_a = EnderecoEstoque.query.filter_by(nome='Rua A').first()
        end_b = EnderecoEstoque.query.filter_by(nome='Rua B').first()
        self.assertEqual(end_a.estoque_id, estoque_a.id)
        self.assertEqual(end_b.estoque_id, estoque_b.id)

    def test_bulk_store_products_distributes_items_across_stock_addresses(self):
        produto_2 = Produto(
            codigo='P002',
            nome='Agua',
            categoria_id=self.categoria.id,
            preco_custo=2.0,
            preco_venda=5.0,
            quantidade_estoque=20,
            quantidade_minima=3,
            ativo=True,
        )
        db.session.add(produto_2)

        estoque = Estoque(nome='CD Bulk', ativo=True)
        db.session.add(estoque)
        db.session.flush()

        endereco_a = EnderecoEstoque(nome='CD Bulk A', estoque_id=estoque.id, cidade='Cuiaba', estado='MT', ativo=True)
        endereco_b = EnderecoEstoque(nome='CD Bulk B', estoque_id=estoque.id, cidade='Cuiaba', estado='MT', ativo=True)
        db.session.add(endereco_a)
        db.session.add(endereco_b)
        db.session.commit()

        response = self.client.post('/produtos/enderecos/armazenar-todos', data={
            'estoque_id': estoque.id,
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(response.status_code, 302)

        db.session.refresh(self.produto)
        db.session.refresh(produto_2)
        self.assertIn(self.produto.endereco_id, {endereco_a.id, endereco_b.id})
        self.assertIn(produto_2.endereco_id, {endereco_a.id, endereco_b.id})
        self.assertNotEqual(self.produto.endereco_id, produto_2.endereco_id)

    def test_audit_log_area_registers_mutation_events(self):
        response = self.client.post('/estoques/novo', data={
            'nome': 'CD Auditoria',
            'descricao': 'Teste de log',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(response.status_code, 302)

        eventos = AuditoriaEvento.query.filter(
            AuditoriaEvento.rota == '/estoques/novo',
            AuditoriaEvento.metodo == 'POST'
        ).all()
        self.assertTrue(len(eventos) >= 1)

        audit_page = self.client.get('/auditoria')
        self.assertEqual(audit_page.status_code, 200)

    def test_new_movement_requires_supplier_when_receiving_from_supplier(self):
        fornecedor = Fornecedor(nome='Fornecedor X', ativo=True)
        db.session.add(fornecedor)
        db.session.commit()

        sem_fornecedor = self.client.post('/movimentacoes/nova', data={
            'produto_id': self.produto.id,
            'tipo': 'entrada',
            'quantidade': 2,
            'recebimento_fornecedor': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(sem_fornecedor.status_code, 302)
        self.assertEqual(Movimentacao.query.count(), 0)

        com_fornecedor = self.client.post('/movimentacoes/nova', data={
            'produto_id': self.produto.id,
            'tipo': 'entrada',
            'quantidade': 2,
            'recebimento_fornecedor': 'on',
            'fornecedor_id': fornecedor.id,
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(com_fornecedor.status_code, 302)
        self.assertEqual(Movimentacao.query.count(), 1)

        mov = Movimentacao.query.first()
        self.assertEqual(mov.fornecedor_id, fornecedor.id)
        self.assertEqual(mov.motivo, 'recebimento_fornecedor')

    def test_recebimento_put_away_updates_stock_only_on_armazenagem(self):
        fornecedor = Fornecedor(nome='Fornecedor PutAway', ativo=True)
        estoque = Estoque(nome='CD Recebimento', ativo=True)
        db.session.add(fornecedor)
        db.session.add(estoque)
        db.session.flush()

        endereco = EnderecoEstoque(
            estoque_id=estoque.id,
            nome='Endereco Recebimento A',
            loja_cd='LJ01',
            setor_zona='deposito',
            tipo_area='recebimento',
            status='ativo',
            tipo_estrutura='rack',
            codigo_armazem='LJ01',
            rua_corredor='03',
            coluna_baia='02',
            nivel_prateleira='01',
            posicao_slot='08',
            lado='LA',
            controle_validade='fifo',
            codigo_localizacao='LJ01-DEP-R03-RK02-N01-V08-LA',
            ativo=True,
        )
        db.session.add(endereco)
        db.session.commit()

        estoque_inicial = self.produto.quantidade_estoque
        create_response = self.client.post('/estoque/recebimentos/novo', data={
            'fornecedor_id': fornecedor.id,
            'tipo_recebimento': RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
            'local_recebimento_id': endereco.id,
            'info_nota': 'NF 123',
            'produto_id[]': [self.produto.id],
            'qtd_recebida[]': ['5'],
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(create_response.status_code, 302)

        recebimento = RecebimentoFornecedor.query.order_by(RecebimentoFornecedor.id.desc()).first()
        self.assertIsNotNone(recebimento)
        self.assertEqual(recebimento.status, RecebimentoFornecedor.STATUS_CRIADO)

        db.session.refresh(self.produto)
        self.assertEqual(self.produto.quantidade_estoque, estoque_inicial)

        item = recebimento.itens[0]
        conferir_response = self.client.post(f'/estoque/recebimentos/{recebimento.id}/conferir', data={
            f'item_{item.id}_qtd_recebida': '5',
            f'item_{item.id}_qtd_avaria': '1',
            f'item_{item.id}_lote': 'L001',
            f'item_{item.id}_validade': '2027-12-31',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(conferir_response.status_code, 302)

        db.session.refresh(recebimento)
        db.session.refresh(self.produto)
        self.assertEqual(recebimento.status, RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM)
        self.assertEqual(self.produto.quantidade_estoque, estoque_inicial)

        armazenar_response = self.client.post(f'/estoque/recebimentos/{recebimento.id}/armazenar', data={
            f'endereco_destino_{item.id}': endereco.id,
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(armazenar_response.status_code, 302)

        db.session.refresh(recebimento)
        db.session.refresh(self.produto)
        self.assertEqual(recebimento.status, RecebimentoFornecedor.STATUS_CONCLUIDO)
        self.assertEqual(self.produto.quantidade_estoque, estoque_inicial + 4)

        mov = Movimentacao.query.filter_by(motivo='recebimento_fornecedor').first()
        self.assertIsNotNone(mov)
        self.assertEqual(mov.fornecedor_id, fornecedor.id)
        self.assertEqual(mov.endereco_destino_id, endereco.id)
        self.assertEqual(mov.quantidade, 4)

    def test_recebimento_multiplos_fornecedores_e_armazenagem_em_enderecos(self):
        produto_2 = Produto(
            codigo='P200',
            nome='Arroz 5Kg',
            categoria_id=self.categoria.id,
            preco_custo=20.0,
            preco_venda=29.9,
            quantidade_estoque=30,
            quantidade_minima=5,
            ativo=True,
        )
        produto_3 = Produto(
            codigo='P300',
            nome='Cafe 500g',
            categoria_id=self.categoria.id,
            preco_custo=9.0,
            preco_venda=14.9,
            quantidade_estoque=15,
            quantidade_minima=4,
            ativo=True,
        )
        db.session.add(produto_2)
        db.session.add(produto_3)

        estoque = Estoque(nome='CD Multi Forn', ativo=True)
        db.session.add(estoque)
        db.session.flush()

        endereco_a = EnderecoEstoque(
            estoque_id=estoque.id,
            nome='Rack A',
            loja_cd='LJ01',
            setor_zona='deposito',
            tipo_area='recebimento',
            status='ativo',
            tipo_estrutura='rack',
            codigo_armazem='LJ01',
            rua_corredor='01',
            coluna_baia='01',
            nivel_prateleira='01',
            posicao_slot='01',
            lado='LA',
            controle_validade='fifo',
            codigo_localizacao='LJ01-DEP-R01-RK01-N01-V01-LA',
            ativo=True,
        )
        endereco_b = EnderecoEstoque(
            estoque_id=estoque.id,
            nome='Rack B',
            loja_cd='LJ01',
            setor_zona='deposito',
            tipo_area='recebimento',
            status='ativo',
            tipo_estrutura='rack',
            codigo_armazem='LJ01',
            rua_corredor='01',
            coluna_baia='02',
            nivel_prateleira='01',
            posicao_slot='02',
            lado='LB',
            controle_validade='fifo',
            codigo_localizacao='LJ01-DEP-R01-RK02-N01-V02-LB',
            ativo=True,
        )
        db.session.add(endereco_a)
        db.session.add(endereco_b)

        fornecedores = [
            Fornecedor(nome='Fornecedor Alfa', ativo=True),
            Fornecedor(nome='Fornecedor Beta', ativo=True),
            Fornecedor(nome='Fornecedor Gama', ativo=True),
        ]
        for fornecedor in fornecedores:
            db.session.add(fornecedor)
        db.session.commit()

        produtos = [self.produto, produto_2, produto_3]
        estoque_inicial = {p.id: p.quantidade_estoque for p in produtos}
        totais_liquidos = {p.id: 0 for p in produtos}

        for idx, fornecedor in enumerate(fornecedores):
            produto = produtos[idx]
            qtd_recebida = 8 + idx
            qtd_avaria = 1
            destino = endereco_a if idx % 2 == 0 else endereco_b

            criar = self.client.post('/estoque/recebimentos/novo', data={
                'fornecedor_id': fornecedor.id,
                'tipo_recebimento': RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
                'local_recebimento_id': destino.id,
                'info_nota': f'NF-MULTI-{idx + 1}',
                'produto_id[]': [produto.id],
                'qtd_recebida[]': [str(qtd_recebida)],
                'csrf_token': self.csrf_token,
            })
            self.assertEqual(criar.status_code, 302)

            recebimento = RecebimentoFornecedor.query.filter_by(info_nota=f'NF-MULTI-{idx + 1}').first()
            self.assertIsNotNone(recebimento)
            item = recebimento.itens[0]

            conferir = self.client.post(f'/estoque/recebimentos/{recebimento.id}/conferir', data={
                f'item_{item.id}_qtd_recebida': str(qtd_recebida),
                f'item_{item.id}_qtd_avaria': str(qtd_avaria),
                f'item_{item.id}_lote': f'LOTE-{idx + 1}',
                f'item_{item.id}_validade': '2028-01-30',
                'csrf_token': self.csrf_token,
            })
            self.assertEqual(conferir.status_code, 302)

            armazenar = self.client.post(f'/estoque/recebimentos/{recebimento.id}/armazenar', data={
                f'endereco_destino_{item.id}': destino.id,
                'csrf_token': self.csrf_token,
            })
            self.assertEqual(armazenar.status_code, 302)

            db.session.refresh(recebimento)
            self.assertEqual(recebimento.status, RecebimentoFornecedor.STATUS_CONCLUIDO)
            totais_liquidos[produto.id] += (qtd_recebida - qtd_avaria)

        for produto in produtos:
            db.session.refresh(produto)
            self.assertEqual(produto.quantidade_estoque, estoque_inicial[produto.id] + totais_liquidos[produto.id])
            self.assertIn(produto.endereco_id, {endereco_a.id, endereco_b.id})

        movimentos_recebimento = Movimentacao.query.filter_by(motivo='recebimento_fornecedor').all()
        self.assertEqual(len(movimentos_recebimento), 3)


if __name__ == '__main__':
    unittest.main()
