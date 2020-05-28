from django.db import models
from driver.models import Driver


class Shipping(models.Model):

    STATUS_CHOICES = (
        ("PENDING", 'Pending'),
        ("ACCEPTED", 'Accepted'),
        ("DECLINED", 'Declined'),
        ("PICKED", 'Picked/Shipped'),
        ("OUT_OF_DELIVERY", 'Out Of Delivery'),
        ("DELIVERED", 'Delivered'),
        ("FAILED", 'Failed')
    )

    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="PENDING")
