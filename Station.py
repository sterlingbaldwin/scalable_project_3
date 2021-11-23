#! ./.venv/bin/python

__title__ = "Station"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

# from typing import Dict, List
# import requests
# import urllib
# import json
# from datetime import datetime
# from numpy.random import uniform
# from time import sleep
from superEntity import SuperEntity

class station(SuperEntity):
    """
    A station, generating and recieving messages

    Parameters:
        location(dict): a dictionary containing the x,y coordinates of the station
        population(int): the size of the stations population, used to determine the rate of message generation
    """
    def __init__(self, population: int, stationId: str, address: str, port: str) -> None:
        self.location = None
        self.population = population
        super().__init__(stationId, port, address)

        print(f"Initializing new station: {self}")
    
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