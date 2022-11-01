import datetime

import bcrypt
from flask import Flask, render_template, redirect, url_for, abort
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from Dto.MessageDto import MessageDto
from Forms.CreateMessageForm import CreateMessageForm
from Forms.LoginForm import LoginForm
from Forms.RegisterForm import RegisterForm
from Forms.ReplyForm import CreateReplyForm
from models import User, Message, Participant
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
            if (';' in form.receiver.data):
                receivers = form.receiver.data.split(';')

                try:

                        new_message = Message(message=form.message.data,
                                              date=datetime.date.today())
                        db.session.add(new_message)
                        db.session.flush()
                        for x in receivers:
                            receiver = User.query.filter_by(username=x).first()
                            new_participants = Participant(senderId=current_user.id,
                                                       receiverId=receiver.id,
                                                       messageId=new_message.id)
                            db.session.add(new_participants)
                            db.session.commit()

                except AttributeError:
                                pass
                return render_template('createMessage.html', form=CreateMessageForm(formdata=None),
                                       error_messsage='Message was sent')
            else:
                receiver = User.query.filter_by(username=form.receiver.data).first()
                new_message = Message(message=form.message.data,
                                      date=datetime.date.today())
                db.session.add(new_message)
                db.session.flush()
                new_participants = Participant(senderId=current_user.id,
                                               receiverId=receiver.id,
                                               messageId=new_message.id)
                db.session.add(new_participants)
                db.session.commit()
                return render_template('createMessage.html', form=CreateMessageForm(formdata=None),
                                       error_messsage='Message was sent')
        except AttributeError:
            return render_template('createMessage.html', form=form, error_messsage='Something went wrong')
    return render_template('createMessage.html', form=form)


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    try:
        messages_db = Participant.query.filter_by(
            receiverId=current_user.id) \
            .join(Message, Participant.messageId == Message.id).join(User, User.id == Participant.senderId)\
            .add_columns(Participant.receiverId,User.username,Message.id, Message.message, Message.date).all()
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
    message_db = Message.query.filter_by(id=message_id).join(Participant, Participant.messageId == Message.id).join(
        User, User.id == Participant.senderId).add_columns(Participant.receiverId,Participant.senderId,User.username,Message.id, Message.message, Message.date).first()
    print(message_db)

    if (message_db.receiverId != current_user.id) and (message_db.senderId != current_user.id):
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
    app.run(debug=True)
