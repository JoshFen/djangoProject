from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from djangoProject.PullData import PullData


def index(request):
    template = loader.get_template('index.html')
    context = dict()
    pd = PullData()  # Create Pull Data.
    data = pd.read_data('BlueMountain2.geojson')  # Pass data to read from.
    ski_graph = pd.convert_data(data)  # Graph returned from convert_data.
    context['ways'] = pd.way_names()

    return render(request, 'index.html', context)