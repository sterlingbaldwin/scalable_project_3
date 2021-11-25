import argparse
import unittest
from subprocess import Popen, PIPE
import uuid
from Ship import ship
from Station import station
import configparser
from time import sleep
from uuid import uuid4

config = configparser.ConfigParser()
config.read('Environment.ini')

class TestStringMethods(unittest.TestCase):

    def test_add_ship(self):
        _id = uuid4().hex
        new_ship = ship(
            ship_id=_id,
            simulator_address=config['MainController']['hostIP'],
            port=config['MainController']['port'])
        res = new_ship.connect()
        self.assertEqual(res.status_code, 200)
        pass
    
    def test_add_station(self):
        _id = uuid4().hex
        new_station = station(
            population=10,
            station_id = _id,
            simulator_address = config['MainController']['hostIP'],
            port=config['MainController']['port']
        )
        res = new_station.connect()
        self.assertEqual(res.status_code, 200)

    # def test_ping(self):
    #     pass

    # def test_update(self):
    #     pass


if __name__ == '__main__':
    unittest.main()