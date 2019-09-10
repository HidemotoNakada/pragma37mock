from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.template.loader import *
from django.shortcuts import render

import json
from mysite.nbdummy import *

class item_list:
    def __init__(self, name, item_list):
        self.name = name
        self.list = item_list


mod_list = item_list('mod', {
        'solar': "Solar Panel Detector", 
        'hotspot': "Hotspot Detector", 
})

cr_list = item_list('cr', {
        'abci': "Japan: AIST ABCI", 
        'nchc': "Taiwan: NCHC Cluster", 
})


dr_list = item_list('dr',  {
        'landsat': "Japan: Landsat 8 Satelite Data",
        'formosat': "Taiwan: Formosat Satelite Data", 
})    

def index(request):
    return  render(request, 'index.html', {
        'dr_list': dr_list,
        'cr_list': cr_list,
        'mod_list': mod_list,
    }, content_type='text/html')

def index2(request):
    return  render(request, 'index2.html', {
        'dr_list': dr_list,
        'cr_list': cr_list,
        'mod_list': mod_list,
    }, content_type='text/html')

nbm = NotebookManager()


@csrf_exempt
def launch(request):
    d = request.POST
    print(d)
    nbm.launch(d["cr"], d["dr"], d["mod"])
    return HttpResponse(
        content='{"result" : "success"}',
        content_type='application/json')


nb = {"id": "0x0000", "time":"2019/9/12 00:00:00", "url": "https://localhost:8000", "status":"shutdown"}
nb2 = {"id": "0x0001", "time":"2019/9/12 00:00:00", "url": "https://localhost:8000", "status":"shutdown"}


def notebooks(request):
    return HttpResponse(
        content=json.dumps(nbm.getStatusDictList()),
        content_type='application/json')

@csrf_exempt
def shutdown(request):
    print(request.POST['id'])
    nbm.shutdown(request.POST['id'])
    return HttpResponse(
        content='{"result" : "success"}',
        content_type='application/json')
