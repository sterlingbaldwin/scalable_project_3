from typing import Union
import pandas as pd
import numpy as np
import datetime
import re

from Ship import ship
from flask import Flask, Response, request

SHIP_DETAILS = pd.DataFrame(columns=['ShipID', 'port', 'Address', 'Speed', 'CommunicationRange', 'location', 'pingTime'])
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
    def __init__(self, host:str = "127.0.0.1", port: str = "3000") -> None:
        self.ship_details = pd.DataFrame(columns=['ShipID', 'port', 'Address', 'Speed', 'CommunicationRange', 'location', 'pingTime'])
        self.station_details = pd.DataFrame(columns=['StationID', 'port', 'Address', 'location', 'pingTime'])
        self.communication_table = pd.DataFrame(columns=['Entity1Type', 'Entity1', 'Entity2Type', 'Entity2'])
        self.host = host
        self.port = port
        self._app = None

    def __call__(self):
        self._app = Flask(__name__)
        self.add_endpoint(
            endpoint='/add_ship',
            name="add_ship",
            handler=self.addShip
        )
        self.add_endpoint(
            endpoint='/add_station',
            name="add_station",
            handler=self.addStation
        )
        self.add_endpoint(
            endpoint='/update_details',
            name="update_details",
            handler=self.updateDetails
        )
        self.add_endpoint(
            endpoint='/ping',
            name="ping",
            handler=self.ping
        )
        print(f"Starting the server with address {self.host}")
        self._app.run(host=self.host, port=self.port)

    def add_endpoint(self, endpoint, name, handler):
        self._app.add_url_rule(endpoint, name, EndpointAction(handler), methods=['GET', "POST"])

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
        shipID = request.form.get("shipID"),
        port = request.form.get("port")
        address = request.form.get("address")
        speed = request.form.get("speed")
        comRange = request.form.get("comRange")
        loc = request.form.getlist("loc")
        SHIP_DETAILS.loc[SHIP_DETAILS.shape[0]] = {
            'ShipID':shipID,
            'port':port,
            'Address':address,
            'Speed':speed,
            'CommunicationRange':comRange,
            'location':'x:{}, y:{}'.format(loc[0], loc[1]),
            'pingTime': datetime.datetime.now()
        }
        res = Response(response=f"{shipID} has been created", status=200)
        return res

    def addStation(self, request):
        """Add new Ship details in the controler PI

        Args:
            StationID (str): New Station ID
            port (str): Entity port for Communication
            address (str): Communication address of the ship
            loc (tuple): Ships location
        """
        StationID = request.form.get("StationID")
        port = request.form.get("port")
        address = request.form.get("address")
        loc = request.form.getlist("loc")
        STATION_DETAILS.loc[STATION_DETAILS.shape[0]] = {
            'StationID':StationID,
            'port':port,
            'Address':address,
            'location':'x:{}, y:{}'.format(loc[0], loc[1]),
            'pingTime': datetime.datetime.now()
        }
        res = Response(response=f"{StationID} has been created", status=200)
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
            SHIP_DETAILS.loc[SHIP_DETAILS['ShipID'] == ID, para] = val
        elif entityType == 'station':
            STATION_DETAILS.loc[STATION_DETAILS['StationID'] == ID, para] = val

    def communicationPairing():
        for i in range(SHIP_DETAILS.shape[0]):
            strloc1 = SHIP_DETAILS.loc[i, 'location']
            range1 = int(SHIP_DETAILS.loc[i, 'CommunicationRange'])
            loc1 = np.array(list(map(float, np.array(re.findall(r'\d+', strloc1)))))
            for j in range(i, SHIP_DETAILS.shape[0]):
                strloc2 = SHIP_DETAILS.loc[j, 'location']
                range2 = int(SHIP_DETAILS.loc[i, 'CommunicationRange'])
                loc2 = np.array(list(map(float, np.array(re.findall(r'\d+', strloc2)))))
                dist = np.linalg.norm(loc1 - loc2)
                if dist <= range1 and dist <= range2:
                    COMMUNICATION_TABLE.loc[COMMUNICATION_TABLE.shape[0]] = {
                        'Entity1Type':'ship',
                        'Entity1':SHIP_DETAILS.loc[i, 'ShipID'],
                        'Entity2Type':'ship',
                        'Entity2':SHIP_DETAILS.loc[j, 'ShipID']
                    }
            for j in range(STATION_DETAILS.shape[0]):
                strloc2 = STATION_DETAILS.loc[j, 'location']
                loc2 = np.array(list(map(float, np.array(re.findall(r'\d+', strloc2)))))
                dist = np.linalg.norm(loc1 - loc2)
                if dist <= range1:
                    COMMUNICATION_TABLE.loc[COMMUNICATION_TABLE.shape[0]] = {
                        'Entity1Type':'ship',
                        'Entity1':SHIP_DETAILS.loc[i, 'ShipID'],
                        'Entity2Type':'station',
                        'Entity2':STATION_DETAILS.loc[j, 'StationID']
                    }
    
    def ping(self, request):
        pass

controller = Controller()
controller()