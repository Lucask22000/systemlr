# SystemLR

Sistema de gestao para loja de conveniencia com operacao integrada de vendas, estoque, RH, financeiro, servicos e e-commerce. O projeto usa Flask, SQLAlchemy, SQLite, Jinja2 e Bootstrap, com foco em operacao web responsiva para desktop e mobile.

## Visao Geral

- Dashboard operacional e gerencial
- PDV, pedidos, mesas, caixas e expedicao
- Estoque com produtos, enderecos, movimentacoes, recebimentos e relatorios
- RH com funcionarios, perfis, permissoes e organograma
- Financeiro com lancamentos, fundos e metricas
- Assistente local "Marcia" com busca hibrida, contexto de pagina e feedback like/dislike
- API interna para analytics e assistente

## Arquitetura Atual

A base esta em transicao de um `app/__init__.py` monolitico para uma estrutura modular.

Principais modulos novos:

- `app/factory.py`: cria a app e configura extensoes
- `app/decorators.py`: `login_required`, `require_role`, `_limit`
- `app/helpers.py`: helpers reutilizaveis de request, login e analytics
- `app/exceptions.py`: excecoes padronizadas de dominio
- `app/utils/validators.py`: validacoes e normalizacoes compartilhadas
- `app/utils/helpers.py`: helpers comuns como `slugify`, `sem_acentos` e `parse_date_range`

Camada de servicos:

- `app/services/pedido_service.py`
- `app/services/estoque_service.py`
- `app/services/financeiro_service.py`
- `app/services/rh_service.py`
- `app/services/assistente_service.py`
- `app/services/utils_service.py`

Rotas novas ja extraidas:

- `app/auth_routes.py`
- `app/api_routes.py`

Rotas ainda em migracao gradual:

- `app/dashboard_routes.py`
- `app/rh_routes.py`
- `app/empresa_routes.py`
- `app/services_routes.py`

## Assistente Local

A Marcia agora possui:

- configuracao de modelo por ambiente
- candidatos de embeddings com fallback
- busca hibrida: lexical + BM25 + semantica + feedback + contexto da pagina
- contexto recente de conversa
- respostas por intencao: `howto`, `problem`, `location`, `permission`, `follow_up`
- feedback persistente por `like` e `dislike`

Variaveis uteis:

- `SYSTEMLR_LOCAL_AI_ENABLED`
- `SYSTEMLR_LOCAL_AI_AUTO_INSTALL`
- `SYSTEMLR_LOCAL_AI_MODEL`
- `SYSTEMLR_LOCAL_AI_MODEL_CANDIDATES`
- `SYSTEMLR_LOCAL_AI_MAX_HISTORY_MESSAGES`

## Testes

O projeto agora possui base `pytest` em `tests/` com fixtures compartilhadas e suites por dominio:

- `tests/conftest.py`
- `tests/test_auth.py`
- `tests/test_pedidos.py`
- `tests/test_estoque.py`
- `tests/test_caixa.py`
- `tests/test_rh.py`
- `tests/test_assistente.py`

Tambem existem testes legados em `tests/test_system_flows.py`.

Executar:

```bash
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m pytest --cov=app --cov=routes --cov-report=term-missing
```

## Instalacao

```bash
cd c:\Users\lucas\OneDrive\Desktop\conveniencia
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Execucao

```bash
.venv\Scripts\python.exe run.py
```

Se necessario, ajuste:

- `FLASK_CONFIG=development`
- `SECRET_KEY`
- configuracoes de cache/Redis em producao

## Banco e Migrations

O projeto usa `Flask-Migrate/Alembic` como caminho oficial de evolucao de schema.

Antes de subir a aplicacao em ambiente novo ou apos atualizar codigo com mudancas estruturais, rode:

```bash
.venv\Scripts\flask.exe db upgrade
```

Existe documentacao de rollout e compatibilidade em [docs/database_migrations.md](c:/Users/lucas/OneDrive/Desktop/conveniencia/docs/database_migrations.md).

Fallback legado:

- `SYSTEMLR_ENABLE_RUNTIME_SCHEMA_PATCHES=1`

Use apenas como contingencia temporaria para ambientes antigos enquanto a migracao formal nao foi aplicada.

## Relatorios e Documentacao

Gerar relatorios de apoio:

```bash
.venv\Scripts\python.exe scripts/generate_backend_ai_report.py
.venv\Scripts\python.exe scripts/generate_system_documentation.py
```

Saidas:

- `docs/backend_ai_report.md`
- `docs/system_overview_ai.md`

Healthcheck tecnico:

```bash
.venv\Scripts\python.exe scripts/healthcheck.py
```

## Smoke Test Manual

Fluxo recomendado apos alteracoes maiores:

1. Fazer login com um usuario admin ou gerente.
2. Abrir dashboard e financeiro.
3. Criar um pedido via PDV ou API.
4. Finalizar o pedido e validar saldo de caixa e baixa de estoque.
5. Registrar movimentacao de estoque.
6. Criar e conferir um recebimento.
7. Abrir analytics de estoque e RH.
8. Testar a Marcia com uma saudacao e uma pergunta operacional.

## Observacoes

- O repositorio pode conter alteracoes locais grandes e nao relacionadas. Revise `git status` antes de commitar.
- Os indices adicionados em `models.py` precisam de migration/aplicacao no banco para efeito completo em producao.
