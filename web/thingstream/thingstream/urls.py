from django.conf.urls import patterns, include, url

#API Stuff
from tastypie.api import Api
from api.resources import TimeSeriesResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#API Setup
v1_api = Api(api_name='v1')
v1_api.register(TimeSeriesResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'timeseries.views.main', name='home'),
    url(r'^graph$', 'timeseries.views.graph', name='graph'),    
    url(r'^console$', 'timeseries.views.console', name='console'),    

    # url(r'^hello/', include('hello.foo.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    #TastyPie config: 
    (r'^api/', include(v1_api.urls)),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
