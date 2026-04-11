"""Registro de context processors da aplicacao.

Extracao incremental do bloco de injecao de contexto de app/__init__.py.
"""

import os
from datetime import datetime

from flask import request, url_for


def register_context_processors(app, *, dependencies):
    """Registra context processor legado com dependencias injetadas."""
    get_funcionario_logado = dependencies['get_funcionario_logado']
    empresa_config_model = dependencies['empresa_config_model']
    produto_model = dependencies['produto_model']
    endpoint_to_pagina = dependencies['endpoint_to_pagina']
    titulo_tela_atual = dependencies['titulo_tela_atual']
    estoques_contexto_disponiveis_fn = dependencies['estoques_contexto_disponiveis_fn']
    estoque_contexto_selecionado_id_fn = dependencies['estoque_contexto_selecionado_id_fn']
    ensure_csrf_token_fn = dependencies['ensure_csrf_token_fn']
    csrf_input_tag_fn = dependencies['csrf_input_tag_fn']
    paginas_permitidas_para_funcionario_fn = dependencies['paginas_permitidas_para_funcionario_fn']
    menu_agrupado_para_paginas_fn = dependencies['menu_agrupado_para_paginas_fn']
    menu_navegacao_principal_fn = dependencies['menu_navegacao_principal_fn']
    montar_indicadores_contexto_usuario_fn = dependencies['montar_indicadores_contexto_usuario_fn']
    registrar_debug_menu_fn = dependencies['registrar_debug_menu_fn']
    local_ai_assistant_getter = dependencies['local_ai_assistant_getter']

    @app.context_processor
    def inject_user():
        funcionario_logado = get_funcionario_logado()
        empresa_config = empresa_config_model.query.first()
        atendimento_mesas_ativo = not empresa_config or empresa_config.atendimento_mesas_ativo is not False
        secao_atual_nome, tela_atual_nome = titulo_tela_atual()
        endpoint_atual = request.endpoint or ''
        pagina_atual_menu = endpoint_to_pagina.get(endpoint_atual)
        estoques_contexto_disponiveis = estoques_contexto_disponiveis_fn(funcionario_logado) if funcionario_logado else []
        estoque_contexto_id = estoque_contexto_selecionado_id_fn(funcionario_logado) if funcionario_logado else None

        produto_imagem_padrao_path = (
            (empresa_config.ecom_produto_placeholder_path if empresa_config else None)
            or 'img/placeholders/imgindisponivel.png'
        )
        favicon_path = (
            (empresa_config.favicon_path if empresa_config else None)
            or (empresa_config.ecom_favicon_path if empresa_config else None)
        )
        store_favicon_path = (
            (empresa_config.ecom_favicon_path if empresa_config else None)
            or favicon_path
        )
        app_icon_path = (
            (empresa_config.app_icon_path if empresa_config else None)
            or (empresa_config.logo_path if empresa_config else None)
            or favicon_path
            or 'uploads/empresa/Loja_do_Lucas_logo.png'
        )
        csrf_token_value = ensure_csrf_token_fn()

        paginas_permitidas_usuario = paginas_permitidas_para_funcionario_fn(funcionario_logado) if funcionario_logado else set()
        menu_paginas_usuario = menu_agrupado_para_paginas_fn(paginas_permitidas_usuario) if funcionario_logado else []
        menu_navegacao_principal = menu_navegacao_principal_fn(
            funcionario_logado,
            empresa_config=empresa_config,
            atendimento_mesas_ativo=atendimento_mesas_ativo,
            current_page_key=pagina_atual_menu,
        ) if funcionario_logado else []

        user_agent_texto = (request.user_agent.string or '').lower()
        acesso_mobile_web = any(token in user_agent_texto for token in ['android', 'iphone', 'ipad', 'ipod', 'mobile'])
        apk_download_url = None
        for candidato in ['downloads/app-release.apk', 'downloads/systemlr.apk', 'downloads/app-latest.apk']:
            caminho = os.path.join(app.static_folder, candidato)
            if os.path.exists(caminho):
                apk_download_url = url_for('static', filename=candidato)
                break

        assistente = local_ai_assistant_getter() if callable(local_ai_assistant_getter) else None
        assistente_status = (
            assistente.status()
            if funcionario_logado and app.config.get('LOCAL_AI_ENABLED') and assistente
            else {'enabled': False}
        )
        indicadores_contexto_usuario = (
            montar_indicadores_contexto_usuario_fn(funcionario_logado, paginas_permitidas_usuario)
            if funcionario_logado else []
        )
        if funcionario_logado:
            registrar_debug_menu_fn(funcionario_logado, paginas_permitidas_usuario, menu_paginas_usuario)

        return {
            'ano_atual': datetime.utcnow().year,
            'total_alertas': produto_model.query.filter(
                produto_model.quantidade_estoque < produto_model.quantidade_minima,
                produto_model.ativo == True,
            ).count(),
            'funcionario_logado': funcionario_logado,
            'empresa_config': empresa_config,
            'atendimento_mesas_ativo': atendimento_mesas_ativo,
            'produto_imagem_padrao_path': produto_imagem_padrao_path,
            'favicon_path': favicon_path,
            'store_favicon_path': store_favicon_path,
            'app_icon_path': app_icon_path,
            'paginas_permitidas_usuario': paginas_permitidas_usuario,
            'menu_paginas_usuario': menu_paginas_usuario,
            'menu_navegacao_principal': menu_navegacao_principal,
            'pagina_atual_menu': pagina_atual_menu,
            'secao_atual_nome': secao_atual_nome,
            'tela_atual_nome': tela_atual_nome,
            'endpoint_atual': endpoint_atual,
            'estoques_contexto_disponiveis': estoques_contexto_disponiveis,
            'estoque_contexto_id': estoque_contexto_id,
            'assistente_local_status': assistente_status,
            'indicadores_contexto_usuario': indicadores_contexto_usuario,
            'apk_download_url': apk_download_url,
            'show_apk_download_mobile_web': bool(apk_download_url and acesso_mobile_web),
            'csrf_token': csrf_token_value,
            'csrf_input': csrf_input_tag_fn(),
        }

    return inject_user
