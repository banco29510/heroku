from django.conf.urls import patterns, include, url

from . import views

urlpatterns = [
    
    url(r'^cgu$', views.cgu, name="main-cgu"),
    url(r'^profile$', views.profile, name="main-profile"),
    
]
