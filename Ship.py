#! ./.venv/bin/python

__title__ = "Ships"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

from time import sleep
from numpy.random import uniform
from typing import List
from uuid import uuid4
import json

from superEntity import SuperEntity

class ship(SuperEntity):
    """Ship Class
    Args:
        loc(tuple): x and y cordinate of the Ships
        ship_id(str): the name of the ship
    """
    def __init__(self, ship_id: str, simulator_address: str, port: str) -> None:
        super().__init__(ship_id, port, simulator_address)
        self.__range = 0
        self.__speed = 0
        self.__itinerary = []
        self.__COMMUNICATION_RANGE = [100, 1000]
        self.__SPEED_RANGE = [100, 1000]
        self.connect()
        pass

    @property
    def itinerary(self):
        return self.__itinerary
    
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
        return str(self.__speed) + 'm/s'
    
    @speed.setter
    def speed(self, inp: float):
        if self.__SPEED_RANGE[0] < inp < self.__SPEED_RANGE[1]:
            self.__speed = inp
        else:
            raise ValueError(f'Speed Range for the ships is between {self.__SPEED_RANGE[0]} & {self.__SPEED_RANGE[1]}')
    
    def connect(self):
        params = {
            'ship_id': self._id,
            'speed': self.__speed,
            'comRange': self.__range,
            'loc': self.loc
        }
        return self.make_request_to_controller('add_ship', params, method="POST")

if __name__ == "__main__":
    pass