# How people make their decisions to take Uber instead of subways in NYC?

## How we choose the data
Here are our data sources, one on Uber pickups by location and time, and the other on NYC subway station .
 - NYC Uber Pickups from April to September 2014: https://github.com/fivethirtyeight/uber-tlc-foil-response
 - NYC Subway Stations: https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49

##Database Specification

COLUMNS: month, station, latitude, longitude, mta, uber, distance

Description
Month: Month of this row
Station: Name of the station
Latitude: Latitude of the station
Longtitude: Longtitude of the station
MTA: Total OUT rides from this station
Uber: Total Uber pickups which nearest to this station 
Distance: The sum of distances of all Uber pickups from pickup location to the nearest station


GUI
Plot stations by latitude and longitude
At each station, shows,
MTA: How many people using MTA
Uber: How many people using Uber
Distance / Uber: Average distance from nearest MTA station to Uber pick-up locations
