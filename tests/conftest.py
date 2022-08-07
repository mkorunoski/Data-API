import os
import pytest
import tempfile
from dialogs import create_app
from dialogs.db import init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'REDIS_DATABASE': 15,
        'SQLITE_DATABASE': db_path,
    })

    with app.app_context():
        fname = os.path.join(os.path.dirname(__file__), 'data.sql')
        init_db(fname)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()