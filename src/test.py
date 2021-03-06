import unittest
from ship import Ship
import configparser
import requests
from uuid import uuid4

config = configparser.ConfigParser()
config.read('Environment.ini')

def remove_entity(addr, port, _id):

    url = url = f"http://{addr}:{port}/remove_entity"
    session = requests.Session()
    session.trust_env = False
    request = session.prepare_request(requests.Request("POST", url, data={'entity_id': _id}))
    if (request := session.send(request)).status_code != 200:
        raise ValueError(f"Error from the controller: {request} from request: {url} and response: {request.content.decode('utf-8')}")

class TestControllerEndpoints(unittest.TestCase):

    def test_add_ship(self):
        _id = uuid4().hex
        new_ship = Ship(
            ship_id=_id,
            simulator_address=config['config']['hostIP'],
            port=config['config']['port'])
        new_ship.loc = (1, 2)
        new_ship.speed = 120
        new_ship.range = 500
        res = new_ship.connect()
        self.assertEqual(res.status_code, 200)

        remove_entity(
            config['config']['hostIP'], 
            config['config']['port'],
            _id)

    def test_ping_in_range(self):
        _id_for_ship_2 = uuid4().hex
        new_ship_2 = Ship(
            ship_id=_id_for_ship_2,
            simulator_address=config['config']['hostIP'],
            port=config['config']['port'])
        new_ship_2.loc = (3, 4)
        new_ship_2.speed = 120
        new_ship_2.range = 500
        new_ship_2.connect()

        _id_for_ship_3 = uuid4().hex
        new_ship_3 = Ship(
            ship_id=_id_for_ship_3,
            simulator_address=config['config']['hostIP'],
            port=config['config']['port'])
        new_ship_3.loc = (4, 5)
        new_ship_3.speed = 120
        new_ship_3.range = 500
        new_ship_3.connect()

        res = new_ship_2.ping()
        self.assertEqual(len(res), 1)

        remove_entity(
            config['config']['hostIP'], 
            config['config']['port'],
            _id_for_ship_2)
        remove_entity(
            config['config']['hostIP'], 
            config['config']['port'],
            _id_for_ship_3)
    

    
    def test_ping_out_of_range(self):
        config = configparser.ConfigParser()
        config.read('Environment.ini')
        _id_for_ship_2 = uuid4().hex
        new_ship_2 = Ship(
            ship_id=_id_for_ship_2,
            simulator_address=config['config']['hostIP'],
            port=config['config']['port'])
        new_ship_2.loc = (3, 4)
        new_ship_2.speed = 120
        new_ship_2.range = 500
        new_ship_2.connect()

        _id_for_ship_3 = uuid4().hex
        new_ship_3 = Ship(
            ship_id=_id_for_ship_3,
            simulator_address=config['config']['hostIP'],
            port=config['config']['port'])
        new_ship_3.loc = (1000000, 5000000)
        new_ship_3.speed = 120
        new_ship_3.range = 500
        new_ship_3.connect()

        res = new_ship_2.ping()
        print(f"response from server: {res}")
        self.assertEqual(len(res), 0)

        remove_entity(
            config['config']['hostIP'], 
            config['config']['port'],
            _id_for_ship_2)
        remove_entity(
            config['config']['hostIP'], 
            config['config']['port'],
            _id_for_ship_3)

    # def test_update(self):
    #     pass


if __name__ == '__main__':
    unittest.main()