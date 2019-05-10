from django.shortcuts import render, redirect
from .models import WebPage
from .pageRank import start_ranking



def index(request):
    # all_matching_urls = WebPage.objects.all()
    input_text = request.POST.get('input', '')

    return render(request, 'index.html', {'test_input': input_text})


def start_crawler(request):
    start_ranking()
    return redirect(index)
