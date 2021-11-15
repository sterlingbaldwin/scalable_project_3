# scalable_project_3
Space Mail!

## Project Initializtion Commands
- `python3 -m venv .venv`
- `source .venv/bin/activate`
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

Each entity will have its own timer and update cycle of some constant ```alpha + uniform(0., beta)```, and during its update will perform the following actions:

1. Send an update message to the simulator with its ID, and speed vector. The simulator will respond with the computed new position from the time delta from last update and the speed. The simulator will also include any messages sent to the craft from other entities since its last update.

2. If the messages include any message_carry requests, it will send the requested messages.


3. The craft will send a radar update request to the simulator, where it will be told of any other craft in radar range. The simulator will respond with the ranges to other entities, and the craft then decides if it should attempt to communicate with them based on its transmission range.


4. Given the results of the radar update, for any new craft in range, the craft will send handshake messages to the simulator bound for the other craft, which they will recieve during their update.


5. If the craft just recieved the handshake response from another craft, it will now transmit the destination list of its message buffer along with its itinerary.


6. If the craft just recieved a destination list of other entities messages buffers, it will check its itinerary, and if its going to be visiting any of the destinations before the other craft (or some other heuristic, for example if it will be getting closer but not actually going to a destination it might request those messages, assuming it'll bump into another craft it can), will transmit which messages its willing to carry. 



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

# API

### new_entity_connect
	ENDPOINT: /new_entity_connect
	PARAMS: 
			entity_type: either "ship" or "station"
			entity_id: a unique ID for this entity
	RETURNS: 
			location: tuple, the x and y position of the new entity

	This endpoint should be used by all new entities when they're instantiated to register with
	the simulator. The simulator will then response with their location. If its a station, a random
	location will be chosen. If its a ship, then if there are stations available, it will be spawned at one of them, otherwise it will be placed randomly.


### update
	ENDPOINT: /update
	PARAMS: 
			src_id: the entities UUID
			speed: the velocity vector of the entity
	RETURNS: 
			location: the new position of the craft
			messages: a list of message objects

	This is the start of an entities update cycle. It sends to the simulator its speed, and gets its updated position and any messages that are bound for it.


### ping
	ENDPOINT: /ping
	PARAMS: 
			src_id: the source entity UUID
			location: the source location
	RETURNS:
			entitys[List]: a list of UUIDs of any entities in radar range


### syn
	ENDPOINT: /syn
	PARAMS:
			src_id: the source entity UUID
			dst_id: the destination entity UUID
	RETURNS:
			void

	This is the endpoint used by an entity to establish a communication channel with another entity


### ack
	ENDPOINT: /ack
	PARAMS:
			src_id: the source entity UUID
			dst_id: the destination entity UUID
			itinerary[List]: the list of locations the entity is planning on visiting
	RETURNS:
			void
	
	After recieving a "syn" message from another craft, each entity will respond with an "ack" along with the list of locations its going to be visiting in the future.


### message_carry_request
	ENDPOINT: /message_carry_request
	PARAMS:
			src_id: the source entity UUID
			dst_id: the destination entity UUID
			messages[List]: the UUIDs of the messages the entity is willing to carry
	
	After opening a commuinication channel with another craft, and recieving the other entities itinerary, the craft will send a request to the other entity requesting that it carry any messages its holding that are bound for destinations on its itinerary.

### message_carry_response
	ENDPOIND: /message_carry_reponse
	PARAMS:
			src_id: the source entity UUID
			dst_id: the destination entity UUID
			messages[List]: a list of message that the source wants to have the destination carry for it
	RETURNS:
			void
	
<<<<<<< HEAD
	This is the response to being send a message asking to carry other messages
=======
	This is the response to being send a message asking to carry other messages
>>>>>>> 44a7935 (readme update)
