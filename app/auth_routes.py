from flask import current_app, flash, redirect, render_template, request, session, url_for

from app.services.auth_service import AuthService
from app.validators.auth_validators import LoginSchema, RegistroSchema
from models import FuncaoRH, PerfilAcesso, db


def register_routes(app, context):
    limit = context['_limit']
    client_ip = context['_client_ip']
    is_login_rate_limited = context['_is_login_rate_limited']
    register_login_attempt = context['_register_login_attempt']
    get_funcionario_logado = context['get_funcionario_logado']
    normalizar_texto = context['_normalizar_texto']
    normalizar_cpf = context['_normalizar_cpf']
    normalizar_campo_organograma = context['_normalizar_campo_organograma']
    normalizar_estado = context['_normalizar_estado']
    parse_date_iso = context['_parse_date_iso']
    role_para_cargo_padrao = context['_role_para_cargo_padrao']
    role_para_nivel_organograma = context['_role_para_nivel_organograma']
    gerar_numero_cadastro_unico = context['_gerar_numero_cadastro_unico']
    gerar_matricula_unica = context['_gerar_matricula_unica']
    listar_cadastros_organograma = context['_listar_cadastros_organograma']
    paginas_permitidas_para_funcionario = context['_paginas_permitidas_para_funcionario']
    sincronizar_garcom_funcionario = context['sincronizar_garcom_funcionario']
    registrar_evento_auditoria = context['registrar_evento_auditoria']
    bootstrap_admin_configurado = context['_bootstrap_admin_configurado']
    primeiro_acesso_email = context['PRIMEIRO_ACESSO_EMAIL']
    roles_permitidos = context['ROLES_PERMITIDOS']
    niveis_organograma = context['NIVEIS_ORGANOGRAMA']
    extensions = context['extensions']
    auth_service = AuthService(
        normalizar_matricula=context['_normalizar_matricula'],
        normalizar_texto=normalizar_texto,
        normalizar_cpf=normalizar_cpf,
    )

    def _pode_registrar_funcionarios(funcionario):
        if not funcionario:
            return False
        paginas_rh_gestao = {'funcionarios', 'rh_funcoes'}
        return bool(set(paginas_permitidas_para_funcionario(funcionario)).intersection(paginas_rh_gestao))

    def _login_rate_limit_rule():
        attempts = int(current_app.config.get('LOGIN_MAX_ATTEMPTS', 5))
        window_seconds = int(current_app.config.get('LOGIN_WINDOW_SECONDS', 300))
        if window_seconds % 60 == 0:
            return f'{attempts} per {max(1, window_seconds // 60)} minute'
        return f'{attempts} per {window_seconds} second'

    @app.route('/login', methods=['GET', 'POST'])
    @limit(_login_rate_limit_rule, methods=['POST'])
    def login():
        if request.method == 'POST':
            ip_addr = client_ip()
            if extensions.limiter is None and is_login_rate_limited(ip_addr):
                flash('Muitas tentativas de login. Tente novamente em alguns minutos.', 'danger')
                registrar_evento_auditoria(
                    funcionario=None,
                    acao='login_rate_limited',
                    entidade='autenticacao',
                    detalhes=f'ip={ip_addr}',
                    status_code=429,
                )
                return redirect(url_for('login'))

            is_valid, errors = LoginSchema().validate(request.form)
            if not is_valid:
                for error in errors.values():
                    flash(error, 'danger')
                return redirect(url_for('login'))

            identificador = (request.form.get('login') or request.form.get('email') or '').strip()
            senha = request.form.get('senha', '')
            funcionario, erro_login = auth_service.login(identificador, senha)

            if funcionario:
                if not funcionario.ativo:
                    register_login_attempt(ip_addr, success=False)
                    registrar_evento_auditoria(
                        funcionario=funcionario,
                        acao='login_bloqueado_inativo',
                        entidade='autenticacao',
                        detalhes=f'identificador={identificador}',
                        status_code=403,
                    )
                    flash('Usuario inativo. Contate um administrador.', 'danger')
                    return redirect(url_for('login'))

                session['funcionario_id'] = funcionario.id
                session['funcionario_nome'] = funcionario.nome
                session['funcionario_role'] = funcionario.role
                db.session.commit()
                register_login_attempt(ip_addr, success=True)
                registrar_evento_auditoria(
                    funcionario=funcionario,
                    acao='login_sucesso',
                    entidade='autenticacao',
                    detalhes=f'identificador={identificador}',
                    status_code=200,
                )

                if getattr(funcionario, 'senha_provisoria', False):
                    flash('Sua senha temporaria deve ser alterada antes de continuar.', 'warning')
                    return redirect(url_for('dashboard'))

                flash(f'Bem-vindo, {funcionario.nome}!', 'success')
                return redirect(url_for('boas_vindas'))

            register_login_attempt(ip_addr, success=False)
            registrar_evento_auditoria(
                funcionario=None,
                acao='login_falha',
                entidade='autenticacao',
                detalhes=f'identificador={identificador}',
                status_code=401,
            )
            flash(erro_login or 'Matricula/email ou senha incorretos.', 'danger')
            return redirect(url_for('login'))

        funcionario_admin_inicial = auth_service.get_primeiro_admin(primeiro_acesso_email)
        mostrar_credenciais_iniciais = bool(
            bootstrap_admin_configurado()
            and getattr(funcionario_admin_inicial, 'senha_provisoria', False)
            and funcionario_admin_inicial
            and auth_service.total_funcionarios() == 1
        )
        return render_template(
            'sistema/login.html',
            mostrar_credenciais_iniciais=mostrar_credenciais_iniciais,
            primeiro_acesso_email=primeiro_acesso_email,
        )

    @app.route('/logout')
    def logout():
        funcionario = get_funcionario_logado()
        registrar_evento_auditoria(
            funcionario=funcionario,
            acao='logout',
            entidade='autenticacao',
            detalhes=f'usuario={funcionario.nome if funcionario else "desconhecido"}',
            status_code=200,
        )
        nome = session.get('funcionario_nome', 'Usuario')
        session.clear()
        flash(f'Ate logo, {nome}!', 'info')
        return redirect(url_for('index'))

    @app.route('/registro', methods=['GET', 'POST'])
    def registro():
        total_funcionarios = auth_service.total_funcionarios()
        funcionario_logado = get_funcionario_logado()

        if total_funcionarios > 0 and not _pode_registrar_funcionarios(funcionario_logado):
            flash('A criacao de contas e restrita a usuarios com acesso de RH.', 'danger')
            if funcionario_logado:
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))

        if request.method == 'POST':
            is_valid, errors = RegistroSchema().validate(request.form)
            if not is_valid:
                for error in errors.values():
                    flash(error, 'danger')
                return redirect(url_for('registro'))

            nome = request.form.get('nome', '').strip()
            email = request.form.get('email', '').strip()
            senha = request.form.get('senha', '')
            role = normalizar_texto(request.form.get('role', 'operador'))
            cargo = (request.form.get('cargo') or '').strip()
            cpf = normalizar_cpf(request.form.get('cpf'))
            rg = normalizar_campo_organograma(request.form.get('rg'))
            data_nascimento = parse_date_iso(request.form.get('data_nascimento'))
            celular = normalizar_campo_organograma(request.form.get('celular'))
            cep = normalizar_campo_organograma(request.form.get('cep'))
            endereco = normalizar_campo_organograma(request.form.get('endereco'))
            bairro = normalizar_campo_organograma(request.form.get('bairro'))
            cidade = normalizar_campo_organograma(request.form.get('cidade'))
            estado = normalizar_estado(request.form.get('estado'))
            departamento = normalizar_campo_organograma(request.form.get('departamento'))
            time_nome = normalizar_campo_organograma(request.form.get('time_nome'))
            nivel_organograma = normalizar_campo_organograma(request.form.get('nivel_organograma'))
            permitir_editar_imagem_perfil = (request.form.get('permitir_editar_imagem_perfil') == 'on')
            perfil_acesso_id = request.form.get('perfil_acesso_id', type=int)

            perfil_acesso, erro_registro = auth_service.validar_registro_basico(
                email=email,
                cpf=cpf,
                perfil_acesso_id=perfil_acesso_id,
                niveis_organograma=niveis_organograma,
                nivel_organograma=nivel_organograma,
            )
            if erro_registro:
                flash(erro_registro, 'danger')
                return redirect(url_for('registro'))

            novo_funcionario = auth_service.build_novo_funcionario(nome=nome, email=email, senha=senha)
            novo_funcionario.cpf = cpf if cpf != '__invalid__' else None
            novo_funcionario.rg = rg
            novo_funcionario.data_nascimento = data_nascimento
            novo_funcionario.celular = celular
            novo_funcionario.cep = cep
            novo_funcionario.endereco = endereco
            novo_funcionario.bairro = bairro
            novo_funcionario.cidade = cidade
            novo_funcionario.estado = estado
            novo_funcionario.permitir_editar_imagem_perfil = permitir_editar_imagem_perfil

            if total_funcionarios == 0:
                novo_funcionario.role = 'admin'
                novo_funcionario.cargo = 'Administrador'
                novo_funcionario.departamento = departamento or 'Diretoria'
                novo_funcionario.time_nome = time_nome or 'Gestao'
                novo_funcionario.nivel_organograma = nivel_organograma or 'Diretoria'
                novo_funcionario.perfil_acesso_id = None
                novo_funcionario.controle_acesso_ativo = False
            elif role in roles_permitidos:
                novo_funcionario.role = role
                novo_funcionario.cargo = cargo or role_para_cargo_padrao(role)
                novo_funcionario.departamento = departamento
                novo_funcionario.time_nome = time_nome
                novo_funcionario.nivel_organograma = nivel_organograma or role_para_nivel_organograma(role)
                novo_funcionario.perfil_acesso_id = perfil_acesso.id if perfil_acesso else None
                novo_funcionario.controle_acesso_ativo = bool(perfil_acesso)
            else:
                flash('Tipo de usuario invalido.', 'danger')
                return redirect(url_for('registro'))

            db.session.add(novo_funcionario)
            db.session.flush()
            novo_funcionario.numero_cadastro = gerar_numero_cadastro_unico(novo_funcionario)
            if not novo_funcionario.matricula:
                novo_funcionario.matricula = gerar_matricula_unica(novo_funcionario)
            sincronizar_garcom_funcionario(novo_funcionario)
            db.session.commit()

            if total_funcionarios == 0:
                flash(f'Conta do administrador criada com sucesso! Bem-vindo, {nome}!', 'success')
                session['funcionario_id'] = novo_funcionario.id
                session['funcionario_nome'] = novo_funcionario.nome
                session['funcionario_role'] = novo_funcionario.role
                return redirect(url_for('boas_vindas'))

            flash(f'Funcionario {nome} registrado com sucesso!', 'success')
            return redirect(url_for('listar_funcionarios'))

        funcoes_rh = FuncaoRH.query.filter_by(ativo=True).order_by(FuncaoRH.nome.asc()).all()
        perfis_acesso = PerfilAcesso.query.filter_by(ativo=True).order_by(PerfilAcesso.nome.asc()).all()
        departamentos_existentes, times_existentes = listar_cadastros_organograma()
        return render_template(
            'sistema/registro.html',
            primeira_vez=(total_funcionarios == 0),
            funcoes_rh=funcoes_rh,
            perfis_acesso=perfis_acesso,
            niveis_organograma=niveis_organograma,
            departamentos_existentes=departamentos_existentes,
            times_existentes=times_existentes,
        )
