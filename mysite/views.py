from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.template.loader import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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



@login_required(login_url='/login')
def index(request):
    return  render(request, 'index.html', {
        'dr_list': dr_list,
        'cr_list': cr_list,
        'mod_list': mod_list,
    }, content_type='text/html')


@login_required(login_url='/login')
def index2(request):
    return  render(request, 'index2.html', {
        'dr_list': dr_list,
        'cr_list': cr_list,
        'mod_list': mod_list,
    }, content_type='text/html')

nbm = NotebookManager()


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def notebooks(request):
    return HttpResponse(
        content=json.dumps(nbm.getStatusDictList()),
        content_type='application/json')


@login_required(login_url='/login')
@csrf_exempt
def shutdown(request):
    print(request.POST['id'])
    nbm.shutdown(request.POST['id'])
    return HttpResponse(
        content='{"result" : "success"}',
        content_type='application/json')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return HttpResponse(
        content='<h1>logged out</h1>',
        content_type='text/html')

def login_view(request):
    return  render(request, 'login.html', 
    content_type='text/html')

from django.contrib.auth import authenticate, login

@csrf_exempt
def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index2.html')
    else:
        return  render(request, 'failed.html', 
                content_type='text/html')
        


from django.contrib.auth.models import User
def createuser():
    user = User.objects.create_user('pragma', 'hidemoto.nakada@gmail.com', 'pragmademo')
    user.save()


#createuser()