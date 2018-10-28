from flask import Blueprint, render_template, redirect, url_for
from app.blueprints.library.models.book import Book
from app.blueprints.library.forms import NewBook
from lib.util_file_form_storage import save_file
library = Blueprint('library', __name__, template_folder='templates')


@library.route('/')
def home():
    # all_book = Book.query.all()
    all_book =[]
    return render_template('home.html', books=all_book)


@library.route('/detail')
def detail():
    return render_template('detail.html')


@library.route('/new', methods=['GET', 'POST'])
def new():
    form = NewBook()
    if form.validate_on_submit():
        genre = form.genre.data
        print(genre)
        # icon_path = save_file(form.icon.data, 'icon')
        # book_path = save_file(form.book.data, )
        # book = Book(
        #     title=form.title.data,
        #     desc=form.desc.data,
        #     icon_path=icon_path,
        #     book_path=
        # )
        # book.save()
        return redirect(url_for('library.home'))
    return render_template('new.html', form=form)
