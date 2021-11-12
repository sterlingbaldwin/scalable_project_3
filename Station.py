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
    def __init__(self, location: tuple, population: int) -> None:
        if len(location) != 2:
            raise ValueError('location must be in the form of x,y')
        self.location = location
        self.population = population
    
    def generate_message(self):
        """
        Generate a new message
        """
        ...