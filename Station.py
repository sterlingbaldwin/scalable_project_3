#! ./.venv/bin/python

__title__ = "Station"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

from typing import Dict, List
import requests
import urllib
import json
from datetime import datetime
from numpy.random import uniform
from time import sleep


class station:
    """
    A station, generating and recieving messages

    Parameters:
        location(dict): a dictionary containing the x,y coordinates of the station
        population(int): the size of the stations population, used to determine the rate of message generation
    """
    def __init__(self, population: int, stationId: str, address: str, port: str) -> None:
        self.location = None
        self.population = population
        self.__id = stationId
        self.__simulator_address = address
        self.__port = port

        print(f"Initializing new station: {self}")
    
    def make_get_request(self, endpoint: str, params: Dict):
        """
        Make an API request to the simulation server on the redefined port
        Parameters:
            endpoint(str): the path relative the server
            params(Dict): a dict of key,value parameters which will be url encoded
        Returns:
            request(requests.Request): the response from the server
        """
        request = None
        url = f"http://{self.__simulator_address}:{self.__port}/{endpoint}"
        if params:
            url += f"?{urllib.parse.urlencode(params)}"
        
        print(f"Sending connection request to simulator on url {url}")
        session = requests.Session()
        session.trust_env = False
        request = session.prepare_request(requests.Request('GET', url))
        if (request := session.send(request)).status_code != 200:
            raise ValueError(f"Unable to connect to simulator: {request}")
        return request
    
    def new_entity_connect(self):
        """
        Register the new station with the simulator
        """
        params = {
            "entity_type": "station",
            "entity_id": self.__id
        }
        res = self.make_get_request("new_entity_connect", params)
        data = json.loads(res.content)
        print(f"simulator response {data}")

        self.loc = tuple(data["location"])
    
    def run(self):
        print("connecting to the server")
        self.new_entity_connect()
        while True:
            sleep(uniform(.5, 1.5))
            print("starting update")
            self.update()

    def update(self):
        """
        Get an update from the simulator
        """
        now = datetime.now().strftime('%H:%M:%S')
        print(f"hello: its {now}")
        params = {
            "entity_id": self.__id,
            "time": now
        }
        res = self.make_get_request("update", params)
        data = json.loads(res.content)
        print(data)
        pass

    def generate_message(self):
        """
        Generate a new message
        """
        ...
    
    @property
    def loc(self):
        return self.location

    @loc.setter
    def loc(self, inp: tuple):
        """Setter fuction for the location property

        Args:
            inp (tuple[float]): (x, y) type input
        """
        if len(inp) == 2:
            self.location = inp
        else:
            raise ValueError('Input type expected in the form of x,y')
    
    def __str__(self):
        return str({
            "location": self.location,
            "population": self.population,
            "id": self.__id,
            "simulator_address": self.__simulator_address,
            "simulator_port": self.__port
        })