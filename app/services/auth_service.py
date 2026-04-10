"""Services do dominio de autenticacao."""

from models import Funcionario, PerfilAcesso, db


class AuthService:
    """Encapsula autenticacao e cadastro inicial de funcionarios."""

    def __init__(self, *, normalizar_matricula, normalizar_texto, normalizar_cpf):
        self._normalizar_matricula = normalizar_matricula
        self._normalizar_texto = normalizar_texto
        self._normalizar_cpf = normalizar_cpf

    def login(self, identificador, senha):
        """Autentica por email ou matricula."""
        identificador = (identificador or '').strip()
        senha = senha or ''
        if not identificador or not senha:
            return None, 'Matricula/email e senha sao obrigatorios.'

        identificador_norm = identificador.lower()
        matricula_norm = self._normalizar_matricula(identificador)
        funcionario = Funcionario.query.filter(
            db.or_(
                db.func.lower(Funcionario.email) == identificador_norm,
                db.func.lower(Funcionario.matricula) == (matricula_norm.lower() if matricula_norm else identificador_norm),
            )
        ).first()
        if not funcionario or not funcionario.check_password(senha):
            return None, 'Matricula/email ou senha incorretos.'
        return funcionario, ''

    def total_funcionarios(self):
        """Retorna total atual de funcionarios."""
        return Funcionario.query.count()

    def get_primeiro_admin(self, email):
        """Busca o usuario inicial esperado para o primeiro acesso."""
        return Funcionario.query.filter(
            db.func.lower(Funcionario.email) == (email or '').lower()
        ).order_by(Funcionario.id.asc()).first()

    def build_novo_funcionario(self, *, nome, email, senha):
        """Cria instancia pronta para persistencia."""
        funcionario = Funcionario(nome=nome, email=email)
        funcionario.set_password(senha)
        funcionario.matricula = None
        return funcionario

    def validar_registro_basico(self, *, email, cpf, perfil_acesso_id, niveis_organograma, nivel_organograma):
        """Executa validacoes de consistencia de cadastro."""
        if Funcionario.query.filter_by(email=email).first():
            return None, 'Email ja cadastrado.'
        if cpf == '__invalid__':
            return None, 'CPF invalido. Informe 11 digitos.'
        if cpf and Funcionario.query.filter_by(cpf=cpf).first():
            return None, 'CPF ja cadastrado para outro funcionario.'
        if nivel_organograma and nivel_organograma not in niveis_organograma:
            return None, 'Nivel de organograma invalido.'
        perfil_acesso = None
        if perfil_acesso_id:
            perfil_acesso = PerfilAcesso.query.get(perfil_acesso_id)
            if not perfil_acesso:
                return None, 'Perfil de acesso invalido.'
        return perfil_acesso, ''
