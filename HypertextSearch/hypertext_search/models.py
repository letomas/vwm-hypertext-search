from django.db import models


class WebPage(models.Model):
    url = models.URLField()
    content = models.TextField()

    def __str__(self):
        return self.url()
