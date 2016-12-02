from django.conf.urls import url

from . import views

app_name = 'nyc'
urlpatterns = [
    url(r'^$', views.show_nyc, name='show_nyc'),
#    url(r'^(?P<month>[0-9\_]+)/$', views.show_nyc, name = "show_nyc"),
]
