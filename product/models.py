import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

from store.models import Store
from category.models import Category


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    is_active = models.BooleanField(default=True)
    num_sales = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_store_name(self):
        return self.store.name

    def get_featured_image(self):
        featured_image = self.images.filter(is_featured=True).first()
        if featured_image:
            return featured_image.pic.url
        return None





class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='product/')
    is_featured = models.BooleanField(default=False)



@receiver(post_delete, sender=ProductImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """ Deletes pic from filesystem when corresponding `ProductImage` object is deleted. """

    if instance.pic:
        if os.path.isfile(instance.pic.path):
            os.remove(instance.pic.path)
