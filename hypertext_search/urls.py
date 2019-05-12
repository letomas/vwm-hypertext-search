from django.urls import path
from .views import index, start_crawler, bulk_index, get_all

urlpatterns = [
    path('', index),
    path('crawl/', start_crawler),
    path('bulk/', bulk_index),
    path('all/', get_all)
]

