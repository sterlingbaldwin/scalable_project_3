"""
    This module contains the server that is responsible for
    managing all the network controllers.
"""
import argparse
from os import remove
import sys
from flask import Response
from flask.wrappers import Request
import requests
from server import Server
from network_controller import NetworkController
import pandas as pd

class ControllerManager(Server):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._controller_list = {}
        self._network_details = pd.DataFrame(columns=['network', 'controller_id'])
        self.add_endpoint(
            endpoint='/add_controller', 
            name='add_controller',
            handler=self.add_controller)
        self.add_endpoint(
            endpoint='/remove_controller',
            name='remove_controller',
            handler=self.remove_controller)

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
            self._controller_list[controller.id] = controller
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
            self._controller_list.pop(ship_id.id)
            self._network_details.drop(self._network_details[self._network_details['network'].isin(request.form.get('network'))].index, inplace=True)
            res = Response(response=f"Removed network_controller: {ship_id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling remove_controller request: {repr(e)}", status=400)
        return res

    def merge_network(self, request: Request):
        try:
            actual_network = request.form.get('actual_network')
            merge_networks_list = request.form.get('merge_networks_list')
            new_main_controller = self._network_details.loc[self._network_details['network'] == actual_network, 'controller_id'][0]
            for controller in self._network_details.loc[self._network_details['network'].isin(merge_networks_list), 'controller_id']:
                self._controller_list[new_main_controller].add_ships(self._controller_list[controller])
                self._controller_list.pop(controller)
            self._network_details.drop(self._network_details[self._network_details['network'].isin(merge_networks_list)].index, inplace=True)
        except Exception as e:
            res = Response(response=f"Error handling merge_network request: {repr(e)}", status=400)
        return res

    def send_injection_message(self, request: Request):
        try:
            ship_id = request.form.get('ship_id')
            for ship in self._controller_list.keys():
                if self._controller_list[ship].ship_in_network(ship) | self._controller_list[ship].id == ship_id | ship_id is None:
                    self._controller_list[ship].message_carry_request(request.form.get('message'))
            res = Response(response=f"Sent the message to the {ship_id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling send_message request: {repr(e)}", status=400)
        return res
    
    def recieve_ship_messages(self, request: Request):
        try:
            message = requests.form.get('message')
            message_sent = False
            for controller in self._controller_list.keys():
                if self._controller_list[controller].ship_in_network(message.source):
                    if self._controller_list[controller].ship_in_network(message.destination) | message.destination is None:
                        self._controller_list[controller].message_carry_request(message)
                        message_sent = True
                        break
                    else:
                        break
            res = Response(response=f"{message_sent}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling send_message request: {repr(e)}", status=400)
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
