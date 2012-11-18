import urllib2
import socket
#Only for python2.6:
import ordereddict as collections
import time

class TimeSeriesData(object):
    """
    Manages requests to a TSD server.
    Some code stolen from the check_tsd script in OpenTSDB.
    """

    accept_keywords = ['start', 'end', 'm', 'o', 'wxh',
                        'yrange', 'y2range', 'ylabel', 'yformat','ylog','y2log',
                        'key', 'nokey','nocache']
            

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = 'http://%s:%s' % (self.host, self.port)

    def put(self, sid, timestamp, value):
        """
        Forward a data point to TSDB server.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        if timestamp == 'now':
            timestamp = int(time.time())
        data_string = ("put data.value %d %f sid=%d\n" % (int(timestamp), 
                                                        float(value),
                                                        int(sid)))
        print data_string
        s.send(data_string)
        s.close()


    def get(self, sid, start, q_params, **kwargs):
        """
        Return the ASCII output of a TSD /q query.
        sid: stream id
        start: start time of the stream
        q_params: additional filter and aggregation parameters
        Accepted kwargs are those defined by the TSD protocol:
        start   The query's start date. 
        end The query's end date.
        m   The query itself.
        nocache Forces TSD to ignore cache and fetch results from HBase.

        Example query:
        http://10.42.0.49:4242/q?start=24h-ago&m=sum:rate:data.value{}&ascii
        """
        params = '/q?start=%s' % start
        try:
            params += '&end=%s' % q_params['end']
        except KeyError:
            pass
        #Now construct the m-query:
        #If we allow multiple streams, we can allow specifying the aggregator
        #m_query = '&m=%s:' % (q_params['agg'] if q_params.has_key('agg') else 'avg')
        #For on data_stream, avg makes sense:
        m_query = '&m=avg:'
        #If this is to be downsampled:
        if q_params.has_key('dsample') and q_params['dsample'] != '':
            m_query += '%s:' % q_params['dsample']
        #If this is a rate stream
        if q_params.has_key('rate') and q_params['rate']=='true':
            m_query += 'rate:'
        m_query += 'data.value{sid=%s}&ascii' % int(sid)
        params += m_query

        print params 

        url = self.url + params
        try:
            data = urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            return None
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            return None

        ret_list = []
        if q_params.has_key('json_format') and q_params['json_format'] == 'rs':
            for line in data.splitlines():
                sp_line = line.split(' ')
                ret_list.append({'x': int(sp_line[1]), 'y': float(sp_line[2])})
            return [{'name': 'series', 'data' : ret_list},]
        else:        
            for line in data.splitlines():
                sp_line = line.split(' ')
                ret_list.append((sp_line[1], sp_line[2]))
            return ret_list

if __name__ == '__main__':
    import json

    tsd = TimeSeriesData('localhost', '4242')
    ret = tsd.get(1, '24h-ago', {})
    print json.dumps(ret)


