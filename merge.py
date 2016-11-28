#!/usr/bin/env python

# Count Uber Pickups close to Stations

import csv
import re
import sys
import sqlite3
import time
from collections import defaultdict, Counter
from geopy.distance import vincenty

stations = defaultdict(defaultdict)
with open('mta.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)  # Skip the header
    for row in reader:
        month = row[0]
        name = row[1]
        stations[month][name] = list(row)

with open('data.csv', 'w') as out_csvfile:
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS mta_uber(
               month, station, lat, lon, mta, uber, avg_dist)""")
    writer = csv.writer(out_csvfile, delimiter=',')
    writer.writerow(['month', 'station','lat','lon','mta','uber','avg_dist'])
    with open('uber.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # Skip the header
        for row in reader:
            month, name, uber, dist = row
            data = stations[month][name]
            data.append(uber)
            data.append(float(dist)/int(uber))
            writer.writerow(data)
            cur.execute("INSERT INTO mta_uber VALUES (?,?,?,?,?,?,?);", data)

    conn.commit()
    conn.close()
