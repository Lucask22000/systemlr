"""
Gera QR Codes para todas as mesas com token, salvando em ./qrcodes/.
Uso:
    python scripts/generate_qrcodes.py --base-url http://localhost:5000
"""
import argparse
import os

import qrcode
from flask import Flask

from app import app, db
from models import Mesa


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://localhost:5000', help='Base da aplicação (sem barra final)')
    parser.add_argument('--out-dir', default='qrcodes', help='Diretório de saída')
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    with app.app_context():
        mesas = Mesa.query.all()
        for mesa in mesas:
            if not mesa.qr_token:
                continue
            url = f"{args.base_url}/m/{mesa.qr_token}"
            img = qrcode.make(url)
            filename = os.path.join(args.out_dir, f"mesa_{mesa.numero}.png")
            img.save(filename)
            print(f"QR gerado para mesa {mesa.numero}: {filename}")


if __name__ == '__main__':
    main()
