#! ./.venv/bin/python

__title__ = "Simulator"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

from uuid import uuid4

from Ship import ship
from Station import station
from util import distance


class simulator:
    def __init__(self, num_ships: int, num_stations: int) -> None:
        self._ships = [ship(ShipID=uuid4.hex()) for _ in range(num_ships)]
        self._stations = [station({'x': 0, 'y': 0}) for _ in range(num_stations)]
    
    def in_range(a, b):
        """
        Determine if entity a and b are able to communicate
        """
        span = distance(a, b)
        if span < a.range and span < b.range:
            return True
        else:
            return False