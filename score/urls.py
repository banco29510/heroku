"""score URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'main.views.main', name="main"), # page d'accueil
    
    url(r'^accounts/', include('allauth.urls')),

    url(r'^main/', include('main.urls')),
    url(r'^repository/', include('repository.urls')),
    url(r'^instrument/', include('instrument.urls')),
    url(r'^licence/', include('licence.urls')),
    url(r'^author/', include('author.urls')),
    url(r'^software/', include('software.urls')),
    url(r'^administration/', include('administration.urls')),
    url(r'^lilypondSoftware/', include('lilypondSoftware.urls')),
]

handler404 = 'main.errors.error404'
handler500 = 'main.errors.error500'