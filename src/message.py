"""
    This class contains the generated text messges between 
    ships, as well as command messages from network controllers
    to ships in their networks.
"""
from enum import Enum
from dataclasses import dataclass

class MessageType(Enum):
    """
    message type for the ship communication
    - message: pass the message
    - change_speed: change the speed of the ship
    - stop: stop the ship
    - fix: fix the ship
    """
    message: 1
    change_speed: 2
    stop: 3
    fix: 4

@dataclass
class Message:
    message_type: MessageType
    contents: str
    source: str
    destination: str
