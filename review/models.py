from django.db import models
from accounts.models import User
from product.models import Product


class Review(models.Model):
    """
    PRODUCT RATINGS
    user can only review a product single time.

    """
    RATING_CHOICES = (
        (1, 'One Star'),
        (2, 'Two Star'),
        (3, 'Three Star'),
        (4, 'Four Star'),
        (5, 'Five Star'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_date = models.DateTimeField(auto_now=True)

