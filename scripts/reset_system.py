r"""
Reseta o banco local do SystemLR com opcao de reaplicar migrations e seed.

Uso:
    .venv\Scripts\python.exe scripts\reset_system.py --yes
    .venv\Scripts\python.exe scripts\reset_system.py --yes --seed-data
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reseta o banco local do SystemLR e reaplica a estrutura base.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirma a operacao destrutiva sem pedir interacao.",
    )
    parser.add_argument(
        "--skip-migrate",
        action="store_true",
        help="Nao roda 'flask db upgrade' apos limpar a base.",
    )
    parser.add_argument(
        "--seed-data",
        action="store_true",
        help="Roda a carga de exemplo do seed_data.py depois das migrations.",
    )
    return parser


def confirm_reset(force: bool, db_path: Path) -> None:
    if force:
        return

    print("ATENCAO: esta operacao apaga os dados locais do sistema.")
    print(f"Banco identificado: {db_path}")
    answer = input("Digite RESETAR para continuar: ").strip()
    if answer != "RESETAR":
        raise SystemExit("Operacao cancelada.")


def discover_sqlite_db() -> Path:
    os.chdir(PROJECT_ROOT)

    from app import create_app  # import tardio para evitar bootstrap cedo demais
    from models import db

    app = create_app()
    with app.app_context():
        database = db.engine.url.database

    if not database:
        raise RuntimeError("Nao foi possivel identificar o banco configurado.")

    db_path = Path(database)
    if not db_path.is_absolute():
        db_path = (PROJECT_ROOT / db_path).resolve()
    return db_path


def remove_file_if_exists(path: Path) -> bool:
    if not path.exists():
        return False
    path.unlink()
    return True


def run_command(args: list[str], *, description: str) -> None:
    print(f"-> {description}")
    result = subprocess.run(args, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        raise RuntimeError(f"Falha ao executar: {' '.join(args)}")


def _credenciais_admin_primeiro_acesso() -> tuple[str, str, str]:
    # Usa exatamente a mesma origem de credenciais do fix_admin_access.py.
    from fix_admin_access import get_admin_credentials

    return get_admin_credentials()


def _sqlite_related_paths(db_file: Path) -> list[Path]:
    return [
        db_file,
        Path(f"{db_file}-wal"),
        Path(f"{db_file}-shm"),
        Path(f"{db_file}-journal"),
    ]


def _candidatos_banco_para_reset(db_path: Path) -> list[Path]:
    candidatos_base = {
        db_path,
        PROJECT_ROOT / "estoque.db",
        PROJECT_ROOT / "instance" / "estoque.db",
    }
    candidatos: list[Path] = []
    vistos: set[str] = set()
    for base in candidatos_base:
        for item in _sqlite_related_paths(base):
            chave = str(item.resolve()) if item.is_absolute() else str((PROJECT_ROOT / item).resolve())
            if chave in vistos:
                continue
            vistos.add(chave)
            candidatos.append(item)
    return candidatos


def resetar_usuarios_para_primeiro_acesso() -> None:
    os.chdir(PROJECT_ROOT)

    from app import create_app
    from models import Funcionario, db

    email, senha, nome = _credenciais_admin_primeiro_acesso()
    app = create_app()

    with app.app_context():
        admin = Funcionario.query.filter_by(email=email).first()
        if admin:
            admin.nome = nome
            admin.role = "admin"
            admin.ativo = True
            admin.senha_provisoria = True
            admin.set_password(senha)
            print(f"-> Admin existente atualizado: {email}")
        else:
            admin = Funcionario()
            admin.nome = nome
            admin.email = email
            admin.role = "admin"
            admin.ativo = True
            admin.senha_provisoria = True
            admin.set_password(senha)
            db.session.add(admin)
            db.session.flush()
            print(f"-> Admin criado: {email}")

        removidos = (
            Funcionario.query
            .filter(Funcionario.id != admin.id)
            .delete(synchronize_session=False)
        )
        db.session.commit()
        print(f"-> Usuarios removidos (exceto admin): {removidos}")
        print(f"-> Primeiro acesso configurado: email={email}")
        print("-> Troca obrigatoria de senha no primeiro login: habilitada")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    db_path = discover_sqlite_db()
    confirm_reset(args.yes, db_path)

    print(f"Projeto: {PROJECT_ROOT}")
    print(f"Banco alvo: {db_path}")

    if db_path.name.lower() != "estoque.db":
        print(f"-> Aviso: banco em runtime diferente de 'estoque.db': {db_path.name}")

    removed_any = False
    for candidate in _candidatos_banco_para_reset(db_path):
        try:
            removed = remove_file_if_exists(candidate)
        except PermissionError as exc:
            raise RuntimeError(
                f"Nao foi possivel remover {candidate}. Feche o servidor/app que esteja usando o banco e tente novamente."
            ) from exc
        if removed:
            removed_any = True
            print(f"-> Removido: {candidate}")

    if not removed_any:
        print("-> Nenhum arquivo de banco existente foi encontrado; seguindo com a recriacao.")

    if not args.skip_migrate:
        run_command(
            [sys.executable, "-m", "flask", "--app", "run.py", "db", "upgrade"],
            description="Aplicando migrations",
        )

    if args.seed_data:
        if not (PROJECT_ROOT / "seed_data.py").exists():
            raise RuntimeError("Arquivo seed_data.py nao encontrado no projeto.")
        run_command(
            [sys.executable, "seed_data.py"],
            description="Executando seed de exemplo",
        )

    resetar_usuarios_para_primeiro_acesso()

    print("Reset concluido com sucesso.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
