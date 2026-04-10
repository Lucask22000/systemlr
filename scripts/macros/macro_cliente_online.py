"""Macro de compra online pelo e-commerce do SystemLR."""

from __future__ import annotations

import json
from datetime import date, timedelta

from selenium.webdriver.common.by import By

from models import ClientePublico, CupomUtilizacao, ItemPedido, Pedido, Produto

from .base_macro import BaseMacro


class MacroClienteOnline(BaseMacro):
    """Executa o fluxo online completo do cliente."""

    CLIENT_NAME = "Maria Silva Teste"
    CLIENT_EMAIL = "maria@teste.com"
    CLIENT_PHONE = "11988887777"

    def __init__(self, **kwargs):
        super().__init__("Macro Cliente Online", **kwargs)
        self.created_order_id: int | None = None
        self.stock_before = 0

    def execute(self) -> None:
        self.run_step("Garantir seed do e-commerce", self._seed_online_data)
        self.run_step("Acessar home", lambda: self.open("/"))
        self.run_step("Buscar produto Coca-Cola", self._search_product)
        self.run_step("Adicionar 3 unidades ao carrinho", self._add_to_cart)
        self.run_step("Aplicar cupom PRIMEIRACOMPRA", self._apply_coupon)
        self.run_step("Ir para checkout", lambda: self.open("/checkout"))
        self.run_step("Preencher checkout", self._fill_checkout)
        self.run_step("Finalizar pedido", self._submit_checkout)
        self.run_step("Validar pedido e cupom no banco", self._validate_order_db)
        self.run_step("Acessar area do cliente", self._visit_customer_area)

    def _seed_online_data(self) -> None:
        self.ensure_company_config()
        categoria = self.ensure_category("Bebidas")
        fornecedor = self.ensure_supplier("Distribuidora ABC", documento="12345678000199")
        estoque = self.ensure_stock("Loja Online", code="ONL01")
        picking = self.ensure_address("Picking A1", estoque=estoque, tipo_area="picking", categoria=categoria)
        cliente_existente = self.get_customer_by_email(self.CLIENT_EMAIL)
        if cliente_existente:
            pedidos_antigos = self.db_session.query(Pedido).filter(Pedido.cliente_publico_id == cliente_existente.id).all()
            for pedido in pedidos_antigos:
                self.db_session.query(ItemPedido).filter(ItemPedido.pedido_id == pedido.id).delete(synchronize_session=False)
                self.db_session.query(CupomUtilizacao).filter(CupomUtilizacao.pedido_id == pedido.id).delete(synchronize_session=False)
                self.db_session.delete(pedido)
            self.db_session.query(CupomUtilizacao).filter(CupomUtilizacao.cliente_id == cliente_existente.id).delete(synchronize_session=False)
            self.db_session.delete(cliente_existente)
            self.commit()
        produto = self.ensure_product(
            "Coca-Cola 2L",
            code="7891000315507",
            category=categoria,
            supplier=fornecedor,
            endereco=picking,
            price=12.9,
            cost=5.0,
            quantity=80,
            validade=date.today() + timedelta(days=30),
        )
        self.ensure_coupon("PRIMEIRACOMPRA")
        self.stock_before = produto.quantidade_estoque

    def _search_product(self) -> None:
        self.wait_for((By.ID, "storeSearchInput"))
        self.fill((By.ID, "storeSearchInput"), "Coca-Cola")
        self.wait.until(lambda d: any("Coca-Cola" in card.text for card in d.find_elements(By.CSS_SELECTOR, ".store-product-card")))

    def _add_to_cart(self) -> None:
        cards = self.find_all(".store-product-card")
        target_card = next((card for card in cards if "Coca-Cola" in card.text), None)
        self.assert_and_screenshot(target_card is not None, "Produto Coca-Cola nao apareceu na home.")
        quantity_input = target_card.find_element(By.CSS_SELECTOR, "input[name='quantidade']")
        self.fill_element(quantity_input, "3")
        self.click_element(target_card.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        self.wait_for_flash("adicionado")

    def _apply_coupon(self) -> None:
        self.open("/carrinho")
        self.wait_for((By.ID, "codigo_cupom"))
        self.fill((By.ID, "codigo_cupom"), "PRIMEIRACOMPRA")
        self.click((By.CSS_SELECTOR, "form[action$='/carrinho/cupom'] button[type='submit']"))

    def _fill_checkout(self) -> None:
        self.wait_for((By.NAME, "nome"))
        fields = {
            "nome": self.CLIENT_NAME,
            "email": self.CLIENT_EMAIL,
            "celular": self.CLIENT_PHONE,
            "cep": "01001000",
            "endereco": "Praça da Sé",
            "numero": "100",
            "bairro": "Sé",
            "cidade": "São Paulo",
            "estado": "SP",
        }
        for name, value in fields.items():
            self.fill((By.NAME, name), value)
        self.fill((By.NAME, "cpf_cnpj"), "12345678909")
        self.click((By.CSS_SELECTOR, "input[name='metodo_pagamento'][value='pix']"))

    def _submit_checkout(self) -> None:
        self.click((By.CSS_SELECTOR, "form button[type='submit']"))
        self.wait.until(lambda d: "/confirmado" in d.current_url)
        pedido = self.latest_order(origem="site", status="aberto")
        self.assert_and_screenshot(pedido is not None, "Pedido online nao foi criado.")
        self.created_order_id = pedido.id
        self.result.metadata["pedido_id"] = pedido.id

    def _validate_order_db(self) -> None:
        pedido = self.db_session.query(Pedido).filter(Pedido.id == self.created_order_id).first()
        self.assert_and_screenshot(pedido is not None and pedido.status == "aberto", "Pedido online nao ficou em status aberto.")
        produto = self.db_session.query(Produto).filter(Produto.codigo == "7891000315507").first()
        self.assert_and_screenshot(produto.quantidade_estoque == self.stock_before, "Checkout do site nao deveria baixar estoque antes do fechamento operacional.")
        cupom_uso = (
            self.db_session.query(CupomUtilizacao)
            .join(ClientePublico, ClientePublico.id == CupomUtilizacao.cliente_id)
            .filter(CupomUtilizacao.pedido_id == pedido.id, ClientePublico.email == self.CLIENT_EMAIL)
            .first()
        )
        self.assert_and_screenshot(cupom_uso is not None, "Uso do cupom PRIMEIRACOMPRA nao foi registrado.")

    def _visit_customer_area(self) -> None:
        self.open("/cliente")
        if "/cliente/login" in self.current_url():
            self.warn(
                "Fluxo passwordless ainda nao existe no produto; a macro reutilizou o cliente criado no checkout e ativou senha de apoio."
            )
            cliente = self.get_customer_by_email(self.CLIENT_EMAIL)
            if cliente and not cliente.senha_hash:
                cliente.set_password("Cliente@123")
                self.commit()
            self.open("/cliente/login")
            self.fill((By.NAME, "email"), self.CLIENT_EMAIL)
            self.fill((By.NAME, "senha"), "Cliente@123")
            self.click((By.CSS_SELECTOR, "button[type='submit']"))
            self.wait.until(lambda d: "/cliente" in d.current_url)
        self.assert_and_screenshot(
            str(self.created_order_id) in self.driver.page_source,
            "Pedido nao apareceu no historico da area do cliente.",
        )


def main() -> int:
    result = MacroClienteOnline().run()
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if result.success else 1


if __name__ == "__main__":  # pragma: no cover - execucao manual
    raise SystemExit(main())
