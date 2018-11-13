from flask import Blueprint, render_template
from app.blueprints.library.models import Book, Genre, Note
from config.settings import DevelopmentConfig
from app.blueprints.login.login_required import login_required

stat = Blueprint('stat', __name__, template_folder='templates')


@stat.route('/')
@login_required()
def index():
    total_book = len(Book.query.all())

    status_list = DevelopmentConfig.STATUS
    status_list_count = [len(Book.query.filter_by(status=status).all()) for status in status_list]
    status_zip = zip(status_list, status_list_count)

    genres = Genre.query.all()
    genre_list_count = [len(Book.query.filter_by(genre=genre).all()) for genre in genres]
    genre_zip = zip(genres, genre_list_count)

    rating_count = range(0, 6)
    rating_list = [len(Book.query.filter_by(rating=star).all()) for star in rating_count]
    rating_zip = zip(rating_count, rating_list)

    return render_template('stat.html', status_zip=status_zip, total_book=total_book,
                           genre_zip=genre_zip, rating_zip=rating_zip)
