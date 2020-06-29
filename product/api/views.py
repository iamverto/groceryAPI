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
    ordering_fields = ['price', 'is_active', 'num_sales']

    def get_queryset(self):
        """ Filters : STORE|CATEGORY """
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        store = self.request.query_params.get('store', None)
        is_active = self.request.query_params.get('is_active', None)

        if category:
            queryset = queryset.filter(categories__in=category)
        if store:
            queryset = queryset.filter(store=store)
        if is_active:
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)


class ProductRetrieveUpdateDeleteAPIView(RetrieveAPIView, RetrieveModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)
