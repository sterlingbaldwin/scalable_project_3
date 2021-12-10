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

from ship import Ship
from message import Message
import requests

class NetworkController(Ship):
    def __init__(self, shipID:str, simulator_address: str, shipPort: str, host:str = "127.0.0.1", port: str = "3000", size:int = 100_000, messages: list = [], entity_server:str = "127.0.0.1") -> None:
        super().__init__(shipID, simulator_address, shipPort)
        self.messages = pd.DataFrame(columns=['source_id', 'destination_id', 'message'])
        self.host = host
        self.port = port
        self._app = None
        self._world_size = size
        self._time = datetime.now()
        self._entity_server = entity_server
        self._network_ships = []

    def get_network(self):
        """
        
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
        """

            Pass source and dest to the controller manager to see if in the same network
        """
        source_id = message.source
        destination_id = message.destination
        contents = message.contents
        message_type = message.message_type
        session = requests.Session()
        session.trust_env = False
        # send request to the network manager to see if in the same network
        request = session.prepare_request(requests.Request('GET', f"{self._simulator_address}/{self._simulator_port}/message_in_range", params={
            "source_id": source_id,
            "destination_id": destination_id,
            "contents": contents
        }))
        res = session.send(request)
        if (res.text == "True"):
            self.messages.loc[self.messages.shape[0]] = {
                "source_id": source_id,
                "destination_id": destination_id,
                "message": contents
            }
        return bool(res.text)


    def message_manager(self, message: Message):
        """

            Pass source and dest to the controller manager to see if in the same network
        """
        source_id = message.source
        destination_id = message.destination
        contents = message.contents
        session = requests.Session()
        session.trust_env = False
        # send message to the entity manager so that it can be forwarded to the intended Entity
        if destination_id is None:
            for entity in self._network_ships:
                request = session.prepare_request(requests.Request('GET', url=f"{self._entity_server}/controller_message", params={
                    "source_id": source_id,
                    "destination_id": entity,
                    "contents": contents
                }))
                res = session.send(request)
                if res.status_code != 200:
                    return f"message Not sent to ship {entity}"
        else:
            request = session.prepare_request(requests.Request('GET', url=f"{self._entity_server}/controller_message", params={
                    "source_id": source_id,
                    "destination_id": destination_id,
                    "contents": contents
                }))
            res = session.send(request)
            if res.status_code != 200:
                return f"message Not sent to ship {destination_id}"


    def add_ships(self, new_ships: list):
        """Add a list of ships to a the controller's entity network list

        Args:
            new_ships (list): List of the ship_ids
        """
        self._network_ships += new_ships
    
    def remove_ship(self, ship_id:str):
        """Remove a ship_id of the controller's entity network list

        Args:
            ship_id (str): ID of the ship that is to be removed from the network
        """
        self._network_ships.remove(ship_id)
    
    def ship_in_network(self, ship_id: str):
        """Check if the ship is part of the controller's network.

        Args:
            ship_id (str): Id of the ship that needs to be verified

        Returns:
            [bool]: Check if the ship is part of the controller's network
        """
        return ship_id in self._network_ships
