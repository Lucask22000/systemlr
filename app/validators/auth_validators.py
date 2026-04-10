"""Schemas simples para validacao do fluxo de autenticacao."""


class LoginSchema:
    """Valida payload do formulario de login."""

    def validate(self, data):
        errors = {}
        identificador = (data.get('login') or data.get('email') or '').strip()
        senha = data.get('senha', '')
        if not identificador:
            errors['login'] = 'Matricula/email e senha sao obrigatorios.'
        if not senha:
            errors['senha'] = 'Matricula/email e senha sao obrigatorios.'
        return (not errors), errors


class RegistroSchema:
    """Valida campos essenciais do cadastro de funcionario."""

    def validate(self, data):
        errors = {}
        nome = (data.get('nome') or '').strip()
        email = (data.get('email') or '').strip()
        senha = data.get('senha', '')
        confirmacao_senha = data.get('confirmacao_senha', '')
        if not nome:
            errors['nome'] = 'Nome e obrigatorio.'
        if not email:
            errors['email'] = 'Email e obrigatorio.'
        if not senha:
            errors['senha'] = 'Senha e obrigatoria.'
        if senha and len(senha) < 6:
            errors['senha'] = 'A senha deve ter no minimo 6 caracteres.'
        if senha != confirmacao_senha:
            errors['confirmacao_senha'] = 'As senhas nao conferem.'
        return (not errors), errors
