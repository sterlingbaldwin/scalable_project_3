from flask import Flask, request, Response
import pandas as pd
import numpy as np
import datetime
import re
from datetime import datetime

import requests

from Station import station

SHIP_DETAILS = pd.DataFrame(columns=['ShipID', 'port', 'Address', 'Speed', 'Communication_range', 'location', 'pingTime'])
STATION_DETAILS = pd.DataFrame(columns=['StationID', 'port', 'Address', 'location', 'pingTime'])
COMMUNICATION_TABLE = pd.DataFrame(columns=['Entity1Type', 'Entity1', 'Entity2Type', 'Entity2'])

class EndpointAction:
    def __init__(self, action):
        self.action = action
        self.response = None

    def __call__(self, *args):
        self.response = self.action(request)
        return self.response

class Controller:
    def __init__(self, host:str = "127.0.0.1", port: str = "3000", size:int = 100_000) -> None:
        self.ship_details = pd.DataFrame(columns=['ship_id', 'port', 'address', 'speed', 'communicationRange', 'location', 'pingTime'])
        self.station_details = pd.DataFrame(columns=['station_id', 'port', 'address', 'location', 'pingTime'])
        self.communication_table = pd.DataFrame(columns=['Entity1Type', 'Entity1', 'Entity2Type', 'Entity2'])
        self.host = host
        self.port = port
        self._app = None
        self._world_size = size
        self._time = datetime.now()
        self._stations = []
        self._ships = []

    def __call__(self):
        self._app = Flask(__name__)
        self.add_endpoint(
            endpoint='/add_ship',
            name="add_ship",
            handler=self.addShip)
        self.add_endpoint(
            endpoint='/add_station',
            name="add_station",
            handler=self.addStation)
        self.add_endpoint(
            endpoint='/update_details',
            name="update_details",
            handler=self.updateDetails)
        self.add_endpoint(
            endpoint='/ping',
            name="ping",
            handler=self.ping)
        self.add_endpoint(
            endpoint='/syn', 
            name='syn',
            handler=self.syn)
        self.add_endpoint(
            endpoint='/ack', 
            name='ack',
            handler=self.ack)
        self.add_endpoint(
            endpoint='/message_carry_request', 
            name='message_carry_request',
            handler=self.message_carry_request)
        self.add_endpoint(
            endpoint='/message_carry_reponse', 
            name='message_carry_reponse',
            handler=self.message_carry_reponse)
        print(f"Starting the controller with address {self.host}")
        self._app.run(host=self.host, port=self.port)

    def add_endpoint(self, endpoint, name, handler):
        self._app.add_url_rule(endpoint, name, EndpointAction(handler), methods=['GET', "POST"])
    
    def message_carry_reponse(self, request):
        print(f"message_carry_reponse with {request}")
        res = Response(response=f"", status=400)
        return res

    def message_carry_request(self, request):
        print(f"message_carry_request with {request}")
        res = Response(response=f"", status=400)
        return res

    def ack(self, request):
        print(f"ack with {request}")
        res = Response(response=f"", status=400)
        return res

    def syn(self, request):
        print(f"syn with {request}")
        res = Response(response=f"", status=400)
        return res

    def addShip(self, request):
        """Add new Ship details in the controler PI

        Args:
            shipID (str): New Ship ID
            port (str): Entity port for Communication
            address (str): Communication address of the ship
            speed (str): Ship's Speed
            comRange (str): Ship's Communication range
            loc (tuple): Ships location
        """
        try:
            ship_id = request.form.get("ship_id")
            port = request.form.get("port")
            address = request.form.get("address")
            speed = request.form.get("speed")
            comRange = request.form.get("comRange")
            loc = request.form.getlist("loc")
            self.ship_details.loc[self.ship_details.shape[0]] = {
                'ship_id':ship_id,
                'port':port,
                'address':address,
                'speed':speed,
                'communicationRange':comRange,
                'location':f'x:{loc[0]}, y:{loc[1]}',
                'pingTime': datetime.now()
            }
            res = Response(response=f"new ship with id={ship_id} has connected", status=200)
        except Exception as e:
            res = Response(response=f"Error handling addShip request: {repr(e)}", status=400)
        return res

    def addStation(self, request):
        """Add new Ship details in the controler PI

        Args:
            StationID (str): New Station ID
            port (str): Entity port for Communication
            address (str): Communication address of the ship
            loc (tuple): Ships location
        """
        try:
            station_id = request.form.get("station_id")
            port = request.form.get("port")
            address = request.form.get("address")
            loc = request.form.getlist("loc")
            print(self.station_details.shape[0])
            self.station_details.loc[self.station_details.shape[0]] = {
                'station_id':station_id,
                'port':port,
                'address':address,
                'location':f'x:{loc[0]}, y:{loc[1]}',
                'pingTime': datetime.now()
            }
        
            res = Response(response=f"new station with id={station_id} has connected", status=200)
        except Exception as e:
            res = Response(response=f"Error handling addStation request: {repr(e)}", status=400)
        return res

    def updateDetails(self, request):
        """[summary]

        Args:
            entityType (str): [description]
            ID (str): ID of the  that needs to change
            para (str): parameter to change
            value (Union[str,tuple]): Details value
        """
        entityType = request.form.get("entityType")
        ID = request.form.get("ID")
        para = request.form.get("para")
        value = request.form.get("value")
        if isinstance(value, tuple) & para == 'location':
            val = 'x:{}, y:{}'.format(value[0], value[1])
        else:
            val = value
        if entityType == 'ship':
            self.ship_details.loc[self.ship_details['ShipID'] == ID, para] = val
        elif entityType == 'station':
            self.station_details.loc[self.station_details['StationID'] == ID, para] = val

    def communicationPairing(self):
        for i in range(self.ship_details.shape[0]):
            strloc1 = self.ship_details.loc[i, 'location']
            range1 = int(self.ship_details.loc[i, 'CommunicationRange'])
            loc1 = np.array(list(map(float, np.array(re.findall(r'\d+', strloc1)))))
            for j in range(i, self.ship_details.shape[0]):
                strloc2 = self.ship_details.loc[j, 'location']
                range2 = int(self.ship_details.loc[i, 'CommunicationRange'])
                loc2 = np.array(list(map(float, np.array(re.findall(r'\d+', strloc2)))))
                dist = np.linalg.norm(loc1 - loc2)
                if dist <= range1 and dist <= range2:
                    self.communication_table.loc[self.communication_table.shape[0]] = {
                        'Entity1Type':'ship',
                        'Entity1':self.ship_details.loc[i, 'ShipID'],
                        'Entity2Type':'ship',
                        'Entity2':self.ship_details.loc[j, 'ShipID']
                    }
            for j in range(self.station_details.shape[0]):
                strloc2 = self.station_details.loc[j, 'location']
                loc2 = np.array(list(map(float, np.array(re.findall(r'\d+', strloc2)))))
                dist = np.linalg.norm(loc1 - loc2)
                if dist <= range1:
                    self.communication_table.loc[self.communication_table.shape[0]] = {
                        'Entity1Type':'ship',
                        'Entity1':self.ship_details.loc[i, 'ShipID'],
                        'Entity2Type':'station',
                        'Entity2':self.station_details.loc[j, 'StationID']
                    }
    
    def ping(self, request):
        """[summary]

        Args:
            shipID: the id of the ship which needs to be pinged
        """
        try:
            shipID = request.args.get("entity_id")
            output = []
            print(shipID)
            print(self.ship_details)
            location = self.ship_details.loc[self.ship_details['ship_id']==shipID]['location'].to_string(index=False)
            communication_range = self.ship_details.loc[self.ship_details['ship_id']==shipID]['communicationRange'].to_string(index=False)
            loc1 = np.array(list(map(float, np.array(re.findall(r'\d+', location)))))
            print(loc1)
            for i in range(self.ship_details.shape[0]):
                if self.ship_details.loc[i, 'ship_id'] == shipID:
                    continue
                else:
                    str_loc2 = self.ship_details.loc[i, 'location']
                    loc2 = np.array(list(map(float, np.array(re.findall(r'\d+', str_loc2)))))
                    print(loc2)
                    distance = np.linalg.norm(loc1 - loc2)
                    if distance <= float(communication_range):
                        output.append(self.ship_details.loc[i, 'ship_id'])
            print(output)
            res = Response(response=f"{output}", status=200)
        except Exception as e:
            res = Response(response=f"Error handling addStation request: {repr(e)}", status=400)
        return res
