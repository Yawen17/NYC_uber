#!/usr/bin/env python

import sqlite3
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

import pandas as pd

plotly.tools.set_credentials_file(username='dun', api_key='ei8wtwn2tf')

mapbox_access_token = 'pk.eyJ1IjoiY2hlbHNlYXBsb3RseSIsImEiOiJjaXFqeXVzdDkwMHFrZnRtOGtlMGtwcGs4In0.SLidkdBMEap9POJGIe1eGw'

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

for row in cur.execute('SELECT station,lat,lon,mta,uber,avg_dist FROM mta_uber'):
    name, lat, lon, mta, uber, dist = row
    locations_name.append("%s: %s pickups within %.0fm vs. MTA %s" % (name, uber, float(dist), mta))
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
py.plot(fig, filename='NYC Uber Pickups near MTA Stations')
#py.image.save_as(fig, filename='uber.png')
