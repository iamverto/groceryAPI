from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from .serializers import OrderSerializer
from order.models import Order
from cart.models import Cart
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import filters


class OrderList(ListAPIView, ListModelMixin):
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']

    def get_queryset(self):
        """ADMIN CAN SEE ALL, STORE/USER CAN SEE THEIRs"""
        # for store show theirs, for drivers show theirs and also accepted orders
        status = self.request.query_params.get('status', None)  # anybody
        store = self.request.query_params.get('store', None)
        driver = self.request.query_params.get('driver', None)
        mode = self.request.query_params.get('mode', None)

        if self.request.user.is_superuser and mode=='admin':
            queryset = Order.objects.all()
        # for drivers | their + accepted orders by store and not having any driver
        # for stores | their
        else:
            queryset = Order.objects.filter(user=self.request.user)


        if status:
            queryset = queryset.filter(status=status)
        if store:
            queryset = queryset.filter(store=store)
        if driver:
            queryset = queryset.filter(driver=driver)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)

class OrderDetail(RetrieveAPIView, RetrieveModelMixin):
    serializer_class = OrderSerializer
    lookup_field = 'id'
    def get_queryset(self):
        mode = self.request.query_params.get('mode', None)
        if self.request.user.is_superuser and mode=='admin':
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(user=self.request.user)
        return queryset

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