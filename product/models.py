import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

from store.models import Store
from category.models import Category


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    num_items = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='product_images/')
    is_featured = models.BooleanField(default=False)


@receiver(post_delete, sender=ProductImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """ Deletes file from filesystem when corresponding `ProductImage` object is deleted. """

    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

