#! ./.venv/bin/python

__title__ = "Ships"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

from time import sleep
from numpy.random import uniform
from typing import List
import json

from superEntity import SuperEntity

__COMMUNICATION_RANGE = [100, 1000]
__SPEED_RANGE = [100, 1000]

class ship(SuperEntity):
    """Ship Class
    Args:
        loc(tuple): x and y cordinate of the Ships
        ShipID(str): the name of the ship
    """
    def __init__(self, shipId: str, simulator_address: str, port: str) -> None:
        super().__init__(shipId, port, simulator_address)
        self.__loc = (0.0, 0.0)
        self.__range = 0
        self.__speed = 0
        self.__itinerary = []
        pass

    @property
    def itinerary(self):
        return self.__itinerary

    @property
    def loc(self):
        """Getter fuction for the location property

        Returns:
            tuple[float]: x and y cordinates of the ships.
        """
        return self.__loc
    
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
    
    @property
    def range(self):
        """Getter fuction for the Communication range property

        Returns:
            int: Communication radius of the ships
        """
        return self.__range
    
    @range.setter
    def range(self, inp: int):
        if __COMMUNICATION_RANGE[0] < inp < __COMMUNICATION_RANGE[1]:
            self.__range = inp
        else:
            raise ValueError(f'Input communication range of the ships is between {__COMMUNICATION_RANGE[0]} & {__COMMUNICATION_RANGE[1]}')
    
    @property
    def speed(self):
        return str(self.__speed) + 'm/s'
    
    @speed.setter
    def speed(self, inp: float):
        if __SPEED_RANGE[0] < inp < __SPEED_RANGE[1]:
            self.__speed = inp
        else:
            raise ValueError(f'Speed Range for the ships is between {__SPEED_RANGE[0]} & {__SPEED_RANGE[1]}')

    def ping(self):
        res = super().make_get_request_to_controller(endpoint="ping", params=self._id)
        data = json.loads(res.content)
        print(f"ping response {data}...")
        return data

if __name__ == "__main__":
    pass