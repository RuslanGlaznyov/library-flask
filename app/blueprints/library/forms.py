from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.blueprints.library.models.genre import Genre


def get_genres():
    genres = Genre.query.all()
    choices = []
    counter = 0
    for genre in genres:
        counter += 1
        choices.append((counter, genre))

    return choices


class NewBook(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    desc = TextAreaField('Description', validators=[Length(1, 2054)])
    icon = FileField('Icon upload', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'svg'], 'Images only!')
    ])
    book = FileField('Book upload', validators=[
        FileRequired(),
        FileAllowed(['epub', 'fb2', 'pdf', 'txt'], 'Books only!')
    ])
    genre = SelectField(u'Genre', choices=get_genres())
