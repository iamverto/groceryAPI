from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from product.models import Product, ProductImage
from .serializers import ProductSerializer
from rest_framework import filters


class ProductListCreateAPIView(ListAPIView, ListModelMixin):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'is_active']

    def get_queryset(self):
        """ Filters : STORE|CATEGORY """
        queryset = Product.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)


class ProductRetrieveUpdateDeleteAPIView(RetrieveAPIView, RetrieveModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)
