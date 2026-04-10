"""
Script para corrigir/criar acesso do admin
Execute: python fix_admin_access.py
"""
import os

from app import app, db
from models import Funcionario

def fix_admin_access():
    """Cria ou atualiza o admin"""
    
    with app.app_context():
        email = os.environ.get("SYSTEMLR_ADMIN_EMAIL", "admin@systemlr.com")
        senha = os.environ.get("SYSTEMLR_ADMIN_PASSWORD", "142536")
        nome = os.environ.get("SYSTEMLR_ADMIN_NAME", "Administrador")
        
        # Procurar por admin existente
        admin = Funcionario.query.filter_by(email=email).first()
        
        if admin:
            print(f"✏️  Atualizando admin existente: {admin.nome}")
            admin.set_password(senha)
            admin.role = "admin"
            admin.ativo = True
        else:
            print(f"✨ Criando novo admin...")
            admin = Funcionario(
                nome=nome,
                email=email,
                role="admin",
                ativo=True
            )
            admin.set_password(senha)
            db.session.add(admin)
        if admin and admin.nome != nome:
            admin.nome = nome
        
        db.session.commit()
        print(f"✅ Acesso de admin corrigido com sucesso!")
        print(f"   Email: {email}")
        print(f"   Senha: {senha}")
        print(f"   Role: admin")
        print(f"   Ativo: {admin.ativo}")

if __name__ == "__main__":
    fix_admin_access()
