# Fase 0 - Matriz de Auditoria de Telas

Data: 2026-03-01
Escopo: 57 templates HTML

## Resumo Geral

- Total de telas: 57
- Telas que estendem `base.html`: 51
- Telas standalone: 6 (`base.html`, `public/*`, `sistema/login`, `sistema/registro`)
- Templates com CSS inline: 18
- Templates com JS inline: 10
- Rotas Flask mapeadas: 79

## Checklist Padrao por Tela

Cada tela deve atender os seguintes itens:

1. Viewport e estrutura responsiva para 360x640, 768x1024 e desktop.
2. Tipografia legivel e espacos de toque adequados.
3. Tabelas com `data-label` e fallback mobile.
4. Estados vazios e mensagens de erro claros.
5. Formularios com CSRF valido.
6. Acoes criticas com confirmacao e permissao por papel.

## Prioridade Alta (Impacto Operacional)

1. `templates/vendas/pdv.html`: fluxo de caixa/vendas, fechamento e pagamento.
2. `templates/vendas/pedidos/pedidos.html`: status, alteracao e monitoramento em tempo real.
3. `templates/vendas/caixas/caixas.html`: abertura/fechamento e seguranca de operacao.
4. `templates/dashboard/index.html`: indicadores e graficos em tempo real.
5. `templates/estoque/relatorios/relatorios.html`: visao analitica para decisao de compra.
6. `templates/rh/indicadores.html`: saude operacional da equipe.

## Riscos Encontrados

1. Ausencia de CSRF global (corrigido nesta etapa).
2. Fluxos divergentes de pedido entre web e API (em consolidacao nesta etapa).
3. Fechamento de pedido sem baixa/financeiro unificado (em consolidacao nesta etapa).
4. Inconsistencia de estilos/listas entre templates legados e novos.

## Backlog Priorizado

1. Migrar restantes de CSS/JS inline para `static/css/pages/*` e `static/js/pages/*`.
2. Completar padronizacao de macros de lista/acoes em todos os modulos.
3. Expandir testes automatizados para fluxos de RH, publico QR e relatorios.
4. Revisar textos com acentuacao quebrada em templates legados.
