"""
    This is a management class for the ships, it holds a record 
    of all the ships and the networks they belong to. It manages
    their communication with the ControllerManager, which resides on
    a sepperate device.
"""
from flask.wrappers import Request, Response
import sys
import argparse
import numpy as np
import pandas as pd
from server import Server
from ship import Ship
import requests

class EntityManager(Server):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._element_details = {}
        self.__max_network = 0
        self._network_details = pd.DataFrame(columns=['ship_id', 'network'])
        self.add_endpoint(
            endpoint='/add_ship',
            name='add_ship',
            handler=self.add_ship,
            methods=["POST"])
        self.add_endpoint(
            endpoint='/remove_ship',
            name='remove_ship',
            handler=self.remove_ship,
            methods=["POST"])
        self.controller_endpoint = kwargs.get('controller_manager_address')
    
    def add_ship(self, request: Request):
        """
        Adds a new ship to the _element_details list

        Parameters:
            ship_id: the UUID of the new ship being added
            simulator_address: the IP address of the simulator managing this ship
            ship_port: the port to use when communicating with the simulator
        Returns:
            Response with status 200 on success, 400 otherwise
        """
        try:
            ship_element = Ship(
                request.form.get('ship_id'),
                request.form.get('simulator_address'),
                request.form.get('ship_port')
            )
            self._element_details[ship_element.id] = ship_element
            res = Response(response=f"Added new ship: {ship_element.id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling add_ship request: {repr(e)}", status=400)
        return res
    
    def remove_ship(self, request:Request):
        """
        Removes a ship from the _element_details list

        Parameters:
            ship_id: the id of the ship to remove
        Returns:
            Response with status 200 on success, 400 otherwise
        """
        try:
            self._elementList = [element for element in self._elementList if element.id != request.form.get('ship_id')]
            res = Response(response=f"Removed Ship: {request.form.get('ship_id')}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling remove_ship request: {repr(e)}", status=400)
        return res

    def add_to_network(self, shipEntity: Ship):
        """
        Adds a ship to the networks dataframe. If no networks exist,
            a new network is created and the ship is added to it,
            otherwise iterate over all the networks and see
            if the ship is in range of any of the ships in each network
        
        Parameters:
            shipEntity (ship): the ship to add to a network
        Returns:
            None
        """

        # there are no networks yet
        if self._network_details.shape[0] == 0:
            self.__max_network += 1
            self._network_details[self._network_details.shape[0]] = {
                'ship_id': shipEntity.id,
                'network': self.__max_network
            }
            shipEntity.create_network(self.controller_endpoint, self.__max_network, True)
            return
        
        loc = np.array(shipEntity.loc)
        networkList = []
        for ship in self._network_details.to_dict('records'):
            shipobj = self._element_details[ship['ship_id']]
            refLoc = np.array(shipobj.loc)
            distance = np.linalg.norm(loc - refLoc)
            if distance < shipEntity.range & distance < shipobj.range:
                networkList.append(ship['network'])

        # the ship wasnt added to any networks
        if len(networkList) == 0:
            self.__max_network += 1
            self._network_details[self._network_details.shape[0]] = {
                'ship_id': shipEntity.id,
                'network': self.__max_network
            }
            
            shipEntity.create_network(self.controller_endpoint, self.__max_network, True)
            return
        
        # find the largers network and add the ship
        maxnetwork = self._network_details.loc[self._network_details['network'].isin(networkList)].groupby(['network']).count().idxmax()[0]
        self._network_details[self._network_details.shape[0]] = {
            'ship_id': shipEntity.id,
            'network': maxnetwork
        }
        shipEntity.create_network(self.controller_endpoint, maxnetwork, False)
        self._network_details.loc[self._network_details['network'].isin(networkList), 'network'] = maxnetwork
        for ship_id in list(self._network_details.loc[self._network_details['network'].isin(networkList), 'ship_id']):
            self._element_details[ship_id].network = maxnetwork
        requests.post(url = self.controller_endpoint, json = {'actualNetwork': maxnetwork, 'mergedNetwork': networkList})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the EntityManager")
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
    em = EntityManager(
        address=args.host,
        port=args.port,
        secret=args.secret)
    em.start_blocking()
    sys.exit(0)
