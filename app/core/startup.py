"""Rotinas de startup extraidas de app/__init__.py.

Mantem comportamento funcional sem alterar regras de negocio.
"""

from sqlalchemy.exc import OperationalError

from app.constants import CARGOS_PERMANENTES
from models import FuncaoRH, Funcionario, PerfilAcesso, db


def garantir_cargos_permanentes():
    try:
        nomes_existentes = {(f.nome or '').strip().lower() for f in FuncaoRH.query.all()}
        mudou = False
        for nome_cargo, descricao_cargo in CARGOS_PERMANENTES:
            if nome_cargo.lower() not in nomes_existentes:
                db.session.add(FuncaoRH(nome=nome_cargo, descricao=descricao_cargo, ativo=True))
                mudou = True
        if mudou:
            db.session.commit()
    except OperationalError:
        db.session.rollback()


def migrar_funcoes_legadas_para_perfis(*, carregar_paginas_json, serializar_paginas_json):
    try:
        perfis_existentes = {
            (perfil.nome or '').strip().lower(): perfil
            for perfil in PerfilAcesso.query.all()
        }
        perfis_criados = {}
        mudou = False

        for funcao in FuncaoRH.query.all():
            paginas = carregar_paginas_json(funcao.permissoes_padrao)
            if not paginas:
                continue

            nome_base = (funcao.nome or '').strip()
            if not nome_base:
                continue

            chave_nome = nome_base.lower()
            perfil = perfis_existentes.get(chave_nome)
            if not perfil:
                perfil = PerfilAcesso(
                    nome=nome_base,
                    descricao=funcao.descricao,
                    permissoes_padrao=serializar_paginas_json(paginas),
                    ativo=funcao.ativo,
                )
                db.session.add(perfil)
                db.session.flush()
                perfis_existentes[chave_nome] = perfil
                mudou = True
            elif not perfil.permissoes_padrao:
                perfil.permissoes_padrao = serializar_paginas_json(paginas)
                if not perfil.descricao and funcao.descricao:
                    perfil.descricao = funcao.descricao
                mudou = True

            perfis_criados[chave_nome] = perfil

        if perfis_criados:
            funcionarios_sem_perfil = Funcionario.query.filter(
                Funcionario.perfil_acesso_id.is_(None),
                Funcionario.cargo.isnot(None)
            ).all()
            for funcionario in funcionarios_sem_perfil:
                chave_cargo = (funcionario.cargo or '').strip().lower()
                perfil = perfis_criados.get(chave_cargo)
                if not perfil:
                    continue
                funcionario.perfil_acesso_id = perfil.id
                if funcionario.role != 'admin':
                    funcionario.controle_acesso_ativo = True
                mudou = True

        if mudou:
            db.session.commit()
    except OperationalError:
        db.session.rollback()
    except Exception:
        db.session.rollback()
        raise


def bootstrap_admin_configurado(*, email, senha):
    return bool(email and senha)


def garantir_admin_primeiro_acesso(
    *,
    app,
    email,
    senha,
    nome,
    gerar_numero_cadastro_unico,
    gerar_matricula_unica,
):
    try:
        if Funcionario.query.count() > 0:
            return
        if not bootstrap_admin_configurado(email=email, senha=senha):
            app.logger.warning(
                'Nenhum usuario encontrado e bootstrap admin nao configurado. '
                'Defina SYSTEMLR_BOOTSTRAP_ADMIN_PASSWORD para criar o primeiro acesso.'
            )
            return
        administrador = Funcionario(
            nome=nome,
            email=email,
            role='admin',
            cargo='Administrador',
            departamento='Diretoria',
            time_nome='Gestao',
            nivel_organograma='Diretoria',
            ativo=True,
            controle_acesso_ativo=False,
            permitir_editar_imagem_perfil=True,
            senha_provisoria=True,
        )
        administrador.set_password(senha)
        db.session.add(administrador)
        db.session.flush()
        administrador.numero_cadastro = gerar_numero_cadastro_unico(administrador)
        administrador.matricula = gerar_matricula_unica(administrador)
        db.session.commit()
    except OperationalError:
        db.session.rollback()
    except Exception:
        db.session.rollback()
        raise
