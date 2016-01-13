#-*- coding: utf-8 -*-
#
# \file urls.py
# \brief Contient les urls pour le logiciel lilypond
# \author A. H.
# \date 29 juillet 2014
#

from  django.conf.urls import include, url

from lilypondSoftware import views 



urlpatterns = [

    url(r'^lilypondMain/$', 'lilypondSoftware.views.main', name="lilypondSoftware-main"),
    url(r'^lilypondCompilation/$', 'lilypondSoftware.views.lilypondCompilation', name="lilypondSoftware-compilation"),
    url(r'^lilypondErrorsCompilation/$', 'lilypondSoftware.views.lilypondErrorsCompilation', name="lilypondSoftware-errorsCompilation"),



]
