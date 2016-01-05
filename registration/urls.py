from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    (r'^login$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html', 'name': 'login',},)

)
