"""
    The Ship class are the message curriers and network nodes
    that make up the meat and potatoes of the simulated networks.
    They're contained as records in the EntityManager, and some of
    them become network controllers.
"""

__title__ = "Ships"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

import json
import urllib
import requests
from time import sleep
from typing import Dict
from numpy.random import uniform
from datetime import datetime
import json
from flask import Flask
import numpy as np
import time
import math


class Ship:
    """Ship Class
    Args:
        loc(tuple): x and y cordinate of the Ships
        ship_id(str): the name of the ship
    """
    def __init__(self, ship_id: str, simulator_address: str, port: str) -> None:
        self.__loc = (0.0, 0.0)
        self._id = ship_id
        self._simulator_port = port
        self._simulator_address = simulator_address

        self.__range = 100
        self.__speed = 10
        self.__source = (0, 0)
        self.__destination = (100, 100)
        self.__create_time = time.time()
        self.__itinerary = []
        self.__COMMUNICATION_RANGE = [100, 1000]
        self.__SPEED_RANGE = [100, 1000]
        self._messages = []
        self._network = None
        self._is_controller = False
        pass
    
    @property
    def range(self):
        """Getter fuction for the Communication range property

        Returns:
            int: Communication radius of the ships
        """
        return self.__range
    
    @range.setter
    def range(self, inp: int):
        if self.__COMMUNICATION_RANGE[0] < inp < self.__COMMUNICATION_RANGE[1]:
            self.__range = inp
        else:
            raise ValueError(f'Input communication range of the ships is between {self.__COMMUNICATION_RANGE[0]} & {self.__COMMUNICATION_RANGE[1]}')
    
    @property
    def speed(self):
        return str(self.__speed)
    
    @speed.setter
    def speed(self, inp: float):
        if self.__SPEED_RANGE[0] < inp < self.__SPEED_RANGE[1]:
            self.__speed = inp
        else:
            raise ValueError(f'Speed Range for the ships is between {self.__SPEED_RANGE[0]} & {self.__SPEED_RANGE[1]}')
    
    def update(self, speed: float = 0, range: int = 0):
        """[summary]
        
            update the speed, location, range
        """
        if speed in self.__SPEED_RANGE:
            self.__speed = speed
        if range in self.__COMMUNICATION_RANGE:
            self.__range = range
        # update the location 
        new_loc_x = 0
        new_loc_y = 0
        current_time = time.time()
        angle = math.atan((self.__destination[1] - self.__source[1]) / (self.__destination[0] - self.__source[0]))
        moved_distance = self.__speed * (current_time - self.__create_time)
        if self.__destination[1] > self.__source[1] and self.__destination[0] > self.__source[0]:
            new_loc_x = self.__loc[0] + math.cos(angle) * moved_distance
            new_loc_y = self.__loc[1] + math.sin(angle) * moved_distance
        elif self.__destination[1] < self.__source[1] and self.__destination[0] > self.__source[0]:
            new_loc_x = math.cos(angle) * moved_distance + self.__loc[0]
            new_loc_y = self.__loc[1] - math.sin(angle) * moved_distance
        elif self.__destination[1] > self.__source[1] and self.__destination[0] < self.__source[0]:
            new_loc_x = self.__loc[0] - math.cos(angle) * moved_distance
            new_loc_y = self.__loc[1] + math.sin(angle) * moved_distance
        elif self.__destination[1] < self.__source[1] and self.__destination[0] < self.__source[0]:
            new_loc_x = self.__loc[0] - math.cos(angle) * moved_distance
            new_loc_y = self.__loc[1] - math.sin(angle) * moved_distance
        else:
            pass
        
        self.__loc = (round(new_loc_x, 2), round(new_loc_y, 2))


    @property
    def loc(self):
        """Getter fuction for the location property

        Returns:
            tuple[float]: x and y cordinates of the ships.
        """
        return self.__loc

    @property
    def id(self):
        """Getter function of entity ID function

        Returns:
            [str]: ID of Entity
        """
        return self._id
    
    @loc.setter
    def loc(self, inp: tuple):
        """Setter fuction for the location property

        Args:
            inp (tuple[float]): (x, y) type input
        """
        if len(inp) == 2:
            self.__loc = inp
        else:
            raise ValueError('Input type expected in the form of x,y')
    
    def ping(self):
        """
            request:
                entity_id: The id of the ship
            response:
                res.text: The list-like string contains all the entities in range
        """
        res = self.make_request_to_controller(endpoint="ping", params={})
        data = json.loads(res.text)
        print(f"ping response {data}...")
        return data

    def make_request_to_controller(self, endpoint: str, params: Dict, method:str = 'GET'):
        """
        Make an API request to the simulation server on the redefined port
        Parameters:
            endpoint(str): the path relative the server
            params(Dict): a dict of key,value parameters which will be url encoded
            method(str): either GET or POST for a get request or a post request
        Returns:
            request(requests.Request): the response from the server
        """
        request = None
        url = f"http://{self._simulator_address}:{self._simulator_port}/{endpoint}"
        session = requests.Session()
        session.trust_env = False
        if method == "GET":
            params['entity_id'] = self._id
            if (params):
                url += f"?{urllib.parse.urlencode(params)}"  
            request = session.prepare_request(requests.Request(method, url))
        else:

            request = session.prepare_request(requests.Request(method, url, data=params))
        if (request := session.send(request)).status_code != 200:
            raise ValueError(f"Error from the controller: {request} from request: {url} and response: {request.content.decode('utf-8')}")
        return request
    
    def generate_message(self):
        """
        Generate a new message
        """
        pass

    def make_controller(self, API_ENDPOINT:str) -> bool:
        """Make a request to the controller server to update the ship entity as a network controller

        Args:
            API_ENDPOINT (str): API endpoint for the controller server

        Returns:
            bool: If successfully updated the ship as a controller
        """
        data = {
            'id': self.id
            ,'messages':self._messages
            ,'itinerary':self.__itinerary
            ,'loc':self.__loc
            ,'simulator_port':self._simulator_port
            ,'simulator_address':self._simulator_address
            ,'range':self.__range
            ,'speed':self.__speed
            ,'network': self._network
        }
        req = requests.post(url = API_ENDPOINT, json = data)
        if req.status_code == 200:
            self._is_controller = True
            return True
        return False
    
    def create_network(self, API_ENDPOINT:str, network:str, is_controller:bool) -> bool:
        """Added a network to the ship and updating the controller also

        Args:
            API_ENDPOINT (str): API endpoint for the controller server
            network (str): Network id to be added

        Returns:
            bool: Request Completed
        """
        self._network = network
        if is_controller:
            return self.make_controller(API_ENDPOINT)
        req = requests.post(url=API_ENDPOINT, json={'ship_id':self.id, 'network': network})
        if req.status_code == 200:
            return True
        return False
        

if __name__ == "__main__":
    pass