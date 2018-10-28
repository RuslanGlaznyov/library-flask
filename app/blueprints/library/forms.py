from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.blueprints.library.models import Genre


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
    genre = QuerySelectField(query_factory=lambda: Genre.query.all())


class NoteForm(FlaskForm):
    text = TextAreaField('Note', validators=[Length(0, 2054)])