#! ./.venv/bin/python

__title__ = "Ships"
__author__ = "Scalable Module Group 15"
__version__ = 1.0


class station:
    """
    A station, generating and recieving messages

    Parameters:
        location(dict): a dictionary containing the x,y coordinates of the station
        population(int): the size of the stations population, used to determine the rate of message generation
    """
    def __init__(self, location: tuple, population: int, stationID: str) -> None:
        if len(location) != 2:
            raise ValueError('location must be in the form of x,y')
        self.location = location
        self.population = population
        self._id = stationID
    
    def generate_message(self):
        """
        Generate a new message
        """
        ...
    
    @property
    def loc(self):
        return self.location

    @loc.setter
    def loc(self, inp: tuple[float]):
        """Setter fuction for the location property

        Args:
            inp (tuple[float]): (x, y) type input
        """
        if len(inp) == 2:
            self.location = inp
        else:
            raise ValueError('Input type expected in the form of x,y')