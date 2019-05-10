from django.urls import path
from .views import index, start_crawler

urlpatterns = [
    path('', index),
    path('crawl/', start_crawler),
]

