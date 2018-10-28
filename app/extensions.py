from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
debug_toolbar = DebugToolbarExtension()
