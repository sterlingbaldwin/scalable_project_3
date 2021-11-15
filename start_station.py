from Station import station
from numpy.random import uniform
from numpy import round
from uuid import uuid4

print('++ creating station object ++')
s = station(
    population=round(uniform(10, 100_00)),
    stationId=uuid4().hex, 
    address='$1',
    port='$2')
print('++ calling station run ++')
s.run()