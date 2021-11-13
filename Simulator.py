#! ./.venv/bin/python

__title__ = "Simulator"
__author__ = "Scalable Module Group 15"
__version__ = 1.0

from uuid import uuid4
from flask import Flask, Response, request
from numpy.random import uniform, choice
# from app import routes

from Ship import ship
from Station import station

class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = None

    def __call__(self, *args):
        self.response = self.action(request)
        return self.response

class simulator:
    def __init__(self, size: int, host:str = "127.0.0.1") -> None:
        # self._ships = [ship(ShipID=uuid4.hex()) for _ in range(num_ships)]
        # self._stations = [station({'x': 0, 'y': 0}) for _ in range(num_stations)]
        print("Initializing the simulator")
        self._world_size = size
        self._app = None
        self._timestep = 0
        self.host = host
        self._stations = []
        self._ships = []

    def __call__(self):
        self._app = Flask(__name__)
        self.add_endpoint(
            endpoint='/new_entity_connect', 
            name='new_entity_connect',
            handler=self.new_entity_endpoint)
        print(f"Starting the server with address {self.host}")
        self._app.run(host=self.host)

    def add_endpoint(self, endpoint, name, handler):
        self._app.add_url_rule(endpoint, name, EndpointAction(handler))

    def new_entity_endpoint(self, request):
        print(f"got a new entity connection request with info {request}")
        res = Response(status=200, headers={})
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
                for ship in self.ships:
                    if ship._id == entity_id:
                        res = Response(response=f"a ship with id {entity_id} already exists", status=400)
                        return res
                # if our station list is empty, just drop the ship anywhere
                if not self._stations:
                    posx = uniform(0, self._world_size)
                    posy = uniform(0, self._world_size)
                else:
                    loc = choice(self._stations).loc
                    posx = loc[0]
                    posy = loc[0]
                new_ship = ship(entity_id)
                new_ship.loc((posx, posy))
                self.ships.append(new_ship)
            if entity_type == "station":
                for station in self.stations:
                    if station._id == entity_id:
                        res = Response(response=f"a station with id {entity_id} already exists", status=400)
                        return res
                posx = uniform(0, self._world_size)
                posy = uniform(0, self._world_size)
                new_station = station(
                    location=(posx, posy),
                    population=uniform(100, 100_000),
                    stationID=entity_id)
                self.ships.append(new_station)
        return res


    