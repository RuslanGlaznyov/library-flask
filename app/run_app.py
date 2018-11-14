from flask import Flask, render_template

from app.blueprints.login.views import login
from app.blueprints.library.views import library
from app.blueprints.stat.views import stat
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
    app.register_blueprint(stat, url_prefix='/stat')
    extensions(app)
    return app


def extensions(app):
    db.init_app(app)
    debug_toolbar.init_app(app)


flask_app = create_app()


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@flask_app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500


@flask_app.errorhandler(401)
def page_not_found(e):
    return render_template('errors/401.html'), 404


@flask_app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Book': Book, 'Genre': Genre}


if flask_app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('error.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    flask_app.logger.addHandler(file_handler)

if __name__ == '__main__':
    flask_app.run()
