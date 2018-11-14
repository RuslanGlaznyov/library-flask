from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class PassForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
