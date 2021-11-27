from flask import Flask, request, Response
from flask.wrappers import Request

class EndpointAction:
    def __init__(self, action):
        self.action = action
        self.response = None

    def __call__(self, *args):
        self.response = self.action(request)
        return self.response

class Server:
    def __init__(self) -> None:
        self._app = None
        pass

    def __call__(self) -> None:
        self._app = Flask(__name__)
    
    def add_endpoint(self, endpoint: str, name: str, handler: function) -> None:
        self._app.add_url_rule(endpoint, name, EndpointAction(handler), methods=['GET', "POST"])