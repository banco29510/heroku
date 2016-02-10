#
# \file urls.py
# \brief Contient les urls des instruments
# \author A. H.
# \date 29 juillet 2014
#

from django.conf.urls import patterns, include, url


from . import views


urlpatterns = [

    url(r'^$', views.listSoftwares, name="software-list"),
    url(r'^detail/(?P<pk>\d+)$', views.detailSoftware, name="software-detail"),
    url(r'^create/$', views.createSoftware, name="software-create"),
    url(r'^update/(?P<pk>\d+)$', views.updateSoftware, name="software-update"),
    url(r'^delete/(?P<pk>\d+)$', views.deleteSoftware, name="software-delete"),


]
