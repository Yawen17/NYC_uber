import sqlite3
import plotly
import plotly.plotly as py

import pandas as pd
import plotly.tools as tls

from plotly.graph_objs import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.conf import settings
from django import forms
from django.db import models
from matplotlib import pyplot

from .forms import InputForm
from .models import Input, MONTHS, MONTHS_DICT

pd.set_option('display.max_colwidth', -1)

def motivation(request):
    contents = {}
    contents['title'] = "Motivation"
    contents['content'] = \
"""
<p>
We already know a few interesting stories about Uber at the New York City.
But can we learn more about Uber users in NYC given that the New York City has the most advanced
public transportation system in the United States?

The answer is Yes. By using Uber pickups and MTA stations open data, we are curious to know: How do
people choose a Uber even there is a subway station around them? For example, will New Yorkers still
choose Uber even if they are reasonably close (i.e., within walking distance) to a subway stations?
Since the New York City has the highest density of subway coverage, and it seems unwise for New
Yorkers to pick up Uber instead of the cheaper public transportation alternative.
</p>
"""

    return render(request, 'index.html', contents)

def more(request):
    contents = {}
    contents['title'] = "Resources and Archive"
    contents['content'] = \
"""
<ul>
<li><p><a href="https://github.com/fivethirtyeight/uber-tlc-foil-response">NYC Uber Pickups from
April to September 2014 (i.e., DB-Uber)</a></p>

<ul>
<li>Data on Uber pickups by location (i.e., geographic coordinates) and time (YY:MM:DD
HH:MM)</li>
</ul></li>
<li><p><a href="https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49">NYC
Subway Stations (i.e., DB-station)</a></p>

<ul>
<li>Names and locations (i.e., geographic coordinates) of the New York City Subway stations</li>
</ul></li>
<li><p><a
href="https://data.ny.gov/Transportation/Fare-Card-History-for-Metropolitan-Transportation-/v7qc-gwpn">NYC
Fare Card history from April to September 2014 (i.e., DB-swipes)</a></p>

<ul>
<li>The number of MetroCard swipes made each week by customers entering each station of the New
York City Subway. We assume that all passengers swipe MetroCard once to enter the subway
station, and all of them are out-bounded (as passengers do not swipe card to exit and we cannot
track them based on this data).This database tells us about total number of people departing a
specific subway station every week (instead of taking Uber).</li>
</ul></li>
</ul>

<p>You can read more about this topic on: <a
href="http://fivethirtyeight.com/features/uber-is-serving-new-yorks-outer-boroughs-more-than-taxis-are/">Uber
Is Serving New York’s Outer Boroughs More Than Taxis Are</a>, <a
href="http://fivethirtyeight.com/features/public-transit-should-be-ubers-new-best-friend/">Public
Transit Should Be Uber’s New Best Friend</a>, <a
href="http://fivethirtyeight.com/features/uber-is-taking-millions-of-manhattan-rides-away-from-taxis/">Uber
Is Taking Millions Of Manhattan Rides Away From Taxis</a>, and <a
href="http://fivethirtyeight.com/features/is-uber-making-nyc-rush-hour-traffic-worse/">Is Uber
Making NYC Rush-Hour Traffic Worse?</a>.
</p>
"""
    return render(request, 'index.html', contents)

def plot(month=4):
    plotly.tools.set_credentials_file(username='Yawen', api_key='ar6lJE4Ml2baADcPw5f2')

    mapbox_access_token = \
        'pk.eyJ1IjoiY2hlbHNlYXBsb3RseSIsImEiOiJjaXFqeXVzdDkwMHFrZnRtOGtlMGtwcGs4In0.SLidkdBMEap9POJGIe1eGw'

    color_scale = [
        [0, 'rgb(0,68,27)'],
        [0.1, 'rgb(0,109,44)'],
        [0.2, 'rgb(35,139,69)'],
        [0.3, 'rgb(65,174,118)'],
        [0.4, 'rgb(102,194,164)'],
        [0.5, 'rgb(253,187,132)'],
        [0.6, 'rgb(252,141,89)'],
        [0.7, 'rgb(239,101,72)'],
        [0.8, 'rgb(215,48,31)'],
        [0.9, 'rgb(179,0,0)'],
        [1, 'rgb(127,0,0)']]

    conn = sqlite3.connect('data.sqlite3')
    cur = conn.cursor()

    lats = []
    lons = []
    locations_name = []
    size = []
    ubers = []
    mtas = []

    def normalize_size(size):
        if size <= 10: return size
        elif size <= 100: return size / 4
        elif size <= 1000: return size / 30
        elif size <= 10000: return size / 150

    for row in cur.execute("SELECT station,lat,lon,mta,uber,avg_dist FROM mta_uber where month='%s'" % \
        month):
        name, lat, lon, mta, uber, dist = row
        locations_name.append("%s/14,%s: %s pickups within %.0fm vs. MTA %s" % \
            (month, name, uber, float(dist), mta))
        ubers.append(int(uber))
        mtas.append(int(mta))
        lats.append(float(lat))
        lons.append(float(lon))
        size.append(normalize_size(int(dist)))

    data = Data([
        Scattermapbox(
            lat=lats,
            lon=lons,
            mode='markers',
            marker=dict(
                cmax=max(ubers),
                cmin=min(ubers),
                color=ubers,
                colorscale=color_scale,
                size=size,
                opacity=0.5
            ),
            text=locations_name,
            hoverinfo='text'
        )]
    )

    layout = Layout(
        title='NYC Uber Pickups near MTA Stations',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat= 40.74221633326165,
                lon=-73.9489160011607
            ),
            pitch=0,
            zoom=10,
            style='streets'
        ),
        width=1100,
        height=900
    )

    fig = dict(data=data, layout=layout)
    url = py.plot(fig, filename='NYC Uber Pickups near MTA Stations', auto_open=False)
    #py.image.save_as(fig, filename='uber.png')
    return url

def show_nyc(request):

    contents = {}

    month = request.GET.get('month', '4')
    contents['title'] = "NYC Uber Pickups around MTA Stations %s 2014" % MONTHS_DICT[month]

    if not month: month = request.POST.get('month', '4')

    params = {'form_action' : reverse_lazy('nyc:show_nyc'),
              'form_method' : 'get',
              'form' : InputForm({'month' : month}),
              'month' : MONTHS_DICT[month]}
    contents.update(params)

    url = plot(month)
    contents['map'] = tls.get_embed(url, height=900)

    conn = sqlite3.connect('data.sqlite3')
    df = pd.read_sql("SELECT station,mta,uber,avg_dist FROM mta_uber WHERE month='%s'"
                     " GROUP BY STATION ORDER BY CAST(uber as unsigned) DESC" % month, conn)
    table = df.to_html(float_format = "%.3f", classes = "table table-striped",
        columns=range(4), col_space=50, justify='left', index_names=False, escape=False)
    contents['table'] = table

    return render(request, 'index.html', contents)
