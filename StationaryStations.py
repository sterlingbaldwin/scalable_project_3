#! ./.venv/bin/python

__title__ = "Ships"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

from typing import List

class stationaryStation:
    def __init__(self, location:List[float]) -> None:
        if len(location) != 2:
            raise ValueError('Location of the station must be in the form of x,y cordinates')
        location = tuple(location)