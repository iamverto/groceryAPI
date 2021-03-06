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
        5. delete cart items
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
            print('not an address!')
            return False
        # DELETING ANY PENDING ORDERS
        print('dd')
        orders = Order.objects.filter(user=self.user, status="PENDING").delete()
        print(items)
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

    def add_to_cart(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
        except CartItem.MultipleObjectsReturned:
            cart_items = CartItem.objects.filter(cart=self, product=product)
            cart_items.delete()
            cart_item = None
        except CartItem.DoesNotExist:
            cart_item = None
        if cart_item is not None:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem(cart=self, product=product)
            cart_item.save()
        return cart_item

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.delete()
            return
        super(CartItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.cart.user.mobile + " [ " + self.product.title + " ] "
