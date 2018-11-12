import os

import pytest

from app.blueprints.library.models import Book, Genre, Note
from app.run_app import create_app
from app.extensions import db as _db
from config.settings import DevelopmentConfig
from lib.util_file_form_storage import save_file


@pytest.yield_fixture(scope='session')
def app():

    test_config = {
        'DEBUG': False,
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://'
    }

    _app = create_app(test_config=test_config)

    with _app.app_context():
        _db.create_all()
        # icon_path = os.path.abspath(DevelopmentConfig.BASEDIR+'/app/tests/fake_data/fake_icon.jpg')
        # book_path = os.path.abspath(DevelopmentConfig.BASEDIR+'/app/tests/fake_data/fake_book.epub')

        book = {
            'title': 'test',
            'desc': 'test',
            'status': 'Todo',
            'rating': 0,
            'icon_path': 'test/path',
            'book_path': 'test/path'
        }
        # save_file(icon_path, 'icon', fake_file=True)
        # save_file(book_path, 'test', fake_file=True)

        genre = {
            'title': 'test'
        }

        note = {
            'text': 'test',
        }

        _db.session.add(Book(**book))
        _db.session.add(Genre(**genre))
        _db.session.add(Note(**note))
        Note.book_id = 1
        Book.genre_id = 1
        _db.session.commit()
        yield _app
        _db.session.remove()  # looks like db.session.close() would work as well
        _db.drop_all()


@pytest.yield_fixture(scope='function')
def client(app):
    yield app.test_client()

