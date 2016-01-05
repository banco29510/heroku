#-*- coding: utf-8 -*-
#
# \file urls.py
# \brief Contient les urls des instruments
# \author A. H.
# \date 29 juillet 2014
#

from django.conf.urls import patterns, include, url


from software.views import *


urlpatterns = patterns('',

    url(r'^$', 'software.views.listSoftwares', name="software-list"),
    url(r'^detail/(?P<pk>\d+)$', 'software.views.detailSoftware', name="software-detail"),
    url(r'^create/$', 'software.views.createSoftware', name="software-create"),
    url(r'^update/(?P<pk>\d+)$', 'software.views.updateSoftware', name="software-update"),
    url(r'^delete/(?P<pk>\d+)$', 'software.views.deleteSoftware', name="software-delete"),




)
