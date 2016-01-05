#-*- coding: utf-8 -*-
#
# \file urls.py
# \brief Contient les urls des instruments
# \author A. H.
# \date 29 juillet 2014
#

from django.conf.urls import patterns, include, url


from licence.views import *


urlpatterns = patterns('',

    url(r'^$', 'licence.views.listLicences', name="licence-list"),
    url(r'^detail/(?P<pk>\d+)$', 'licence.views.detailLicence', name="licence-detail"),
    url(r'^create/$', 'licence.views.createLicence', name="licence-create"),
    url(r'^update/(?P<pk>\d+)$', 'licence.views.updateLicence', name="licence-update"),
    url(r'^delete/(?P<pk>\d+)$', 'licence.views.deleteLicence', name="licence-delete"),




)
