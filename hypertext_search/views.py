import os
from django.shortcuts import render, redirect
from elasticsearch_dsl.query import Q
from .models import WebPage
from .pageRank import rank_func
from .search import WebPageIndex, bulk_indexing
import http.client
http.client._MAXHEADERS = 10000


def index(request):
    input_text = request.POST.get('input', '')
    if input_text:
        result = WebPageIndex.search().query(Q('match', url=input_text))
    else:
        result = ''
    return render(request, 'index.html', {'result': result})


def get_all(request):
    result = WebPage.objects.all()[0:]
    return render(request, 'index.html', {'result': result})


def start_crawler(request):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    rank_func()
    return redirect(index)


def bulk_index(request):
    bulk_indexing()
    return redirect(index)

