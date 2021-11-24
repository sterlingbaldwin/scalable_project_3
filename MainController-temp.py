from flask import Flask, request, Response
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
flaskMethods = ['GET', 'POST']

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

def getShipDetails():
    if SHIP_DETAILS.shape[0] > 0:
        return {'error': 'No ship Details yet'}
    return {
        "shipCount": SHIP_DETAILS.shape[0]
        ,"shipIDs": list(SHIP_DETAILS['ShipID'])
    }

app.add_url_rule('/addShips', 'adding Ship', addShip, methods=['GET','POST'])
app.add_url_rule('/GetShipDetails', 'Ship Details', getShipDetails, methods=['GET','POST'])

if __name__=="__main__":
    app.run(
        host=config['MainController']['hostIP']
        ,port=config['MainController']['port']
        ,debug=config['MainController'].getboolean('debug')
    )