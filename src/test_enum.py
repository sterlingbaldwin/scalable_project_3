from enum import Enum

class MessageType(Enum):
    """
    message type for the ship communication
    - message: pass the message
    - change_speed: change the speed of the ship
    - stop: stop the ship
    - fix: fix the ship
    """
    message = 1
    change_speed = 2
    stop = 3
    fix = 4

print(MessageType.message.value)