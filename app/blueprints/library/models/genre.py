from app.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class Genre(ResourceMixin, db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)

    books = db.relationship("Book", backref="genre")

    genre = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Genre, self).__init__(**kwargs)

    def __repr__(self):
        return '<Genre {}>'.format(self.title)
