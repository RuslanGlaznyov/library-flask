import os
import random
from time import sleep

from app.run_app import db
from app.blueprints.library.models import Book, Genre
from app.run_app import flask_app

from faker import Faker

from lib.util_file_form_storage import save_fake_file, save_file

fake = Faker()

status_tuple = ('Todo', 'In progress', 'Save', 'Done')


def create_fake_genres(genre_number):
    title_genre_list = fake.words(nb=genre_number, ext_word_list=None, unique=True)
    for title in title_genre_list:
        gen_db = Genre(title=title)
        gen_db.save()


def create_fake_books(genre_number, books_qt):
    icon_path = os.path.abspath('fake_data/fake_icon.jpg')
    book_path = os.path.abspath('fake_data/fake_book.epub')
    for i in range(books_qt):
        genre_id = random.randint(1, genre_number)
        book = Book(title=fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                    desc=fake.text(max_nb_chars=100, ext_word_list=None),
                    status=random.choice(status_tuple),
                    rating=random.randint(0, 5),
                    genre_id=genre_id,
                    icon_path=save_file(icon_path, 'icon', fake_file=True),
                    book_path=save_file(book_path, Genre.query.get(genre_id).title, fake_file=True)
                    )
        book.save()


def create_fake_database(genres_qt=3, books_qt=50):
    create_fake_genres(genres_qt)
    create_fake_books(genres_qt, books_qt)


if __name__ == '__main__':
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        create_fake_database()
