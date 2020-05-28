from django.db import models


class Address(models.Model):
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    street = models.TextField()
