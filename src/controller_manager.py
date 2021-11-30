"""
    This module contains the server that is responsible for
    managing all the network controllers.
"""
from flask import Response
from flask.wrappers import Request
from server import Server
from network_controller import NetworkController

class ControllerManager(Server):
    def __init__(self) -> None:
        self._controller_list = []
        pass

    def __call__(self) -> None:
        super().__call__()
        self.add_endpoint(
            endpoint='/add_controller', 
            name='add_controller',
            handler=self.add_controller)
        self.add_endpoint(
            endpoint='/remove_controller',
            name='remove_controller',
            handler=self.remove_controller)
        self._app.run()

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
            res = Response(response=f"Removed network_controller: {ship_id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling remove_controller request: {repr(e)}", status=400)
        return res
    

