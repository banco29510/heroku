#
# \file urls.py
# \brief Contient les urls des instruments
# \author A. H.
# \date 29 juillet 2014
#

from django.conf.urls import include, url


from . import views


urlpatterns = [

    url(r'^$', views.listLicences, name="licence-list"),
    url(r'^detail/(?P<pk>\d+)$', views.detailLicence, name="licence-detail"),
    url(r'^create/$', views.createLicence, name="licence-create"),
    url(r'^update/(?P<pk>\d+)$', views.updateLicence, name="licence-update"),
    url(r'^delete/(?P<pk>\d+)$', views.deleteLicence, name="licence-delete"),




]
