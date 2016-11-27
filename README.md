# New Yorkers, go for Uber or Subway?

## How we choose the data
Basically, we start with the question, "will New Yorkers still choose Uber even if they are rather close (say, reasonably walking distance) from the subway stations?" This can be a rather interesting topic as the New York City has the highest density of subway coverage, and it seems unwise for New Yorkers to call Uber instead of walking just 200m to take the public transportation. 

So, here come our data sources:

* NYC Uber Pickups from April to September 2014 (short for "DB-Uber"): https://github.com/fivethirtyeight/uber-tlc-foil-response
  * Data on Uber pickups by location and time.  
  
* NYC Subway Stations (short for "DB-station"): https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49
  * Locations of the New York City Subway stations 
   
  
* NYC Fare Card history from April to September 2014 (short for "DB-swipes"): https://data.ny.gov/Transportation/Fare-Card-History-for-Metropolitan-Transportation-/v7qc-gwpn
  * The number of MetroCard swipes made each week by customers entering each station of the New York City Subway. We assume that all passengers swipe MetroCard once to enter the subway station, and all of them are out-bounded (as passengers do not swipe card to exit and we cannot track them based on this data).This database tells us about total number of people departing a specific subway station every week (instead of taking Uber). 
  

## How we merge the data
### 1. Key of subway station: Map fare card history to subway stations' total counts
One subway station has multiple remote card stations that passangers can swipe their card on.
Hence the first step is to merge all the affiliated remote stations (DB-swipes) into one subway station they belong to (DB-station).

### 2. Key of date: Merge the weekly data of DB-swipes into monthly data, identical to DB-Uber


### Database specification*

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
