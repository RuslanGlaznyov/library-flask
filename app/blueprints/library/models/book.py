from app.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class Book(ResourceMixin, db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)

    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    title = db.Column(db.String(128))
    desc = db.Column(db.String(512))
    status = db.Column(db.Enum('Save', 'In progress', 'Save', 'Done'), server_default='Save')
    rating = db.Column(db.Integer)
    icon_path = db.Column(db.String(128))
    book_path = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)

    def __repr__(self):
        return '<Book {}>'.format(self.title)
