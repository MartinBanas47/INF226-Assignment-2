from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[validators.Regexp(r'[A-Za-z0-9]+'), InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password',
                             validators=[validators.Regexp('(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9]).{7,20}',
                                                           message="Password has to contain"
                                                                   " 1 upper case character,"
                                                                   "1 number and 1 special character"),
                                         InputRequired(), Length(min=7, max=20),
                                         ])
