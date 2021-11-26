from enum import Enum
from dataclasses import dataclass

class MessageType(Enum):
    syn = 1
    ack = 2
    mail = 3
    carry_request = 4
    carry_response = 5


@dataclass
class Message:
    message_type: MessageType
    contents: str
    source: str
    destination: str
