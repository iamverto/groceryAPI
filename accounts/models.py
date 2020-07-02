import pyotp
from django.db import models
from django.contrib.auth.models import AbstractUser
from address.models import Address

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# USERNAME AND MOBILE WILL BE SAME
class User(AbstractUser):
    fullname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    key = models.CharField(max_length=500, blank=True)
    addresses = models.ManyToManyField(Address, related_name='users', blank=True)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def is_driver(self):
        return self.driver

    def is_store(self):
        return self.store


def generate_key():
    """ User otp key generator """
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    generate_key()


def is_unique(key):
    try:
        User.objects.get(key=key)
    except User.DoesNotExist:
        return True
    return False


@receiver(pre_save, sender=User)
def create_key(sender, instance, **kwargs):
    """This creates the key for users that don't have keys"""
    print("KEY GENERATED")
    if not instance.key:
        instance.key = generate_key()


@receiver(post_save, sender=User)
def create_cart(sender, instance, **kwargs):
    """Creating cart after register"""
    from cart.models import Cart
    try:
        Cart.objects.get(user=instance)
    except Cart.DoesNotExist:
        cart = Cart(user=instance)
        cart.save()


"""
@TODO IS CART CREATED ON USER CREATION?
"""
