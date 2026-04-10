"""Macro de recebimento, armazenagem e transferencia entre estoques."""

from __future__ import annotations

import json
from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from models import Funcionario, Movimentacao, Produto, RecebimentoFornecedor

from .base_macro import BaseMacro


class MacroEstoque(BaseMacro):
    """Executa recebimento de fornecedor e transferencia entre estoques."""

    def __init__(self, **kwargs):
        super().__init__("Macro Estoque", **kwargs)
        self.recebimento_id: int | None = None

    def execute(self) -> None:
        self.run_step("Preparar gerente, fornecedor e enderecos", self._seed_inventory_data)
        self.run_step("Login como gerente de estoque", self._login_manager)
        self.run_step("Criar recebimento operacional", self._create_receiving)
        self.run_step("Conferir recebimento", self._confirm_receiving)
        self.run_step("Armazenar em Picking A1", self._store_receiving)
        self.run_step("Validar estoque e movimentacao de entrada", self._validate_receiving_db)
        self.run_step("Transferir produto entre estoques", self._transfer_between_stocks)
        self.run_step("Validar transferencia", self._validate_transfer_db)

    def _seed_inventory_data(self) -> None:
        admin = self.ensure_admin()
        estoque_cd = self.ensure_stock("CD Central", code="CD01")
        estoque_loja = self.ensure_stock("Loja 01", code="LJ01")
        perfil = self.ensure_profile("Gerencia Estoque", ["recebimentos", "movimentacoes", "produtos", "enderecos_estoque", "transferencias_estoque"])
        self.ensure_employee(
            name="Gerente Estoque",
            email="estoque@systemlr.com",
            senha="Estoque@123",
            role="gerente",
            cargo="Gerente de Estoque",
            profile=perfil,
            matricula="EST001",
            superior=admin,
            estoque_principal=estoque_cd,
            nivel_organograma="Gerencia",
        )
        categoria = self.ensure_category("Bebidas")
        fornecedor = self.ensure_supplier("Distribuidora ABC", documento="12345678000199")
        recebimento = self.ensure_address("Doca Recebimento", estoque=estoque_cd, tipo_area="recebimento", categoria=categoria)
        self.ensure_address("Picking A1", estoque=estoque_cd, tipo_area="picking", categoria=categoria)
        self.ensure_address("Loja 01 Picking", estoque=estoque_loja, tipo_area="picking", categoria=categoria)
        self.ensure_product(
            "Coca-Cola 2L",
            code="7891000315507",
            category=categoria,
            supplier=fornecedor,
            endereco=recebimento,
            price=12.9,
            cost=5.0,
            quantity=0,
            validade=date.today() + timedelta(days=60),
        )
        self.ensure_product(
            "Coca-Cola 2L Transferencia",
            code="7891000315514",
            category=categoria,
            supplier=fornecedor,
            endereco=recebimento,
            price=12.9,
            cost=5.0,
            quantity=30,
            validade=date.today() + timedelta(days=60),
        )

    def _login_manager(self) -> None:
        self.login("estoque@systemlr.com", "Estoque@123")

    def _create_receiving(self) -> None:
        produto = self.db_session.query(Produto).filter(Produto.nome == "Coca-Cola 2L").first()
        fornecedor = produto.fornecedor
        local_recebimento = produto.endereco
        gerente = self.db_session.query(Funcionario).filter(Funcionario.email == "estoque@systemlr.com").first()
        self.open("/estoque/recebimentos/novo")
        self.select_by_value("fornecedor_id", fornecedor.id)
        self.select_by_value("local_recebimento_id", local_recebimento.id)
        Select(self.driver.find_element(By.NAME, "produto_id[]")).select_by_value(str(produto.id))
        self.fill((By.NAME, "qtd_recebida[]"), "100")
        self.fill((By.NAME, "preco_unitario[]"), "5.00")
        self.fill((By.NAME, "descricao_item[]"), "Coca-Cola 2L")
        self.fill((By.NAME, "recebedor_busca"), gerente.nome)
        self.driver.execute_script(
            "document.getElementById('recebedor_funcionario_id').value = arguments[0];",
            str(gerente.id),
        )
        self.fill((By.NAME, "recebedor_nome"), gerente.nome)
        self.fill((By.NAME, "recebedor_assinatura"), gerente.nome)
        self.fill((By.NAME, "entregador_nome"), "Motorista Distribuidora")
        self.fill((By.NAME, "entregador_assinatura"), "Motorista Distribuidora")
        checkbox = self.driver.find_element(By.NAME, "ir_para_armazenagem")
        if checkbox.is_selected():
            self.click_element(checkbox)
        self.click((By.CSS_SELECTOR, "button[type='submit']"))
        recebimento = self.db_session.query(RecebimentoFornecedor).order_by(RecebimentoFornecedor.id.desc()).first()
        self.recebimento_id = recebimento.id
        self.assert_and_screenshot(recebimento.status == "criado", "Recebimento nao ficou com status criado.")

    def _confirm_receiving(self) -> None:
        self.open(f"/estoque/recebimentos/{self.recebimento_id}/conferir")
        self.wait_for((By.CSS_SELECTOR, "input[name$='_qtd_avaria']"))
        row_inputs = self.find_all("input[name$='_qtd_avaria']")
        self.fill_element(row_inputs[0], "0")
        self.click((By.CSS_SELECTOR, "button[type='submit']"))

    def _store_receiving(self) -> None:
        from models import EnderecoEstoque

        self.open(f"/estoque/recebimentos/{self.recebimento_id}/armazenar")
        self.wait_for((By.CSS_SELECTOR, "select[name^='endereco_destino_']"))
        picking = self.db_session.query(EnderecoEstoque).filter(EnderecoEstoque.nome == "Picking A1").first()
        options = self.find_all("select[name^='endereco_destino_']")
        Select(options[0]).select_by_value(str(picking.id))
        self.click((By.CSS_SELECTOR, "button[type='submit']"))

    def _validate_receiving_db(self) -> None:
        produto = self.db_session.query(Produto).filter(Produto.nome == "Coca-Cola 2L").first()
        self.assert_and_screenshot(produto.quantidade_estoque == 100, "Estoque do produto nao subiu para 100 apos armazenagem.")
        movimento = (
            self.db_session.query(Movimentacao)
            .filter(Movimentacao.recebimento_id == self.recebimento_id, Movimentacao.tipo == "entrada")
            .order_by(Movimentacao.id.desc())
            .first()
        )
        self.assert_and_screenshot(movimento is not None, "Movimentacao de entrada do recebimento nao foi criada.")

    def _transfer_between_stocks(self) -> None:
        from models import EnderecoEstoque

        self.open("/movimentacoes/transferencia")
        produto = self.db_session.query(Produto).filter(Produto.nome == "Coca-Cola 2L Transferencia").first()
        destino = self.db_session.query(EnderecoEstoque).filter(EnderecoEstoque.nome == "Loja 01 Picking").first()
        self.select_by_value("produto_id", produto.id)
        self.select_by_value("endereco_destino_id", destino.id)
        self.fill((By.NAME, "motivo"), "transferencia_centro_distribuicao")
        self.fill((By.NAME, "observacoes"), "Transferencia automatizada de 30 unidades para a Loja 01.")
        self.click((By.CSS_SELECTOR, "button[type='submit']"))

    def _validate_transfer_db(self) -> None:
        produto = self.db_session.query(Produto).filter(Produto.nome == "Coca-Cola 2L Transferencia").first()
        self.assert_and_screenshot(produto.endereco is not None and produto.endereco.nome == "Loja 01 Picking", "Produto transferido nao ficou no estoque destino.")
        movimento = (
            self.db_session.query(Movimentacao)
            .filter(Movimentacao.produto_id == produto.id, Movimentacao.tipo == "transferencia")
            .order_by(Movimentacao.id.desc())
            .first()
        )
        self.assert_and_screenshot(movimento is not None, "Movimentacao de transferencia nao foi registrada.")


def main() -> int:
    result = MacroEstoque().run()
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if result.success else 1


if __name__ == "__main__":  # pragma: no cover - execucao manual
    raise SystemExit(main())
