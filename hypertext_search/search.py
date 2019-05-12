from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Float
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection()


class WebPageIndex(DocType):
    url = Text()
    content = Text()
    web_rank = Float()

    class Meta:
        index = 'webpage-index'


def bulk_indexing():
    es = Elasticsearch()
    es.indices.delete(index='webpage-index', ignore=[400, 404])
    WebPageIndex.init()
    bulk(client=es, actions=(b.indexing() for b in models.WebPage.objects.all().iterator()))

