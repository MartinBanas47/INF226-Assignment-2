from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

'''Table for users'''


class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    salt = db.Column(db.String(30), nullable=False)


'''Table for messages'''


class Message(db.Model):
    __tablename__ = "Message"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=True)
    date = db.Column(db.Date)


'''Table for receivers and senders'''


class Participant(db.Model):
    __tablename__ = "Participant"
    id = db.Column(db.Integer, primary_key=True)
    senderId = db.Column(db.Integer, ForeignKey("User.id"))
    receiverId = db.Column(db.Integer, ForeignKey("User.id"))
    messageId = db.Column(db.Integer, ForeignKey("Message.id"))
