#!/usr/bin/env python

# Get Remote station's GPS coordinates

import csv
import re
import geopy
import time
from collections import defaultdict

TRANSACTIONS_FILE = 'MTA_Fare_Card_Transactions.csv'
COORDS_FILE = 'MTA_Coords.csv'

geolocator = geopy.geocoders.googlev3.GoogleV3()

station_addrs = defaultdict(str) # id -> addr
# Build in-memory station ID -> coordinates index map
with open(TRANSACTIONS_FILE, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)  # Skip the header
    for row in reader:
        station_id = row[2]
        address = row[3]
        if station_id not in station_addrs:
            station_addrs[station_id] = address

with open(COORDS_FILE, 'a') as csvfile: # append, just in case exceeded request limit
    writer = csv.writer(csvfile, delimiter=',')
    for id in sorted(station_addrs.keys()):
        coords = geolocator.geocode(station_addrs[id] + ", New York")
        if coords:
            writer.writerow([id, coords.latitude, coords.longitude])
            print('{}: {}, {}'.format(id, coords.latitude, coords.longitude))
        else:
            writer.writerow([id, 'None', 'None'])
            print('warning: cannot get {}: {}'.format(id, station_addrs[id]))
        time.sleep(1)
