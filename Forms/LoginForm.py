from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[validators.Regexp(r'[A-Za-z0-9]+'), InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=7, max=80)])
