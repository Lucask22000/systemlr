# Macros SystemLR

Macros Selenium para validar fluxos operacionais do SystemLR.

## Variaveis de ambiente

```powershell
$env:SYSTEMLR_TEST_URL="http://localhost:5000"
$env:SYSTEMLR_TEST_DATABASE="sqlite:///test_estoque.db"
$env:SYSTEMLR_HEADLESS="true"
$env:SYSTEMLR_SCREENSHOT_ON_FAIL="true"
```

## Dependencias

```powershell
pip install -r scripts/macros/requirements.txt
```

## Execucao individual

```powershell
python -m scripts.macros.macro_funcionarios
python -m scripts.macros.macro_cliente_online
python -m scripts.macros.macro_pdv
python -m scripts.macros.macro_expedicao
python -m scripts.macros.macro_estoque
```

## Execucao integrada

```powershell
python -m scripts.macros.macro_integrador
```

Arquivos gerados:

- `reports/summary.html`
- `reports/errors.json`
- `reports/performance.json`
- `reports/screenshots/`

## Observacoes praticas

- A area do cliente atual ainda nao tem magic link/passwordless. A macro online reaproveita a sessao criada no checkout e, se necessario, ativa senha de apoio para validar o historico.
- O fluxo de caixa com saldo inicial zero esta mantido como teste negativo: se o sistema aceitar a abertura, a macro registra falha.
- A transferencia entre estoques usa o fluxo atual do produto, que move o saldo inteiro associado ao endereco do item.
