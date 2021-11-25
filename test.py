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
        new_ship.loc = (1, 2)
        new_ship.speed = 120
        new_ship.range = 500
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

    def test_ping(self):
        config = configparser.ConfigParser()
        config.read('Environment.ini')
        _id_for_ship_2 = uuid4().hex
        new_ship_2 = ship(
            ship_id=_id_for_ship_2,
            simulator_address=config['MainController']['hostIP'],
            port=config['MainController']['port'])
        new_ship_2.loc = (3, 4)
        new_ship_2.speed = 120
        new_ship_2.range = 500
        new_ship_2.connect()

        _id_for_ship_3 = uuid4().hex
        new_ship_3 = ship(
            ship_id=_id_for_ship_3,
            simulator_address=config['MainController']['hostIP'],
            port=config['MainController']['port'])
        new_ship_3.loc = (4, 5)
        new_ship_3.speed = 120
        new_ship_3.range = 500
        new_ship_3.connect()

        res = new_ship_2.ping()
        self.assertEqual(len(res.split(',')), 2)

    # def test_update(self):
    #     pass


if __name__ == '__main__':
    unittest.main()