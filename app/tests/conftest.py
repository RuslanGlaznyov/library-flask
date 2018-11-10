import os
import tempfile

import pytest
from app.run_app import create_app


@pytest.yield_fixture(scope='session')
def app():
    # db_fd, db_path =
    test_config = {
        'DEBUG': False,
        'TESTING': True,
    }

    _app = create_app(test_config=test_config)

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    yield app.test_client()
