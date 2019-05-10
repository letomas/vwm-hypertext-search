from django.db import models
from .search import WebPageIndex


class WebPage(models.Model):
    url = models.URLField()
    content = models.TextField()
    rank = models.FloatField()

    def indexing(self):
        obj = WebPageIndex(
            meta={'id': self.id},
            url=self.url,
            content=self.content
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    def __str__(self):
        return self.url()
