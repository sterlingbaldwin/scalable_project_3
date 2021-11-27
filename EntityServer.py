from flask.wrappers import Request, Response
from Server import Server
from Ship import ship

class EntityServer(Server):
    def __init__(self) -> None:
        super().__init__()
        self._elementList = []
        pass
    
    def __call__(self) -> None:
        super().__call__()
        self.add_endpoint(
            endpoint='/addShip',
            name='addShip',
            handler=self.addShip
        )
    
    def addShip(self, request: Request):
        try:
            Ship = ship(
                request.form.get('shipID'),
                request.form.get('simulator_address'),
                request.form.get('shipPort')
            )
            self._elementList.append(Ship)
            res = Response(response=f"Added Ship {Ship.id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling addShip request: {repr(e)}", status=400)
        return res
    
    def removeShip(self, request:Request):
        try:
            self._elementList = [element for element in self._elementList if element.id != request.form.get('shipID')]
            res = Response(response=f"Removed Ship {request.form.get('shipID')}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling removeShip request: {repr(e)}", status=400)
        return res
