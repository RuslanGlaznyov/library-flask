from flask import Config
import os
# '..'
BASEDIR = os.environ.get('PYTHONPATH')


class DevelopmentConfig(Config):
    try:
        BASEDIR = BASEDIR.split(':')[1]
    except Exception:
        BASEDIR = BASEDIR

    DEBUG = os.environ.get('DEBUG') or True
    PASSWORD = 'pass'
    STATUS = ['Done', 'Todo', 'In progress', 'Save']
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # SERVER_NAME = 'localhost.localdomain:5000'
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'data.db')

    UPLOAD_PATH = 'app/static/uploads'
    DOWNLOAD_PATH = 'app/static'
    FILE_SPLIT = 'KiiiiiK'
    DEBUG_TB_INTERCEPT_REDIRECTS = False


