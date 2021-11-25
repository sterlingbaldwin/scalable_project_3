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
    def __init__(self, population: int, station_id: str, simulator_address: str, port: str) -> None:
        super().__init__(station_id, port, simulator_address)
        self.population = population

        print(f"Initializing new station: {self}")
    
    def __str__(self):
        return str({
            "location": self.loc,
            "population": self.population,
            "id": self._id,
            "simulator_address": self._simulator_address,
            "simulator_port": self._simulator_port
        })

    def connect(self):
        print(self._id)
        params = {
            'station_id': self._id,
            'loc': self.loc
        }
        return self.make_request_to_controller('add_station', params, method="POST")

    