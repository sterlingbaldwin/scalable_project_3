#! ./.venv/bin/python

__title__ = "Station"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

import json
import urllib
import requests
from time import sleep
from typing import Dict
from datetime import datetime
from numpy.random import uniform

class SuperEntity:
    def __init__(self, id: str, port: str, address: str) -> None:
        self.__loc = (0.0, 0.0)
        self._id = id
        self._simulator_port = port
        self._simulator_address = address
    
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
    
    def connect(self):
        pass
    
    def run(self):
        print("connecting to the controller")
        self.connect()
        while True:
            sleep(uniform(1.5, 2.5))
            print("starting update")
            self.update()

    def update(self):
        """
        Get an update from the simulator
        """
        now = datetime.now().strftime('%H:%M:%S')
        params = {
            "time": now
        }
        res = self.make_request_to_controller("update", params)
        try:
            data = json.loads(res.content)
        except Exception as e:
            print(res.content)
        else:
            print(data.decode('utf-8'))
        pass

    def generate_message(self):
        """
        Generate a new message
        """
        ...
    