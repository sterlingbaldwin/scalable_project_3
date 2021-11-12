#! ./.venv/bin/python

"""Ships management on the control side
code to be used on the controler pi
"""

__title__ = "ShipMangaement"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

from StationaryStations import stationaryStation
from Ships import ships
import numpy as np

shipsDetails = {}

def canCommunicate(ship1: ships, ship2: ships):
    """Check if 2 ships can communicate with each other

    Args:
        ship1 (ships): Ship 1 object for consideration
        ship2 (ships): ship 2 object for consideration

    Returns:
        boolean: if the 2 ships are in each others range for communication.
    """
    distance = abs(np.linalg.norm(ship1.loc - ship2))
    if distance < ship1.range & distance < ship2.range:
        return True
    else:
        return False

def addShipDetails(ship: ships):
    shipsDetails[ship.id] = ship
