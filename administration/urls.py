from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^dashboard$', views.dashboard, name='administration-dashboard'),
    url(r'^informationsServer$', views.informationsServer, name='administration-informationsServer'),
    url(r'^seo$', views.seo, name='administration-seo'),
    url(r'^admin-commands$', views.managementCommands, name='administration-managementCommands'),
    url(r'^documentation$', views.documentation, name='administration-documentation'),
]
