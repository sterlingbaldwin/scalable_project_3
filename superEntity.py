#! ./.venv/bin/python

__title__ = "Station"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

import json
import urllib
import requests
from time import sleep
from typing import Dict
from datetime import datetime
from numpy.random import uniform

class SuperEntity:
    def __init__(self, id: str, port: str, address: str) -> None:
        self._id = id
        self._simulator_port = port
        self._simulator_address = address
        pass

    def make_get_request(self, endpoint: str, params: Dict):
        """
        Make an API request to the simulation server on the redefined port
        Parameters:
            endpoint(str): the path relative the server
            params(Dict): a dict of key,value parameters which will be url encoded
        Returns:
            request(requests.Request): the response from the server
        """
        request = None
        url = f"http://{self._simulator_address}:{self._port}/{endpoint}"
        if params:
            url += f"?{urllib.parse.urlencode(params)}"
        
        print(f"Sending get request: {url}")
        session = requests.Session()
        session.trust_env = False
        request = session.prepare_request(requests.Request('GET', url))
        if (request := session.send(request)).status_code != 200:
            raise ValueError(f"Error from the simulator: {request} from request: {url}")
        return request
        

    def new_entity_connect(self):
        """
        Register the new station with the simulator
        """
        params = {
            "entity_type": "station",
            "entity_id": self._id
        }
        res = self.make_get_request("new_entity_connect", params)
        data = json.loads(res.content)
        print(f"simulator response {data}")

        self.loc = tuple(data["location"])
    
    def run(self):
        print("connecting to the server")
        self.new_entity_connect()
        while True:
            sleep(uniform(1.5, 2.5))
            print("starting update")
            self.update()

    def update(self):
        """
        Get an update from the simulator
        """
        now = datetime.now().strftime('%H:%M:%S')
        print(f"hello: its {now}")
        params = {
            "entity_id": self._id,
            "time": now
        }
        res = self.make_get_request("update", params)
        try:
            data = json.loads(res.content)
        except Exception as e:
            # it wasnt json data
            print(res.content)
        else:
            print(data.decode('utf-8'))
        pass

    def generate_message(self):
        """
        Generate a new message
        """
        ...
    

    pass