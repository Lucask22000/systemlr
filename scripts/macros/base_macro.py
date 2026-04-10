"""Infraestrutura base para macros Selenium do SystemLR."""

from __future__ import annotations

import html
import json
import logging
import os
import re
import sys
import time
import traceback
import unicodedata
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import urljoin

from freezegun import freeze_time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

PRODUCT_IMAGES_DIR = ROOT_DIR / "static" / "uploads" / "produtos"
ALLOWED_PRODUCT_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
PRODUCT_IMAGE_HINTS = {
    "bebidas": ("cocacola2l", "aguamineral15l", "suconaturallaranja1l"),
    "alimentos": ("biscoitoaguaesal", "bolodechocolate", "brigadeiro", "chocolateaoleite"),
    "limpeza": ("desinfetante",),
    "higiene": ("papelhigienico4rolos", "shampoo350ml", "cremedental90g"),
    "utilidades": ("batatafritapequena", "papelhigienico4rolos"),
    "pereciveis": ("chocolateaoleite", "bolodechocolate", "brigadeiro"),
    "bomboniere": ("balasortida", "brigadeiro", "chocolateaoleite"),
    "conveniencia": ("balasortida", "batatafritapequena", "cocacola2l"),
}

from app.services.rh_service import sincronizar_garcom_funcionario
from models import (
    Caixa,
    Categoria,
    ClientePublico,
    Cupom,
    EnderecoEstoque,
    EmpresaConfig,
    Fornecedor,
    FrotaVeiculo,
    FuncaoRH,
    Funcionario,
    Garcom,
    ItemPedido,
    MovimentacaoCaixa,
    Pedido,
    PerfilAcesso,
    Produto,
)


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (value or "").strip().lower()).strip("-") or "macro"


def _bool_env(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off"}


def _normalize_image_key(value: str | None) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def _looks_like_hash(name: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{24,}", name or ""))


def _catalog_product_images() -> tuple[tuple[str, str], ...]:
    if not PRODUCT_IMAGES_DIR.exists():
        return ()

    items: list[tuple[str, str]] = []
    for path in PRODUCT_IMAGES_DIR.iterdir():
        if not path.is_file() or path.suffix.lower() not in ALLOWED_PRODUCT_IMAGE_EXTENSIONS:
            continue
        key = _normalize_image_key(path.stem)
        if not key:
            continue
        items.append((key, f"uploads/produtos/{path.name}"))

    items.sort(key=lambda item: (_looks_like_hash(item[0]), len(item[0]), item[0]))
    return tuple(items)


def _resolve_product_image_path(product_name: str, category_name: str | None = None) -> str | None:
    images = _catalog_product_images()
    if not images:
        return None

    name_key = _normalize_image_key(product_name)
    category_key = _normalize_image_key(category_name)

    def _score(stem_key: str) -> tuple[int, int]:
        if name_key and stem_key == name_key:
            return (0, len(stem_key))
        if name_key and stem_key.startswith(name_key):
            return (1, len(stem_key))
        if name_key and name_key in stem_key:
            return (2, len(stem_key))
        if category_key and stem_key.startswith(category_key):
            return (3, len(stem_key))
        return (9, len(stem_key))

    direct_matches = [item for item in images if name_key and (item[0] == name_key or item[0].startswith(name_key) or name_key in item[0])]
    if direct_matches:
        return min(direct_matches, key=lambda item: _score(item[0]))[1]

    hints = PRODUCT_IMAGE_HINTS.get(category_key or "", ())
    for hint in hints:
        hinted_matches = [item for item in images if hint in item[0]]
        if hinted_matches:
            return min(hinted_matches, key=lambda item: (_looks_like_hash(item[0]), len(item[0]), item[0]))[1]

    category_matches = [item for item in images if category_key and (item[0].startswith(category_key) or category_key in item[0])]
    if category_matches:
        return min(category_matches, key=lambda item: (_looks_like_hash(item[0]), len(item[0]), item[0]))[1]

    return images[0][1]


@dataclass
class MacroFailure:
    macro: str
    step: str
    error_type: str
    message: str
    traceback: str
    screenshot: str | None = None


@dataclass
class StepResult:
    step: str
    success: bool
    started_at: str
    ended_at: str
    duration_seconds: float
    details: str = ""
    screenshot: str | None = None


@dataclass
class MacroResult:
    macro: str
    success: bool
    started_at: str
    ended_at: str
    duration_seconds: float
    steps: list[StepResult] = field(default_factory=list)
    failures: list[MacroFailure] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "macro": self.macro,
            "success": self.success,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_seconds": self.duration_seconds,
            "steps": [asdict(item) for item in self.steps],
            "failures": [asdict(item) for item in self.failures],
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }


class MacroExecutionError(RuntimeError):
    """Erro consolidado da macro."""


class BaseMacro:
    """Base comum para macros com navegador, espera e sessao SQLAlchemy."""

    ADMIN_EMAIL = "admin@systemlr.com"
    ADMIN_PASSWORD = "Admin@123"
    DEFAULT_TIMEOUT = 20

    def __init__(self, macro_name: str, *, close_driver: bool = True):
        self.macro_name = macro_name
        self.close_driver = close_driver
        self.base_url = os.environ.get("SYSTEMLR_TEST_URL", "http://localhost:5000").rstrip("/") + "/"
        self.database_url = os.environ.get("SYSTEMLR_TEST_DATABASE", "sqlite:///test_estoque.db")
        self.browser = (os.environ.get("SYSTEMLR_BROWSER") or "chrome").strip().lower()
        self.headless = _bool_env("SYSTEMLR_HEADLESS", True)
        self.screenshot_on_fail = _bool_env("SYSTEMLR_SCREENSHOT_ON_FAIL", True)
        self.timeout = int(os.environ.get("SYSTEMLR_SELENIUM_TIMEOUT", str(self.DEFAULT_TIMEOUT)))
        self.reports_dir = ROOT_DIR / "reports"
        self.screenshots_dir = self.reports_dir / "screenshots" / _slugify(macro_name)
        self.log_path = self.reports_dir / "macro.log"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self._build_logger()
        self.driver = self._build_driver()
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.db_engine = create_engine(self.database_url, future=True)
        self.db_session = sessionmaker(bind=self.db_engine, autoflush=False, expire_on_commit=False)()
        self.result = MacroResult(macro=macro_name, success=False, started_at=datetime.now().isoformat(), ended_at="", duration_seconds=0.0)
        self.log(f"Macro inicializada em {self.base_url}", "info")

    def _build_logger(self) -> logging.Logger:
        logger = logging.getLogger(f"systemlr.macros.{_slugify(self.macro_name)}")
        logger.setLevel(logging.INFO)
        if not any(isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", "") == str(self.log_path) for h in logger.handlers):
            handler = logging.FileHandler(self.log_path, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(message)s"))
            logger.addHandler(handler)
        logger.propagate = False
        return logger

    def _build_driver(self):
        if self.browser == "firefox":
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("-headless")
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1600,1200")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def execute(self) -> None:
        raise NotImplementedError

    def run(self) -> MacroResult:
        started = time.perf_counter()
        try:
            self.execute()
            self.result.success = not self.result.failures
        except Exception as exc:  # pragma: no cover - caminho operacional
            self.result.failures.append(self._register_failure("macro", exc))
            self.result.success = False
        finally:
            self.result.ended_at = datetime.now().isoformat()
            self.result.duration_seconds = round(time.perf_counter() - started, 2)
            if self.close_driver:
                self.close()
        return self.result

    def close(self) -> None:
        try:
            self.db_session.close()
        except Exception:
            pass
        try:
            self.db_engine.dispose()
        except Exception:
            pass
        try:
            self.driver.quit()
        except Exception:
            pass

    def log(self, message: str, level: str = "info") -> None:
        line = f"[{level.upper()}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {self.macro_name} - {message}"
        getattr(self.logger, level.lower(), self.logger.info)(line)

    def warn(self, message: str) -> None:
        self.result.warnings.append(message)
        self.log(message, "warning")

    def screenshot(self, step_name: str) -> str | None:
        file_path = self.screenshots_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{_slugify(step_name)}.png"
        try:
            self.driver.save_screenshot(str(file_path))
            return str(file_path.relative_to(ROOT_DIR))
        except Exception:
            return None

    def assert_and_screenshot(self, condition: bool, message: str) -> None:
        if condition:
            return
        screenshot = self.screenshot(message) if self.screenshot_on_fail else None
        if screenshot:
            self.log(f"Falha capturada em {screenshot}: {message}", "error")
        raise AssertionError(message)

    def _register_failure(self, step_name: str, exc: Exception) -> MacroFailure:
        return MacroFailure(
            macro=self.macro_name,
            step=step_name,
            error_type=type(exc).__name__,
            message=str(exc),
            traceback=traceback.format_exc(),
            screenshot=self.screenshot(step_name) if self.screenshot_on_fail else None,
        )

    def run_step(self, step_name: str, action: Callable[[], Any], *, continue_on_error: bool = False) -> Any:
        start_dt = datetime.now().isoformat()
        started = time.perf_counter()
        self.log(f"Etapa: {step_name}", "info")
        try:
            result = action()
            self.result.steps.append(StepResult(step_name, True, start_dt, datetime.now().isoformat(), round(time.perf_counter() - started, 2)))
            return result
        except Exception as exc:
            failure = self._register_failure(step_name, exc)
            self.result.failures.append(failure)
            self.result.steps.append(
                StepResult(step_name, False, start_dt, datetime.now().isoformat(), round(time.perf_counter() - started, 2), str(exc), failure.screenshot)
            )
            if continue_on_error:
                return None
            raise

    def open(self, path: str) -> None:
        self.driver.get(urljoin(self.base_url, path.lstrip("/")))

    def current_url(self) -> str:
        return self.driver.current_url

    def wait_for(self, locator: tuple[str, str], condition=EC.presence_of_element_located):
        return self.wait.until(condition(locator))

    def find(self, css: str):
        return self.driver.find_element(By.CSS_SELECTOR, css)

    def find_all(self, css: str):
        return self.driver.find_elements(By.CSS_SELECTOR, css)

    def fill(self, locator: tuple[str, str], value: Any) -> None:
        element = self.driver.find_element(*locator)
        self.fill_element(element, value)

    def fill_element(self, element, value: Any) -> None:
        value_str = "" if value is None else str(value)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
        except Exception:
            pass
        try:
            element.clear()
            element.send_keys(value_str)
            return
        except Exception:
            pass

        self.driver.execute_script(
            """
            const el = arguments[0];
            const value = arguments[1];
            const tag = (el.tagName || '').toLowerCase();
            const setter = Object.getOwnPropertyDescriptor(
                tag === 'textarea' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype,
                'value'
            ).set;
            setter.call(el, value);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            value_str,
        )

    def select_by_value(self, name: str, value: Any) -> None:
        Select(self.driver.find_element(By.NAME, name)).select_by_value(str(value))

    def click(self, locator: tuple[str, str]) -> None:
        self.click_element(self.driver.find_element(*locator))

    def click_element(self, element) -> None:
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
        except Exception:
            pass
        try:
            element.click()
            return
        except Exception:
            pass
        self.driver.execute_script("arguments[0].click();", element)

    def wait_for_flash(self, text: str) -> None:
        self.wait.until(lambda d: text.lower() in d.page_source.lower())

    def login(self, email: str, senha: str) -> None:
        self.open("/login")
        self.wait_for((By.NAME, "login"))
        self.fill((By.NAME, "login"), email)
        self.fill((By.NAME, "senha"), senha)
        self.click((By.CSS_SELECTOR, "button[type='submit']"))
        self.wait.until(lambda d: "/login" not in d.current_url)

    def logout(self) -> None:
        self.open("/logout")

    def browser_fetch_json(self, url: str, payload: dict[str, Any], *, method: str = "POST") -> dict[str, Any]:
        script = """
            const done = arguments[arguments.length - 1];
            const url = arguments[0];
            const method = arguments[1];
            const payload = arguments[2];
            const csrf = document.querySelector('meta[name="csrf-token"]')?.content || '';
            fetch(url, {
                method,
                credentials: 'same-origin',
                headers: {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-CSRF-Token': csrf},
                body: method === 'GET' ? undefined : JSON.stringify(payload)
            }).then(async (response) => {
                const text = await response.text();
                let data;
                try { data = JSON.parse(text); } catch (error) { data = {raw: text}; }
                done({ok: response.ok, status: response.status, data});
            }).catch((error) => done({ok: false, status: 0, data: {message: String(error)}}));
        """
        result = self.driver.execute_async_script(script, url, method.upper(), payload)
        if not result.get("ok"):
            message = (result.get("data") or {}).get("message") or (result.get("data") or {}).get("raw") or "Falha no fetch do navegador."
            raise MacroExecutionError(message)
        return result.get("data") or {}

    @contextmanager
    def frozen(self, frozen_at: str):
        with freeze_time(frozen_at):
            yield

    def commit(self) -> None:
        self.db_session.commit()

    def ensure_admin(self, *, email: str | None = None, senha: str | None = None) -> Funcionario:
        email = (email or self.ADMIN_EMAIL).strip().lower()
        senha = senha or self.ADMIN_PASSWORD
        admin = self.db_session.query(Funcionario).filter(Funcionario.email == email).first()
        if admin is None:
            admin = self.db_session.query(Funcionario).filter(Funcionario.role == "admin").order_by(Funcionario.id.asc()).first()
        if admin is None:
            admin = Funcionario(
                nome="Administrador SystemLR",
                email=email,
                role="admin",
                cargo="Administrador",
                departamento="Diretoria",
                time_nome="Gestao",
                nivel_organograma="Diretoria",
                ativo=True,
                controle_acesso_ativo=False,
                numero_cadastro=1,
                matricula="ADM001",
            )
            admin.set_password(senha)
            self.db_session.add(admin)
        else:
            admin.email = email
            admin.role = "admin"
            admin.ativo = True
            admin.controle_acesso_ativo = False
            admin.nome = admin.nome or "Administrador SystemLR"
            admin.cargo = admin.cargo or "Administrador"
            admin.numero_cadastro = admin.numero_cadastro or 1
            admin.matricula = admin.matricula or "ADM001"
            admin.set_password(senha)
        self.commit()
        return admin

    def get_admin(self) -> Funcionario | None:
        return self.db_session.query(Funcionario).filter(Funcionario.role == "admin").order_by(Funcionario.id.asc()).first()

    def ensure_company_config(self) -> EmpresaConfig:
        empresa = self.db_session.query(EmpresaConfig).order_by(EmpresaConfig.id.asc()).first()
        if empresa is None:
            empresa = EmpresaConfig(nome_fantasia="SystemLR Testes", razao_social="SystemLR Testes LTDA")
            self.db_session.add(empresa)
        empresa.canal_operacao = EmpresaConfig.CANAL_OPERACAO_HIBRIDO
        empresa.ecommerce_ativo = True
        empresa.separacao_entrega_ativa = True
        empresa.roteirizacao_entrega_ativa = True
        empresa.atendimento_mesas_ativo = True
        empresa.entrega_local_saida_padrao = empresa.entrega_local_saida_padrao or "Expedicao Principal"
        empresa.entrega_veiculo_padrao = empresa.entrega_veiculo_padrao or "Fiorino branco"
        empresa.entrega_motorista_padrao = empresa.entrega_motorista_padrao or "Carlos"
        self.commit()
        return empresa

    def ensure_category(self, name: str) -> Categoria:
        categoria = self.db_session.query(Categoria).filter(Categoria.nome == name).first()
        if categoria is None:
            categoria = Categoria(nome=name, descricao=f"Categoria da macro {self.macro_name}")
            self.db_session.add(categoria)
            self.commit()
        return categoria

    def ensure_supplier(self, name: str, *, documento: str | None = None) -> Fornecedor:
        fornecedor = self.db_session.query(Fornecedor).filter(Fornecedor.nome == name).first()
        if fornecedor is None:
            fornecedor = Fornecedor(nome=name, documento=documento, ativo=True)
            self.db_session.add(fornecedor)
        fornecedor.documento = documento or fornecedor.documento
        fornecedor.telefone = fornecedor.telefone or "11999990000"
        fornecedor.email = fornecedor.email or "contato@fornecedor.teste"
        fornecedor.contato = fornecedor.contato or "Equipe Comercial"
        fornecedor.endereco_rua = fornecedor.endereco_rua or "Rua do Fornecedor"
        fornecedor.endereco_numero = fornecedor.endereco_numero or "100"
        fornecedor.endereco_bairro = fornecedor.endereco_bairro or "Centro"
        fornecedor.endereco_cidade = fornecedor.endereco_cidade or "Sao Paulo"
        fornecedor.ativo = True
        self.commit()
        return fornecedor

    def ensure_stock(self, name: str, *, code: str | None = None, descricao: str | None = None):
        from models import Estoque

        estoque = self.db_session.query(Estoque).filter(Estoque.nome == name).first()
        if estoque is None:
            estoque = Estoque(nome=name, codigo_filial=code, descricao=descricao or name, ativo=True)
            self.db_session.add(estoque)
        else:
            estoque.codigo_filial = code or estoque.codigo_filial
            estoque.descricao = descricao or estoque.descricao or name
            estoque.ativo = True
        self.commit()
        return estoque

    def ensure_address(self, name: str, *, estoque, tipo_area: str, categoria: Categoria | None = None, setor_zona: str = "deposito") -> EnderecoEstoque:
        endereco = self.db_session.query(EnderecoEstoque).filter(EnderecoEstoque.nome == name).first()
        categoria = categoria or self.ensure_category("Bebidas")
        if endereco is None:
            endereco = EnderecoEstoque(nome=name)
            self.db_session.add(endereco)
        endereco.estoque_id = estoque.id
        endereco.loja_cd = estoque.codigo_filial or "LJ01"
        endereco.setor_zona = setor_zona
        endereco.tipo_area = tipo_area
        endereco.status = "ativo"
        endereco.tipo_estrutura = "area_aberta"
        endereco.ponto_local = name
        endereco.codigo_localizacao = endereco.codigo_localizacao or _slugify(name).upper()[:24]
        endereco.controle_validade = "fifo"
        endereco.tipo_produto_reservado = categoria.nome
        endereco.rua = endereco.rua or "Rua Teste"
        endereco.numero = endereco.numero or "100"
        endereco.bairro = endereco.bairro or "Centro"
        endereco.cidade = endereco.cidade or "Sao Paulo"
        endereco.estado = endereco.estado or "SP"
        endereco.cep = endereco.cep or "01001000"
        endereco.ativo = True
        self.commit()
        return endereco

    def ensure_product(self, name: str, *, code: str, category: Categoria, supplier: Fornecedor | None = None, endereco: EnderecoEstoque | None = None, price: float = 10.0, cost: float = 5.0, quantity: int = 0, validade: date | None = None, image_path: str | None = None) -> Produto:
        produto = self.db_session.query(Produto).filter(Produto.codigo == code).first()
        if produto is None:
            produto = Produto(codigo=code, nome=name, categoria_id=category.id, preco_custo=cost, preco_venda=price)
            self.db_session.add(produto)
        produto.nome = name
        produto.categoria_id = category.id
        produto.fornecedor_id = supplier.id if supplier else produto.fornecedor_id
        produto.endereco_id = endereco.id if endereco else produto.endereco_id
        produto.preco_venda = price
        produto.preco_custo = cost
        produto.quantidade_estoque = quantity
        produto.validade = validade
        produto.ativo = True
        produto.status_disponibilidade = Produto.STATUS_DISPONIVEL_ONLINE
        produto.imagem_path = image_path or _resolve_product_image_path(name, getattr(category, "nome", None))
        self.commit()
        return produto

    def ensure_coupon(self, code: str = "PRIMEIRACOMPRA") -> Cupom:
        cupom = self.db_session.query(Cupom).filter(Cupom.codigo == code).first()
        if cupom is None:
            cupom = Cupom(codigo=code, descricao="Cupom da macro", tipo_desconto="percentual", valor=10.0)
            self.db_session.add(cupom)
        cupom.ativo = True
        cupom.primeira_compra = True
        cupom.uso_unico_por_cliente = True
        cupom.data_inicio = date.today() - timedelta(days=1)
        cupom.data_fim = date.today() + timedelta(days=30)
        self.commit()
        return cupom

    def ensure_cash_register(self, name: str = "Caixa Macro 01") -> Caixa:
        caixa = self.db_session.query(Caixa).filter(Caixa.nome == name).first()
        if caixa is None:
            caixa = Caixa(nome=name, saldo_inicial=0.0, saldo_atual=0.0, aberto=False)
            self.db_session.add(caixa)
            self.commit()
        return caixa

    def ensure_function(self, name: str) -> FuncaoRH:
        item = self.db_session.query(FuncaoRH).filter(FuncaoRH.nome == name).first()
        if item is None:
            item = FuncaoRH(nome=name, descricao=f"Funcao da macro {self.macro_name}", ativo=True)
            self.db_session.add(item)
        item.ativo = True
        self.commit()
        return item

    def ensure_profile(self, name: str, pages: Iterable[str]) -> PerfilAcesso:
        perfil = self.db_session.query(PerfilAcesso).filter(PerfilAcesso.nome == name).first()
        if perfil is None:
            perfil = PerfilAcesso(nome=name)
            self.db_session.add(perfil)
        perfil.descricao = perfil.descricao or f"Perfil da macro {self.macro_name}"
        perfil.permissoes_padrao = json.dumps(sorted(set(pages)), ensure_ascii=False)
        perfil.ativo = True
        self.commit()
        return perfil

    def ensure_employee(self, *, name: str, email: str, senha: str, role: str, cargo: str, profile: PerfilAcesso | None = None, matricula: str | None = None, superior: Funcionario | None = None, estoque_principal=None, nivel_organograma: str | None = None) -> Funcionario:
        funcionario = self.db_session.query(Funcionario).filter(Funcionario.email == email).first()
        if funcionario is None:
            funcionario = Funcionario(email=email)
            self.db_session.add(funcionario)
        funcionario.nome = name
        funcionario.role = role
        funcionario.cargo = cargo
        funcionario.departamento = funcionario.departamento or "Operacoes"
        funcionario.time_nome = funcionario.time_nome or "Operacao"
        funcionario.nivel_organograma = nivel_organograma or ("Gerencia" if role == "gerente" else "Operacao")
        funcionario.ativo = True
        funcionario.perfil_acesso_id = profile.id if profile else None
        funcionario.controle_acesso_ativo = bool(profile)
        funcionario.superior_id = superior.id if superior else funcionario.superior_id
        funcionario.estoque_principal_id = estoque_principal.id if estoque_principal else funcionario.estoque_principal_id
        funcionario.numero_cadastro = funcionario.numero_cadastro or int(time.time() * 1000) % 1000000
        funcionario.matricula = matricula or funcionario.matricula or f"M{funcionario.numero_cadastro}"
        funcionario.set_password(senha)
        self.db_session.flush()
        try:
            sincronizar_garcom_funcionario(funcionario)
            self.db_session.flush()
        except Exception as exc:
            role_norm = (role or "").strip().lower()
            cargo_norm = (cargo or "").strip().lower()
            if role_norm == "garcom" or cargo_norm in {"garcom", "garçom"}:
                garcom = self.db_session.query(Garcom).filter(Garcom.funcionario_id == funcionario.id).first()
                if garcom is None:
                    garcom = Garcom(funcionario_id=funcionario.id, nome=funcionario.nome, ativo=True)
                    self.db_session.add(garcom)
                else:
                    garcom.nome = funcionario.nome
                    garcom.ativo = True
                self.db_session.flush()
            else:
                self.warn(f"Sincronizacao de garcom falhou para {name}: {exc}")
        self.commit()
        return funcionario

    def ensure_vehicle(self, nome: str, *, placa: str = "ABC1D23", motorista: str = "Carlos") -> FrotaVeiculo:
        empresa = self.ensure_company_config()
        veiculo = self.db_session.query(FrotaVeiculo).filter(FrotaVeiculo.nome == nome).first()
        if veiculo is None:
            veiculo = FrotaVeiculo(empresa_id=empresa.id, nome=nome)
            self.db_session.add(veiculo)
        veiculo.empresa_id = empresa.id
        veiculo.placa = placa
        veiculo.tipo = FrotaVeiculo.TIPO_UTILITARIO
        veiculo.capacidade_kg = 500.0
        veiculo.capacidade_volume = 4.0
        veiculo.capacidade_pedidos = 30
        veiculo.motorista_padrao = motorista
        veiculo.tipo_entrega = "site"
        veiculo.ativo = True
        self.commit()
        return veiculo

    def latest_order(self, *, origem: str | None = None, status: str | None = None) -> Pedido | None:
        query = self.db_session.query(Pedido).order_by(Pedido.id.desc())
        if origem:
            query = query.filter(Pedido.origem == origem)
        if status:
            query = query.filter(Pedido.status == status)
        return query.first()

    def get_customer_by_email(self, email: str) -> ClientePublico | None:
        return self.db_session.query(ClientePublico).filter(ClientePublico.email == email).first()

    def adjust_timestamps(self, pedido_ids: Iterable[int], when: datetime) -> None:
        pedido_ids = [int(item) for item in pedido_ids if item]
        if not pedido_ids:
            return
        pedidos = self.db_session.query(Pedido).filter(Pedido.id.in_(pedido_ids)).all()
        for pedido in pedidos:
            pedido.criado_em = when
            if pedido.fechado_em:
                pedido.fechado_em = when
        caixa_ids = [pedido.caixa_id for pedido in pedidos if pedido.caixa_id]
        if caixa_ids:
            movimentos = self.db_session.query(MovimentacaoCaixa).filter(MovimentacaoCaixa.caixa_id.in_(caixa_ids)).all()
            for mov in movimentos:
                if mov.criado_em and mov.criado_em > when:
                    mov.criado_em = when
        self.commit()

    def find_order_row(self, pedido_id: int, *, selector: str = "table tbody tr"):
        target = f"#{pedido_id}"
        for row in self.find_all(selector):
            if target in (row.text or ""):
                return row
        raise NoSuchElementException(f"Linha do pedido {pedido_id} nao encontrada.")

    @classmethod
    def render_summary_html(cls, results: list[MacroResult], target_path: Path) -> None:
        rows = []
        for result in results:
            failures = "".join(f"<li><strong>{html.escape(item.step)}</strong>: {html.escape(item.message)}</li>" for item in result.failures) or "<li>Sem falhas</li>"
            warnings = "".join(f"<li>{html.escape(item)}</li>" for item in result.warnings) or "<li>Sem avisos</li>"
            rows.append(f"<tr class=\"{'ok' if result.success else 'fail'}\"><td>{html.escape(result.macro)}</td><td>{'PASS' if result.success else 'FAIL'}</td><td>{result.duration_seconds:.2f}s</td><td><ul>{failures}</ul></td><td><ul>{warnings}</ul></td></tr>")
        page = f"""<!DOCTYPE html>
<html lang="pt-br"><head><meta charset="utf-8"><title>SystemLR Macros Summary</title>
<style>body{{font-family:Arial,sans-serif;margin:24px;background:#f8fafc;color:#0f172a}}table{{width:100%;border-collapse:collapse;background:#fff}}th,td{{border:1px solid #cbd5e1;padding:12px;vertical-align:top}}th{{background:#e2e8f0;text-align:left}}tr.ok td{{background:#f0fdf4}}tr.fail td{{background:#fef2f2}}ul{{margin:0;padding-left:20px}}</style>
</head><body><h1>Resumo das macros SystemLR</h1><p>Gerado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.</p>
<table><thead><tr><th>Macro</th><th>Status</th><th>Tempo</th><th>Falhas</th><th>Avisos</th></tr></thead><tbody>{''.join(rows)}</tbody></table></body></html>"""
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(page, encoding="utf-8")
