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
    __table_args__ = (
        db.Index('ix_produtos_categoria_fornecedor', 'categoria_id', 'fornecedor_id'),
        db.Index('ix_produtos_endereco_ativo', 'endereco_id', 'ativo'),
    )

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
    tipo_movimentacao = db.Column(db.String(20), default='manual', nullable=False)
    fora_picking = db.Column(db.Boolean, default=False)
    prioridade_reabastecimento = db.Column(db.Integer, nullable=True)
    ultima_baixa_picking_em = db.Column(db.DateTime, nullable=True)
    servico_montagem_disponivel = db.Column(db.Boolean, default=False)
    servico_instalacao_disponivel = db.Column(db.Boolean, default=False)
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
    __table_args__ = (
        db.Index('ix_movimentacoes_tipo_criado_em', 'tipo', 'criado_em'),
        db.Index('ix_movimentacoes_produto_criado_em', 'produto_id', 'criado_em'),
    )
    
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

    endereco_origem = db.relationship(
        'EnderecoEstoque',
        foreign_keys=[endereco_origem_id],
        backref=db.backref('movimentacoes_como_origem', lazy=True),
        lazy='select',
    )
    endereco_destino = db.relationship(
        'EnderecoEstoque',
        foreign_keys=[endereco_destino_id],
        backref=db.backref('movimentacoes_como_destino', lazy=True),
        lazy='select',
    )
    
    def __repr__(self):
        return f'<Movimentacao {self.produto_id} - {self.tipo}>'


class EquipamentoMovimentacao(db.Model):
    __tablename__ = 'equipamentos_movimentacao'

    TIPO_EMPILHADEIRA = 'empilhadeira'
    TIPO_PALETEIRA = 'paleteira'
    TIPO_CARRINHO = 'carrinho'
    TIPOS_VALIDOS = [TIPO_EMPILHADEIRA, TIPO_PALETEIRA, TIPO_CARRINHO]

    STATUS_OPERACIONAL = 'operacional'
    STATUS_MANUTENCAO = 'manutencao'
    STATUS_INATIVO = 'inativo'
    STATUS_VALIDOS = [STATUS_OPERACIONAL, STATUS_MANUTENCAO, STATUS_INATIVO]

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(40), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default=TIPO_EMPILHADEIRA)
    placa = db.Column(db.String(20), nullable=True)
    capacidade_kg = db.Column(db.Float, nullable=True)
    bateria_codigo = db.Column(db.String(40), nullable=True)
    bateria_nivel = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), nullable=False, default=STATUS_OPERACIONAL)
    proxima_manutencao_em = db.Column(db.Date, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    manutencoes = db.relationship(
        'ManutencaoEquipamento',
        backref='equipamento',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<EquipamentoMovimentacao {self.codigo} - {self.tipo}>'


class ManutencaoEquipamento(db.Model):
    __tablename__ = 'manutencoes_equipamento'

    id = db.Column(db.Integer, primary_key=True)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamentos_movimentacao.id'), nullable=False, index=True)
    tipo = db.Column(db.String(20), nullable=False, default='preventiva')
    descricao = db.Column(db.String(255), nullable=False)
    custo = db.Column(db.Float, nullable=True)
    realizado_em = db.Column(db.Date, nullable=True)
    proxima_em = db.Column(db.Date, nullable=True)
    responsavel = db.Column(db.String(120), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<ManutencaoEquipamento eq={self.equipamento_id} tipo={self.tipo}>'


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
    codigo_filial = db.Column(db.String(20), nullable=True, index=True)
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


funcionario_estoques = db.Table(
    'funcionario_estoques',
    db.Column('funcionario_id', db.Integer, db.ForeignKey('funcionarios.id'), primary_key=True),
    db.Column('estoque_id', db.Integer, db.ForeignKey('estoques.id'), primary_key=True),
)


class EnderecoEstoque(db.Model):
    __tablename__ = 'enderecos_estoque'
    __table_args__ = (
        db.Index('ix_enderecos_estoque_estoque_status', 'estoque_id', 'status'),
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
    __table_args__ = (
        db.Index('ix_recebimentos_status_criado_em', 'status', 'criado_em'),
        db.Index('ix_recebimentos_fornecedor_criado_em', 'fornecedor_id', 'criado_em'),
    )

    TIPO_COMPRA_REVENDA = 'compra_revenda'
    TIPO_USO_CONSUMO = 'uso_consumo_operacional'
    TIPO_BONIFICACAO = 'bonificacao'
    TIPO_CONSIGNADO = 'consignado'
    TIPO_RETORNO_INDUSTRIALIZACAO = 'retorno_industrializacao'
    TIPOS_VALIDOS = [
        TIPO_COMPRA_REVENDA,
        TIPO_USO_CONSUMO,
        TIPO_BONIFICACAO,
        TIPO_CONSIGNADO,
        TIPO_RETORNO_INDUSTRIALIZACAO,
    ]

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
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=True)
    tipo_recebimento = db.Column(db.String(40), nullable=False, default=TIPO_COMPRA_REVENDA)
    fornecedor_documento = db.Column(db.String(30), nullable=True)
    data_entrega = db.Column(db.Date, nullable=True)
    info_nota = db.Column(db.String(255), nullable=True)
    subtotal = db.Column(db.Float, nullable=True, default=0.0)
    desconto = db.Column(db.Float, nullable=True, default=0.0)
    total_pagar = db.Column(db.Float, nullable=True, default=0.0)
    status = db.Column(db.String(30), default=STATUS_CRIADO, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    recebedor_funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    recebedor_nome = db.Column(db.String(120), nullable=True)
    recebedor_assinatura = db.Column(db.String(255), nullable=True)
    entregador_nome = db.Column(db.String(120), nullable=True)
    entregador_assinatura = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    conferido_em = db.Column(db.DateTime, nullable=True)
    armazenado_em = db.Column(db.DateTime, nullable=True)

    itens = db.relationship('RecebimentoItem', backref='recebimento', lazy=True, cascade='all, delete-orphan')
    recebedor_funcionario = db.relationship('Funcionario', foreign_keys=[recebedor_funcionario_id], lazy='select')

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
    __table_args__ = (
        db.Index('ix_pedidos_status_criado_em', 'status', 'criado_em'),
        db.Index('ix_pedidos_status_fechado_em', 'status', 'fechado_em'),
    )

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
    rota_entrega = db.Column(db.String(120), nullable=True)
    ordem_rota = db.Column(db.Integer, nullable=True)
    local_saida = db.Column(db.String(160), nullable=True)
    veiculo_tipo = db.Column(db.String(80), nullable=True)
    veiculo_placa = db.Column(db.String(20), nullable=True)
    motorista_nome = db.Column(db.String(120), nullable=True)
    empresa_terceirizada = db.Column(db.String(150), nullable=True)
    nota_fiscal_numero = db.Column(db.String(60), nullable=True)
    nota_fiscal_chave = db.Column(db.String(120), nullable=True)
    nota_fiscal_emitida_em = db.Column(db.DateTime, nullable=True)
    saiu_para_entrega_em = db.Column(db.DateTime, nullable=True)
    entrega_concluida_em = db.Column(db.DateTime, nullable=True)
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
    __table_args__ = (
        db.Index('ix_funcionarios_matricula_ativo', 'matricula', 'ativo'),
        db.Index('ix_funcionarios_email_ativo', 'email', 'ativo'),
        db.Index('ix_funcionarios_cpf_ativo', 'cpf', 'ativo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    numero_cadastro = db.Column(db.Integer, unique=True, nullable=True, index=True)
    matricula = db.Column(db.String(30), unique=True, nullable=True, index=True)
    cpf = db.Column(db.String(14), nullable=True, index=True)
    rg = db.Column(db.String(20), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    celular = db.Column(db.String(30), nullable=True)
    cep = db.Column(db.String(12), nullable=True)
    endereco = db.Column(db.String(180), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    imagem_perfil_path = db.Column(db.String(255), nullable=True)
    permitir_editar_imagem_perfil = db.Column(db.Boolean, default=False)
    senha_provisoria = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='operador')  # admin, gerente, caixa, operador
    cargo = db.Column(db.String(100), nullable=True)
    departamento = db.Column(db.String(80), nullable=True)
    time_nome = db.Column(db.String(80), nullable=True)
    nivel_organograma = db.Column(db.String(40), nullable=True)
    pagina_inicial = db.Column(db.String(30), default='dashboard')
    receber_alertas = db.Column(db.Boolean, default=True)
    restricao_estoques_ativa = db.Column(db.Boolean, default=False)
    estoque_principal_id = db.Column(db.Integer, db.ForeignKey('estoques.id'), nullable=True)
    perfil_acesso_id = db.Column(db.Integer, db.ForeignKey('perfis_acesso.id'), nullable=True)
    superior_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    controle_acesso_ativo = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    permissoes = db.relationship('PermissaoAcesso', backref='funcionario', lazy=True, cascade='all, delete-orphan')
    estoque_principal = db.relationship('Estoque', foreign_keys=[estoque_principal_id], lazy='select')
    perfil_acesso = db.relationship('PerfilAcesso', foreign_keys=[perfil_acesso_id], lazy='select')
    estoques_permitidos = db.relationship(
        'Estoque',
        secondary=funcionario_estoques,
        backref=db.backref('funcionarios_vinculados', lazy='select'),
        lazy='select',
    )
    superior = db.relationship('Funcionario', remote_side=[id], backref=db.backref('subordinados', lazy=True))

    def set_password(self, senha):
        """Hash e armazena a senha."""
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Funcionario {self.nome} - {self.role}>'


class AlmoxarifadoAtribuicao(db.Model):
    __tablename__ = 'almoxarifado_atribuicoes'

    DESTINO_FUNCIONARIO = 'funcionario'
    DESTINO_SETOR = 'setor'
    DESTINOS_VALIDOS = [DESTINO_FUNCIONARIO, DESTINO_SETOR]

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False, index=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True)
    registrado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    destino_tipo = db.Column(db.String(20), nullable=False, default=DESTINO_FUNCIONARIO)
    nome_destino = db.Column(db.String(120), nullable=False)
    setor_destino = db.Column(db.String(80), nullable=True)
    matricula_referencia = db.Column(db.String(30), nullable=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    observacoes = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    produto = db.relationship('Produto', foreign_keys=[produto_id], lazy='select')
    funcionario = db.relationship('Funcionario', foreign_keys=[funcionario_id], lazy='select')
    registrado_por = db.relationship('Funcionario', foreign_keys=[registrado_por_id], lazy='select')

    def __repr__(self):
        return f'<AlmoxarifadoAtribuicao {self.id} prod={self.produto_id} destino={self.destino_tipo}>'


class FuncaoRH(db.Model):
    __tablename__ = 'funcoes_rh'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    permissoes_padrao = db.Column(db.Text)  # Campo legado migrado para PerfilAcesso
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<FuncaoRH {self.nome}>'


class PerfilAcesso(db.Model):
    __tablename__ = 'perfis_acesso'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    permissoes_padrao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PerfilAcesso {self.nome}>'


class PermissaoAcesso(db.Model):
    __tablename__ = 'permissoes_acesso'

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    pagina = db.Column(db.String(80), nullable=False)
    permitido = db.Column(db.Boolean, default=True, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('funcionario_id', 'pagina', name='uq_funcionario_pagina'),
    )

    def __repr__(self):
        return f'<PermissaoAcesso funcionario={self.funcionario_id} pagina={self.pagina} permitido={self.permitido}>'


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


class LancamentoFinanceiro(db.Model):
    __tablename__ = 'lancamentos_financeiros'
    __table_args__ = (
        db.Index('ix_lancamentos_tipo_data_competencia', 'tipo', 'data_competencia'),
    )

    TIPO_CONSUMO_PROPRIO = 'consumo_proprio'
    TIPO_DESPESA = 'despesa'
    TIPO_RECEITA = 'receita'
    TIPO_AJUSTE = 'ajuste'
    TIPOS = [TIPO_CONSUMO_PROPRIO, TIPO_DESPESA, TIPO_RECEITA, TIPO_AJUSTE]

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(30), nullable=False, index=True)
    categoria = db.Column(db.String(80), nullable=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_competencia = db.Column(db.Date, nullable=False, index=True)
    incluir_contabilidade = db.Column(db.Boolean, default=True, nullable=False)
    enviado_contador = db.Column(db.Boolean, default=False, nullable=False)
    enviado_em = db.Column(db.DateTime, nullable=True)
    referencia_documento = db.Column(db.String(120), nullable=True)
    centro_custo = db.Column(db.String(120), nullable=True)

    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=True)
    quantidade = db.Column(db.Float, nullable=True)

    criado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    produto = db.relationship('Produto', backref=db.backref('lancamentos_financeiros', lazy=True))
    criado_por = db.relationship('Funcionario', backref=db.backref('lancamentos_financeiros', lazy=True))

    def __repr__(self):
        return f'<LancamentoFinanceiro {self.tipo} {self.valor}>'


class FundoSolicitacao(db.Model):
    __tablename__ = 'fundos_solicitacoes'

    TIPO_APORTE = 'aporte'
    TIPO_SAQUE = 'saque'
    TIPOS_VALIDOS = [TIPO_APORTE, TIPO_SAQUE]

    STATUS_SOLICITADA = 'solicitada'
    STATUS_APROVADA = 'aprovada'
    STATUS_REJEITADA = 'rejeitada'
    STATUS_LIBERADA = 'liberada'
    STATUS_CANCELADA = 'cancelada'
    STATUS_VALIDOS = [STATUS_SOLICITADA, STATUS_APROVADA, STATUS_REJEITADA, STATUS_LIBERADA, STATUS_CANCELADA]

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False, default=TIPO_APORTE)
    categoria = db.Column(db.String(80), nullable=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    centro_custo = db.Column(db.String(120), nullable=True)
    referencia_documento = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), nullable=False, default=STATUS_SOLICITADA, index=True)
    motivo_rejeicao = db.Column(db.String(255), nullable=True)
    solicitado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True)
    aprovado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    liberado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    lancamento_financeiro_id = db.Column(db.Integer, db.ForeignKey('lancamentos_financeiros.id'), nullable=True)
    solicitado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    aprovado_em = db.Column(db.DateTime, nullable=True)
    liberado_em = db.Column(db.DateTime, nullable=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    solicitado_por = db.relationship('Funcionario', foreign_keys=[solicitado_por_id], backref=db.backref('fundos_solicitados', lazy=True))
    aprovado_por = db.relationship('Funcionario', foreign_keys=[aprovado_por_id], backref=db.backref('fundos_aprovados', lazy=True))
    liberado_por = db.relationship('Funcionario', foreign_keys=[liberado_por_id], backref=db.backref('fundos_liberados', lazy=True))
    lancamento_financeiro = db.relationship('LancamentoFinanceiro', backref=db.backref('fundo_origem', uselist=False))

    def __repr__(self):
        return f'<FundoSolicitacao {self.id} {self.tipo} {self.status}>'


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
    codigo_empresa = db.Column(db.String(20))
    cnpj = db.Column(db.String(20))
    inscricao_estadual = db.Column(db.String(30))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(12))
    logo_path = db.Column(db.String(255))
    favicon_path = db.Column(db.String(255), nullable=True)
    app_icon_path = db.Column(db.String(255), nullable=True)
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
    pagamentos_pdv_json = db.Column(db.Text, nullable=True)
    pagamentos_ecommerce_json = db.Column(db.Text, nullable=True)
    integracoes_pdv_json = db.Column(db.Text, nullable=True)
    integracoes_ecommerce_json = db.Column(db.Text, nullable=True)
    atendimento_mesas_ativo = db.Column(db.Boolean, default=True)
    reposicao_loja_fisica_ativa = db.Column(db.Boolean, default=True)
    emissao_etiqueta_loja_ativa = db.Column(db.Boolean, default=True)
    emissao_etiqueta_endereco_ativa = db.Column(db.Boolean, default=True)
    separacao_entrega_ativa = db.Column(db.Boolean, default=True)
    emissao_etiqueta_entrega_ativa = db.Column(db.Boolean, default=True)
    separacao_entrega_unir_vendas_off = db.Column(db.Boolean, default=False)
    roteirizacao_entrega_ativa = db.Column(db.Boolean, default=True)
    emissao_nota_entrega_ativa = db.Column(db.Boolean, default=True)
    entrega_local_saida_padrao = db.Column(db.String(160), nullable=True)
    entrega_veiculo_padrao = db.Column(db.String(80), nullable=True)
    entrega_motorista_padrao = db.Column(db.String(120), nullable=True)
    entrega_horario_fechamento_roteirizacao = db.Column(db.String(5), nullable=True)
    entrega_veiculos_json = db.Column(db.Text, nullable=True)
    entrega_terceirizadas_json = db.Column(db.Text, nullable=True)
    entrega_regras_roteirizacao_json = db.Column(db.Text, nullable=True)
    servicos_tecnicos_ativos = db.Column(db.Boolean, default=False)
    servico_montagem_instalacao_ativo = db.Column(db.Boolean, default=False)
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


class AssistenteLocalFeedback(db.Model):
    __tablename__ = 'assistente_local_feedback'
    __table_args__ = (
        db.UniqueConstraint('funcionario_id', 'response_id', name='uq_assistente_feedback_funcionario_response'),
    )

    VOTO_LIKE = 'like'
    VOTO_DISLIKE = 'dislike'
    VOTOS_VALIDOS = [VOTO_LIKE, VOTO_DISLIKE]

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False, index=True)
    response_id = db.Column(db.String(64), nullable=False, index=True)
    vote = db.Column(db.String(10), nullable=False, index=True)
    question = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=True)
    reason = db.Column(db.String(255), nullable=True)
    endpoint_atual = db.Column(db.String(120), nullable=True)
    pagina_atual = db.Column(db.String(80), nullable=True, index=True)
    tela_atual = db.Column(db.String(120), nullable=True)
    matched_doc_ids_json = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    funcionario = db.relationship('Funcionario', backref=db.backref('feedbacks_assistente_local', lazy=True))

    def __repr__(self):
        return f'<AssistenteLocalFeedback funcionario={self.funcionario_id} vote={self.vote}>'


class OrdemServico(db.Model):
    __tablename__ = 'ordens_servico'

    TIPO_ORDEM_SERVICO = 'ordem_servico'
    TIPO_AVARIA = 'avaria'
    TIPO_INSPECAO = 'inspecao'
    TIPOS_VALIDOS = [TIPO_ORDEM_SERVICO, TIPO_AVARIA, TIPO_INSPECAO]

    SERVICO_MONTAGEM = 'montagem'
    SERVICO_INSTALACAO = 'instalacao'
    SERVICO_NENHUM = 'nenhum'
    SERVICOS_VALIDOS = [SERVICO_NENHUM, SERVICO_MONTAGEM, SERVICO_INSTALACAO]

    STATUS_ABERTA = 'aberta'
    STATUS_ENVIADA = 'enviada'
    STATUS_EM_EXECUCAO = 'em_execucao'
    STATUS_CONCLUIDA = 'concluida'
    STATUS_CANCELADA = 'cancelada'
    STATUS_VALIDOS = [STATUS_ABERTA, STATUS_ENVIADA, STATUS_EM_EXECUCAO, STATUS_CONCLUIDA, STATUS_CANCELADA]

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(160), nullable=False)
    tipo = db.Column(db.String(30), nullable=False, default=TIPO_ORDEM_SERVICO, index=True)
    servico_tipo = db.Column(db.String(20), nullable=False, default=SERVICO_NENHUM)
    prioridade = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(30), nullable=False, default=STATUS_ABERTA, index=True)
    descricao = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    avaria_detalhes = db.Column(db.Text, nullable=True)
    inspecao_detalhes = db.Column(db.Text, nullable=True)
    resultado_inspecao = db.Column(db.String(120), nullable=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=True, index=True)
    funcionario_destino_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True)
    criado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    data_agendada = db.Column(db.Date, nullable=True)
    enviada_em = db.Column(db.DateTime, nullable=True)
    iniciado_em = db.Column(db.DateTime, nullable=True)
    concluida_em = db.Column(db.DateTime, nullable=True)
    retorno_tecnico = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    produto = db.relationship('Produto', backref=db.backref('ordens_servico', lazy=True))
    pedido = db.relationship('Pedido', backref=db.backref('ordens_servico', lazy=True))
    funcionario_destino = db.relationship('Funcionario', foreign_keys=[funcionario_destino_id], backref=db.backref('ordens_recebidas', lazy=True))
    criado_por = db.relationship('Funcionario', foreign_keys=[criado_por_id], backref=db.backref('ordens_criadas', lazy=True))

    def __repr__(self):
        return f'<OrdemServico #{self.id} {self.tipo} {self.status}>'


class ChamadoInterno(db.Model):
    __tablename__ = 'chamados_internos'

    CATEGORIA_SISTEMA = 'sistema'
    CATEGORIA_ESTOQUE = 'estoque'
    CATEGORIA_FINANCEIRO = 'financeiro'
    CATEGORIA_VENDAS = 'vendas'
    CATEGORIA_RH = 'rh'
    CATEGORIA_EXPEDICAO = 'expedicao'
    CATEGORIA_INFRA = 'infraestrutura'
    CATEGORIAS_VALIDAS = [
        CATEGORIA_SISTEMA,
        CATEGORIA_ESTOQUE,
        CATEGORIA_FINANCEIRO,
        CATEGORIA_VENDAS,
        CATEGORIA_RH,
        CATEGORIA_EXPEDICAO,
        CATEGORIA_INFRA,
    ]

    PRIORIDADES_VALIDAS = ['baixa', 'media', 'alta', 'critica']
    STATUS_ABERTO = 'aberto'
    STATUS_TRIAGEM = 'triagem'
    STATUS_EM_ANDAMENTO = 'em_andamento'
    STATUS_AGUARDANDO = 'aguardando'
    STATUS_CONCLUIDO = 'concluido'
    STATUS_CANCELADO = 'cancelado'
    STATUS_VALIDOS = [
        STATUS_ABERTO,
        STATUS_TRIAGEM,
        STATUS_EM_ANDAMENTO,
        STATUS_AGUARDANDO,
        STATUS_CONCLUIDO,
        STATUS_CANCELADO,
    ]

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(160), nullable=False, index=True)
    categoria = db.Column(db.String(40), nullable=False, default=CATEGORIA_SISTEMA, index=True)
    prioridade = db.Column(db.String(20), nullable=False, default='media', index=True)
    status = db.Column(db.String(30), nullable=False, default=STATUS_ABERTO, index=True)
    setor_origem = db.Column(db.String(80), nullable=True)
    descricao = db.Column(db.Text, nullable=False)
    resolucao = db.Column(db.Text, nullable=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False, index=True)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True)
    aberto_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    concluido_em = db.Column(db.DateTime, nullable=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    solicitante = db.relationship('Funcionario', foreign_keys=[solicitante_id], backref=db.backref('chamados_abertos', lazy=True))
    responsavel = db.relationship('Funcionario', foreign_keys=[responsavel_id], backref=db.backref('chamados_responsaveis', lazy=True))

    def __repr__(self):
        return f'<ChamadoInterno #{self.id} {self.status}>'


