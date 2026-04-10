from flask import Response, render_template, request

from models import AssistenteLocalFeedback, db
from app.user_messages import resolve_action
from security import json_response


def register_routes(app, context):
    login_required = context['login_required']
    limit = context['_limit']
    parse_date_range = context['_parse_date_range']
    coletar_dashboard_analytics = context['_coletar_dashboard_analytics']
    get_funcionario_logado = context['get_funcionario_logado']
    endpoint_to_pagina = context['ENDPOINT_TO_PAGINA']
    local_ai_assistant = context['local_ai_assistant_getter']
    normalizar_historico = context['_normalizar_historico_assistente']
    normalizar_voto = context['_normalizar_voto_assistente']
    carregar_feedbacks = context['_carregar_feedbacks_assistente_local']
    paginas_permitidas = context['_paginas_permitidas_para_funcionario']

    @app.route('/api/dashboard/analytics')
    @login_required
    def dashboard_analytics_api():
        inicio_periodo, fim_periodo, data_inicial_str, data_final_str = parse_date_range(
            request.args.get('data_inicial'),
            request.args.get('data_final'),
            default_days=7
        )
        analytics = coletar_dashboard_analytics(inicio_periodo, fim_periodo)
        return json_response(
            True,
            'Analytics carregado com sucesso.',
            code='analytics_loaded',
            data={
                'data_inicial': data_inicial_str,
                'data_final': data_final_str,
                **analytics
            },
        )

    @app.route('/api/docs')
    @login_required
    def api_docs():
        return render_template('api/docs.html')

    @app.route('/api/assistente-local/status')
    @login_required
    @limit('60 per minute')
    def assistente_local_status():
        assistant = local_ai_assistant()
        if not app.config.get('LOCAL_AI_ENABLED') or not assistant:
            return json_response(
                False,
                'Assistente local desativado.',
                status=503,
                code='assistant_disabled',
                action=resolve_action(code='assistant_disabled', status_code=503),
            )
        return json_response(True, 'Status do assistente local.', code='assistant_status_loaded', data=assistant.status())

    @app.route('/api/assistente-local/perguntar', methods=['POST'])
    @login_required
    @limit('30 per minute')
    def assistente_local_perguntar():
        assistant = local_ai_assistant()
        if not app.config.get('LOCAL_AI_ENABLED') or not assistant:
            return json_response(
                False,
                'Assistente local desativado.',
                status=503,
                code='assistant_disabled',
                action=resolve_action(code='assistant_disabled', status_code=503),
            )

        payload = request.get_json(silent=True) or {}
        pergunta = (payload.get('pergunta') or '').strip()
        if not pergunta:
            return json_response(
                False,
                'Pergunta obrigatoria.',
                status=400,
                code='assistant_question_required',
                fields={'pergunta': 'Informe uma pergunta com ate 500 caracteres.'},
                action=resolve_action(code='assistant_question_required', status_code=400),
            )
        if len(pergunta) > 500:
            return json_response(
                False,
                'Pergunta invalida.',
                status=400,
                code='assistant_question_too_long',
                fields={'pergunta': 'Use no maximo 500 caracteres.'},
                action=resolve_action(code='assistant_question_too_long', status_code=400),
            )

        endpoint_atual = str(payload.get('endpoint_atual') or '').strip()
        endpoint_resolvido = endpoint_atual.split('.')[-1] if endpoint_atual else ''
        pagina_atual = endpoint_to_pagina.get(endpoint_resolvido)
        historico = normalizar_historico(payload.get('historico') or [])
        funcionario = get_funcionario_logado()
        resposta = assistant.answer(
            pergunta,
            paginas_permitidas=paginas_permitidas(funcionario),
            pagina_atual=pagina_atual,
            tela_atual=(payload.get('tela_atual') or '').strip() or None,
            conversation_history=historico,
            feedback_items=carregar_feedbacks(pagina_atual=pagina_atual),
        )
        return json_response(True, 'Resposta do assistente local gerada com sucesso.', code='assistant_answer_generated', data=resposta)

    @app.route('/api/assistente-local/feedback', methods=['POST'])
    @login_required
    @limit('60 per minute')
    def assistente_local_feedback():
        assistant = local_ai_assistant()
        if not app.config.get('LOCAL_AI_ENABLED') or not assistant:
            return json_response(
                False,
                'Assistente local desativado.',
                status=503,
                code='assistant_disabled',
                action=resolve_action(code='assistant_disabled', status_code=503),
            )

        payload = request.get_json(silent=True) or {}
        response_id = (payload.get('response_id') or '').strip()
        vote = normalizar_voto(payload.get('vote'))
        if not response_id:
            return json_response(
                False,
                'Resposta avaliada obrigatoria.',
                status=400,
                code='assistant_feedback_response_required',
                fields={'response_id': 'Informe a resposta que voce deseja avaliar.'},
                action=resolve_action(code='assistant_feedback_response_required', status_code=400),
            )
        if not vote:
            return json_response(
                False,
                'Voto obrigatorio.',
                status=400,
                code='assistant_feedback_vote_required',
                fields={'vote': 'Escolha like ou dislike para continuar.'},
                action=resolve_action(code='assistant_feedback_vote_required', status_code=400),
            )

        endpoint_atual = str(payload.get('endpoint_atual') or '').strip()
        endpoint_resolvido = endpoint_atual.split('.')[-1] if endpoint_atual else ''
        pagina_atual = endpoint_to_pagina.get(endpoint_resolvido)
        funcionario = get_funcionario_logado()
        if not funcionario:
            return json_response(
                False,
                'Login obrigatorio.',
                status=401,
                code='auth_required',
                action=resolve_action(code='auth_required', status_code=401),
            )

        matched_doc_ids = []
        for item in payload.get('matched_doc_ids') or []:
            texto = str(item).strip()
            if texto:
                matched_doc_ids.append(texto)
            if len(matched_doc_ids) >= 8:
                break

        registro = AssistenteLocalFeedback.query.filter_by(
            funcionario_id=funcionario.id,
            response_id=response_id,
        ).first()
        if not registro:
            registro = AssistenteLocalFeedback(
                funcionario_id=funcionario.id,
                response_id=response_id,
            )
            db.session.add(registro)

        registro.vote = vote
        registro.question = (payload.get('question_text') or '').strip()[:2000] or None
        registro.answer = (payload.get('answer_text') or '').strip()[:5000] or None
        registro.reason = (payload.get('reason') or '').strip()[:255] or None
        registro.endpoint_atual = endpoint_resolvido or None
        registro.pagina_atual = pagina_atual or None
        registro.tela_atual = (payload.get('tela_atual') or '').strip()[:120] or None
        registro.matched_doc_ids_json = context['json_dumps'](matched_doc_ids)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return json_response(
                False,
                'Nao foi possivel salvar o feedback agora.',
                status=500,
                code='assistant_feedback_save_failed',
                action=resolve_action(code='assistant_feedback_save_failed', status_code=500),
            )

        return json_response(True, 'Feedback da assistente registrado com sucesso.', code='assistant_feedback_saved', data={
            'vote': registro.vote,
            'response_id': registro.response_id,
        })
