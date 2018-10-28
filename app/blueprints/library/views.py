from flask import Blueprint, render_template, redirect, url_for, Response
from app.blueprints.library.models import Book, Genre, Note
from app.blueprints.library.forms import NewBook, NoteForm
from lib.util_file_form_storage import save_file

library = Blueprint('library', __name__, template_folder='templates')


@library.route('/')
def home():
    all_book = Book.query.all()
    all_genre = Genre.query.all()
    return render_template('home.html', books=all_book, genre=all_genre)


@library.route('/detail/<genre>/<int:book_id>/<title>', methods=['GET', 'POST'])
def detail(genre, book_id, title):
    form = NoteForm()
    current_book = Book.query.get(book_id)
    if form.validate_on_submit():
        note = Note(text=str(form.text.data), book_id=current_book.id)
        note.save()
        return redirect(url_for('library.detail', genre=genre, book_id=book_id, title=title))
    return render_template('detail.html', book=current_book, form=form)


@library.route('/new', methods=['GET', 'POST'])
def new():
    form = NewBook()
    if form.validate_on_submit():
        genre = Genre.query.filter_by(title=str(form.genre.data)).first_or_404()
        icon_path = save_file(form.icon.data, 'icon')
        book_path = save_file(form.book.data, genre.title)
        book = Book(
            title=form.title.data,
            desc=form.desc.data,
            icon_path=icon_path,
            book_path=book_path,
            genre=genre
        )
        book.save()
        return redirect(url_for('library.home'))
    return render_template('new.html', form=form)


@library.route('/change-status/<genre>/<int:book_id>/<title>/<status>')
def change_status(**kwargs):
    book = Book.query.get(kwargs.get('book_id'))
    book.status = kwargs.get('status')
    book.save()
    return redirect(url_for('library.detail', **kwargs))


@library.route('/delete-post/<genre>/<int:book_id>/<title>/<int:post_id>', methods=['POST'])
def delete_post(**kwargs):
    book = Note.query.get(kwargs.get('post_id'))
    book.delete()
    return redirect(url_for('library.detail', **kwargs))
