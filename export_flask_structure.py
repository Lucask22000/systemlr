#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exporta estrutura e arquivos relevantes de um projeto Flask em um único .md.
Rode dentro da pasta do projeto:
    python export_flask_structure.py
Saída:
    flask_export.md
"""

from __future__ import annotations

import re
from pathlib import Path
from datetime import datetime

# =========================
# CONFIGURAÇÕES
# =========================

OUTPUT_FILE = "flask_export.md"

# Pastas para ignorar totalmente
IGNORE_DIRS = {
    ".git", ".hg", ".svn",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "venv", ".venv", "env", ".env",  # ambientes virtuais
    "node_modules",
    "dist", "build", ".build", ".eggs",
    ".idea", ".vscode",
    "static/vendor",  # comum ter libs grandes
    "media", "uploads",  # opcional: uploads geralmente são pesados
}

# Arquivos específicos a ignorar
IGNORE_FILES = {
    ".DS_Store",
    "Thumbs.db",
}

# Extensões normalmente desnecessárias para "estrutura+codigo"
IGNORE_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".pdf", ".zip", ".rar", ".7z", ".tar", ".gz",
    ".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav",
    ".sqlite", ".db", ".log",
}

# Extensões que queremos capturar
INCLUDE_EXTS = {
    ".py", ".html", ".jinja", ".jinja2", ".css", ".js",
    ".txt", ".md", ".ini", ".cfg", ".toml", ".yaml", ".yml",
    ".env.example",  # caso exista como arquivo literal
}

# Arquivos importantes mesmo sem extensão / nomes comuns de projeto
INCLUDE_FILENAMES = {
    "requirements.txt", "requirements-dev.txt", "pyproject.toml", "poetry.lock",
    "Pipfile", "Pipfile.lock",
    "setup.py", "MANIFEST.in",
    "Dockerfile", "docker-compose.yml", "compose.yml",
    ".flaskenv", ".env.example",
    "wsgi.py", "asgi.py", "manage.py",
    "README", "README.md", "README.rst",
    "config.py",
}

# Limite de tamanho por arquivo (para não puxar coisas enormes sem querer)
MAX_FILE_SIZE_BYTES = 400_000  # 400 KB

# Se quiser evitar capturar minificados mesmo sendo .js/.css
MINIFIED_REGEX = re.compile(r"\.min\.(js|css)$", re.IGNORECASE)

# =========================
# FUNÇÕES
# =========================

def is_ignored_dir(path: Path) -> bool:
    parts = set(path.parts)
    # ignora se qualquer parte do caminho estiver em IGNORE_DIRS
    return any(p in IGNORE_DIRS for p in parts)

def is_included_file(path: Path) -> bool:
    name = path.name

    if name in IGNORE_FILES:
        return False

    if MINIFIED_REGEX.search(name):
        return False

    # ignora extensões pesadas
    if path.suffix.lower() in IGNORE_EXTS:
        return False

    # inclui por nome
    if name in INCLUDE_FILENAMES:
        return True

    # inclui por extensão
    if path.suffix.lower() in INCLUDE_EXTS:
        return True

    # inclui casos como ".env.example" (sufixo é ".example" então não cai em INCLUDE_EXTS)
    if name.endswith(".env.example"):
        return True

    return False

def safe_read_text(path: Path) -> str:
    # Tenta ler como utf-8, com fallback "replace"
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")

def build_tree_lines(root: Path, included_files: set[Path]) -> list[str]:
    """
    Mostra árvore apenas de pastas e arquivos incluídos (pra ficar limpo).
    """
    lines: list[str] = []
    root = root.resolve()

    # Agrupa por diretório
    dirs = set()
    for f in included_files:
        try:
            rel = f.relative_to(root)
        except ValueError:
            continue
        # adiciona todos os pais
        for parent in rel.parents:
            dirs.add(parent)

    # Nós: diretórios e arquivos
    nodes = sorted(
        list(dirs) + [f.relative_to(root) for f in included_files],
        key=lambda p: (len(p.parts), str(p).lower())
    )

    # Monta tree simples por indentação
    for n in nodes:
        indent = "  " * (len(n.parts) - 1)
        lines.append(f"{indent}- {n.name if n.name else '.'}")
    return lines

def collect_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if p.is_dir():
            # rglob não permite pular fácil; filtramos nos arquivos
            continue

        if is_ignored_dir(p.parent):
            continue

        if not is_included_file(p):
            continue

        try:
            size = p.stat().st_size
        except OSError:
            continue

        if size > MAX_FILE_SIZE_BYTES:
            continue

        files.append(p)

    # Ordena de forma estável
    files.sort(key=lambda x: str(x).lower())
    return files

def main() -> None:
    root = Path(".").resolve()
    files = collect_files(root)
    included_set = set(files)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"# Export do Projeto Flask\n\n")
        out.write(f"- Pasta raiz: `{root}`\n")
        out.write(f"- Gerado em: `{now}`\n")
        out.write(f"- Total de arquivos incluídos: **{len(files)}**\n\n")

        out.write("## 1) Árvore do projeto (somente itens relevantes)\n\n")
        out.write("```text\n")
        out.write(".\n")
        for line in build_tree_lines(root, included_set):
            out.write(line + "\n")
        out.write("```\n\n")

        out.write("## 2) Lista de arquivos incluídos\n\n")
        for f in files:
            rel = f.relative_to(root)
            out.write(f"- `{rel}`\n")
        out.write("\n")

        out.write("## 3) Conteúdo dos arquivos\n\n")
        for f in files:
            rel = f.relative_to(root)
            out.write(f"\n---\n\n")
            out.write(f"### Arquivo: `{rel}`\n\n")

            # tenta detectar linguagem pelo sufixo
            lang = f.suffix.lower().lstrip(".")
            if rel.name in {"Dockerfile"}:
                lang = "dockerfile"
            elif rel.name in {"docker-compose.yml", "compose.yml"}:
                lang = "yaml"
            elif rel.name in {"requirements.txt", "requirements-dev.txt"}:
                lang = "text"

            out.write(f"```{lang}\n")
            out.write(safe_read_text(f))
            if not safe_read_text(f).endswith("\n"):
                out.write("\n")
            out.write("```\n")

    print(f"[OK] Export gerado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
