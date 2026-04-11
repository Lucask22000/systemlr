# SystemLR

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web-black)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)
![License](https://img.shields.io/badge/license-privado-red)

**ERP web completo para gestão empresarial com automação inteligente e assistente integrado.**

---

## 📌 Descrição

O **SystemLR** é uma plataforma ERP completa desenvolvida em Python com Flask, projetada para centralizar e automatizar operações empresariais em uma única aplicação.

O sistema atende principalmente operações de **varejo e gestão empresarial**, integrando módulos essenciais como estoque, vendas, financeiro, recursos humanos, expedição e e-commerce.

Um dos grandes diferenciais do projeto é a presença da assistente inteligente **Márcia**, que auxilia na operação com base no contexto do sistema.

---

## 🚀 Funcionalidades

### 📊 Gestão e Operação

* Dashboard operacional e gerencial
* Indicadores de desempenho em tempo real

### 💰 Financeiro

* Lançamentos financeiros e contábeis
* Gestão de fundos
* Métricas e análises

### 🛒 Vendas

* PDV (Ponto de Venda)
* Gestão de pedidos
* Mesas, caixas e garçons
* Fluxo de expedição

### 📦 Estoque

* Cadastro de produtos
* Endereçamento de estoque
* Movimentações e transferências
* Recebimento de mercadorias
* Relatórios operacionais

### 👥 Recursos Humanos (RH)

* Gestão de funcionários
* Perfis de acesso e permissões
* Organograma empresarial

### 🌐 E-commerce

* Configuração de loja online
* Gestão de campanhas e cupons

### 🤖 Assistente Inteligente (Márcia)

* Busca híbrida (lexical + semântica)
* Contexto baseado na página atual
* Histórico de conversas
* Respostas por intenção
* Sistema de feedback (like/dislike)

---

## 🛠️ Tecnologias

* **Python**
* **Flask**
* **SQLAlchemy**
* **SQLite**
* **Jinja2**
* **Bootstrap**
* **Flask-Migrate / Alembic**
* **Pytest**

---

## 🏗️ Arquitetura

O sistema está em evolução de uma arquitetura monolítica para uma estrutura modular.

### 🔹 Núcleo

* `app/factory.py` → criação e configuração da aplicação
* `app/decorators.py` → autenticação e controle de acesso
* `app/helpers.py` → utilitários reutilizáveis
* `app/exceptions.py` → tratamento de exceções
* `app/utils/validators.py` → validações compartilhadas

### 🔹 Serviços

* `pedido_service.py`
* `estoque_service.py`
* `financeiro_service.py`
* `rh_service.py`
* `assistente_service.py`

### 🔹 Rotas

* `auth_routes.py`
* `api_routes.py`

### 🔹 Em migração

* `dashboard_routes.py`
* `rh_routes.py`
* `empresa_routes.py`

---

## 🤖 Assistente Local Márcia

A assistente **Márcia** é integrada ao sistema e oferece suporte operacional inteligente.

### Funcionalidades:

* Busca híbrida (BM25 + semântica)
* Contexto da página atual
* Histórico de interações
* Classificação de intenção (how-to, problema, etc.)
* Feedback contínuo para aprendizado

### Variáveis importantes:

* `SYSTEMLR_LOCAL_AI_ENABLED`
* `SYSTEMLR_LOCAL_AI_MODEL`
* `SYSTEMLR_LOCAL_AI_MODEL_CANDIDATES`
* `SYSTEMLR_LOCAL_AI_MAX_HISTORY_MESSAGES`

---

## ⚙️ Instalação

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Execução

```bash
.venv\Scripts\python.exe run.py
```

---

## 🔐 Variáveis de Ambiente

Principais configurações:

* `FLASK_CONFIG=development`
* `SECRET_KEY`
* `SYSTEMLR_LOCAL_AI_ENABLED`
* `SYSTEMLR_LOCAL_AI_MODEL`

Recomendado criar um arquivo `.env`.

---

## 🧪 Testes

Executar testes:

```bash
.venv\Scripts\python.exe -m pytest -q
```

Cobertura:

```bash
.venv\Scripts\python.exe -m pytest --cov=app --cov=routes --cov-report=term-missing
```

---

## 🗄️ Banco de Dados e Migrations

O projeto utiliza **Flask-Migrate (Alembic)** para controle de versão do banco.

```bash
.venv\Scripts\flask.exe db upgrade
```

Fallback (uso temporário):

```bash
SYSTEMLR_ENABLE_RUNTIME_SCHEMA_PATCHES=1
```

---

## 📁 Estrutura do Projeto

```text
app/
routes/
tests/
docs/
scripts/
models.py
run.py
config.py
```

---

## 🛣️ Roadmap

* [x] Estrutura inicial do ERP
* [x] Módulos principais (estoque, vendas, financeiro, RH)
* [x] Assistente inteligente integrada
* [ ] Modularização completa das rotas
* [ ] Melhorias de responsividade
* [ ] Otimização de performance
* [ ] Expansão do e-commerce
* [ ] API pública externa

---

## ⚠️ Observações

* Projeto em evolução contínua
* Revisar migrations antes de deploy
* Evitar subir arquivos sensíveis (.env, banco local)
* Estrutura está sendo progressivamente modularizada

---

## 📌 Status

🚧 Em desenvolvimento ativo

---

## 💡 Autor

Lucas Ramalho
Especialista em automação, sistemas e desenvolvimento Python
---
