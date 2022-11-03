import string
from models import User


def get_user_by_username(username) -> User:
    return User.query.filter_by(username=username).first()

def create_user(session,username, password, salt) -> User:
    new_user = User(username=username, password=password, salt=salt)
    session.add(new_user)
    session.flush()
    return new_user