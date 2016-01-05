#-*- coding: utf-8 -*-
#
# \file urls.py
# \brief Contient les urls des instruments
# \author A. H.
# \date 29 juillet 2014
#

from django.conf.urls import patterns, include, url


from author.views import *


urlpatterns = patterns('',

    url(r'^$', 'author.views.listAuthors', name="author-list"),
    url(r'^detail/(?P<pk>\d+)$', 'author.views.detailAuthor', name="author-detail"),
    url(r'^create/$', 'author.views.createAuthor', name="author-create"),
    url(r'^update/(?P<pk>\d+)$', 'author.views.updateAuthor', name="author-update"),
    url(r'^delete/(?P<pk>\d+)$', 'author.views.deleteAuthor', name="author-delete"),




)
