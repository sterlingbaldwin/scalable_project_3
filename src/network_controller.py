"""
    This is a management class for the network controlers, it holds a record 
    of all the controllers and takes care of routing messages from ships 
    to their appropriate controller and vis-versa.
"""

import requests
import pandas as pd
import numpy as np
import datetime
import re
from datetime import datetime
import json

from ship import ship
from message import Message
import requests

class NetworkController(ship):
    def __init__(self, shipID:str, simulator_address: str, shipPort: str, host:str = "127.0.0.1", port: str = "3000", size:int = 100_000, messages: list = []) -> None:
        super().__init__(shipID, simulator_address, shipPort, messages)
        self.messages = pd.DataFrame(columns=['source_id', 'destination_id', 'message'])
        self.host = host
        self.port = port
        self._app = None
        self._world_size = size
        self._time = datetime.now()
        self._ships = []

    def get_network(self):
        """[summary]
        
            Get the network 
        """
        session = requests.Session()
        session.trust_env = False
        request = session.prepare_request(requests.Request('GET', f"{self._simulator_address}/{self._simulator_port}/get_network", params={
            "controller_id": self.shipID
        }))
        res = requests.send(request)
        self._ships = res.ships

    def message_carry_request(self, message: Message):
        """[summary]

            Pass the source and destination to the server to get the shortest distance
            then send the message
        """
        source_id = message.source
        destination_id = message.destination
        contents = message.contents
        session = requests.Session()
        session.trust_env = False
        request = session.prepare_request(requests.Request('GET', f"{self._simulator_address}/{self._simulator_port}/send_message", params={
            "source_id": source_id,
            "destination_id": destination_id,
            "contents": contents
        }))
        res = requests.send(request)
        return res
        

    