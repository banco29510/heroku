from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^dashboard$', 'administration.views.dashboard', name='administration-dashboard'),
    url(r'^informationsServer$', 'administration.views.informationsServer', name='administration-informationsServer'),
    url(r'^seo$', 'administration.views.seo', name='administration-seo'),
    url(r'^admin-commands$', 'administration.views.managementCommands', name='administration-managementCommands'),
    url(r'^documentation$', 'administration.views.documentation', name='administration-documentation'),
]
