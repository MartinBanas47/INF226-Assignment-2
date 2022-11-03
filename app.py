import datetime

import bcrypt
from flask import Flask, render_template, redirect, url_for, abort
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from logging import FileHandler, WARNING

from Dto.MessageDto import MessageDto
from Forms.CreateMessageForm import CreateMessageForm
from Forms.LoginForm import LoginForm
from Forms.RegisterForm import RegisterForm
from Forms.ReplyForm import CreateReplyForm
from models import User, Message, Participant
from models import db
from Repository import UserRepository, MessageRepository, ParticipantRepository
from Utility import ValidationCheck

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '123456789'
app.config['SESSION_COOKIE_SAMESITE'] = "Strict"
app.app_context().push()
db.init_app(app)
db.create_all()
Bootstrap4(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
file_handler = FileHandler("instance/errorlog.txt")
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():

        if not ValidationCheck.username_valid(form.username.data):
            return render_template('login.html', form=form, mess='Username can contain only alphanumeric characters')
        if not ValidationCheck.password_valid(form.password.data):
            return render_template('login.html', form=form, mess='Password can not contain whitespaces')

        user = UserRepository.get_user_by_username(form.username.data)
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

    if form.is_submitted():

        if not ValidationCheck.username_valid(form.username.data):
            return render_template('register.html', form=form,
                                   error_message='Username can contain only alphanumeric characters')
        if not ValidationCheck.password_valid(form.password.data):
            return render_template('register.html', form=form,
                                   error_message='Password can not contain whitespaces')

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes(form.password.data, 'utf-8'), salt)
        try:
            UserRepository.create_user(db.session, form.username.data, hashed_password, salt)
            db.session.commit()
        except IntegrityError as e:
            if "UNIQUE constraint failed: User.username" in e.args[0]:
                return render_template('register.html', form=form,
                                       error_message='Username is already used')
            return render_template('register.html', form=form, error_mesage="Something went wrong")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def create_message():
    form = CreateMessageForm()
    if form.is_submitted():
        if not ValidationCheck.username_group_valid(form.receiver.data):
            return render_template('createMessage.html', form=form,
                                   error_message='Username can contain only alphanumeric characters')

        receivers = form.receiver.data.split(';')
        new_message = MessageRepository.create_message(db.session, form.message.data)
        for receiver in receivers:
            new_receiver = UserRepository.get_user_by_username(receiver)
            if new_receiver is None:
                return render_template('createMessage.html', form=form, error_message='Non existing user included')
            ParticipantRepository.add_participant(db.session, current_user.id, new_receiver.id, new_message.id)
        db.session.commit()
        return render_template('createMessage.html', form=CreateMessageForm(formdata=None),
                               error_message='Message was sent')
    return render_template('createMessage.html', form=form)


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    try:
        messages_db = MessageRepository.get_messages_for_user(current_user.id)
        messages_list = []
        for message in messages_db:
            messages_list.append(MessageDto(
                message_id=message.id,
                sender_username=message.username,
                timestamp=message.date,
                message=message.message
            ))

        return render_template('messages.html', messageexists=True, messages=messages_list, len=len(messages_list))
    except AttributeError:
        return render_template('messages.html', messageexists=False)


@app.route('/message/<int:message_id>', methods=['GET', 'POST'])
@login_required
def message(message_id):
    form = CreateReplyForm()
    message_db = Message.query.filter_by(id=message_id).join(Participant, Participant.messageId == Message.id)\
        .filter_by(receiverId=current_user.id).join(
        User, User.id == Participant.senderId).add_columns(Participant.receiverId, Participant.senderId, User.username,
                                                           Message.id, Message.message, Message.date).first()

    if message_db.receiverId != current_user.id:
        abort(404)
    message = MessageDto(
        message_id=message_db.id,
        sender_username=message_db.username,
        timestamp=message_db.date,
        message=message_db.message
    )

    if form.is_submitted():
        try:
            new_message = Message(message=form.message.data,
                                  date=datetime.date.today(),
                                  replyToId=message_id
                                  )
            db.session.add(new_message)
            db.session.flush()
            group_query = Participant.query.filter_by(messageId=message_id).filter(
                Participant.senderId != current_user.id).add_columns(Participant.receiverId, Participant.senderId).all()
            sender_id = None
            for x in group_query:
                if x.senderId != current_user.id:
                    sender_id = x.senderId
                if x.receiverId != current_user.id:
                    new_participants = Participant(senderId=current_user.id,
                                                   receiverId=x.receiverId,
                                                   messageId=new_message.id)
                    db.session.add(new_participants)
                    db.session.flush()
            new_participants = Participant(senderId=current_user.id,
                                           receiverId=sender_id,
                                           messageId=new_message.id)
            db.session.add(new_participants)
            db.session.flush()
            db.session.commit()
            return redirect(url_for('messages'))
        except AttributeError:
            return render_template('message.html', meessage=message, form=form, error_messsage='Something went wrong')

    return render_template('message.html', message=message, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
