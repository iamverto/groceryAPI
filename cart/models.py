from django.db import models
from accounts.models import User
from product.models import Product
from address.models import Address
from order.models import Order, OrderItem


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.mobile

    def place_order(self, address_id):
        """
        1. check if all items is available
        2. check if address is right
        3. delete previous pending orders
        4. then => create order and order_items
        todo delete cart items
        """
        items = self.items.all()
        for item in items:
            if item.product.is_active:
                pass
            else:
                return False
        try:
            address = self.user.addresses.get(id=address_id)
        except Address.DoesNotExist:
            return False
        # DELETING ANY PENDING ORDERS
        orders = Order.objects.filter(user=self.user, status="PENDING").delete()

        # PLACING ORDER and GROUPING
        for item in items:
            store = item.product.store
            amount = item.product.price * item.quantity
            try:
                order = Order.objects.get(store=store,user=self.user, status="PENDING")
            except Order.DoesNotExist:
                order = Order(store=store, user=self.user, status="PENDING", amount=0, address=address)
                order.save()
            order_item = OrderItem(order=order, product=item.product, quantity=item.quantity, amount=amount)
            order_item.save()
            # here is important to save order [to make sure amount will be added correctly to order object!]
            order.save()
        orders = Order.objects.filter(user=self.user, status="PENDING")

        items.delete()
        return orders.update(status="SUCCESS")

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.delete()
            return
        super(CartItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.cart.user.mobile + " [ " + self.product.title + " ] "
