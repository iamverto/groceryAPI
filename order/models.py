from django.db import models
from product.models import Product
from address.models import Address
from driver.models import Driver
from accounts.models import User
from store.models import Store
"""
GROUPING ORDER ITEMS BY STORE AND KEEPING IT SEPARATE ORDER
"""


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING','Pending'),
        ('SUCCESS','Success'),
        ('ACCEPTED','Accepted'),
        ('SHIPPED','Shipped'),
        ('DELIVERED','Delivered'),
        ('DECLINED','Declined'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default="PENDING", max_length=50)
    # payment

    def save(self, *args, **kwargs):
        if self.status == "PENDING":
            order_items = self.items.all()
            amount = 0
            for item in order_items:
                amount += item.amount
            self.amount = amount
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return "Order ID #" + str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def save(self, *args, **kwargs):
        """settings amount based on product on each time order_time update"""
        self.amount = self.product.price*self.quantity
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.title + " in  " + self.order.__str__()