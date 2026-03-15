import importlib
import math
import os
import re
import subprocess
import sys
import threading
import unicodedata
import uuid
from pathlib import Path


LOCAL_AI_PACKAGES = (
    'torch==2.5.1',
    'sentence-transformers==3.3.1',
    'huggingface-hub==0.26.2',
    'safetensors==0.4.5',
)


class LocalAIAssistant:
    def __init__(self, app, knowledge_builder):
        self.app = app
        self.knowledge_builder = knowledge_builder
        self.model_id = app.config.get(
            'LOCAL_AI_MODEL_ID',
            'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        )
        raw_candidates = app.config.get('LOCAL_AI_MODEL_CANDIDATES') or self.model_id
        self.model_candidates = [
            item.strip()
            for item in str(raw_candidates).split(',')
            if item and item.strip()
        ] or [self.model_id]
        self.enabled = bool(app.config.get('LOCAL_AI_ENABLED', True))
        self.auto_install = bool(app.config.get('LOCAL_AI_AUTO_INSTALL', True))
        self.max_history_messages = int(app.config.get('LOCAL_AI_MAX_HISTORY_MESSAGES', 5) or 5)
        self.instance_dir = Path(app.instance_path) / 'local_ai'
        self.model_dir = self.instance_dir / 'semantic-model'
        self._lock = threading.Lock()
        self._thread = None
        self._status = {
            'enabled': self.enabled,
            'ready': False,
            'state': 'idle',
            'mode': 'lexical',
            'message': 'Marcia pronta para inicializar.',
            'document_count': 0,
            'model_id': self.model_id,
            'last_error': None,
        }
        self._documents = []
        self._document_vectors = []
        self._encoder = None
        self._query_vector_cache = {}
        self._avg_doc_length = 0.0
        self._idf_map = {}

    def start_background_prepare(self):
        if not self.enabled:
            return
        if self.app.debug and os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            return
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._thread = threading.Thread(
                target=self._prepare_runtime,
                name='systemlr-local-ai',
                daemon=True,
            )
            self._thread.start()

    def status(self):
        self._ensure_documents()
        if self._status.get('state') == 'idle':
            if self.auto_install:
                self._ensure_prepare_started()
            else:
                self._set_status(
                    ready=True,
                    state='ready',
                    mode='lexical',
                    message='Marcia esta em modo local basico. O modelo semantico automatico esta desabilitado.',
                    last_error=None,
                )
        payload = dict(self._status)
        payload['document_count'] = len(self._documents)
        return payload

    def answer(
        self,
        question,
        *,
        paginas_permitidas=None,
        pagina_atual=None,
        tela_atual=None,
        conversation_history=None,
        feedback_items=None,
    ):
        pergunta = (question or '').strip()
        if not pergunta:
            return {
                'answer': 'Envie uma pergunta para a Marcia orientar a navegacao e o proximo passo no sistema.',
                'actions': self._fallback_actions(paginas_permitidas or set(), pagina_atual),
                'sources': [],
                'status': self.status(),
                'response_id': uuid.uuid4().hex,
                'matched_doc_ids': [],
            }

        self._ensure_documents()
        self._ensure_prepare_started()
        paginas_permitidas = set(paginas_permitidas or [])

        saudacao = self._match_greeting_reply(pergunta)
        if saudacao:
            return {
                'response_id': uuid.uuid4().hex,
                'answer': saudacao,
                'actions': [],
                'sources': [],
                'status': self.status(),
                'matched_doc_ids': [],
            }

        documentos = [
            item
            for item in self._documents
            if self._documento_visivel(item, paginas_permitidas)
        ]
        if not documentos:
            return {
                'answer': 'Nao encontrei conteudo liberado para o seu perfil. Abra a Ajuda ou revise as permissoes do usuario.',
                'actions': [],
                'sources': [],
                'status': self.status(),
                'response_id': uuid.uuid4().hex,
                'matched_doc_ids': [],
            }

        question_context = self._build_question_context(pergunta, conversation_history)
        ranking = self._rank_documents(
            question_context['query_text'],
            documentos,
            pagina_atual=pagina_atual,
            feedback_items=feedback_items,
        )
        melhores = [item for item in ranking[:3] if item['score'] > 0]
        if not melhores:
            melhores = ranking[:2]

        resposta = self._compose_answer(
            pergunta,
            melhores,
            pagina_atual=pagina_atual,
            tela_atual=tela_atual,
        )
        acoes = self._build_actions(
            melhores,
            paginas_permitidas=paginas_permitidas,
            pagina_atual=pagina_atual,
        )

        fontes = []
        for item in melhores:
            doc = item['doc']
            fontes.append({
                'title': doc.get('title'),
                'url': doc.get('url'),
                'kind': doc.get('kind'),
                'section': doc.get('section'),
            })

        return {
            'response_id': uuid.uuid4().hex,
            'answer': resposta,
            'actions': acoes,
            'sources': fontes,
            'status': self.status(),
            'matched_doc_ids': [
                item['doc'].get('id')
                for item in melhores
                if item.get('doc') and item['doc'].get('id')
            ],
        }

    def _ensure_prepare_started(self):
        if not self.enabled:
            return
        if self._status.get('state') == 'idle':
            self.start_background_prepare()

    def _prepare_runtime(self):
        self._set_status(
            ready=False,
            state='preparing',
            mode='lexical',
            message='Preparando a Marcia para uso offline.',
            last_error=None,
        )
        try:
            self._ensure_documents(force=True)
            if not self.auto_install:
                self._set_status(
                    ready=True,
                    state='ready',
                    mode='lexical',
                    message='Marcia esta em modo local basico. O modelo semantico automatico esta desabilitado.',
                    last_error=None,
                )
                return

            if self._try_prepare_semantic_model():
                self._set_status(
                    ready=True,
                    state='ready',
                    mode='semantic',
                    message='Marcia esta pronta para uso offline.',
                    last_error=None,
                )
                return

            self._set_status(
                ready=True,
                state='ready',
                mode='lexical',
                message='Marcia esta em modo local basico enquanto o modelo semantico nao fica disponivel.',
                last_error=self._status.get('last_error'),
            )
        except Exception as exc:
            self.app.logger.exception('Falha ao preparar a IA local.')
            self._set_status(
                ready=True,
                state='ready',
                mode='lexical',
                message='Marcia esta em modo local basico por falha na preparacao offline.',
                last_error=str(exc),
            )

    def _try_prepare_semantic_model(self):
        modules = self._ensure_runtime_dependencies()
        if not modules:
            return False

        SentenceTransformer = modules['sentence_transformer']
        self.instance_dir.mkdir(parents=True, exist_ok=True)

        encoder = None
        errors = []
        try:
            if self.model_dir.exists():
                encoder = SentenceTransformer(str(self.model_dir), device='cpu')
        except Exception as exc:
            errors.append(str(exc))
            encoder = None

        if encoder is None:
            for candidate in self.model_candidates:
                try:
                    encoder = SentenceTransformer(candidate, device='cpu')
                    self.model_id = candidate
                    try:
                        encoder.save(str(self.model_dir))
                    except Exception:
                        pass
                    break
                except Exception as exc:
                    errors.append(f'{candidate}: {exc}')

        if encoder is None:
            self._status['last_error'] = '; '.join(errors[-3:]) if errors else 'modelo indisponivel'
            self.app.logger.warning('Nao foi possivel carregar o modelo semantico local: %s', self._status['last_error'])
            return False

        textos = [item['search_text'] for item in self._documents]
        try:
            vetores = encoder.encode(
                textos,
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=False,
            )
        except Exception as exc:
            self._status['last_error'] = str(exc)
            self.app.logger.warning('Nao foi possivel vetorizar a base do assistente: %s', exc)
            return False

        self._encoder = encoder
        self._document_vectors = [self._vector_to_list(item) for item in vetores]
        self._query_vector_cache = {}
        self._status['model_id'] = self.model_id
        return True

    def _ensure_runtime_dependencies(self):
        try:
            sentence_transformers = importlib.import_module('sentence_transformers')
            return {'sentence_transformer': sentence_transformers.SentenceTransformer}
        except Exception:
            if not self.auto_install:
                return None

        try:
            subprocess.check_call(
                [
                    sys.executable,
                    '-m',
                    'pip',
                    'install',
                    '--disable-pip-version-check',
                    '--no-input',
                    *LOCAL_AI_PACKAGES,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as exc:
            self._status['last_error'] = str(exc)
            self.app.logger.warning('Falha ao instalar dependencias da IA local: %s', exc)
            return None

        try:
            sentence_transformers = importlib.import_module('sentence_transformers')
            return {'sentence_transformer': sentence_transformers.SentenceTransformer}
        except Exception as exc:
            self._status['last_error'] = str(exc)
            self.app.logger.warning('Dependencias instaladas, mas o import da IA local falhou: %s', exc)
            return None

    def _ensure_documents(self, force=False):
        if self._documents and not force:
            return
        with self.app.app_context():
            with self.app.test_request_context('/'):
                documentos = self.knowledge_builder() or []
        preparados = []
        for item in documentos:
            doc = dict(item)
            doc['search_text'] = self._build_search_text(doc)
            doc['normalized_search_text'] = self._normalize_text(doc['search_text'])
            doc['normalized_title'] = self._normalize_text(doc.get('title') or '')
            doc['tokens'] = self._tokenize(doc['search_text'])
            doc['token_list'] = list(re.findall(r'[a-z0-9]{2,}', doc['normalized_search_text']))
            frequencias = {}
            for token in doc['token_list']:
                frequencias[token] = frequencias.get(token, 0) + 1
            doc['token_freq'] = frequencias
            doc['doc_length'] = len(doc['token_list'])
            doc['title_tokens'] = self._tokenize(doc.get('title') or '')
            doc['keyword_tokens'] = self._tokenize(' '.join(doc.get('keywords') or ()))
            preparados.append(doc)
        self._documents = preparados
        total_docs = len(preparados) or 1
        total_len = sum(doc.get('doc_length', 0) for doc in preparados)
        self._avg_doc_length = (total_len / total_docs) if total_docs else 0.0
        document_frequency = {}
        for doc in preparados:
            for token in set(doc.get('token_list') or ()):
                document_frequency[token] = document_frequency.get(token, 0) + 1
        self._idf_map = {
            token: math.log(1 + ((total_docs - freq + 0.5) / (freq + 0.5)))
            for token, freq in document_frequency.items()
        }
        self._status['document_count'] = len(preparados)
        self._query_vector_cache = {}

    def _rank_documents(self, question, documents, *, pagina_atual=None, feedback_items=None):
        query_text = question.strip()
        query_tokens = self._tokenize(query_text)
        query_text_normalized = self._normalize_text(query_text)
        semantic_mode = self._status.get('mode') == 'semantic' and self._encoder and self._document_vectors
        query_vector = self._get_query_vector(query_text) if semantic_mode else None

        ranking = []
        for doc in documents:
            lexical = self._lexical_score(
                query_tokens,
                doc,
                query_text_normalized=query_text_normalized,
            )
            bm25 = self._bm25_score(query_tokens, doc)
            semantic = 0.0
            if query_vector is not None:
                try:
                    idx = self._documents.index(doc)
                    semantic = self._cosine(query_vector, self._document_vectors[idx])
                except Exception:
                    semantic = 0.0
            feedback_score = self._feedback_score(
                query_tokens,
                doc,
                feedback_items,
                pagina_atual=pagina_atual,
            )

            page_boost = self._page_context_boost(doc, query_text, pagina_atual=pagina_atual)
            score = (lexical * 0.46) + (bm25 * 0.24) + feedback_score + page_boost
            if semantic > 0:
                score = max(
                    score,
                    (semantic * 0.42) + (lexical * 0.24) + (bm25 * 0.16) + max(feedback_score, 0.0) + page_boost,
                )

            ranking.append({
                'doc': doc,
                'score': score,
                'lexical_score': lexical,
                'bm25_score': bm25,
                'semantic_score': semantic,
                'feedback_score': feedback_score,
                'page_score': page_boost,
            })

        ranking.sort(key=lambda item: item['score'], reverse=True)
        return ranking

    def _compose_answer(self, question, ranking, *, pagina_atual=None, tela_atual=None):
        if not ranking:
            return 'Nao encontrei uma rota segura para esta pergunta. Abra a Ajuda ou use a Home Operacional para continuar.'

        intent = self._detect_intent(question)
        return self._generate_answer(
            question,
            ranking,
            intent,
            pagina_atual=pagina_atual,
            tela_atual=tela_atual,
        )

    def _build_actions(self, ranking, *, paginas_permitidas=None, pagina_atual=None):
        paginas_permitidas = set(paginas_permitidas or [])
        actions = []
        vistos = set()

        for item in ranking:
            doc = item['doc']
            for action in doc.get('actions') or ():
                page_key = action.get('page')
                if page_key and paginas_permitidas and page_key not in paginas_permitidas:
                    continue
                if not action.get('url'):
                    continue
                key = (action.get('label'), action.get('url'))
                if key in vistos:
                    continue
                vistos.add(key)
                actions.append({
                    'label': action.get('label'),
                    'url': action.get('url'),
                    'reason': action.get('reason') or doc.get('title'),
                    'kind': action.get('kind') or 'navigate',
                })
                if len(actions) >= 4:
                    return actions

            if doc.get('kind') == 'topic' and doc.get('url'):
                key = ('Abrir guia', doc.get('url'))
                if key not in vistos:
                    vistos.add(key)
                    actions.append({
                        'label': 'Abrir guia',
                        'url': doc.get('url'),
                        'reason': f'Passo a passo de {doc.get("title")}',
                        'kind': 'guide',
                    })
                    if len(actions) >= 4:
                        return actions

        if not actions:
            return self._fallback_actions(paginas_permitidas, pagina_atual)
        return actions

    def _fallback_actions(self, paginas_permitidas, pagina_atual):
        acoes = []
        if pagina_atual:
            for doc in self._documents:
                if doc.get('kind') == 'page' and pagina_atual in set(doc.get('pages') or []):
                    for action in doc.get('actions') or ():
                        if action.get('url'):
                            acoes.append({
                                'label': action.get('label'),
                                'url': action.get('url'),
                                'reason': action.get('reason') or doc.get('title'),
                                'kind': action.get('kind') or 'navigate',
                            })
                    break
        if acoes:
            return acoes[:3]
        return []

    def _documento_visivel(self, doc, paginas_permitidas):
        paginas_doc = set(doc.get('pages') or [])
        if not paginas_doc:
            return True
        return bool(paginas_doc.intersection(paginas_permitidas))

    def _build_search_text(self, doc):
        partes = [
            doc.get('title') or '',
            doc.get('summary') or '',
            doc.get('snippet') or '',
            ' '.join(doc.get('keywords') or ()),
            ' '.join(doc.get('pages') or ()),
            doc.get('section') or '',
        ]
        for item in doc.get('faq_pairs') or ():
            partes.append(item.get('question') or '')
            partes.append(item.get('answer') or '')
        partes.extend(doc.get('steps') or ())
        partes.extend(doc.get('checklist') or ())
        partes.extend(doc.get('alerts') or ())
        for item in doc.get('problems') or ():
            partes.append(item.get('situation') or '')
            partes.append(item.get('action') or '')
        if doc.get('source_topic'):
            partes.append(doc.get('source_topic'))
        return ' '.join(item for item in partes if item).strip()

    def _lexical_score(self, query_tokens, doc, *, query_text_normalized=''):
        if not query_tokens:
            return 0.0
        doc_tokens = set(doc.get('tokens') or ())
        if not doc_tokens:
            return 0.0
        comuns = query_tokens.intersection(doc_tokens)
        score = self._overlap_ratio(query_tokens, doc_tokens)

        search_text = doc.get('normalized_search_text', '')
        if query_text_normalized and query_text_normalized in search_text:
            score += 0.24

        title_text = doc.get('normalized_title', '')
        if query_text_normalized and query_text_normalized in title_text:
            score += 0.22

        title_tokens = set(doc.get('title_tokens') or ())
        if comuns.intersection(title_tokens):
            score += 0.12

        keywords = set(doc.get('keyword_tokens') or ())
        if comuns.intersection(keywords):
            score += 0.14

        kind_bonus = {
            'issue': 0.12,
            'faq': 0.1,
            'topic': 0.05,
            'page': 0.02,
        }
        score += kind_bonus.get(doc.get('kind'), 0.0)
        return score

    def _feedback_score(self, query_tokens, doc, feedback_items, *, pagina_atual=None):
        if not query_tokens or not feedback_items:
            return 0.0

        doc_id = doc.get('id')
        if not doc_id:
            return 0.0

        ajuste = 0.0
        for item in feedback_items:
            doc_ids = item.get('doc_ids') or ()
            if doc_id not in doc_ids:
                continue

            feedback_tokens = item.get('_tokens')
            if feedback_tokens is None:
                feedback_tokens = self._tokenize(item.get('question') or item.get('reason') or '')
                item['_tokens'] = feedback_tokens

            similaridade = self._overlap_ratio(query_tokens, feedback_tokens)
            if pagina_atual and item.get('pagina_atual') == pagina_atual:
                similaridade += 0.08
            if similaridade <= 0:
                continue

            peso = min(0.24, 0.02 + (similaridade * 0.24))
            if item.get('vote') == 'like':
                ajuste += peso
            else:
                ajuste -= peso * 0.85

        return max(min(ajuste, 0.28), -0.22)

    def _question_targets_current_screen(self, question):
        texto = self._normalize_text(question)
        marcadores = ('nesta tela', 'nessa tela', 'aqui', 'pagina atual', 'onde estou')
        return any(item in texto for item in marcadores)

    def _tokenize(self, text):
        texto_normalizado = self._normalize_text(text)
        return set(re.findall(r'[a-z0-9]{2,}', texto_normalizado))

    def _normalize_text(self, text):
        texto = unicodedata.normalize('NFKD', str(text or ''))
        texto = texto.encode('ascii', 'ignore').decode('ascii')
        return texto.lower().strip()

    def _build_question_context(self, question, conversation_history):
        historico = []
        for item in conversation_history or ():
            if not isinstance(item, dict):
                continue
            role = (item.get('role') or '').strip().lower()
            texto = (item.get('text') or '').strip()
            if role not in {'user', 'assistant'} or not texto:
                continue
            historico.append({'role': role, 'text': texto})
        historico = historico[-self.max_history_messages:]

        perguntas_anteriores = [item['text'] for item in historico if item['role'] == 'user']
        if perguntas_anteriores and self._normalize_text(perguntas_anteriores[-1]) == self._normalize_text(question):
            perguntas_anteriores = perguntas_anteriores[:-1]

        precisa_contexto = self._question_needs_history(question)
        contexto = perguntas_anteriores[-3:] if precisa_contexto else []
        partes = contexto + [question]
        return {
            'query_text': ' '.join(item for item in partes if item).strip(),
            'used_history': bool(contexto),
            'history_messages': historico,
        }

    def _question_needs_history(self, question):
        texto = self._normalize_text(question)
        tokens = self._tokenize(texto)
        marcadores = (
            'e depois',
            'depois disso',
            'e agora',
            'como assim',
            'isso',
            'essa',
            'esse',
            'nela',
            'nele',
            'nessa',
            'nesse',
            'aqui',
        )
        return len(tokens) <= 4 or any(item in texto for item in marcadores)

    def _normalize_short_message(self, text):
        texto = self._normalize_text(text)
        texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
        return re.sub(r'\s+', ' ', texto).strip()

    def _match_greeting_reply(self, question):
        texto = self._normalize_short_message(question)
        if not texto:
            return ''

        respostas = {
            'bom dia': 'Bom dia! Em que posso ajudar?',
            'boa tarde': 'Boa tarde! Em que posso ajudar?',
            'boa noite': 'Boa noite! Como posso te ajudar?',
            'ola': 'Ola! Como posso te ajudar?',
            'oi': 'Oi! O que voce precisa?',
        }
        if texto in respostas:
            return respostas[texto]

        tokens = texto.split()
        if len(tokens) > 3:
            return ''
        if texto in {'oii', 'opa', 'e ai', 'iae'}:
            return 'Oi! Como posso te ajudar?'
        return ''

    def _detect_intent(self, question):
        texto = self._normalize_short_message(question)
        if re.search(r'\b(nao consigo|nao aparece|erro|falha|problema|travou|bloqueado|invalid|incorreto)\b', texto):
            return 'problem'
        if re.search(r'\b(e depois|depois disso|proximo passo|qual o proximo|e agora|como continuo)\b', texto):
            return 'follow_up'
        if re.search(r'\b(onde|onde fica|onde altero|onde configuro|localizar|em qual tela|fica em qual menu)\b', texto):
            return 'location'
        if re.search(r'\b(como|passo a passo|quais passos|o que fazer|registrar|configurar|criar|finalizar|lancar)\b', texto):
            return 'howto'
        if re.search(r'\b(posso|permissao|acesso|liberar|perfil)\b', texto):
            return 'permission'
        if re.search(r'\b(ajuda|explica|entender|duvida)\b', texto):
            return 'general_help'
        return 'general'

    def _generate_answer(self, question, ranking, intent, *, pagina_atual=None, tela_atual=None):
        principal = ranking[0]['doc']
        titulo = principal.get('title') or tela_atual or 'esta area'
        resposta_direta = self._resolve_direct_answer(question, ranking, intent)
        passos = self._select_steps(question, ranking, intent)
        alerta = self._select_alert(ranking, question)

        if pagina_atual and self._question_targets_current_screen(question) and tela_atual:
            abertura = f'Voce esta em {tela_atual}.'
        elif intent == 'location':
            abertura = f'Voce encontra isso em {titulo}.'
        elif intent == 'permission':
            abertura = f'Posso te orientar com base no que esta liberado para o seu perfil em {titulo}.'
        elif intent == 'problem':
            abertura = f'Vamos resolver isso em {titulo}.'
        elif intent in {'howto', 'follow_up'}:
            abertura = f'Para seguir com seguranca em {titulo}:'
        else:
            abertura = f'O melhor contexto para essa duvida agora e {titulo}.'

        linhas = [abertura]
        if resposta_direta:
            prefixo = {
                'problem': 'Tente o seguinte:',
                'location': 'Caminho sugerido:',
                'permission': 'Regra principal:',
            }.get(intent)
            if prefixo:
                linhas.append(f'{prefixo} {self._ensure_sentence(resposta_direta)}')
            else:
                linhas.append(self._ensure_sentence(resposta_direta))

        if passos:
            if intent in {'howto', 'follow_up'}:
                linhas.append('Passo a passo:')
            elif intent == 'problem':
                linhas.append('Checklist rapido:')
            else:
                linhas.append('Passos sugeridos:')
            for indice, passo in enumerate(passos, start=1):
                linhas.append(f'{indice}. {self._ensure_sentence(passo)}')

        if alerta:
            linhas.append(f'Atencao: {self._ensure_sentence(alerta)}')

        if len(linhas) == 1:
            linhas.append(self._ensure_sentence(principal.get('summary') or principal.get('snippet') or 'Veja as opcoes abaixo.'))

        return '\n'.join(item for item in linhas if item).strip()

    def _resolve_direct_answer(self, question, ranking, intent):
        principal = ranking[0]['doc']
        if principal.get('kind') in {'faq', 'issue'} and principal.get('summary'):
            return principal.get('summary')

        if intent == 'location':
            secao = principal.get('section')
            if secao and principal.get('title'):
                return f'Voce encontra isso em {secao} > {principal.get("title")}.'

        melhor_faq = self._best_faq_match(question, ranking)
        if melhor_faq:
            return melhor_faq.get('answer')

        if intent == 'problem':
            melhor_problema = self._best_problem_match(question, ranking)
            if melhor_problema:
                return melhor_problema.get('action')

        return principal.get('summary') or principal.get('snippet') or 'Use a opcao indicada para continuar com seguranca.'

    def _best_faq_match(self, question, ranking):
        query_tokens = self._tokenize(question)
        melhor = None
        melhor_score = 0.0
        for item in ranking[:3]:
            doc = item['doc']
            for faq in doc.get('faq_pairs') or ():
                score = self._text_match_score(query_tokens, faq.get('question'))
                if score > melhor_score:
                    melhor = faq
                    melhor_score = score
        return melhor if melhor_score >= 0.18 else None

    def _best_problem_match(self, question, ranking):
        query_tokens = self._tokenize(question)
        melhor = None
        melhor_score = 0.0
        for item in ranking[:3]:
            doc = item['doc']
            for problema in doc.get('problems') or ():
                score = self._text_match_score(query_tokens, problema.get('situation'))
                if score > melhor_score:
                    melhor = problema
                    melhor_score = score
        return melhor if melhor_score >= 0.18 else None

    def _select_steps(self, question, ranking, intent):
        query_tokens = self._tokenize(question)
        candidatos = []
        for doc_pos, item in enumerate(ranking[:3]):
            doc = item['doc']
            for step_pos, passo in enumerate(doc.get('steps') or ()):
                score = self._text_match_score(query_tokens, passo)
                if intent == 'follow_up' and step_pos > 0:
                    score += 0.08
                if doc.get('kind') in {'faq', 'issue'}:
                    score += 0.05
                score += max(0.0, 0.08 - (doc_pos * 0.02) - (step_pos * 0.01))
                candidatos.append((score, passo))

        if not candidatos:
            return []

        vistos = set()
        passos = []
        limite = 2 if intent in {'location', 'permission'} else 4
        for _, passo in sorted(candidatos, key=lambda item: item[0], reverse=True):
            chave = self._normalize_text(passo)
            if not chave or chave in vistos:
                continue
            vistos.add(chave)
            passos.append(passo)
            if len(passos) >= limite:
                break
        return passos

    def _select_alert(self, ranking, question):
        query_tokens = self._tokenize(question)
        melhor_alerta = ''
        melhor_score = 0.0
        for item in ranking[:2]:
            doc = item['doc']
            for alerta in doc.get('alerts') or ():
                score = self._text_match_score(query_tokens, alerta)
                if score > melhor_score:
                    melhor_score = score
                    melhor_alerta = alerta
        return melhor_alerta if melhor_score >= 0.14 else ''

    def _text_match_score(self, query_tokens, text):
        candidate_tokens = self._tokenize(text)
        if not candidate_tokens:
            return 0.0
        score = self._overlap_ratio(query_tokens, candidate_tokens)
        query_text = ' '.join(sorted(query_tokens))
        candidate_text = self._normalize_text(text)
        if query_text and query_text in candidate_text:
            score += 0.12
        return score

    def _page_context_boost(self, doc, question, *, pagina_atual=None):
        if not pagina_atual:
            return 0.0
        paginas = set(doc.get('pages') or ())
        if pagina_atual not in paginas:
            return 0.0
        return 0.32 if self._question_targets_current_screen(question) else 0.08

    def _bm25_score(self, query_tokens, doc, *, k1=1.5, b=0.75):
        if not query_tokens:
            return 0.0
        token_freq = doc.get('token_freq') or {}
        doc_length = float(doc.get('doc_length') or 0.0)
        avg_doc_length = self._avg_doc_length or 1.0
        total = 0.0
        for token in query_tokens:
            freq = float(token_freq.get(token) or 0.0)
            if freq <= 0:
                continue
            idf = self._idf_map.get(token, 0.0)
            denominador = freq + k1 * (1 - b + b * (doc_length / avg_doc_length))
            if denominador <= 0:
                continue
            total += idf * ((freq * (k1 + 1)) / denominador)
        return min(total, 1.4)

    def _get_query_vector(self, query_text):
        chave = self._normalize_text(query_text)
        if not chave or not self._encoder:
            return None
        if chave in self._query_vector_cache:
            return self._query_vector_cache[chave]
        try:
            vector = self._vector_to_list(
                self._encoder.encode(
                    [query_text],
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )[0]
            )
        except Exception:
            return None
        self._query_vector_cache[chave] = vector
        if len(self._query_vector_cache) > 96:
            self._query_vector_cache.pop(next(iter(self._query_vector_cache)))
        return vector

    def _overlap_ratio(self, left_tokens, right_tokens):
        left = set(left_tokens or ())
        right = set(right_tokens or ())
        if not left or not right:
            return 0.0
        comuns = left.intersection(right)
        return len(comuns) / max(len(left), 1)

    def _ensure_sentence(self, text):
        texto = (text or '').strip()
        if not texto:
            return ''
        return texto if texto.endswith(('.', '!', '?')) else f'{texto}.'

    def _vector_to_list(self, vector):
        if hasattr(vector, 'tolist'):
            return vector.tolist()
        return list(vector)

    def _cosine(self, left, right):
        if not left or not right:
            return 0.0
        numerador = sum(float(a) * float(b) for a, b in zip(left, right))
        norma_left = math.sqrt(sum(float(a) * float(a) for a in left))
        norma_right = math.sqrt(sum(float(b) * float(b) for b in right))
        if not norma_left or not norma_right:
            return 0.0
        return numerador / (norma_left * norma_right)

    def _set_status(self, **kwargs):
        self._status.update(kwargs)
