from flask import Config
import os
# '..'
basedir = os.environ.get('PYTHONPATH')


class DevelopmentConfig(Config):
    basedir = basedir.split(':')[1]
    DEBUG = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')
    UPLOAD_PATH = 'app/static/uploads'
    FILE_SPLIT = 'KiiiiiK'
    DEBUG_TB_INTERCEPT_REDIRECTS = False


