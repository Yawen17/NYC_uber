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
from .models import Input, STATES, STATES_DICT

pd.set_option('display.max_colwidth', -1)

class InputForm(forms.ModelForm):
    attrs = {'class ' : 'form−control ',
             'onchange ' : 'this.form.submit() '}
    state = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    class Meta:

        model = Input
        fields = ['state']

def to_link_name(county_name):
    name = county_name.lower().replace(' county', '') \
        .replace(' city', '') \
        .replace('(', '') \
        .replace(')', '') \
        .replace('.', '') \
        .strip() \
        .replace(' ', '_')
    return name

def index(request, month=4):
    contents = {}
    contents['title'] = "NYC Uber Pickups around MTA Stations April - September 2014"

    return render(request, 'index.html', contents)

def plot(month=4):
    plotly.tools.set_credentials_file(username='Yawen', api_key='ar6IJE4MI2baADcPw5f2')

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

from django.views.generic import FormView
class FormClass(FormView):
    template_name = 'index.html'
    form_class = InputForm


    def get(self, request):

      state = request.GET.get('state', 'PA')

      return render(request, self.template_name, {'form_action' : reverse_lazy('nyc:formclass'),
                                                  'form_method' : 'get',
                                                  'form' : InputForm({'state' : state}),
                                                  'state' : STATES_DICT[state]})

    def post(self, request):

      state = request.POST.get('state', 'PA')

      return render(request, self.template_name, {'form_action' : reverse_lazy('nyc:formclass'),
                                                  'form_method' : 'get',
                                                  'form' : InputForm({'state' : state}),
                                                  'state' : STATES_DICT[state]})

from .forms import InputForm
from .models import STATES_DICT

def form(request):

    state = request.GET.get('state', '')
    if not state: state = request.POST.get('state', 'PA')

    params = {'form_action' : reverse_lazy('nyc:form'),
              'form_method' : 'get',
              'form' : InputForm({'state' : state}),
              'state' : STATES_DICT[state]}

    return render(request, 'index.html', params)


from django.views.generic import FormView
class FormClass(FormView):
    template_name = 'index.html'
    form_class = InputForm


    def get(self, request):
      state = request.GET.get('state', 'PA')
      return render(request, self.template_name, {'form_action' : reverse_lazy('nyc:formclass'),
                                                  'form_method' : 'get',
                                                  'form' : InputForm({'state' : state}),
                                                  'state' : STATES_DICT[state]})

    def post(self, request):
      state = request.POST.get('state', 'PA')
      return render(request, self.template_name, {'form_action' : reverse_lazy('nyc:formclass'),
                                                  'form_method' : 'get',
                                                  'form' : InputForm({'state' : state}),
                                                  'state' : STATES_DICT[state]})

def show_nyc(request, month=4):
    url = plot(month)

    contents = {}
    contents['title'] = "NYC Uber Pickups around MTA Stations 2014/%s" % month
    contents['map'] = tls.get_embed(url, height=900)

    return render(request, 'index.html', contents)
