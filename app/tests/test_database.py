from app.run_app import db
from app.blueprints.library.models import Book, Genre
from app.run_app import flask_app

# flask_app.app_context().push()


def delete_db():
    genres = Genre.query.all()
    for genre in genres:
        genre.delete()

    books = Book.query.all()
    for book in books:
        book.delete()


if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()
        delete_db()
        title_genre_list = ['One', 'Two', 'Tree', 'For']
        for title in title_genre_list:
            gen_db = Genre(title=title)
            gen_db.save()
