from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection()


class WebPageIndex(DocType):
    url = Text()
    content = Text()

    class Meta:
        index = 'webpage-index'


def bulk_indexing():
    WebPageIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.WebPage.objects.all().iterator()))
