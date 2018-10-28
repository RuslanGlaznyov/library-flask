from flask import Config
import os

basedir = os.path.abspath(os.path.dirname('..'))


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')
    UPLOAD_PATH = 'app/static/uploads'
    FILE_SPLIT = 'KiiiiiK'


