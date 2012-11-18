from django.db import models
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource, Resource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from timeseries.models import TimeSeries
import api.opentsd as opentsd
from django.conf.urls import patterns, include, url
import json

TSD_HOST = 'localhost'
TSD_PORT = 4242

class TimeSeriesResource(ModelResource):

    allowed_q_params = ['end', 'agg', 'dsample', 'rate', 'json_format']
    class Meta:
        queryset = TimeSeries.objects.all()
        allowed_methods = ['get']
        #include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

    #To allow the datastream as a sub-query to a timeseries:
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/data/$" % (self._meta.resource_name), 
                                                            self.wrap_view('map_data'), name="api_map_data"),
        ]

    def _client(self):
        return opentsd.TimeSeriesData(TSD_HOST, TSD_PORT)

    def map_data(self, request, **kwargs):
        """
        Allows requesting data streams and posting new datum elements.
        """
        #Check API key here;
        auth_answer = self._meta.authentication.is_authenticated(request)
        if auth_answer != True:
            return auth_answer
        #Ok, user is authenticated
        client = self._client()
        #Accept incoming data point(s)
        if request.META.get('REQUEST_METHOD') == 'POST':
            if TimeSeries.objects.get(pk=kwargs['pk']).user != request.user:
                return HttpUnauthorized()
            #TimeSeries.
            print request.POST.items()
            datum = json.loads(request.POST.items()[0][0])
            print datum
            client.put(kwargs['pk'], datum['timestamp'], datum['value'])
            return self.create_response(request, datum)
        #Return data:
        else:
            try:
                start = request.GET['start']
            except KeyError:
                start = '6h-ago' #Sane default value
            q_params = {}
            q_params.update(dict([(key, request.GET[key]) for key in self.allowed_q_params if request.GET.has_key(key)]))
            ret_val = client.get(kwargs['pk'], start=start, q_params=q_params,)
            return self.create_response(request, ret_val)