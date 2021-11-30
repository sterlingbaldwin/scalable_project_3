from flask.wrappers import Request, Response
from server import Server

class Simulator(Server):
    def __init__(self, *args, **kwargs):
        super().init(args, kwargs)
    
    def __call__(self):
        self.super().__call__()
        self.add_endpoint(
            endpoint='/global_event',
            name='global_event',
            handler=self.global_event)
        self._app.run()
    
    def global_event(self, request):
        return Response(response=f"This endpoing has not been implemented yet, come back later!", status=400)
        
