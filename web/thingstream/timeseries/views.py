from django.shortcuts import render_to_response
import api.opentsd as opentsd

TSD_HOST = 'localhost'
TSD_PORT = 4242

# Create your views here.
def main(request):
    return render_to_response('timeseries/index.html')

def graph(request):
    return render_to_response('timeseries/graph.html')

def console(request):
    ot = opentsd.TimeSeriesData(TSD_HOST, TSD_PORT)
    ret = ot.get(3, start='10m-ago', q_params={'dsample' : '1m-avg'})
    try:
        foo = int(float(ret[-1][1]))
    except IndexError:
        foo = 0
    #foo = 5
    return render_to_response('timeseries/console.html', dict(foo=foo))


