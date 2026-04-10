"""Service de permissao por pagina/endpoint."""

from app.constants import API_FALLBACK_ACCESS_PAGES, ENDPOINT_TO_PAGINA


class PermissaoService:
    """Centraliza o calculo de paginas permitidas e acesso por endpoint."""

    def __init__(self, *, resolver_paginas):
        self._resolver_paginas = resolver_paginas

    def get_paginas_permitidas(self, funcionario):
        """Retorna paginas efetivas disponiveis ao funcionario."""
        return self._resolver_paginas(funcionario)

    def tem_acesso(self, funcionario, endpoint, *, is_api_request=False):
        """Valida acesso ao endpoint considerando fallback para APIs."""
        if not funcionario:
            return False
        if funcionario.role == 'admin':
            return True
        if not funcionario.controle_acesso_ativo:
            return True

        paginas_resolvidas = set(self.get_paginas_permitidas(funcionario))
        pagina = ENDPOINT_TO_PAGINA.get(endpoint)
        if not pagina:
            if is_api_request:
                return bool(paginas_resolvidas.intersection(API_FALLBACK_ACCESS_PAGES))
            return True
        return pagina in paginas_resolvidas
