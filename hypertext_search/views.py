from django.shortcuts import render, redirect
from elasticsearch_dsl.query import Q
from .models import WebPage
from .pageRank import rank_func
from .search import WebPageIndex, bulk_indexing
from .constants import SEARCH_WEIGHT, PAGE_RANK_WEIGHT
import http.client
http.client._MAXHEADERS = 10000


def index(request):
    input_text = request.POST.get('input', '')
    if input_text:
        s = WebPageIndex.search().query(Q('match', content=input_text))
        result = s.execute()
        i = 0
        for page in result:
            page.score = SEARCH_WEIGHT * result.hits[i].meta.score + PAGE_RANK_WEIGHT * page.web_rank
            i += 1
    else:
        result = ''
    return render(request, 'index.html', {'result': result})


def get_all(request):
    result = WebPage.objects.all()[0:]
    return render(request, 'index.html', {'result': result})


def start_crawler(request):
    rank_func()
    return redirect(index)


def bulk_index(request):
    bulk_indexing()
    return redirect(index)

