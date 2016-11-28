# New Yorkers, go for Uber or Subway?

## Motivation
We already know a few interesting stories about Uber at the New York City: [Uber Is Serving New York’s Outer Boroughs More Than Taxis Are](http://fivethirtyeight.com/features/uber-is-serving-new-yorks-outer-boroughs-more-than-taxis-are/), [Public Transit Should Be Uber’s New Best Friend](http://fivethirtyeight.com/features/public-transit-should-be-ubers-new-best-friend/), [Uber Is Taking Millions Of Manhattan Rides Away From Taxis](http://fivethirtyeight.com/features/uber-is-taking-millions-of-manhattan-rides-away-from-taxis/), and [Is Uber Making NYC Rush-Hour Traffic Worse?](http://fivethirtyeight.com/features/is-uber-making-nyc-rush-hour-traffic-worse/). But can we learn more about Uber users in NYC given that the New York City has the most advanced public transportation system in the United States?

The answer is Yes. By using Uber pickups and MTA stations open data, we are curious to know: _How do people choose a Uber even there is a subway station around them?_

## How we choose the data
Basically, we start with the question, "will New Yorkers still choose Uber even if they are rather close (say, reasonably walking distance) from the subway stations?" This can be a rather interesting topic as the New York City has the highest density of subway coverage, and it seems unwise for New Yorkers to call Uber instead of walking just 200m to take the public transportation. 

So, here come our data sources:

* [NYC Uber Pickups from April to September 2014 (i.e., DB-Uber)](https://github.com/fivethirtyeight/uber-tlc-foil-response)
  * Data on Uber pickups by location and time
  
* [NYC Subway Stations (i.e., DB-station)](https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49)
  * Locations of the New York City Subway stations 
   
  
* [NYC Fare Card history from April to September 2014 (i.e., DB-swipes)](https://data.ny.gov/Transportation/Fare-Card-History-for-Metropolitan-Transportation-/v7qc-gwpn)
  * The number of MetroCard swipes made each week by customers entering each station of the New York City Subway. We assume that all passengers swipe MetroCard once to enter the subway station, and all of them are out-bounded (as passengers do not swipe card to exit and we cannot track them based on this data).This database tells us about total number of people departing a specific subway station every week (instead of taking Uber). 
  

## How we merge the data
### 1. Key of subway stations
Map fare card history to subway stations' total counts

One subway station has multiple remote card stations that passangers can swipe their card on.
Hence the first step is to merge all the affiliated remote stations (DB-swipes) into one subway station they belong to (DB-station). Each subway station has one specific geographic location ploted by Geopy.

### 2. Key of Geo locations
The most critical step is to assign Uber pickup locations to the neareast surrounding subway station.
This can be done by Geopy, matching each pickup location to all subway stations one at a time. By calculating and comparing all the results, python select the shortest distance between two points and match a subway station. All Uber pickup locations are matched up with their nearest subway station. We then calculate the average distance from nearest MTA station to Uber pick-up locations. Distances are outputs in this regard.

### 3. Key of dates
Merge the weekly data of DB-swipes into monthly data, identical to the DB-Uber timeline.

### 4. Database specification

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

## Challenges

## Website Visualization

## Conclusion
