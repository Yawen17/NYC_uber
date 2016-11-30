"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.http import HttpResponse

def home(request):
    html = \
"""<h2>Yawen Zhao 454663 & Liping Jiang 454668: Final Project</h2>
<a href="/nyc/4/">Uber NYC</a>
"""
    return HttpResponse(html)

urlpatterns = [
    url(r'^$', home),
    url(r'^nyc/', include('nyc.urls')),
    url(r'^admin/', admin.site.urls),
]
