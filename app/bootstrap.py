"""Application bootstrap helpers.

Mantem a inicializacao centralizada sem alterar o fluxo legado.
"""


def bootstrap_app(app, *, db, extensions_module, register_cli_fn):
    """Inicializa extensoes e comandos CLI no mesmo fluxo do bootstrap atual."""
    db.init_app(app)
    extensions_module.init_extensions(app, db)
    register_cli_fn(app)
