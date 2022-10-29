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


'''Table for messages'''
class Message(db.Model):
    __tablename__ = "Message"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=True)
    sender = db.Column(db.Integer, ForeignKey("User.id"))
    receiver = db.Column(db.Integer, ForeignKey("User.id"))
    date = db.Column(db.Date)
