import string
from datetime import datetime


class MessageDto:
    def __init__(self,
                 message_id: int,
                 sender_id: int,
                 sender_username: string,
                 timestamp: datetime,
                 message: string
                 ) -> None:
        self.message_id = message_id
        self.message = message
        self.timestamp = timestamp
        self.sender_id = sender_id
        self.sender_username = sender_username
