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
    
    def add_endpoint(self, endpoint: str, name: str, handler: function) -> None:
        self._app.add_url_rule(endpoint, name, EndpointAction(handler), methods=['GET', "POST"])

    def ping(self, request: Request):
        """[summary]
        Args:
            entity_id: the id of the ship which needs to be pinged
        """
        try:
            entity_id = request.args.get("entity_id")
            output = []
            print(entity_id)
            print(self.ship_details)
            location = self.ship_details.loc[self.ship_details['ship_id']==entity_id]['location'].to_string(index=False)
            communication_range = self.ship_details.loc[self.ship_details['ship_id']==entity_id]['communicationRange'].to_string(index=False)
            loc1 = np.array(list(map(float, np.array(re.findall(r'\d+', location)))))
            print(loc1)
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
            res = Response(response=f"{output}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling addStation request: {repr(e)}", status=400)
        return res