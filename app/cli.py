import os

import click
import qrcode

from models import Funcionario, Mesa, db


def register_cli(app):
    """Registra comandos Flask CLI para operacoes administrativas."""

    @app.cli.command('seed-data')
    def seed_data_command():
        """Popula o banco com dados de exemplo."""
        from seed_data import seed_database

        seed_database()
        click.echo('Seed finalizado.')

    @app.cli.command('fix-admin')
    @click.option('--email', default=lambda: os.environ.get('SYSTEMLR_ADMIN_EMAIL', 'admin@conveniencia.local'))
    @click.option('--senha', default=lambda: os.environ.get('SYSTEMLR_ADMIN_PASSWORD', '142536'))
    @click.option('--nome', default=lambda: os.environ.get('SYSTEMLR_ADMIN_NAME', 'Administrador'))
    def fix_admin_command(email, senha, nome):
        """Cria/atualiza usuario admin."""
        admin = Funcionario.query.filter_by(email=email).first()
        if admin:
            admin.nome = nome
            admin.role = 'admin'
            admin.ativo = True
            admin.set_password(senha)
        else:
            admin = Funcionario(nome=nome, email=email, role='admin', ativo=True)
            admin.set_password(senha)
            db.session.add(admin)
        db.session.commit()
        click.echo(f'Admin pronto: {email}')

    @app.cli.command('generate-qrcodes')
    @click.option('--base-url', default='http://localhost:5000', show_default=True)
    @click.option('--out-dir', default='qrcodes', show_default=True)
    def generate_qrcodes_command(base_url, out_dir):
        """Gera QR codes para mesas com token."""
        os.makedirs(out_dir, exist_ok=True)
        mesas = Mesa.query.all()
        total = 0
        for mesa in mesas:
            if not mesa.qr_token:
                continue
            url = f'{base_url.rstrip("/")}/m/{mesa.qr_token}'
            img = qrcode.make(url)
            filename = os.path.join(out_dir, f'mesa_{mesa.numero}.png')
            img.save(filename)
            total += 1
        click.echo(f'QR codes gerados: {total}')
