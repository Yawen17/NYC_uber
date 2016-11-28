#!/usr/bin/env python

# Merge MTA Fare Transcations into Stations

import csv
import re
from collections import defaultdict, Counter
from geopy.distance import vincenty


TRANSACTIONS_FILE = 'MTA_Fare_Card_Transactions_2014_04_09.csv'
STATIONS_FILE = 'MTA_Stations.csv'
COORDS_FILE = 'MTA_Coords.csv'
MTA_OUTBOUND_FILE = 'MTA_Outbound.csv'
COORD_PATTERN = r'[-+]?\d*\.\d+|\d+'

def closest_station(stations, point):
    min_distance = float('inf')
    min_station = None
    for station, coords in stations.items():
        distance = vincenty(coords, point).meters
        if distance < min_distance:
            min_distance = distance
            min_station = station
    return min_station

# Build in-memory stations index using dictionary, since it is very small
stations = defaultdict(list)
coord_pattern = re.compile(COORD_PATTERN)
with open(STATIONS_FILE, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)  # Skip the header
    for row in reader:
        coord, name, _, line = row
        # Extract coordinates
        longtitude, latitude = coord_pattern.findall(coord)
        station_key = "{} ({})".format(name, line)
        stations[station_key] = (latitude, longtitude)
        #print(station_key), stations[station_key]

# Build in-memory stations index using dictionary, since it is very small
remote_stations_coords = defaultdict(list)
with open(COORDS_FILE, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)  # Skip the header
    for row in reader:
        remote_stations_coords[row[0]] = (float(row[1]), float(row[2]))

# Merge remote stations ID to stations
remote2station = defaultdict(str)
for rid, coords in remote_stations_coords.items():
    remote2station[rid] = closest_station(stations, coords)

with open(MTA_OUTBOUND_FILE, 'w') as out_csvfile:
    writer = csv.writer(out_csvfile, delimiter=',')
    writer.writerow(['month','station','lat','lon','mta'])
    with open(TRANSACTIONS_FILE, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # Skip the header
        station_total = Counter()
        current_month = 0
        for row in reader:
            month = int(row[0][0:2])
            remote_station_id = row[2]
            station = remote2station[remote_station_id]
            total = sum(int(value) for value in row[4:])
            if month != current_month:
                for st in station_total:
                    la, lo = stations[st]
                    writer.writerow([current_month, st, la, lo, station_total[st]])
                    station_total[st] = 0
                current_month = month
            station_total[station] += total
    # Flush last month
    for st in station_total:
        la, lo = stations[st]
        writer.writerow([current_month, st, la, lo, station_total[st]])
