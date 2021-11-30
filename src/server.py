"""
    This is the parent class for all the servers. It sets up the flask app
    and exposes the method to add endpoints
"""

from flask import Flask, request, Response
from flask.wrappers import Request
import numpy as np
import re
import json

class EndpointAction:
    def __init__(self, action):
        self.action = action
        self.response = None

    def __call__(self, *args):
        self.response = self.action(request)
        return self.response

class Server:
    def __init__(self) -> None:
        self._app = None
        pass

    def __call__(self) -> None:
        self._app = Flask(__name__)
        self.add_endpoint(
            endpoint='/ping',
            name='ping',
            handler=self.ping)
    
    def add_endpoint(self, endpoint: str, name: str, handler: function) -> None:
        self._app.add_url_rule(endpoint, name, EndpointAction(handler), methods=['GET', "POST"])

    def ping(self, request: Request):
        """
        Returns the list of all ships inside communication range of a ship sending out a ping

        Parameters:
            ship_id: the id of the ship which is sending out a ping
        Returns:

        """
        try:
            entity_id = request.args.get("ship_id")
            output = []
            _ship = self.ship_details.loc[self.ship_details['ship_id']==entity_id]
            location = _ship['location'].to_string(index=False)

            communication_range = _ship['communicationRange'].to_string(index=False)
            loc1 = np.array(list(map(float, np.array(re.findall(r'\d+', location)))))
            
            for i in range(self.ship_details.shape[0]):
                if self.ship_details.loc[i, 'ship_id'] == entity_id:
                    continue
                else:
                    str_loc2 = self.ship_details.loc[i, 'location']
                    loc2 = np.array(list(map(float, np.array(re.findall(r'\d+', str_loc2)))))
                    print(loc2)
                    distance = np.linalg.norm(loc1 - loc2)
                    if distance <= float(communication_range):
                        output.append(self.ship_details.loc[i, 'ship_id'])
            print(output)
            output = json.dumps(output)
            res = Response(response=output, status=200)
        except Exception as e:
            res = Response(response=f"Error handling addStation request: {repr(e)}", status=400)
        return res