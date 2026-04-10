import os

from app import create_app


app = create_app()


if __name__ == '__main__':
    debug = (os.environ.get('SYSTEMLR_DEBUG') or '0').strip().lower() in {'1', 'true', 'yes', 'on'}
    use_reloader = (os.environ.get('SYSTEMLR_USE_RELOADER') or '').strip().lower() in {'1', 'true', 'yes', 'on'}
    host = (os.environ.get('SYSTEMLR_HOST') or '0.0.0.0').strip() or '0.0.0.0'
    try:
        port = int((os.environ.get('SYSTEMLR_PORT') or '5000').strip())
    except ValueError:
        port = 5000

    app.run(
        debug=debug,
        use_reloader=use_reloader if debug else False,
        host=host,
        port=port,
    )
