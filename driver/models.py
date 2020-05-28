from django.db import models


class Driver(models.Model):
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=12)
    password = models.CharField(max_length=512)
