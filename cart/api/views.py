from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from .serializers import CartItemSerializer
from cart.models import Cart, CartItem


class CartItemListCreateAPIView(ListAPIView, ListModelMixin):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.filter(cart__user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)


"""
UPDATE CartItem quantity
DELETE CartItem
Checkout
"""
