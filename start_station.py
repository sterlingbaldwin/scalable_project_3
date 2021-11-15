from Station import station
from numpy.random import uniform
from numpy import round
from sys import argv

print('++ creating station object ++')
s = station(
    population=round(uniform(10, 10_000)),
    address=argv[1],
    port=argv[2],
    stationId=argv[3])
print('++ calling station run ++')
s.run()
