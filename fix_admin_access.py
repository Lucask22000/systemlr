"""
Script para corrigir/criar acesso do admin.
Execute: python fix_admin_access.py
"""

from __future__ import annotations

import os


def get_admin_credentials() -> tuple[str, str, str]:
    """Retorna as credenciais principais do admin (env + defaults)."""
    email = os.environ.get("SYSTEMLR_ADMIN_EMAIL", "admin@systemlr.com").strip().lower()
    senha = os.environ.get("SYSTEMLR_ADMIN_PASSWORD", "12345678")
    nome = os.environ.get("SYSTEMLR_ADMIN_NAME", "Administrador").strip() or "Administrador"
    return email, senha, nome


def fix_admin_access() -> None:
    """Cria ou atualiza o admin principal e exige troca de senha no primeiro login."""
    from app import app, db
    from models import Funcionario

    with app.app_context():
        email, senha, nome = get_admin_credentials()
        admin = Funcionario.query.filter_by(email=email).first()

        if admin:
            print(f"Atualizando admin existente: {admin.nome}")
        else:
            print("Criando novo admin...")
            admin = Funcionario()
            db.session.add(admin)

        admin.nome = nome
        admin.email = email
        admin.role = "admin"
        admin.ativo = True
        admin.senha_provisoria = True
        admin.set_password(senha)

        db.session.commit()
        print("Acesso de admin corrigido com sucesso.")
        print(f"  Email: {email}")
        print(f"  Senha: {senha}")
        print("  Role: admin")
        print(f"  Ativo: {admin.ativo}")
        print(f"  Senha provisoria: {admin.senha_provisoria}")


if __name__ == "__main__":
    fix_admin_access()
