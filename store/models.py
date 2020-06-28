from django.db import models
from accounts.models import User
from address.models import Address


class Store(models.Model):
    name = models.CharField(max_length=128)
    about = models.TextField()
    owner = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    icon = models.ImageField(upload_to='store/icons')
    banner = models.ImageField(upload_to='store/banners')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
