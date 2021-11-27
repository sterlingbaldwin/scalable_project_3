from flask import Flask, request, Response
from flask.wrappers import Request
from Server import Server
from MainController import MainController

class controller(Server):
    def __init__(self) -> None:
        self._ControllerList = []
        pass

    def __call__(self) -> None:
        super().__call__()
        self.add_endpoint(
            endpoint='/addController', 
            name='addedController',
            handler=self.addController
        )
        self.add_endpoint(
            endpoint='/removeController',
            name='removecontroller',
            handler=self.removeController
        )

    def addController(self, request: Request):
        try:
            controller = MainController(
                request.form.get('shipID'),
                request.form.get('simulator_address'),
                request.form.get('shipPort')
            )
            self._ControllerList.append(controller)
            res = Response(response=f"Added Controller {controller.id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling remove_entity request: {repr(e)}", status=400)
        return res
    
    def removeController(self, request: Request):
        try:
            shipID = request.form.get('controllerID')
            self._ControllerList=[element for element in self._ControllerList if element.id != shipID]
            res = Response(response=f"Removed Controller {shipID}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling remove_entity request: {repr(e)}", status=400)
        return res
    


