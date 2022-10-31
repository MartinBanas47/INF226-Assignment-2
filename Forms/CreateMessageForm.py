from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators
from wtforms.validators import InputRequired, Length


class CreateMessageForm(FlaskForm):
    receiver = StringField('Receiver',
                           validators=[validators.Regexp(r'[A-Za-z0-9]+'), InputRequired(), Length(max=20)])
    message = TextAreaField('Message', validators=[InputRequired(), Length(max=200)])
