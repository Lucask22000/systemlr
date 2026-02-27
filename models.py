from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    produtos = db.relationship('Produto', backref='categoria', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    preco_custo = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0)
    quantidade_minima = db.Column(db.Integer, default=5)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Produto {self.nome}>'
    
    @property
    def lucro_unitario(self):
        return self.preco_venda - self.preco_custo
    
    @property
    def margem_lucro(self):
        if self.preco_venda == 0:
            return 0
        return ((self.preco_venda - self.preco_custo) / self.preco_venda) * 100
    
    @property
    def em_falta(self):
        return self.quantidade_estoque < self.quantidade_minima

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'
    
    TIPO_ENTRADA = 'entrada'
    TIPO_SAIDA = 'saida'
    TIPOS = [TIPO_ENTRADA, TIPO_SAIDA]
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=True)
    tipo = db.Column(db.String(20), nullable=False)  # entrada ou saida
    quantidade = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(200))  # venda, compra, devolução, perda, etc
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Movimentacao {self.produto_id} - {self.tipo}>'


# ======= NOVOS MODELOS =======

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True, nullable=False)
    contato = db.Column(db.String(120))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    movimentacoes = db.relationship('Movimentacao', backref='fornecedor', lazy=True)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'

class Caixa(db.Model):
    __tablename__ = 'caixas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    saldo_inicial = db.Column(db.Float, default=0.0)
    saldo_atual = db.Column(db.Float, default=0.0)
    saldo_fechamento = db.Column(db.Float, nullable=True)
    aberto = db.Column(db.Boolean, default=False)
    aberto_em = db.Column(db.DateTime, nullable=True)
    fechado_em = db.Column(db.DateTime, nullable=True)
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    pedidos = db.relationship('Pedido', backref='caixa', lazy=True)
    funcionario = db.relationship('Funcionario', backref='caixas_abertas')
    movimentacoes_caixa = db.relationship('MovimentacaoCaixa', backref='caixa', lazy=True, cascade='all, delete-orphan')

    @property
    def diferenca(self):
        """Calcul a diferença entre saldo de fechamento e saldo_atual"""
        if self.saldo_fechamento is None:
            return None
        return self.saldo_fechamento - self.saldo_atual

    def __repr__(self):
        return f'<Caixa {self.nome} - {'aberto' if self.aberto else 'fechado'}>'


class Mesa(db.Model):
    __tablename__ = 'mesas'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    capacidade = db.Column(db.Integer, default=4)
    status = db.Column(db.String(20), default='livre')  # livre, ocupada
    qr_token = db.Column(db.String(64), unique=True, nullable=True)
    descricao = db.Column(db.Text)

    pedidos = db.relationship('Pedido', backref='mesa', lazy=True)

    def __repr__(self):
        return f'<Mesa {self.numero} - {self.status}>'


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable=True)
    caixa_id = db.Column(db.Integer, db.ForeignKey('caixas.id'), nullable=True)
    total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='aberto')  # aberto, em_preparo, entregue, fechado, cancelado
    origem = db.Column(db.String(20), default='interno')  # interno, qr
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    fechado_em = db.Column(db.DateTime)
    observacoes = db.Column(db.Text)

    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')

    def calcular_total(self):
        self.total = sum(item.quantidade * item.preco_unitario for item in self.itens)
        return self.total

    def __repr__(self):
        return f'<Pedido {self.id} - {self.status}>'


class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)

    produto = db.relationship('Produto')

    def __repr__(self):
        return f'<ItemPedido {self.produto.nome} x{self.quantidade}>'


class Funcionario(db.Model):
    __tablename__ = 'funcionarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='operador')  # admin, gerente, caixa, operador
    ativo = db.Column(db.Boolean, default=True)
    controle_acesso_ativo = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    permissoes = db.relationship('PermissaoAcesso', backref='funcionario', lazy=True, cascade='all, delete-orphan')

    def set_password(self, senha):
        """Hash e armazena a senha."""
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Funcionario {self.nome} - {self.role}>'


class PermissaoAcesso(db.Model):
    __tablename__ = 'permissoes_acesso'

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    pagina = db.Column(db.String(80), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('funcionario_id', 'pagina', name='uq_funcionario_pagina'),
    )

    def __repr__(self):
        return f'<PermissaoAcesso funcionario={self.funcionario_id} pagina={self.pagina}>'


class MovimentacaoCaixa(db.Model):
    __tablename__ = 'movimentacoes_caixa'

    TIPO_ENTRADA = 'entrada'
    TIPO_SAIDA = 'saida'
    TIPOS = [TIPO_ENTRADA, TIPO_SAIDA]

    id = db.Column(db.Integer, primary_key=True)
    caixa_id = db.Column(db.Integer, db.ForeignKey('caixas.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # entrada ou saida
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MovimentacaoCaixa caixa={self.caixa_id} {self.tipo} {self.valor}>'


