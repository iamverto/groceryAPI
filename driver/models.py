from django.db import models
from accounts.models import User


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
