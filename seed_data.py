"""
Script para popular o banco de dados com dados de teste.
Execute: python seed_data.py
"""
import sys
from datetime import datetime, timedelta
import secrets

from app import app, db
from models import (
    Categoria, Produto, Fornecedor, Funcionario, Mesa, Caixa, 
    Movimentacao, PermissaoAcesso, Pedido
)

def seed_database():
    """Popula o banco com dados de teste"""
    
    with app.app_context():
        # Limpar dados existentes
        print("🗑️  Limpando dados existentes...")
        db.drop_all()
        db.create_all()
        
        print("📝 Criando funcionários...")
        # Criar funcionários
        admin = Funcionario(
            nome="Administrador",
            email="admin@conveniencia.local",
            role="admin",
            ativo=True
        )
        admin.set_password("admin123")
        
        gerente = Funcionario(
            nome="Gerente",
            email="gerente@conveniencia.local",
            role="gerente",
            ativo=True
        )
        gerente.set_password("gerente123")
        
        operador1 = Funcionario(
            nome="João Operador",
            email="joao@conveniencia.local",
            role="operador",
            ativo=True
        )
        operador1.set_password("joao123")
        
        operador2 = Funcionario(
            nome="Maria Caixa",
            email="maria@conveniencia.local",
            role="caixa",
            ativo=True
        )
        operador2.set_password("maria123")
        
        db.session.add_all([admin, gerente, operador1, operador2])
        db.session.commit()
        
        print("📂 Criando categorias...")
        # Criar categorias
        categorias_data = [
            {"nome": "Bebidas", "descricao": "Refrigerantes, sucos e bebidas em geral"},
            {"nome": "Alimentos", "descricao": "Snacks, lanches e alimentos diversos"},
            {"nome": "Doces", "descricao": "Chocolates, balas e doces"},
            {"nome": "Cuidados Pessoais", "descricao": "Produtos de higiene e cuidados"},
            {"nome": "Outros", "descricao": "Diversos"}
        ]
        
        categorias = []
        for cat_data in categorias_data:
            cat = Categoria(**cat_data)
            categorias.append(cat)
            db.session.add(cat)
        db.session.commit()
        
        print("🤝 Criando fornecedores...")
        # Criar fornecedores
        fornecedores_data = [
            {"nome": "Distribuidora ABC", "contato": "João Silva", "telefone": "(11) 3000-0000", "email": "vendas@distributora-abc.com"},
            {"nome": "Sua Bebida", "contato": "Carlos", "telefone": "(11) 2000-0000", "email": "vendas@suabebida.com"},
            {"nome": "Alimentos Brasil", "contato": "Pedro", "telefone": "(11) 1000-0000", "email": "contato@alimentosbrasil.com"},
            {"nome": "Premium Doces", "contato": "Ana", "telefone": "(11) 4000-0000", "email": "vendas@premiumdoces.com"},
        ]
        
        fornecedores = []
        for forn_data in fornecedores_data:
            forn = Fornecedor(**forn_data)
            fornecedores.append(forn)
            db.session.add(forn)
        db.session.commit()
        
        print("📦 Criando produtos...")
        # Criar produtos
        produtos_data = [
            # Bebidas
            {"codigo": "BEB001", "nome": "Coca-Cola 2L", "categoria_id": categorias[0].id, "preco_custo": 5.00, "preco_venda": 8.50, "quantidade_estoque": 50},
            {"codigo": "BEB002", "nome": "Suco Natural Laranja 1L", "categoria_id": categorias[0].id, "preco_custo": 3.50, "preco_venda": 6.90, "quantidade_estoque": 30},
            {"codigo": "BEB003", "nome": "Água Mineral 1.5L", "categoria_id": categorias[0].id, "preco_custo": 1.20, "preco_venda": 2.50, "quantidade_estoque": 100},
            
            # Alimentos
            {"codigo": "ALI001", "nome": "Biscoito Água e Sal", "categoria_id": categorias[1].id, "preco_custo": 1.50, "preco_venda": 3.50, "quantidade_estoque": 80},
            {"codigo": "ALI002", "nome": "Bolo de Chocolate", "categoria_id": categorias[1].id, "preco_custo": 4.00, "preco_venda": 8.90, "quantidade_estoque": 20},
            {"codigo": "ALI003", "nome": "Batata Frita Pequena", "categoria_id": categorias[1].id, "preco_custo": 2.00, "preco_venda": 4.90, "quantidade_estoque": 60},
            
            # Doces
            {"codigo": "DOC001", "nome": "Chocolate Ao Leite", "categoria_id": categorias[2].id, "preco_custo": 3.00, "preco_venda": 6.50, "quantidade_estoque": 45},
            {"codigo": "DOC002", "nome": "Bala Sortida", "categoria_id": categorias[2].id, "preco_custo": 0.50, "preco_venda": 1.50, "quantidade_estoque": 200},
            {"codigo": "DOC003", "nome": "Brigadeiro", "categoria_id": categorias[2].id, "preco_custo": 1.50, "preco_venda": 3.50, "quantidade_estoque": 35},
            
            # Cuidados Pessoais
            {"codigo": "CUI001", "nome": "Papel Higiênico 4 rolos", "categoria_id": categorias[3].id, "preco_custo": 4.50, "preco_venda": 8.90, "quantidade_estoque": 25},
            {"codigo": "CUI002", "nome": "Desinfetante", "categoria_id": categorias[3].id, "preco_custo": 2.50, "preco_venda": 5.50, "quantidade_estoque": 15},
        ]
        
        produtos = []
        for prod_data in produtos_data:
            prod = Produto(**prod_data)
            produtos.append(prod)
            db.session.add(prod)
        db.session.commit()
        
        print("🏪 Criando mesas...")
        # Criar mesas
        mesas_data = [
            {"numero": "1", "capacidade": 2, "status": "livre"},
            {"numero": "2", "capacidade": 2, "status": "livre"},
            {"numero": "3", "capacidade": 4, "status": "ocupada"},
            {"numero": "4", "capacidade": 4, "status": "livre"},
            {"numero": "5", "capacidade": 6, "status": "livre"},
            {"numero": "6", "capacidade": 4, "status": "ocupada"},
        ]
        
        mesas = []
        for mesa_data in mesas_data:
            mesa = Mesa(**mesa_data)
            mesa.qr_token = secrets.token_urlsafe(12)
            mesas.append(mesa)
            db.session.add(mesa)
        db.session.commit()
        
        print("💰 Criando caixas...")
        # Criar caixas
        caixas_data = [
            {"nome": "Caixa 1", "funcionario_id": maria.id if (maria := operador2) else None, "saldo_inicial": 0.0, "aberto": False},
            {"nome": "Caixa 2", "funcionario_id": None, "saldo_inicial": 0.0, "aberto": False},
            {"nome": "Caixa 3", "funcionario_id": None, "saldo_inicial": 0.0, "aberto": False},
        ]
        
        caixas = []
        for caixa_data in caixas_data:
            caixa = Caixa(**caixa_data)
            caixa.saldo_atual = caixa_data["saldo_inicial"]
            caixas.append(caixa)
            db.session.add(caixa)
        db.session.commit()
        
        # sample pedido with payment
        print("💳 Criando um pedido de exemplo com pagamento")
        if caixas and produtos:
            ped = Pedido(caixa_id=caixas[0].id, total=produtos[0].preco_venda, metodo_pagamento='dinheiro', valor_pago=produtos[0].preco_venda)
            db.session.add(ped)
            db.session.commit()

        print("📋 Criando movimentações de estoque...")
        # Criar algumas movimentações para histórico
        for i, produto in enumerate(produtos[:5]):
            mov = Movimentacao(
                produto_id=produto.id,
                fornecedor_id=fornecedores[0].id,
                tipo=Movimentacao.TIPO_ENTRADA,
                quantidade=100,
                motivo="Compra inicial",
                observacoes="Estoque de abertura"
            )
            db.session.add(mov)
        db.session.commit()
        
        print("🔐 Configurando permissões...")
        # Adicionar permissões para funcionários
        paginas_admin = ['inicio', 'produtos', 'categorias', 'fornecedores', 'movimentacoes', 
                        'relatorios', 'caixas', 'mesas', 'pedidos', 'vendas', 'funcionarios']
        paginas_gerente = ['inicio', 'produtos', 'categorias', 'movimentacoes', 'relatorios', 
                          'caixas', 'mesas', 'pedidos', 'vendas']
        paginas_operador = ['inicio', 'produtos', 'pedidos', 'vendas']
        
        # Admin
        for pagina in paginas_admin:
            perm = PermissaoAcesso(funcionario_id=admin.id, pagina=pagina)
            db.session.add(perm)
        
        # Gerente
        for pagina in paginas_gerente:
            perm = PermissaoAcesso(funcionario_id=gerente.id, pagina=pagina)
            db.session.add(perm)
        
        # Operadores
        for pagina in paginas_operador:
            perm = PermissaoAcesso(funcionario_id=operador1.id, pagina=pagina)
            db.session.add(perm)
            perm = PermissaoAcesso(funcionario_id=operador2.id, pagina=pagina)
            db.session.add(perm)
        
        db.session.commit()
        
        print("\n" + "="*60)
        print("✅ BANCO DE DADOS POPULADO COM SUCESSO!")
        print("="*60)
        print("\n📊 Dados Criados:")
        print(f"  • {len([admin, gerente, operador1, operador2])} funcionários")
        print(f"  • {len(categorias)} categorias")
        print(f"  • {len(fornecedores)} fornecedores")
        print(f"  • {len(produtos)} produtos")
        print(f"  • {len(mesas)} mesas")
        print(f"  • {len(caixas)} caixas")
        print("\n🔐 Contas para Teste:")
        print("  Admin:      admin@conveniencia.local / admin123")
        print("  Gerente:    gerente@conveniencia.local / gerente123")
        print("  Operador:   joao@conveniencia.local / joao123")
        print("  Caixa:      maria@conveniencia.local / maria123")
        print("\n" + "="*60)

if __name__ == '__main__':
    try:
        seed_database()
    except Exception as e:
        print(f"❌ Erro ao popular banco: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
