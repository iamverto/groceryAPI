from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=128)
    about = models.TextField()
    mobile = models.CharField(max_length=12)
    password = models.CharField(max_length=512)
    icon = models.ImageField(upload_to='store/icons')
    banner = models.ImageField(upload_to='store/banners')
    # address

