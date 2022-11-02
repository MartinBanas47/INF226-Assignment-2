from models import Participant


def add_participant(session, sender_id, receiver_id, message_id) -> Participant:
    new_participant = Participant(senderId=sender_id,
                                  receiverId=receiver_id,
                                  messageId=message_id)
    session.add(new_participant)
    session.flush()
    return new_participant
