from sqlalchemy import or_

from app.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class Book(ResourceMixin, db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)

    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))

    notes = db.relationship('Note', backref='book', lazy='dynamic')

    title = db.Column(db.String(128))
    desc = db.Column(db.String(512))
    status = db.Column(db.Enum('Todo', 'In progress', 'Save', 'Done'), server_default='Save')
    rating = db.Column(db.Integer(), default=0)
    icon_path = db.Column(db.String(128))
    book_path = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)

    def __repr__(self):
        return '<Book {}>'.format(self.title)

    @classmethod
    def search(cls, query):
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (Book.title.ilike(search_query),
                        Book.desc.ilike(search_query))

        return or_(*search_chain)


class Note(ResourceMixin, db.Model):
    __tablename__ = 'Note'

    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    text = db.Column(db.Text)

    def __init__(self, **kwargs):
        super(Note, self).__init__(**kwargs)

    def __str__(self):
        return self.title

    def __repr__(self):
        return 'Text: {}'.format(self.text)


class Genre(ResourceMixin, db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)

    books = db.relationship('Book', backref='genre', lazy='dynamic')

    title = db.Column(db.String(128), unique=True)

    def __init__(self, **kwargs):
        super(Genre, self).__init__(**kwargs)

    def __str__(self):
        return self.title

    def __repr__(self):
        return 'Genre: {}'.format(self.title)
