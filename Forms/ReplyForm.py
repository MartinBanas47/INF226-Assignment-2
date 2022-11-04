from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import InputRequired, Length


class CreateReplyForm(FlaskForm):
    message = TextAreaField('Reply', validators=[InputRequired(), Length(max=200)])
