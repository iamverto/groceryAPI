from django.db import models


class Address(models.Model):
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    street = models.TextField(blank=True, null=True)
