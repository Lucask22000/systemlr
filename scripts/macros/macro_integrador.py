"""Integrador que executa todas as macros e consolida relatorios."""

from __future__ import annotations

import json
from pathlib import Path

from .base_macro import BaseMacro, MacroResult
from .macro_cliente_online import MacroClienteOnline
from .macro_estoque import MacroEstoque
from .macro_expedicao import MacroExpedicao
from .macro_funcionarios import MacroFuncionarios
from .macro_pdv import MacroPDV


MACROS = [
    MacroFuncionarios,
    MacroClienteOnline,
    MacroPDV,
    MacroExpedicao,
    MacroEstoque,
]


def run_all() -> tuple[list[MacroResult], list[dict], list[dict]]:
    """Executa as macros em sequencia sem interromper nas falhas."""
    results: list[MacroResult] = []
    errors: list[dict] = []
    performance: list[dict] = []

    for macro_cls in MACROS:
        result = macro_cls().run()
        results.append(result)
        performance.append(
            {
                "macro": result.macro,
                "duration_seconds": result.duration_seconds,
                "success": result.success,
            }
        )
        for failure in result.failures:
            errors.append(
                {
                    "macro": failure.macro,
                    "step": failure.step,
                    "error_type": failure.error_type,
                    "message": failure.message,
                    "traceback": failure.traceback,
                    "screenshot": failure.screenshot,
                }
            )
        print(f"[{'OK' if result.success else 'FAIL'}] {result.macro} em {result.duration_seconds:.2f}s")
    return results, errors, performance


def main() -> int:
    """Ponto de entrada do integrador."""
    reports_dir = Path(__file__).resolve().parents[2] / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    results, errors, performance = run_all()
    BaseMacro.render_summary_html(results, reports_dir / "summary.html")
    (reports_dir / "errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    (reports_dir / "performance.json").write_text(json.dumps(performance, ensure_ascii=False, indent=2), encoding="utf-8")
    (reports_dir / "macro_results.json").write_text(
        json.dumps([result.to_dict() for result in results], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return 0 if all(item.success for item in results) else 1


if __name__ == "__main__":  # pragma: no cover - execucao manual
    raise SystemExit(main())
