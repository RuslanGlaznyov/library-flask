from flask import Flask

from app.blueprints.login.views import login
from app.blueprints.library.views import library
from app.extensions import debug_toolbar
from app.extensions import db
from app.blueprints.library.models import Book, Genre


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.settings.DevelopmentConfig')
    if test_config:
        app.config.update(test_config)

    app.register_blueprint(login)
    app.register_blueprint(library, url_prefix='/library')
    extensions(app)
    return app


def extensions(app):
    db.init_app(app)
    debug_toolbar.init_app(app)


flask_app = create_app()

with flask_app.app_context():
    # db.drop_all()
    db.create_all()


@flask_app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Book': Book, 'Genre': Genre}


if __name__ == '__main__':
    flask_app.run()
