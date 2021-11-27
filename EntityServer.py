from flask.wrappers import Request, Response
import numpy as np
import pandas as pd
from Server import Server
from Ship import ship

class EntityServer(Server):
    def __init__(self) -> None:
        super().__init__()
        self._elementDetails = {}
        self.__max_network = 0
        self.networkDetails = pd.DataFrame(columns=['network', 'elementCount'])
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
            shipElement = ship(
                request.form.get('shipID'),
                request.form.get('simulator_address'),
                request.form.get('shipPort')
            )
            self._elementDetails[shipElement.id] = {
                'ship': shipElement
            }
            res = Response(response=f"Added Ship {shipElement.id}", status=200)
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

    def addtoNetwork(self, shipEntity: ship):
        recognisedShips = list(self._elementDetails.keys())
        networkList = []
        if len(recognisedShips) == 0:
            self.__max_network += 1
            self._elementDetails[shipEntity.id]['network'] = self.__max_network
            self.networkDetails.loc[self.networkDetails.shape[0]] = {'network': self.__max_network, 'elementCount': 1}
        else:
            shipLocation = np.array(shipEntity.loc)
            for ele in recognisedShips:
                element = self._elementDetails[ele]['ship']
                refLocation = np.array(element.loc)
                distance = np.linalg.norm(shipLocation - refLocation)
                if distance < shipEntity.range & distance < element.loc:
                    if 'network' in self._elementDetails[shipEntity.id].keys():
                        networkList.append(self._elementDetails[ele]['network'])
            if len(networkList) == 0:
                self.__max_network += 1
                self._elementDetails[shipEntity.id]['network'] = self.__max_network
                self.networkDetails.loc[self.networkDetails.shape[0]] = {'network': self.__max_network, 'elementCount': 1}
            elif len(networkList) == 1:
                self._elementDetails[shipEntity.id]['network'] = networkList[0]
                self.networkDetails.loc[self.networkDetails['network'] == networkList[0], 'elementCount'] += 1
            else:
                self._elementDetails[shipEntity.id]['network'] = self.networkDetails.loc[self.networkDetails['elementCount'].idxmax(), 'network']
                self.networkDetails.loc[self.networkDetails['network'] == self._elementDetails[shipEntity.id]['network'], 'elementCount'] += 1
