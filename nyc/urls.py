from django.conf.urls import url

from . import views

app_name = 'nyc'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<month>[0-9\_]+)/$', views.show_nyc),
    url(r'^form/$', views.form, name = "form"),
    url(r'^formclass/$', views.FormClass.as_view(), name = "formclass"),
]
