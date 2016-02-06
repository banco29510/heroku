from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^cgu$', 'main.views.cgu', name="main-cgu"),
    url(r'^login$', 'main.views.MyLogin', name="main-login"),
    url(r'^profile$', 'main.views.profile', name="main-profile"),
)
