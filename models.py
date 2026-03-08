from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    imagem_path = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    produtos = db.relationship('Produto', backref='categoria', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Produto(db.Model):
    __tablename__ = 'produtos'

    STATUS_DISPONIVEL_ONLINE = 'online'
    STATUS_DISPONIVEL_OFF = 'off'
    STATUS_DISPONIBILIDADE_VALIDOS = [
        STATUS_DISPONIVEL_ONLINE,
        STATUS_DISPONIVEL_OFF,
    ]
    STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES = [
        STATUS_DISPONIVEL_ONLINE,
        'disponivel_online',
        'disponivel_venda',
    ]
    STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES = [
        STATUS_DISPONIVEL_OFF,
        'indisponivel',
        'somente_ressuprimento',
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    imagem_path = db.Column(db.String(255))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=True)
    endereco_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    preco_custo = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0)
    quantidade_minima = db.Column(db.Integer, default=5)
    status_disponibilidade = db.Column(db.String(30), default=STATUS_DISPONIVEL_ONLINE, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True, cascade='all, delete-orphan')
    fornecedor = db.relationship('Fornecedor', backref=db.backref('produtos', lazy=True))
    
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

    @classmethod
    def normalizar_status_disponibilidade(cls, status):
        status_normalizado = (status or cls.STATUS_DISPONIVEL_ONLINE).strip().lower()
        if status_normalizado in cls.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES:
            return cls.STATUS_DISPONIVEL_ONLINE
        if status_normalizado in cls.STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES:
            return cls.STATUS_DISPONIVEL_OFF
        return cls.STATUS_DISPONIVEL_ONLINE

    @property
    def disponivel_para_venda(self):
        status = self.normalizar_status_disponibilidade(self.status_disponibilidade)
        return bool(self.ativo) and status == self.STATUS_DISPONIVEL_ONLINE

    @property
    def status_disponibilidade_label(self):
        status = self.normalizar_status_disponibilidade(self.status_disponibilidade)
        labels = {
            self.STATUS_DISPONIVEL_ONLINE: 'Online',
            self.STATUS_DISPONIVEL_OFF: 'Off',
        }
        return labels.get(status, 'Online')

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'
    
    TIPO_ENTRADA = 'entrada'
    TIPO_SAIDA = 'saida'
    TIPO_TRANSFERENCIA = 'transferencia'
    TIPOS = [TIPO_ENTRADA, TIPO_SAIDA, TIPO_TRANSFERENCIA]
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=True)
    endereco_origem_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    endereco_destino_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    tipo = db.Column(db.String(20), nullable=False)  # entrada ou saida
    quantidade = db.Column(db.Integer, nullable=False)
    valor_compra = db.Column(db.Float, nullable=True)
    info_nota = db.Column(db.String(255))
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
    documento = db.Column(db.String(30), nullable=True)
    contato = db.Column(db.String(120))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    endereco_rua = db.Column(db.String(160), nullable=True)
    endereco_numero = db.Column(db.String(20), nullable=True)
    endereco_bairro = db.Column(db.String(100), nullable=True)
    endereco_cidade = db.Column(db.String(100), nullable=True)
    tipo_produtos_fornece = db.Column(db.String(255), nullable=True)
    observacoes_gerais = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    movimentacoes = db.relationship('Movimentacao', backref='fornecedor', lazy=True)
    recebimentos = db.relationship('RecebimentoFornecedor', backref='fornecedor', lazy=True)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'


class Estoque(db.Model):
    __tablename__ = 'estoques'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    endereco_origem_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    endereco_destino_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)

    endereco_origem = db.relationship(
        'EnderecoEstoque',
        foreign_keys=[endereco_origem_id],
        backref='estoques_como_origem',
        lazy='select'
    )
    endereco_destino = db.relationship(
        'EnderecoEstoque',
        foreign_keys=[endereco_destino_id],
        backref='estoques_como_destino',
        lazy='select'
    )

    enderecos = db.relationship(
        'EnderecoEstoque',
        foreign_keys='EnderecoEstoque.estoque_id',
        backref=db.backref('estoque', foreign_keys='EnderecoEstoque.estoque_id'),
        lazy=True
    )

    def __repr__(self):
        return f'<Estoque {self.nome}>'


class EnderecoEstoque(db.Model):
    __tablename__ = 'enderecos_estoque'
    __table_args__ = (
        db.UniqueConstraint(
            'codigo_armazem',
            'rua_corredor',
            'coluna_baia',
            'nivel_prateleira',
            'posicao_slot',
            name='uq_endereco_componentes'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    estoque_id = db.Column(db.Integer, db.ForeignKey('estoques.id'), nullable=True)
    nome = db.Column(db.String(120), nullable=False, unique=True)
    codigo_localizacao = db.Column(db.String(60), unique=True, nullable=True)
    loja_cd = db.Column(db.String(20), nullable=True)
    setor_zona = db.Column(db.String(30), nullable=True)
    tipo_area = db.Column(db.String(40), nullable=True)
    status = db.Column(db.String(20), default='ativo', nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    tipo_estrutura = db.Column(db.String(20), nullable=True)
    codigo_armazem = db.Column(db.String(20), nullable=True)
    rua_corredor = db.Column(db.String(20), nullable=True)
    coluna_baia = db.Column(db.String(10), nullable=True)
    nivel_prateleira = db.Column(db.String(10), nullable=True)
    posicao_slot = db.Column(db.String(10), nullable=True)
    lado = db.Column(db.String(4), nullable=True)
    ponto_local = db.Column(db.String(255), nullable=True)
    permite_fracionado = db.Column(db.Boolean, default=False)
    permite_mistura_sku = db.Column(db.Boolean, default=False)
    permite_mistura_lote = db.Column(db.Boolean, default=False)
    controle_validade = db.Column(db.String(20), default='nenhum', nullable=True)
    temperatura = db.Column(db.String(20), nullable=True)
    restricoes = db.Column(db.String(255), nullable=True)
    capacidade_caixas = db.Column(db.Integer, nullable=True)
    capacidade_fardos = db.Column(db.Integer, nullable=True)
    capacidade_unidades = db.Column(db.Integer, nullable=True)
    capacidade_pallets = db.Column(db.Integer, nullable=True)
    peso_max_kg = db.Column(db.Float, nullable=True)
    volume_max_m3 = db.Column(db.Float, nullable=True)
    prioridade_picking = db.Column(db.Integer, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    tipo_produto_reservado = db.Column(db.String(120), nullable=True)
    sku_produto = db.Column(db.String(100), nullable=True)
    data_alocacao = db.Column(db.DateTime, nullable=True)
    tipo_endereco = db.Column(db.String(30), nullable=True)
    rua = db.Column(db.String(160))
    numero = db.Column(db.String(20))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(12))
    complemento = db.Column(db.String(120))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    produtos = db.relationship('Produto', backref='endereco', lazy=True)

    def __repr__(self):
        return f'<EnderecoEstoque {self.nome}>'

    def build_codigo_localizacao(self, pad=2):
        """Gera codigo composto padronizado a partir dos componentes."""
        rc = (self.rua_corredor or '').strip().upper()
        cb = (self.coluna_baia or '').strip().zfill(pad)
        nv = (self.nivel_prateleira or '').strip().zfill(pad)
        ps = (self.posicao_slot or '').strip().zfill(pad)
        return '-'.join([rc, cb, nv, ps]) if rc and cb and nv and ps else None

    @property
    def rack_estante(self):
        return self.coluna_baia

    @rack_estante.setter
    def rack_estante(self, valor):
        self.coluna_baia = valor


class RecebimentoFornecedor(db.Model):
    __tablename__ = 'recebimentos_fornecedor'

    STATUS_CRIADO = 'criado'
    STATUS_AGUARDANDO_ARMAZENAGEM = 'aguardando_armazenagem'
    STATUS_CONCLUIDO = 'concluido'
    STATUS_CANCELADO = 'cancelado'
    STATUS_VALIDOS = [
        STATUS_CRIADO,
        STATUS_AGUARDANDO_ARMAZENAGEM,
        STATUS_CONCLUIDO,
        STATUS_CANCELADO,
    ]

    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    fornecedor_documento = db.Column(db.String(30), nullable=True)
    data_entrega = db.Column(db.Date, nullable=True)
    info_nota = db.Column(db.String(255), nullable=True)
    subtotal = db.Column(db.Float, nullable=True, default=0.0)
    desconto = db.Column(db.Float, nullable=True, default=0.0)
    total_pagar = db.Column(db.Float, nullable=True, default=0.0)
    status = db.Column(db.String(30), default=STATUS_CRIADO, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    recebedor_nome = db.Column(db.String(120), nullable=True)
    recebedor_assinatura = db.Column(db.String(255), nullable=True)
    entregador_nome = db.Column(db.String(120), nullable=True)
    entregador_assinatura = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    conferido_em = db.Column(db.DateTime, nullable=True)
    armazenado_em = db.Column(db.DateTime, nullable=True)

    itens = db.relationship('RecebimentoItem', backref='recebimento', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<RecebimentoFornecedor {self.id} - {self.status}>'


class RecebimentoItem(db.Model):
    __tablename__ = 'recebimentos_itens'

    id = db.Column(db.Integer, primary_key=True)
    recebimento_id = db.Column(db.Integer, db.ForeignKey('recebimentos_fornecedor.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    qtd_recebida = db.Column(db.Integer, nullable=False, default=0)
    unidade = db.Column(db.String(10), nullable=True)
    descricao_item = db.Column(db.String(255), nullable=True)
    preco_unitario = db.Column(db.Float, nullable=True, default=0.0)
    total_item = db.Column(db.Float, nullable=True, default=0.0)
    qtd_avaria = db.Column(db.Integer, nullable=False, default=0)
    lote = db.Column(db.String(80), nullable=True)
    validade = db.Column(db.Date, nullable=True)
    endereco_destino_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    produto = db.relationship('Produto')
    endereco_destino = db.relationship('EnderecoEstoque')

    @property
    def qtd_liquida(self):
        return max(int(self.qtd_recebida or 0) - int(self.qtd_avaria or 0), 0)

    def __repr__(self):
        return f'<RecebimentoItem rec={self.recebimento_id} prod={self.produto_id}>'

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

    STATUS_ABERTO = 'aberto'
    STATUS_EM_PREPARO = 'em_preparo'
    STATUS_ENTREGUE = 'entregue'
    STATUS_FECHADO = 'fechado'
    STATUS_CANCELADO = 'cancelado'
    STATUS_IMUTAVEIS = {STATUS_FECHADO, STATUS_CANCELADO}
    TRANSICOES_PERMITIDAS = {
        STATUS_ABERTO: {STATUS_EM_PREPARO, STATUS_ENTREGUE, STATUS_FECHADO, STATUS_CANCELADO},
        STATUS_EM_PREPARO: {STATUS_ENTREGUE, STATUS_FECHADO, STATUS_CANCELADO},
        STATUS_ENTREGUE: {STATUS_FECHADO, STATUS_CANCELADO},
        STATUS_FECHADO: set(),
        STATUS_CANCELADO: set(),
    }

    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable=True)
    caixa_id = db.Column(db.Integer, db.ForeignKey('caixas.id'), nullable=True)
    garcom_id = db.Column(db.Integer, db.ForeignKey('garcons.id'), nullable=True)
    cliente_nome = db.Column(db.String(120))
    cliente_celular = db.Column(db.String(30))
    total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default=STATUS_ABERTO, index=True)  # aberto, em_preparo, entregue, fechado, cancelado
    origem = db.Column(db.String(20), default='interno')  # interno, qr
    metodo_pagamento = db.Column(db.String(50))
    valor_pago = db.Column(db.Float, nullable=True)
    estoque_processado = db.Column(db.Boolean, default=False)
    financeiro_processado = db.Column(db.Boolean, default=False)
    separacao_entrega_concluida = db.Column(db.Boolean, default=False)
    separacao_entrega_em = db.Column(db.DateTime, nullable=True)
    etiqueta_entrega_emitida_em = db.Column(db.DateTime, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    fechado_em = db.Column(db.DateTime)
    observacoes = db.Column(db.Text)

    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')

    @staticmethod
    def _normalizar_status(status, default=STATUS_ABERTO):
        status = (status or default).strip().lower()
        return status if status in Pedido.TRANSICOES_PERMITIDAS else default

    def transitar_para(self, novo_status, on_fechamento=None):
        """Valida e aplica transicao de status do pedido."""
        status_atual = self._normalizar_status(self.status, default=self.STATUS_ABERTO)
        novo_status = self._normalizar_status(novo_status, default=status_atual)

        if status_atual in self.STATUS_IMUTAVEIS and novo_status != status_atual:
            raise ValueError(f'Pedido {status_atual} e imutavel.')
        if novo_status != status_atual and novo_status not in self.TRANSICOES_PERMITIDAS.get(status_atual, set()):
            raise ValueError(f'Transicao invalida: {status_atual} -> {novo_status}.')

        if novo_status == self.STATUS_FECHADO and status_atual != self.STATUS_FECHADO:
            if on_fechamento:
                on_fechamento(self)
            else:
                self.fechado_em = datetime.utcnow()
        elif novo_status == self.STATUS_CANCELADO and status_atual != self.STATUS_CANCELADO:
            self.fechado_em = datetime.utcnow()
            if self.mesa:
                self.mesa.status = 'livre'
        elif self.mesa and novo_status in {self.STATUS_ABERTO, self.STATUS_EM_PREPARO, self.STATUS_ENTREGUE}:
            self.mesa.status = 'ocupada'

        self.status = novo_status
        return self.status

    def calcular_total(self):
        self.total = sum(item.quantidade * item.preco_unitario for item in self.itens)
        return self.total

    def marcar_separacao_entrega(self, concluida=True):
        concluida = bool(concluida)
        self.separacao_entrega_concluida = concluida
        self.separacao_entrega_em = datetime.utcnow() if concluida else None
        return self.separacao_entrega_concluida

    def marcar_etiqueta_entrega_emitida(self):
        self.etiqueta_entrega_emitida_em = datetime.utcnow()
        return self.etiqueta_entrega_emitida_em

    def __repr__(self):
        return f'<Pedido {self.id} - {self.status}>'


class ClientePublico(db.Model):
    __tablename__ = 'clientes_publicos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    celular = db.Column(db.String(30), nullable=False, index=True)
    cpf_cnpj = db.Column(db.String(20), nullable=True, index=True)
    cep = db.Column(db.String(12), nullable=True)
    endereco = db.Column(db.String(180), nullable=True)
    numero = db.Column(db.String(20), nullable=True)
    complemento = db.Column(db.String(120), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    referencia = db.Column(db.String(180), nullable=True)
    recebe_ofertas = db.Column(db.Boolean, default=False)
    observacoes = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ClientePublico {self.nome} ({self.email})>'


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


class Garcom(db.Model):
    __tablename__ = 'garcons'

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    nome = db.Column(db.String(120), nullable=False)
    celular = db.Column(db.String(30))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    pedidos = db.relationship('Pedido', backref='garcom', lazy=True)
    funcionario = db.relationship('Funcionario', backref=db.backref('garcom_perfil', uselist=False))

    def __repr__(self):
        return f'<Garcom {self.nome}>'


class Funcionario(db.Model):
    __tablename__ = 'funcionarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='operador')  # admin, gerente, caixa, operador
    cargo = db.Column(db.String(100), nullable=True)
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


class FuncaoRH(db.Model):
    __tablename__ = 'funcoes_rh'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    permissoes_padrao = db.Column(db.Text)  # JSON list de endpoints permitidos para o perfil
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<FuncaoRH {self.nome}>'


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


class EmpresaConfig(db.Model):
    __tablename__ = 'empresa_config'

    TIPO_NEGOCIO_CONVENIENCIA = 'conveniencia'
    TIPO_NEGOCIO_SUPERMERCADO = 'supermercado'
    TIPO_NEGOCIO_FARMACIA = 'farmacia'
    TIPO_NEGOCIO_MODA = 'moda'
    TIPO_NEGOCIO_HOME_CENTER = 'home_center'
    TIPO_NEGOCIO_OUTRO = 'outro'
    TIPOS_NEGOCIO_VALIDOS = {
        TIPO_NEGOCIO_CONVENIENCIA,
        TIPO_NEGOCIO_SUPERMERCADO,
        TIPO_NEGOCIO_FARMACIA,
        TIPO_NEGOCIO_MODA,
        TIPO_NEGOCIO_HOME_CENTER,
        TIPO_NEGOCIO_OUTRO,
    }

    CANAL_OPERACAO_FISICO = 'fisico'
    CANAL_OPERACAO_ECOMMERCE = 'ecommerce'
    CANAL_OPERACAO_HIBRIDO = 'hibrido'
    CANAIS_OPERACAO_VALIDOS = {
        CANAL_OPERACAO_FISICO,
        CANAL_OPERACAO_ECOMMERCE,
        CANAL_OPERACAO_HIBRIDO,
    }

    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150))
    nome_fantasia = db.Column(db.String(150))
    cnpj = db.Column(db.String(20))
    inscricao_estadual = db.Column(db.String(30))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(12))
    logo_path = db.Column(db.String(255))
    mensagem_comprovante = db.Column(db.String(255))
    cardapio_titulo = db.Column(db.String(120))
    cardapio_subtitulo = db.Column(db.String(255))
    cardapio_mensagem = db.Column(db.String(255))
    cardapio_mostrar_imagem = db.Column(db.Boolean, default=True)
    cardapio_mostrar_descricao = db.Column(db.Boolean, default=True)
    cardapio_qtd_maxima = db.Column(db.Integer, default=20)
    tipo_negocio = db.Column(db.String(30), default=TIPO_NEGOCIO_CONVENIENCIA)
    canal_operacao = db.Column(db.String(30), default=CANAL_OPERACAO_HIBRIDO)
    ecommerce_ativo = db.Column(db.Boolean, default=True)
    ecom_cor_primaria = db.Column(db.String(20), default='#ff7848')
    ecom_cor_secundaria = db.Column(db.String(20), default='#ff5a2a')
    ecom_titulo_banner = db.Column(db.String(140), nullable=True)
    ecom_subtitulo_banner = db.Column(db.String(255), nullable=True)
    ecom_texto_promocao = db.Column(db.String(255), nullable=True)
    ecom_banner_path = db.Column(db.String(255), nullable=True)
    ecom_favicon_path = db.Column(db.String(255), nullable=True)
    ecom_produto_placeholder_path = db.Column(db.String(255), nullable=True)
    ecom_banners_json = db.Column(db.Text, nullable=True)
    ecom_campanhas_json = db.Column(db.Text, nullable=True)
    ecom_footer_bg = db.Column(db.String(20), default='#1f2b38')
    ecom_footer_texto = db.Column(db.String(255), nullable=True)
    ecom_footer_contato = db.Column(db.String(255), nullable=True)
    ecom_footer_creditos = db.Column(db.String(255), nullable=True)
    atendimento_mesas_ativo = db.Column(db.Boolean, default=True)
    separacao_entrega_ativa = db.Column(db.Boolean, default=True)
    emissao_etiqueta_entrega_ativa = db.Column(db.Boolean, default=True)
    separacao_entrega_unir_vendas_off = db.Column(db.Boolean, default=False)
    distribuicao_ativa = db.Column(db.Boolean, default=True)
    modo_distribuicao_pedidos = db.Column(db.String(30), default='round_robin')
    ultimo_garcom_id = db.Column(db.Integer, db.ForeignKey('garcons.id'), nullable=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<EmpresaConfig {self.nome_fantasia or self.razao_social or self.id}>'


class AuditoriaEvento(db.Model):
    __tablename__ = 'auditoria_eventos'

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    funcionario_nome = db.Column(db.String(120))
    funcionario_email = db.Column(db.String(120))
    funcionario_role = db.Column(db.String(20))
    metodo = db.Column(db.String(10), nullable=False)
    endpoint = db.Column(db.String(120))
    rota = db.Column(db.String(255))
    acao = db.Column(db.String(120), nullable=False)
    entidade = db.Column(db.String(80))
    detalhes = db.Column(db.Text)
    status_code = db.Column(db.Integer)
    ip = db.Column(db.String(64))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    funcionario = db.relationship('Funcionario', backref=db.backref('eventos_auditoria', lazy=True))

    def __repr__(self):
        return f'<AuditoriaEvento {self.metodo} {self.rota} ({self.status_code})>'


