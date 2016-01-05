#
# \file urls.py
# \brief Contient les urls des instruments
# \author A. H.
# \date 18/03/2015
#

from django.conf.urls import patterns, include, url


from instrument.views import *


urlpatterns = patterns('',

    url(r'^$', 'instrument.views.listInstruments', name="instrument-list"),
    url(r'^detail/(?P<pk>\d+)$', 'instrument.views.detailInstrument', name="instrument-detail"),
    url(r'^create/$', 'instrument.views.createInstrument', name="instrument-create"),
    url(r'^update/(?P<pk>\d+)$', 'instrument.views.updateInstrument', name="instrument-update"),
    url(r'^delete/(?P<pk>\d+)$', 'instrument.views.deleteInstrument', name="instrument-delete"),




)
