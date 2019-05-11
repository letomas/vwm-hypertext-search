from django.shortcuts import render, redirect
from elasticsearch_dsl.query import Q
from .pageRank import start_ranking
from .search import WebPageIndex, bulk_indexing


def index(request):
    input_text = request.POST.get('input', '')
    if input_text:
        result = WebPageIndex.search().query(Q('match', title=input_text) | Q('match', content=input_text))
    else:
        result = ''
    return render(request, 'index.html', {'result': result})


def start_crawler(request):
    start_ranking()
    bulk_indexing()
    return redirect(index)
