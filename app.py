from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '123456789'
db = SQLAlchemy(app)
Bootstrap4(app)



@app.route('/')
def index():
    return render_template('index.html')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=7, max=80)])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>'+ 'jebko' +'</h1>'

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
