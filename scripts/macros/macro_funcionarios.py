"""Macro de RH, colaborador operacional e rotina de caixa."""

from __future__ import annotations

import json
from datetime import datetime

from selenium.webdriver.common.by import By

from models import Caixa, Funcionario, Garcom, MovimentacaoCaixa, Pedido, Produto

from .base_macro import BaseMacro, MacroExecutionError


class MacroFuncionarios(BaseMacro):
    """Executa o fluxo principal de cadastro de colaborador e operacao de caixa."""

    JOAO_EMAIL = "joao.silva@systemlr.com"
    JOAO_PASSWORD = "Joao@123"

    def __init__(self, **kwargs):
        super().__init__("Macro Funcionarios", **kwargs)

    def execute(self) -> None:
        self.run_step("Garantir configuracao da empresa", self.ensure_company_config)
        self.run_step("Garantir dados de venda para a rotina", self._seed_sales_products)
        self.run_step("Bootstrap do admin", self._bootstrap_admin)
        self.run_step("Login como admin", lambda: self.login(self.ADMIN_EMAIL, self.ADMIN_PASSWORD))
        self.run_step("Cadastrar cargo Garcom de Teste", self._create_function_via_ui)
        self.run_step("Cadastrar perfil Operacional PDV", self._create_profile_via_ui)
        self.run_step("Cadastrar funcionario Joao Silva", self._create_employee_via_ui)
        self.run_step("Validar menu do Joao", self._validate_joao_menu)
        self.run_step("Simular dia 1 de trabalho", self._simulate_day_1)
        self.run_step("Simular dia 2 de trabalho", self._simulate_day_2)
        self.run_step("Simular dia 3 sem saldo inicial", self._simulate_day_3_without_cash, continue_on_error=True)
        self.run_step("Validar RH e caixa no banco", self._validate_database)

    def _seed_sales_products(self) -> None:
        categoria = self.ensure_category("Conveniencia")
        fornecedor = self.ensure_supplier("Fornecedor RH")
        estoque = self.ensure_stock("Loja Operacional", code="LJ01")
        picking = self.ensure_address("Picking RH", estoque=estoque, tipo_area="picking", categoria=categoria)
        self.ensure_product(
            "Venda Dia 1",
            code="1111111111111",
            category=categoria,
            supplier=fornecedor,
            endereco=picking,
            price=50.0,
            cost=20.0,
            quantity=30,
        )
        self.ensure_cash_register("Caixa RH 01")

    def _bootstrap_admin(self) -> None:
        admin = self.get_admin()
        if admin is not None:
            self.ensure_admin()
            return
        self.open("/registro")
        self.wait_for((By.NAME, "nome"))
        self.fill((By.NAME, "nome"), "Administrador SystemLR")
        self.fill((By.NAME, "email"), self.ADMIN_EMAIL)
        self.fill((By.NAME, "senha"), self.ADMIN_PASSWORD)
        self.fill((By.NAME, "confirmacao_senha"), self.ADMIN_PASSWORD)
        self.click((By.CSS_SELECTOR, "button[type='submit']"))
        self.wait.until(lambda d: "/registro" not in d.current_url)
        self.ensure_admin()

    def _create_function_via_ui(self) -> None:
        from models import FuncaoRH

        if self.db_session.query(FuncaoRH).filter(FuncaoRH.nome == "Garçom de Teste").first():
            self.ensure_function("Garçom de Teste")
            return
        self.open("/rh/funcoes")
        self.wait_for((By.NAME, "nome"))
        self.fill((By.NAME, "nome"), "Garçom de Teste")
        self.fill((By.NAME, "descricao"), "Cargo operacional para o macro test")
        self.click((By.CSS_SELECTOR, "form[action$='/rh/funcoes/nova'] button[type='submit']"))
        self.ensure_function("Garçom de Teste")

    def _create_profile_via_ui(self) -> None:
        from models import PerfilAcesso

        if self.db_session.query(PerfilAcesso).filter(PerfilAcesso.nome == "Operacional PDV").first():
            self.ensure_profile("Operacional PDV", ["pdv", "pedidos", "caixas"])
            return
        self.open("/rh/perfis")
        self.wait_for((By.NAME, "nome"))
        self.fill((By.NAME, "nome"), "Operacional PDV")
        self.fill((By.NAME, "descricao"), "Acesso reduzido ao PDV")
        for pagina in ("pdv", "pedidos", "caixas"):
            checkbox = self.driver.find_element(By.CSS_SELECTOR, f"input[name='paginas'][value='{pagina}']")
            if not checkbox.is_selected():
                self.click_element(checkbox)
        self.click((By.CSS_SELECTOR, "form[action$='/rh/perfis-acesso/novo'] button[type='submit']"))
        self.ensure_profile("Operacional PDV", ["pdv", "pedidos", "caixas"])

    def _create_employee_via_ui(self) -> None:
        admin = self.ensure_admin()
        perfil = self.ensure_profile("Operacional PDV", ["pdv", "pedidos", "caixas"])
        existente = self.db_session.query(Funcionario).filter(Funcionario.email == self.JOAO_EMAIL).first()
        if existente:
            existente.set_password(self.JOAO_PASSWORD)
            existente.matricula = "F001"
            existente.cargo = "Garçom"
            existente.role = "caixa"
            existente.superior_id = admin.id
            existente.perfil_acesso_id = perfil.id
            existente.controle_acesso_ativo = True
            self.commit()
            return

        self.open("/funcionarios/novo")
        self.wait_for((By.NAME, "nome"))
        self.fill((By.NAME, "nome"), "João Silva")
        self.fill((By.NAME, "email"), self.JOAO_EMAIL)
        self.fill((By.NAME, "senha"), self.JOAO_PASSWORD)
        self.fill((By.NAME, "confirmacao_senha"), self.JOAO_PASSWORD)
        self.select_by_value("role", "caixa")
        self.fill((By.NAME, "cargo"), "Garçom")
        self.select_by_value("perfil_acesso_id", perfil.id)
        self.fill((By.NAME, "departamento"), "Operacoes")
        self.fill((By.NAME, "time_nome"), "Atendimento")
        self.select_by_value("superior_id", admin.id)
        self.click((By.CSS_SELECTOR, "button[type='submit']"))
        joao = self.ensure_employee(
            name="João Silva",
            email=self.JOAO_EMAIL,
            senha=self.JOAO_PASSWORD,
            role="caixa",
            cargo="Garçom",
            profile=perfil,
            matricula="F001",
            superior=admin,
        )
        joao.matricula = "F001"
        self.commit()

    def _validate_joao_menu(self) -> None:
        self.logout()
        self.login(self.JOAO_EMAIL, self.JOAO_PASSWORD)
        for fragment in ("/pdv", "/pedidos", "/caixas"):
            self.open(fragment)
            self.assert_and_screenshot(fragment in self.current_url(), f"Menu sem acesso esperado: {fragment}")
        for fragment in ("/produtos", "/movimentacoes", "/financeiro"):
            self.open(fragment)
            self.assert_and_screenshot(fragment not in self.current_url(), f"Menu exposto indevidamente: {fragment}")

    def _open_cash_register(self, saldo_inicial: float) -> Caixa:
        caixa = self.ensure_cash_register("Caixa RH 01")
        caixa.aberto = False
        caixa.funcionario_id = None
        caixa.saldo_inicial = 0.0
        caixa.saldo_atual = 0.0
        self.commit()

        self.open(f"/caixas/{caixa.id}/abrir")
        self.wait_for((By.NAME, "funcionario_id"))
        joao = self.db_session.query(Funcionario).filter(Funcionario.email == self.JOAO_EMAIL).first()
        self.select_by_value("funcionario_id", joao.id)
        self.fill((By.NAME, "saldo_inicial"), saldo_inicial)
        self.fill((By.NAME, "observacoes"), "Abertura automatizada pela macro")
        self.click((By.CSS_SELECTOR, "button[type='submit']"))
        self.db_session.expire_all()
        caixa = self.db_session.query(Caixa).filter(Caixa.id == caixa.id).first()
        self.assert_and_screenshot(bool(caixa and caixa.aberto), "Caixa nao abriu corretamente.")
        return caixa

    def _sell_using_browser_api(self, caixa_id: int, produto_codigo: str, quantidade: int) -> int:
        produto = self.db_session.query(Produto).filter(Produto.codigo == produto_codigo).first()
        if not produto:
            raise MacroExecutionError(f"Produto {produto_codigo} nao encontrado para venda.")
        self.open("/pdv")
        self.wait_for((By.ID, "caixaSelect"))
        self.select_by_value("caixaSelect", caixa_id)
        response = self.browser_fetch_json(
            "/api/pedidos/criar",
            {
                "caixa_id": caixa_id,
                "itens": [{"produto_id": produto.id, "quantidade": quantidade}],
            },
        )
        pedido_id = int(response["data"]["pedido_id"])
        self.browser_fetch_json(
            f"/api/pedidos/{pedido_id}/finalizar",
            {
                "metodo_pagamento": "dinheiro",
                "valor_pago": produto.preco_venda * quantidade,
            },
        )
        return pedido_id

    def _close_cash_register(self, caixa: Caixa, saldo_fechamento: float) -> None:
        self.open(f"/caixas/{caixa.id}/fechar")
        self.wait_for((By.NAME, "saldo_fechamento"))
        self.fill((By.NAME, "saldo_fechamento"), saldo_fechamento)
        self.fill((By.NAME, "observacoes"), "Fechamento automatizado pela macro")
        self.click((By.CSS_SELECTOR, "button[type='submit']"))

    def _simulate_day_1(self) -> None:
        caixa = self._open_cash_register(200.0)
        pedido_a = self._sell_using_browser_api(caixa.id, "1111111111111", 2)
        pedido_b = self._sell_using_browser_api(caixa.id, "1111111111111", 1)
        self._close_cash_register(caixa, 350.0)
        self.adjust_timestamps([pedido_a, pedido_b], datetime(2026, 4, 1, 10, 0, 0))

    def _simulate_day_2(self) -> None:
        caixa = self._open_cash_register(100.0)
        pedido = self._sell_using_browser_api(caixa.id, "1111111111111", 1)
        self._close_cash_register(caixa, 150.0)
        self.adjust_timestamps([pedido], datetime(2026, 4, 2, 10, 0, 0))

    def _simulate_day_3_without_cash(self) -> None:
        caixa = self.ensure_cash_register("Caixa RH 01")
        caixa.aberto = False
        self.commit()
        self.open(f"/caixas/{caixa.id}/abrir")
        joao = self.db_session.query(Funcionario).filter(Funcionario.email == self.JOAO_EMAIL).first()
        self.select_by_value("funcionario_id", joao.id)
        self.fill((By.NAME, "saldo_inicial"), 0)
        self.click((By.CSS_SELECTOR, "button[type='submit']"))
        self.db_session.expire_all()
        caixa = self.db_session.query(Caixa).filter(Caixa.id == caixa.id).first()
        self.assert_and_screenshot(not caixa.aberto, "Caixa abriu com saldo inicial zero; comportamento deveria ser bloqueado.")

    def _validate_database(self) -> None:
        joao = self.db_session.query(Funcionario).filter(Funcionario.matricula == "F001").first()
        self.assert_and_screenshot(joao is not None and joao.ativo, "Funcionario F001 nao encontrado ou inativo.")
        garcom = self.db_session.query(Garcom).filter(Garcom.funcionario_id == joao.id).first()
        self.assert_and_screenshot(garcom is not None, "Perfil de garcom nao foi sincronizado.")
        movimentos = (
            self.db_session.query(MovimentacaoCaixa)
            .join(Caixa, Caixa.id == MovimentacaoCaixa.caixa_id)
            .filter(Caixa.nome == "Caixa RH 01")
            .order_by(MovimentacaoCaixa.id.asc())
            .all()
        )
        self.assert_and_screenshot(len(movimentos) >= 4, "Movimentacoes de caixa insuficientes para o cenario de 2 dias.")
        descricoes = [mov.descricao for mov in movimentos]
        self.assert_and_screenshot(any("Abertura de caixa" in item for item in descricoes), "Abertura de caixa nao registrada.")
        pedidos_fechados = self.db_session.query(Pedido).filter(Pedido.status == "fechado").count()
        self.assert_and_screenshot(pedidos_fechados >= 3, "Vendas esperadas nao foram concluídas.")


def main() -> int:
    result = MacroFuncionarios().run()
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if result.success else 1


if __name__ == "__main__":  # pragma: no cover - execucao manual
    raise SystemExit(main())
