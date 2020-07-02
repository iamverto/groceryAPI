from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from .serializers import OrderSerializer
from order.models import Order
from cart.models import Cart
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.shortcuts import get_object_or_404


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
        open_order_for_drivers = self.request.query_params.get('open_order_for_drivers', None)

        if self.request.user.is_superuser and mode == 'admin':
            queryset = Order.objects.all()

        # for drivers | their + accepted orders by store and not having any driver
        elif self.request.user.is_driver() and mode == 'driver':
            # open orders will shown to drivers once the store has been accepted.
            if open_order_for_drivers:
                queryset = Order.objects.filter(status="ACCEPTED", driver=None)
            else:
                queryset = Order.objects.filter(driver=self.request.user.driver)

        elif self.request.user.is_store() and mode == 'store':
            queryset = Order.objects.filter(store=self.request.user.store)

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

        if self.request.user.is_superuser and mode == 'admin':
            queryset = Order.objects.all()
        elif self.request.user.is_driver() and mode == 'driver':
            queryset = Order.objects.all()
        elif self.request.user.is_store() and mode == 'store':
            queryset = Order.objects.filter(store=self.request.user.store)
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
    return Response({"err": 'Please provide address!'}, status=status.HTTP_400_BAD_REQUEST)


# accept order by store
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_order_by_store(request, id):
    # check if user is a store owner
    order = get_object_or_404(Order, id=id)
    if request.user.is_store() and order.store.owner == request.user:
        order.status = "ACCEPTED"
        order.save()
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


# decline order by store
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_order_by_store(request, id):
    order = get_object_or_404(Order, id=id)
    if request.user.is_store() and order.store.owner == request.user:
        order.status = "DECLINED"
        order.save()
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


# accept order delivery boy
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_order_by_driver(request, id):
    order = get_object_or_404(Order, id=id)
    if request.user.is_driver() and order.status=="ACCEPTED":
        order.status = "READY"
        order.driver = request.user.driver
        order.save()
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


# deliver order by delivery boy
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deliver_order_by_driver(request, id):
    order = get_object_or_404(Order, id=id)
    if request.user.is_driver() and order.driver==request.user.driver:
        order.status = "DELIVERED"
        order.save()
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

# decline order delivery boy
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_order_by_driver(request, id):
    order = get_object_or_404(Order, id=id)
    if request.user.is_driver() and order.driver==request.user.driver:
        order.status = "DECLINED"
        order.save()
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
