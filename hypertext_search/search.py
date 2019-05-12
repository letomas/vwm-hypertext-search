from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, analyzer, tokenizer, Keyword, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection()

html_strip = analyzer('html_strip',
                      tokenizer="uax_url_email",
                      filter=["lowercase"],
                      char_filter=["html_strip"])


class WebPageIndex(DocType):
    url = Keyword()
    content = Text()

    class Meta:
        index = 'webpage-index'


def bulk_indexing():
    es = Elasticsearch()
    WebPageIndex.init()
    es.indices.delete(index='webpage-index', ignore=[400, 404])
    bulk(client=es, actions=(b.indexing() for b in models.WebPage.objects.all().iterator()))

