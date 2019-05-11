import subprocess
import os
import time
from django.shortcuts import render, redirect
from elasticsearch_dsl.query import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import WebPage
from .pageRank import rank_func
from .search import WebPageIndex, bulk_indexing
import http.client
http.client._MAXHEADERS = 10000


def index(request):
    input_text = request.POST.get('input', '')
    if input_text:
        #result = WebPageIndex.search().query(Q('match', title=input_text) | Q('match', content=input_text))
        # url_match = WebPage.objects.filter(url=input_text)[0:]
        # content_match = WebPage.objects.filter(content=input_text)[0:]
        vector = SearchVector('url') + SearchVector('content')
        query = SearchQuery(input_text)
        result = WebPage.objects.annotate(rank=SearchRank(vector, query))
    else:
        result = WebPage.objects.all()
    return render(request, 'index.html', {'result': result})


def start_crawler(request):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #subprocess.Popen('python3.6 pageRank.py', cwd=dir_path, shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # os.system("python3.6 pageRank.py")
    rank_func()
    bulk_indexing()
    return redirect(index)
