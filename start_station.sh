#!/bin/bash

cd projects/scalable_project_3
source .venv/bin/activate
echo "Starting station on $HOSTNAME communicating with $1:$2"
python3 -c "

from Station import station
from numpy.random import uniform
from numpy import round
from uuid import uuid4

s = station(
    population=round(uniform(10, 100_00)),
    stationId=uuid4().hex, 
    address='$1',
    port='$2')
s.run()

" &
