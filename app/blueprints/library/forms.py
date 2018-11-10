from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.blueprints.library.models import Genre


def unique_genre_validate(form, field):
    if Genre.query.filter_by(title=field.data).first():
        raise ValidationError('Genre is already exist')


class NewBook(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    desc = TextAreaField('Description', validators=[Length(0, 2054)])
    icon = FileField('Icon upload', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'svg'], 'Images only!')
    ])
    book = FileField('Book upload', validators=[
        FileRequired(),
        FileAllowed(['epub', 'fb2', 'pdf', 'txt'], 'Books only!')
    ])
    genre = QuerySelectField(query_factory=lambda: Genre.query.all())
    new_genre = StringField('New genre', validators=[Length(0, 128), unique_genre_validate])


class NoteForm(FlaskForm):
    text = TextAreaField('Note', validators=[Length(1, 2054)])


class SearchForm(FlaskForm):
    q = StringField('Search terms', [Optional(), Length(1, 256)])
