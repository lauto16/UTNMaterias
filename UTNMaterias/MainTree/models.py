from django.db import models


class UTNSubject(models.Model):
    name = models.CharField(max_length=100)
    approval_fathers = models.CharField(max_length=100, blank=True)
    approval_children = models.CharField(max_length=100, blank=True)
    regular_fathers = models.CharField(max_length=100, blank=True)
    regular_children = models.CharField(max_length=100, blank=True)
    year = models.IntegerField()
