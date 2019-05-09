from django.db import models


class WebPage(models.Model):
    url = models.URLField()
