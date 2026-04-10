"""Macro de separacao, roteirizacao e entrega."""

from __future__ import annotations

import json

from selenium.webdriver.common.by import By

from models import Pedido

from .base_macro import BaseMacro
from .macro_cliente_online import MacroClienteOnline


class MacroExpedicao(BaseMacro):
    """Executa separacao de pedido, despacho e confirmacao de entrega."""

    def __init__(self, **kwargs):
        super().__init__("Macro Expedicao", **kwargs)
        self.pedido_id: int | None = None

    def execute(self) -> None:
        self.run_step("Garantir usuario de expedicao e frota", self._seed_expedicao_data)
        self.run_step("Garantir pedido online aberto", self._ensure_open_site_order)
        self.run_step("Login como operador de expedicao", self._login_operator)
        self.run_step("Validar bloqueio sem area de picking", self._negative_non_picking_scenario)
        self.run_step("Separar pedido", self._separate_order)
        self.run_step("Despachar pedido", self._dispatch_order)
        self.run_step("Confirmar entrega", self._deliver_order)
        self.run_step("Validar expedicao no banco", self._validate_delivery_db)

    def _seed_expedicao_data(self) -> None:
        admin = self.ensure_admin()
        perfil = self.ensure_profile("Operador Expedicao", ["pedidos", "expedicao"])
        estoque = self.ensure_stock("Loja Online", code="ONL01")
        self.ensure_employee(
            name="Operador Expedicao",
            email="expedicao@systemlr.com",
            senha="Expedicao@123",
            role="operador",
            cargo="Operador de Expedicao",
            profile=perfil,
            matricula="EXP001",
            superior=admin,
            estoque_principal=estoque,
        )
        self.ensure_vehicle("Fiorino branco", placa="BRA0S11", motorista="Carlos")

    def _ensure_open_site_order(self) -> None:
        pedido = self.latest_order(origem="site", status="aberto")
        if pedido:
            self.pedido_id = pedido.id
            return
        nested = MacroClienteOnline(close_driver=True).run()
        if not nested.success:
            raise RuntimeError("Nao foi possivel criar pedido online para a macro de expedicao.")
        self.pedido_id = int(nested.metadata.get("pedido_id") or 0)
        self.assert_and_screenshot(bool(self.pedido_id), "Pedido online nao foi retornado pela macro cliente online.")

    def _login_operator(self) -> None:
        self.login("expedicao@systemlr.com", "Expedicao@123")

    def _expand_order_row(self) -> None:
        self.wait_for((By.CSS_SELECTOR, f"button[data-separacao-toggle='separacao-details-{self.pedido_id}']"))
        self.click((By.CSS_SELECTOR, f"button[data-separacao-toggle='separacao-details-{self.pedido_id}']"))

    def _fill_separation_form(self) -> None:
        row = self.driver.find_element(By.ID, f"separacao-details-{self.pedido_id}")
        self.fill_element(row.find_element(By.NAME, "rota_entrega"), "Rota 01 - Zona Sul")
        self.fill_element(row.find_element(By.NAME, "veiculo_tipo"), "Fiorino branco")
        self.fill_element(row.find_element(By.NAME, "motorista_nome"), "Carlos")

    def _negative_non_picking_scenario(self) -> None:
        pedido = self.db_session.query(Pedido).filter(Pedido.id == self.pedido_id).first()
        produto = pedido.itens[0].produto
        estoque = self.ensure_stock("Loja Online", code="ONL01")
        categoria = self.ensure_category("Bebidas")
        quarentena = self.ensure_address("Quarentena Q1", estoque=estoque, tipo_area="quarentena", categoria=categoria)
        produto.endereco_id = quarentena.id
        self.commit()
        self.open("/pedidos/separacao-entrega")
        self._expand_order_row()
        self._fill_separation_form()
        self.click((By.CSS_SELECTOR, f"tr#separacao-details-{self.pedido_id} button[type='submit']"))
        self.wait.until(lambda d: "picking" in d.page_source.lower() or "endere" in d.page_source.lower())
        picking = self.ensure_address("Picking A1", estoque=estoque, tipo_area="picking", categoria=categoria)
        produto.endereco_id = picking.id
        self.commit()

    def _separate_order(self) -> None:
        self.open("/pedidos/separacao-entrega")
        self._expand_order_row()
        self._fill_separation_form()
        self.click((By.CSS_SELECTOR, f"tr#separacao-details-{self.pedido_id} button[type='submit']"))
        self.wait.until(lambda d: "Separado" in d.page_source)

    def _dispatch_order(self) -> None:
        self.open("/pedidos/roteirizacao-entrega")
        row = self.find_order_row(self.pedido_id)
        self.click_element(row.find_element(By.CSS_SELECTOR, "form[action*='/despacho'] button[type='submit']"))
        self.wait.until(lambda d: "Em rota" in d.page_source or "Saiu para entrega" in d.page_source)

    def _deliver_order(self) -> None:
        self.open("/pedidos/roteirizacao-entrega")
        row = self.find_order_row(self.pedido_id)
        self.click_element(row.find_element(By.CSS_SELECTOR, "form[action*='/despacho'] button[type='submit']"))
        self.wait.until(lambda d: "Entregue" in d.page_source)

    def _validate_delivery_db(self) -> None:
        pedido = self.db_session.query(Pedido).filter(Pedido.id == self.pedido_id).first()
        self.assert_and_screenshot(pedido.status == "entregue", "Pedido nao foi marcado como entregue.")
        self.assert_and_screenshot(pedido.entrega_concluida_em is not None, "Data de entrega nao foi preenchida.")
        self.assert_and_screenshot(pedido.rota_entrega == "Rota 01 - Zona Sul", "Rota nao foi salva.")
        self.assert_and_screenshot(pedido.motorista_nome == "Carlos", "Motorista nao foi salvo.")


def main() -> int:
    result = MacroExpedicao().run()
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if result.success else 1


if __name__ == "__main__":  # pragma: no cover - execucao manual
    raise SystemExit(main())
