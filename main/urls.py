from django.conf.urls import patterns, include, url

from . import views

urlpatterns = [
    
    url(r'^cgu$', views.cgu, name="main-cgu"),
    url(r'^login$', views.MyLogin, name="main-login"),
    url(r'^logout$', views.MyLogout, name="main-logout"),
    url(r'^register$', views.MyRegistration, name="main-register"),
    url(r'^profile$', views.profile, name="main-profile"),
    
]
