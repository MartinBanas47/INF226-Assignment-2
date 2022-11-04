import string
from datetime import datetime

from sqlalchemy import or_

from models import Message, Participant, User


def create_message(session, message: string, replying_to_message_id=None) -> Message:
    new_message = Message(message=message,
                          date=datetime.today())
    if replying_to_message_id is not None:
        new_message.replyToId = replying_to_message_id
    session.add(new_message)
    session.flush()
    return new_message


def get_messages_for_user(user_id):
    return Participant.query.filter_by(receiverId=user_id) \
        .join(Message, Participant.messageId == Message.id) \
        .join(User, User.id == Participant.senderId) \
        .add_columns(Participant.receiverId, User.username, Message.id, Message.message, Message.date).all()


def get_message_with_participants(message_id, current_user_id):
    return Message.query.filter_by(id=message_id).join(Participant, Participant.messageId == Message.id) \
        .filter(or_(Participant.receiverId == current_user_id, Participant.senderId == current_user_id)) \
        .join(User, User.id == Participant.senderId) \
        .add_columns(Participant.receiverId, Participant.senderId,
                     User.username, Message.id, Message.message, Message.date, Message.replyToId) \
        .first()
