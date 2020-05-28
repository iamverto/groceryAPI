from django.db import models
from django.contrib.auth.models import AbstractUser
from category.models import Category


class User(AbstractUser):
    mobile = models.CharField(max_length=100)
    key = models.CharField(max_length=500)
    addresses = models.ManyToManyField(Category, blank=True)
