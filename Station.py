#! ./.venv/bin/python

__title__ = "Station"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

import requests
import json
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
    
    
    def connect(self):
        """
        Register the new station with the simulator
        """
        url = f"http://{self.__simulator_address}:{self.__port}/new_entity_connect"
        params = {
            "entity_type": "station",
            "entity_id": self.__id
        }
        print("Sending connection request to simulator")
        if (res := requests.get(url, params)).status_code != 200:
            raise ValueError("Unable to connect to simulator: {res}")
        data = json.loads(res.content)
        print(f"simulator response {data}")
        self.loc = tuple(data["location"])
    
    def run(self):
        self.connect()
        while True:
            sleep(uniform(.5, 1.5))
            self.update()
    
    def update(self):
        """
        Get an update from the simulator
        """
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