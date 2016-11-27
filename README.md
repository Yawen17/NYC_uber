# New Yorkers, go for Uber or subway?

## How we choose the data
Basically, we start with the question, "will New Yorkers still choose Uber even if they are rather close (say, reasonably walking distance) from the subway stations?" This can be a rather interesting topic as the New York City has the highest density of subway coverage, and it seems unwise for New Yorkers to call Uber instead of walking just 200m to take the public transportation. 

So, here come our data sources:
* NYC Uber Pickups from April to September 2014: https://github.com/fivethirtyeight/uber-tlc-foil-response
  *Data on Uber pickups by location and time
  
* NYC Subway Stations: https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49
  *Locations of the New York City Subway stations
  
* NYC Fare Card history from April to September 2014: https://data.ny.gov/Transportation/Fare-Card-History-for-Metropolitan-Transportation-/v7qc-gwpn
  *The number of MetroCard swipes made each week by customers entering each station of the New York City Subway
  

## How we merge the data

### *Database Specification*

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
