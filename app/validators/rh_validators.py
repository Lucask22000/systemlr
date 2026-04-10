"""Validacoes do dominio de RH."""


class FuncionarioSchema:
    """Valida campos obrigatorios minimos de funcionario."""

    def validate(self, data):
        errors = {}
        if not (data.get('nome') or '').strip():
            errors['nome'] = 'Nome do funcionario e obrigatorio.'
        if not (data.get('email') or '').strip():
            errors['email'] = 'Email do funcionario e obrigatorio.'
        return (not errors), errors
