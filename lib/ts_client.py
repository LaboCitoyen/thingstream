#!/usr/bin/python

import urllib2
import json

"""
curl --dump-header - -H "Accept: application/json" -H "Content-Type: application/json"   
-X POST --data '{"timestamp": "now", "value": {$1}}' 
"http://thingstream.com/api/v1/timeseries/2/data/?username=test1&api_key=623171139baf2c6c99b6ca033b2f048ef173fc91"
"""
class ThingStream(object):

    API_URL = 'http://thingstream.com/api/v1/timeseries/{sid}/data/?username={username}&api_key={api_key}'

    def __init__(self, username, api_key, stream_id):

        self.username = username
        self.api_key = api_key
        self.stream_id = int(stream_id)
        self.url = self.API_URL.format(**{'sid': self.stream_id,
                                   'username' : self.username,
                                   'api_key' : self.api_key })

    def push_data(self, value, timestamp='now'):
        data_struct = {'timestamp' : timestamp,
                        'value' : value }
        data_json = json.dumps(data_struct)

        opener = urllib2.build_opener()
        opener.addheaders = [('Accept', 'application/json'), 
                              ('Content-Type', 'application/json')]
        req = urllib2.Request(url=self.url, data=data_json)
        opener.open(req)
