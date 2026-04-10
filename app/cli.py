import json
import os
from datetime import date, datetime

import click
import qrcode

from models import Funcionario, Mesa, Produto, db


def register_cli(app):
    """Registra comandos Flask CLI para operacoes administrativas."""

    @app.cli.command('seed-data')
    def seed_data_command():
        """Popula o banco com dados de exemplo."""
        from seed_data import seed_database

        seed_database()
        click.echo('Seed finalizado.')

    @app.cli.command('seed-operational-homologation')
    @click.option('--reset', is_flag=True, help='Limpa a base antes da carga. Use com cuidado.')
    def seed_operational_homologation_command(reset):
        """Popula o banco com massa operacional de homologacao."""
        from scripts.seed_operational_homologation import seed_operational_homologation

        resumo = seed_operational_homologation(reset=reset)
        click.echo(json.dumps(resumo, ensure_ascii=False, indent=2))

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

    @app.cli.command('check-expired-products')
    @click.option('--reference-date', default=None, help='Data de referencia no formato YYYY-MM-DD.')
    def check_expired_products_command(reference_date):
        """Desativa produtos vencidos e retira sua disponibilidade operacional."""
        if reference_date:
            try:
                referencia = datetime.strptime(reference_date, '%Y-%m-%d').date()
            except ValueError as exc:
                raise click.BadParameter('Use o formato YYYY-MM-DD para --reference-date.') from exc
        else:
            referencia = date.today()

        produtos = Produto.query.filter(
            Produto.validade.is_not(None),
            Produto.validade < referencia,
        ).all()

        atualizados = 0
        for produto in produtos:
            mudou = False
            if produto.ativo:
                produto.ativo = False
                mudou = True
            if Produto.normalizar_status_disponibilidade(produto.status_disponibilidade) != Produto.STATUS_DISPONIVEL_OFF:
                produto.status_disponibilidade = Produto.STATUS_DISPONIVEL_OFF
                mudou = True
            if mudou:
                atualizados += 1

        db.session.commit()
        click.echo(
            f'{atualizados} produto(s) vencido(s) atualizado(s) em {referencia.isoformat()}. '
            f'Total expirado encontrado: {len(produtos)}.'
        )
