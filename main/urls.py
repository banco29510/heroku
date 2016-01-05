from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^cgu$', 'main.views.cgu', name="main-cgu"),
)
