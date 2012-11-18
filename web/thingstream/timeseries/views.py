from django.shortcuts import render_to_response
# Create your views here.
def main(request):
    return render_to_response('timeseries/index.html')

def graph(request):
    return render_to_response('timeseries/graph.html')
