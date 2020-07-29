from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CartItemSerializer
from cart.models import Cart, CartItem
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from product.models import Product
from django.shortcuts import get_object_or_404



class CartItemListCreateAPIView(ListAPIView, ListModelMixin):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.filter(cart__user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product', None)
    product = get_object_or_404(Product, id=product_id)
    ci = request.user.cart.add_to_cart(product)
    serializer = CartItemSerializer(ci, context={'request':request})
    return Response(serializer.data, status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request):
    cart_item_id = request.data.get('cart_item', None)
    quantity = request.data.get('quantity', None)
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity = quantity
    cart_item.save()
    serializer = CartItemSerializer(cart_item, context={'request':request})
    return Response(serializer.data, status.HTTP_200_OK)

"""
UPDATE CartItem quantity
DELETE CartItem
Checkout
"""
