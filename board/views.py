from django.shortcuts import render
from pymongo import MongoClient

db_url = "mongodb://127.0.0.1:27017"
# Create your views here.
def listwithmongo(request):
    data = request.GET.copy()
    with MongoClient(db_url) as client:
        mydb = client.mydb
        result = list(mydb.economic.find({}))
        print(result)
        data['page_obj'] = result

    return render(request, 'board/listwithmongo.html', context=data)

from django.core.paginator import Paginator
def listwithmongowithpaginator(request):
    data = request.GET.copy()
    with MongoClient(db_url) as client:
        mydb = client.mydb
        contact_list = list(mydb.economic.find({}))			# get Collection with find()
        for info in contact_list:						# Cursor
            print(info)

    paginator = Paginator(contact_list, 10) # Show 15 contacts per page.

    page_number = request.GET.get('page', 1)
    # page_number = page_number if page_number else 1
    data['page_obj'] = paginator.get_page(page_number)

    for row in data['page_obj']:
        print(f"{row['title']}, {row['link']}")

    return render(request, 'board/listwithmongowithpaginator.html', context=data)


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
