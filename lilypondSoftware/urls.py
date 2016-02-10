#
# \file urls.py
# \brief Contient les urls pour le logiciel lilypond
# \author A. H.
# \date 29 juillet 2014
#

from  django.conf.urls import include, url

from . import views



urlpatterns = [

    url(r'^lilypondMain/$', views.main, name="lilypondSoftware-main"),
    url(r'^lilypondCompilation/$', views.lilypondCompilation, name="lilypondSoftware-compilation"),
    url(r'^lilypondErrorsCompilation/$', views.lilypondErrorsCompilation, name="lilypondSoftware-errorsCompilation"),



]
