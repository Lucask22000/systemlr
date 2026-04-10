"""Macro de venda no PDV."""

from __future__ import annotations

import json
from datetime import date, timedelta

from selenium.webdriver.common.by import By

from models import Caixa, Funcionario, Movimentacao, Pedido

from .base_macro import BaseMacro


class MacroPDV(BaseMacro):
    """Executa uma venda de balcão no PDV e valida os reflexos no banco."""

    def __init__(self, **kwargs):
        super().__init__("Macro PDV", **kwargs)
        self.caixa_id: int | None = None
        self.pedido_id: int | None = None
        self.saldo_antes = 0.0

    def execute(self) -> None:
        self.run_step("Preparar colaborador e produtos do PDV", self._seed_pdv_data)
        self.run_step("Login como caixa", self._login_caixa)
        self.run_step("Abrir caixa com R$ 500", self._open_cash_register)
        self.run_step("Acessar PDV", lambda: self.open("/pdv"))
        self.run_step("Buscar Coca-Cola por codigo de barras", self._add_coke_by_barcode)
        self.run_step("Adicionar segunda unidade da Coca-Cola", self._add_coke_by_barcode)
        self.run_step("Buscar Chocolate por nome", self._add_chocolate_by_name)
        self.run_step("Finalizar venda em dinheiro", self._finalize_sale)
        self.run_step("Validar pedido, estoque e caixa", self._validate_sale_db)
        self.run_step("Bloquear venda de produto vencido", self._validate_expired_product_block)
        self.run_step("Fechar caixa", self._close_cash_register)

    def _seed_pdv_data(self) -> None:
        admin = self.ensure_admin()
        perfil = self.ensure_profile("Operacional PDV", ["pdv", "pedidos", "caixas"])
        estoque = self.ensure_stock("Loja PDV", code="PDV01")
        categoria = self.ensure_category("Bomboniere")
        fornecedor = self.ensure_supplier("Fornecedor PDV")
        picking = self.ensure_address("Picking PDV A1", estoque=estoque, tipo_area="picking", categoria=categoria)
        self.ensure_employee(
            name="João Silva",
            email="joao.silva@systemlr.com",
            senha="Joao@123",
            role="caixa",
            cargo="Garçom",
            profile=perfil,
            matricula="F001",
            superior=admin,
            estoque_principal=estoque,
        )
        self.ensure_product(
            "Coca-Cola 2L",
            code="7891000315507",
            category=categoria,
            supplier=fornecedor,
            endereco=picking,
            price=12.9,
            cost=5.0,
            quantity=60,
            validade=date.today() + timedelta(days=30),
        )
        self.ensure_product(
            "Chocolate",
            code="7890000000001",
            category=categoria,
            supplier=fornecedor,
            endereco=picking,
            price=20.0,
            cost=8.0,
            quantity=40,
            validade=date.today() + timedelta(days=30),
        )
        caixa = self.ensure_cash_register("Caixa Macro 01")
        caixa.aberto = False
        self.commit()

    def _login_caixa(self) -> None:
        self.login("joao.silva@systemlr.com", "Joao@123")

    def _open_cash_register(self) -> None:
        caixa = self.ensure_cash_register("Caixa Macro 01")
        self.open(f"/caixas/{caixa.id}/abrir")
        funcionario = self.db_session.query(Funcionario).filter(Funcionario.email == "joao.silva@systemlr.com").first()
        self.select_by_value("funcionario_id", funcionario.id)
        self.fill((By.NAME, "saldo_inicial"), 500)
        self.click((By.CSS_SELECTOR, "button[type='submit']"))
        self.db_session.expire_all()
        caixa = self.db_session.query(Caixa).filter(Caixa.id == caixa.id).first()
        self.caixa_id = caixa.id
        self.saldo_antes = float(caixa.saldo_atual or 0.0)
        self.assert_and_screenshot(caixa.aberto, "Caixa do PDV nao abriu.")

    def _select_cash_register_inside_pdv(self) -> None:
        self.wait_for((By.ID, "caixaSelect"))
        from selenium.webdriver.support.select import Select
        Select(self.driver.find_element(By.ID, "caixaSelect")).select_by_value(str(self.caixa_id))

    def _add_coke_by_barcode(self) -> None:
        self._select_cash_register_inside_pdv()
        self.fill((By.ID, "filtroNome"), "7891000315507")
        self.wait.until(lambda d: "Coca-Cola 2L" in d.page_source)

    def _add_chocolate_by_name(self) -> None:
        field = self.driver.find_element(By.ID, "filtroNome")
        self.fill_element(field, "Chocolate")
        field.send_keys("\n")

    def _finalize_sale(self) -> None:
        self.click((By.ID, "btnNovaVenda"))
        self.wait.until(lambda d: "Finalizar pagamento" in d.page_source)
        self.fill((By.ID, "paymentValor"), "50")
        self.click((By.ID, "btnConfirmarPagamento"))
        self.wait.until(lambda d: "Pedido finalizado com sucesso" in d.page_source or "comprovante" in d.page_source.lower())
        pedido = self.latest_order(status="fechado")
        self.assert_and_screenshot(pedido is not None, "Nenhum pedido fechado foi gerado pelo PDV.")
        self.pedido_id = pedido.id

    def _validate_sale_db(self) -> None:
        pedido = self.db_session.query(Pedido).filter(Pedido.id == self.pedido_id).first()
        self.assert_and_screenshot(pedido.status == "fechado", "Pedido do PDV nao ficou fechado.")
        movimentos = self.db_session.query(Movimentacao).filter(Movimentacao.pedido_id == pedido.id, Movimentacao.tipo == "saida").all()
        self.assert_and_screenshot(bool(movimentos), "Baixa de estoque da venda de PDV nao foi registrada.")
        caixa = self.db_session.query(Caixa).filter(Caixa.id == self.caixa_id).first()
        self.assert_and_screenshot(
            round(float(caixa.saldo_atual or 0.0), 2) == round(self.saldo_antes + 45.8, 2),
            "Saldo do caixa nao refletiu os R$ 45,80 da venda.",
        )

    def _validate_expired_product_block(self) -> None:
        categoria = self.ensure_category("Bloqueio")
        fornecedor = self.ensure_supplier("Fornecedor Bloqueio")
        estoque = self.ensure_stock("Loja PDV", code="PDV01")
        picking = self.ensure_address("Picking PDV A1", estoque=estoque, tipo_area="picking", categoria=categoria)
        expired = self.ensure_product(
            "Produto Vencido",
            code="9999999999999",
            category=categoria,
            supplier=fornecedor,
            endereco=picking,
            price=3.0,
            cost=1.0,
            quantity=10,
            validade=date.today() - timedelta(days=1),
        )
        self.open("/pdv")
        self._select_cash_register_inside_pdv()
        self.fill((By.ID, "filtroNome"), expired.codigo)
        self.assert_and_screenshot("Produto Vencido" not in self.driver.page_source, "Produto vencido apareceu como vendavel no PDV.")

    def _close_cash_register(self) -> None:
        self.open(f"/caixas/{self.caixa_id}/fechar")
        caixa = self.db_session.query(Caixa).filter(Caixa.id == self.caixa_id).first()
        self.fill((By.NAME, "saldo_fechamento"), f"{caixa.saldo_atual:.2f}")
        self.click((By.CSS_SELECTOR, "button[type='submit']"))


def main() -> int:
    result = MacroPDV().run()
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if result.success else 1


if __name__ == "__main__":  # pragma: no cover - execucao manual
    raise SystemExit(main())
