"""
    This module contains the server that is responsible for
    managing all the network controllers.
"""
import argparse
import sys
from flask import Response
from flask.wrappers import Request
from server import Server
from network_controller import NetworkController
import pandas as pd

class ControllerManager(Server):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._controller_list = []
        self._network_details = pd.DataFrame(columns=['network', 'controller_id'])
        self.add_endpoint(
            endpoint='/add_controller', 
            name='add_controller',
            handler=self.add_controller)
        self.add_endpoint(
            endpoint='/remove_controller',
            name='remove_controller')

    def add_controller(self, request: Request):
        """
        Add a new controller to the controller_list
        
        Parameters:
            ship_id: the UUID of the new ship being added
            simulator_address: the IP address of the simulator managing this ship
            ship_port: the port to use when communicating with the simulator
        Returns:
            Response with status 200 on success, 400 otherwise
        """
        try:
            controller = NetworkController(
                request.form.get('ship_id'),
                request.form.get('simulator_address'),
                request.form.get('ship_port')
            )
            self._controller_list.append(controller)
            self._network_details.loc[self._network_details.shape[0]] = {
                'network': request.form.get('network'),
                'controller_id': request.form.get('ship_id')
            }
            res = Response(response=f"Added new network_controller: {controller.id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling add_controller request: {repr(e)}", status=400)
        return res
    
    def remove_controller(self, request: Request):
        """
        Add a new controller to the controller_list
        
        Parameters:
            ship_id: the UUID of the new ship to remove
        Returns:
            Response with status 200 on success, 400 otherwise
        """
        try:
            ship_id = request.form.get('controller_id')
            self._controller_list=[element for element in self._controller_list if element.id != ship_id]
            self._network_details.drop(self._network_details[self._network_details['network'].isin(request.form.get('network'))].index, inplace=True)
            res = Response(response=f"Removed network_controller: {ship_id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling remove_controller request: {repr(e)}", status=400)
        return res
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the ControllerManager")
    parser.add_argument(
        '--host',
        type=str)
    parser.add_argument(
        "--port",
        type=int)
    parser.add_argument(
        "--secret",
        type=str)
    args = parser.parse_args()
    cm = ControllerManager(
        address=args.host,
        port=args.port,
        secret=args.secret)
    cm.start_blocking()
    sys.exit(0)
