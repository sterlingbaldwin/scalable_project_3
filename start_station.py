from Station import station
from numpy.random import uniform
from numpy import round
from uuid import uuid4
from sys import argv

print('++ creating station object ++')
s = station(
    population=round(uniform(10, 100_00)),
    address=argv[1],
    port=argv[2],
    stationId=argv[3])
print('++ calling station run ++')
s.run()
