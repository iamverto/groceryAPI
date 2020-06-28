from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from .serializers import OrderSerializer
from order.models import Order
from cart.models import Cart
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


class OrderList(ListAPIView, ListModelMixin):
    serializer_class = OrderSerializer

    def get_queryset(self):
        """TODO ADMIN CAN SEE ALL, STORE/USER CAN SEE THEIRs"""
        queryset = Order.objects.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)

@api_view(['POST'])
def place_order(request):
    address_id = request.data.get('address', None)
    print(address_id)
    if address_id:
        cart = request.user.cart
        orders = cart.place_order(address_id)
        if orders:
            return Response(status.HTTP_201_CREATED)
        else:
            return Response({"err": 'Looks like some products are not available!'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"err":'Please provide address!'},status=status.HTTP_400_BAD_REQUEST)