import datetime
import bcrypt

from flask import Flask, render_template, redirect, url_for, abort
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from Dto.MessageDto import MessageDto
from Forms.CreateMessageForm import CreateMessageForm
from Forms.LoginForm import LoginForm
from Forms.RegisterForm import RegisterForm
from models import User, Message
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '123456789'
app.app_context().push()
db.init_app(app)
db.create_all()
Bootstrap4(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            checking_password = bcrypt.hashpw(bytes(form.password.data, 'utf-8'), user.salt)
            if checking_password == user.password:
                login_user(user)
                return redirect(url_for('messages'))
        return render_template('login.html', form=form, mess='Something failed')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes(form.password.data, 'utf-8'), salt)
        new_user = User(username=form.username.data, password=hashed_password, salt=salt)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def createMessage():
    form = CreateMessageForm()
    if form.is_submitted():
        try:
            receiver = User.query.filter_by(username=form.receiver.data).first()
            new_message = Message(receiver=receiver.id,
                                  message=form.message.data,
                                  sender=current_user.id,
                                  date=datetime.date.today())
            db.session.add(new_message)
            db.session.commit()
            return render_template('createMessage.html', form=CreateMessageForm(formdata=None),
                                   error_messsage='Message was sent')
        except AttributeError:
            return render_template('createMessage.html', form=form, error_messsage='Something went wrong')
    return render_template('createMessage.html', form=form)


@app.route('/messages')
@login_required
def messages():
    messages_db = User.query \
        .join(Message, User.id == Message.sender).add_columns(User.id, User.username, Message.id, Message.date,
                                                              Message.message, Message.receiver) \
        .filter_by(receiver=current_user.id). \
        all()
    messages_list = []
    for message in messages_db:
        messages_list.append(MessageDto(
            message_id=message.id,
            sender_username=message.username,
            timestamp=message.date,
            message=message.message
        ))
    return render_template('messages.html', messages=messages_list, len=len(messages_list))


@app.route('/message/<int:message_id>')
@login_required
def message(message_id):
    message_db = User.query \
        .join(Message, User.id == Message.sender).add_columns(User.username, Message.id, Message.date, Message.message,
                                                              Message.receiver) \
        .filter_by(id=message_id) \
        .first()
    if message_db.receiver != current_user.id:
        abort(404)
    message = MessageDto(
        message_id=message_db.id,
        sender_username=message_db.username,
        timestamp=message_db.date,
        message=message_db.message
    )
    return render_template('message.html', message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
