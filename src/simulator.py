import os
import paramiko
import requests
from random import choice
from server import Server
from uuid import uuid4
from pathlib import Path
import urllib
from flask.wrappers import Request, Response


SSH_KEY = f"{os.environ['HOME']}/.ssh/id_rsa.pub"
USER = os.environ['USER']
PROJECT_PATH = f"source /users/pgrad/{USER}/projects/scalable_project_3/"
SRC_VENV = f"source .venv/bin/activate"
PI_ADDRESSES = {
    "controllers": ["10.35.70.29"], 
    "entities": ["10.35.70.30"]
}

class Simulator(Server):
    def __init__(self, *args, **kwargs):
        super().init(args, kwargs)
        self._num_ships = kwargs.get('num_ships')
        self._world_size = kwargs.get('world_size')
        self._entity_managers = {ip: uuid4().hex for ip in PI_ADDRESSES["entities"]}
        self._controller_managers = {ip: uuid4().hex for ip in PI_ADDRESSES["controllers"]}
        self.add_endpoint(
            endpoint='/global_event',
            name='global_event',
            handler=self.global_event)
        self._app.run()
    
    def __call__(self):
        self.setup_entity_manager()
        self.setup_controller_manager()
        for _ in range(self._num_ships):
            self.generate_ship()

    def generate_ship(self):
        pass

    def send_request(self, url, params=None):
        session = requests.Session()
        session.trust_env = False
        if params is not None:
            url += f"?{urllib.parse.urlencode(params)}"  
        request = session.prepare_request(requests.Request("GET", url))
        if not request.status_code == 200:
            print(f"Got an error response to request: {url}; {request.content}")

    def shuwdown_services(self):
        managers = dict(self._entity_managers, **self._controller_managers)
        for ip, secret in managers.items():
            print(f"shutting down {ip}")
            url = f"http://{ip}/shutdown"
            self.send_request(url, {'secret': secret})

    def setup_entity_manager(self):
        # pick one of the addresses reserved for the entity manager
        manager_address = choice(PI_ADDRESSES["entities"])
        logdir = "./logs"
        
        cmd = f'cd {PROJECT_PATH}; {SRC_VENV};  python entity_manager.py 0.0.0.0 {self._port} {self._entity_manager_secrets[manager_address]} > {Path(logdir).absolute()}/entity_manager.out 2>&1; echo Running on process: $?'

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
        logdir = "./logs"
        
        cmd = f'cd {PROJECT_PATH}; {SRC_VENV};  python controller_manager.py 0.0.0.0 {self._port} {self._controller_manager_secrets[manager_address]} > {Path(logdir).absolute()}/controller_manager.out 2>&1; echo Running on process: $?'

        new_client = paramiko.SSHClient()
        new_client.load_system_host_keys()
        new_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        new_client.connect(manager_address, username=USER, key_filename=SSH_KEY)

        print(f"executing command: {cmd}")
        new_client.exec_command(cmd)
        print(f"Finished setting up the Controller Manager on {manager_address}")
    
    def global_event(self, request):
        return Response(response=f"This endpoing has not been implemented yet, come back later!", status=400)
        
