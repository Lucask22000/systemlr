from datetime import datetime
import secrets
import qrcode
from io import BytesIO
from flask import render_template, request, redirect, url_for, flash, session, Response, jsonify
from sqlalchemy.orm import selectinload

from models import db, Caixa, Mesa, Pedido, Produto, ItemPedido, Movimentacao, MovimentacaoCaixa, Funcionario, Garcom, EmpresaConfig
from realtime import publish_alert, sse_stream
from security import json_response


METODOS_PAGAMENTO = {'dinheiro', 'cartao', 'pix', 'crediario', 'dividido'}
ORDER_ALLOWED_TRANSITIONS = Pedido.TRANSICOES_PERMITIDAS
ORDER_IMMUTABLE_STATUSES = Pedido.STATUS_IMUTAVEIS
DELIVERY_SEPARATION_STATUSES = {Pedido.STATUS_ABERTO, Pedido.STATUS_EM_PREPARO, Pedido.STATUS_ENTREGUE}


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


def _origens_separacao_entrega(empresa=None):
    empresa = empresa or _obter_empresa_config()
    origens = ['site']
    if empresa.separacao_entrega_unir_vendas_off:
        origens.append('interno')
    return origens


def _bloquear_se_atendimento_mesas_desativado():
    if _atendimento_mesas_ativo():
        return None
    flash('Modulo de mesas e garcons esta desativado para esta empresa.', 'warning')
    return redirect(url_for('pdv'))


def _to_float(valor, default=None):
    if valor is None or valor == '':
        return default
    if isinstance(valor, str):
        valor = valor.replace(',', '.').strip()
    return float(valor)


def _build_payment_data(metodo_raw, valor_raw, total_pedido, split_raw=None, cliente_crediario=''):
    metodo = (metodo_raw or '').strip().lower()
    if metodo not in METODOS_PAGAMENTO:
        raise ValueError('Metodo de pagamento invalido.')
    total = float(total_pedido or 0.0)

    if metodo == 'dividido':
        split_raw = split_raw or {}
        valor_dinheiro = _to_float(split_raw.get('dinheiro'), 0.0) or 0.0
        valor_cartao = _to_float(split_raw.get('cartao'), 0.0) or 0.0
        if valor_dinheiro < 0 or valor_cartao < 0:
            raise ValueError('Valores de pagamento nao podem ser negativos.')
        valor_pago = valor_dinheiro + valor_cartao
        if valor_pago <= 0:
            raise ValueError('Informe ao menos um valor para dinheiro ou cartao.')
        if valor_pago < total:
            raise ValueError('Valor informado insuficiente para finalizar o pedido.')
        metodo_texto = f'dividido (dinheiro: {valor_dinheiro:.2f} | cartao: {valor_cartao:.2f})'
        return metodo_texto, valor_pago

    valor_pago = _to_float(valor_raw, None)
    if valor_pago is None:
        valor_pago = 0.0 if metodo == 'crediario' else float(total_pedido or 0.0)
    if valor_pago < 0:
        raise ValueError('Valor pago nao pode ser negativo.')

    if metodo == 'crediario':
        cliente = (cliente_crediario or '').strip()
        metodo_texto = f'crediario ({cliente})' if cliente else 'crediario'
    else:
        if metodo == 'dinheiro' and valor_pago < total:
            raise ValueError('Valor recebido insuficiente para finalizar o pedido.')
        metodo_texto = metodo

    return metodo_texto, valor_pago


def _garcom_logado_id():
    funcionario_id = session.get('funcionario_id')
    if not funcionario_id:
        return None
    garcom = Garcom.query.filter_by(funcionario_id=funcionario_id, ativo=True).first()
    return garcom.id if garcom else None


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


def _normalizar_item_payload(item):
    produto_id = item.get('produto_id')
    quantidade = item.get('quantidade', 1)
    try:
        produto_id = int(produto_id)
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        return None, 'Item invalido.'
    if quantidade <= 0:
        return None, 'Quantidade deve ser maior que zero.'
    produto = Produto.query.get(produto_id)
    if not produto or not produto.ativo:
        return None, 'Produto invalido ou inativo.'
    return {'produto': produto, 'quantidade': quantidade}, None


def _recalcular_total_pedido(pedido):
    pedido.total = sum((item.quantidade or 0) * (item.preco_unitario or 0) for item in pedido.itens)
    return pedido.total


def _processar_fechamento_pedido(pedido):
    """Aplica regras de negócio para encerrar um pedido.

    - Garante que há itens
    - Calcula total e registra timestamps de fechamento
    - Marca pedido como processado para estoque/financeiro quando aplicável
    """
    if not pedido.itens:
        raise ValueError('Pedido sem itens nao pode ser fechado.')

    if not pedido.estoque_processado:
        for item in pedido.itens:
            produto = item.produto or Produto.query.get(item.produto_id)
            if not produto:
                raise ValueError(f'Produto do item {item.id} nao encontrado.')
            if produto.quantidade_estoque < item.quantidade:
                raise ValueError(f'Estoque insuficiente para "{produto.nome}".')

        for item in pedido.itens:
            produto = item.produto or Produto.query.get(item.produto_id)
            produto.quantidade_estoque -= item.quantidade
            db.session.add(Movimentacao(
                produto_id=produto.id,
                tipo=Movimentacao.TIPO_SAIDA,
                quantidade=item.quantidade,
                motivo='venda',
                observacoes=f'Pedido {pedido.id} fechado'
            ))
        pedido.estoque_processado = True

    if pedido.caixa_id and not pedido.financeiro_processado:
        caixa = pedido.caixa or Caixa.query.get(pedido.caixa_id)
        if not caixa:
            raise ValueError('Caixa do pedido nao encontrada.')
        if not caixa.aberto:
            raise ValueError('Caixa do pedido esta fechada. Nao e possivel concluir o financeiro.')

        valor_pedido = float(pedido.total or 0.0)
        caixa.saldo_atual = float(caixa.saldo_atual or 0.0) + valor_pedido
        db.session.add(MovimentacaoCaixa(
            caixa_id=caixa.id,
            tipo=MovimentacaoCaixa.TIPO_ENTRADA,
            valor=valor_pedido,
            descricao=f'Fechamento do pedido #{pedido.id}'
        ))
        pedido.financeiro_processado = True

    pedido.fechado_em = datetime.utcnow()
    if pedido.mesa:
        pedido.mesa.status = 'livre'


def _aplicar_transicao_status(pedido, novo_status):
    return pedido.transitar_para(novo_status, on_fechamento=_processar_fechamento_pedido)


def register_vendas_routes(app, login_required, require_role):
    vendas_operacao_roles = ('admin', 'gerente', 'caixa', 'operador', 'garcom')
    vendas_gestao_roles = ('admin', 'gerente')
    caixa_operacao_roles = ('admin', 'gerente', 'caixa')
    separacao_entrega_roles = ('admin', 'gerente', 'caixa', 'operador')
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
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        status_filtro = (request.args.get('status') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()

        query = Pedido.query.options(
            selectinload(Pedido.mesa),
            selectinload(Pedido.caixa),
            selectinload(Pedido.garcom)
        )
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

        pedidos = query.order_by(Pedido.criado_em.desc()).paginate(page=page, per_page=per_page, error_out=False)
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
            selectinload(Pedido.caixa),
            selectinload(Pedido.mesa),
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
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
        )

    @app.route('/pedidos/<int:pedido_id>/separacao-entrega', methods=['POST'])
    @require_role(*separacao_entrega_roles)
    def atualizar_separacao_entrega_pedido(pedido_id):
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(request.referrer or url_for('listar_pedidos'))

        pedido = Pedido.query.get_or_404(pedido_id)
        if pedido.origem not in _origens_separacao_entrega(empresa):
            flash('Pedido fora da fila configurada para separacao de entrega.', 'warning')
            return redirect(request.referrer or url_for('listar_separacao_entrega'))

        acao = (request.form.get('acao') or 'concluir').strip().lower()
        try:
            if acao == 'reabrir':
                pedido.marcar_separacao_entrega(False)
                mensagem = f'Pedido #{pedido.id} retornou para fila de separacao.'
            else:
                pedido.marcar_separacao_entrega(True)
                mensagem = f'Pedido #{pedido.id} marcado como separado.'
            db.session.commit()
            flash(mensagem, 'success')
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
        except Exception:
            db.session.rollback()

        return render_template(
            'vendas/pedidos/etiqueta_entrega.html',
            pedido=pedido,
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
            _aplicar_transicao_status(pedido, novo_status)
            db.session.commit()
            status_label = 'venda concluida' if novo_status == 'fechado' else novo_status
            flash(f'Pedido {pedido.id} atualizado para {status_label}.', 'success')
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), 'danger')

        return redirect(request.referrer or url_for('listar_pedidos'))

    @app.route('/pedidos/novo', methods=['GET', 'POST'])
    @require_role(*vendas_operacao_roles)
    def novo_pedido():
        produtos = Produto.query.filter_by(ativo=True).all()
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

                if caixa_id:
                    caixa = Caixa.query.get(caixa_id)
                    if not caixa or not caixa.aberto:
                        flash('Caixa invalida ou fechada.', 'danger')
                        return redirect(url_for('novo_pedido'))

                pedido = Pedido(
                    mesa_id=mesa_id,
                    caixa_id=caixa_id,
                    garcom_id=_garcom_logado_id() if atendimento_mesas_ativo else None,
                    observacoes=observacoes,
                    status='aberto',
                    estoque_processado=False,
                    financeiro_processado=False
                )
                db.session.add(pedido)
                db.session.flush()

                itens_validos = 0
                for i in range(int(request.form.get('item_count', 0))):
                    pid = request.form.get(f'produto_{i}')
                    qty = request.form.get(f'quantidade_{i}', 1)
                    if not pid:
                        continue
                    normalizado, erro = _normalizar_item_payload({'produto_id': pid, 'quantidade': qty})
                    if erro:
                        continue

                    produto = normalizado['produto']
                    quantidade = normalizado['quantidade']
                    ip = ItemPedido(
                        pedido_id=pedido.id,
                        produto_id=produto.id,
                        quantidade=quantidade,
                        preco_unitario=produto.preco_venda
                    )
                    db.session.add(ip)
                    itens_validos += 1

                if itens_validos == 0:
                    raise ValueError('Adicione ao menos um item valido ao pedido.')

                _recalcular_total_pedido(pedido)
                if atendimento_mesas_ativo and pedido.mesa:
                    pedido.mesa.status = 'ocupada'
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
        produtos = Produto.query.filter_by(ativo=True).all()
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        mesas = Mesa.query.all() if atendimento_mesas_ativo else []
        caixas = Caixa.query.all()
        if request.method == 'POST':
            try:
                status_atual = _parse_status(pedido.status)
                novo_status = _parse_status(request.form.get('status', pedido.status), default=status_atual)
                if status_atual in ORDER_IMMUTABLE_STATUSES and novo_status != status_atual:
                    raise ValueError(f'Pedido {status_atual} e imutavel.')

                pedido.mesa_id = request.form.get('mesa_id', type=int) or None
                if not atendimento_mesas_ativo:
                    pedido.mesa_id = None
                    pedido.garcom_id = None
                pedido.caixa_id = request.form.get('caixa_id', type=int) or None
                pedido.observacoes = request.form.get('observacoes', pedido.observacoes)

                if pedido.caixa_id:
                    caixa = Caixa.query.get(pedido.caixa_id)
                    if not caixa:
                        raise ValueError('Caixa informada nao existe.')
                    if novo_status == 'fechado' and not caixa.aberto:
                        raise ValueError('Caixa informada esta fechada.')

                if status_atual not in ORDER_IMMUTABLE_STATUSES:
                    pedido.itens.clear()
                    itens_validos = 0
                    for i in range(int(request.form.get('item_count', 0))):
                        pid = request.form.get(f'produto_{i}')
                        qty = request.form.get(f'quantidade_{i}', 1)
                        if not pid:
                            continue
                        normalizado, erro = _normalizar_item_payload({'produto_id': pid, 'quantidade': qty})
                        if erro:
                            continue
                        produto = normalizado['produto']
                        quantidade = normalizado['quantidade']
                        ip = ItemPedido(
                            pedido_id=pedido.id,
                            produto_id=produto.id,
                            quantidade=quantidade,
                            preco_unitario=produto.preco_venda
                        )
                        db.session.add(ip)
                        itens_validos += 1
                    if itens_validos == 0:
                        raise ValueError('Adicione ao menos um item valido no pedido.')

                    _recalcular_total_pedido(pedido)

                metodo = request.form.get('metodo_pagamento')
                if metodo:
                    metodo_texto, valor_pago = _build_payment_data(
                        metodo_raw=metodo,
                        valor_raw=request.form.get('valor_pago'),
                        total_pedido=pedido.total,
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

                _aplicar_transicao_status(pedido, novo_status)
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
            atendimento_mesas_ativo=atendimento_mesas_ativo
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
        return render_template('vendas/pedidos/detalhes_pedido.html', pedido=pedido)

    @app.route('/pdv')
    @require_role(*vendas_operacao_roles)
    def pdv():
        """Interface de PDV (Ponto de Venda) para o operador de caixa"""
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
        caixas_abertas = Caixa.query.filter_by(aberto=True).all()
        mesas = Mesa.query.all() if atendimento_mesas_ativo else []
        garcons = Garcom.query.filter_by(ativo=True).order_by(Garcom.nome.asc()).all() if atendimento_mesas_ativo else []
        return render_template(
            'vendas/pdv.html',
            produtos=produtos,
            caixas_abertas=caixas_abertas,
            mesas=mesas,
            garcons=garcons,
            atendimento_mesas_ativo=atendimento_mesas_ativo
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
            if not caixa or not caixa.aberto:
                return json_response(False, 'Caixa nao esta aberta.', status=409, code='business_rule')

            pedido = Pedido(
                mesa_id=mesa_id,
                caixa_id=caixa_id,
                garcom_id=_garcom_logado_id() if atendimento_mesas_ativo else None,
                status='aberto',
                estoque_processado=False,
                financeiro_processado=False
            )
            db.session.add(pedido)
            db.session.flush()

            itens_validos = 0
            for item in itens:
                normalizado, erro = _normalizar_item_payload(item)
                if erro:
                    continue

                produto = normalizado['produto']
                quantidade = normalizado['quantidade']
                ip = ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=produto.id,
                    quantidade=quantidade,
                    preco_unitario=produto.preco_venda
                )
                db.session.add(ip)
                itens_validos += 1

            if itens_validos == 0:
                db.session.rollback()
                return json_response(False, 'Nenhum item valido para criar o pedido.', status=400, code='validation_error')

            _recalcular_total_pedido(pedido)

            mesa = None
            if atendimento_mesas_ativo and mesa_id:
                mesa = Mesa.query.get(mesa_id)
                if mesa:
                    mesa.status = 'ocupada'

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

            return json_response(
                True,
                f'Pedido #{pedido.id} criado com sucesso.',
                data={'pedido_id': pedido.id, 'total': float(pedido.total or 0.0)}
            )
        except Exception as e:
            db.session.rollback()
            return json_response(False, str(e), status=500, code='internal_error')

    @app.route('/api/pedidos/<int:pedido_id>/finalizar', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def finalizar_pedido_api(pedido_id):
        """API para finalizar pedido via AJAX."""
        try:
            pedido = Pedido.query.get_or_404(pedido_id)
            if _parse_status(pedido.status) in ORDER_IMMUTABLE_STATUSES:
                return json_response(False, f'Pedido ja esta {pedido.status}.', status=409, code='business_rule')

            dados = request.get_json(silent=True) or {}
            metodo = dados.get('metodo_pagamento')
            if metodo:
                metodo_texto, valor_pago = _build_payment_data(
                    metodo_raw=metodo,
                    valor_raw=dados.get('valor_pago'),
                    total_pedido=pedido.total,
                    split_raw=dados.get('split_pagamento'),
                    cliente_crediario=dados.get('cliente_crediario', '')
                )
                pedido.metodo_pagamento = metodo_texto
                pedido.valor_pago = valor_pago

            _aplicar_transicao_status(pedido, 'fechado')
            db.session.commit()

            return json_response(
                True,
                'Pedido finalizado com sucesso.',
                data={
                    'pedido_id': pedido_id,
                    'metodo_pagamento': pedido.metodo_pagamento,
                    'valor_pago': pedido.valor_pago,
                    'status': pedido.status
                }
            )
        except ValueError as e:
            db.session.rollback()
            status_code, code = _http_status_for_order_error(str(e))
            return json_response(False, str(e), status=status_code, code=code)
        except Exception as e:
            db.session.rollback()
            return json_response(False, str(e), status=500, code='internal_error')

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




