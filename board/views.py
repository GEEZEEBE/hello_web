from django.shortcuts import render
from pymongo import MongoClient

db_url = "mongodb://172.17.0.1:27017"
# Create your views here.
def listwithmongo(request):
    data = request.GET.copy()
    with MongoClient(db_url) as client:
        mydb = client.mydb
        result = list(mydb.economic.find({}))
        print(result)
        data['page_obj'] = result

    return render(request, 'board/listwithmongo.html', context=data)


def list_kstartup(request):
    data = request.GET.copy()
    with MongoClient(db_url) as client:
        mydb = client.webscrapDB
        result = list(mydb.kstartupCollection.find({}).sort("_id", -1))
        print(result)
        data['data'] = result

    return render(request, 'board/list_kstartup.html', context=data)


def list_workorkr(request):
    data = request.GET.copy()
    with MongoClient(db_url) as client:
        mydb = client.webscrapDB
        result = list(mydb.workorkrCollection.find({}).sort("_id", -1))
        print(result)
        data['data'] = result

    return render(request, 'board/list_workorkr.html', context=data)
