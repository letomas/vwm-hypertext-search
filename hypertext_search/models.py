from django.db import models
from .search import WebPageIndex


class WebPage(models.Model):
    url = models.URLField()
    web_rank = models.FloatField(null=True, blank=True, default=0)
    content = models.TextField()

    def indexing(self):
        obj = WebPageIndex(
            meta={'id': self.id},
            url=self.url,
            content=self.content,
            web_rank=self.web_rank
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    def __str__(self):
        return self.url()
