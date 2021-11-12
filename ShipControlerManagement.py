#! ./.venv/bin/python

"""Ships management on the control side
code to be used on the controler pi
"""

__title__ = "ShipMangaement"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

from Station import station
from Ship import ship
import numpy as np

shipsDetails = {}

def canCommunicate(ship1: ship, ship2: ship):
    """Check if 2 ships can communicate with each other

    Args:
        ship1 (ships): Ship 1 object for consideration
        ship2 (ships): Ship 2 object for consideration

    Returns:
        boolean: if the 2 ships are in each others range for communication.
    """
    distance = abs(np.linalg.norm(ship1.loc - ship2.loc))
    if distance < ship1.range & distance < ship2.range:
        return True
    else:
        return False

def addShipDetails(ship: ship):
    shipsDetails[ship.id] = ship
