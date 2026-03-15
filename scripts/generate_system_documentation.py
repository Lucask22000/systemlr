#!/usr/bin/env python3
"""
Generate a complete system documentation file for humans/AI.

Outputs a markdown document with:
- project/technology overview
- key folders and files
- main HTTP routes
- core data models
- important code snippets

Usage:
    python scripts/generate_system_documentation.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "system_overview_ai.md"


IMPORTANT_FUNCTIONS = {
    "app/__init__.py": [
        "dashboard",
        "gestao_negocio",
        "financeiro",
        "editar_empresa",
        "configurar_ecommerce",
        "central_ajuda",
        "detalhe_ajuda",
        "listar_funcionarios",
        "listar_perfis_rh",
    ],
    "routes/estoque_routes.py": [
        "listar_produtos",
        "novo_produto",
        "editar_produto",
        "listar_movimentacoes",
        "transferir_armazenamento",
        "relatorios",
    ],
    "routes/vendas_routes.py": [
        "register_vendas_routes",
        "listar_pedidos",
        "detalhes_pedido",
        "atualizar_separacao_entrega_pedido",
        "listar_roteirizacao_entrega",
        "painel_expedicao",
        "central_expedicao",
        "frota_expedicao",
    ],
}


ROUTE_FILES = [
    ROOT / "app" / "__init__.py",
    ROOT / "routes" / "estoque_routes.py",
    ROOT / "routes" / "vendas_routes.py",
    ROOT / "routes" / "public_routes.py",
]


TECH_HINTS = {
    "Flask": "Web framework (routing, request handling, templates).",
    "Flask-SQLAlchemy": "ORM integration with SQLAlchemy.",
    "Flask-Migrate": "Database schema migrations (Alembic integration).",
    "Flask-WTF": "Forms and CSRF protection.",
    "Flask-Limiter": "Rate limiting for endpoints.",
    "Flask-Caching": "Caching layer for computed data/queries.",
    "redis": "Cache backend/message broker support.",
    "python-dotenv": "Environment variable loading from .env.",
    "qrcode": "QR code generation.",
    "pillow": "Image processing.",
    "pytest": "Automated tests.",
    "openpyxl": "Excel export generation.",
}


def read_text(path: Path) -> str:
    for enc in ("utf-8", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def parse_requirements(path: Path) -> list[str]:
    if not path.exists():
        return []
    pkgs = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        pkg = line.split("==", 1)[0].strip()
        if pkg:
            pkgs.append(pkg)
    return pkgs


def detect_tech_stack(root: Path) -> list[tuple[str, str]]:
    requirements = parse_requirements(root / "requirements.txt")
    stack: list[tuple[str, str]] = []
    for pkg in requirements:
        stack.append((pkg, TECH_HINTS.get(pkg, "Dependency used in the project.")))

    if (root / "docker-compose.yml").exists():
        stack.append(("docker-compose", "Container orchestration for local/dev execution."))
    if (root / "Dockerfile").exists():
        stack.append(("Docker", "Container image definition for app runtime."))
    if (root / "instance" / "estoque.db").exists():
        stack.append(("SQLite", "Primary local database file detected (instance/estoque.db)."))

    return stack


def collect_core_files(root: Path) -> list[str]:
    files: list[str] = []
    for rel in [
        "app/__init__.py",
        "app/constants.py",
        "app/services/analytics.py",
        "models.py",
        "config.py",
        "security.py",
        "realtime.py",
        "routes/estoque_routes.py",
        "routes/vendas_routes.py",
        "routes/public_routes.py",
        "templates/base.html",
    ]:
        p = root / rel
        if p.exists():
            files.append(rel)
    return files


def route_methods_from_decorator(line: str) -> str:
    m = re.search(r"methods\s*=\s*\[([^\]]+)\]", line)
    if not m:
        return "GET"
    methods = re.findall(r"'([^']+)'|\"([^\"]+)\"", m.group(1))
    resolved = []
    for a, b in methods:
        token = (a or b or "").strip().upper()
        if token:
            resolved.append(token)
    return ", ".join(resolved) if resolved else "GET"


def extract_routes(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    lines = read_text(path).splitlines()
    routes: list[dict[str, str]] = []
    for idx, line in enumerate(lines):
        if "@app.route(" not in line:
            continue
        route_path = "-"
        m_path = re.search(r"@app\.route\(\s*['\"]([^'\"]+)['\"]", line)
        if m_path:
            route_path = m_path.group(1)
        methods = route_methods_from_decorator(line)

        fn_name = "-"
        line_no = idx + 1
        for j in range(idx + 1, min(idx + 10, len(lines))):
            m_fn = re.search(r"^\s*def\s+([a-zA-Z0-9_]+)\s*\(", lines[j])
            if m_fn:
                fn_name = m_fn.group(1)
                line_no = j + 1
                break

        routes.append(
            {
                "file": path.relative_to(ROOT).as_posix(),
                "path": route_path,
                "methods": methods,
                "function": fn_name,
                "line": str(line_no),
            }
        )
    return routes


def extract_models(models_file: Path, max_fields: int) -> list[dict[str, object]]:
    if not models_file.exists():
        return []
    lines = read_text(models_file).splitlines()
    models: list[dict[str, object]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m_class = re.match(r"^class\s+([A-Za-z0-9_]+)\(.*db\.Model.*\):", line)
        if not m_class:
            i += 1
            continue
        model_name = m_class.group(1)
        base_indent = len(line) - len(line.lstrip(" "))
        fields: list[str] = []
        i += 1
        while i < len(lines):
            cur = lines[i]
            cur_indent = len(cur) - len(cur.lstrip(" "))
            if cur.strip() and cur_indent <= base_indent and not cur.lstrip().startswith("#"):
                break
            m_col = re.match(r"^\s+([A-Za-z0-9_]+)\s*=\s*db\.Column\((.+)\)\s*$", cur)
            if m_col:
                field_name = m_col.group(1)
                col_desc = m_col.group(2)
                col_desc = re.sub(r"\s+", " ", col_desc)
                fields.append(f"{field_name}: {col_desc}")
            i += 1
        models.append({"name": model_name, "fields": fields[:max_fields]})
    return models


def extract_function_snippet(path: Path, function_name: str, max_lines: int) -> tuple[int, str] | None:
    if not path.exists():
        return None
    lines = read_text(path).splitlines()
    target_re = re.compile(rf"^\s*def\s+{re.escape(function_name)}\s*\(")
    for idx, line in enumerate(lines):
        if not target_re.match(line):
            continue

        def_indent = len(line) - len(line.lstrip(" "))
        start = idx
        k = idx - 1
        while k >= 0:
            prev = lines[k]
            prev_indent = len(prev) - len(prev.lstrip(" "))
            if prev.lstrip().startswith("@") and prev_indent == def_indent:
                start = k
                k -= 1
                continue
            break

        end = min(len(lines), idx + max_lines)
        for j in range(idx + 1, min(len(lines), idx + 1000)):
            cur = lines[j]
            cur_indent = len(cur) - len(cur.lstrip(" "))
            stripped = cur.lstrip()
            if stripped.startswith("def ") and cur_indent <= def_indent:
                end = j
                break
            if stripped.startswith("class ") and cur_indent <= def_indent:
                end = j
                break
            if (j - start) >= max_lines:
                end = j + 1
                break

        snippet = "\n".join(lines[start:end]).rstrip() + "\n"
        return (start + 1, snippet)
    return None


def to_markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def generate_documentation(output_path: Path, max_snippet_lines: int, max_model_fields: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generated_at = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tech_stack = detect_tech_stack(ROOT)
    core_files = collect_core_files(ROOT)

    routes: list[dict[str, str]] = []
    for f in ROUTE_FILES:
        routes.extend(extract_routes(f))

    models = extract_models(ROOT / "models.py", max_fields=max_model_fields)

    parts: list[str] = []
    parts.append("# Documentacao Tecnica do Sistema (Leitura Humana e IA)")
    parts.append("")
    parts.append(f"- Gerado em: `{generated_at}`")
    parts.append(f"- Projeto: `{ROOT.as_posix()}`")
    parts.append("- Objetivo: apresentar arquitetura, tecnologias e codigo-chave para interpretacao rapida.")
    parts.append("")

    parts.append("## 1) Tecnologias e Dependencias")
    tech_rows = [[f"`{name}`", desc] for name, desc in tech_stack]
    if tech_rows:
        parts.append(to_markdown_table(["Tecnologia", "Uso no sistema"], tech_rows))
    else:
        parts.append("Nenhuma dependencia encontrada.")
    parts.append("")

    parts.append("## 2) Arquivos Estruturais Principais")
    for rel in core_files:
        parts.append(f"- `{rel}`")
    parts.append("")

    parts.append("## 3) Rotas HTTP Principais")
    route_rows: list[list[str]] = []
    for r in routes:
        route_rows.append(
            [
                f"`{r['methods']}`",
                f"`{r['path']}`",
                f"`{r['function']}`",
                f"`{r['file']}:{r['line']}`",
            ]
        )
    parts.append(to_markdown_table(["Metodos", "Rota", "Funcao", "Arquivo"], route_rows))
    parts.append("")

    parts.append("## 4) Modelos de Dados Centrais")
    for model in models:
        parts.append(f"### Modelo: `{model['name']}`")
        fields = model["fields"]
        if not fields:
            parts.append("- Nenhum campo mapeado automaticamente.")
        else:
            for field in fields:
                parts.append(f"- `{field}`")
        parts.append("")

    parts.append("## 5) Fluxos de Negocio (Resumo)")
    parts.append("- **Cadastro e acesso**: login por funcionario com controle de permissao por pagina.")
    parts.append("- **Estoque**: produtos, movimentacoes, recebimentos, enderecamento e relatorios.")
    parts.append("- **Vendas**: PDV, pedidos, status e comprovantes.")
    parts.append("- **Expedicao**: separacao, roteirizacao, etiquetas, frota e painel em tempo real.")
    parts.append("- **Financeiro**: indicadores, lancamentos, fundos e exportacao para contador.")
    parts.append("- **RH**: funcionarios, funcoes/perfis, organograma e auditoria.")
    parts.append("- **E-commerce**: tema, banners, promocoes e configuracoes de loja.")
    parts.append("")

    parts.append("## 6) Codigo Mais Importante (Snippets)")
    for rel_path, functions in IMPORTANT_FUNCTIONS.items():
        file_path = ROOT / rel_path
        parts.append(f"### Arquivo: `{rel_path}`")
        for fn in functions:
            snippet_data = extract_function_snippet(file_path, fn, max_lines=max_snippet_lines)
            if not snippet_data:
                parts.append(f"- Funcao `{fn}` nao encontrada.")
                continue
            start_line, snippet = snippet_data
            parts.append(f"#### `{fn}` (`{rel_path}:{start_line}`)")
            parts.append("```python")
            parts.append(snippet.rstrip())
            parts.append("```")
            parts.append("")

    parts.append("## 7) Como Atualizar Esta Documentacao")
    parts.append("```bash")
    parts.append("python scripts/generate_system_documentation.py")
    parts.append("```")
    parts.append("")
    parts.append("Parametros uteis:")
    parts.append("- `--output docs/system_overview_ai.md`")
    parts.append("- `--max-snippet-lines 120`")
    parts.append("- `--max-model-fields 20`")
    parts.append("")
    parts.append(
        "Observacao: este arquivo e um resumo tecnico orientado a entendimento rapido. "
        "Para dump completo de backend, use `scripts/generate_backend_ai_report.py`."
    )
    parts.append("")

    output_path.write_text("\n".join(parts), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate system documentation for human/AI interpretation.")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT), help="Markdown output path.")
    parser.add_argument(
        "--max-snippet-lines",
        type=int,
        default=120,
        help="Max lines per code snippet.",
    )
    parser.add_argument(
        "--max-model-fields",
        type=int,
        default=20,
        help="Max fields shown per model.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = Path(args.output).resolve()
    generate_documentation(
        output_path=output,
        max_snippet_lines=max(30, args.max_snippet_lines),
        max_model_fields=max(5, args.max_model_fields),
    )
    print(f"Documentation generated at: {output}")


if __name__ == "__main__":
    main()
