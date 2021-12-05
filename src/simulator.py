import os
import paramiko
import requests
import json
from random import choice
from server import Server
from uuid import uuid4
from pathlib import Path
from time import sleep
import urllib
from requests.exceptions import ConnectionError
from flask.wrappers import Request, Response


SSH_KEY = f"{os.environ['HOME']}/.ssh/id_rsa.pub"
USER = os.environ['USER']
PROJECT_PATH = f"/users/pgrad/{USER}/projects/scalable_project_3/"
VENV_PATH = f".venv/bin/activate"
PI_ADDRESSES = {
    "controllers": ["10.35.70.29"], 
    "entities": ["10.35.70.30"]
}

class Simulator(Server):
    def __init__(self, *args, **kwargs):
        super(Simulator, self).__init__(*args, **kwargs)
        self._num_ships = kwargs.get('num_ships')
        self._world_size = kwargs.get('world_size')
        self._dont_setup = kwargs.get('dont_setup')
        self._entity_managers = {
            ip: {
                'secret': uuid4().hex,
                'port': 0 
            } for ip in PI_ADDRESSES["entities"]}
        self._controller_managers = {
            ip: {
                'secret': uuid4().hex,
                'port': 0 
            } for ip in PI_ADDRESSES["controllers"]}
        self.add_endpoint(
            endpoint='/global_event',
            name='global_event',
            handler=self.global_event)
    
    def __call__(self):
        self.start()
        if self._dont_setup:
            manager_info = self._entity_managers[PI_ADDRESSES["entities"][0]]
            manager_info['port'] = self._port + 1
            
            manager_info = self._entity_managers[PI_ADDRESSES["controllers"][0]]
            manager_info['port'] = self._port + 1
        else:
            self.setup_entity_manager()
            self.setup_controller_manager()
        sleep(3) # give flask some time to get up and running
        for _ in range(self._num_ships):
            self.generate_ship()
        self.update_cycle()

    def update_cycle(self):
        while True:
            sleep(1)

    def generate_ship(self):
        ship_data = {
            "ship_id": uuid4().hex,
            "simulator_address": self._address,
            "ship_port": self._port }
        ip = choice(PI_ADDRESSES["entities"])
        url = f"http://{ip}:{self._entity_managers[ip]['port']}/add_ship"
        self.send_request(url=url, method="GET", params=ship_data)

    def send_request(self, url, method="GET", params=None):
        session = requests.Session()
        session.trust_env = False
        if method == "GET": 
            if params is not None:
                url += f"?{urllib.parse.urlencode(params)}"
            req = requests.Request("GET", url)
        elif method == "POST":
            if params is not None:
                data = json.dumps(params)
            else:
                data = {}
            req = requests.Request("POST", url, data=data)
        
        print(f"Sending {method} request to url: {url}")
        res = session.send(session.prepare_request(req))
        if not res.status_code == 200:
            print(f"Got an error response to request: {url}; {res.content}")

    def shutdown_services(self):
        managers = dict(self._entity_managers, **self._controller_managers)
        for ip, info in managers.items():
            print(f"shutting down {ip}")
            url = f"http://{ip}:{info['port']}/shutdown"
            try:
                self.send_request(url, "GET", {'secret': info['secret']})
            except ConnectionError:
                print("Client disconnected")

    def setup_entity_manager(self):
        # pick one of the addresses reserved for the entity manager
        manager_address = choice(PI_ADDRESSES["entities"])
        manager_info = self._entity_managers[manager_address]
        manager_info['port'] = self._port + 1
        cmd = f'cd {PROJECT_PATH}; source {VENV_PATH}; cd src; python entity_manager.py --host 0.0.0.0 --port {manager_info["port"]} --secret {manager_info["secret"]} > ../logs/entity_manager.out 2>&1;'

        new_client = paramiko.SSHClient()
        new_client.load_system_host_keys()
        new_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        new_client.connect(manager_address, username=USER, key_filename=SSH_KEY)

        print(f"executing command: {cmd}")
        new_client.exec_command(cmd)
        print(f"Finished setting up the Entity Manager on {manager_address}")

    def setup_controller_manager(self):
        # pick one of the addresses reserved for the entity manager
        manager_address = choice(PI_ADDRESSES["controllers"])
        manager_info = self._controller_managers[manager_address]
        manager_info['port'] = self._port + 1
        cmd = f'cd {PROJECT_PATH}; source {VENV_PATH}; cd src; python controller_manager.py --host 0.0.0.0 --port {manager_info["port"]} --secret {manager_info["secret"]} > ../logs/controller_manager.out 2>&1;'

        new_client = paramiko.SSHClient()
        new_client.load_system_host_keys()
        new_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        new_client.connect(manager_address, username=USER, key_filename=SSH_KEY)

        print(f"executing command: {cmd}")
        new_client.exec_command(cmd)
        print(f"Finished setting up the Controller Manager on {manager_address}")
    
    def global_event(self, request):
        return Response(response=f"This endpoing has not been implemented yet, come back later!", status=400)
        
