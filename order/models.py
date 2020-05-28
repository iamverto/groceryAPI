from django.db import models
from product.models import Product
from address.models import Address
from shipping.models import Shipping
from accounts.models import User
from store.models import Store
"""
GROUPING ORDER ITEMS BY STORE AND KEEPING IT SEPARATE ORDER
"""


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    # payment


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)
