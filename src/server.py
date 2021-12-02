
"""
    This is the parent class for all the servers. It sets up the flask app
    and exposes the method to add endpoints
"""
import re
import sys
import os
import json
from typing import Callable
import numpy as np
from time import sleep
import psutil
from flask.wrappers import Request
from multiprocessing import Process
from flask import Flask, request, Response

class EndpointAction:
    def __init__(self, action):
        self.action = action
        self.response = None

    def __call__(self, *args):
        print(f"got a request: {request}")
        self.response = self.action(request)
        return self.response

class Server:
    def __init__(self, address:str = "127.0.0.1", port:int = 33000, secret:str = None, *args, **kwargs) -> None:
        self._address = address
        self._port = port
        self._app = None
        self._proc = None
        self._secret = secret
        self._app = Flask(__name__)
        self.add_endpoint(
            endpoint='/ping',
            name='ping',
            handler=self.ping)
        self.add_endpoint(
            endpoint='/shutdown',
            name='shutdown',
            handler=self.shutdown)
    
    def start(self):
        print(f"Starting server from process: {os.getpid()} with secret {self._secret}")
        self._proc = Process(
            target=self._app.run,
            daemon=True,
            kwargs={
                "host": self._address,
                "port": self._port})
        self._proc.start()
    
    def start_blocking(self):
        self.start()
        while True:
            sys.stdout.flush()
            sleep(1)
            if not self._proc.is_alive():
            # if psutil.pid_exists(self._proc.pid):
                print("child is not alive, exiting", flush=True)
                sys.exit(0)
    
    def shutdown(self, request=None):
        """
        Shut down the server
        Parameters:
            secret: a string, it should match the value given at startup
        Returns:
            Response with status 200 on success, 400 otherwise
        """
        try:
            print("Got a shutdown request", flush=True)
            # secret = json.loads(request.form.get("secret"))
            secret = request.args.get('secret')
            print(f"request secret = {secret}, my secret = {self._secret}", flush=True)
            if secret == self._secret or self._secret == None: 
                print("secrets match, exiting", flush=True)
                # self._proc.terminate()
                # self._proc.join()
                sleep(1)
                sys.exit(0)
                # res = Response(response=f"Shutting down", status=200)
            else:
                res = Response(response=f"Not shutting down for you!", status=400)
        except Exception as e:
            res = Response(response=f"Unable to shutdown: {repr(e)}", status=400)
        return res
    
    def add_endpoint(self, endpoint: str, name: str, handler: Callable) -> None:
        self._app.add_url_rule(endpoint, name, EndpointAction(handler), methods=["GET", "POST"])

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