#!/usr/bin/env python

# Count Uber Pickups close to Stations

import csv
import re
import sys
import time
from collections import defaultdict, Counter
from geopy.distance import vincenty

if len(sys.argv) < 2:
    print("usage: %s YYMM" % sys.argv[0])
    sys.exit(1)

STATIONS_FILE = 'mta_%s.csv' % sys.argv[1]
COORD_PATTERN = r'[-+]?\d*\.\d+|\d+'
UBER_FILE = 'uber_%s.csv' % sys.argv[1]
UBER_OUTBOUND_FILE = 'uber_outbound_%s.csv' % sys.argv[1]

def closet_station(stations, point):
    min_distance = float('inf')
    min_station = None
    for station, coords in stations.items():
        distance = vincenty(coords, point).meters
        if distance < min_distance:
            min_distance = distance
            min_station = station
    return min_station, min_distance

# Build in-memory stations index using dictionary, since it is very small
stations = defaultdict(list)
coord_pattern = re.compile(COORD_PATTERN)
with open(STATIONS_FILE, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        _, name, lat, lon, _ = row
        stations[name] = (lat, lon)
print("load %d stations coordinates" % len(stations.keys()))

start_time = time.time()
with open(UBER_OUTBOUND_FILE, 'w') as out_csvfile:
    writer = csv.writer(out_csvfile, delimiter=',')
    writer.writerow(['station','lat','lon','uber','dist'])
    station_total = Counter()
    station_total_distance = Counter()
    with open(UBER_FILE, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # Skip the header
        for i, row in enumerate(reader):
            _, lat, lon, _ = row
            closest, distance = closet_station(stations, (lat, lon))
            #print(closest, distance)
            station_total[closest] += 1
            station_total_distance[closest] += distance
            if i % 10000 == 0:
                print(i, time.time() - start_time)
    for st in station_total:
        writer.writerow([st, station_total[st], station_total_distance[st]])
