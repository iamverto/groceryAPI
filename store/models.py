from django.db import models
from accounts.models import User
from address.models import Address
from category.models import Category


class Store(models.Model):
    name = models.CharField(max_length=128)
    about = models.TextField()
    owner = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    icon = models.ImageField(upload_to='store/icons', blank=True, null=True)
    banner = models.ImageField(upload_to='store/banners', blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    num_sales = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='stores', blank=True)





    def __str__(self):
        return self.name

    # OWNER CHANGE NOT ALLOWED
