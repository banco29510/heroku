#
# \file urls.py
# \brief Contient les urls des auteurs
# \author A. H.
# \date 29 juillet 2014
#

from django.conf.urls import include, url


from . import views


urlpatterns = [

    url(r'^$', views.listAuthors, name="author-list"),
    url(r'^detail/(?P<pk>\d+)$', views.detailAuthor, name="author-detail"),
    url(r'^create/$', views.createAuthor, name="author-create"),
    url(r'^update/(?P<pk>\d+)$', views.updateAuthor, name="author-update"),
    url(r'^delete/(?P<pk>\d+)$', views.deleteAuthor, name="author-delete"),


]
