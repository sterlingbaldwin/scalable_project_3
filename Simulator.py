#! ./.venv/bin/python

__title__ = "Simulator"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

import json
from flask import Flask, Response, request
from flask.json import dumps
from numpy.random import uniform, choice
from dataclasses import dataclass

class EndpointAction:

    def __init__(self, action):
        self.action = action
        self.response = None

    def __call__(self, *args):
        self.response = self.action(request)
        return self.response

@dataclass
class ShipRecord:
    """Class to hold basic info about a ship"""
    name: str
    location: tuple

@dataclass
class StationRecord:
    """Class to hold basic info about a station"""
    name: str
    location: tuple


class simulator:
    def __init__(self, size: int, host:str = "127.0.0.1", port: str = "5000") -> None:
        print("Initializing the simulator")
        self._world_size = size
        self._app = None
        self._timestep = 0
        self._stations = []
        self._ships = []
        self.host = host
        self.port = port

    def __call__(self):
        self._app = Flask(__name__)
        self.add_endpoint(
            endpoint='/new_entity_connect', 
            name='new_entity_connect',
            handler=self.new_entity_endpoint)
        print(f"Starting the server with address {self.host}")
        self._app.run(host=self.host, port=self.port)

    def add_endpoint(self, endpoint, name, handler):
        self._app.add_url_rule(endpoint, name, EndpointAction(handler))

    def new_entity_endpoint(self, request):
        print(f"got a new entity connection request with info {request}")
        res = None
        entity_type = request.args.get('entity_type')
        entity_id = request.args.get('entity_id')
        if not entity_type:
            res = Response(response="No entity_type in request", status=400)
            return res
        if not entity_id:
            res = Response(response="No entity_id in request", status=400)
            return res
        else:
            if entity_type not in ["ship", "station"]:
                res = Response(response=f"{entity_type} is not a valid entity type", status=400)
                return res
            if entity_type == "ship":
                for ship in self._ships:
                    if ship.name == entity_id:
                        res = Response(response=f"a ship with id {entity_id} already exists", status=400)
                        return res
                # if our station list is empty, just drop the ship anywhere
                if not self._stations:
                    posx = uniform(0, self._world_size)
                    posy = uniform(0, self._world_size)
                else:
                    loc = choice(self._stations).location
                    posx = loc[0]
                    posy = loc[0]
                new_ship = ShipRecord(name=entity_id, location=(posx, posy))
                self._ships.append(new_ship)
                res = Response(
                    json.dumps({
                        "location": (posx, posy)
                    }),
                    status=200)
            if entity_type == "station":
                for station in self._stations:
                    if station.name == entity_id:
                        res = Response(response=f"a station with id {entity_id} already exists", status=400)
                        return res
                posx = uniform(0, self._world_size)
                posy = uniform(0, self._world_size)
                new_station = StationRecord(
                    location=(posx, posy),
                    name=entity_id)
                self._stations.append(new_station)
                res = Response(
                    json.dumps({
                        "location": (posx, posy)
                    }),
                    status=200)
        return res


    