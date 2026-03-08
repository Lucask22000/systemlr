# Checklist de Rollout

## Pre-deploy

1. Definir `FLASK_CONFIG=production`.
2. Definir `SECRET_KEY` forte no ambiente.
3. Confirmar HTTPS e `SESSION_COOKIE_SECURE` ativo.
4. Executar testes automatizados:
   - `.venv\\Scripts\\python.exe -m unittest tests.test_system_flows -v`

## Smoke Test Pos Deploy

1. Login e logout.
2. Criar pedido via PDV e adicionar item.
3. Finalizar pedido e validar:
   - baixa de estoque
   - aumento de saldo da caixa
4. Tentar reabrir pedido fechado (deve falhar).
5. Abrir dashboard, relatorios e RH e validar graficos.

## Rollback

1. Reverter deploy da aplicacao.
2. Restaurar banco via backup anterior.
3. Validar login e fluxo de pedidos basico.
