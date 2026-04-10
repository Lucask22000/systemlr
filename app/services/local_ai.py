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
LOCAL_SEMANTIC_VECTOR_SIZE = 384

TOPIC_PROFILES = {
    'estoque': {
        'overview': 'Estoque normalmente envolve cadastro de produtos, entradas e saidas, saldo disponivel, estoque minimo e relatorios de acompanhamento.',
        'starter_steps': [
            'Cadastre categorias, produtos e dados basicos do item.',
            'Registre recebimentos, transferencias e demais movimentacoes de entrada e saida.',
            'Acompanhe saldo, estoque minimo, enderecamento e inconsistencias.',
            'Use relatorios para conferir giro, ruptura e necessidade de reposicao.',
        ],
        'refinements': ['cadastro de produtos', 'recebimentos', 'movimentacoes', 'enderecamento', 'relatorios'],
        'aliases': ('estoque', 'produto', 'produtos', 'recebimento', 'recebimentos', 'movimentacao', 'movimentacoes', 'enderecamento'),
    },
    'pedidos': {
        'overview': 'Pedidos cobrem abertura, inclusao de itens, conferencia de totais, transicoes de status e fechamento com caixa ou entrega.',
        'starter_steps': [
            'Abra ou localize o pedido correto.',
            'Inclua itens, quantidades e observacoes necessarias.',
            'Confira status, totais, pagamento e liberacoes operacionais.',
            'Finalize o pedido e acompanhe a proxima etapa da operacao.',
        ],
        'refinements': ['criacao', 'itens', 'status', 'pagamento', 'finalizacao'],
        'aliases': ('pedido', 'pedidos', 'venda', 'vendas', 'roteirizacao', 'entrega'),
    },
    'caixa': {
        'overview': 'Caixa envolve abertura, recebimentos, sangrias, conferencias e fechamento do turno com rastreabilidade financeira.',
        'starter_steps': [
            'Abra o caixa do turno com o valor inicial correto.',
            'Registre entradas, saidas e recebimentos vinculados as vendas.',
            'Acompanhe divergencias, sangrias e saldo parcial durante o expediente.',
            'Feche o caixa com conferencia final e justificativa quando necessario.',
        ],
        'refinements': ['abertura', 'movimentacoes', 'recebimentos', 'sangria', 'fechamento'],
        'aliases': ('caixa', 'caixas', 'sangria', 'fechamento de caixa', 'abertura de caixa'),
    },
    'financeiro': {
        'overview': 'Financeiro concentra lancamentos, competencias, contas a pagar e receber, conciliacao e indicadores do negocio.',
        'starter_steps': [
            'Cadastre ou importe os lancamentos com data e tipo corretos.',
            'Classifique receitas, despesas e formas de pagamento.',
            'Acompanhe vencimentos, competencias e status de quitacao.',
            'Use os indicadores para analisar fluxo de caixa e resultado.',
        ],
        'refinements': ['lancamentos', 'competencia', 'contas', 'conciliacao', 'indicadores'],
        'aliases': ('financeiro', 'lancamento', 'lancamentos', 'contas', 'receitas', 'despesas'),
    },
    'rh': {
        'overview': 'RH reune cadastro de funcionarios, perfis de acesso, funcoes, organograma e indicadores de equipe.',
        'starter_steps': [
            'Cadastre o funcionario com dados pessoais e matricula.',
            'Defina funcao, perfil de acesso e vinculos necessarios.',
            'Revise permissoes, lotacao e estrutura organizacional.',
            'Acompanhe indicadores e historico administrativo da equipe.',
        ],
        'refinements': ['funcionarios', 'permissoes', 'funcoes', 'organograma', 'indicadores'],
        'aliases': ('rh', 'recursos humanos', 'funcionario', 'funcionarios', 'acessos', 'permissoes', 'organograma'),
    },
    'expedicao': {
        'overview': 'Expedicao cobre separacao, roteirizacao, conferencias de saida, frota e acompanhamento da entrega.',
        'starter_steps': [
            'Organize os pedidos liberados para expedicao.',
            'Monte a carga ou rota conforme prioridade operacional.',
            'Confirme itens, volumes e responsaveis pela entrega.',
            'Acompanhe a saida e o retorno da operacao.',
        ],
        'refinements': ['roteirizacao', 'separacao', 'conferencia', 'frota', 'entrega'],
        'aliases': ('expedicao', 'frota', 'rota', 'roteirizacao', 'entrega'),
    },
    'ecommerce': {
        'overview': 'E-commerce envolve vitrine, configuracoes da loja, pedidos online, checkout e acompanhamento do fluxo digital.',
        'starter_steps': [
            'Revise configuracoes da loja e publicacao de produtos.',
            'Garanta preco, estoque e disponibilidade corretos no canal online.',
            'Acompanhe pedidos, checkout e confirmacoes de pagamento.',
            'Monitore a experiencia do cliente e integracoes do canal.',
        ],
        'refinements': ['configuracao', 'produtos', 'checkout', 'pedidos online', 'integracoes'],
        'aliases': ('ecommerce', 'e-commerce', 'loja online', 'checkout', 'site'),
    },
}

# Intent labels
INTENT_LABELS = {
    'greeting',
    'broad_exploration',
    'operational_how_to',
    'incident_problem',
    'navigation_request',
    'access_permission',
    'fallback_unknown',
}

# Score thresholds
MIN_GUIDE_SCORE = 0.24
MIN_COHERENCE_SCORE = 0.12

# Domain/action keyword hints (normalized ascii, lower)
DOMAIN_KEYWORDS = {
    'recebimento': {'receber', 'recebimento', 'fornecedor', 'entrada', 'mercadoria', 'nota', 'nf', 'doca', 'armazenar'},
    'estoque': {'estoque', 'produto', 'produtos', 'saldo', 'picking', 'enderecamento', 'ruptura'},
    'pedidos': {'pedido', 'pedidos', 'venda', 'pdv', 'caixa', 'mesa', 'garcom'},
    'expedicao': {'expedicao', 'roteirizacao', 'entrega', 'entregas', 'separacao', 'roteiro', 'etiqueta'},
    'financeiro': {'financeiro', 'lancamento', 'lancamentos', 'contas', 'competencia', 'fundo'},
    'rh': {'rh', 'acesso', 'permissao', 'perfil', 'cargo', 'organograma'},
    'ecommerce': {'ecommerce', 'loja', 'vitrine', 'banner', 'campanha'},
    'servicos': {'chamado', 'ordem', 'servico', 'os', 'tecnico', 'manutencao'},
}

ACTION_KEYWORDS = {
    'operational_how_to': {'receber', 'conferir', 'lancar', 'registrar', 'abrir', 'fechar', 'finalizar', 'transferir'},
    'incident_problem': {'nao consigo', 'erro', 'falha', 'travou', 'sumiu', 'negativo', 'nao aparece', 'bloqueado'},
    'navigation_request': {'onde', 'menu', 'fica', 'como abrir', 'qual tela', 'em qual menu'},
    'access_permission': {'sem acesso', 'sem permissao', 'bloqueado', 'nao tenho acesso', 'perfil'},
}


class LightweightSemanticEncoder:
    def __init__(self, dimension=LOCAL_SEMANTIC_VECTOR_SIZE):
        self.dimension = max(int(dimension or LOCAL_SEMANTIC_VECTOR_SIZE), 128)

    def encode(self, texts, normalize_embeddings=True, convert_to_numpy=False, show_progress_bar=False):
        vectors = [self._encode_text(text, normalize_embeddings=normalize_embeddings) for text in (texts or [])]
        return vectors

    def _encode_text(self, text, *, normalize_embeddings=True):
        normalized = unicodedata.normalize('NFKD', str(text or ''))
        normalized = normalized.encode('ascii', 'ignore').decode('ascii').lower()
        tokens = re.findall(r'[a-z0-9]{2,}', normalized)
        vector = [0.0] * self.dimension
        features = list(tokens)
        compact = normalized.replace(' ', '')
        for size in (3, 4):
            if len(compact) < size:
                continue
            for index in range(len(compact) - size + 1):
                features.append(compact[index:index + size])
        for index in range(len(tokens) - 1):
            features.append(f'{tokens[index]}_{tokens[index + 1]}')
        for feature in features:
            bucket = hash(feature) % self.dimension
            sign = -1.0 if (hash(f'sign:{feature}') % 2) else 1.0
            weight = 1.3 if '_' in feature else 1.0
            vector[bucket] += sign * weight
        if normalize_embeddings:
            norm = math.sqrt(sum(value * value for value in vector))
            if norm:
                vector = [value / norm for value in vector]
        return vector


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
        self._dependency_install_attempted = False

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
            self._ensure_prepare_started()
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
        intent = self._detect_intent(pergunta)
        entities, actions = self._extract_entities_actions(pergunta)
        domain = self._infer_domain(entities, actions, pagina_atual)

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
            intent=intent,
            pagina_atual=pagina_atual,
            feedback_items=feedback_items,
            domain=domain,
            actions=actions,
        )
        melhores = [item for item in ranking[:3] if item['score'] > 0]
        if not melhores:
            melhores = ranking[:2]

        clarification = self._build_clarifying_answer(pergunta, ranking, intent)
        resposta = clarification or ''

        selected_doc = melhores[0]['doc'] if melhores else None

        if not resposta:
            resposta = self._generate_structured_response(
                intent=intent,
                question=pergunta,
                domain=domain,
                actions=actions,
                doc=selected_doc,
                pagina_atual=pagina_atual,
                tela_atual=tela_atual,
            )

        guia_score = melhores[0]['score'] if melhores else 0.0
        coherence_score = self._validate_coherence(
            user_message=pergunta,
            domain=domain,
            actions=actions,
            doc=selected_doc,
            draft=resposta,
        )

        if guia_score < MIN_GUIDE_SCORE or coherence_score < MIN_COHERENCE_SCORE:
            if len(melhores) > 1:
                selected_doc = melhores[1]['doc']
                resposta = self._generate_structured_response(
                    intent=intent,
                    question=pergunta,
                    domain=domain,
                    actions=actions,
                    doc=selected_doc,
                    pagina_atual=pagina_atual,
                    tela_atual=tela_atual,
                )
                coherence_score = self._validate_coherence(
                    user_message=pergunta,
                    domain=domain,
                    actions=actions,
                    doc=selected_doc,
                    draft=resposta,
                )

        if coherence_score < MIN_COHERENCE_SCORE:
            resposta = self._fallback_refinement(intent, domain, actions)

        acoes = []
        if selected_doc and intent not in {'broad_exploration', 'general_help'}:
            acoes = self._build_actions(
                [{'doc': selected_doc, 'score': guia_score}],
                paginas_permitidas=paginas_permitidas,
                pagina_atual=pagina_atual,
            )

        fontes = []
        if selected_doc:
            fontes.append({
                'title': selected_doc.get('title'),
                'url': selected_doc.get('url'),
                'kind': selected_doc.get('kind'),
                'section': selected_doc.get('section'),
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
            if self._try_prepare_semantic_model():
                self._set_status(
                    ready=True,
                    state='ready',
                    mode='semantic',
                    message='Marcia esta pronta para uso offline com busca semantica local.',
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
        encoder = None
        errors = []

        if modules:
            SentenceTransformer = modules['sentence_transformer']
            self.instance_dir.mkdir(parents=True, exist_ok=True)
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
            encoder = LightweightSemanticEncoder()
            self.model_id = 'local-lightweight-semantic-v1'
            if errors:
                self._status['last_error'] = '; '.join(errors[-3:])
                self.app.logger.warning(
                    'Usando encoder semantico local leve apos falha no sentence-transformers: %s',
                    self._status['last_error'],
                )
            else:
                self._status['last_error'] = None

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

        if sys.version_info >= (3, 13):
            self._status['last_error'] = (
                f'Python {sys.version_info.major}.{sys.version_info.minor} usando encoder semantico local leve.'
            )
            return None

        if self._dependency_install_attempted:
            return None
        self._dependency_install_attempted = True

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
            doc['domain'] = self._infer_doc_domain(doc)
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

    def _rank_documents(self, question, documents, *, intent='general', pagina_atual=None, feedback_items=None, domain=None, actions=None):
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
            intent_score = self._intent_document_boost(intent, doc)
            topic_score = self._topic_alignment_boost(query_text, doc)
            domain_score = self._domain_alignment_score(domain, doc)
            action_score = self._action_alignment_score(actions, doc)
            score = (lexical * 0.36) + (bm25 * 0.18) + feedback_score + page_boost + intent_score + topic_score + domain_score + action_score
            if semantic > 0:
                score = max(
                    score,
                    (semantic * 0.38) + (lexical * 0.22) + (bm25 * 0.14) + max(feedback_score, 0.0) + page_boost + max(intent_score, 0.0) + topic_score + domain_score + action_score,
                )

            ranking.append({
                'doc': doc,
                'score': score,
                'lexical_score': lexical,
                'bm25_score': bm25,
                'semantic_score': semantic,
                'feedback_score': feedback_score,
                'page_score': page_boost,
                'intent_score': intent_score,
                'topic_score': topic_score,
                'domain_score': domain_score,
                'action_score': action_score,
            })

        ranking.sort(key=lambda item: item['score'], reverse=True)
        return ranking

    def _compose_answer(self, question, ranking, *, intent=None, pagina_atual=None, tela_atual=None):
        if not ranking:
            return 'Nao encontrei uma rota segura para esta pergunta. Abra a Ajuda ou use a Home Operacional para continuar.'

        if intent is None:
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
        respostas_anteriores = [item['text'] for item in historico if item['role'] == 'assistant']
        if perguntas_anteriores and self._normalize_text(perguntas_anteriores[-1]) == self._normalize_text(question):
            perguntas_anteriores = perguntas_anteriores[:-1]

        precisa_contexto = self._question_needs_history(question)
        contexto = []
        if precisa_contexto:
            if respostas_anteriores:
                contexto.append(respostas_anteriores[-1])
            contexto.extend(perguntas_anteriores[-2:])
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
        if not texto:
            return 'fallback_unknown'
        if self._is_broad_teaching_request(texto):
            return 'broad_exploration'
        if any(term in texto for term in ('ola', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'opa', 'iae', 'e ai')):
            return 'greeting'
        if re.search(r'\b(nao consigo|nao aparece|erro|falha|problema|travou|bloqueado|invalid|incorreto|negativo)\b', texto):
            return 'incident_problem'
        if re.search(r'\b(onde|onde fica|onde altero|onde configuro|localizar|em qual tela|fica em qual menu|onde encontro)\b', texto):
            return 'navigation_request'
        if re.search(r'\b(posso|permissao|acesso|liberar|perfil|sem acesso|sem permissao|menu bloqueado)\b', texto):
            return 'access_permission'
        if re.search(r'\b(como|passo a passo|quais passos|o que fazer|registrar|configurar|criar|finalizar|lancar|receber|conferir|abrir|fechar)\b', texto):
            return 'operational_how_to'
        if re.search(r'\b(ajuda|explica|entender|duvida)\b', texto):
            return 'broad_exploration'
        return 'fallback_unknown'

    def _is_broad_teaching_request(self, texto):
        if not texto:
            return False
        topic_terms = tuple(TOPIC_PROFILES.keys()) + ('funcionarios', 'vendas', 'recebimentos', 'movimentacoes', 'ajuda')
        teaching_terms = (
            'quero saber sobre',
            'me explica',
            'me explique',
            'explica sobre',
            'falar sobre',
            'entender',
            'entender melhor',
            'como funciona',
            'quero aprender',
            'duvida sobre',
            'sobre ',
        )
        tokens = texto.split()
        if len(tokens) <= 5 and any(term == texto for term in topic_terms):
            return True
        return any(term in texto for term in teaching_terms) and any(topic in texto for topic in topic_terms)

    def _extract_question_topics(self, text):
        texto = self._normalize_short_message(text)
        temas = []
        for topic, profile in TOPIC_PROFILES.items():
            for alias in profile.get('aliases') or (topic,):
                if alias and alias in texto:
                    temas.append(topic)
                    break
        return temas

    def _detect_primary_topic(self, text, doc=None):
        temas = self._extract_question_topics(text)
        if temas:
            return temas[0]
        if not doc:
            return None
        base = ' '.join(
            item
            for item in (
                doc.get('section'),
                doc.get('title'),
                doc.get('source_topic'),
                ' '.join(doc.get('pages') or ()),
                ' '.join(doc.get('keywords') or ()),
            )
            if item
        )
        temas_doc = self._extract_question_topics(base)
        return temas_doc[0] if temas_doc else None

    def _intent_document_boost(self, intent, doc):
        intent = {
            'broad_exploration': 'broad_teaching',
            'operational_how_to': 'howto',
            'incident_problem': 'problem',
            'navigation_request': 'location',
            'access_permission': 'permission',
            'fallback_unknown': 'general',
            'greeting': 'general',
        }.get(intent, intent)
        kind = doc.get('kind')
        boost_map = {
            'broad_teaching': {'topic': 0.24, 'page': 0.12, 'faq': 0.04, 'issue': -0.18},
            'general_help': {'topic': 0.18, 'page': 0.1, 'faq': 0.05, 'issue': -0.12},
            'general': {'topic': 0.1, 'page': 0.06, 'faq': 0.03, 'issue': -0.08},
            'howto': {'topic': 0.14, 'faq': 0.1, 'page': 0.05, 'issue': -0.04},
            'follow_up': {'topic': 0.08, 'faq': 0.08, 'page': 0.04, 'issue': 0.02},
            'location': {'page': 0.18, 'topic': 0.08, 'faq': 0.03, 'issue': -0.08},
            'permission': {'faq': 0.12, 'page': 0.08, 'topic': 0.06, 'issue': -0.05},
            'problem': {'issue': 0.2, 'faq': 0.08, 'topic': 0.03, 'page': 0.0},
        }
        boost = boost_map.get(intent, boost_map['general']).get(kind, 0.0)
        if intent in {'broad_teaching', 'general_help', 'general'} and doc.get('steps'):
            boost += 0.05
        if intent in {'howto', 'follow_up'} and doc.get('steps'):
            boost += 0.07
        if intent == 'problem' and doc.get('problems'):
            boost += 0.06
        if intent == 'location' and doc.get('url'):
            boost += 0.04
        return boost

    def _topic_alignment_boost(self, question, doc):
        temas = self._extract_question_topics(question)
        if not temas:
            return 0.0
        texto_doc = self._normalize_text(' '.join(
            item
            for item in (
                doc.get('section'),
                doc.get('title'),
                doc.get('source_topic'),
                ' '.join(doc.get('pages') or ()),
                ' '.join(doc.get('keywords') or ()),
                doc.get('summary'),
            )
            if item
        ))
        for topic in temas:
            profile = TOPIC_PROFILES.get(topic) or {}
            aliases = profile.get('aliases') or (topic,)
            if any(alias and alias in texto_doc for alias in aliases):
                return 0.16
        return 0.0

    def _extract_entities_actions(self, question):
        texto = self._normalize_text(question)
        tokens = self._tokenize(texto)
        entities = set()
        actions = set()
        for domain, kws in DOMAIN_KEYWORDS.items():
            if tokens.intersection(kws):
                entities.add(domain)
        for intent_key, kws in ACTION_KEYWORDS.items():
            if any(k in texto for k in kws):
                actions.add(intent_key)
        return entities, actions

    def _infer_domain(self, entities, actions, pagina_atual):
        candidatos = {}
        tokens_pagina = self._tokenize(pagina_atual or '')
        for domain, kws in DOMAIN_KEYWORDS.items():
            score = 0
            if domain in entities:
                score += 2
            if tokens_pagina.intersection(kws):
                score += 1.5
            if actions and 'operational_how_to' in actions and domain in {'recebimento', 'estoque', 'pedidos', 'expedicao', 'financeiro'}:
                score += 0.5
            candidatos[domain] = score
        if not candidatos:
            return None
        melhor = max(candidatos.items(), key=lambda item: item[1])
        return melhor[0] if melhor[1] > 0 else None

    def _infer_doc_domain(self, doc):
        base = ' '.join(
            item for item in [
                doc.get('title') or '',
                doc.get('summary') or '',
                doc.get('section') or '',
                ' '.join(doc.get('pages') or ()),
                ' '.join(doc.get('keywords') or ()),
            ] if item
        )
        texto = self._normalize_text(base)
        tokens = self._tokenize(texto)
        best = (None, 0.0)
        for domain, kws in DOMAIN_KEYWORDS.items():
            overlap = len(tokens.intersection(kws))
            if overlap > best[1]:
                best = (domain, overlap)
        return best[0]

    def _domain_alignment_score(self, domain, doc):
        if not doc:
            return 0.0
        doc_domain = doc.get('domain') or self._infer_doc_domain(doc)
        if not domain or not doc_domain:
            return 0.0
        if domain == doc_domain:
            return 0.18
        return -0.12

    def _action_alignment_score(self, actions, doc):
        if not actions or not doc:
            return 0.0
        text = self._normalize_text(' '.join([
            doc.get('title') or '',
            doc.get('summary') or '',
            ' '.join(doc.get('keywords') or ()),
        ]))
        score = 0.0
        if 'operational_how_to' in actions and re.search(r'\b(receber|conferir|lancar|registrar|abrir|fechar|finalizar|transferir)\b', text):
            score += 0.08
        if 'incident_problem' in actions and re.search(r'\b(erro|falha|problema|negativo|travou)\b', text):
            score += 0.06
        return score

    def _validate_coherence(self, user_message, domain, actions, doc, draft):
        texto = self._normalize_text(draft or '')
        if not doc:
            return 0.0
        doc_domain = doc.get('domain') or self._infer_doc_domain(doc)
        if not doc_domain:
            return 0.0
        expected = {
            'recebimento': {'receber', 'fornecedor', 'entrada', 'mercadoria', 'conferencia', 'estoque', 'nota'},
            'estoque': {'estoque', 'produto', 'saldo', 'picking', 'enderecamento'},
            'pedidos': {'pedido', 'venda', 'pdv', 'caixa', 'mesa'},
            'expedicao': {'expedicao', 'entrega', 'separacao', 'roteirizacao', 'etiqueta'},
            'financeiro': {'financeiro', 'lancamento', 'competencia', 'fundo'},
            'rh': {'acesso', 'permissao', 'perfil', 'cargo', 'organograma', 'rh'},
        }
        unexpected = {
            'recebimento': {'pdv', 'caixa', 'rh', 'perfil', 'permissao', 'chamado', 'garcom'},
            'estoque': {'pdv', 'caixa', 'rh', 'chamado'},
        }
        exp_terms = expected.get(doc_domain, set())
        unexp_terms = unexpected.get(doc_domain, set())
        tokens = self._tokenize(texto)
        score = 0.0
        if exp_terms and tokens.intersection(exp_terms):
            score += min(0.2, len(tokens.intersection(exp_terms)) * 0.05)
        if unexp_terms and tokens.intersection(unexp_terms):
            score -= min(0.2, len(tokens.intersection(unexp_terms)) * 0.08)
        # penalize if no expected terms
        if exp_terms and not tokens.intersection(exp_terms):
            score -= 0.1
        return score

    def _fallback_refinement(self, intent, domain, actions):
        if intent == 'greeting':
            return 'Ola! Como posso ajudar?'
        opcoes = []
        if domain in {'recebimento', 'estoque'}:
            opcoes = [
                'cadastrar fornecedor',
                'receber mercadoria',
                'conferir itens recebidos',
                'lancar entrada no sistema',
            ]
        elif intent == 'access_permission':
            return 'Quero responder certo. Voce esta sem acesso a qual menu? Financeiro, Estoque, Vendas ou outro?'
        elif intent == 'navigation_request':
            return 'Posso te mostrar o caminho. Qual tela voce quer abrir agora?'
        if opcoes:
            return (
                'Quero te responder certo. Voce quer saber como: '
                + '; '.join(opcoes[:4])
                + '?'
            )
        return 'Posso ajudar melhor se voce der um pouco mais de contexto ou o modulo que quer usar.'

    def _generate_structured_response(self, intent, question, domain, actions, doc, pagina_atual=None, tela_atual=None):
        titulo = (doc or {}).get('title') or tela_atual or 'esta area'
        passos = (doc or {}).get('steps') or []
        checklist = (doc or {}).get('checklist') or []
        alertas = (doc or {}).get('alerts') or []
        problemas = (doc or {}).get('problems') or []

        def format_passos(lista, limite=5):
            return [self._ensure_sentence(item) for item in lista[:limite]]

        if intent == 'greeting':
            return 'Ola! Como posso ajudar?'

        if intent == 'broad_exploration':
            resumo = (doc or {}).get('summary') or (doc or {}).get('snippet') or 'Posso detalhar as partes principais.'
            topicos = []
            if doc and doc.get('checklist'):
                topicos.append('pre-requisitos')
            if passos:
                topicos.append('passo a passo')
            if alertas:
                topicos.append('alertas operacionais')
            extras = f" Posso detalhar {', '.join(topicos)}." if topicos else ''
            return f'Claro! Posso te explicar {titulo.lower()} passo a passo. {resumo} Qual parte voce quer entender primeiro?{extras}'

        if intent == 'operational_how_to':
            corpo = []
            corpo.append(f'Posso te ajudar com {titulo.lower()}.')
            if domain == 'recebimento':
                corpo.append('Objetivo: registrar a entrada da mercadoria, conferir itens e atualizar o estoque.')
            elif domain == 'estoque':
                corpo.append('Objetivo: manter o estoque correto enquanto voce registra entradas e saidas.')
            if passos:
                corpo.append('Passos sugeridos:')
                for idx, passo in enumerate(format_passos(passos), start=1):
                    corpo.append(f'{idx}. {passo}')
            if checklist:
                corpo.append('Antes de executar, confira:')
                for item in checklist[:3]:
                    corpo.append(f'- {self._ensure_sentence(item)}')
            if alertas:
                corpo.append('Atencao: ' + self._ensure_sentence(alertas[0]))
            corpo.append('Se precisar, posso detalhar algum passo ou mostrar a tela certa.')
            return '\n'.join(corpo)

        if intent == 'incident_problem':
            corpo = [f'Vamos tratar o problema em {titulo}.']
            if problemas:
                corpo.append('Causas provaveis e acoes:')
                for item in problemas[:3]:
                    corpo.append(f'- {self._ensure_sentence(item.get("situation"))}: {self._ensure_sentence(item.get("action"))}')
            else:
                corpo.append('Cheque primeiros: filtros da tela, status do registro e permissoes.')
            if alertas:
                corpo.append('Alerta: ' + self._ensure_sentence(alertas[0]))
            corpo.append('Se persistir, me diga o erro exato ou mensagem na tela para detalharmos.')
            return '\n'.join(corpo)

        if intent == 'navigation_request':
            caminho = (doc or {}).get('page_labels') or []
            caminho_txt = ' > '.join(caminho) if caminho else titulo
            return f'Voce encontra isso em {caminho_txt}. Abra e siga o fluxo indicado para continuar.'

        if intent == 'access_permission':
            passos_chk = [
                'Confirmar se o usuario esta ativo e com cargo/perfil corretos.',
                'Revisar paginas liberadas para o perfil no modulo de acessos.',
                'Fazer novo login apos ajustar permissoes.',
            ]
            corpo = ['Parece falta de permissao.']
            for idx, passo in enumerate(passos_chk, start=1):
                corpo.append(f'{idx}. {passo}')
            corpo.append('Se mesmo assim nao aparecer, informe o menu exato para eu detalhar.')
            return '\n'.join(corpo)

        return 'Posso detalhar melhor se voce explicar o que quer fazer.'

    def _build_clarifying_answer(self, question, ranking, intent):
        intent_alias = {
            'incident_problem': 'problem',
            'navigation_request': 'location',
            'access_permission': 'permission',
            'broad_exploration': 'broad_teaching',
        }.get(intent, intent)
        if not ranking or intent_alias in {'problem', 'follow_up', 'location', 'permission', 'broad_teaching'}:
            return ''

        best = ranking[0]
        second = ranking[1] if len(ranking) > 1 else None
        best_score = float(best.get('score') or 0.0)
        score_gap = best_score - float(second.get('score') or 0.0) if second else best_score
        same_section = bool(
            second
            and (best['doc'].get('section') or '').strip().lower() == (second['doc'].get('section') or '').strip().lower()
        )
        question_tokens = self._tokenize(question)
        very_short = len(question_tokens) <= 3
        low_confidence = best_score < 0.18 or (best_score < 0.28 and score_gap < 0.05 and not same_section)
        if not low_confidence and not very_short:
            return ''

        topic = self._detect_primary_topic(question, best.get('doc'))
        profile = TOPIC_PROFILES.get(topic or '')
        if profile:
            partes = ', '.join(profile.get('refinements')[:4])
            return (
                f'Posso te ajudar com mais precisao em {topic}. '
                f'Normalmente essa area envolve {profile.get("overview").rstrip(".")}. '
                f'Se quiser, eu detalho {partes}. Qual parte voce quer ver primeiro?'
            )

        opcoes = []
        vistos = set()
        for item in ranking[:3]:
            label = (item['doc'].get('source_topic') or item['doc'].get('title') or item['doc'].get('section') or '').strip()
            chave = label.lower()
            if not label or chave in vistos:
                continue
            vistos.add(chave)
            opcoes.append(label)
        if not opcoes:
            return ''
        return (
            'Posso te orientar melhor se voce me disser qual parte quer entender primeiro. '
            f'As opcoes mais proximas da sua pergunta agora sao: {", ".join(opcoes[:3])}.'
        )

    def _generate_answer(self, question, ranking, intent, *, pagina_atual=None, tela_atual=None):
        principal = ranking[0]['doc']
        titulo = principal.get('title') or tela_atual or 'esta area'
        resposta_direta = self._resolve_direct_answer(question, ranking, intent)
        passos = self._select_steps(question, ranking, intent)
        alerta = self._select_alert(ranking, question)

        if intent == 'broad_teaching':
            return self._generate_teaching_answer(question, ranking)
        if intent == 'general_help' and self._detect_primary_topic(question, principal):
            return self._generate_teaching_answer(question, ranking)

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

    def _generate_teaching_answer(self, question, ranking):
        principal = ranking[0]['doc']
        topic_key = self._detect_primary_topic(question, principal)
        tema = self._extract_topic_label(question, principal)
        profile = TOPIC_PROFILES.get(topic_key or '')
        resumo = self._ensure_sentence(
            (profile or {}).get('overview')
            or principal.get('summary')
            or principal.get('snippet')
            or f'{tema} envolve cadastros, operacao do dia a dia, controles e acompanhamento.'
        )
        passos = list((profile or {}).get('starter_steps') or ())
        if not passos:
            passos = self._select_steps(question, ranking, 'howto')
        if not passos:
            passos = self._collect_onboarding_steps(ranking)

        linhas = [
            f'Claro! Posso te explicar {tema} passo a passo.',
            resumo,
        ]
        if passos:
            linhas.append('Se voce estiver comecando, o fluxo mais comum e:')
            for indice, passo in enumerate(passos[:4], start=1):
                linhas.append(f'{indice}. {self._ensure_sentence(passo)}')
        refinements = list((profile or {}).get('refinements') or ())
        if refinements:
            linhas.append(f'Posso te explicar primeiro {", ".join(refinements[:4])}.')
        linhas.append('Posso te explicar qual parte primeiro?')
        return '\n'.join(linhas)

    def _extract_topic_label(self, question, principal):
        topic = self._detect_primary_topic(question, principal)
        if topic:
            return topic
        return (principal.get('section') or principal.get('title') or 'essa area').strip().lower()

    def _collect_onboarding_steps(self, ranking):
        passos = []
        vistos = set()
        for item in ranking[:3]:
            doc = item['doc']
            for passo in doc.get('steps') or ():
                chave = self._normalize_text(passo)
                if not chave or chave in vistos:
                    continue
                vistos.add(chave)
                passos.append(passo)
                if len(passos) >= 4:
                    return passos
        return passos

    def _resolve_direct_answer(self, question, ranking, intent):
        principal = ranking[0]['doc']
        if principal.get('kind') in {'faq', 'issue'} and principal.get('summary'):
            if intent != 'broad_teaching':
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

        if intent == 'broad_teaching':
            return principal.get('summary') or principal.get('snippet')

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
            if intent == 'problem' and doc.get('kind') not in {'issue', 'faq'} and not doc.get('problems'):
                continue
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
