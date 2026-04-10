#!/usr/bin/env python3
"""
Gera um relatorio completo do backend em Markdown para analise por IA.

Uso rapido:
    python scripts/generate_backend_ai_report.py

Saida padrao:
    docs/backend_ai_report.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "backend_ai_report.md"


EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".vscode",
    "static",
    "templates",
    "tests",
    "docs",
    "instance",
    "migrations",
}

INCLUDE_DIRS = ["app", "routes", "utils"]
INCLUDE_ROOT_FILES = [
    "run.py",
    "config.py",
    "models.py",
    "security.py",
    "realtime.py",
    "seed_data.py",
    "fix_admin_access.py",
]


def _iter_python_files(base: Path) -> Iterable[Path]:
    for rel in INCLUDE_DIRS:
        path = base / rel
        if not path.exists():
            continue
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for name in files:
                if name.endswith(".py"):
                    yield Path(root) / name

    for name in INCLUDE_ROOT_FILES:
        file_path = base / name
        if file_path.exists() and file_path.suffix == ".py":
            yield file_path


def _safe_read_text(path: Path) -> str:
    for enc in ("utf-8", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def _count_lines(text: str) -> int:
    return 0 if not text else text.count("\n") + 1


def _sha256_short(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def _build_tree_lines(files: list[Path], base: Path) -> list[str]:
    lines: list[str] = []
    grouped: dict[str, list[str]] = {}
    root_files: list[str] = []
    for f in files:
        rel = f.relative_to(base).as_posix()
        if "/" not in rel:
            root_files.append(rel)
            continue
        top = rel.split("/", 1)[0]
        grouped.setdefault(top, []).append(rel)

    for rel in sorted(root_files):
        lines.append(f"- {rel}")
    for top in sorted(grouped):
        lines.append(f"- {top}/")
        for rel in sorted(grouped[top]):
            if rel == top:
                continue
            lines.append(f"  - {rel}")
    return lines


def _build_optimization_hints() -> str:
    return (
        "## 7) Pistas de otimizacao para IA\n"
        "- Mapear funcoes com mais de 80 linhas e sugerir extracao de servicos.\n"
        "- Identificar queries repetidas por rota e sugerir cache/local batching.\n"
        "- Verificar N+1 em relacionamentos SQLAlchemy e aplicar selectinload/joinedload.\n"
        "- Revisar rotas com muita regra de negocio e mover para camada de servico.\n"
        "- Auditar validacoes de entrada e centralizar em funcoes reutilizaveis.\n"
        "- Propor padrao unico de respostas de erro e mensagens de usuario.\n"
        "- Sugerir testes para rotas criticas (auth, pedidos, financeiro, estoque).\n"
        "- Revisar nomes/encoding para padrao unico e evitar regressao de idioma.\n"
        "\n"
        "### Prompt recomendado para outra IA\n"
        "Use este relatorio para:\n"
        "1. identificar gargalos de performance,\n"
        "2. sugerir refatoracoes por prioridade (alto/medio/baixo),\n"
        "3. listar riscos tecnicos,\n"
        "4. sugerir plano de implementacao em etapas curtas com baixo risco.\n"
    )


def generate_report(output_path: Path, max_file_kb: int) -> tuple[int, int]:
    files = sorted(set(_iter_python_files(ROOT)))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_lines = 0
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_parts: list[str] = []
    report_parts.append("# Relatorio Completo do Backend (para IA)\n")
    report_parts.append(f"- Gerado em: {now}\n")
    report_parts.append(f"- Projeto base: `{ROOT.as_posix()}`\n")
    report_parts.append(f"- Total de arquivos Python mapeados: **{len(files)}**\n")
    report_parts.append(
        "\n## 1) Escopo\n"
        "- Inclui: `app/`, `routes/`, `utils/` e arquivos Python principais na raiz.\n"
        "- Exclui: assets frontend, migracoes, ambiente virtual e caches.\n"
    )

    report_parts.append("\n## 2) Estrutura de arquivos\n")
    report_parts.extend(_build_tree_lines(files, ROOT))

    report_parts.append("\n## 3) Inventario de arquivos\n")
    report_parts.append("| Arquivo | Linhas | Tamanho (KB) | Hash (sha256-16) |")
    report_parts.append("|---|---:|---:|---|")

    file_entries: list[tuple[Path, str, int, float, str]] = []
    for f in files:
        text = _safe_read_text(f)
        lines = _count_lines(text)
        size_kb = f.stat().st_size / 1024
        digest = _sha256_short(text)
        total_lines += lines
        rel = f.relative_to(ROOT).as_posix()
        file_entries.append((f, rel, lines, size_kb, digest))
        report_parts.append(f"| `{rel}` | {lines} | {size_kb:.1f} | `{digest}` |")

    report_parts.append(f"\n**Total de linhas backend:** {total_lines}\n")
    report_parts.append(
        "\n## 4) Codigo fonte consolidado\n"
        "Observacao: arquivos muito grandes podem ser truncados para manter o relatorio utilizavel.\n"
    )

    max_bytes = max_file_kb * 1024
    for f, rel, lines, size_kb, _ in file_entries:
        report_parts.append(f"\n### Arquivo: `{rel}`")
        report_parts.append(f"- Linhas: {lines}")
        report_parts.append(f"- Tamanho: {size_kb:.1f} KB")
        text = _safe_read_text(f)
        encoded = text.encode("utf-8", errors="replace")
        if len(encoded) > max_bytes:
            trimmed = encoded[:max_bytes].decode("utf-8", errors="ignore")
            report_parts.append(f"- Status: truncado em {max_file_kb} KB")
            report_parts.append("\n```python")
            report_parts.append(trimmed)
            report_parts.append("\n# ... arquivo truncado para caber no relatorio")
            report_parts.append("```\n")
        else:
            report_parts.append("- Status: completo")
            report_parts.append("\n```python")
            report_parts.append(text)
            report_parts.append("```\n")

    report_parts.append(
        "\n## 5) Checklist para auditoria tecnica\n"
        "- Seguranca: auth, autorizacao por perfil, CSRF, validacao de entrada.\n"
        "- Performance: consultas pesadas, paginação, cache, N+1.\n"
        "- Qualidade: duplicacao de codigo, tamanho de funcoes, acoplamento.\n"
        "- Operacao: logs, auditoria, tratamento de erro, observabilidade.\n"
        "- Testes: cobertura de rotas criticas e regras de negocio.\n"
    )
    report_parts.append(
        "\n## 6) Metadados para comparacao de versoes\n"
        "- Este arquivo pode ser gerado periodicamente e comparado por hash/linhas.\n"
        "- Recomendacao: salvar junto com hash do commit para trilha de evolucao.\n"
    )
    report_parts.append(_build_optimization_hints())

    output_path.write_text("\n".join(report_parts), encoding="utf-8")
    return len(files), total_lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gerador de relatorio backend para IA.")
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT),
        help="Caminho do arquivo de saida Markdown.",
    )
    parser.add_argument(
        "--max-file-kb",
        type=int,
        default=512,
        help="Limite de tamanho por arquivo antes de truncar no relatorio.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output).resolve()
    files, lines = generate_report(output_path, max_file_kb=max(32, args.max_file_kb))
    print(f"Relatorio gerado: {output_path}")
    print(f"Arquivos: {files} | Linhas totais: {lines}")


if __name__ == "__main__":
    main()
