from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from djangoProject.PullData import PullData
import json


def index(request):
    template = loader.get_template('index.html')
    context = dict()
    pd = PullData()  # Create Pull Data.
    data = pd.read_data('BlueMountain2.geojson')  # Pass data to read from.
    pd.convert_data(data)  # Graph returned from convert_data
    context['ways'] = pd.way_names()

    return render(request, 'index.html', context)

def handle_request(request):
    if request.method == 'POST':
        if 'data' in request.POST:
            del request.session['route']
            array = request.POST['data']
            array = json.loads(array)
            print(array)
            pd = PullData()
            data = pd.read_data('BlueMountain2.geojson')
            pd.convert_data(data)
            print("herie", array[0])
            print("yeet", array[1])
            request.session['route'] = None
            request.session['route'] = pd.find_route(array[0], array[1])
            print(request.session['route'])

            return JsonResponse({'route': request.session['route']})
        else:
            print(request.body)
            array = request.POST['data']
            array = json.loads(array)
            print(array)
    else:
        return JsonResponse({'route': request.session['route']})


