from datetime import datetime
import secrets
import qrcode
from io import BytesIO
from flask import render_template, request, redirect, url_for, flash, session, Response, jsonify

from models import db, Caixa, Mesa, Pedido, Produto, ItemPedido, Movimentacao, MovimentacaoCaixa, Funcionario
from realtime import publish_alert, sse_stream


METODOS_PAGAMENTO = {'dinheiro', 'cartao', 'pix', 'crediario', 'dividido'}


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

    if metodo == 'dividido':
        split_raw = split_raw or {}
        valor_dinheiro = _to_float(split_raw.get('dinheiro'), 0.0) or 0.0
        valor_cartao = _to_float(split_raw.get('cartao'), 0.0) or 0.0
        if valor_dinheiro < 0 or valor_cartao < 0:
            raise ValueError('Valores de pagamento nao podem ser negativos.')
        valor_pago = valor_dinheiro + valor_cartao
        if valor_pago <= 0:
            raise ValueError('Informe ao menos um valor para dinheiro ou cartao.')
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
        metodo_texto = metodo

    return metodo_texto, valor_pago


def register_vendas_routes(app, login_required):
    @app.route('/caixas')
    @login_required
    def listar_caixas():
        caixas = Caixa.query.all()
        return render_template('vendas/caixas/caixas.html', caixas=caixas)

    @app.route('/caixas/nova', methods=['GET', 'POST'])
    @login_required
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
    @login_required
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
    @login_required
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
    @login_required
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
    @login_required
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
    @login_required
    def historico_caixa(caixa_id):
        """Exibe histórico de movimentações da caixa"""
        caixa = Caixa.query.get_or_404(caixa_id)
        movimentacoes = MovimentacaoCaixa.query.filter_by(caixa_id=caixa_id).order_by(
            MovimentacaoCaixa.criado_em.desc()
        ).all()
        
        return render_template('vendas/caixas/historico_caixa.html', caixa=caixa, movimentacoes=movimentacoes)

    @app.route('/mesas')
    @login_required
    def listar_mesas():
        mesas = Mesa.query.all()
        # Garante que todas as mesas tenham token para QR Code
        for mesa in mesas:
            if not mesa.qr_token:
                mesa.qr_token = secrets.token_urlsafe(12)
        db.session.commit()
        return render_template('vendas/mesas/mesas.html', mesas=mesas)

    @app.route('/mesas/nova', methods=['GET', 'POST'])
    @login_required
    def nova_mesa():
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
    @login_required
    def editar_mesa(mesa_id):
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
    @login_required
    def deletar_mesa(mesa_id):
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
    @login_required
    def visualizar_qrcode_mesa(mesa_id):
        """Exibe o QR code da mesa com opções de impressão e download"""
        mesa = Mesa.query.get_or_404(mesa_id)
        
        # Garante que a mesa tenha token
        if not mesa.qr_token:
            mesa.qr_token = secrets.token_urlsafe(12)
            db.session.commit()
        
        # URL do QR code (remonta do Flask)
        app_url = request.host_url.rstrip('/')
        qr_url = f"{app_url}/m/{mesa.qr_token}"
        
        return render_template('vendas/mesas/qrcode_mesa.html', mesa=mesa, qr_url=qr_url)

    @app.route('/mesas/<int:mesa_id>/qrcode/download')
    @login_required
    def download_qrcode_mesa(mesa_id):
        """Faz download da imagem do QR code"""
        mesa = Mesa.query.get_or_404(mesa_id)
        
        if not mesa.qr_token:
            flash('QR code não disponível para esta mesa', 'error')
            return redirect(url_for('listar_mesas'))
        
        try:
            # Gera o QR code
            app_url = request.host_url.rstrip('/')
            qr_url = f"{app_url}/m/{mesa.qr_token}"
            
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
    @login_required
    def print_qrcode_mesa(mesa_id):
        """Exibe o QR code em formato para impressão"""
        mesa = Mesa.query.get_or_404(mesa_id)
        
        if not mesa.qr_token:
            flash('QR code não disponível para esta mesa', 'error')
            return redirect(url_for('listar_mesas'))
        
        app_url = request.host_url.rstrip('/')
        qr_url = f"{app_url}/m/{mesa.qr_token}"
        
        return render_template('vendas/mesas/print_qrcode_mesa.html', mesa=mesa, qr_url=qr_url)

    @app.route('/pedidos')
    @login_required
    def listar_pedidos():
        pedidos = Pedido.query.order_by(Pedido.criado_em.desc()).all()
        return render_template('vendas/pedidos/pedidos.html', pedidos=pedidos)

    @app.route('/pedidos/pendentes')
    @login_required
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
    @login_required
    def alterar_status_pedido(pedido_id):
        novo_status = request.form.get('status')
        if novo_status not in ['em_preparo', 'entregue', 'fechado', 'cancelado', 'aberto']:
            flash('Status inválido.', 'danger')
            return redirect(url_for('listar_pedidos'))
        pedido = Pedido.query.get_or_404(pedido_id)
        pedido.status = novo_status
        if novo_status in ['entregue', 'fechado']:
            pedido.fechado_em = datetime.utcnow()
            if pedido.mesa:
                pedido.mesa.status = 'livre'
        db.session.commit()
        flash(f'Pedido {pedido.id} atualizado para {novo_status}.', 'success')
        return redirect(request.referrer or url_for('listar_pedidos'))

    @app.route('/pedidos/novo', methods=['GET', 'POST'])
    @login_required
    def novo_pedido():
        produtos = Produto.query.filter_by(ativo=True).all()
        mesas = Mesa.query.all()
        caixas = Caixa.query.filter_by(aberto=True).all()
        if request.method == 'POST':
            try:
                mesa_id = request.form.get('mesa_id') or None
                caixa_id = request.form.get('caixa_id') or None
                observacoes = request.form.get('observacoes')
                pedido = Pedido(mesa_id=mesa_id, caixa_id=caixa_id, observacoes=observacoes)
                db.session.add(pedido)
                db.session.flush()
                total = 0
                for i in range(int(request.form.get('item_count', 0))):
                    pid = request.form.get(f'produto_{i}')
                    qty = int(request.form.get(f'quantidade_{i}', 1))
                    if not pid:
                        continue
                    prod = Produto.query.get(pid)
                    if not prod:
                        continue
                    ip = ItemPedido(
                        pedido_id=pedido.id,
                        produto_id=prod.id,
                        quantidade=qty,
                        preco_unitario=prod.preco_venda
                    )
                    db.session.add(ip)
                    total += qty * prod.preco_venda
                pedido.total = total
                db.session.commit()
                flash('Pedido criado com sucesso!', 'success')
                return redirect(url_for('listar_pedidos'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar pedido: {str(e)}', 'error')
        return render_template('vendas/pedidos/novo_pedido.html', produtos=produtos, mesas=mesas, caixas=caixas)

    @app.route('/pedidos/<int:pedido_id>/editar', methods=['GET', 'POST'])
    @login_required
    def editar_pedido(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        produtos = Produto.query.filter_by(ativo=True).all()
        mesas = Mesa.query.all()
        caixas = Caixa.query.all()
        if request.method == 'POST':
            try:
                pedido.mesa_id = request.form.get('mesa_id') or None
                pedido.caixa_id = request.form.get('caixa_id') or None
                pedido.status = request.form.get('status', pedido.status)
                pedido.observacoes = request.form.get('observacoes', pedido.observacoes)

                pedido.itens.clear()
                total = 0
                for i in range(int(request.form.get('item_count', 0))):
                    pid = request.form.get(f'produto_{i}')
                    qty = int(request.form.get(f'quantidade_{i}', 1))
                    if not pid:
                        continue
                    prod = Produto.query.get(pid)
                    if not prod:
                        continue
                    ip = ItemPedido(
                        pedido_id=pedido.id,
                        produto_id=prod.id,
                        quantidade=qty,
                        preco_unitario=prod.preco_venda
                    )
                    db.session.add(ip)
                    total += qty * prod.preco_venda
                pedido.total = total

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

                if pedido.status == 'fechado' and not pedido.fechado_em:
                    pedido.fechado_em = datetime.utcnow()
                    for ip in pedido.itens:
                        prod = Produto.query.get(ip.produto_id)
                        if prod:
                            prod.quantidade_estoque -= ip.quantidade
                            mov = Movimentacao(
                                produto_id=prod.id,
                                tipo=Movimentacao.TIPO_SAIDA,
                                quantidade=ip.quantidade,
                                motivo='venda',
                                observacoes=f'Pedido {pedido.id}'
                            )
                            db.session.add(mov)
                db.session.commit()
                flash('Pedido atualizado com sucesso!', 'success')
                return redirect(url_for('listar_pedidos'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar pedido: {str(e)}', 'error')
        return render_template('vendas/pedidos/editar_pedido.html', pedido=pedido, produtos=produtos, mesas=mesas, caixas=caixas)

    @app.route('/pedidos/<int:pedido_id>/deletar', methods=['POST'])
    @login_required
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

    @app.route('/vendas')
    @login_required
    def listar_vendas():
        vendas = Pedido.query.filter_by(status='fechado').all()
        return render_template('vendas/vendas.html', vendas=vendas)

    @app.route('/pdv')
    @login_required
    def pdv():
        """Interface de PDV (Ponto de Venda) para o operador de caixa"""
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
        caixas_abertas = Caixa.query.filter_by(aberto=True).all()
        mesas = Mesa.query.all()
        return render_template(
            'vendas/pdv.html',
            produtos=produtos,
            caixas_abertas=caixas_abertas,
            mesas=mesas
        )

    @app.route('/api/pedidos/criar', methods=['POST'])
    @login_required
    def criar_pedido_api():
        """API para criar pedido via AJAX"""
        try:
            data = request.get_json()
            caixa_id = data.get('caixa_id')
            mesa_id = data.get('mesa_id') or None
            itens = data.get('itens', [])
            
            if not caixa_id or not itens:
                return jsonify({'success': False, 'message': 'Caixa e produtos são obrigatórios'}), 400
            
            caixa = Caixa.query.get(caixa_id)
            if not caixa or not caixa.aberto:
                return jsonify({'success': False, 'message': 'Caixa não está aberta'}), 400
            
            pedido = Pedido(mesa_id=mesa_id, caixa_id=caixa_id, status='aberto')
            db.session.add(pedido)
            db.session.flush()
            
            total = 0
            for item in itens:
                produto_id = item.get('produto_id')
                quantidade = int(item.get('quantidade', 1))
                
                produto = Produto.query.get(produto_id)
                if not produto:
                    continue
                
                ip = ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=produto_id,
                    quantidade=quantidade,
                    preco_unitario=produto.preco_venda
                )
                db.session.add(ip)
                total += quantidade * produto.preco_venda
            
            pedido.total = total
            
            # Atualizar saldo do caixa
            caixa.saldo_atual += total
            
            # Marcar mesa como ocupada se houver
            if mesa_id:
                mesa = Mesa.query.get(mesa_id)
                if mesa:
                    mesa.status = 'ocupada'
            
            db.session.commit()
            
            publish_alert(f"Nova venda! Pedido #{pedido.id} - Total: R$ {total:.2f}")
            
            return jsonify({
                'success': True,
                'pedido_id': pedido.id,
                'total': total,
                'message': f'Pedido #{pedido.id} criado com sucesso!'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/pedidos/<int:pedido_id>/finalizar', methods=['POST'])
    @login_required
    def finalizar_pedido_api(pedido_id):
        """API para finalizar pedido via AJAX"""
        try:
            pedido = Pedido.query.get_or_404(pedido_id)
            
            if pedido.status == 'fechado':
                return jsonify({'success': False, 'message': 'Pedido já está fechado'}), 400
            
            pedido.status = 'fechado'
            pedido.fechado_em = datetime.utcnow()

            # registrar forma e valor se enviados
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
            
            if pedido.mesa:
                pedido.mesa.status = 'livre'
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Pedido finalizado com sucesso!',
                'pedido_id': pedido_id,
                'metodo_pagamento': pedido.metodo_pagamento,
                'valor_pago': pedido.valor_pago
            })
        except ValueError as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/pedidos/aberto/<int:caixa_id>')
    @login_required
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

    @app.route('/api/pedidos/<int:pedido_id>/adicionar', methods=['POST'])
    @login_required
    def adicionar_itens_pedido_api(pedido_id):
        """Adiciona itens a um pedido já aberto"""
        pedido = Pedido.query.get_or_404(pedido_id)
        if pedido.status != 'aberto':
            return jsonify({'success': False, 'message': 'Pedido não está aberto'}), 400
        dados = request.get_json(silent=True) or {}
        itens = dados.get('itens', [])
        total_add = 0
        try:
            for it in itens:
                prod = Produto.query.get(it.get('produto_id'))
                if not prod:
                    continue
                qty = int(it.get('quantidade', 0))
                if qty <= 0:
                    continue
                ip = ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=prod.id,
                    quantidade=qty,
                    preco_unitario=prod.preco_venda
                )
                db.session.add(ip)
                total_add += qty * prod.preco_venda
            pedido.total += total_add
            db.session.commit()
            return jsonify({'success': True, 'message': 'Itens adicionados', 'pedido_id': pedido.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/eventos/pedidos')
    @login_required
    def sse_pedidos():
        return Response(sse_stream(), mimetype='text/event-stream')
