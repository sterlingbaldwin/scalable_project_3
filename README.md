# scalable_project_3
Space Mail!

## Project Initializtion Commands
- `python3 -m venv .venv`
- `python3 -m pip install -U pip`
- `python3 -m pip install -r requirements.txt`

## Version 1
- Ships.py: Newly created file contains the ships class
- ShipControlerManagement.py: Functions for Ship mangement from the controler end
- StationaryStations.py: Contains the code for the Starting and end points stationay stations for the ships to traverse between.


# Project Outline

The purpose of this project is to simulate sending email (space mail) between entities in the solar system, who have no direct method of communication (no phone lines between Earth and Mars) and so must rely on currier ships. There are four simulated entity types:

	* Messages: These are the data objects which make their way from a source to their destination
	* Stations: These are stationary objects which generate and receive messages.
	* Ships: These carry messages between stations, and exchange them with other ships.
	* Physics Simulator: In the real world we would call this base reality, however since were not actually sending email to Neptune we’ve gotta simulate it somehow. The physics simulator keeps track of the global state of the system, and mediates communication between the other entities.

Each of the entities exists in a sepperates process, and must use HTTP to communicate. The entities will be spread over the available raspberry pis. Although we only have two pis to work with, the design should work with any number. During initialization, the simulator is created first, and sits waiting for entities to connect to it. As each ship and station is instantiated, it will reach out to the simulator to register its existance.

## Message

The message object is our atomic data unit and consists of the following:

	* Sender, name and station location
	* Receiver, name and optionally last known location
	* checksum
	* if we have time and decide to get fancy, public key of the sender

## Station

As you may guess from their name, a Station is a stationary object. They have a population who generate and transmit/receive messages. A station has the following attributes:

	* Name, the station identifier
	* Population, a list of people. The population simulation doesn’t need to be fancy at all, just a list of randomly generated names  to be used for sending/recieving messages.
	* Population size, this is used to determine the rate of message generation.
	* Location, the physical location of the station.

## Ship

A Ship is basically a much smaller mobile station. The crew on a ship may also generate and receive messages, but at a much lower rate then a station. Ships have the following:

	* Name, the ship identifier
	* Crew, a relatively small number of people on the ship
	* Message list, a list of the messages the ship is carrying
	* Communication range, a potentially fixed radius around the ship that its able to transmit messages. If we get fancy, we can decide to have this variable between ships to make things more interesting.
	* Speed, the rate of movement through the celestial aether.	
    * A bunch of simulated sensor stuff, TBD

## Physics Simulator

The simulation of base reality. This will keep track of all the locations of the ships/stations and let them know who they can communicate with. Although its tempting to try and do a fancy simulation of the orbital mechanics involved in the actual solar system, I (Sterling) believe it to be out of scope of our project, and so I think just a regular 2d grid without a sun, and with the stations assigned to random locations is fine. The simulator will need:

    * A list of stations
    * A list of ships

At each time step, the simulator will iterate over all the ships, and determine if they're in communication range with any other ships or stations. 

### API

	ENDPOINT: /new_entity_connect
	PARAMS: entity_type: either "ship" or "station"
			entity_id: a unique ID for this entity
	RETURNS: location: tuple, the x and y position of the new entity

	This endpoint should be used by all new entities when they're instantiated to register with
	the simulator. The simulator will then response with their location. If its a station, a random
	location will be chosen. If its a ship, then if there are stations available, it will be spawned at one of them, otherwise it will be placed randomly.