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
from numpy.lib.utils import source
import pandas as pd
from server import Server
from ship import Ship
import requests
import configparser

config = configparser.ConfigParser()
config.read('Environment.ini')

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
            methods=["GET"])
        self.add_endpoint(
            endpoint='/remove_ship',
            name='remove_ship',
            handler=self.remove_ship,
            methods=["POST"])
        self.add_endpoint(
            endpoint='/add_to_network',
            name='add_to_network',
            handler=self.add_to_network,
            methods=["GET"])
        self.add_endpoint(
            endpoint='/message_in_range',
            name="message_in_range",
            handler=self.message_in_range,
            methods=["GET"]
        )
        self.add_endpoint(
            endpoint='/update',
            name='update',
            handler=self.update,
            methods=['GET']
        )
        self.add_endpoint(
            endpoint='controller_message',
            name='controller_message',
            handler=self.netweork_controller_message,
            methods=['GET']
        )
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
                request.args.get('ship_id'),
                request.args.get('simulator_address'),
                request.args.get('ship_port')
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
            self._element_details.pop(request.form.get('ship_id'))
            self._network_details.drop(request.form.get("ship_id"))
            res = Response(response=f"Removed Ship: {request.form.get('ship_id')}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling remove_ship request: {repr(e)}", status=400)
        return res

    def add_to_network(self, request:Request):
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
        try:
            ship_id = request.args.get("ship_id")
            shipEntity = self._element_details[ship_id]
            session = requests.Session()
            session.trust_env = False
            # there are no networks yet
            if self._network_details.shape[0] == 0:
                self.__max_network += 1
                self._network_details.loc[self._network_details.shape[0]] = {
                    'ship_id': ship_id,
                    'network': self.__max_network
                }
                shipEntity.create_network(self.controller_endpoint, self.__max_network, True)
                res = Response(response=f"Added to network: {ship_id}", status=200)
                return res
            loc = np.array(shipEntity.loc)

            networkList = []
            for ship in self._network_details.to_dict('records'):
                shipobj = self._element_details[ship['ship_id']]
                refLoc = np.array(shipobj.loc)
                distance = np.linalg.norm(loc - refLoc)
                if distance <= shipEntity.range and distance <= shipobj.range:
                    networkList.append(ship['network'])
            # the ship wasnt added to any networks
            if len(networkList) == 0:
                self.__max_network += 1
                self._network_details.loc[self._network_details.shape[0]] = {
                    'ship_id': shipEntity.id,
                    'network': self.__max_network
                }
                
                shipEntity.create_network(self.controller_endpoint, self.__max_network, True)
                res = Response(response=f"Added to network: {ship_id}", status=200)
                return res
            
            # find the largers network and add the ship
            maxnetwork = self._network_details.loc[self._network_details['network'].isin(networkList)].groupby(['network']).count().idxmax()[0]
            self._network_details.loc[self._network_details.shape[0]] = {
                'ship_id': shipEntity.id,
                'network': maxnetwork
            }
            shipEntity.create_network(self.controller_endpoint, int(maxnetwork), False)
            self._network_details.loc[self._network_details['network'].isin(networkList), 'network'] = maxnetwork
            for ship_id in list(self._network_details.loc[self._network_details['network'].isin(networkList), 'ship_id']):
                self._element_details[ship_id].network = maxnetwork
            # requests.post(url = self.controller_endpoint + '/merge_network', json = {})
            request = session.prepare_request(requests.Request('GET', url=f"{self.controller_endpoint}/merge_network", params={
                    'actualNetwork': maxnetwork, 'mergedNetwork': networkList
                }))
            ouput_res = session.send(request)
            res = Response(response=f"Added to network: {ship_id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling add_to_network request: {repr(e)}", status=400)
        return res

    def netweork_controller_message(self, request:Request):
        try:
            message = request.args.get("message")
            message_type = message.message_type
            dest_id = message.destination
            if message_type.name == 'communication':
                self._element_details[dest_id].receive_message(message)
                res = Response(response=f"Communication success", status=200)
            else:
                for ship_id in self._element_details:
                    self._element_details[ship_id].receive_message(message)
                res = Response(response=f"put Action success", status=200)
        except Exception as e:
            res = Response(response=f"Error handling message_in_range request: {repr(e)}", status=400)
        return res 

    def update(self, request: Request):
        """
        Go through the element_details table to update the ship details

        Parametes:
        None
        Return:

        """
        try:
            for ship_id in self._element_details:
                self._element_details[ship_id].update()
            res = Response(response=f"Have updated", status=200)
            
        except Exception as e:
            res = Response(response=f"Error handling update request: {repr(e)}", status=400)
        return res  
    
    def remove_from_network(self, request: Request):
        try:
            ship_id = request.args.get("ship_id")
            self._network_details.drop([ship_id])
            res = Response(response=f"Remove from network: {ship_id}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling remove from network request: {repr(e)}", status=400)
        return res

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
    parser.add_argument(
        "--endpoint",
        type=str
    )
    args = parser.parse_args()
    hostIP = config['config']['hostIP']
    port = config['config']['port']
    # mock controller manager address
    em = EntityManager(
        address=args.host,
        port=args.port,
        secret=args.secret,
        controller_manager_address=f'http://{hostIP}:{port}/{args.endpoint}')
    em.start_blocking()
    sys.exit(0)
