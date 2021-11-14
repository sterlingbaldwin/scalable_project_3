#!/bin/bash

cd projects/scalable_project_3
source venv/bin/activate
python -c "

from Station import station
from numpy.random import random
from uuid import uuid4

s = station(
    population=random(10, 100_00),
    stationID=uuid4.hex(), 
    address=$1,
    port=$2)
s.connect()

" &
