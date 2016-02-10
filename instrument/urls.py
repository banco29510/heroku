#
# \file urls.py
# \brief Contient les urls des instruments
# \author A. H.
# \date 18/03/2015
#

from django.conf.urls import include, url


from . import views


urlpatterns = [

    url(r'^$', views.listInstruments, name="instrument-list"),
    url(r'^detail/(?P<pk>\d+)$', views.detailInstrument, name="instrument-detail"),
    url(r'^create/$', views.createInstrument, name="instrument-create"),
    url(r'^update/(?P<pk>\d+)$', views.updateInstrument, name="instrument-update"),
    url(r'^delete/(?P<pk>\d+)$', views.deleteInstrument, name="instrument-delete"),




]
