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
        # self.networkDetails = pd.DataFrame(columns=['network', 'elementCount'])
        self.networkDetails = pd.DataFrame(columns=['shipID', 'network'])
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
            self._elementDetails[shipElement.id] = shipElement
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

    def addtoNetwork(self, shipEntity: str):
        networkController = None
        if self.networkDetails.shape[0] == 0:
            self.__max_network += 1
            self.networkDetails[self.networkDetails.shape[0]] = {
                'shipID': shipEntity.id,
                'network': self.__max_network
            }
            self._elementDetails[shipEntity].network = self.__max_network
            self._elementDetails[shipEntity].make_controller()
        else:
            loc = np.array(self._elementDetails[shipEntity].loc)
            networkList = []
            for ship in self.networkDetails.to_dict('records'):
                shipobj = self._elementDetails[ship['shipID']]
                refLoc = np.array(shipobj.loc)
                distance = np.linalg.norm(loc - refLoc)
                if distance < self._elementDetails[shipEntity].range & distance < shipobj.range:
                    networkList.append(ship['network'])
            if len(networkList) == 0:
                self.__max_network += 1
                self.networkDetails[self.networkDetails.shape[0]] = {
                    'shipID': self._elementDetails[shipEntity].id,
                    'network': self.__max_network
                }
                self._elementDetails[shipEntity].network = self.__max_network
                self._elementDetails[shipEntity].make_controller()
            else:
                maxnetwork = self.networkDetails.loc[self.networkDetails['network'].isin(networkList)].groupby(['network']).count().idxmax()[0]
                self.networkDetails[self.networkDetails.shape[0]] = {
                    'shipID': self._elementDetails[shipEntity].id,
                    'network': maxnetwork
                }
                self._elementDetails[shipEntity].network = maxnetwork
                networkList.remove(maxnetwork)
                self.networkDetails.loc[self.networkDetails['network'].isin(networkList), 'network'] = maxnetwork
                for shipid in list(self.networkDetails.loc[self.networkDetails['network'].isin(networkList), 'shipID']):
                    self._elementDetails[shipid].network = maxnetwork
                msg = {
                    'network': maxnetwork,
                    'mergingNetwork': networkList
                }
