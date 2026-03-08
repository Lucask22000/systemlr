from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from models import (
    Categoria,
    EnderecoEstoque,
    Fornecedor,
    Funcionario,
    Movimentacao,
    Produto,
    RecebimentoFornecedor,
    db,
)


def _run_integrity_checks() -> list[str]:
    issues: list[str] = []

    sem_categoria = (
        db.session.query(Produto)
        .outerjoin(Categoria, Produto.categoria_id == Categoria.id)
        .filter(Categoria.id.is_(None))
        .count()
    )
    sem_fornecedor = (
        db.session.query(Produto)
        .outerjoin(Fornecedor, Produto.fornecedor_id == Fornecedor.id)
        .filter((Produto.fornecedor_id.is_(None)) | (Fornecedor.id.is_(None)))
        .count()
    )
    sem_endereco = (
        db.session.query(Produto)
        .outerjoin(EnderecoEstoque, Produto.endereco_id == EnderecoEstoque.id)
        .filter((Produto.endereco_id.is_(None)) | (EnderecoEstoque.id.is_(None)))
        .count()
    )
    codigos_dup = (
        db.session.query(Produto.codigo, db.func.count(Produto.id))
        .group_by(Produto.codigo)
        .having(db.func.count(Produto.id) > 1)
        .all()
    )
    end_cod_dup = (
        db.session.query(EnderecoEstoque.codigo_localizacao, db.func.count(EnderecoEstoque.id))
        .filter(EnderecoEstoque.codigo_localizacao.isnot(None))
        .group_by(EnderecoEstoque.codigo_localizacao)
        .having(db.func.count(EnderecoEstoque.id) > 1)
        .all()
    )
    mov_qtd_neg = Movimentacao.query.filter(Movimentacao.quantidade <= 0).count()
    receb_status_invalid = (
        db.session.query(RecebimentoFornecedor)
        .filter(~RecebimentoFornecedor.status.in_(RecebimentoFornecedor.STATUS_VALIDOS))
        .count()
    )

    print("INTEGRITY_SUMMARY")
    print(f"PRODUTOS_TOTAL={Produto.query.count()}")
    print(f"PRODUTOS_SEM_CATEGORIA={sem_categoria}")
    print(f"PRODUTOS_SEM_FORNECEDOR={sem_fornecedor}")
    print(f"PRODUTOS_SEM_ENDERECO={sem_endereco}")
    print(f"PRODUTOS_CODIGO_DUP={len(codigos_dup)}")
    print(f"ENDERECOS_TOTAL={EnderecoEstoque.query.count()}")
    print(f"ENDERECOS_CODIGO_DUP={len(end_cod_dup)}")
    print(f"MOVIMENTACOES_QTD_NEG_OU_ZERO={mov_qtd_neg}")
    print(f"RECEBIMENTOS_STATUS_INVALIDO={receb_status_invalid}")

    if sem_categoria:
        issues.append("Produtos sem categoria")
    if sem_fornecedor:
        issues.append("Produtos sem fornecedor")
    if sem_endereco:
        issues.append("Produtos sem endereco")
    if codigos_dup:
        issues.append("Duplicidade de codigo de produto")
    if end_cod_dup:
        issues.append("Duplicidade de codigo_localizacao")
    if mov_qtd_neg:
        issues.append("Movimentacoes com quantidade <= 0")
    if receb_status_invalid:
        issues.append("Recebimentos com status invalido")

    return issues


def _run_smoke_get_checks() -> list[str]:
    issues: list[str] = []
    user = Funcionario.query.filter_by(ativo=True).order_by(Funcionario.id.asc()).first()
    if not user:
        print("SMOKE_SKIPPED=sem_funcionario_ativo")
        return issues

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["funcionario_id"] = user.id
        sess["funcionario_nome"] = user.nome
        sess["funcionario_role"] = user.role

    failures: list[tuple[str, int | str]] = []
    ok = 0
    skipped = 0
    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue
        if "GET" not in rule.methods:
            continue
        if rule.arguments:
            skipped += 1
            continue
        path = rule.rule
        if path.startswith("/api/pedidos/sse"):
            skipped += 1
            continue
        if any(k in path for k in ("/download", "/print")):
            skipped += 1
            continue
        try:
            resp = client.get(path)
            if resp.status_code >= 500:
                failures.append((path, resp.status_code))
            else:
                ok += 1
        except Exception:
            failures.append((path, "EXC"))

    print("SMOKE_SUMMARY")
    print(f"SMOKE_USER={user.id}:{user.role}")
    print(f"GET_OK={ok}")
    print(f"GET_SKIPPED={skipped}")
    print(f"GET_500_OR_EXC={len(failures)}")
    for path, status in failures[:30]:
        print(f"FAIL {status} {path}")

    if failures:
        issues.append("Endpoints GET com erro 500/excecao")
    return issues


def main() -> int:
    with app.app_context():
        issues = []
        issues.extend(_run_integrity_checks())
        issues.extend(_run_smoke_get_checks())

    if issues:
        print("HEALTHCHECK_STATUS=ISSUES")
        print("HEALTHCHECK_ISSUES=" + "; ".join(issues))
        return 1

    print("HEALTHCHECK_STATUS=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
