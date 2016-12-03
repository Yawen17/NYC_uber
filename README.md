# New Yorkers, go for Uber or Subway?

## Motivation

We already know a few interesting stories about Uber at the New York City: [Uber Is Serving New York’s Outer Boroughs More Than Taxis Are](http://fivethirtyeight.com/features/uber-is-serving-new-yorks-outer-boroughs-more-than-taxis-are/), [Public Transit Should Be Uber’s New Best Friend](http://fivethirtyeight.com/features/public-transit-should-be-ubers-new-best-friend/), [Uber Is Taking Millions Of Manhattan Rides Away From Taxis](http://fivethirtyeight.com/features/uber-is-taking-millions-of-manhattan-rides-away-from-taxis/), and [Is Uber Making NYC Rush-Hour Traffic Worse?](http://fivethirtyeight.com/features/is-uber-making-nyc-rush-hour-traffic-worse/). But can we learn more about Uber users in NYC given that the New York City has the most advanced public transportation system in the United States?

The answer is Yes. By using Uber pickups and MTA stations open data, we are curious to know: _How do people choose a Uber even there is a subway station around them?_ For example, will New Yorkers still choose Uber even if they are reasonably close (i.e., within walking distance) to a subway stations? Since the New York City has the highest density of subway coverage, and it seems unwise for New Yorkers to pick up Uber instead of the cheaper public transportation alternative.

## How to run
```
python manage.py runserver
```
then go to [here](http://127.0.0.1:8000/)

You need to install [Plotly](https://plot.ly/python/getting-started/) first

## How we choose the data

Our data sources include:

* [NYC Uber Pickups from April to September 2014 (i.e., DB-Uber)](https://github.com/fivethirtyeight/uber-tlc-foil-response)
  * Data on Uber pickups by location (i.e., geographic coordinates) and time (YY:MM:DD HH:MM)

* [NYC Subway Stations (i.e., DB-station)](https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49)
  * Names and locations (i.e., geographic coordinates) of the New York City Subway stations

* [NYC Fare Card history from April to September 2014 (i.e., DB-swipes)](https://data.ny.gov/Transportation/Fare-Card-History-for-Metropolitan-Transportation-/v7qc-gwpn)
  * The number of MetroCard swipes made each week by customers entering each station of the New York City Subway. We assume that all passengers swipe MetroCard once to enter the subway station, and all of them are out-bounded (as passengers do not swipe card to exit and we cannot track them based on this data).This database tells us about total number of people departing a specific subway station every week (instead of taking Uber).

## How we merge the data
### 1. Key of subway stations
Map fare card history to subway stations' total counts

One subway station has multiple remote card stations that passangers can swipe their card on.
Hence the first step is to merge all the affiliated remote stations (DB-swipes) into one subway station they belong to (DB-station). Each subway station has one specific geographic location ploted by Geopy.

### 2. Key of Geo locations
The most critical step is to assign Uber pickup locations to the neareast surrounding subway station.
This can be done by Geopy, matching each pickup location to all subway stations one at a time. By calculating and comparing all the results, python select the shortest distance between two points and match the nearest subway station. All Uber pickup locations are matched up with their nearest subway stations. We then calculate the average distance from nearest MTA station to Uber pick-up locations. Average Distances are saved as outputs in the mta_uber.csv.

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

### Large Merge of Geographic Location Distances

Unlikely general keys, e.g., string or integer, used during databases merge, geographic coordinates cannot be compared simply by theirs equality. The affinity of locations is measured by their distance, aka [Vincenty distance](https://en.wikipedia.org/wiki/Vincenty's_formulae). Fortunately, geopy alreay provides [distance calculation](https://geopy.readthedocs.io/en/1.10.0/#module-geopy.distance).

As a result, to find out the neareset MTA station for a Uber pickup, we have to calculate every distance from the pickup location to each MTA station and then choose the station with the shortest distance. Therefore, for one single pickup, we have to calcualte vincenty distance between this pickup location and all 250 MTA stations' locations to find the minimum one. As shown below, there are 4534333 pickup locations in total from April to September, 2014 and thus we have 250 * 4,534,333, or 1.13 billion distances to calculate. On a Mac Pro with 2.5 GHz Intel Core i7, it takes 80 seconds to process 10,000 pickups (i.e., 250 * 10000 distances) by using one CPU core and thus took 2.5 hours to process all pickups by 4 CPU cores.

```
$ wc -l uber-raw-data-*.csv
  564517 uber-raw-data-apr14.csv
  829276 uber-raw-data-aug14.csv
  796122 uber-raw-data-jul14.csv
  663845 uber-raw-data-jun14.csv
  652436 uber-raw-data-may14.csv
 1028137 uber-raw-data-sep14.csv
 4534333 total
```

Also we find it hard to optimize the data visualization on our website. To intuitively show all the information, namely uber picku amounts, MTA rider amounts and average distance in a single map, we need to utilized several dimensions, and spent a lot of time normalizing the data to optimize the size the color-depth contrast of our visualization.

The extension is another challenge.

## Website Visualization
Here is our [website] ().

We also did experiments in [Tableau](https://public.tableau.com/views/NYCUber/Dashboard1?:embed=y&:display_count=yes) to testify our hypothesis and demostrated initial results before buiding our Django structure. The Tableau dashboard is embedded in our website.

SQL:

Extensions:
we   
![Website Screensot](hhttps://cloud.githubusercontent.com/assets/22580466/20856764/803bf8ec-b8cc-11e6-9834-48d7ffca93b5.png)

## Conclusion

![tableau dashboard](https://cloud.githubusercontent.com/assets/22580466/20686199/867e2b2a-b56c-11e6-9b9a-c747815a31d9.png)

What we can see from the map is that, on the edge of the New York, where the public transit coverage is relatively limited, people who chose to use Uber was usually far away from the available metro station, this was especially the case for people taking Uber near airports; and if people are near enough to those suburban stations, they would in most cases choose subway instead of Uber (probably to save money$).

The counterintuitive things happened in Manhattan, where the public transportation is usually a good option. Yet, New Yorkers are more likely to take Uber in midtown and downtown Manhattan even within walking distance from the subway station (mostly below 300m). The higher the density of passengers in town, the shorter the distances are. we couldn't explain this clearly without further information about the drop-offs and length of these Uber rides. Possible explanations may include that: people living in Manhattan are more wealthy, who can afford to value their time more highly, or they just want to stay away from the dirty MTA. Another explanation maybe that Uber in the core area of the city is a complement to the MTA, it works with the public transit system to substitute the use of the private cars. 

With regard to the policy implications of this attempted exploration, we can see that if Uber took business from taxi and thrives in the area where the public transit system is strong, then policy that part of taxes levied from taxi business to subsidize the MTA should also applied to Uber too.



