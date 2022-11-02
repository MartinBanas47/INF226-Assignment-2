import string
from datetime import datetime

from models import Message, Participant, User


def create_message(session, message: string) -> Message:
    new_message = Message(message=message,
                          date=datetime.today())
    session.add(new_message)
    session.flush()
    return new_message


def get_messages_for_user(user_id: int):
    return Participant.query.filter_by(receiverId=user_id) \
        .join(Message, Participant.messageId == Message.id) \
        .join(User, User.id == Participant.senderId) \
        .add_columns(Participant.receiverId, User.username, Message.id, Message.message, Message.date).all()
