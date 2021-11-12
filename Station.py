#! ./.venv/bin/python

__title__ = "Ships"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

from typing import List

class station:
    """
    A station, generating and recieving messages

    Parameters:
        location(dict): a dictionary containing the x,y coordinates of the station
        population(int): the size of the stations population, used to determine the rate of message generation
    """
    def __init__(self, location: dict, population: int) -> None:
        if location.get('x') is None:
            raise ValueError("A station must have an x coordinate")
        if location.get('y') is None:
            raise ValueError("A station must have an y coordinate")
        self.location = location
        self.population = population
    
    def generate_message(self):
        """
        Generate a new message
        """
        ...