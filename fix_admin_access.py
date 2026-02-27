"""
Script para corrigir/criar acesso do admin
Execute: python fix_admin_access.py
"""
from app import app, db
from models import Funcionario

def fix_admin_access():
    """Cria ou atualiza o admin"""
    
    with app.app_context():
        email = "admin@conveniencia.local"
        senha = "142536"
        
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
                nome="Administrador",
                email=email,
                role="admin",
                ativo=True
            )
            admin.set_password(senha)
            db.session.add(admin)
        
        db.session.commit()
        print(f"✅ Acesso de admin corrigido com sucesso!")
        print(f"   Email: {email}")
        print(f"   Senha: {senha}")
        print(f"   Role: admin")
        print(f"   Ativo: {admin.ativo}")

if __name__ == "__main__":
    fix_admin_access()
