from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin,RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status
from .serializers import StoreSerializer
from store.models import Store
from rest_framework import filters
from accounts.models import User
from address.models import Address


class StoreList(ListCreateAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = StoreSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'about']
    ordering_fields = ['num_sales']

    def get_queryset(self):
        queryset = Store.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(categories__in=category)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)

    # admin create a store
    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            # mobile number > create user > then create store [ I'm using perform_create]
            return self.create(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        mobile = self.request.data.get('mobile', None)
        if mobile:
            try:
                user = User.objects.get(mobile=mobile)
            except User.DoesNotExist:
                temp_email = "doorpay987654321@doorpay.com"
                user = User(mobile=mobile, email=temp_email, username=mobile, password="nc9ehr4cx3cxf3y4nc3r")
                user.save()
            return serializer.save(owner=user)


class StoreDetail(RetrieveUpdateDestroyAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = StoreSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Store.objects.all()
        return queryset

    def put(self, request, *args, **kwargs):
        pass
    def patch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.partial_update(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def perform_update(self, serializer):
        print(self.request.data)
        instance = self.get_object()
        if self.request.data.get('categories', None):
            categories = self.request.data.copy().pop('categories')
            if categories:
                instance.categories.clear()
                for category in categories:
                    instance.categories.add(category)

        # todo update (create if not available) address [city, pincode, street, lat, lng]
        city = self.request.data.get('city', None)
        pincode = self.request.data.get('pincode', None)
        street = self.request.data.get('street', None)

        # todo PROBLEM : Address is not saving.
        if city or pincode or street:
            print('hi')
            if instance.address:
                address = instance.address
                print('hii2')
            else:
                address = Address(city=city, pincode=pincode, street=street)
                address.save()
                instance.address = address
        instance.save()
        print(instance.address)

        serializer.save()

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.destroy(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



