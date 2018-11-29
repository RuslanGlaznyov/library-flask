from flask import Blueprint, render_template, redirect, url_for, Response, request, send_file, abort, flash
from flask_wtf.file import FileAllowed

from app.blueprints.library.models import Book, Genre, Note
from app.blueprints.library.forms import BookForm, NoteForm
from lib.util_file_form_storage import save_file, delete_file
from sqlalchemy import text
from app.blueprints.library.forms import SearchForm
from config import settings
from app.blueprints.login.login_required import login_required
import lib.util_google_drive as gd

library = Blueprint('library', __name__, template_folder='templates')


@library.route('/', defaults={'page': 1})
@library.route('/page/<int:page>')
@login_required()
def index(page):
    # return 1/0
    search_form = SearchForm()
    all_genre = Genre.query.all()

    book_query = Book.query

    sort_by = Book.sort_by(request.args.get('sort', 'created_on') or 'created_on',
                           request.args.get('direction', 'desc') or 'desc')

    sort_by_genre = request.args.get('genreSort', '')
    sort_by_status = request.args.get('status', '')

    order_values = '{0} {1} '.format(sort_by[0], sort_by[1])

    if sort_by_genre in [str(value) for value in Genre.query.all()]:
        book_query = book_query.filter(Book.genre.has(title=sort_by_genre))

    if sort_by_status in settings.DevelopmentConfig.STATUS:
        book_query = book_query.filter_by(status=sort_by_status)

    paginate_books = book_query \
        .filter(Book.search(request.args.get('q', ''))) \
        .order_by(text(order_values)) \
        .paginate(page, 5, True)

    return render_template('index.html', form=search_form, books=paginate_books, genre=all_genre)


@library.route('/detail/<genre>/<int:book_id>/<title>', methods=['GET', 'POST'])
@login_required()
def detail(genre, book_id, title):
    form = NoteForm()
    current_book = Book.query.get(book_id)
    if form.validate_on_submit():
        note = Note(text=str(form.text.data), book_id=current_book.id)
        note.save()
        return redirect(url_for('library.detail', genre=genre, book_id=book_id, title=title))
    return render_template('note.html', book=current_book, form=form)


@library.route('/new', methods=['GET', 'POST'])
@login_required()
def new():
    form = BookForm()

    if form.validate_on_submit():
        genre = Genre.query.filter_by(title=str(form.genre.data)).first()
        if form.new_genre.data:
            genre = Genre(title=form.new_genre.data)
            genre.save()
        elif not genre:
            flash('please select or add new genre', 'danger')
            return redirect(url_for('library.new'))

        icon_path = save_file(form.icon.data, 'icon')
        # book_path = save_file(form.book.data, genre.title)
        book_id = gd.save_file(form.book.data, genre.title)

        book = Book(
            title=form.title.data,
            desc=form.desc.data,
            icon_path=icon_path,
            # book_path=book_path,
            drive_id=book_id,
            genre=genre
        )
        book.save()
        flash('New book is added.', 'success')
        return redirect(url_for('library.index'))
    return render_template('new.html', form=form)


@library.route('/edit-book/<genre>/<int:book_id>/<title>', methods=['POST', 'GET'])
@login_required()
def edit_book(genre, book_id, title):
    book = Book.query.get(book_id)
    form = BookForm(obj=book)
    form.icon.validators = [FileAllowed(['jpg', 'png', 'svg'], 'Images only!')]
    form.book.validators = [FileAllowed(['epub', 'fb2', 'pdf', 'txt'], 'Books only!')]
    if form.validate_on_submit():
        # repeat code
        genre = Genre.query.filter_by(title=str(form.genre.data)).first()
        if form.new_genre.data:
            genre = Genre(title=form.new_genre.data)
            genre.save()
        elif not genre:
            flash('please select or add new genre', 'danger')
            return render_template('new.html', form=form, book=book)

        book.title = form.title.data
        book.desc = form.desc.data
        book.genre = genre
        book.save()
        flash('Successfully edited', 'success')
        return redirect(url_for('library.detail', genre=book.genre, title=book.title, book_id=book.id))
    return render_template('new.html', form=form, book=book)


@library.route('/change-status/<genre>/<int:book_id>/<title>/<status>', methods=['POST'])
@login_required()
def change_status(genre, book_id, title, status):
    book = Book.query.get(book_id)
    book.status = status
    book.save()
    return redirect(url_for('library.detail', genre=genre, book_id=book_id, title=title))


@library.route('/delete-note/<genre>/<int:book_id>/<title>/<int:note_id>', methods=['POST'])
@login_required()
def delete_note(genre, book_id, title, note_id):
    note = Note.query.get(note_id)
    note.delete()
    flash('Successfully deleted.', 'success')
    return redirect(url_for('library.detail', genre=genre, book_id=book_id, title=title))


@library.route('/edit_note/<genre>/<int:book_id>/<title>/<int:note_id>', methods=['POST', 'GET'])
@login_required()
def edit_note(genre, book_id, title, note_id):
    note = Note.query.get(note_id)
    book = Book.query.get(book_id)
    form = NoteForm(text=note.text)
    ref = {
        'genre': genre,
        'book_id': book_id,
        'title': title,
        'note_id': note_id
    }
    if form.validate_on_submit():
        note.text = form.text.data
        note.save()
        return redirect(url_for('library.detail', genre=genre, book_id=book_id, title=title))
    return render_template('edit_note.html', book=book, form=form, ref=ref)


@library.route('/set-rating/<genre>/<int:book_id>/<title>/<int:rating>', methods=['POST'])
@login_required()
def set_rating(genre, book_id, title, rating):
    book = Book.query.get(book_id)
    book.rating = rating
    book.save()
    return redirect(url_for('library.detail', genre=genre, book_id=book_id, title=title))


@library.route('/download/<genre>/<int:book_id>/<title>')
@login_required()
def download_book(genre, book_id, title):
    book = Book.query.get(book_id)
    try:
        return send_file('static/' + book.book_path)
    except Exception as e:
        abort(500)


@library.route('/delete_book/<genre>/<int:book_id>/<title>', methods=['POST'])
@login_required()
def delete_book(genre, book_id, title):
    book = Book.query.get(book_id)
    genre = Genre.query.get(book.genre_id)
    delete_file(book.book_path)
    delete_file(book.icon_path)

    if len(genre.books.all()) == 1:
        genre.delete()
    book.delete()
    flash('Successfully deleted.', 'success')
    return redirect(url_for('library.index'))
