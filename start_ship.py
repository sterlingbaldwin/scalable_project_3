from Ship import ship
from numpy.random import random
from uuid import uuid4

s = ship(
    shipId=uuid4().hex, 
    address='$1',
    port='$2')
s.run()