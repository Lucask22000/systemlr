from contextlib import contextmanager

from models import db


@contextmanager
def atomic_transaction(session=None):
    session = session or db.session
    with session.begin_nested():
        yield session
