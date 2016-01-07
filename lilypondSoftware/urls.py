#-*- coding: utf-8 -*-
#
# \file urls.py
# \brief Contient les urls des instruments
# \author A. H.
# \date 29 juillet 2014
#

from django.conf.urls import patterns, include, url



urlpatterns = patterns('',

    url(r'^lilypondMain/$', 'lilypondSoftware.views.main', name="lilypondSoftware-main"),
    url(r'^lilypondCompilation/$', 'lilypondSoftware.views.lilypondCompilation', name="lilypondSoftware-compilation"),
    url(r'^lilypondErrorsCompilation/$', 'lilypondSoftware.views.lilypondErrorsCompilation', name="lilypondSoftware-errorsCompilation"),



)
