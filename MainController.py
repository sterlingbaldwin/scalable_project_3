from flask import Flask, request
from typing import Union
import configparser
import pandas as pd
import numpy as np
import datetime
import re

from setup_stations import main

SHIP_DETAILS = pd.DataFrame(columns=['ShipID', 'port', 'Address', 'Speed', 'CommunicationRange', 'location', 'pingTime'])
STATION_DETAILS = pd.DataFrame(columns=['StationID', 'port', 'Address', 'location', 'pingTime'])
COMMUNICATION_TABLE = pd.DataFrame(columns=['Entity1Type', 'Entity1', 'Entity2Type', 'Entity2'])

config = configparser.ConfigParser()
config.read('Environment.ini')
app = Flask(__name__)

def addShip():
    """Add new Ship details in the controler PI
    """
    if request.method == 'POST':
        inputShipDetails = request.json
        inputShipDetails['pingTime'] = datetime.datetime.now()
        print(inputShipDetails)
        SHIP_DETAILS.loc[SHIP_DETAILS.shape[0]] = request.json
        return f'Ship count is {SHIP_DETAILS.shape[0]}'
    else:
        return """
        This is method needs to be run using post method with json entry similar to the one below:

        {
            'ShipID':shipID,
            'port':port,
            'Address':address,
            'Speed':speed,
            'CommunicationRange':comRange,
            'location':'x:{}, y:{}'.format(loc[0], loc[1]), #here loc[0] coresponds to the x position and loc[1] the corresponding y
        }
        """

def addStation(StationID:str, port:str, address:str, loc:tuple):
    """Add new Ship details in the controler PI

    Args:
        StationID (str): New Station ID
        port (str): Entity port for Communication
        address (str): Communication address of the ship
        loc (tuple): Ships location
    """
    STATION_DETAILS.loc[STATION_DETAILS.shape[0]] = {
        'StationID':StationID,
        'port':port,
        'Address':address,
        'location':'x:{}, y:{}'.format(loc[0], loc[1]),
        'pingTime': datetime.datetime.now()
    }

def updateDetails(entityType:str, ID:str, para:str, value:Union[str,tuple]):
    """[summary]

    Args:
        entityType (str): [description]
        ID (str): ID of the  that needs to change
        para (str): parameter to change
        value (Union[str,tuple]): Details value
    """
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
        loc1 = np.array(re.findall(r'\d+', strloc1))
        for j in range(i, SHIP_DETAILS.shape[0]):
            strloc2 = SHIP_DETAILS.loc[j, 'location']
            range2 = int(SHIP_DETAILS.loc[i, 'CommunicationRange'])
            loc2 = np.array(re.findall(r'\d+', strloc2))
            dist = np.linalg.norm(loc1 - loc2)
            if dist <= range1 & dist <= range2:
                COMMUNICATION_TABLE.loc[COMMUNICATION_TABLE.shape[0]] = {
                    'Entity1Type':'ship',
                    'Entity1':SHIP_DETAILS.loc[i, 'ShipID'],
                    'Entity2Type':'ship',
                    'Entity2':SHIP_DETAILS.loc[j, 'ShipID']
                }
        for j in range(STATION_DETAILS):
            strloc2 = STATION_DETAILS.loc[j, 'location']
            loc2 = np.array(re.findall(r'\d+', strloc2))
            dist = np.linalg.norm(loc1 - loc2)
            if dist <= range1:
                COMMUNICATION_TABLE.loc[COMMUNICATION_TABLE.shape[0]] = {
                    'Entity1Type':'ship',
                    'Entity1':SHIP_DETAILS.loc[i, 'ShipID'],
                    'Entity2Type':'station',
                    'Entity2':STATION_DETAILS.loc[j, 'StationID']
                }




app.add_url_rule('/addShips', 'adding Ship', addShip, methods=['GET','POST'])

if __name__=="__main__":
    app.run(
        host=config['MainController']['hostIP']
        ,port=config['MainController']['port']
        ,debug=config['MainController'].getboolean('debug')
    )
